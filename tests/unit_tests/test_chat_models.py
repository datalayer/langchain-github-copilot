# Copyright (c) 2024-2025 Datalayer, Inc.
#
# MIT License

"""Test chat model integration."""

from typing import Type

from langchain_tests.unit_tests import ChatModelUnitTests

from langchain_github_copilot.chat_models import ChatGitHubCopilot


class TestChatGitHubCopilotUnit(ChatModelUnitTests):
    @property
    def chat_model_class(self) -> Type[ChatGitHubCopilot]:
        return ChatGitHubCopilot

    @property
    def chat_model_params(self) -> dict:
        # These should be parameters used to initialize your integration for testing
        return {
            "model": "copilot-001",
            "temperature": 0,
        }
