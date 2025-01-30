from importlib import metadata

from langchain_github_copilot.chat_models import ChatGithubCopilot

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ChatGithubCopilot",
    "__version__",
]
