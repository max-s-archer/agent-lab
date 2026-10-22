# Validation Guide

## Purpose

Define how Phase 1 changes are checked. A command listed here is only an available or planned entry point; it is evidence only after it has actually run.

## Documentation changes

For documentation-only changes:

```text
git diff --check
```

Also inspect the changed Markdown links and confirm that bilingual counterparts describe the same behavior.

## Automated checks

For the simulated CLI implementation, run:

```text
uv run pytest
uv run ruff check .
```

The offline tests must verify request construction, successful response handling, missing configuration, transport failure, and malformed responses without using the network.

## Real API validation

A real Model Studio call requires separate authorization. Its result must be recorded separately from offline tests. Logs and reports must not include `DASHSCOPE_API_KEY` or any API key value.

## Current evidence

On 2026-10-15, the simulated CLI slice was checked with:

```text
uv sync --dev
uv run pytest
uv run ruff check .
```

The environment resolved CPython 3.12.15. Pytest reported 7 passed, and Ruff reported all checks passed after fixing two import-order findings. No real Model Studio call has been made.
