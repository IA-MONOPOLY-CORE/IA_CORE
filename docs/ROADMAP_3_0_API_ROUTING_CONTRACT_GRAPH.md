# Roadmap 3.0 N1 - API, Routing and Contract Graph

## Gate

`ROADMAP_3_0_N1_API_ROUTING_CONTRACT_GRAPH_PASSED`

## Method

The graph is a static read of `api.py` and directly named collaborators. It
does not import the application, start FastAPI, call an endpoint, submit a
provider request, or write a store. `input` and `output` below describe the
declared handler contract, not an observed HTTP response.

## Route inventory

| Method | Path | Handler | Input | Output | Auth evidence | Write | Network/execution | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GET | `/api/status` | `get_status` | `full: bool` | dict | none found | read | supervisor/provider listing | legacy |
| GET | `/api/memory` | `get_memory_snapshot` | key, history limit | dict | none found | read | memory read | legacy |
| GET | `/api/logs` | `get_logs` | lines | dict | none found | read | filesystem read | legacy |
| GET | `/api/metrics/dynamic` | `get_dynamic_metrics` | none | dict | none found | read | evolution read | legacy |
| POST | `/api/debate/start` | `start_debate` | `DebateRequest` | dict | none found | event/background | orchestration | legacy |
| POST | `/api/validation/start` | `start_validation` | `DebateRequest` | dict | none found | event/background | orchestration | legacy |
| GET | `/api/validation/next` | `get_next_validation_info` | none | dict | none found | read | domain/evolution | legacy |
| GET | `/api/validation/{validation_id}` | `get_validation` | path id | dict | none found | read | validation read | legacy |
| POST | `/api/validation/{validation_id}/reveal` | `reveal_validation` | id + result | dict | none found | validation state | validation flow | legacy |
| GET | `/api/ranking` | `get_ranking` | none | dict | none found | read | domain read | legacy |
| GET | `/api/evolucion/stats` | `get_evolucion_stats` | none | dict | none found | read | evolution read | legacy |
| POST | `/api/evolucion/reset` | `reset_ciclo` | `nuevo_inicio` | dict | none found | state | domain lifecycle | legacy |
| GET | `/api/debate/{debate_id}` | `get_debate` | path id | dict | none found | read | orchestration read | legacy |
| GET | `/api/debates` | `list_debates` | none | list/dict | none found | read | orchestration read | legacy |
| POST | `/api/chat` | `chat_endpoint` | `ChatRequest` | dict | none found | event/memory | supervisor/providers | legacy |
| POST | `/api/learn` | `learn_endpoint` | `LearnRequest` | dict | none found | memory/vector | learning flow | legacy |
| GET | `/api/conversation/{conversation_id}` | `get_conversation` | path id | dict | none found | read | memory read | legacy |
| GET | `/api/catalogs/domain-creation` | catalog endpoint | none | dict | none found | read | none | legacy |
| GET | `/api/catalogs/roles` | catalog endpoint | none | dict | none found | read | none | legacy |
| GET | `/api/catalogs/specializations` | catalog endpoint | role id | dict | none found | read | none | legacy |
| GET | `/api/domains/list` | `get_domains` | none | list/dict | none found | read | filesystem read | legacy |
| GET | `/api/domains/{domain_id}/profile-catalog` | catalog endpoint | domain id | dict | none found | read | filesystem read | legacy |
| GET | `/api/domains/{domain_id}/agent-presets` | preset endpoint | domain id | dict | none found | read | filesystem read | legacy |
| GET | `/api/domains/{domain_id}/agent-presets/match` | match endpoint | domain, role, specialization | dict | none found | read | filesystem read | legacy |
| POST | `/api/domains/create` | `create_domain_endpoint` | `DomainCreateRequest` | dict | none found | domain JSON | materialization | legacy |
| POST | `/api/agents/create` | `create_agent_endpoint` | form agent fields | dict | none found | agent JSON | materialization | legacy |
| POST | `/api/settings` | `save_settings` | provider, api key, model, agents | dict | none found | config/secrets | provider config | legacy |
| GET | `/api/settings` | `get_settings` | none | dict | none found | read | config read | legacy |
| POST | `/api/agents/model-recommendation` | recommendation endpoint | form IDs/provider/model | dict | none found | none | local hardware probe | legacy |
| GET | `/api/system/hardware-profile` | hardware endpoint | none | dict | none found | read | local hardware probe | legacy |
| POST | `/api/system/model-compatibility` | compatibility endpoint | provider/model | dict | none found | none | provider metadata path | legacy |
| GET | `/api/agents/list` | `list_agents` | none | list/dict | none found | read | agent/provider listing | legacy |
| PUT | `/api/agents/{agent_id}` | `update_agent` | id + request + domain | dict | none found | agent JSON | materialization | legacy |
| DELETE | `/api/agents/{agent_id}` | `delete_agent` | id + domain | dict | none found | delete/rmtree | materialization | legacy |
| POST | `/api/agents/{agent_id}/regenerate-paper` | `regenerate_agent_paper` | id + request | dict | none found | paper JSON | regeneration path | legacy |
| GET | `/` | root | none | HTML/response | none found | read | none | legacy |

Total: 36 routes, including 22 GET/read-oriented routes and 14 POST/PUT/DELETE
mutation-capable routes. The read-oriented count does not imply authentication.

## Contract and boundary findings

- No FastAPI `Depends`, `Security`, OAuth/JWT, API-key dependency, or equivalent
  route-level auth evidence was found in the static search.
- CORS is configured with wildcard origins, methods, and headers.
- Pydantic/request validation and path/domain ID validation exist in parts of
  the API, but validation is not authorization.
- The legacy route graph reaches `Supervisor` and can reach providers after
  application startup. This is callable source reachability, not a call made by
  Roadmap 3.0.
- The graph contains settings and agent/domain mutation routes that are outside
  the contract-only backend frontier and require a security/activation audit.
- The graph contains a secret-bearing input (`api_key`) and a config write path.

## N1 conclusion

The API surface is a live-looking legacy boundary with no demonstrated
authentication or authorization barrier. The next work must audit activation,
permission and trust boundaries around these routes before any operational
backend phase is considered.
