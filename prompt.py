# Copyright (c) 2024-2025 Datalayer, Inc.
#
# MIT License
 
from langchain_github_copilot import ChatGitHubCopilot

llm = ChatGitHubCopilot()

response = llm.invoke("Sing a ballad of GitHub and LangChain.")

print(response)

# print(response["content"])
# print(response["response_metadata"])

