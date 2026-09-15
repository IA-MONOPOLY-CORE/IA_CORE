# Roadmap 4.x Macro-Mission 04.3

## P1-A truth matrix

`OBSERVED` is directly supported by the current repository or a passing test.
`INFERRED` is a bounded conclusion from observed code. `UNKNOWN` is not
claimed. `EXTERNAL_EVIDENCE_REQUIRED` is intentionally outside the local
repository boundary.

| Claim / field | Status | Source | Consumer | Sensitivity | Cost / side effect | Decision |
|---|---|---|---|---|---|---|
| `GET /api/status` exists | OBSERVED | `api.py` route | connection poller, Overview | low | one local read | preserve |
| legacy route probed Lotería | OBSERVED | pre-remediation handler | historical tests/docs | high | domain work | remove from canonical view |
| legacy route enumerated providers/models | OBSERVED | pre-remediation handler | provider panel | high | provider calls | remove from status; panel no longer uses it |
| legacy route read memory/runtime metrics | OBSERVED | pre-remediation handler | Overview | high | store/metric reads | remove from status |
| minimal `platform_status.v1` shape | OBSERVED | schema + handler tests | poller, Overview | low | bounded local flag | preserve |
| minimal has no collections | OBSERVED | strict schema + adversarial tests | poller | low | no enumeration | preserve |
| minimal status | OBSERVED | local lifecycle projection | poller | low | no health probe | preserve |
| minimal liveness/readiness distinction | OBSERVED | absent/initializing/broken tests | Overview | low | no external work | preserve |
| detailed `platform_status.v1` shape | OBSERVED | schema + authorized handler test | Hybrid | internal | fixed four components | preserve |
| `full=true` is only an alias | OBSERVED | route + denial tests | Hybrid | low | no authority | preserve |
| detailed access is server-side | OBSERVED | access module + forged-header tests | detailed caller | high | fail closed | preserve |
| default principal source | OBSERVED | resolver | detailed caller | high | no identity configured | deny by default |
| recursive redaction | OBSERVED | sanitizer tests | detail projection | high | bounded recursion | preserve |
| component failure isolation | OBSERVED | broken lifecycle test | detailed caller | internal | safe fallback | preserve |
| generic domain position | OBSERVED | fixed component contract | future domains | internal | no domain scan | preserve |
| Lotería privilege in new payload | OBSERVED | payload allowlist | all consumers | high | none | absent |
| external status exposure | EXTERNAL_EVIDENCE_REQUIRED | hosting/ingress not configured | external callers | high | deployment dependent | `DEFAULT_DENIED` |
| trusted identity deployment | EXTERNAL_EVIDENCE_REQUIRED | no provider configured | detailed caller | high | Owner/deployment boundary | remain inactive |
| active provider health | UNKNOWN | excluded by contract | none | high | intentionally unmeasured | future separate capability |

### Field disposition from the legacy payload

| Legacy field | Disposition | Reason |
|---|---|---|
| `running` | transformed | retained as bounded lifecycle boolean |
| `providers`, `providers_ready` | eliminated from status | enumeration and provider probing |
| `agents` | eliminated from status | inventory disclosure |
| `overview` counters/tools/memory | eliminated from status | runtime, activity and memory disclosure |
| `hybrid` router snapshot | transformed | fixed generic component and default-denied exposure |
| `fase_actual`, `sorteo_actual`, `limites_sistema` | eliminated from status | Lotería privilege/domain computation |
| `schema/view/scope/status/liveness/readiness` | introduced | versioned honest contract |
