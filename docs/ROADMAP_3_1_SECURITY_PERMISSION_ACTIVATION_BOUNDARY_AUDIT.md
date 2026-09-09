# Roadmap 3.1 - Security, Permission and Activation Boundary Audit

## A. Mission identity and decision boundary

- **Mission ID:** `roadmap_3_1_security_permission_activation_boundary_read_only_audit`
- **Mission type:** `BACKEND_SECURITY_ACTIVATION_BOUNDARY_READ_ONLY_AUDIT`
- **Mode:** `READ_ONLY_PRODUCT_AUDIT`
- **Baseline:** `4c898eae74c0a6c59cda4e659ec6a1e2d2d3641a`
- **Repository:** `C:\IA_CORE`
- **Authority order:** current repository state, Git/checkpoints/contracts/tests, GOKV/OCI, current canonical documentation, then historical material.
- **Historical ZIP:** `IA_CORE_clean(1).zip` was classified as `HISTORICAL_REPOSITORY_SNAPSHOT = NON_AUTHORITATIVE_FOR_CURRENT_STATE`; it was not opened or used.

This document records a static, reproducible audit. It does not select a remediation, change architecture, change authentication or authorization, narrow CORS, alter secret storage, activate providers, or advance the roadmap. The exhaustive machine-readable route and boundary evidence is in [ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json](C:/IA_CORE/docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json).

## B. Method and station compilation

The block was compiled from the first true non-deterministic frontier rather than from an arbitrary station count:

| Station | Closed surface | Evidence | Internal gate | State |
| --- | --- | --- | --- | --- |
| S0 | Preflight and authority | Git state, 3.0/3.0.A checkpoints, OCI manifest/pack | Authority, scope, secret-safety | PASS |
| S1 | API surface, auth/authz, CORS and exposure | AST-only route census plus `api.py` source | Coverage, evidence, negative-evidence | PASS |
| S2 | Secrets, providers, network, writes and activation | `config.py`, `Supervisor`, `AgentManager`, registry/adapters and gates | No-side-effect, frontier | PASS |
| S3 | Trust graph, findings, tests and checkpoint | Manifest/document correspondence and safe validation | Test, diff, closure | PASS |

The non-deterministic frontier is the point where proof would require deployment, traffic, credentials, network/provider execution, or a product remediation decision. The audit documents that frontier and does not cross it.

## C. Source census and baseline comparison

The current count was obtained from `git ls-files` at the mission baseline and a read-only AST scan of `api.py`:

| Measure | Current inventory | Roadmap 3.0 documented inventory | Interpretation |
| --- | ---: | ---: | --- |
| Tracked files | 1,614 | 1,598 | Different category/exclusion scope; not an automatic regression |
| Python files | 820 | 802 | Later documentary/test additions are included in current tracked inventory |
| JSON files | 198 | 179 | Later fixtures/knowledge artifacts are included |
| Markdown files | 578 | 560 | Later 3.0/3.0.A documentation is included |
| Non-test Python | 213 | 217 | Different test/path classification; current source was not inferred from the old count |
| Test-surface files | 626 | 594 | Later roadmap test additions are included |

The 3.0 values are retained as historical checkpoint evidence. The current route census is independent and authoritative for this mission: **36 routes, 22 GET, 12 POST, 1 PUT and 1 DELETE, therefore 14 mutative routes**.

## D. Route-by-route inventory

All routes are registered on the FastAPI `app` in `api.py`. Source registration is not treated as proof of mounting, deployment, network reachability, authentication, authorization, or actual invocation. Every route has `authentication = NOT_DEMONSTRATED` unless explicitly marked `NOT_APPLICABLE`, and every route is subject to the source-level wildcard CORS middleware at `api.py:165-175`.

| Route | Method | Registration | Handler | Auth | Authz | Provider | Write | Severity |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `/api/status` | GET | 505 | `get_status:506` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/memory` | GET | 577 | `get_memory_snapshot:578` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/logs` | GET | 611 | `get_logs:612` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/metrics/dynamic` | GET | 628 | `get_dynamic_metrics:629` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/debate/start` | POST | 677 | `start_debate:678` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/validation/start` | POST | 708 | `start_validation:709` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/validation/next` | GET | 764 | `get_next_validation_info:765` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/validation/{validation_id}` | GET | 798 | `get_validation:799` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/validation/{validation_id}/reveal` | POST | 806 | `reveal_validation:807` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/ranking` | GET | 822 | `get_ranking:823` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/evolucion/stats` | GET | 830 | `get_evolucion_stats:831` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/evolucion/reset` | POST | 843 | `reset_ciclo:844` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/debate/{debate_id}` | GET | 854 | `get_debate:855` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/debates` | GET | 862 | `list_debates:863` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/chat` | POST | 872 | `chat_endpoint:873` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/learn` | POST | 948 | `learn_endpoint:949` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/conversation/{conversation_id}` | GET | 971 | `get_conversation:972` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/catalogs/domain-creation` | GET | 985 | `get_domain_creation_catalog_endpoint:986` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/catalogs/roles` | GET | 994 | `get_roles_catalog_endpoint:995` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/catalogs/specializations` | GET | 1003 | `get_specializations_catalog_endpoint:1004` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/domains/list` | GET | 1016 | `get_domains:1017` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/domains/{domain_id}/profile-catalog` | GET | 1027 | `get_domain_profile_catalog_endpoint:1028` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/domains/{domain_id}/agent-presets` | GET | 1040 | `get_domain_agent_presets_endpoint:1041` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/domains/{domain_id}/agent-presets/match` | GET | 1059 | `get_domain_agent_preset_match_endpoint:1060` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/domains/create` | POST | 1096 | `create_domain_endpoint:1097` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/agents/create` | POST | 1180 | `create_agent_endpoint:1181` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | CONFIG_GATED | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/settings` | POST | 1449 | `save_settings:1450` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | CONFIG_GATED | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/settings` | GET | 1505 | `get_settings:1506` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | CONFIG_GATED | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/agents/model-recommendation` | POST | 1526 | `get_model_recommendation:1527` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | SOURCE_CALLABLE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/system/hardware-profile` | GET | 1603 | `get_hardware_profile:1604` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/system/model-compatibility` | POST | 1628 | `get_model_compatibility:1629` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |
| `/api/agents/list` | GET | 1647 | `list_agents:1648` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P1 |
| `/api/agents/{agent_id}` | PUT | 1720 | `update_agent:1721` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | CONFIG_GATED | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/agents/{agent_id}` | DELETE | 1802 | `delete_agent:1803` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/api/agents/{agent_id}/regenerate-paper` | POST | 1836 | `regenerate_agent_paper:1837` | NOT_DEMONSTRATED | NOT_DEMONSTRATED | NOT_REACHABLE_FROM_ROUTE | ROUTE_REACHABLE_WRITE_CANDIDATE | P1 |
| `/` | GET | 1934 | `root:1935` | NOT_DEMONSTRATED | NOT_APPLICABLE | NOT_REACHABLE_FROM_ROUTE | NO_WRITE_PATH_DEMONSTRATED | P2 |

The full evidence object adds stores, subprocess/shell reachability, agent/orchestrator reachability, trust boundaries, controls, bypass candidates, positive evidence, limited negative evidence, confidence and unknowns for each row.

## E. Auth, authorization, exposure and CORS

### Authentication and authorization

The scoped source search and AST inspection did not demonstrate a route-local FastAPI `Depends`/`Security` identity dependency, OAuth/JWT/Bearer middleware, role/owner/tenant/resource authorization, or deny-by-default routing policy on the legacy app. This supports `NOT_DEMONSTRATED`; it does **not** support the stronger claim that an external hosting edge cannot exist. The corresponding external state remains `HOSTING_EDGE_UNKNOWN`.

The dedicated permission and internal-contract modules are evidence of a separate contract plane, not proof that every legacy route traverses that plane. In particular, no route registration in `api.py` was shown to dispatch through `runtime_activation_gate`, `attempt_factory` or `backend_internal_confirmation_gate`.

### CORS

`api.py:165-175` applies `CORSMiddleware` to the FastAPI app with:

- `allow_origins=["*"]`;
- `allow_methods=["*"]`;
- `allow_headers=["*"]`.

No versioned production override was established. `credentials`, deployment ingress, TLS, browser policy and hosting edge behavior remain unknown. The wildcard is therefore a confirmed source-level control finding, not a claim about every deployed environment.

## F. Secret-bearing settings flow

The route `POST /api/settings` accepts a parameter named `api_key` at `api.py:1450`. Without reading any value, static tracing establishes the following potential flow:

1. The handler places the supplied value, or an empty string, in a `settings` dictionary at `api.py:1469-1478`.
2. That dictionary is written to `memory/user_settings.json` at `api.py:1477-1478`.
3. If the parameter is truthy, the handler reads `config.py`, performs a string replacement, and writes `config.py` at `api.py:1480-1492`.
4. The success response structurally includes `settings`; no request was executed and no real response was observed.
5. No route-local redaction before settings object construction is demonstrated.

The audit did not open `.env`, private settings, keychains, credential stores, real persisted settings or any API key. The manifest records only the field name, source references and uncertainty. The NVIDIA adapter's credential lookup is recorded by variable name only; no credential value was read or copied.

## G. `/api/chat` and provider/network chain

The current source supports this potential legacy chain:

```text
POST /api/chat
  -> api.py:873 chat_endpoint
  -> core/supervisor.py:159-218 Supervisor.orchestrate_async
  -> agents/manager.py:247-305 provider association
  -> providers/registry.py:116-129 generate_with_fallback
  -> providers/nvidia_provider.py or providers/ollama_provider.py
  -> external NVIDIA HTTP or local Ollama HTTP boundary
```

This is classified as `SOURCE_CALLABLE` and `RUNTIME_REACHABLE_NOT_EXECUTED`, not as deployed or actually reachable. NVIDIA uses a requests boundary and a credential-bearing authorization header in source; Ollama uses urllib HTTP calls. No provider, model, DNS, socket, HTTP request, server, startup sequence or agent was invoked by this audit.

`GET /api/status` and `POST /api/agents/model-recommendation` also expose source-level provider metadata/health paths. `Supervisor.start` registers builtins, may configure fallback, starts memory/tools/agents and can preload Ollama based on configuration. That source chain is classified as startup/provider-capable and remains unexecuted.

## H. Activation and execution boundaries

| Gate | Static result | Boundary conclusion |
| --- | --- | --- |
| `api.py` lifecycle | Startup constructs `Supervisor`, optional loteria state, starts Supervisor; shutdown stops it | Startup policy and actual process exposure unknown |
| `core/runtime_activation_gate.py` | Runtime/execution/runner/worker/queue/tool/model/write/store/network/secret/host flags are `False`; contract-only module | Strong dedicated negative evidence, not global legacy coverage |
| `core/attempt_factory.py` | Factory/runtime/store/model/tool/external/API/UI flags are `False`; operational states are rejected | Contract-only and safe to inspect; no legacy route reference demonstrated |
| `core/active_executor.py` | Source exists; active path checks runtime, execution, external access, active contract and approval; dry-run is separate | Gated source, not invoked |
| `core/backend_internal_confirmation_gate.py` | Confirmation and service execution policy keep runtime/execution/UI runtime disabled | Contract validation only; legacy route integration not demonstrated |
| provider/config gate | NVIDIA credential and Ollama local service/config influence adapter behavior | Config-dependent; no external reachability claim |

The decisive limitation is coverage: dedicated contracts demonstrate their own blocked states, while the legacy `api.py -> Supervisor` chain does not prove that it crosses those contracts. That is a finding and an unknown, not a license to enable, bypass or redesign anything.

## I. Write and side-effect reachability

Static source confirms write candidates but not real writes. The main classified paths are:

- `/api/settings`: `memory/user_settings.json` and conditional `config.py` rewrite;
- `/api/agents/create`: agent config, paper and memory/vector candidates;
- `/api/domains/create`: domain filesystem/registry candidates;
- `/api/agents/{agent_id}` PUT/DELETE: agent files, paper and vector-memory candidates;
- `/api/agents/{agent_id}/regenerate-paper`: paper/config JSON;
- orchestration, validation, evolution, chat and learn routes: in-memory stores, memory, loteria/evolution and logging candidates.

The audit never provoked a write, opened operational stores, created a server, ran an agent, called a subprocess, or executed an adapter. The evidence distinguishes `ROUTE_REACHABLE_WRITE_CANDIDATE` from `PRODUCTIVE_REACHABILITY_UNKNOWN` and from contract-only blocked paths.

## J. Trust boundaries and bypass candidates

The manifest contains the boundary graph for client/API, handler, Supervisor, AgentManager, provider registry, adapters/network, settings/secrets, filesystem/stores, contract gates and deployment edge. The canonical compressed decisions are:

1. A client-to-API boundary exists with wildcard CORS and no demonstrated local identity dependency.
2. A legacy API-to-Supervisor boundary exists for orchestration and provider-capable routes.
3. Dedicated permission/runtime contracts exist but their coverage over legacy routes is not demonstrated.
4. Settings crosses from request input into secret-bearing persistence/config paths without a demonstrated route authz/redaction boundary.
5. Deployment/hosting edge is an external unknown and cannot be inferred from source absence.

Repeated route-level instances are compressed into findings while preserving route provenance in the manifest. These are **bypass candidates**, not exploitation claims.

## K. Findings

| ID | Severity | Confidence | Finding | Reachability |
| --- | --- | --- | --- | --- |
| F-3.1-001 | P1 | HIGH | Legacy route authentication and authorization not demonstrated | Registered; deployment unknown |
| F-3.1-002 | P1 | HIGH | Global CORS wildcard remains on FastAPI app | Source-confirmed; deployment override unknown |
| F-3.1-003 | P1 | HIGH | `/api/settings` is secret-bearing and writes settings/config paths | Route write candidate |
| F-3.1-004 | P1 | HIGH | `/api/chat` is a legacy provider-capable orchestration path | Source-callable; runtime not executed |
| F-3.1-005 | P1 | HIGH | Multiple mutation routes lack demonstrated route authz | Route write candidates |
| F-3.1-006 | P2 | HIGH | Dedicated gates are disabled but not proven global over legacy API | Contract-only; legacy coverage unknown |
| F-3.1-007 | P2 | MEDIUM | Provider/network reachability cannot be closed statically | Deployment/runtime unknown |

No P0 finding was established by this static audit. Each finding carries exact source references, condition, impact, unknowns and `REMEDIATION_NOT_DESIGNED_OUT_OF_SCOPE` in the manifest. No fix, replacement architecture, policy or roadmap step is proposed here.

## L. Unknowns and hard frontier

Preserved unknowns are deployment exposure, hosting-edge auth, actual traffic, secret storage posture, provider reachability, startup policy, legacy gate coverage, integration configuration, filesystem permissions and reconciliation of historical count scopes.

The hard frontier is **reached for any next action that would require external/runtime evidence or a product decision**, including live route checks, network/provider checks, credential checks, auth/authz design, CORS change, secret-storage change, runtime activation or remediation. It was recorded and not crossed. The deterministic audit itself remains within scope.

## M. Safety and non-remediation declaration

- No product, endpoint, handler, middleware, CORS, configuration, provider, agent, runtime, execution, store, dependency, UI or CI file was modified.
- No secret value, token, API key, private settings file, `.env` value or credential store was read, printed, copied or persisted.
- No network, DNS, socket, HTTP, browser, provider, model server, subprocess, server, runtime, execution or agent was started or invoked.
- No operational store or product filesystem write was performed.
- No remediation was designed; the report uses `REMEDIATION_NOT_DESIGNED_OUT_OF_SCOPE`.
- GOKV, DOOL and OCI remain unchanged. Any new operational learning intake is `NOT_APPLIED_REQUIRES_GOVERNANCE_REVIEW`.

## N. Validation plan and closure state

The focal, safe group, canonical and deep historical layers are recorded in the final checkpoint. The focal commands are:

```text
python -m json.tool docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_EVIDENCE.json
python -m pytest -q tests/test_roadmap_3_1_security_permission_activation_boundary_audit.py
git diff --check
```

This station closes only the documentary route/boundary evidence. The final decision, test results, station commits, diff proof and readiness are recorded in [ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_CHECKPOINT.md](C:/IA_CORE/docs/ROADMAP_3_1_SECURITY_PERMISSION_ACTIVATION_BOUNDARY_CHECKPOINT.md) after the authorized tests pass.
