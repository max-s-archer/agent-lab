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

The first phase includes:

- a minimal model API integration;
- a controlled runtime loop;
- direct model responses;
- validated requests for a small number of tools;
- tool results returned to the model;
- bounded execution steps;
- basic model and tool error handling;
- structured run traces;
- simulated-model tests;
- a small real-model smoke validation.

## Non-goals

The first phase is not intended to:

- create a general-purpose agent platform;
- support arbitrary shell commands;
- modify files or system state through model-generated instructions;
- provide multi-user service infrastructure;
- implement multi-agent collaboration;
- add planning, memory, RAG, MCP, persistence, or concurrency without a demonstrated need;
- decide how Agent Lab will be embedded into Android.

## Success criteria

The project is progressing successfully when the author can explain, test, and observe the complete controlled loop from user input to final result, including:

- what the model is allowed to decide;
- what the Runtime must control;
- how tools are registered and validated;
- how failures are classified;
- how execution stops;
- how tests demonstrate the behavior;
- how traces provide evidence without exposing secrets or unnecessary sensitive data.

## Current technical decisions

The following are not yet decided:

- Python version;
- dependency manager;
- package layout;
- model provider and model selection;
- test framework;
- lint and static-analysis tools;
- synchronous or asynchronous execution beyond the first learning slice;
- public release and contribution workflow details.

These decisions belong in the appropriate technical or decision document after confirmation. This overview should not be used to infer them.

## Related documents

- [Phase 1 Requirements](docs/requirements/phase-1.md)
- [Documentation Map](docs/documentation.md)
- [Agent Routing](AGENTS.md)

