# Roadmap 3.x - Legacy Route Disposition

## Scope

This document records the B-2 disposition attempt for
`roadmap_3x_macro_01_security_legacy_canonical_alignment` after the published
security-boundary piece `be5986e`. It is a static disposition record. It does
not claim deployment exposure, external consumers, runtime reachability or
canonical route coverage.

The source-of-truth route census remains the published Roadmap 3.2 evidence:
36 registered routes, 22 GET, 12 POST, 1 PUT and 1 DELETE. The current source
still has the same census. The root route is included in the 36-route count.

## Disposition vocabulary

Every route receives exactly one primary destination. `UNKNOWN` is intentional
when ownership, external consumers, canonical successor or deployment scope
cannot be demonstrated. `UNKNOWN` does not authorize mutation or retirement.

| Destination | Meaning in this checkpoint |
| --- | --- |
| `KEEP_CANONICAL` | Not assigned: canonical route authority is not demonstrated. |
| `MIGRATE_TO_CANONICAL` | Not assigned: successor/owner equivalence is not demonstrated. |
| `REPLACE_WITH_SUCCESSOR` | Not assigned: no successor equivalence is demonstrated. |
| `INTERNAL_ONLY` | Not assigned: deployment and caller boundary are not demonstrated. |
| `REMOVE` | Not assigned: consumer and compatibility proof are absent. |
| `UNKNOWN` | Evidence is insufficient; preserve the route and stop mutation. |

## Complete route disposition table

`UI` means a current static UI reference was found where noted. `TEST` means
repository test or fixture references, not production consumption. External
consumers remain unknown unless separately demonstrated. `SUCCESSOR_NONE` means
no canonical successor was proven, not that no future successor can exist.

| Route ID | Method | Path | Current purpose / consumers | Write or reachability risk | Destination | Successor / migration | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `api_status_get` | GET | `/api/status` | Status/readiness read; UI | Supervisor/provider metadata path; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE`; owner evidence pending | `api.py::get_status`; 3.2 route record |
| `api_memory_get` | GET | `/api/memory` | Memory/admin read; UI admin panel | Sensitive memory exposure; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE`; owner evidence pending | `api.py::get_memory_snapshot`; 3.2 route record |
| `api_logs_get` | GET | `/api/logs` | Log tail read; UI admin panel | Raw log exposure; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE`; sanitized read contract not connected | `api.py::get_logs`; 3.2 route record |
| `api_metrics_dynamic_get` | GET | `/api/metrics/dynamic` | Dynamic domain metrics read | Domain/evolution exposure; deployment unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_dynamic_metrics`; 3.2 route record |
| `api_debate_start_post` | POST | `/api/debate/start` | Starts legacy debate background flow | Mutative orchestration; auth/activation unknown | `UNKNOWN` | `SUCCESSOR_NONE`; migration requires authority | `api.py::start_debate`; 3.2 route record |
| `api_validation_start_post` | POST | `/api/validation/start` | Starts legacy validation flow | Background state/persistence; domain boundary unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::start_validation`; 3.2 route record |
| `api_validation_next_get` | GET | `/api/validation/next` | Validation progress read | Domain data exposure; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_next_validation_info`; 3.2 route record |
| `api_validation_by_id_get` | GET | `/api/validation/{validation_id}` | Validation result read | Identifier ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_validation`; 3.2 route record |
| `api_validation_reveal_post` | POST | `/api/validation/{validation_id}/reveal` | Reveals validation result | State mutation; confirmation/auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::reveal_validation`; 3.2 route record |
| `api_ranking_get` | GET | `/api/ranking` | Ranking read | Domain data exposure; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_ranking`; 3.2 route record |
| `api_evolution_stats_get` | GET | `/api/evolucion/stats` | Evolution statistics read | Domain state exposure; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_evolucion_stats`; 3.2 route record |
| `api_evolution_reset_post` | POST | `/api/evolucion/reset` | Resets evolution cycle | Direct lifecycle/state mutation | `UNKNOWN` | `SUCCESSOR_NONE`; retirement blocked without owner | `api.py::reset_ciclo`; 3.2 route record |
| `api_debate_by_id_get` | GET | `/api/debate/{debate_id}` | Debate read | Conversation ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_debate`; 3.2 route record |
| `api_debates_get` | GET | `/api/debates` | Debate list read | Cross-owner listing risk; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::list_debates`; 3.2 route record |
| `api_chat_post` | POST | `/api/chat` | Legacy orchestration chat | Provider-capable Supervisor -> AgentManager -> ProviderRegistry bypass | `UNKNOWN` | `SUCCESSOR_NONE`; no provider migration authorized | `api.py::chat_endpoint`; bypass finding F-3.1-004 |
| `api_learn_post` | POST | `/api/learn` | Legacy memory learning write | Memory/vector persistence; ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::learn_endpoint`; 3.2 route record |
| `api_conversation_get` | GET | `/api/conversation/{conversation_id}` | Conversation read | Sensitive content ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_conversation`; 3.2 route record |
| `api_catalog_domain_creation_get` | GET | `/api/catalogs/domain-creation` | Domain creation catalog; UI | Catalog exposure; route auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_domain_creation_catalog_endpoint`; UI reference |
| `api_catalog_roles_get` | GET | `/api/catalogs/roles` | Global roles catalog; UI | Catalog exposure; route auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_roles_catalog_endpoint`; UI reference |
| `api_catalog_specializations_get` | GET | `/api/catalogs/specializations` | Specializations catalog; UI | Catalog exposure; route auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_specializations_catalog_endpoint`; UI reference |
| `api_domains_list_get` | GET | `/api/domains/list` | Domain listing; UI | Domain ownership/exposure unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_domains`; UI reference |
| `api_domain_profile_catalog_get` | GET | `/api/domains/{domain_id}/profile-catalog` | Domain profile catalog; UI | Domain ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_domain_profile_catalog_endpoint`; UI reference |
| `api_domain_agent_presets_get` | GET | `/api/domains/{domain_id}/agent-presets` | Preset listing; UI | Provider/model metadata exposure | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_domain_agent_presets_endpoint`; UI reference |
| `api_domain_agent_preset_match_get` | GET | `/api/domains/{domain_id}/agent-presets/match` | Preset matching; UI | Domain and profile ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_domain_agent_preset_match_endpoint`; UI reference |
| `api_domains_create_post` | POST | `/api/domains/create` | Domain creation write; UI | Direct domain directory/manifest write; partial coverage | `UNKNOWN` | `SUCCESSOR_NONE`; canonical materializer equivalence not proven | `api.py::create_domain_endpoint`; partial coverage finding |
| `api_agents_create_post` | POST | `/api/agents/create` | Agent materialization; UI | Agent/paper/memory writes; ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::create_agent_endpoint`; 3.2 route record |
| `api_settings_post` | POST | `/api/settings` | Provider/model/agent settings write | Secret input is now rejected; non-secret settings owner/auth unknown | `UNKNOWN` | `SUCCESSOR_NONE`; F-003 storage owner pending | `api.py::save_settings`; F-003 |
| `api_settings_get` | GET | `/api/settings` | Settings read | Legacy persisted shape and ownership unknown; api_key is removed from response | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_settings`; F-003 |
| `api_agent_model_recommendation_post` | POST | `/api/agents/model-recommendation` | Provider/model recommendation; UI | Provider metadata/health path; no invocation performed | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_model_recommendation`; 3.2 route record |
| `api_hardware_profile_get` | GET | `/api/system/hardware-profile` | Hardware profile read | Local probe semantics; deployment unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_hardware_profile`; 3.2 route record |
| `api_model_compatibility_post` | POST | `/api/system/model-compatibility` | Model compatibility evaluation; UI | Provider/model metadata path; auth unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::get_model_compatibility`; UI reference |
| `api_agents_list_get` | GET | `/api/agents/list` | Agent listing; UI/admin | Sensitive provider/model fields; ownership unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::list_agents`; UI reference |
| `api_agent_update_put` | PUT | `/api/agents/{agent_id}` | Agent JSON update; UI | Direct agent/memory write; no route authz | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::update_agent`; 3.2 route record |
| `api_agent_delete_delete` | DELETE | `/api/agents/{agent_id}` | Agent/paper/vector deletion; UI | Direct unlink/rmtree candidates; no confirmation route | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::delete_agent`; 3.2 route record |
| `api_agent_regenerate_paper_post` | POST | `/api/agents/{agent_id}/regenerate-paper` | Paper regeneration; tests/UI lineage | Paper/config writes and optional provider path | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::regenerate_agent_paper`; 3.2 route record |
| `root_get` | GET | `/` | Static UI root; local browser | Exposure and hosting edge unknown | `UNKNOWN` | `SUCCESSOR_NONE` | `api.py::root`; `start_api.bat` |

## Counts and gate

| Destination | Count |
| --- | ---: |
| `KEEP_CANONICAL` | 0 |
| `MIGRATE_TO_CANONICAL` | 0 |
| `REPLACE_WITH_SUCCESSOR` | 0 |
| `INTERNAL_ONLY` | 0 |
| `REMOVE` | 0 |
| `UNKNOWN` | 36 |

No route is marked `REMOVE`; therefore no removed-route proof exists and no
retirement was performed. No compatibility wrapper or internal-only boundary
was created. No successor map is asserted because semantic equivalence and
ownership are not demonstrated.

The explicit `UNKNOWN` classification is the B-2 stop condition. The route
disposition contract is complete as an inventory, but B-2 cannot close until
Direction/Architect resolves the bridge, owner, successor and retirement
policy for the live legacy surface. No B-3 execution follows this stop.

## B-3 coverage snapshot

| Classification | Before | After this mission |
| --- | ---: | ---: |
| `CANONICAL_CONTROL_PLANE_COVERED` | 0 | 0 |
| `PARTIALLY_COVERED` | 1 | 1 |
| `LEGACY_BYPASS_DEMONSTRATED` | 2 | 2 |
| `COVERAGE_NOT_DEMONSTRATED` | 33 | 33 |
| `NOT_APPLICABLE` | 0 | 0 |

The CORS and settings boundary fixes do not constitute canonical control-plane
coverage. `/api/chat` remains a legacy provider-capable bypass. `/api/settings`
remains a legacy settings route, now with raw `api_key` persistence and
response exposure blocked, but without route identity/authorization or a final
settings owner contract.

## Frontier record

- `F-001`: local startup configuration is demonstrated; current external exposure and traffic remain `UNKNOWN_EXTERNAL_EXPOSURE`.
- `F-002`: dissolved for the authorized source boundary; CORS now uses an explicit allowlist, default local origin, deny on wildcard/invalid configured origins, minimum methods/headers and credentials disabled.
- `F-003A`: dissolved for raw API-key persistence and response exposure; secret values were not read or printed by the audit.
- `F-003B`: remains conditional for ownership, non-secret settings persistence, deployment storage and route authorization.
- `F-004`: reached as a true hard frontier; no route-level bridge/retirement/successor authority is available for the complete live legacy surface.
- `F-005`: not executed because B-2 stopped before canonical adapter alignment.

## Non-remediation declarations

No provider, runtime, agent, model, integration, external service, deployment,
business-data mutation, UI redesign, new endpoint, new identity system or API
generation was created. B-4, B-5, B-6 and B-7 were not entered.
