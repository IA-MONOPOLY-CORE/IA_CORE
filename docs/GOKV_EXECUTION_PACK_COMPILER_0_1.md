# GOKV 0.1 — Deterministic Execution Pack Compiler

## Gate

`N6_GOKV_EXECUTION_PACK_COMPILER_PASSED`

The compiler is a development-only deterministic transformation from an explicit request and the Git-backed vault to a validated `gokv.execution_pack.v1` document. It is not an execution engine, model router, runtime context provider, or agent integration.

## Selection Contract

The request must declare:

- `mission_class`;
- optional `task_type`, `scope`, `risk_class`, `required_capabilities`, `tags`;
- `agent_class` and `model_size_class` as declared labels only;
- `mode`, either `PROMOTED_ONLY` or explicit `DEVELOPMENT_VALIDATED`.

The compiler then applies stable filters:

1. Lifecycle status is `PROMOTED` only by default.
2. `VALIDATED` is selectable only in explicit `DEVELOPMENT_VALIDATED` mode.
3. `CANDIDATE`, `OBSERVED`, `REVISED`, `DEPRECATED`, and `REPLACED` are never selected implicitly.
4. Item scope must match the requested scope or be `GLOBAL`.
5. Item privacy must match the requested privacy class or be `global_public`.
6. Declared mission, task type, capability, and tag constraints must be compatible.
7. Items are sorted by `knowledge_id` and the pack ID is derived from the normalized request and selected IDs.

No current runtime or product path consumes the resulting pack.

## Pack Contract

Each pack contains the requested mission metadata, selected knowledge IDs, principles, procedures, decision rules, stop conditions, validation rules, failure modes, recovery guidance, evidence summary, and a fixed output contract:

- structured JSON output;
- runtime disabled;
- execution disabled;
- payload disabled;
- explicit human approval required.

This keeps the first compiler useful for development inspection while preventing it from creating actions, submit behavior, runtime state, or permissions.

## Fixtures and Results

The four fixtures under `tests/fixtures/gokv/` cover:

| Fixture | Expected behavior |
|---|---|
| `fixture_a_ui_ux.json` | Explicit validated mode selects only compatible contract knowledge. |
| `fixture_b_default_promoted_only.json` | Empty pack because Generation 0 has no promoted items. |
| `fixture_c_tag_filter.json` | `gates` tag selects only the two compatible gated patterns. |
| `fixture_d_capability_mismatch.json` | An unrecorded required capability selects nothing. |

The focal compiler test also proves deterministic repeatability and rejects a tampered operational contract.

## Safety Boundary

`gokv/compiler.py` imports only the GOKV schema/storage helpers and standard-library modules. It does not import UI, API, backend, runtime, execution, providers, integrations, memory, or payload code. It performs no network access, model invocation, embedding lookup, vector search, scheduler dispatch, or tool execution.
