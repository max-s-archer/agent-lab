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

The offline tests must verify request construction, successful response handling, missing configuration, transport failure, HTTP errors, and malformed responses without using the network.

## Real API validation

A real Model Studio call requires separate authorization. Its result must be recorded separately from offline tests. Logs and reports must not include `DASHSCOPE_API_KEY` or any API key value.

## Current evidence

### Offline checks

On 2026-10-15, the HTTP transport slice was checked with:

```text
uv sync --dev
uv run pytest
uv run ruff check .
```

The environment resolved CPython 3.12.15. Pytest reported 10 passed, and Ruff reported all checks passed. The HTTP transport tests replace `urlopen` with simulated responses and do not open a network connection.

### Real API smoke test

On 2026-10-15, one authorized Model Studio call was run:

```text
uv run agent-lab "Reply with exactly: pong"
```

The call used `qwen3.8-flash`, the confirmed compatible endpoint, and `DASHSCOPE_API_KEY` from the process environment. It returned `pong` with exit code 0. The credential value was not printed, logged, or committed. This smoke result does not replace the offline tests.
