import requests
import time

GITHUB_CLIENT_ID = "Iv1.b507a08c87ecfe98"
HEADERS = {
    'accept': 'application/json',
    'editor-version': 'Neovim/0.6.1',
    'editor-plugin-version': 'copilot.vim/1.16.0',
    'content-type': 'application/json',
    'user-agent': 'GitHubCopilot/1.155.0',
    'accept-encoding': 'gzip,deflate,br'
}

def setup():
    access_token = get_access_token()
    token = get_token(access_token)
    
    with open('.env', 'a') as f:
        f.write(f'\nGITHUB_TOKEN="{token}"\n')

    print('Authentication success!')

def get_token(access_token):
    response = requests.get(
        'https://api.github.com/copilot_internal/v2/token',
        headers={**HEADERS, 'authorization': f'token {access_token}'}
    )
    response.raise_for_status()
    return response.json().get('token')

def get_access_token():
    response = requests.post(
        'https://github.com/login/device/code',
        headers=HEADERS,
        json={'client_id': GITHUB_CLIENT_ID, 'scope': 'read:user'}
    )
    response.raise_for_status()
    data = response.json()
    device_code = data.get('device_code')
    user_code = data.get('user_code')
    verification_uri = data.get('verification_uri')

    print(f'Please visit {verification_uri} and enter code {user_code} to authenticate.')

    while True:
        time.sleep(5)
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            headers=HEADERS,
            json={
                'client_id': GITHUB_CLIENT_ID,
                'device_code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            }
        )
        response.raise_for_status()
        access_token = response.json().get('access_token')
        if access_token:
            return access_token

if __name__ == '__main__':
    setup()
