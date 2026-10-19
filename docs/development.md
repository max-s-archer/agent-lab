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

The implementation has not been created yet. This guide records the confirmed baseline only. A future CLI must send one input directly to the model and display or report its response. It must not add tools, file operations, planning, memory, or another model round trip in Phase 1.

## Planned commands

The following commands are planned after the implementation is authorized:

```text
uv sync
uv run pytest
uv run ruff check .
```

Do not report any of these commands as executed until a validation record shows the actual result.
