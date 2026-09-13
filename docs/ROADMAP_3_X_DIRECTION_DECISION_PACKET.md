# Roadmap 3.x Direction Decision Packet

## Status and use

- Mission origin: `ROADMAP_3X_MACRO_MISSION_04_TRUE_COMPLETION_RECALIBRATION_EVIDENCE_COVERAGE_AND_CLOSURE_PATH`
- Packet state: `DIRECTION_ACCEPTED_AND_ADOPTED_BY_MACRO_05`
- Evidence baseline: `43530e656066a3c40d9afb8a5a4a381b38f29f38`
- Historical route destination for all rows: `UNKNOWN`
- Active route decision layer: `docs/ROADMAP_3_X_LEGACY_ROUTE_DECISION_ADJUDICATION.json`
- The packet is now an adopted policy record. It is not an adapter
  specification, implementation proof or production decision.

## Decision 1: recalibrated 3.x evidence

**Object:** the true completion contract, original-scope crosswalk, gap
register, this packet, the 4.x execution plan and the forecast.

**Recommendation:** accept the technical evidence package as complete for the
repository/documentary boundary, with all external, trust, persistence,
provider, route-authority and workforce limits preserved.

**Required acceptance text:**

> Accept or reject the recalibrated Roadmap 3.x technical evidence package
> with every named F-001 through F-011 boundary preserved. This acceptance
> does not authorize a route adapter, product remediation, runtime, provider,
> external action, payload change, production claim or Roadmap 4.x execution.

This is the decision that Macro 03 had prepared but could not simulate. Macro
05 records Direction's explicit acceptance in
`docs/ROADMAP_3_X_DIRECTION_ACCEPTANCE_RECORD.md`.

## Decision 2: future F-004 family selection

Direction has accepted one future family candidate for a later authorized
review. The decision object includes:

- one family ID and complete route membership;
- one destination policy;
- one service owner and one authority owner;
- identity, tenant, permission and confirmation assumptions;
- compatibility and external-consumer evidence;
- payload, lifecycle, persistence and rollback requirements;
- negative bypass tests and a stop condition.

The selected family is `P4_CATALOG_DOMAIN_READS`. It is `DECIDED_FOR_3X` as a
future policy selection, while every implementation destination is
`DEFERRED_TO_4X_BY_EXPLICIT_DIRECTION`.

## Family-level recommendations

| Family | Routes | Recommendation | Why this is not an authorization |
| --- | ---: | --- | --- |
| `P1_STATUS_OBSERVABILITY_MEMORY` | 4 | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Status, logs and memory disclosure require audience, identity, tenant, retention and deployment evidence. |
| `P2_CHAT_ORCHESTRATION` | 6 | `CONTAIN` | Keep the legacy surface bounded until caller, provider chain, memory and activation ownership are evidenced. |
| `P3_LOTERIA_VALIDATION_EVOLUTION` | 7 | `KEEP_AS_COMPATIBILITY_SURFACE` | Preserve domain-specific behavior while refusing a generic rewrite or lifecycle authority inference. |
| `P4_CATALOG_DOMAIN_READS` | 7 | `KEEP_AS_COMPATIBILITY_SURFACE` | Read catalogs can remain a compatibility concern, but visibility and ownership still need a route decision. |
| `P5_DOMAIN_MATERIALIZATION` | 1 | `CONTAIN` | Materialization is a write-capable boundary and must stay behind ownership, sandbox and rollback gates. |
| `P6_WORKFORCE_AGENT_LIFECYCLE` | 5 | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Agent and paper lifecycle touches workforce, provider, persistence and activation authority. |
| `P7_SETTINGS` | 2 | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Secret-bearing input and config persistence require storage, redaction, rotation and authorization evidence. |
| `P8_PROVIDER_HARDWARE` | 3 | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Provider reachability, credentials, cost and hardware disclosure cannot be inferred from source. |
| `P9_HOSTING_ROOT` | 1 | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | Root exposure, ingress, identity and actual traffic require deployment evidence. |

Recommendations describe the adopted policy for the active layer. They do not
change the inherited historical destination field in any route row.

## Route-by-route decision register

Every legacy route is listed exactly once. `Current destination` is the
historical published fact; `Recommendation` is the adopted Direction
disposition; `Missing evidence` is the reason implementation remains
deferred. The authoritative post-decision fields are in the linked JSON
adjudication register.

| # | Route ID | Method | Path | Family | Current destination | Recommendation | Missing evidence |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `api_status_get` | GET | `/api/status` | P1 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | identity, audience, deployment |
| 2 | `api_memory_get` | GET | `/api/memory` | P1 | `UNKNOWN` | `CONTAIN` | memory owner, tenant scope, sanitized response |
| 3 | `api_logs_get` | GET | `/api/logs` | P1 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | admin identity, sink, retention |
| 4 | `api_metrics_dynamic_get` | GET | `/api/metrics/dynamic` | P1 | `UNKNOWN` | `CONTAIN` | metric owner and audience |
| 5 | `api_debate_start_post` | POST | `/api/debate/start` | P2 | `UNKNOWN` | `CONTAIN` | orchestration authority and activation bridge |
| 6 | `api_validation_start_post` | POST | `/api/validation/start` | P3 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | domain lifecycle owner and confirmation |
| 7 | `api_validation_next_get` | GET | `/api/validation/next` | P3 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | validation resource scope |
| 8 | `api_validation_by_id_get` | GET | `/api/validation/{validation_id}` | P3 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | identifier owner and tenant scope |
| 9 | `api_validation_reveal_post` | POST | `/api/validation/{validation_id}/reveal` | P3 | `UNKNOWN` | `CONTAIN` | reveal authority, confirmation and recovery |
| 10 | `api_ranking_get` | GET | `/api/ranking` | P3 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | ranking owner and audience |
| 11 | `api_evolution_stats_get` | GET | `/api/evolucion/stats` | P3 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | evolution owner and response policy |
| 12 | `api_evolution_reset_post` | POST | `/api/evolucion/reset` | P3 | `UNKNOWN` | `CONTAIN` | destructive owner, confirmation and rollback |
| 13 | `api_debate_by_id_get` | GET | `/api/debate/{debate_id}` | P2 | `UNKNOWN` | `CONTAIN` | debate store owner and scope |
| 14 | `api_debates_get` | GET | `/api/debates` | P2 | `UNKNOWN` | `CONTAIN` | list visibility and tenant scope |
| 15 | `api_chat_post` | POST | `/api/chat` | P2 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | provider chain, credentials, caller |
| 16 | `api_learn_post` | POST | `/api/learn` | P2 | `UNKNOWN` | `CONTAIN` | memory retention, content owner, caller |
| 17 | `api_conversation_get` | GET | `/api/conversation/{conversation_id}` | P2 | `UNKNOWN` | `CONTAIN` | conversation owner and response policy |
| 18 | `api_catalog_domain_creation_get` | GET | `/api/catalogs/domain-creation` | P4 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| 19 | `api_catalog_roles_get` | GET | `/api/catalogs/roles` | P4 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| 20 | `api_catalog_specializations_get` | GET | `/api/catalogs/specializations` | P4 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | catalog audience and authorization |
| 21 | `api_domains_list_get` | GET | `/api/domains/list` | P4 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | domain visibility and deployment scope |
| 22 | `api_domain_profile_catalog_get` | GET | `/api/domains/{domain_id}/profile-catalog` | P4 | `UNKNOWN` | `KEEP_AS_COMPATIBILITY_SURFACE` | domain ownership and visibility |
| 23 | `api_domain_agent_presets_get` | GET | `/api/domains/{domain_id}/agent-presets` | P4 | `UNKNOWN` | `CONTAIN` | workforce owner and provider metadata scope |
| 24 | `api_domain_agent_preset_match_get` | GET | `/api/domains/{domain_id}/agent-presets/match` | P4 | `UNKNOWN` | `CONTAIN` | matching authority and scope |
| 25 | `api_domains_create_post` | POST | `/api/domains/create` | P5 | `UNKNOWN` | `CONTAIN` | materializer authority, caller and rollback |
| 26 | `api_agents_create_post` | POST | `/api/agents/create` | P6 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | workforce owner and sandbox/product boundary |
| 27 | `api_settings_post` | POST | `/api/settings` | P7 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | settings owner, storage and secret policy |
| 28 | `api_settings_get` | GET | `/api/settings` | P7 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | response owner, persisted shape and authorization |
| 29 | `api_agent_model_recommendation_post` | POST | `/api/agents/model-recommendation` | P8 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | provider availability, cost and caller |
| 30 | `api_hardware_profile_get` | GET | `/api/system/hardware-profile` | P8 | `UNKNOWN` | `CONTAIN` | probe owner and disclosure policy |
| 31 | `api_model_compatibility_post` | POST | `/api/system/model-compatibility` | P8 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | provider/model policy and caller |
| 32 | `api_agents_list_get` | GET | `/api/agents/list` | P6 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | workforce owner, sensitive fields and scope |
| 33 | `api_agent_update_put` | PUT | `/api/agents/{agent_id}` | P6 | `UNKNOWN` | `CONTAIN` | lifecycle owner, confirmation and rollback |
| 34 | `api_agent_delete_delete` | DELETE | `/api/agents/{agent_id}` | P6 | `UNKNOWN` | `CONTAIN` | deletion owner, confirmation and recovery |
| 35 | `api_agent_regenerate_paper_post` | POST | `/api/agents/{agent_id}/regenerate-paper` | P6 | `UNKNOWN` | `CONTAIN` | paper owner, provider policy and rollback |
| 36 | `root_get` | GET | `/` | P9 | `UNKNOWN` | `BLOCK_UNTIL_EXTERNAL_EVIDENCE` | hosting edge, identity and actual traffic |

### Route register integrity

- `36/36` routes accounted for exactly once.
- Method counts: `22 GET`, `12 POST`, `1 PUT`, `1 DELETE`.
- Family counts: P1 `4`, P2 `6`, P3 `7`, P4 `7`, P5 `1`, P6 `5`, P7 `2`,
  P8 `3`, P9 `1`.
- Historical current destination counts: `UNKNOWN 36`; all other historical
  destination values are `0`.
- No route was migrated, bridged, made internal-only, retired, removed or
  connected to a canonical adapter. All implementation destinations are
  deferred by explicit Direction.

## External and human decision checklist

| Decision surface | Required input | Owner | Stop condition |
| --- | --- | --- | --- |
| 3.x evidence acceptance | Accept/reject text with explicit limits | Direction/Architect | Do not call B7 accepted without the recorded decision. |
| Trust and CORS | approved origins, identity, tenant and edge enforcement | Direction, security, hosting | Stop before changing trust authority. |
| Secret/settings | secret owner, redaction, rotation, retention and authorization | Direction, storage, deployment | Stop before reading values or opening live stores. |
| Route family | one family, destination, compatibility and owner | Direction plus route owner | Stop before adapter, migration, retirement or removal. |
| Provider/network | credential, egress, availability, cost and traffic evidence | provider/deployment owner | Stop before DNS, socket, HTTP or provider calls. |
| Workforce | activation, permission, provider and deployment gates | workforce/activation owner | Stop before agent execution or active team state. |

## Packet conclusion

This packet records the accepted evidence boundary and preserves every open
technical frontier. Its active policy layer resolves the decision ambiguity
without falsifying any technical destination. Its strongest operational
restriction is to keep every implementation deferred until the required gates
and P4 contract are satisfied.

`ROADMAP_3_X_DIRECTION_DECISION_PACKET_ACCEPTED_POLICY_ADOPTED`
