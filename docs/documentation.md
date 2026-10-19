# Documentation Map

## Purpose

This document defines the responsibility and authority of Agent Lab documentation. Each durable product fact should have one authoritative owner.

## Current documents

- `README.md`: Public English entry point and concise project introduction.
- `README.zh-CN.md`: Chinese counterpart of the public entry point.
- `overview.md`: Semantic source for product positioning, goals, scope, non-goals, and future relationship with Launcher4Max.
- `overview.zh-CN.md`: Chinese counterpart of the product overview.
- `docs/requirements/phase-1.md`: Semantic source for the confirmed first-phase behavioral requirements and acceptance criteria.
- `docs/requirements/phase-1.zh-CN.md`: Chinese counterpart of the first-phase requirements.
- `docs/development.md`: Selected toolchain, configuration names, and setup boundaries.
- `docs/validation.md`: Validation commands and evidence rules. Command availability is not evidence of a successful run.

## Planned document responsibilities

The following documents are not current authoritative documents and should be created only when their responsibility has confirmed content:

- `docs/architecture.md`: confirmed runtime boundaries, dependencies, and technical direction;
- `docs/decisions/`: consequential technical or product decisions and their trade-offs;
- `docs/security.md`: confirmed security and permission boundaries if the Phase 1 requirements no longer provide enough detail;
- `docs/release.md`: public release and artifact governance when release work begins.

Do not create empty documents or directories merely to complete the planned structure.

## Authority and working state

Product facts, requirements, architecture, decisions, implementation, tests, validation, and releases belong in this product repository.

Private proposals, open questions, prompts, personal todo items, and active task handoffs belong in:

`/Users/v_zhangzheming/GitHubProjects/max-dev-context/projects/agent-lab/`

Private working-state files are not product contracts or project-specific overrides. When a proposal is confirmed, transfer the durable decision to the appropriate product document and keep the private proposal state updated.

## Language

English files are semantic sources for public project documentation. `.zh-CN.md` files are maintained Chinese counterparts. Keep bilingual counterparts aligned when their intended meaning changes.

## Maintenance

Update this map when a new durable document is created, moved, or retired. Do not duplicate the complete content of another document merely to make the map more descriptive.

