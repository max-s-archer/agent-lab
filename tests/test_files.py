import os

import pytest

from agent_lab.files import list_workspace_files, read_workspace_file
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


def test_reads_bounded_utf8_text(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "note.txt").write_text("hello", encoding="utf-8")
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    assert read_workspace_file({"relative_file": "note.txt"}) == "hello"


def test_rejects_sensitive_oversized_and_binary_files(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / ".env").write_text("TOKEN=secret", encoding="utf-8")
    (workspace / "large.txt").write_bytes(b"a" * 8193)
    (workspace / "binary.txt").write_bytes(b"\xff")
    monkeypatch.setenv("AGENT_LAB_WORKSPACE", str(workspace))

    with pytest.raises(ToolError, match="not readable"):
        read_workspace_file({"relative_file": ".env"})
    with pytest.raises(ToolError, match="read limit"):
        read_workspace_file({"relative_file": "large.txt"})
    with pytest.raises(ToolError, match="not UTF-8"):
        read_workspace_file({"relative_file": "binary.txt"})
