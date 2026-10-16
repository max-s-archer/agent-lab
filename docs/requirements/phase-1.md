# Phase 1 Requirements

## Status

Planning

This document defines the proposed first-phase product boundary. It becomes the authoritative first-phase requirement only after the project author confirms it.

## Objective

Establish an initial model API capability and a practical understanding of the control model behind a small LLM-powered agent.

The phase should produce a minimal but complete controlled loop rather than a feature-rich general-purpose platform.

## User-visible flow

The first phase should support this observable flow:

```text
user input
  -> agent runtime
  -> model request
  -> direct response or structured tool request
  -> tool validation and execution
  -> tool result returned to the model
  -> final response, another bounded step, or controlled termination
```

The first interaction surface is a synchronous CLI unless a later confirmed decision changes this boundary.

## Required behavior

### Model interaction

- The system can send a user request to a model.
- The system can handle a direct model response.
- The system can handle a model response that requests a registered tool.
- The system can return a tool result to the model.
- The system can accept a subsequent model response or terminate with a clear reason.

### Runtime control

- The Runtime owns the execution loop.
- The model cannot directly execute code, shell commands, or unregistered capabilities.
- The Runtime enforces a maximum execution-step limit.
- The Runtime enforces a tool-call limit.
- The Runtime distinguishes normal completion, model failure, tool failure, invalid request, limit termination, and user cancellation.
- An exception must not leave the run without a controlled final state.

### Tool boundary

The first tool set should remain small and low risk:

- `calculate`: deterministic arithmetic operations with explicit operation and numeric arguments; no `eval`.
- `list_workspace_files`: list a bounded set of entries inside an explicitly configured workspace; validate path resolution and prevent traversal outside the workspace.

File writes, arbitrary shell execution, network-side effects, and high-risk system mutation are out of scope for this phase.

### Trace and observability

Each run should have a Run ID. The trace should record, at minimum:

- run and step identifiers;
- event type;
- model and tool call metadata needed for diagnosis;
- execution duration;
- errors and their classification;
- final stop reason.

Logs must not include API keys, secrets, or unnecessary sensitive file contents by default.

## Testing requirements

The Runtime should be testable without a real model API or network connection.

The offline test suite should cover:

- direct model response;
- successful tool request;
- tool execution failure;
- unknown tool;
- invalid tool arguments;
- multiple bounded tool calls;
- execution-step limit;
- model exception;
- user cancellation behavior where the selected CLI/runtime boundary supports it;
- trace emission and final stop reason.

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

1. A local CLI can accept a request and produce a final response or controlled termination.
2. A simulated model can verify the Runtime loop without network access or credentials.
3. A registered tool can be validated, executed, and returned to the model.
4. Execution and tool limits prevent uncontrolled loops.
5. Model, tool, invalid-request, cancellation, and limit failures have distinguishable outcomes.
6. A structured trace can explain the important events in a run without exposing secrets by default.
7. Automated tests cover the required Runtime behavior.
8. A real-model smoke validation has been performed and its result is recorded separately from offline test evidence.
9. The author can explain the responsibilities of the model, Runtime, registry, tool implementation, and trace.

## Open decisions

The following remain `To be decided`:

- Python version;
- dependency manager;
- package layout;
- model provider and model selection;
- API client and SDK version;
- test framework;
- lint and static-analysis tools;
- exact CLI interaction format;
- workspace configuration mechanism;
- timeout and cancellation implementation details;
- public contribution and release workflow.

