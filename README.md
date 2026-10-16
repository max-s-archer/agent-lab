# Agent Lab

Agent Lab is a public Python engineering laboratory for learning and building reliable LLM-powered agent systems.

The project uses a CLI as its first interaction surface and focuses on understanding the execution model behind an agent: model calls, structured tool requests, runtime control, validation, failure handling, testing, and run traces.

## Status

Planning

## Goals

The project has three connected goals, in this priority order:

1. Build practical Agent Engineering knowledge through a real, evolving project.
2. Produce a clear, testable, explainable public GitHub portfolio project.
3. Preserve reusable protocols and engineering experience for possible future integration with Launcher4Max.

## First phase

The first phase aims to establish an initial model API integration and a minimal controlled agent loop:

```text
user input
  -> runtime
  -> model decision
  -> validated tool request
  -> tool execution
  -> tool result returned to the model
  -> final answer or another controlled step
```

The phase is intended to build an initial understanding of how model calls and runtime control work internally. Its detailed requirements are defined in [Phase 1 Requirements](docs/requirements/phase-1.md).

## Scope boundaries

The project will not begin by building a general-purpose agent platform. Planning, memory, RAG, MCP, multi-agent collaboration, persistence, concurrency, arbitrary shell execution, and high-risk system mutation remain outside the first phase unless a concrete problem justifies them.

## Documentation

- [Project overview](overview.md)
- [Chinese project overview](overview.zh-CN.md)
- [Documentation map](docs/documentation.md)
- [Phase 1 requirements](docs/requirements/phase-1.md)
- [Chinese Phase 1 requirements](docs/requirements/phase-1.zh-CN.md)
- [Agent routing](AGENTS.md)

## License

This project is available under the Apache License 2.0. See [LICENSE](LICENSE).
