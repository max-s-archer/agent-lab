"""Read-only workspace file tools."""

import os
from pathlib import Path

from agent_lab.runtime import ToolError

MAX_LISTED_FILES = 20
MAX_READ_BYTES = 8 * 1024
WORKSPACE_ENV = "AGENT_LAB_WORKSPACE"
SENSITIVE_NAMES = {".env", ".env.local", "credentials.json", "id_rsa"}


def workspace_root() -> Path:
    """Return the explicitly configured workspace or the current directory."""

    configured = os.getenv(WORKSPACE_ENV)
    root = Path(configured).resolve() if configured else Path.cwd().resolve()
    if not root.is_dir():
        raise ToolError("Workspace directory does not exist.")
    return root


def resolve_workspace_path(relative_path: str) -> Path:
    """Resolve one workspace-relative path and reject escapes."""

    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ToolError("Invalid workspace path.")
    if Path(relative_path).is_absolute():
        raise ToolError("Path escapes the workspace.")
    root = workspace_root()
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root):
        raise ToolError("Path escapes the workspace.")
    return candidate


def list_workspace_files(arguments: dict) -> str:
    """List a bounded set of file names without reading file contents."""

    relative_directory = arguments.get("relative_directory", ".")
    if not isinstance(relative_directory, str) or not relative_directory.strip():
        raise ToolError("Invalid list_workspace_files arguments.")
    if Path(relative_directory).is_absolute():
        raise ToolError("Directory path escapes the workspace.")

    candidate = resolve_workspace_path(relative_directory)
    if not candidate.is_dir():
        raise ToolError("Directory path escapes the workspace.")

    names = sorted(path.name for path in candidate.iterdir() if path.is_file())
    return "\n".join(names[:MAX_LISTED_FILES])


def read_workspace_file(arguments: dict) -> str:
    """Read one bounded UTF-8 text file without following workspace escapes."""

    relative_file = arguments.get("relative_file")
    candidate = resolve_workspace_path(relative_file)
    if candidate.name.casefold() in SENSITIVE_NAMES or not candidate.is_file():
        raise ToolError("File is not readable.")
    if candidate.stat().st_size > MAX_READ_BYTES:
        raise ToolError("File exceeds the read limit.")
    data = candidate.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ToolError("File is not UTF-8 text.") from error
