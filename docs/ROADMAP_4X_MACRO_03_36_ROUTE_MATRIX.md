# Roadmap 4.x Macro-Mission 03 - Legacy Route Matrix

## Integrity

The canonical adjudication contains exactly `36` routes. The matrix below is
one row per stable `route_id`; no adapter, migration, successor or consumer is
invented. The canonical source does not demonstrate an external consumer for
any deferred route. P4 local consumers are limited to the published API,
registry readers and tests; that is not external-consumer evidence.

- Duplicate route IDs: `0`.
- Duplicate method/path pairs: `0`.
- P4 routes treated internally: `7`.
- Routes remaining after P4: `29`.
- External state for every route: `REMAIN_DISABLED_OR_CONTAINED`.

## Matrix

| ID | Family | Method | Path | Historical disposition | Current internal state | External state | Main dependency | Known consumer | Risk | Next allowed treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `api_status_get` | P1 | GET | `/api/status` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | identity, audience, deployment, compatibility | not demonstrated | status/provider disclosure | bounded P1 identity/audience review |
| `api_memory_get` | P1 | GET | `/api/memory` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | memory owner, tenant scope, sanitization | not demonstrated | memory and retention disclosure | bounded P1 memory read contract |
| `api_logs_get` | P1 | GET | `/api/logs` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | admin identity, sink, retention, redaction | not demonstrated | log and secret disclosure | bounded P1 admin/log contract |
| `api_metrics_dynamic_get` | P1 | GET | `/api/metrics/dynamic` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | metric owner, audience, tenant scope | not demonstrated | operational disclosure | bounded P1 metrics contract |
| `api_debate_start_post` | P2 | POST | `/api/debate/start` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | orchestration, activation, provider, lifecycle | not demonstrated | write/provider activation | later P2 authority review |
| `api_validation_start_post` | P3 | POST | `/api/validation/start` | KEEP_AS_COMPATIBILITY_SURFACE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | lifecycle owner, confirmation, compatibility | not demonstrated | domain state mutation | later P3 compatibility review |
| `api_validation_next_get` | P3 | GET | `/api/validation/next` | KEEP_AS_COMPATIBILITY_SURFACE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | validation scope, compatibility | not demonstrated | wrong-scope read | later P3 read review |
| `api_validation_by_id_get` | P3 | GET | `/api/validation/{validation_id}` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | identifier owner, tenant scope, consumer evidence | not demonstrated | cross-scope disclosure | later P3 identifier review |
| `api_validation_reveal_post` | P3 | POST | `/api/validation/{validation_id}/reveal` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | reveal authority, confirmation, recovery | not demonstrated | irreversible disclosure/state transition | later P3 lifecycle review |
| `api_ranking_get` | P3 | GET | `/api/ranking` | KEEP_AS_COMPATIBILITY_SURFACE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | ranking owner, audience, tenant scope | not demonstrated | audience/tenant disclosure | later P3 read review |
| `api_evolution_stats_get` | P3 | GET | `/api/evolucion/stats` | KEEP_AS_COMPATIBILITY_SURFACE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | evolution owner, response policy, compatibility | not demonstrated | domain state disclosure | later P3 read review |
| `api_evolution_reset_post` | P3 | POST | `/api/evolucion/reset` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | destructive owner, confirmation, rollback | not demonstrated | destructive lifecycle mutation | later P3 recovery review |
| `api_debate_by_id_get` | P2 | GET | `/api/debate/{debate_id}` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | debate store owner, visibility, tenant scope | not demonstrated | persistence disclosure | later P2 read contract |
| `api_debates_get` | P2 | GET | `/api/debates` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | list visibility, store owner, tenant scope | not demonstrated | cross-tenant listing | later P2 list contract |
| `api_chat_post` | P2 | POST | `/api/chat` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | provider chain, credentials, caller, activation | not demonstrated | provider/network/activation | later P2 provider boundary |
| `api_learn_post` | P2 | POST | `/api/learn` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | memory retention, content owner, caller, tenant | not demonstrated | ungoverned persistence | later P2 learning contract |
| `api_conversation_get` | P2 | GET | `/api/conversation/{conversation_id}` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | conversation owner, response policy, retention | not demonstrated | conversation disclosure | later P2 retention contract |
| `api_catalog_domain_creation_get` | P4 | GET | `/api/catalogs/domain-creation` | KEEP_AS_COMPATIBILITY_SURFACE | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | catalog audience, tenant visibility, authorization, compatibility | local API/tests; external not demonstrated | unauthorized catalog read | preserve closed P4 boundary |
| `api_catalog_roles_get` | P4 | GET | `/api/catalogs/roles` | KEEP_AS_COMPATIBILITY_SURFACE | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | catalog audience, tenant visibility, authorization, compatibility | local API/tests; external not demonstrated | role/catalog confusion | preserve closed P4 boundary |
| `api_catalog_specializations_get` | P4 | GET | `/api/catalogs/specializations` | KEEP_AS_COMPATIBILITY_SURFACE | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | catalog audience, tenant visibility, authorization, compatibility | local API/tests; external not demonstrated | unauthorized catalog read | preserve closed P4 boundary |
| `api_domains_list_get` | P4 | GET | `/api/domains/list` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | domain visibility, ingress, tenant isolation, compatibility | local API/tests; external not demonstrated | enumeration/cross-tenant read | preserve closed P4 boundary |
| `api_domain_profile_catalog_get` | P4 | GET | `/api/domains/{domain_id}/profile-catalog` | KEEP_AS_COMPATIBILITY_SURFACE | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | domain ownership, visibility, tenant scope, compatibility | local API/tests; external not demonstrated | unauthorized domain read | preserve closed P4 boundary |
| `api_domain_agent_presets_get` | P4 | GET | `/api/domains/{domain_id}/agent-presets` | CONTAIN | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | workforce owner, provider metadata, tenant visibility | local API/tests; external not demonstrated | sensitive preset disclosure | preserve closed P4 boundary |
| `api_domain_agent_preset_match_get` | P4 | GET | `/api/domains/{domain_id}/agent-presets/match` | CONTAIN | INTERNAL_REMEDIATION_COMPLETE | `REMAIN_DISABLED_OR_CONTAINED` | matching authority, tenant scope, provider metadata | local API/tests; external not demonstrated | sanitized-match disclosure | preserve closed P4 boundary |
| `api_domains_create_post` | P5 | POST | `/api/domains/create` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | materializer, persistence, rollback, compatibility | not demonstrated | write/recovery blast radius | later P5 materialization review |
| `api_agents_create_post` | P6 | POST | `/api/agents/create` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | workforce, sandbox, provider, lifecycle | not demonstrated | activation and provider | later P6 workforce review |
| `api_settings_post` | P7 | POST | `/api/settings` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | settings owner, storage, secrets, rotation | not demonstrated | secret-bearing write | later P7 settings review |
| `api_settings_get` | P7 | GET | `/api/settings` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | response owner, persistence, redaction, authorization | not demonstrated | secret/config disclosure | later P7 settings review |
| `api_agent_model_recommendation_post` | P8 | POST | `/api/agents/model-recommendation` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | provider availability, cost, caller, network | not demonstrated | external provider/egress | later P8 provider review |
| `api_hardware_profile_get` | P8 | GET | `/api/system/hardware-profile` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | probe owner, disclosure policy, audience | not demonstrated | environment disclosure | later P8 hardware review |
| `api_model_compatibility_post` | P8 | POST | `/api/system/model-compatibility` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | provider/model policy, cost, caller, network | not demonstrated | provider/egress disclosure | later P8 compatibility review |
| `api_agents_list_get` | P6 | GET | `/api/agents/list` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | workforce owner, sensitive-field policy, scope | not demonstrated | workforce disclosure | later P6 list contract |
| `api_agent_update_put` | P6 | PUT | `/api/agents/{agent_id}` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | lifecycle owner, confirmation, rollback | not demonstrated | mutable workforce state | later P6 lifecycle review |
| `api_agent_delete_delete` | P6 | DELETE | `/api/agents/{agent_id}` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | deletion owner, confirmation, recovery | not demonstrated | destructive workforce state | later P6 recovery review |
| `api_agent_regenerate_paper_post` | P6 | POST | `/api/agents/{agent_id}/regenerate-paper` | CONTAIN | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | paper owner, provider policy, rollback | not demonstrated | provider/workforce mutation | later P6 paper contract |
| `root_get` | P9 | GET | `/` | BLOCK_UNTIL_EXTERNAL_EVIDENCE | DEFERRED | `REMAIN_DISABLED_OR_CONTAINED` | hosting edge, identity, ingress, tenant, traffic | not demonstrated | public root exposure | later P9 hosting review |

## Family totals

| Family | Routes | Methods | Reads | Mutations | P4 treatment |
| --- | ---: | --- | ---: | ---: | --- |
| P1 | 4 | 4 GET | 4 | 0 | remaining |
| P2 | 6 | 3 GET, 3 POST | 3 | 3 | remaining |
| P3 | 7 | 4 GET, 3 POST | 4 | 3 | remaining |
| P4 | 7 | 7 GET | 7 | 0 | internally complete |
| P5 | 1 | 1 POST | 0 | 1 | remaining |
| P6 | 5 | GET, POST, PUT, DELETE | 1 | 4 | remaining |
| P7 | 2 | GET, POST | 1 | 1 | remaining |
| P8 | 3 | 1 GET, 2 POST | 1 | 2 | remaining |
| P9 | 1 | 1 GET | 1 | 0 | remaining |
| **Total** | **36** |  | **22** | **14** | **7 treated / 29 remaining** |

`ROADMAP_4X_MACRO_03_LEGACY_ROUTE_MATRIX_RECONCILED_36_UNIQUE_7_P4_29_REMAINING`
