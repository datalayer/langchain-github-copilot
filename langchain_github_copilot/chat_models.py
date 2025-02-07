"""
Github Copilot Chat Model.

Inspired from https://github.com/langchain-ai/langchain/blob/master/libs/partners/openai/langchain_openai/chat_models/azure.py
with modifications for Github Copilot API.

Several fields are not used with Github Copilot API.
Cleaning of the unused fields should be done in the future.
"""

from __future__ import annotations

import logging
import uuid
import secrets
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from langchain_core.language_models.chat_models import LangSmithParams
from langchain_core.utils import secret_from_env
from pydantic import Field, SecretStr, model_validator
from typing_extensions import Self

from langchain_github_copilot.base import BaseChatOpenAI

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://api.githubcopilot.com"

LGC_VERSION = "0.0.1"
EDITOR_VERSION = f"LangchainGithubCopilot/{LGC_VERSION}"
EDITOR_PLUGIN_VERSION = f"LangchainGithubCopilot/{LGC_VERSION}"
USER_AGENT = f"LangchainGithubCopilot/{LGC_VERSION}"
MACHINE_ID = secrets.token_hex(33)[0:65]


class ChatGithubCopilot(BaseChatOpenAI):
    
    github_token: Optional[SecretStr] = Field(alias="api_key", default_factory=secret_from_env(["GITHUB_TOKEN"], default=None),)
    """Automatically inferred from env var `GITHUB_TOKEN` if not provided."""
    model_name: str = Field(default="gpt-4o", alias="model")
    """
    Github copilot supports the following models (as of 2024-02-07): gpt-4o, o1, o3-mini, gemini-2.0-flash-001, claude-3.5-sonnet.
    Unexpected behavior may occur if you use models outside the openai ecosystem (i.e. gemini-2.0-flash-001 and claude-3.5-sonnet).
    Check your GithubCopilot settings to make sure the model you want to use is enabled.
    """
    
    # Following fields are not used with Github Copilot API
    deployment_name: Union[str, None] = Field(default=None, alias="azure_deployment")
    model_version: str = ""
    openai_api_type: Optional[str] = Field(default=None)
    openai_api_version: Optional[str] = Field(alias="api_version", default=None)
    header: Optional[Dict[str, str]] = Field(default=None)
    
    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "chat_models", "azure_openai"]

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {
            "github_token": "GITHUB_TOKEN",
        }

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

    @model_validator(mode="after")
    def validate_environment(self) -> Self:
        
        copilot_header = {
            "authorization": f"Bearer {self.github_token.get_secret_value() if self.github_token else None}",
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
        
        if not self.client:
            self.client = f"{API_ENDPOINT}/chat/completions"
            self.header = copilot_header
        return self

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            **{"azure_deployment": self.deployment_name},
            **super()._identifying_params,
        }

    @property
    def _llm_type(self) -> str:
        return "azure-openai-chat"

    @property
    def lc_attributes(self) -> Dict[str, Any]:
        return {
            "openai_api_type": self.openai_api_type,
            "openai_api_version": self.openai_api_version,
        }

    def _get_ls_params(
        self, stop: Optional[List[str]] = None, **kwargs: Any
    ) -> LangSmithParams:
        """Get the parameters used to invoke the model."""
        params = super()._get_ls_params(stop=stop, **kwargs)
        params["ls_provider"] = "github-copilot"
        if self.model_name:
            if self.model_version and self.model_version not in self.model_name:
                params["ls_model_name"] = (
                    self.model_name + "-" + self.model_version.lstrip("-")
                )
            else:
                params["ls_model_name"] = self.model_name
        elif self.deployment_name:
            params["ls_model_name"] = self.deployment_name
        return params