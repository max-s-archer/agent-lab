# Phase 1 Requirements

## Status

Confirmed for the initial API-call slice.

This document is the authoritative Phase 1 requirement. It defines only the direct model-call slice; it does not authorize creating the project configuration or implementation until the author separately authorizes that work.

## Objective

Establish a correct synchronous call from the CLI to Alibaba Cloud Model Studio and a practical understanding of the request and response boundary.

The phase sends the user's input directly to the model API and handles the returned response. It does not add tools, planning, memory, file operations, or other intermediate agent behavior.

## User-visible flow

The first phase should support this observable flow:

```text
CLI input
  -> direct Model Studio request
  -> response handling
  -> CLI output or controlled error
```

The interaction is synchronous. The model provider is Alibaba Cloud Model Studio through its OpenAI-compatible API. The Runtime must not depend directly on the provider SDK.

## Required behavior

### Model interaction

- The CLI accepts one user input and sends it directly to the configured model.
- The system handles a successful text response and displays it.
- The system reports configuration, transport, and response-format failures with a controlled message.
- The system does not call tools or perform another model round trip in this phase.

### Technical baseline

- Python 3.12.
- `uv` with `pyproject.toml`.
- Package layout: `src/agent_lab/`.
- `pytest` for tests and Ruff for linting.
- Credentials are read from environment variables and are never stored in source or logs.

## Testing requirements

The Runtime should be testable without a real model API or network connection.

The offline tests should cover:

- request construction from CLI input;
- successful response handling;
- missing configuration;
- transport or provider failure;
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

- tool calling and multi-step agent loops;
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

1. A local CLI sends one input directly to the configured model boundary.
2. A successful text response is displayed without intermediate tool processing.
3. Missing configuration, transport failure, and malformed responses terminate with distinguishable messages.
4. Automated tests verify request construction and response handling without network access.
5. Credentials are not present in source, examples, or logs.
6. One real Model Studio smoke call is recorded separately from offline evidence.
7. The author can explain the CLI, provider adapter, request, and response responsibilities.

## Open decisions

The following remain `To be decided`:

- exact Model Studio model name;
- OpenAI-compatible endpoint;
- credential environment-variable name;
- timeout value;
- public contribution and release workflow.

