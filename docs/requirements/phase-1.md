# Phase 1 Requirements

## Status

Confirmed for the bounded runtime slice.

This document is the authoritative Phase 1 requirement. The runtime slice uses simulated models for its tests. A new real Model Studio call requires separate authorization.

## Objective

Establish a correct synchronous call from the CLI to Alibaba Cloud Model Studio and a practical understanding of the request and response boundary.

The phase keeps the direct model call and controlled tool decision. The model may answer directly, calculate, list file names, or read one bounded text file. The Runtime validates the request and returns the tool result to the model. It does not write files, plan, or use memory.

## User-visible flow

The first phase should support this observable flow:

```text
CLI input
  -> model decision
  -> optional calculate, directory-list, or bounded text-read execution
  -> tool result returned to the model
  -> final answer or controlled stop
```

The interaction is synchronous. The model provider is Alibaba Cloud Model Studio through its OpenAI-compatible API. The Runtime must not depend directly on the provider SDK.

## Required behavior

### Model interaction

- A one-shot CLI command accepts one user input and starts one runtime run.
- `--interactive` keeps a local in-process message list and resends at most 8 messages on each turn.
- Interactive history is discarded when the process exits. The provider does not keep an open session.
- The model may return text directly.
- The real model request declares `calculate`, `list_workspace_files`, and `read_workspace_file`.
- `read_workspace_file` reads at most 8 KB of UTF-8 text from one regular file.
- The Runtime rejects absolute paths, parent-directory escapes, symlink escapes, binary content, oversized files, and sensitive names such as `.env`.
- `list_workspace_files` accepts only a relative directory and returns at most 20 file names.
- The Runtime resolves the directory and rejects paths outside the configured workspace, including symlink escapes.
- The Runtime validates the tool name and arguments before execution.
- A tool result is returned to the model, which must then provide the final text.
- The Runtime allows at most two model calls and one tool call.
- Unknown tools, invalid arguments, model failures, and step limits stop with distinguishable messages.
- Each run writes a local JSONL trace with a run ID, request and response events, tool results, and a final status.
- Traces redact credentials and are not durable conversation memory.

### Technical baseline

- Python 3.12.
- `uv` with `pyproject.toml`.
- Package layout: `src/agent_lab/`.
- `pytest` for tests and Ruff for linting.
- Credentials are read from the `DASHSCOPE_API_KEY` environment variable and are never stored in source, examples, or logs.
- The initial model is `qwen3.8-flash`.
- The OpenAI-compatible base URL is `https://ws-nnpvwzj2vhzbu3i6.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`.
- The request timeout is 30 seconds.

## Testing requirements

The Runtime should be testable without a real model API or network connection.

The offline tests should cover:

- direct answer;
- successful bounded text-file read;
- rejection of oversized, binary, and sensitive files;
- directory traversal and symlink escape rejection;
- unknown tool;
- invalid calculation arguments;
- model or transport failure;
- two-model-call limit;
- malformed provider response;
- absence of credentials, prompts, and response secrets in logs.

Real model calls are used for integration and behavior smoke validation. They are not a replacement for deterministic Runtime tests.

## Security and privacy boundaries

- Credentials must come from local environment or an equivalent secure configuration mechanism.
- Credentials must not be committed, printed, or written to traces.
- Model-generated text must never be treated as an arbitrary shell command.
- Local filesystem tools must use an explicit bounded workspace.
- Returned output must have a bounded size.
- Any future tool that changes system state, accesses sensitive data, or creates external side effects requires a separate permission design and author confirmation.

## Deferred capabilities

The following are not part of Phase 1:

- writing files or tool calling beyond the three confirmed tools;
- planning systems;
- persistent memory;
- reflection loops;
- RAG;
- MCP;
- multi-agent collaboration;
- background concurrency;
- durable task persistence and recovery;
- generic HTTP service infrastructure;
- Android integration;
- arbitrary shell or unrestricted filesystem operations.

Adding one of these capabilities requires a concrete problem statement, a comparison with a simpler alternative, an acceptance criterion, and an explicit decision.

## Acceptance criteria

Phase 1 is ready for review when:

1. A direct model answer is displayed without tool execution.
2. A valid request for `calculate`, `list_workspace_files`, or `read_workspace_file` is executed.
   Its result returns to the model.
3. Unknown tools, invalid arguments, and path escapes do not execute the tool.
4. The runtime stops at two model calls.
5. Automated tests verify the behavior without network access.
6. Credentials are not present in source, examples, or logs.
7. One real Model Studio smoke call is recorded separately from offline evidence.
8. The author can explain the CLI, provider adapter, request, and response responsibilities.

The public contribution and release workflow remains `To be decided`.

