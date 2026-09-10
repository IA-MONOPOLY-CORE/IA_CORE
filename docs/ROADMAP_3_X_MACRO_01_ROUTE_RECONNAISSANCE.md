# Roadmap 3.x Macro-Mission 01 - F-004 Route Reconnaissance

Mission: `roadmap_3x_macro_01_security_legacy_canonical_alignment`

This record recalculates F-004 after the initial safe pause. It preserves both
green commits and does not change product behavior. The purpose is to prove
that every `UNKNOWN` route was investigated, rather than treating the initial
36-row inventory as sufficient evidence by itself.

## Recalculation result

| Item | Result |
| --- | --- |
| Initial classification | `TRUE_HARD_FRONTIER` for an undifferentiated 36-route surface |
| Policy-level frontier | Dissolved by Direction's six-destination policy |
| Remaining work | Route-specific reconnaissance and coherent-piece discovery |
| Final route-level result | No route had enough semantic, owner and consumer evidence for a non-`UNKNOWN` destination |
| B-2 result | `PASS_UNKNOWN_QUALITY_GATE` |
| B-3 result | Entered only after this record and its guards passed |

`UNKNOWN` here means `INVESTIGATED + INSUFFICIENT_EVIDENCE`.
`UNKNOWN != NOT_INVESTIGATED`. It does not authorize mutation, retirement or
public exposure.

## Evidence surfaces inspected

- `api.py` route decorators, handler bodies, imports and direct call graph.
- `ui/web/index.html`, `ui/web/admin-panels.js` and `ui/web/domains.js`.
- Python callsites, tests, fixtures, scripts and startup files.
- `core/catalog_registry.py`, `core/domain_registry.py`, `core/supervisor.py`,
  `core.model_recommendation`, `memory/manager.py` and Loteria domain modules.
- Canonical contract/control-plane modules and tests, including permission,
  secret, activation, readiness, internal UI, exposure, request envelope,
  dispatcher, confirmation and response-adapter contracts.
- `docs/DOMAIN_CREATION_ROUTES_AUDIT.md`, architecture decisions and the
  published Roadmap 3.2 route evidence.
- Git history and the current tracked source. No application import, server
  startup, provider call, network call or secret-value read was performed.

## Coherent pieces

| Piece | Routes | Derived current owner | Canonical successor result | Destination pattern |
| --- | --- | --- | --- | --- |
| `PIECE_STATUS_OBSERVABILITY_MEMORY` | `/api/status`, `/api/memory`, `/api/logs`, `/api/metrics/dynamic`, `/api/learn`, `/api/conversation/{conversation_id}` | `Supervisor`, `MemoryManager`, local log/session stores, Loteria evolution | No route-connected canonical read/learning owner; canonical contracts are contract-only | `UNKNOWN` |
| `PIECE_CHAT_ORCHESTRATION` | `/api/debate/start`, `/api/debate/{debate_id}`, `/api/debates`, `/api/chat` | `Supervisor.orchestrate_async`, `AgentManager`, `ProviderRegistry`, in-memory debate/conversation stores | Canonical permission/activation boundaries exist but no API adapter or route-level authz path is demonstrated | `UNKNOWN` |
| `PIECE_LOTERIA_VALIDATION_EVOLUTION` | `/api/validation/start`, `/api/validation/next`, `/api/validation/{validation_id}`, `/api/validation/{validation_id}/reveal`, `/api/ranking`, `/api/evolucion/stats`, `/api/evolucion/reset` | `domains/loteria` validation/evolution/database modules plus in-memory stores | No generic canonical successor for this domain-specific lifecycle is demonstrated | `UNKNOWN` |
| `PIECE_CATALOG_DOMAIN_READS` | `/api/catalogs/domain-creation`, `/api/catalogs/roles`, `/api/catalogs/specializations`, `/api/domains/list`, `/api/domains/{domain_id}/profile-catalog`, `/api/domains/{domain_id}/agent-presets`, `/api/domains/{domain_id}/agent-presets/match` | `core.catalog_registry` and `core.domain_registry` | Current service owners are clear, but canonical control-plane exposure/authz equivalence is not demonstrated | `UNKNOWN` |
| `PIECE_DOMAIN_MATERIALIZATION` | `/api/domains/create` | `core.domain_registry.create_domain` through the legacy API adapter | Internal preview/materialization direction is documented; no enabled canonical materializer or HTTP adapter exists | `UNKNOWN` |
| `PIECE_WORKFORCE_AGENT_LIFECYCLE` | `/api/agents/create`, `/api/agents/list`, `/api/agents/{agent_id}`, `/api/agents/{agent_id}`, `/api/agents/{agent_id}/regenerate-paper` | `core.domain_registry`, agent config/paper schemas, `mejorar_papers.py`, filesystem and vector-memory helpers | Agent/permission/active contracts exist, but no route-connected canonical lifecycle adapter or confirmation path is demonstrated | `UNKNOWN` |
| `PIECE_SETTINGS` | `/api/settings` GET/POST | `memory/user_settings.json`, `config.py` read path and `api.py` compatibility handler | No canonical settings owner or route authorization contract is demonstrated; raw secret path is blocked by B-1 | `UNKNOWN` |
| `PIECE_PROVIDER_HARDWARE` | `/api/agents/model-recommendation`, `/api/system/hardware-profile`, `/api/system/model-compatibility` | `core.model_recommendation`, hardware profile helper, `Supervisor.providers` | Model/activation boundaries exist as contracts; provider/hardware route ownership and exposure are not reconciled | `UNKNOWN` |
| `PIECE_HOSTING_ROOT` | `/` | `api.py` static mount and `start_api.bat` | No deployment/hosting owner or external consumer boundary is available locally | `UNKNOWN` |

No piece had a deterministic migration, replacement, internalization or
removal action that could be executed without adding authority, compatibility
or product semantics. Therefore there are no material product changes in this
recalculation and no fake no-diff commits.

## Consumer map

| Consumer evidence | Routes |
| --- | --- |
| `ui/web/admin-panels.js` | `/api/status`, `/api/memory`, `/api/logs`, `/api/agents/list` |
| `ui/web/domains.js` | `/api/catalogs/domain-creation`, `/api/domains/list`, `/api/domains/create` |
| `ui/web/index.html` | `/api/catalogs/roles`, `/api/catalogs/specializations`, `/api/domains/{domain_id}/profile-catalog`, `/api/domains/{domain_id}/agent-presets/match`, `/api/agents/model-recommendation`, `/api/system/model-compatibility`, `/api/agents/list`, `/api/agents/create`, `/api/agents/{agent_id}`, `/api/status` |
| Repository tests and fixtures | Catalog, domain, agent, paper, deletion, admin-panel and API route tests; these are test consumers, not proof of deployment consumers |
| Python route-to-route callers | None demonstrated; handlers call local modules directly |
| External/deployed consumers | Unknown; no deployment or traffic evidence is available in the repository |

## Owner map and successor map

| Capability family | Derived owner | Canonical artifact checked | Result |
| --- | --- | --- | --- |
| Catalogs | `core.catalog_registry` | Catalog schemas/loaders and tests | Current owner derived; public canonical control-plane adapter absent |
| Domains | `core.domain_registry` plus domain state/materialization helpers | Domain registry, identity, state, preview and route audit | Current owner derived; public materializer is not enabled |
| Agents/papers | Agent config/paper schemas, `core.domain_registry`, `mejorar_papers.py` | Agent permission/active contracts and lifecycle docs | Current storage owner derived; route lifecycle adapter absent |
| Orchestration/chat | `core.supervisor`, `agents.manager`, `providers.registry` | Permission, activation, invocation and readiness contracts | Provider-capable chain derived; permission/activation bridge absent |
| Memory/learning | `memory.manager`, `core.memoria_perpetua`, local stores | Secret/output/readiness contracts | Current persistence path derived; canonical retention/ownership contract absent |
| Settings | `memory/user_settings.json` compatibility path and `config.py` read path | Secret policy and B-1 settings guard | Raw secret path blocked; non-secret owner unresolved |
| Provider/hardware | `core.model_recommendation`, hardware profile helper, provider registry | Model invocation and activation boundaries | Current helper owner derived; route boundary unresolved |
| Loteria lifecycle | `domains.loteria.*` modules | Generic control-plane contracts | Domain owner derived; generic successor absent |
| Hosting | `api.py` and `start_api.bat` | No deployment artifact | Local startup path only; external owner unknown |

No successor map can be promoted because every apparent successor is either a
contract-only artifact with no route adapter, a domain-specific implementation
with unresolved external scope, or a future internal materialization path.

## UNKNOWN quality records

Every row below was checked against the evidence surfaces above and the
published Roadmap 3.2 record. The repeated fields are intentional: they make
the quality gate auditable per route, not only per family.

| Route | Unknown reason | Search surfaces checked | Caller evidence checked | Contract evidence checked | Canonical owner checked | Successor checked | External consumer risk | Evidence that would resolve it |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `GET /api/status` | route authz and deployment scope unresolved | `api.py`, UI, tests, startup, docs | admin panel, main UI, tests | readiness, exposure, response contracts | Supervisor/provider path | no route adapter | public status/provider metadata exposure | deployment boundary, route owner/authz, response policy |
| `GET /api/memory` | memory ownership and sensitivity unresolved | `api.py`, admin UI, memory modules, tests | admin panel, tests | secret/output/readiness contracts | Supervisor/MemoryManager | no canonical memory read route | memory content exposure | consumer identity, retention owner, sanitized contract |
| `GET /api/logs` | log sensitivity and admin boundary unresolved | `api.py`, admin UI, log config, tests | admin panel, tests | output/exposure contracts | local log/session stores | no sanitized log successor | raw logs may contain sensitive data | deployment/admin authz and sanitized response contract |
| `GET /api/metrics/dynamic` | Loteria metric ownership and exposure unresolved | `api.py`, Loteria modules, tests/docs | no current UI caller found; test/docs evidence | readiness/output contracts | Loteria evolution | no generic metrics adapter | domain metrics exposure | owner, audience and metric sensitivity contract |
| `POST /api/debate/start` | background orchestration authority unresolved | `api.py`, UI, tests, supervisor/docs | no current UI caller; tests/docs | permission, activation, runtime, confirmation contracts | Supervisor/orchestration | no route adapter | unauthenticated orchestration trigger | authorized internal caller and activation bridge |
| `GET /api/debate/{debate_id}` | debate store ownership unresolved | `api.py`, tests, supervisor/docs | tests/docs; no UI caller | output/readiness contracts | in-memory debate store/Supervisor | no canonical debate read route | cross-owner result exposure | owner, scope and stable response contract |
| `GET /api/debates` | debate listing ownership unresolved | `api.py`, tests/docs | tests/docs; no UI caller | output/exposure contracts | in-memory debate store | no canonical list route | cross-owner listing exposure | owner, scope and authz contract |
| `POST /api/chat` | provider-capable bypass and credentials unresolved | `api.py`, Supervisor, agents, providers, tests/docs | no current UI caller; source chain and tests/docs | permission, activation, invocation, readiness, secret contracts | Supervisor -> AgentManager -> ProviderRegistry | no canonical chat adapter | provider invocation and conversation exposure | explicit route owner, permission bridge, credential policy and consumer proof |
| `POST /api/validation/start` | Loteria background validation authority unresolved | `api.py`, Loteria modules, tests/docs | tests/docs; no current UI caller | activation/runtime/confirmation contracts | Loteria validation/evolution | no generic validation successor | background state mutation | authorized domain owner and lifecycle contract |
| `GET /api/validation/next` | validation resource ownership unresolved | `api.py`, Loteria modules, tests/docs | tests/docs; no current UI caller | output/readiness contracts | Loteria evolution/database | no generic validation read route | domain state exposure | owner and response scope |
| `GET /api/validation/{validation_id}` | validation identifier ownership unresolved | `api.py`, tests/docs, validation store | tests/docs | output/exposure contracts | in-memory validation store | no successor | cross-owner validation exposure | owner, tenant scope and stable contract |
| `POST /api/validation/{validation_id}/reveal` | reveal authority and confirmation unresolved | `api.py`, Loteria modules, tests/docs | tests/docs | confirmation/activation/runtime contracts | Loteria reveal function | no successor | irreversible/result disclosure risk | confirmation and lifecycle authority |
| `GET /api/ranking` | domain ranking owner unresolved | `api.py`, Loteria modules, tests/docs | tests/docs | output/readiness contracts | Loteria evolution | no generic ranking successor | domain intelligence exposure | owner and audience contract |
| `GET /api/evolucion/stats` | evolution state owner unresolved | `api.py`, Loteria modules, tests/docs | tests/docs | output/readiness contracts | Loteria evolution | no generic evolution successor | state exposure | owner and stable response policy |
| `POST /api/evolucion/reset` | lifecycle reset authority unresolved | `api.py`, Loteria modules, tests/docs | tests/docs | confirmation/activation/runtime contracts | Loteria evolution | no successor | destructive state mutation | explicit owner, confirmation and rollback policy |
| `POST /api/learn` | memory/vector retention owner unresolved | `api.py`, memory modules, tests/docs | tests/docs; no UI caller | secret/output/write contracts | `core.memoria_perpetua` and vector path | no canonical learning route | user content and vector persistence | retention owner, content policy and authenticated caller |
| `GET /api/conversation/{conversation_id}` | conversation owner and sensitivity unresolved | `api.py`, tests/docs | tests/docs; no UI caller | secret/output contracts | in-memory conversation store | no canonical conversation route | sensitive conversation disclosure | owner, scope and response policy |
| `GET /api/catalogs/domain-creation` | public catalog authz unresolved | `api.py`, domains UI, catalog module, tests | domains UI, tests | catalog and exposure contracts | `core.catalog_registry` | no control-plane exposure adapter | catalog exposure | route owner/authz and stable public contract |
| `GET /api/catalogs/roles` | public catalog authz unresolved | `api.py`, main UI, catalog module, tests | main UI, tests | catalog and exposure contracts | `core.catalog_registry` | no control-plane exposure adapter | catalog exposure | route owner/authz and stable public contract |
| `GET /api/catalogs/specializations` | public catalog authz unresolved | `api.py`, main UI, catalog module, tests | main UI, tests | catalog and exposure contracts | `core.catalog_registry` | no control-plane exposure adapter | catalog exposure | route owner/authz and stable public contract |
| `GET /api/domains/list` | domain visibility owner and deployment scope unresolved | `api.py`, domains UI, domain registry, tests/docs | domains UI, tests | domain state/exposure contracts | `core.domain_registry` | no control-plane exposure adapter | domain metadata exposure | owner, visibility and route authz |
| `GET /api/domains/{domain_id}/profile-catalog` | domain ownership/authz unresolved | `api.py`, main UI, domain registry, tests | main UI, tests | profile/catalog contracts | `core.domain_registry` | no control-plane exposure adapter | profile metadata exposure | owner and domain scope policy |
| `GET /api/domains/{domain_id}/agent-presets` | workforce owner and provider metadata scope unresolved | `api.py`, domain registry, tests/docs | tests/docs; no direct current UI caller found | agent/preset/exposure contracts | `core.domain_registry` | no control-plane exposure adapter | provider/model metadata exposure | workforce owner and response policy |
| `GET /api/domains/{domain_id}/agent-presets/match` | workforce owner and matching authority unresolved | `api.py`, main UI, domain registry, tests | main UI, tests | agent/preset/permission contracts | `core.domain_registry` | no control-plane exposure adapter | profile/provider metadata exposure | owner and stable matching contract |
| `POST /api/domains/create` | public materialization successor not enabled | `api.py`, domains UI, domain registry, preview/materializer docs, tests | domains UI, tests; UI caller is legacy | domain identity/state/materialization contracts | `core.domain_registry.create_domain` | preview/internal materializer documented but not exposed | direct domain writes and unknown callers | enabled internal materializer, caller proof, confirmation and rollback |
| `POST /api/agents/create` | workforce owner and operational boundary unresolved | `api.py`, main UI, agent schemas, tests/docs | main UI, tests | agent permission/active/paper contracts | domain registry, config/paper helpers | no route-connected canonical lifecycle adapter | agent/paper/memory writes | owner, confirmation and sandbox/product boundary |
| `GET /api/settings` | settings owner and persisted shape unresolved | `api.py`, settings file, tests/docs | no current UI caller found; tests/docs | secret policy and output contracts | compatibility handler/config read path | no canonical settings service | settings metadata exposure | settings owner, response schema and route authz |
| `POST /api/settings` | non-secret settings owner and route authz unresolved | `api.py`, settings file, config, tests/docs | no current UI caller found; tests/docs | secret policy, write and output contracts | compatibility handler and config read path | no canonical settings service | settings mutation and external caller risk | owner/authz/storage policy; raw secret remains blocked |
| `POST /api/agents/model-recommendation` | provider reachability and route owner unresolved | `api.py`, main UI, model recommendation, providers, tests/docs | main UI, tests | invocation/activation/provider contracts | `core.model_recommendation` plus Supervisor providers | no control-plane recommendation adapter | provider metadata and health exposure | owner, provider policy and authz |
| `GET /api/system/hardware-profile` | local probe policy and route owner unresolved | `api.py`, hardware helper, tests/docs | tests/docs; no current UI caller found | output/exposure contracts | hardware profile helper | no control-plane hardware route | local hardware exposure | owner and probe disclosure policy |
| `POST /api/system/model-compatibility` | provider/model boundary unresolved | `api.py`, main UI, model recommendation, tests/docs | main UI, tests | invocation/activation contracts | compatibility helper and hardware profile | no control-plane compatibility adapter | provider/model metadata exposure | owner, authz and stable contract |
| `GET /api/agents/list` | workforce owner and sensitive fields unresolved | `api.py`, UI, agent registry, tests/docs | admin panel, main UI, tests | agent permission/output contracts | Supervisor AgentManager plus domain registry/files | no canonical workforce read route | provider/model/system prompt metadata | workforce owner and response policy |
| `PUT /api/agents/{agent_id}` | lifecycle owner and confirmation unresolved | `api.py`, main UI, agent helpers, tests/docs | main UI, tests | permission/active/confirmation/write contracts | domain registry/filesystem agent config | no canonical lifecycle adapter | direct agent mutation | owner, confirmation and rollback |
| `DELETE /api/agents/{agent_id}` | deletion authority and rollback unresolved | `api.py`, main UI, agent helpers, tests/docs | main UI, tests | permission/confirmation/rollback contracts | filesystem/vector-memory helpers | no canonical deletion route | irreversible deletion | owner, confirmation and recovery proof |
| `POST /api/agents/{agent_id}/regenerate-paper` | paper owner and optional provider path unresolved | `api.py`, paper helper, tests/docs | tests/docs; no current UI caller found | agent/paper/provider contracts | `mejorar_papers.py` and domain paths | no canonical paper lifecycle adapter | paper/config mutation and provider path | owner, provider policy and rollback |
| `GET /` | deployment/hosting owner unknown | `api.py`, static mount, `start_api.bat`, tests/docs | local startup/browser docs; no deployment proof | exposure/hosting evidence | API static mount | no hosting successor in repo | external public exposure | deployment inventory and hosting boundary |

## Learning gate

| Piece | Observation | Pattern | State | Reused by later piece |
| --- | --- | --- | --- | --- |
| `PIECE_CATALOG_DOMAIN_READS` | Existing core registry owners can be derived, but route exposure is not equivalent to canonical control-plane ownership | `DERIVE_SERVICE_OWNER_BEFORE_DESTINATION` | `OBSERVED` | Domain materialization and workforce pieces |
| `PIECE_CHAT_ORCHESTRATION` | A callable provider chain is not evidence of permission or activation authority | `CALLABLE_CHAIN_IS_NOT_AUTHORIZED_ROUTE` | `OBSERVED` | Provider/hardware and B-3 coverage |
| `PIECE_DOMAIN_MATERIALIZATION` | Existing domain primitive is safe only under the documented internal/fixture boundary | `LEGACY_WRITE_NEEDS_BOUNDARY_PROOF` | `OBSERVED` | Workforce lifecycle |
| `PIECE_SETTINGS` | Raw secret blocking can close one risk without resolving non-secret settings ownership | `PARTIAL_SECURITY_FIX_DOES_NOT_ASSIGN_OWNER` | `OBSERVED` | B-3 high-risk route checks |
| `PIECE_STATUS_OBSERVABILITY_MEMORY` | Read-only HTTP method does not imply safe exposure | `READ_ONLY_METHOD_IS_NOT_READ_AUTHZ` | `OBSERVED` | B-3 coverage checks |
| `PIECE_WORKFORCE_AGENT_LIFECYCLE` | Existing artifact schemas are not a route-connected lifecycle owner | `CONTRACT_EXISTS_IS_NOT_ROUTE_ADAPTER` | `OBSERVED` | B-3 coverage checks |

No observation was promoted automatically. The earlier checkpoint-bounded
historical-guard learning remains valid and was reused by the current test
strategy.
