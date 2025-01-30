"""GithubCopilot chat models."""

import os
import secrets
import requests
import uuid

from typing import Any, Dict, List, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field


API_ENDPOINT = "https://api.githubcopilot.com"

LGC_VERSION = "0.0.1"
EDITOR_VERSION = f"LangchainGithubCopilot/{LGC_VERSION}"
EDITOR_PLUGIN_VERSION = f"LangchainGithubCopilot/{LGC_VERSION}"
USER_AGENT = f"LangchainGithubCopilot/{LGC_VERSION}"
MACHINE_ID = secrets.token_hex(33)[0:65]

class ChatGithubCopilot(BaseChatModel):
    """GithubCopilot chat model integration.

    Setup:
        Install ``langchain-github-copilot`` and set environment variable ``GITHUB_TOKEN``.

        .. code-block:: bash

            pip install -U langchain-github-copilot
            export GITHUB_TOKEN="your-github-token"

    Key init args — completion params:
        model: str
            Name of GithubCopilot model to use.
        temperature: float
            Sampling temperature.
        max_tokens: Optional[int]
            Max number of tokens to generate.
        stop: Optional[List[str]]
            List of strings on which the model should stop generating.

    Key init args — client params:
        timeout: Optional[float]
            Timeout for requests.

    See full list of supported init args and their descriptions in the params section.

    Instantiate:
        .. code-block:: python

            from langchain_github_copilot import ChatGithubCopilot

            llm = ChatGithubCopilot(
                model="...",
                temperature=0,
                max_tokens=None,
                timeout=None,
                stop=["<END>"],
            )

    Invoke:
        .. code-block:: python

            messages = [
                ("system", "You are a helpful translator. Translate the user sentence to French."),
                ("human", "I love programming."),
            ]
            llm.invoke(messages)

        .. code-block:: python

            AIMessage(content="J'adore la programmation.", additional_kwargs={}, response_metadata={'model': 'gpt-3.5-turbo-0613'}, id='run-b1a6611c-b8f5-462d-a9fc-12bab50fd0c8-0', usage_metadata={'input_tokens': 31, 'output_tokens': 8, 'total_tokens': 39})

    Token usage:
        .. code-block:: python

            ai_msg = llm.invoke(messages)
            ai_msg.usage_metadata

        .. code-block:: python

            {'input_tokens': 31, 'output_tokens': 8, 'total_tokens': 39}

    Response metadata
        .. code-block:: python

            ai_msg = llm.invoke(messages)
            ai_msg.response_metadata

        .. code-block:: python

             {'model': 'gpt-3.5-turbo-0613'}

    """  # noqa: E501

    model_name: str = Field("github-copilot", alias="model")
    """The name of the model"""
    temperature: Optional[float] = 0
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    stop: Optional[List[str]] = ["<END>"]
    
    
    def __init__(self, *args, **kwargs):
        super(BaseChatModel, self).__init__(*args, **kwargs)
        self.temperature = kwargs.get("temperature", 0)
        self.max_tokens = kwargs.get("max_tokens", None)
        self.timeout = kwargs.get("timeout", None)
        self.stop = kwargs.get("stop", ["<END>"])
        

    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "chat-github-copilot"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters.

        This information is used by the LangChain callback system, which
        is used for tracing purposes make it possible to monitor LLMs.
        """
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": self.model_name,
            "temperature": self.temperature,
        }

    def _generate(
        self,
        messages: List[BaseMessage],
        **kwargs: Any,
    ) -> ChatResult:
        """Override the _generate method to implement the chat model logic.

        This can be a call to an API, a call to a local model, or any other
        implementation that generates a response to the input prompt.

        Args:
            messages: the prompt composed of a list of messages.
            stop: a list of strings on which the model should stop generating.
                  If generation stops due to a stop token, the stop token itself
                  SHOULD BE INCLUDED as part of the output. This is not enforced
                  across models right now, but it's a good practice to follow since
                  it makes it much easier to parse the output of the model
                  downstream and understand why generation stopped.
            run_manager: A run manager with callbacks for the LLM.
        """
        messages_to_copilot = []
        for message in messages:
            if isinstance(message, HumanMessage):
                messages_to_copilot.append({"role": "user", "content": message.content})
            elif isinstance(message, SystemMessage):
                messages_to_copilot.append(
                    {"role": "system", "content": message.content}
                )
            elif isinstance(message, AIMessage):
                messages_to_copilot.append(
                    {"role": "assistant", "content": message.content}
                )

        token = os.getenv("GITHUB_TOKEN")
        if token is None:
            raise ValueError("GITHUB_TOKEN environment variable is not set")

        copilot_header = {
            "authorization": f"Bearer {token}",
            "editor-version": EDITOR_VERSION,
            "editor-plugin-version": EDITOR_PLUGIN_VERSION,
            "user-agent": USER_AGENT,
            "content-type": "application/json",
            "openai-intent": "conversation-panel",
            "openai-organization": "github-copilot",
            "copilot-integration-id": "vscode-chat",
            "x-request-id": str(uuid.uuid4()),
            "vscode-sessionid": str(uuid.uuid4()),
            "vscode-machineid": MACHINE_ID,
        }

        data = {
            "messages": messages_to_copilot,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature, 
            "top_p": 1,
            "n": 1,
            "stop": self.stop,
        }

        request = requests.post(
            f"{API_ENDPOINT}/chat/completions",
            headers=copilot_header,
            json=data,
            timeout=self.timeout,
        )

        response = request.json()
        output = response["choices"][0]["message"]["content"]

        message = AIMessage(
            content=output,
            usage_metadata={
                "input_tokens": response["usage"]["prompt_tokens"],
                "output_tokens": response["usage"]["completion_tokens"],
                "total_tokens": response["usage"]["total_tokens"],
            },
            response_metadata={"model": response["model"]},
        )

        generation = ChatGeneration(message=message)

        return ChatResult(generations=[generation])
