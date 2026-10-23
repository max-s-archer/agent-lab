"""Read-only workspace directory listing."""

import os
from pathlib import Path

from agent_lab.runtime import ToolError

MAX_LISTED_FILES = 20
WORKSPACE_ENV = "AGENT_LAB_WORKSPACE"


def workspace_root() -> Path:
    """Return the explicitly configured workspace or the current directory."""

    configured = os.getenv(WORKSPACE_ENV)
    root = Path(configured).resolve() if configured else Path.cwd().resolve()
    if not root.is_dir():
        raise ToolError("Workspace directory does not exist.")
    return root


def list_workspace_files(arguments: dict) -> str:
    """List a bounded set of file names without reading file contents."""

    relative_directory = arguments.get("relative_directory", ".")
    if not isinstance(relative_directory, str) or not relative_directory.strip():
        raise ToolError("Invalid list_workspace_files arguments.")
    if Path(relative_directory).is_absolute():
        raise ToolError("Directory path escapes the workspace.")

    root = workspace_root()
    candidate = (root / relative_directory).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_dir():
        raise ToolError("Directory path escapes the workspace.")

    names = sorted(path.name for path in candidate.iterdir() if path.is_file())
    return "\n".join(names[:MAX_LISTED_FILES])
