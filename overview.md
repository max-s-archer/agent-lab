# Agent Lab Overview

## Status

Planning

## Problem

LLM applications are easy to demonstrate with a short API call, but reliable agent systems require a deeper understanding of execution control, tool boundaries, state, failure handling, and evidence. A one-off demo does not provide enough engineering practice to understand these mechanisms or evaluate whether a new capability actually improves a system.

Agent Lab addresses this problem through a small, continuously evolving project that makes the execution model visible and testable.

## Product goal

Build a Python-based engineering laboratory in which the author can progressively understand and implement the core runtime of an LLM-powered agent.

The first interaction surface is a CLI. The CLI is an entry point rather than the product's core value. Future HTTP or Android integration remains possible, but no integration architecture is required at the current stage.

## Learning goals

The project should provide practical experience with:

- LLM APIs and structured output;
- function calling and tool calling;
- agent loops and harnesses;
- tool registration, parameter validation, authorization, and execution;
- task state, stop conditions, errors, and cancellation;
- run traces and structured observability;
- simulated-model testing and real-model integration;
- evaluation and reliability engineering.

Planning, memory, reflection, RAG, MCP, concurrency, persistence, and recovery are future learning topics. They must be introduced in response to a concrete problem, not to increase the number of technologies in the project.

## Portfolio goal

The repository should gradually accumulate evidence of engineering judgment:

- a clear product and runtime boundary;
- readable architecture explanations;
- automated tests;
- reproducible failure cases;
- documented trade-offs;
- a fixed set of validation tasks;
- stage reviews explaining what was learned and what complexity was deferred.

The portfolio value comes from explainable decisions and evidence, not from the number of frameworks or features.

## Future Launcher4Max relationship

Agent Lab may later inform Agent capabilities in Launcher4Max, such as natural-language search, controlled local operations, and multi-step tasks.

The most reusable future assets are expected to be:

- tool input and output protocols;
- runtime responsibility boundaries;
- task state models;
- permission and execution policies;
- error classifications;
- evaluation methods and engineering decisions.

Python implementation details, CLI interaction, and desktop-specific tools must not be assumed to be directly reusable in Android. The integration approach remains `To be decided`.

## Current scope

The confirmed first phase includes:

- a synchronous CLI;
- one direct request from CLI input to Alibaba Cloud Model Studio;
- handling and displaying the returned model response;
- configuration and transport errors reported without exposing credentials;
- simulated response tests for request construction and response handling;
- one real-model smoke validation after implementation is separately authorized.

## Non-goals

The first phase is not intended to:

- implement tool calling or a multi-step agent loop;
- create a general-purpose agent platform;
- support arbitrary shell commands;
- modify files or system state through model-generated instructions;
- provide multi-user service infrastructure;
- implement multi-agent collaboration;
- add planning, memory, RAG, MCP, persistence, or concurrency without a demonstrated need;
- decide how Agent Lab will be embedded into Android.

## Success criteria

The first phase is successful when the author can explain, test, and observe one direct model call, including:

- how CLI input becomes a provider request;
- how a text response is handled and displayed;
- how configuration, transport, and malformed-response failures are distinguished;
- how tests verify the behavior without network access;
- how credentials stay out of source, examples, and logs.

## Current technical decisions

The following baseline is confirmed for Phase 1:

- Python 3.12;
- `uv` and `pyproject.toml`;
- the `src/agent_lab/` package layout;
- `pytest` and Ruff;
- a synchronous CLI;
- Alibaba Cloud Model Studio through its OpenAI-compatible API;
- credentials supplied through the `DASHSCOPE_API_KEY` environment variable;
- `qwen3.8-flash` as the initial model;
- a 30-second request timeout;
- a provider adapter that keeps future Runtime code independent of the provider SDK.

The public contribution and release workflow remains `To be decided`.

## Related documents

- [Phase 1 Requirements](docs/requirements/phase-1.md)
- [Documentation Map](docs/documentation.md)
- [Agent Routing](AGENTS.md)

