# GOKV Continuous Development Capture Protocol v1

## Purpose

This protocol governs development-time capture after the GOKV 0.1 bootstrap. It records operational knowledge without changing product behavior, activating runtime learning, or allowing unreviewed promotion.

## Required Sequence

1. Confirm the change is inside the declared development-only GOKV boundary.
2. Run `python -m gokv validate` before adding records.
3. Capture an event only when a development block has a real start/end boundary.
4. Capture an execution metric with `NOT_AVAILABLE` for any unknown duration, quota, or cost.
5. Add new observations as `OBSERVED` or `CANDIDATE`; never write `PROMOTED` directly.
6. Rebuild the registry after adding a knowledge item.
7. Compile packs only with an explicit mode and inspect selected IDs.
8. Run focused tests, canonical GOKV tests, protected-surface checks, `py_compile`, Node checks, and `git diff --check`.
9. Commit the station only after its gate passes.

## Commands

From `C:\IA_CORE`:

```text
python -m gokv validate
python -m gokv rebuild-index
python -m gokv show-item <knowledge_id>
python -m gokv list-promoted
python -m gokv append-event <event.json>
python -m gokv append-metric <metric.json>
python -m gokv add-candidate <candidate.json>
python -m gokv compile-pack <compile-request.json>
```

The `--repo-root <path>` option allows isolated development storage for tests. It does not change the canonical location, which remains `knowledge/global_operational/`.

## Lifecycle Rules

- `OBSERVED -> CANDIDATE -> VALIDATED -> PROMOTED` is the normal evidence path.
- `PROMOTED` requires explicit evidence and `HIGH` confidence.
- `REVISED`, `DEPRECATED`, and `REPLACED` require relationship/version evidence.
- A compiler never promotes, revises, deprecates, or replaces an item.
- Default pack mode is `PROMOTED_ONLY`.
- `DEVELOPMENT_VALIDATED` is an explicit inspection mode, not runtime permission.

## Measurement Rules

Use measured values only when actually measured. Use `OPERATOR_REPORTED`, `OPERATOR_ESTIMATED`, `RESET_INTERRUPTED`, or `NOT_AVAILABLE` when appropriate. Unknown quotas, durations, model performance, token use, and costs remain null or explicitly unavailable. No value is inferred from a UI display, a model label, or a planned commit.

## Safety Boundary

The protocol does not authorize changes to HTML, CSS product behavior, JavaScript contractual logic, i18n, backend, payload, runtime, execution, providers, integrations, endpoints, scheduler, queue, browser automation, agent memory, or current UI contracts. It does not create public APIs, multi-tenant learning, downloaded models, embeddings, vector databases, RAG, fine-tuning, or autonomous action.

## Required Review Before Promotion

Promotion requires a separate evidence review, explicit lifecycle transition, updated tests, a bounded commit, and a clean protected-surface diff. Until then, Generation 0 candidates remain candidates and are excluded from default packs.
