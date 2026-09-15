# Roadmap 4.x Macro-Mission 04.1

## Commit accountability ledger

## Mission boundary

Baseline: `5bde1c10acfd98d436f961e91661a104c7667593` on `main`.

The ledger records real station commits only. Hashes are filled after each
commit; no empty commit is created for a station that produced no change.

| Station | Commit | Responsibility | State |
| --- | --- | --- | --- |
| Owner direction acceptance | `aaeac84` | Translate explicit direction into bounded current/G0/future contracts | complete |
| Kernel G0 foundation | `99d8868` | Inert graph, schema and deterministic validator | complete |
| Kernel guards | `a0905a2` | Deterministic positive/negative tests for families, generations and edges | complete |
| DOOL and OCI contracts | `1c337a8` | Permanent lineage and necessary/sufficient inheritance semantics | complete |
| Historical exact reservations | `22eb52d` | Add exact paths to historical allowlists without weakening assertions | complete |
| Validation basis | `THIS_COMMIT_POST_COMMIT_HASH_RECORDED_IN_FINAL_EVIDENCE` | Final pre-checkpoint scope/allowlist basis | in progress |
| Checkpoint evidence | pending | Checkpoint, machine evidence and final ledger | pending |

## Protected scope

No change is permitted to `api.py`, P1 routes, product UI, HTML, CSS,
JavaScript, i18n, backend, payload, runtime, execution, providers,
integrations, stores, secrets, P0/P1/P3/P4, widgets or Request Draft Panel.
The graph validator is development-only and has no runtime side effects.

## Publication rule

Validation basis and final evidence must remain distinct. The final evidence
does not embed its own containing commit hash; post-fetch `HEAD`, `origin/main`
and `0/0` are recorded by the mission report after remote verification.
