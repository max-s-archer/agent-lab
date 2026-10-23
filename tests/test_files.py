import os

import pytest

from agent_lab.files import list_workspace_files
from agent_lab.runtime import ToolError


def test_lists_only_file_names(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    nested = workspace / "nested"
    nested.mkdir(parents=True)
    (nested / "beta.txt").write_text("secret", encoding="utf-8")
    (nested / "alpha.txt").write_text("secret", encoding="utf-8")
    (nested / "directory").mkdir()
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    result = list_workspace_files({"relative_directory": "nested"})

    assert result == "alpha.txt\nbeta.txt"
    assert "secret" not in result


def test_limits_results_to_twenty_names(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    for index in range(21):
        (workspace / f"{index:02d}.txt").write_text("content", encoding="utf-8")
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    assert len(list_workspace_files({"relative_directory": "."}).splitlines()) == 20


def test_rejects_parent_directory_escape(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    with pytest.raises(ToolError, match="escapes the workspace"):
        list_workspace_files({"relative_directory": ".."})


def test_rejects_symlink_escape(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "hidden.txt").write_text("hidden", encoding="utf-8")
    link = workspace / "linked"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except OSError:
        pytest.skip("Symlink creation is unavailable.")
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    with pytest.raises(ToolError, match="escapes the workspace"):
        list_workspace_files({"relative_directory": "linked"})
