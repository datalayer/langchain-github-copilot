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

Run the setup.py python script to create a .env file with the Github Token.


> IMPORTANT
>  
> The Github Token generated expires after 25 minutes. We are currently working on a solution to refresh the token automatically. If needed, rerun the setup.py script to generate a new token.

```bash
python setup.py
```

Ressources used to understand how to generate a Github Token:
- https://github.com/B00TK1D/copilot-api
- https://thakkarparth007.github.io/copilot-explorer/posts/copilot-internals.html

</details>

## Chat Models

`ChatGithubCopilot` class exposes chat models from GithubCopilot.

```python
from langchain_github_copilot import ChatGithubCopilot

llm = ChatGithubCopilot()
llm.invoke("Sing a ballad of LangChain.")
```

