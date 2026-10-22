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

The offline tests must verify request construction, successful response handling, tool declaration, missing configuration, transport failure, HTTP errors, malformed responses, and bounded tool execution without using the network.

## Real API validation

A real Model Studio call requires separate authorization. Its result must be recorded separately from offline tests. Logs and reports must not include `DASHSCOPE_API_KEY` or any API key value.

## Current evidence

### Offline checks

On 2026-10-15, the tool-calling slice was checked with:

```text
uv run pytest
uv run ruff check .
```

The environment resolved CPython 3.12.15. Pytest reported 17 passed, and Ruff reported all checks passed. Simulated responses do not open a network connection.

### Real API smoke test

On 2026-10-15, one authorized Model Studio call was run:

```text
uv run agent-lab "Reply with exactly: pong"
```

The call used `qwen3.8-flash`, the confirmed compatible endpoint, and `DASHSCOPE_API_KEY` from the process environment. It returned `pong` with exit code 0. The credential value was not printed, logged, or committed. This direct-answer result does not replace the offline tests.

### Real tool-call smoke test

On 2026-10-15, one authorized tool-calling flow was run with the same model and credential variable. The prompt requested `calculate` to add 2 and 3.

The first model response requested `calculate` with operation `add`, left `2`, and right `3`. The local runtime returned `5`, and the second model response returned `result=5`. No credential value was recorded. This smoke result is separate from the offline tests.
