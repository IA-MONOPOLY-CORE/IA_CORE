# Roadmap 3.x True Completion Contract

## Identity and authority

- Mission: `ROADMAP_3X_MACRO_MISSION_04_TRUE_COMPLETION_RECALIBRATION_EVIDENCE_COVERAGE_AND_CLOSURE_PATH`
- Entry parent: `43530e656066a3c40d9afb8a5a4a381b38f29f38`
- Repository: `C:/IA_CORE`
- Branch at entry: `main`
- Mode: `READ_ONLY_DOCUMENTARY_ARCHITECTURE_AND_PLANNING`
- Current source, contracts, tests and published checkpoints are authoritative.
- Prior checkpoints remain historical evidence and are not rewritten by this
  mission.

This contract recalibrates what it means for Roadmap 3.x to be technically
complete. It does not activate a runtime, select a route destination, approve
an external policy or authorize Roadmap 4.x remediation.

## Recalibrated equation

```text
3.x = COMPLETE_BACKEND_TRUTH
      + COMPLETE_AUDIT_COVERAGE
      + DECISION_READY_FINDINGS
      + EXECUTABLE_REMEDIATION_PLAN_FOR_4X

4.x = AUTHORIZED_EXECUTION_OF_REMEDIATIONS_ALREADY_DEFINED_BY_3X
```

The first line is a documentary and planning exit contract. The second line
is an execution contract owned by a later, explicitly authorized phase. A
green 3.x evidence package never implies that 4.x has started.

## State taxonomy

Every original 3.x scope item is assigned one primary maturity state. States
are monotonic evidence labels, not capability flags:

| State | Meaning | Does not mean |
| --- | --- | --- |
| `AUDITED` | Current source, contract, test and known boundary evidence is mapped to the scope. | Runtime, deployment or production readiness |
| `DECIDED` | A named authority has selected a disposition and its limits are recorded. | That the disposition was implemented |
| `REMEDIATION_READY` | A later execution block has owner, scope, dependencies, tests, rollback and stop conditions. | That remediation happened |
| `REMEDIATED` | An authorized bounded change was implemented and verified. | Activation or production use |
| `ACTIVATED` | A separately authorized runtime or operational capability is enabled and evidenced. | Production readiness |
| `PRODUCTION_READY` | A separately accepted deployment and operational gate is green. | Automatic deployment or release |

The following labels describe evidence coverage and may accompany a state:

- `VERIFIED_COMPLETE`: the assigned original documentary scope is fully
  evidenced, including explicit exclusions.
- `PARTIAL`: some assigned evidence or disposition is bounded but incomplete.
- `MISSING`: required evidence is absent and has not been safely classified.
- `NOT_APPLICABLE_WITH_ENFORCEABLE_GATE`: the scope is not applicable to the
  current surface and the gate preventing accidental use is evidenced.
- `EXTERNAL_EVIDENCE_REQUIRED`: repository evidence cannot prove the claim.
- `DIRECTION_DECISION_REQUIRED`: the claim changes authority, trust, policy or
  phase acceptance and cannot be inferred by the executor.
- `TRUE_HARD_FRONTIER`: progress would change an authority or compatibility
  boundary and must stop until the named owner acts.

`CLOSED_WITH_EXPLICIT_LIMITS` and `CONTRACT_READY` remain valid historical
checkpoint labels. They are not substitutes for the state taxonomy and do not
mean that the original 3.x scope is `REMEDIATED`, `ACTIVATED` or
`PRODUCTION_READY`.

## True 3.x completion predicates

The technical evidence package may report
`ROADMAP_3X_TRUE_COMPLETION_TECHNICAL_EVIDENCE_COMPLETE_DIRECTION_DECISIONS_READY`
only when all predicates below are true:

1. The original scopes `3.0` through `3.9` each have exactly one primary
   coverage record.
2. Scopes `3.0` through `3.8` are at least `AUDITED`, with source paths,
   checkpoint provenance, tests, positive evidence, negative evidence and
   explicit unknowns.
3. The master findings scope `3.8` has decision-ready findings. An unresolved
   human decision is recorded as pending; it is never silently converted into
   a technical decision.
4. Scope `3.9` is at least `REMEDIATION_READY`: its plan is executable by a
   future authorized mission and contains owners, ordering, protected scope,
   evidence gates, negative tests, rollback and stop conditions.
5. Every unresolved gap is classified as a named frontier, external evidence
   requirement, Direction decision or legitimate later-phase task. No
   unclassified `MISSING` item remains hidden in the coverage table.
6. The 36 legacy routes are accounted for exactly once. `UNKNOWN` remains a
   valid route destination until ownership, authority, compatibility and
   evidence are demonstrated.
7. The test and historical-test contracts are preserved. A test may use its
   own historical checkpoint, but no assertion, protected path or negative
   guard is removed.
8. No protected product surface changes as a consequence of producing this
   evidence package.

This outcome is deliberately weaker than phase acceptance. `B7_ACCEPTED` and
`ROADMAP_3_X_CLOSED` require the separate Direction decision described below.

## Non-closure predicates

The package must not report technical closure if any of these occurs:

- an original scope is absent, duplicated or supported only by future prose;
- a contract is treated as positive route coverage without a demonstrated
  route-to-canonical call path;
- `UNKNOWN` route destinations are replaced by inferred policy;
- deployment, identity, tenant, provider, credential, traffic or external
  facts are claimed from static source presence;
- an executable remediation plan lacks a named owner, rollback or stop gate;
- a historical guard is made globally permissive to accommodate new files;
- product code, endpoints, payloads, runtime, providers, stores or
  integrations are changed to make the evidence appear complete.

## Authority boundaries

### Executor may do

- read current source and published historical evidence;
- map original scope to exact documents, tests, routes, functions and commits;
- create documentary contracts, coverage records, gap registers, decision
  packets, plans, forecasts, checkpoint evidence and focused tests;
- propose bounded route-family recommendations without changing the current
  `UNKNOWN` destination;
- preserve development-origin GOKV/DOOL/OCI evidence without automatic
  promotion.

### Executor may not do

- change HTML, CSS, JavaScript, i18n, backend behavior or payloads;
- add payload v2, endpoints, adapters, bridges, migrations or integrations;
- activate runtime, execution, queues, workers, agents, providers or external
  network access;
- read or expose secret values, use live stores or claim deployment evidence;
- modify P0, P1, the P3 matrix, contract-aware widgets or Request Draft Panel;
- declare `B7_ACCEPTED`, `ROADMAP_3_X_CLOSED`, `PRODUCTION_READY` or start 4.x.

## Decision-ready versus decided

`DECISION_READY` is an evidence property, not a maturity state. It means that
the decision packet contains the object, options, consequences, evidence
requirements, owner and stop condition needed for an authorized human or
owner to decide. It does not mean that the executor selected the result.

For F-004, the allowed recommendation vocabulary is:

`KEEP_AS_CANONICAL`, `KEEP_AS_COMPATIBILITY_SURFACE`, `ADAPTER_REQUIRED`,
`MIGRATE`, `CONTAIN`, `DEPRECATE`, `RETIRE`, `BLOCK_UNTIL_EXTERNAL_EVIDENCE`.

These are recommendations only. The inherited route destination remains
`UNKNOWN` until the relevant authority records a decision and the required
route evidence exists.

## Direction gate

The minimum Direction decision after this recalibration is:

> Accept or reject the recalibrated Roadmap 3.x technical evidence package,
> with every external-evidence, trust, route-authority, persistence,
> workforce and provider boundary preserved, without authorizing a route
> adapter, product remediation, runtime activation or Roadmap 4.x execution.

Direction may accept the evidence package without accepting any individual
legacy route destination. A route-family decision is a separate authority
event.

## 4.x entry contract produced by 3.x

Before any later 4.x implementation block, the selected family must have:

1. one family, one owner and one authority owner;
2. one explicit destination policy and compatibility obligation;
3. identity, tenant, permission and confirmation semantics;
4. payload, response, lifecycle and persistence ownership;
5. negative bypass tests and protected-surface tests;
6. rollback and recovery evidence at the same boundary;
7. applicable provider, credential, network and deployment evidence;
8. a new checkpoint and publication review.

The maximum first block remains one F-004 family. No 4.x work is selected or
executed by Macro 04.

## Evidence quality and measurement

Facts, inferences, decisions and deferrals are labelled separately. Static
inspection proves repository structure and source-callable paths; it does not
prove live execution. External evidence is recorded as pending when the
repository cannot provide it. Operation duration is measured only from
captured timestamps; inherited operator-reported durations retain their
original quality label and are not merged into a fabricated end-to-end value.

## Stable result vocabulary

Allowed Macro 04 results are:

- `ROADMAP_3X_TRUE_COMPLETION_TECHNICAL_EVIDENCE_COMPLETE_DIRECTION_DECISIONS_READY`
- `ROADMAP_3X_TRUE_COMPLETION_PARTIAL_WITH_EXPLICIT_TECHNICAL_GAPS_PLANNED`
- `ROADMAP_3X_TRUE_COMPLETION_BLOCKED_WITH_EVIDENCE_PRESERVED`

Forbidden result claims are `ROADMAP_3_X_CLOSED`, `B7_ACCEPTED`,
`PRODUCTION_READY` and `ROADMAP_4_X_STARTED`.

`ROADMAP_3X_TRUE_COMPLETION_CONTRACT_PUBLISHED_FOR_MACRO_04`
