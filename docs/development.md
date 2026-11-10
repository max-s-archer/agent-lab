# Development Guide

## Toolchain

- Python 3.12
- `uv`
- Project metadata: `pyproject.toml`
- Package layout: `src/agent_lab/`
- Test runner: `pytest`
- Linter: Ruff

## Model configuration

Phase 1 uses Alibaba Cloud Model Studio through its OpenAI-compatible API.

- Model: `qwen3.8-flash`
- Base URL: `https://ws-nnpvwzj2vhzbu3i6.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- Credential variable: `DASHSCOPE_API_KEY`
- Timeout: 30 seconds

Copy `.env.example` to a local `.env` only when implementation needs it. Put the real API key in the local environment or the untracked `.env`; never commit the key.

## Current boundary

The CLI declares read-only `read_workspace_file`. It reads at most 8 KB of UTF-8 text from one regular file inside the configured workspace. It rejects absolute paths, parent-directory escapes, symlink escapes, binary content, oversized files, and sensitive file names such as `.env`. It must not write files.

`agent-lab --interactive` keeps conversation history in the local process and resends at most 8 messages on each turn. Closing the process discards that history. The provider does not keep an open session.

Each run writes `traces/<run-id>.jsonl`. The directory is ignored by Git. Traces omit authorization values and are discarded from version control; they are not long-term memory. A new real Model Studio call requires separate authorization.

## Validation commands

The simulated CLI slice uses these offline checks:

```text
uv sync --dev
uv run pytest
uv run ruff check .
```

The latest execution result is recorded in [Validation Guide](validation.md). Do not report a new run unless its result is recorded separately.
