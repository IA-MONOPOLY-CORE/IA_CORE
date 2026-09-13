# Roadmap 3.x Completion Execution Plan

## Purpose and state

- Plan state: `EXECUTABLE_PLAN_READY_NOT_STARTED`
- Mission: `ROADMAP_3X_MACRO_MISSION_04_TRUE_COMPLETION_RECALIBRATION_EVIDENCE_COVERAGE_AND_CLOSURE_PATH`
- Current baseline: `43530e656066a3c40d9afb8a5a4a381b38f29f38`
- Next phase: Roadmap 4.x only after explicit 3.x acceptance and one-family
  selection.

This is an executable plan in the sense of ordered work, owners, inputs,
gates, tests, rollback and stop conditions. It does not execute any item in
the plan and does not authorize production remediation.
Do not start 4.x from this document.

## Operating invariants

1. One coherent boundary per mission; the first 4.x implementation maximum is
   one F-004 family.
2. One material station equals one accountable commit.
3. `UNKNOWN` remains the route destination until authority and compatibility
   evidence exist.
4. No product change is implied by a green documentary checkpoint.
5. External evidence, human decisions and source evidence remain separate.
6. Every future implementation block has a negative bypass test, rollback
   test, protected-surface test and post-publication checkpoint.

## Work packages

| Package | Objective | Inputs | Exit evidence | Owner | State |
| --- | --- | --- | --- | --- | --- |
| `3X-0` | Publish the recalibrated contract, original-scope coverage, gap register, decision packet and plan. | Macro 03 published evidence and current repository. | Macro 04 checkpoint, JSON, ledger, tests and clean published head. | Architecture/test owner | `CURRENT_MISSION` |
| `3X-1` | Consume the Direction acceptance decision for the technical evidence package. | Direction packet Decision 1. | Recorded accept/reject decision with explicit F-001 through F-011 limits. | Direction/Architect | `BLOCKED_PENDING_DECISION` |
| `3X-2` | Close applicable external and trust evidence without changing product behavior. | Accepted package, deployment/security/provider owners. | Identity, tenant, CORS, ingress, provider and credential evidence, or an explicit deferral. | Hosting/security/provider owners | `BLOCKED_PENDING_EXTERNAL_EVIDENCE` |
| `3X-3` | Select one F-004 family and disposition for a later bounded review. | Accepted package plus external/owner evidence. | One family, one destination, owner, compatibility contract and stop condition. | Direction plus selected route owner | `BLOCKED_PENDING_SELECTION` |
| `4X-1` | Implement or contain exactly one selected family under its contract. | `3X-3` output; approved identity, payload, lifecycle, store and rollback contract. | Focused implementation, negative bypass suite, rollback proof and checkpoint. | Selected family owner | `FUTURE_AUTHORIZED_ONLY` |
| `4X-2` | Reassess the remaining families and whether another block is coherent. | Published `4X-1` evidence. | New direction packet or safe pause; no automatic second-family expansion. | Direction/Architect | `FUTURE_REVIEW_ONLY` |

## Ordering by distance to the next true hard frontier

### Immediate and autonomous

- validate the Macro 04 contract, crosswalk and gap register;
- verify exact 36-route accounting and preserved `UNKNOWN` destinations;
- run focused, historical and full tests;
- run JSON/schema, Python compile, secret-pattern, protected-diff and
  `git diff --check` gates;
- publish only after clean-tree and remote-equality verification.

These activities cannot change route authority or product behavior.

### Decision-gated

- Direction accepts or rejects the recalibrated evidence package;
- Direction and owners define whether external evidence is sufficient;
- Direction selects one F-004 family and its destination policy.

The executor must stop at each gate and may not infer approval from a green
test suite or a source-callable implementation.

### Future implementation-gated

- define the selected family's route, identity, tenant, permission,
  confirmation, payload, lifecycle and persistence contract;
- prove compatibility and external-consumer impact;
- implement the smallest reversible boundary or document containment;
- prove no bypass into a second authority;
- prove rollback at the same boundary;
- publish and re-evaluate the next frontier.

## Gate matrix for a future one-family block

| Gate | Pass condition | Required negative proof | Stop if |
| --- | --- | --- | --- |
| Entry | B7/evidence acceptance and one-family selection are recorded. | Protected diff is empty before work. | Acceptance or selection is missing. |
| Authority | Destination, owner and compatibility obligations are explicit. | No unselected route or second authority is touched. | Policy is inferred or route list is incomplete. |
| Trust | Identity, tenant, permission and confirmation semantics are evidenced. | Unauthorized caller and cross-tenant cases are rejected. | Trust policy remains unknown. |
| Payload | Existing payload contract is explicit and no v2 is invented. | Invalid/forbidden fields do not reach the boundary. | Payload ownership is ambiguous. |
| Lifecycle | States, activation and terminal behavior are contractually bounded. | Runtime/processing/active paths remain closed unless authorized. | A contract-only gate would need to open. |
| Persistence | Destination, retention and owner are explicit. | Unowned or out-of-scope writes are rejected. | Product store or tenant ownership is unknown. |
| External | Provider/network/deployment evidence is applicable and accepted. | No unapproved DNS, socket, HTTP or credential use. | The selected family needs unobserved external facts. |
| Recovery | Rollback and recovery owner are tested in the same boundary. | Failed partial work leaves the prior checkpoint intact. | Rollback is only hypothetical. |
| Publication | Focal/group/historical suite and diff gates pass. | Protected product paths remain unchanged. | Green evidence cannot be reproduced. |

## Remaining-mission estimate

The exact number of future missions is not knowable from static source. The
minimum path is one Direction decision cycle plus the applicable external and
owner evidence gates, followed by at least one separately authorized family
mission. Additional missions are expected if a family exposes a new trust,
provider, persistence or recovery frontier. This is a bounded dependency
statement, not a duration promise.

## Safe pause conditions

Pause at the latest green checkpoint if:

- a requested step changes route authority, tenant scope or compatibility;
- an external fact is needed but unavailable or unapproved;
- a product file, payload, endpoint, provider, store, runtime or integration
  would need modification outside the current contract;
- a second F-004 family is required for coherence;
- negative tests or rollback cannot be made explicit;
- Direction has not recorded the necessary acceptance or selection.

`ROADMAP_3_X_COMPLETION_EXECUTION_PLAN_READY_WITH_4X_BLOCKED_UNTIL_AUTHORIZED`
