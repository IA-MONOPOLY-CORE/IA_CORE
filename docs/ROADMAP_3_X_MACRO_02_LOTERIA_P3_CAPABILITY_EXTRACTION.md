# Roadmap 3.x Macro-Mission 02: Loteria P3 Capability Extraction

`ROADMAP_3X_MACRO_02_LOTERIA_P3_CAPABILITY_EXTRACTION_MATERIALIZED`

This is a read-only extraction of capability families from `domains/loteria`.
It does not move code, rename artifacts, change payloads, or make a domain
function global.

| Capability family | Evidence | Classification | Reuse boundary |
| --- | --- | --- | --- |
| validation | `domains/loteria/validation_loteria.py` coordinates draw-specific validation, debate state, and reveal preconditions | `LOTTERY_SPECIFIC` | Keep draw semantics in the domain; future global validation may consume an adapter contract |
| ranking | `domains/loteria/scoring.py`, `domains/loteria/uscore_calculator.py` calculate lottery-specific scores and historical comparisons | `LOTTERY_SPECIFIC` | No generic ranking authority is inferred from numeric helpers |
| evolution | `domains/loteria/evolution_loteria.py` implements phases, draw visibility, parameters, and cycle state | `LOTTERY_SPECIFIC` | `core.evolution_base` is a possible contract ancestor; domain ownership remains local |
| learning | `domains/loteria/memoria_loteria.py`, `evolution_loteria.py`, and validation flow record domain observations | `GLOBAL_CONTRACT_WITH_DOMAIN_ADAPTER` | GOKV/DOOL can capture development evidence only through an explicit Loteria adapter; runtime learning is not enabled |
| evidence | Loteria database/history and GOKV evidence schemas are separate surfaces | `GLOBAL_CONTRACT_WITH_DOMAIN_ADAPTER` | GOKV evidence is reusable; Loteria evidence mapping, sensitivity, and owner require an adapter contract |
| reveal | `validation_loteria.py` reveals a draw result and updates domain-specific measures | `LOTTERY_SPECIFIC` | Reveal remains domain-owned and must not be generalized into a global action |
| lifecycle | `domains/loteria/database_loteria.py`, API validation/evolution routes, and memory/evolution writes form a legacy-connected surface | `BLOCKED_BY_OWNER_OR_BOUNDARY` | Owner, authorization, retention, rollback, and route coverage are not contractually demonstrated |

## Negative findings

- No capability is classified as `CANONICAL_DUPLICATE`; no movement is justified.
- No capability is promoted to global runtime behavior.
- No `LOTTERY_SPECIFIC` function is treated as a generic platform authority.
- The lifecycle family is not made safe by the existence of domain schemas or
  a callable database helper.
- No UI, endpoint, backend, payload, provider, execution, or integration change
  is included in this extraction.

## Next evidence

The reusable learning/evidence candidates need a domain adapter contract that
defines owner, source, sensitivity, retention, tenant/deployment scope, and
rollback. The lifecycle family needs route-specific authorization and
persistence evidence. Both are future governed surfaces, not implicit follow-up
work in this station.
