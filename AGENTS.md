# Agent Routing

> Semantic source: English. Chinese counterpart: [AGENTS.zh-CN.md](AGENTS.zh-CN.md).

## Bootstrap

Before proposing or editing project documentation or code:

1. Read `/Users/v_zhangzheming/GitHubProjects/max-ai-toolkit/prompts/project-bootstrap.md`.
2. Follow the Toolkit routing and progressive-consumption guidance.
3. Read this file and only the project documents relevant to the task.

The Toolkit locator is `/Users/v_zhangzheming/GitHubProjects/max-ai-toolkit`. The Toolkit provides reusable methods; this repository remains authoritative for Agent Lab product facts, requirements, architecture, decisions, implementation, validation, and releases.

## Project identity

- Product name: Agent Lab
- Repository: `agent-lab`
- Project visibility: Public
- Project ownership and decision authority: The project author

## Project entry documents

- Public project entry: [README.md](README.md)
- Chinese public project entry: [README.zh-CN.md](README.zh-CN.md)
- Product overview semantic source: [overview.md](overview.md)
- Chinese product overview: [overview.zh-CN.md](overview.zh-CN.md)
- Documentation map and governance: [docs/documentation.md](docs/documentation.md)
- Phase 1 requirements semantic source: [docs/requirements/phase-1.md](docs/requirements/phase-1.md)
- Chinese Phase 1 requirements: [docs/requirements/phase-1.zh-CN.md](docs/requirements/phase-1.zh-CN.md)
- License: [LICENSE](LICENSE)

Development, validation, architecture, security, privacy, release, and decision documents have not yet been established. Create each one only when confirmed project facts, evidence, or an authorized decision give it a real responsibility. Do not infer a technical baseline from planned paths.

## External context

Private working state is maintained in `/Users/v_zhangzheming/GitHubProjects/max-dev-context/projects/agent-lab/`. Its `agent-proposals.md`, `author-prompts.md`, `author-todo.md`, and task handoffs are non-authoritative working material. They must not be treated as product requirements, project overrides, architecture approval, or authorization.

## Language

English is the semantic source for public project documentation and repository-facing output. Chinese is maintained in corresponding `.zh-CN.md` documents. When a bilingual pair differs materially, update the English source first and align the Chinese counterpart.

Use English for commit messages, pull requests, issues, release notes, and other public repository output unless the author explicitly decides otherwise.

## Project-specific rules

- Preserve the product principles and confirmed boundaries in `overview.md`.
- Mark unknown product or technical facts as `To be decided`; do not turn assumptions into decisions.
- Keep product decisions separate from technical architecture decisions.
- Do not prescribe unconfirmed implementation details from product documentation.
- Give each durable product fact one authoritative owner under `docs/documentation.md`.
- Keep proposals, open questions, and temporary investigation notes in the private development-state repository.
- The first priority is Agent Engineering learning, followed by portfolio value, followed by future Android Launcher integration.
- Runtime must retain control over model-proposed tool calls. Do not allow a model to execute arbitrary shell commands.
- Use simulated models for deterministic Runtime tests and real models for integration and behavior validation; neither replaces the other.
- Do not add Planning, Memory, RAG, MCP, multi-agent collaboration, persistence, or concurrency before a concrete problem justifies the added complexity.
- Production implementation requires an applicable current product definition and explicit authorization from the project author.
- Stop and obtain separate author direction when work would materially change product scope, require a consequential architecture decision, or introduce a specialist-review need.
- Commits, pushes, tags, releases, credentials, and remote-system changes require separate authorization for the exact action.

## Development and validation baseline

Phase 1 uses Python 3.12, `uv`, `pyproject.toml`, the `src/agent_lab/` layout, `pytest`, Ruff, and a synchronous CLI. The selected provider is Alibaba Cloud Model Studio through its OpenAI-compatible API.

The exact model name, compatible endpoint, credential variable, and authoritative development commands remain `To be decided`. The current confirmed behavior is a direct CLI-to-model call with response handling only. Do not add tools or a multi-step loop, and do not report a model call or validation result unless the corresponding action was actually performed.

