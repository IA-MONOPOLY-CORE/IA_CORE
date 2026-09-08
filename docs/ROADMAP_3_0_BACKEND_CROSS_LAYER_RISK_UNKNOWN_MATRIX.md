# Roadmap 3.0 N7 - Backend Cross-Layer Risk and Unknown Matrix

## Gate

`ROADMAP_3_0_N7_CROSS_LAYER_MATRIX_PASSED`

## Classification matrix

| Classification | Current evidence |
| --- | --- |
| `REAL_ACTIVE` | none observed in the current audit process; no runtime was started |
| `REAL_CONTROLLED` | sandbox materializers, artifact manifests, contract gates and internal read/validation services |
| `REAL_SANDBOX` | domain/preset/paper/agent/team materialization paths with operational-root rejection |
| `REAL_READ_ONLY` | static inventory, read models, catalog reads, docs and GOKV validators |
| `CODE_PRESENT_INACTIVE` | runtime activation flags, queue/worker/scheduler contracts, OpenAI placeholder, future services |
| `CALLABLE_BUT_GATED` | active executor, dry-run runner, internal dispatcher and approval/confirmation paths |
| `TEST_ONLY` | `tests/` source and checkpoint suites |
| `FIXTURE_ONLY` | `tests/fixtures/` and audit evidence fixtures |
| `DOCUMENTED_ONLY` | roadmap handoffs, future architecture notes and unexecuted mission manifests |
| `LEGACY` | `api.py`, `Supervisor`, legacy agents/providers, memory, Lotería DB/evolution paths |
| `FUTURE` | next-mission declarations and disabled runtime/execution expansion surfaces |
| `UNKNOWN_REQUIRES_AUDIT` | deployment exposure, actual server startup policy, route auth at hosting edge, secret storage posture, legacy caller traffic, integration configuration |

## Cross-layer risk matrix

| ID | Layers | Finding | Evidence status | Risk |
| --- | --- | --- | --- | --- |
| R1 | API -> provider -> credential | `/api/chat` can reach legacy orchestration/provider source; no route auth evidence | source-confirmed path, invocation not performed | P1 |
| R2 | API -> settings -> secret/config write | `/api/settings` accepts `api_key` and writes configuration; CORS is wildcard | source-confirmed write candidate | P1 |
| R3 | API -> agent/domain filesystem | create/update/delete/regenerate routes expose mutation candidates | source-confirmed candidate, deployment unknown | P1 |
| R4 | runtime contract -> legacy supervisor | disabled 3.x flags coexist with a legacy callable runtime path | source-confirmed coexistence | P2 |
| R5 | sandbox -> operational filesystem | materializers have explicit rejection/validation boundary | controlled evidence | P2 residual |
| R6 | provider -> network | NVIDIA/Ollama adapters are real but not invoked; availability/credential state unknown | source-confirmed, reachability unknown | P2 |
| R7 | agent/preset/paper/team -> activation | definitions and materializers exist; no active team/paper chain observed | mixed definition evidence | P2 |
| R8 | process primitive -> host | subprocess hardware/benchmark references exist | source-confirmed, not executed | P2 |
| R9 | legacy DB/memory -> product state | SQLite/JSON memory writes exist in legacy domain/application path | source-confirmed candidate | P2 |

## Counts and frontier

- Write/side-effect candidates: **60** across 30 non-test Python files.
- Execution paths: **1 legacy application execution chain** is source-reachable;
  the dedicated runtime plane is disabled/dry-run/gated.
- Network-capable references: **9**; provider adapters: **3** (2 real network
  adapters and 1 placeholder).
- Security boundaries inventoried: **10**; unguarded legacy boundaries: **4**
  (route auth, route authz, wildcard CORS, secret-bearing settings).
- Unknown boundaries requiring audit: **6** deployment/traffic/hosting/secret/
  integration questions; none were inferred as safe.
- No side effect was performed by this audit.

## N7 conclusion

The highest-value unknown is no longer “does backend code exist?” It is “what
legacy API surface is actually exposed and trusted in deployment, and what
permission boundary protects it?” That question determines whether provider,
memory, domain and filesystem candidates are merely source or real operational
risk.

