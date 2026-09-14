# Roadmap 4.x Macro-Mission 03 - Family Selection Matrix

## Method

P4 is excluded because it is the family closed by this mission. The remaining
families are scored on two five-point axes:

- **Urgency**: security/exposure reduction, side-effect containment, contract
  debt, architectural centrality and cost of delay.
- **Internal readiness**: evidence, known payload/consumers, deterministic
  testing, independence from external infrastructure/secrets/providers,
  reversibility and bounded scope.

The total is the sum, not an authority to expose a route. A high score still
requires the future family contract and all applicable gates.

## Complete comparison

| Family | Routes | Reads/mutations | Main dependencies and risks | Internal evidence/readiness | External gates | Urgency | Readiness | Total | Decision |
| --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| P1 `STATUS_OBSERVABILITY_MEMORY` | 4 | 4 / 0 | identity, tenant scope, redaction, retention; status is provider-adjacent and logs/memory can disclose sensitive data | observability contracts, memory tests, audit persistence contracts and deterministic negative-policy tests exist; route boundary is not yet closed | G01, G02, G03, G04, G06, G08, G10, G11, G18 | **5** | **4** | **9** | **SELECTED** |
| P2 `CHAT_ORCHESTRATION` | 6 | 3 / 3 | providers, credentials, activation, orchestration stores and retention; chat is an activation frontier | internal orchestration pieces exist, but caller/provider/activation ownership is incomplete | G01, G02, G03, G04, G10, G11, G13, G14, G16, G18, G19 | 4 | 2 | 6 | defer |
| P3 `LOTERIA_VALIDATION_EVOLUTION` | 7 | 4 / 3 | domain lifecycle, reveal/reset, recovery and compatibility; reset/reveal have state effects | existing domain tests and compatibility surfaces provide useful evidence, but lifecycle authority and tenant scope are unresolved | G01, G02, G03, G04, G16, G17, G18, G19 | 4 | 3 | 7 | defer |
| P5 `DOMAIN_MATERIALIZATION` | 1 | 0 / 1 | persistence, materializer ownership, backup/restore and rollback; write-capable | domain registry/materializer contracts exist, but product destination and recovery ownership are not proven | G01, G02, G03, G04, G10, G12, G17, G18, G19 | 4 | 2 | 6 | defer |
| P6 `WORKFORCE_AGENT_LIFECYCLE` | 5 | 1 / 4 | workforce activation, providers, lifecycle and recovery; large mutation blast radius | agent schemas and internal lifecycle contracts exist, but active workforce and provider boundaries are not authorized | G01, G02, G03, G04, G08, G10, G13, G15, G16, G17, G18, G19 | 4 | 2 | 6 | defer |
| P7 `SETTINGS` | 2 | 1 / 1 | secrets, rotation, persistence, retention and authorization; both read and write can disclose or change authority | settings-related policy exists, but owner, storage, redaction and rotation evidence are incomplete | G01, G02, G03, G04, G07, G08, G09, G10, G11, G19 | 5 | 2 | 7 | defer |
| P8 `PROVIDER_HARDWARE` | 3 | 1 / 2 | provider credentials, network egress, cost, hardware disclosure and payload compatibility | model recommendation contracts exist, but external provider/network facts are required | G01, G02, G03, G04, G13, G14, G18, G19 | 4 | 1 | 5 | defer |
| P9 `HOSTING_ROOT` | 1 | 1 / 0 | ingress, hosting, identity, CORS, tenant and actual traffic; public boundary | no internal evidence can replace deployment/ingress evidence | G01, G02, G03, G04, G05, G06, G18 | 4 | 1 | 5 | defer |

## Selection rationale

P1 wins on risk reduction and centrality without being selected merely because
it is easy. It is the only remaining family that combines a concentrated
security-sensitive read boundary with substantial internal contract evidence,
deterministic testability and a separable no-external-exposure treatment. Its
four routes remain risky precisely because they expose status, memory, logs or
metrics; that risk is a reason to govern the boundary, not permission to expose
it.

The authorized tie-break sequence was applied conceptually: P1 reduces the
most immediate disclosure risk, is central to observability and memory
governance, has stronger internal evidence than P3/P7, requires no real
provider or hosting proof for a bounded internal station, has a smaller blast
radius than mutation-heavy families, and is reversible by route-boundary
rollback. No material tie remains.

`P1_STATUS_OBSERVABILITY_MEMORY_SELECTED_NOT_STARTED`
