# Copyright (c) 2024-2025 Datalayer, Inc.
#
# MIT License

from importlib import metadata

from langchain_github_copilot.chat_models import ChatGitHubCopilot

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""

del metadata  # optional, avoids polluting the results of dir(__package__)


__all__ = [
    "ChatGitHubCopilot",
    "__version__",
]
