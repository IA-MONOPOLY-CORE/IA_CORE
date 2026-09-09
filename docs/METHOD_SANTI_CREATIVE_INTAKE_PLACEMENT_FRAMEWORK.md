# METHOD SANTI CREATIVE INTAKE & PLACEMENT FRAMEWORK

## Status

`BASE_DOCUMENT_RECOMMENDED_FOR_NEW_AND_EXISTING_PROJECTS`

This is a documentary placement framework. It does not implement a product
feature, database, intake UI, automation, reminder, runtime, agent or GOKV
promotion. It keeps ideas visible without allowing them to contaminate the
current mission.

Central rule:

```text
NO HAY QUE IMPLEMENTARLA.
NO HAY QUE OLVIDARLA.
SE UBICA.
Y SE SIGUE TRABAJANDO.
```

## Primary classification

Every idea receives exactly one primary classification:

1. `PRODUCT_NOW`
2. `PRODUCT_FUTURE`
3. `ARCHITECTURAL_RESERVATION`
4. `METHOD_EVOLUTION`
5. `OPERATIONAL_LEARNING`
6. `BUSINESS_STRATEGY`
7. `EXTERNAL_BENCHMARK`
8. `NOT_RELEVANT_DISCARD`

Secondary tags may describe domain, urgency, risk or source, but they never
replace the primary classification.

## IDEA_RECORD contract

Every retained idea must have:

| Field | Meaning |
| --- | --- |
| `IDEA_ID` | Stable human-readable identifier |
| `DATE` | Capture date, not reconstructed if unknown |
| `RAW_IDEA` | Original wording or faithful short capture |
| `PRIMARY_CLASSIFICATION` | Exactly one of the eight categories |
| `SECONDARY_TAGS` | Optional supporting tags |
| `WHY_IT_MATTERS` | Value, risk or learning rationale |
| `WHY_NOW` | Evidence for current timing, or `NOT_NOW` |
| `WHY_NOT_NOW` | Boundary, dependency or missing evidence |
| `ARCHITECTURAL_HOME` | Where the idea belongs if retained |
| `DEPENDENCIES` | Contracts, decisions, surfaces or evidence required |
| `TRIGGER_TO_REVISIT` | Observable condition for review |
| `RISK_IF_FORGOTTEN` | Consequence of losing the idea |
| `STATUS` | Captured, triaged, parked, promoted to scope or discarded |
| `SOURCE_PROVENANCE` | Prompt, decision, artifact, observation or external source |

## Placement decisions

### PRODUCT_NOW

Only `PRODUCT_NOW` with demonstrated `WHY_NOW`, current authority, explicit
scope and an approved route may modify the active product mission. A label of
urgency is not evidence. The idea still needs a contract, tests, owner,
rollback and a mission checkpoint.

### PRODUCT_FUTURE

The idea belongs to a future product phase. It receives an architectural home,
dependencies and a trigger, but does not alter the current route.

### ARCHITECTURAL_RESERVATION

The idea describes a capability or constraint that must have a safe future home
before implementation is needed. Enterprise reservations are the canonical
example. It is not a readiness or implementation claim.

### METHOD_EVOLUTION

The idea changes how projects are directed, tested, paused, recalculated or
closed. It must remain separate from GOKV learning promotion and preserve
earlier method versions.

### OPERATIONAL_LEARNING

The idea is a development-origin observation from execution and validation.
It requires provenance, assessment, lifecycle and promotion governance. It does
not imply field-operation learning, runtime autonomy or automatic promotion.

### BUSINESS_STRATEGY

The idea concerns positioning, customers, sectors, pricing, procurement or
organizational direction. It is not silently converted into product scope.

### EXTERNAL_BENCHMARK

The idea comes from an external standard, competitor, customer or research
source. It remains an external reference until authority, provenance and scope
are accepted.

### NOT_RELEVANT_DISCARD

The idea is explicitly recorded as discarded when useful for auditability, with
a reason. Discard does not mean it was implemented or that its source was
forgotten.

## Intake flow

```text
CAPTURE
  -> PRESERVE_RAW_IDEA
  -> CLASSIFY_PRIMARY
  -> CHECK_WHY_NOW
  -> PLACE_ARCHITECTURALLY
  -> RECORD_DEPENDENCIES_AND_TRIGGER
  -> DECIDE_SCOPE_OR_PARK
  -> REVISIT_ON_TRIGGER
```

Ideas are not promoted into the active mission by repetition, emotional force,
or convenience. `PRODUCT_NOW` is the only class that can change current flow,
and only after its why-now evidence and authority are explicit.

## Integration with Method Santi 3.0

The framework supports destination/route separation, phase graphs, frontier
engineering, safe pause and route recalculation. When new evidence appears
during a mission, the idea is first captured and placed. The agent may continue
only when the placement is already within authorized scope. Otherwise it becomes
a safe-pause input for Direction.

## Governance boundary

This framework does not create a new GOKV item by itself. A development-origin
learning event still requires the existing DOOL lifecycle, assessment and
promotion rules. No idea creates authority, permission, endpoint, provider,
runtime, execution or store access merely by being recorded.

`METHOD_SANTI_CREATIVE_INTAKE_PLACEMENT_FRAMEWORK_DOCUMENTED`
