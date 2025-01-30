# langchain-github-copilot

This package contains the LangChain integration with GithubCopilot

## Installation

```bash
pip install -U langchain-github-copilot
```

And you should configure credentials by setting the following environment variables:

`GITHUB_TOKEN`

<details>
<summary>How to get a Github Token?</summary>
Use the following function to set up your Github Token as an environment variable.

```python
import requests, os, time

def setup():
    resp = requests.post('https://github.com/login/device/code', headers={
            'accept': 'application/json',
            'editor-version': 'Neovim/0.6.1',
            'editor-plugin-version': 'copilot.vim/1.16.0',
            'content-type': 'application/json',
            'user-agent': 'GithubCopilot/1.155.0',
            'accept-encoding': 'gzip,deflate,br'
        }, data='{"client_id":"Iv1.b507a08c87ecfe98","scope":"read:user"}')


    # Parse the response json, isolating the device_code, user_code, and verification_uri
    resp_json = resp.json()
    device_code = resp_json.get('device_code')
    user_code = resp_json.get('user_code')
    verification_uri = resp_json.get('verification_uri')

    # Print the user code and verification uri
    print(f'Please visit {verification_uri} and enter code {user_code} to authenticate.')


    while True:
        time.sleep(5)
        resp = requests.post('https://github.com/login/oauth/access_token', headers={
            'accept': 'application/json',
            'editor-version': 'Neovim/0.6.1',
            'editor-plugin-version': 'copilot.vim/1.16.0',
            'content-type': 'application/json',
            'user-agent': 'GithubCopilot/1.155.0',
            'accept-encoding': 'gzip,deflate,br'
            }, data=f'{{"client_id":"Iv1.b507a08c87ecfe98","device_code":"{device_code}","grant_type":"urn:ietf:params:oauth:grant-type:device_code"}}')

        # Parse the response json, isolating the access_token
        resp_json = resp.json()
        access_token = resp_json.get('access_token')

        if access_token:
            break
        
    with open('.env', 'a') as f:
        f.write(f'GITHUB_TOKEN={access_token}\n')

    print('Authentication success!')
```
</details>

## Chat Models

`ChatGithubCopilot` class exposes chat models from GithubCopilot.

```python
from langchain_github_copilot import ChatGithubCopilot

llm = ChatGithubCopilot()
llm.invoke("Sing a ballad of LangChain.")
```

