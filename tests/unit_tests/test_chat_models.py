"""Test chat model integration."""

from typing import Type

from langchain_tests.unit_tests import ChatModelUnitTests

from langchain_github_copilot.chat_models import ChatGithubCopilot


class TestChatGithubCopilotUnit(ChatModelUnitTests):
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
