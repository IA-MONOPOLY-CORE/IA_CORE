# Roadmap 4.x Macro-Mission 06 - Repository Truth Matrix

## Scope and method

This matrix is a repository-grounded adjudication after the published
Macro 05.1 head `ccd982555ac76803ef8372fdd01f2dceb287afaf`. It distinguishes a
documented contract, a tested behavior, an implemented module, a runtime-active
path, an externally exposed path, and productive use. The first two are not
treated as proof of the latter four.

| Candidate/responsibility | Material evidence | State | Current owner | Real overlap | Real gap | Frontier | Decision | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Verified enterprise reality and outcomes | `docs/ROADMAP_4X_MACRO_05_1_*`, P1 status/memory/logs/metrics contracts, `core/platform_status_schema.py`, `core/protected_*`, test evidence | Partial composition: evidence, metrics and bounded reads exist; no VERO runtime | P1 read contracts plus Method Santi and GOKV/DOOL/OCI boundaries | VERO would duplicate status/metrics and closure evidence if made a new store | No canonical value/outcome/intervention contract family exists | No external or productive exposure | MERGE existing capabilities; preserve VERO as an adjudicated architectural vocabulary, not a new pillar | High |
| Failure intelligence and resilience evidence | invalidated Level B attempts, repair ledgers, rollback contracts, adversarial suites, `docs/ROADMAP_4X_MACRO_05_1_ROOT_CAUSE_AND_RECURRENCE_PREVENTION.md` | Partial evidence and derived reports; no FIRE component | Method Santi closure and existing tests; GOKV retains lifecycle candidates | FIRE as a service would duplicate closure diagnostics and GOKV provenance | No normalized derived failure vocabulary or coverage view | Must remain development-only and non-productive | MERGE as a future Method/GOKV derived evidence profile; do not create runtime | High |
| Developmental Symmetry | Method 3.2.1 through 3.2.5, historical impact gates, validation basis invalidation, closure gate | Implemented as a set of engineering controls, not a named component | Method Santi plus closure authority | A new module would duplicate existing gates and test discipline | A single explicit principle and anti-abuse checklist are missing | No productive activation | ADOPT as a Method Santi principle and readiness criterion | High |
| Platform status | `core/platform_status.py`, `core/platform_status_schema.py`, P1-A contract and tests | Implemented, internally exercised, default-denied | P1-A platform status contract | VERO observation vocabulary overlaps only at bounded read semantics | No enterprise outcome semantics | External status remains denied | Preserve; no VERO takeover | High |
| Protected memory | `core/protected_memory_access.py`, P1-B contract/tests | Implemented, internally exercised, default-denied | P1-B access contract | VERO evidence retention could overlap with protected memory | No outcome-specific evidence ownership | Tenant view future/inactive | Preserve; VERO cannot become a memory store | High |
| Protected logs/events | `core/protected_logs_access.py`, P1-C contract/tests | Implemented, internally exercised, default-denied | P1-C observability contract | FIRE may derive from sanitized events but cannot own raw logs | No normalized resilience derivation | External raw logs forbidden | Preserve; FIRE consumes bounded evidence only | High |
| Protected dynamic metrics | `core/protected_dynamic_metrics.py`, P1-D contract/tests | Implemented, internally exercised, default-denied | P1-D metrics contract | VERO semantic metrics would need to consume, not replace, bounded metrics | No value/outcome measurement contract | Tenant metrics future/inactive | Preserve; no new metrics endpoint | High |
| Closure authority | `scripts/validate_mission_closure.py`, V1 tests and Macro 05.1 evidence | Implemented, mission-specific | Method Santi 3.2.5 | V2 must not rewrite V1 history | Generic policy-driven successor was absent | Repo-local CI can be added; remote ruleset not proven | ADOPT V2 as additive method infrastructure | High |
| GOKV | `gokv/`, schema, promotion and inheritance tests | Implemented and tested; promotion remains governed | GOKV lifecycle | VERO/FIRE candidates could incorrectly claim promotion authority | No VERO/FIRE production capability | GOKV promotion and OCI activation unchanged | Preserve as lifecycle/provenance owner | High |
| DOOL | `docs/GOKV_DOOL_OCI_*`, capture/provenance tests | Implemented for development-origin lineage | DOOL | VERO/FIRE could duplicate provenance | No productive global learning authority | Development-only boundary | Preserve as provenance owner | High |
| OCI | inheritance/shadow/resource governance contracts and tests | Implemented as bounded inheritance controls | OCI | Candidate planes must not activate inheritance | No candidate-specific runtime | Activation remains off | Preserve; no OCI change | High |
| P3 validation/evolution | 36-route matrix, legacy validation routes, domain lifecycle modules and tests | Documented and partially implemented; not closed as a family | Existing validation/domain modules | VERO outcome assessment could be confused with domain validation state | Lifecycle authority, compatibility and tenant evidence remain incomplete | Product and mutation routes remain deferred | Select as next execution family; not started | Medium-high |

## Material status rules

```text
DOCUMENTED != TESTED != IMPLEMENTED != RUNTIME_ACTIVE
RUNTIME_ACTIVE != EXTERNALLY_EXPOSED
EXTERNALLY_EXPOSED != PRODUCTIVELY_USED
```

The repository contains many future contracts and internal tests. No evidence
was found that VERO or FIRE has a product endpoint, store, tenant capability,
provider, panel, runtime activation, or external exposure. The absence of a
named module is not treated as proof that every proposed responsibility is
absent: several responsibilities are already distributed across Method Santi,
P1 contracts, GOKV, DOOL, OCI and the closure gate.

## Contradictions resolved

1. VERO's fourth-pillar language is conceptual package language, not a current
   repository fact. The material evidence supports a composition, not a new
   constitutional pillar.
2. FIRE's proposed derived intelligence is compatible with existing failure
   evidence, but a new runtime would duplicate assurance and create a new
   authority surface.
3. Developmental Symmetry is visible in current practice. It is a useful
   explicit principle, not evidence for a new subsystem.
4. V1 is mission-specific by design. This is a portability gap, not a reason
   to alter Macro 05.1 evidence or tests.

## Repository result

The material result is `MERGE`: the candidates become explicit architectural
decisions and method vocabulary while existing contracts keep their owners.
The only new executable capability required by this mission is generic closure
authority V2, which is method infrastructure and not product behavior.
