from support_toolbox.utils.helper import PRIVATE_API_URLS
import requests


def get_agent_id(admin_token):
    get_user_url = f"{PRIVATE_API_URLS['MT/PI']}/user"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    response = requests.get(get_user_url, cookies=cookies, headers=header)

    # Verify the get
    if response.status_code == 200:
        response_json = response.json()
        agent_id = response_json['agentid']
        return agent_id
    else:
        print(response.text)
