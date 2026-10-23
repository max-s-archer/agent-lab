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

The CLI sends the local `calculate` and read-only `list_workspace_files` tool definitions with each model request. Offline tests replace the network transport. The file tool lists names only inside its configured workspace and must not read file contents, write files, or follow paths outside that workspace. A new real Model Studio call requires separate authorization.

## Validation commands

The simulated CLI slice uses these offline checks:

```text
uv sync --dev
uv run pytest
uv run ruff check .
```

The latest execution result is recorded in [Validation Guide](validation.md). Do not report a new run unless its result is recorded separately.
