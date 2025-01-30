"""Test ChatGithubCopilot chat model."""

from typing import Type

from langchain_tests.integration_tests import ChatModelIntegrationTests

from langchain_github_copilot.chat_models import ChatGithubCopilot


class TestChatGithubCopilotIntegration(ChatModelIntegrationTests):
    @property
    def chat_model_class(self) -> Type[ChatGithubCopilot]:
        return ChatGithubCopilot

    @property
    def chat_model_params(self) -> dict:
        # These should be parameters used to initialize your integration for testing
        return {
            "model": "copilot-001",
            "temperature": 0,
        }
