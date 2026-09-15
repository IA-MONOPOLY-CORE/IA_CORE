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
| Validation basis | `703c1721d18b2ca43019aa5f84f1abcc297fda90` | Final pre-checkpoint scope/allowlist basis | complete |
| Checkpoint evidence | pending | Checkpoint, machine evidence and final ledger | in progress |

Level A: 82 focused tests passed, with `py_compile` and `git diff --check`
passing. Level B: 7032 tests passed, 6 skipped and 6 warnings. The warnings
are existing framework deprecations only. The tracked JSON census is 258,
versus 255 at baseline; the delta is the three canonical mission JSON files.

## Protected scope

No change is permitted to `api.py`, P1 routes, product UI, HTML, CSS,
JavaScript, i18n, backend, payload, runtime, execution, providers,
integrations, stores, secrets, P0/P1/P3/P4, widgets or Request Draft Panel.
The graph validator is development-only and has no runtime side effects.

## Publication rule

Validation basis and final evidence must remain distinct. The final evidence
does not embed its own containing commit hash; post-fetch `HEAD`, `origin/main`
and `0/0` are recorded by the mission report after remote verification.
