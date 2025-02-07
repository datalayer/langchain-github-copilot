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

```bash
python setup.py
```
</details>

## Chat Models

`ChatGithubCopilot` class exposes chat models from GithubCopilot.

```python
from langchain_github_copilot import ChatGithubCopilot

llm = ChatGithubCopilot()
llm.invoke("Sing a ballad of LangChain.")
```

