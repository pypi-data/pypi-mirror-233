import json
import requests
import re
import os
import configparser
from support_toolbox.utils.dataset import create_dataset
from support_toolbox.utils.helper import PRIVATE_API_URLS
from support_toolbox.utils.user import get_agent_id
from support_toolbox.deploy_browse_card import deploy_browse_card
from support_toolbox.deploy_integrations import deploy_integrations
from support_toolbox.utils.org import onboard_org, authorize_access_to_org, deauthorize_access_to_org, validate_org_input
from support_toolbox.deploy_ctk import deploy_ctk, CTK_STACK
from support_toolbox.utils.entitlements import update_org_entitlements, get_entitlements, get_default_values, update_default_plan, ORG_DEFAULT_ENTITLEMENTS, USER_DEFAULT_ENTITLEMENTS
from support_toolbox.utils.site import create_site, SAML_PLACEHOLDER, DEFAULT_ORGS
from support_toolbox.utils.service_account import create_service_account, create_env_variable, SERVICE_ACCOUNTS, CIRCLECI_PROJECTS


# Get the path to the user's home directory
user_home = os.path.expanduser("~")

# Construct the full path to the configuration file
tokens_file_path = os.path.join(user_home, ".tokens.ini")

# Initialize the configparser and read the tokens configuration file
config = configparser.ConfigParser()
config.read(tokens_file_path)

# Read tokens/variables for the deploy_service_accounts tool
circleci_api_token = config['deploy_pi']['CIRCLECI_API_TOKEN']


def sanitize_public_slug(slug):
    # Convert to lowercase
    slug = slug.lower()

    # Remove spaces, symbols, and numbers
    slug = re.sub(r'[^a-z]+', '', slug)

    return slug


def config_site(admin_token):
    # Update the orgs that are created by default with the necessary Org Default Entitlements
    for org_id in DEFAULT_ORGS:
        source = get_entitlements(admin_token, org_id)
        order = 1
        for name, product_id in ORG_DEFAULT_ENTITLEMENTS.items():
            update_org_entitlements(admin_token, org_id, product_id, order, source, name)
            order += 1

    # Update Org Default Plan with the necessary ORG_DEFAULT_ENTITLEMENTS
    org_values = get_default_values(admin_token, "organization")
    org_agent_type = org_values['agent_type']
    org_offering_slug = org_values['offering_slug']
    org_offering_id = org_values['offering_id']
    org_product_ids = org_values['product_ids']

    # Update Product IDs with the ORG_DEFAULT_ENTITLEMENTS
    for entitlement in ORG_DEFAULT_ENTITLEMENTS.values():
        org_product_ids.append(entitlement)
    update_default_plan(admin_token, org_offering_id, org_agent_type, org_offering_slug, org_product_ids)

    # Update User Default Plan with the necessary USER_DEFAULT_ENTITLEMENTS
    user_values = get_default_values(admin_token, "user")
    user_agent_type = user_values['agent_type']
    user_offering_slug = user_values['offering_slug']
    user_offering_id = user_values['offering_id']
    user_product_ids = user_values['product_ids']

    # Update Product IDs with the USER_DEFAULT_ENTITLEMENTS
    for entitlement in USER_DEFAULT_ENTITLEMENTS.values():
        user_product_ids.append(entitlement)
    update_default_plan(admin_token, user_offering_id, user_agent_type, user_offering_slug, user_product_ids)

    # Authorize 'datadotworldsupport' access to 'ddw'
    authorize_access_to_org(admin_token, 'ddw')


def deploy_metrics(admin_token, public_slug):
    # Ask user to select an option
    print("Before we continue, please select an option (1/2): ")
    print("1. Existing customer moving to a PI")
    print("2. New customer PI deployment")
    user_choice = input()

    # Set existing_customer based on user input
    if user_choice == "1":
        existing_customer = True
    elif user_choice == "2":
        existing_customer = False
    else:
        print("Invalid selection.")
        return

    metrics_deployment_choice = input("Start metrics deployment? (y/n): ")

    if metrics_deployment_choice.lower() == 'y':
        org_id = "data-catalog-team"
        org_display_name = "Data Catalog Team"

        standard_org_choice = input("Use the standard Data Catalog Team org (y/n): ")

        if standard_org_choice.lower() == 'n':
            org_id = input("Enter the org id: ")
            org_display_name = input("Enter the org display name: ")

        print(f"Onboarding {org_id}...")
        onboard_org(admin_token, org_id, org_display_name)

        print(f"Authorizing datadotworldsupport access to {org_id}...")
        authorize_access_to_org(admin_token, org_id)

        if existing_customer:
            # Create ddw-metrics-{public_slug} dataset
            create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}", visibility="PRIVATE")
            public_slug = public_slug + "_PI"

        else:
            all_time_metrics_choice = input("Is the customer paying for the 'All-time' metrics upgrade (y/n): ")

            if all_time_metrics_choice.lower() == 'y':
                # Create ddw-metrics-{public_slug} dataset
                create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}", visibility="PRIVATE")
            else:
                # Create ddw-metrics-{public_slug}-last-90-days dataset
                create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}-last-90-days", visibility="PRIVATE")

        # Create the baseplatformdata dataset
        create_dataset(admin_token, org_id, dataset_id="baseplatformdata", visibility="PRIVATE")
        return public_slug, org_id

    else:
        metrics_continue_choice = input("Do you want to continue without completing the metrics setup?\n"
                                        "We will skip creating the necessary org and datasets for metric deployment (y/n): ")

        if metrics_continue_choice.lower() == 'n':
            # Restart the metrics deployment process
            deploy_metrics(admin_token, public_slug)
        else:
            print("Continuing without metrics setup...")


def deploy_service_accounts(api_token, site_slug, circleci_api_token):
    for i, sa in enumerate(SERVICE_ACCOUNTS):
        token = create_service_account(api_token, sa)

        # Configure parameters for CircleCI API
        circleci_project = CIRCLECI_PROJECTS[i]
        name = site_slug.upper() + "_API_TOKEN"

        create_env_variable(circleci_project, name, token, circleci_api_token=circleci_api_token)


def cleanup_site_creation(admin_token, metrics_org=''):
    agent_id = get_agent_id(admin_token)
    print(f"Cleaning up any resources {agent_id} is in...")

    for org_id in DEFAULT_ORGS:
        if org_id == 'datadotworldsupport':
            continue
        deauthorize_access_to_org(admin_token, agent_id, org_id)

    deauthorize_access_to_org(admin_token, agent_id, metrics_org)


def run():
    api_url = PRIVATE_API_URLS['MT/PI']

    while True:
        user_input = input("Enter the URL slug: ")
        public_slug = sanitize_public_slug(user_input)

        if not public_slug:
            print("Invalid slug. Please enter a valid URL slug.")
            continue

        preview_url = f"https://{public_slug}.app.data.world"
        selection = input(f"Here is a preview of the URL: {preview_url}\nDoes this look correct? (y/n): ")

        if selection == 'y':
            saml_choice = input("Do you want to use placeholder values for SAML? (y/n): ")
            if saml_choice == 'y':
                entity_id = SAML_PLACEHOLDER['entity_id']
                sso_url = SAML_PLACEHOLDER['sso_url']
                x509_cert = SAML_PLACEHOLDER['x509_cert']

            else:
                sso_url = input("Enter the SSO URL: ")
                entity_id = input("Enter the Entity ID: ")
                x509_cert = input("Enter the X.509 Certificate: ")

            # Final verification before creating site
            print(f"\n{preview_url} will deploy with the following SAML values")
            print(f"SSO URL: {sso_url}")
            print(f"ENTITY ID: {entity_id}")
            print(f"x509 CERTIFICATE: {x509_cert}")

            # Create site
            admin_token = input("Enter your active admin token for the community site: ")
            create_site(admin_token, entity_id, public_slug, sso_url, x509_cert, api_url)

            # Get the users active admin_token to complete the deployment using Private APIs
            admin_token = input(f"Enter your active admin token for the {public_slug} site: ")

            # Configure site with default entitlements, update org entitlements, update permissions
            config_site(admin_token)

            # Deploy CTK using the entered 'main' org as the Display Name
            while True:
                main_display_name = input("What will the Display Name for the 'main' org be called? (CASE SENSITIVE): ")
                if validate_org_input(main_display_name):
                    CTK_STACK['main'] = main_display_name
                    break
                else:
                    print('Invalid organization name. Please try again.')
            deploy_ctk(admin_token)

            # Deploy Metrics and return the altered public_slug used to create service accounts
            public_slug, metrics_org = deploy_metrics(admin_token, public_slug)

            print("Deploying browse card...")
            deploy_browse_card(admin_token, 'n')

            print("Deploying integrations...")
            deploy_integrations(admin_token, '1')

            print("Deploying service accounts...")
            deploy_service_accounts(admin_token, public_slug, circleci_api_token)

            cleanup_site_creation(admin_token, metrics_org)
            break

        # URL Value denied
        elif selection == 'n':
            continue

        # URL Value invalid
        else:
            print("Enter a valid option: 'y'/'n'")
