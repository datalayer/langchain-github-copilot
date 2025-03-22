[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🦜🔗 ✨ LangChain GitHub Copilot

This package contains the LangChain integration with GitHub Copilot.

```bash
In [3]: from langchain_github_copilot import ChatGitHubCopilot
   ...: 
   ...: llm = ChatGitHubCopilot()
   ...: llm.invoke("Sing a ballad of GitHub and LangChain.")
   ...: 
Out[3]: AIMessage(content="(Verse 1)\nIn the realm of code and dreams untold,\nWhere developers brave and bold,\nThere lies a haven, vast and wide,\nGitHub, where our projects reside.\n\n(Chorus)\nOh, GitHub and LangChain, together they stand,\nGuiding the coder's hand,\nIn the world of AI, they light the way,\nBuilding tomorrow, code by code each day.\n\n(Verse 2)\nLangChain, with its wisdom deep,\nIn the language of machines, it speaks,\nFrom data's whispers to insights grand,\nIt crafts the future, hand in hand.\n\n(Chorus)\nOh, GitHub and LangChain, together they stand,\nGuiding the coder's hand,\nIn the world of AI, they light the way,\nBuilding tomorrow, code by code each day.\n\n(Bridge)\nRepositories like stars in the night,\nForks and pulls, a developer's delight,\nCollaborations that span the globe,\nIn this digital world, our skills we hone.\n\n(Verse 3)\nWith every commit and every merge,\nWe ride the innovation surge,\nLangChain's power, GitHub's grace,\nTogether they conquer time and space.\n\n(Chorus)\nOh, GitHub and LangChain, together they stand,\nGuiding the coder's hand,\nIn the world of AI, they light the way,\nBuilding tomorrow, code by code each day.\n\n(Outro)\nSo here's to the coders, near and far,\nOn GitHub's platform, like a guiding star,\nWith LangChain's brilliance, we pave the lane,\nFor a future bright, in code's domain.", additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 324, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens': 18, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}, 'total_tokens': 342}, 'model_name': 'gpt-4o-2024-05-13', 'system_fingerprint': 'fp_ded0d14823', 'finish_reason': 'stop'}, id='run-e9f5530d-8918-451d-8e94-baaeab92552b-0', usage_metadata={'input_tokens': 18, 'output_tokens': 324, 'total_tokens': 342, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})
```

## Installation

```bash
pip install -U langchain-github-copilot
```

## GitHub Token

You should configure credentials by setting the `GITHUB_TOKEN` environment variables.

<details>
<summary>How to get a GitHub Token?</summary>

Run the `setup.py` python script to create a `.env` file with the GitHub Token.

> IMPORTANT
>  
> The GitHub Token generated expires after 25 minutes. We are currently working on a solution to refresh the token automatically. If needed, rerun the setup.py script to generate a new token.

```bash
python setup.py
```

Ressources used to understand how to generate a GitHub Token:

- https://github.com/B00TK1D/copilot-api
- https://thakkarparth007.github.io/copilot-explorer/posts/copilot-internals.html

</details>

## Use with Chat Models

```python
from langchain_github_copilot import ChatGitHubCopilot

llm = ChatGitHubCopilot()
llm.invoke("Sing a ballad of GitHub and LangChain.")
```
