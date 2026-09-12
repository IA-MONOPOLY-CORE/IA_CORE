# Roadmap 4.x Entry Contract

## Status

- Prepared by Macro 03, not executed.
- State: `PARTIAL_BLOCKED_BY_B7_DIRECTION_ACCEPTANCE_AND_EXTERNAL_EVIDENCE`.
- Parent baseline: `8eda61c1c6e1611435cf4d4881a374502018abdc`.
- Precondition: B-7 must be accepted with explicit limits; acceptance is not simulated here.
- Canonical doctrine: [IA_CORE One Core, Four Surfaces](C:/IA_CORE/docs/IA_CORE_ONE_CORE_FOUR_SURFACES_DOCTRINE.md).
- Governing method: [Method Santi 3.2.2](C:/IA_CORE/docs/METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION.md).

This is an entry contract, not a roadmap execution plan. It defines what a
future authorized mission would need before changing one F-004 family. It does
not select a legacy destination, implement an adapter, activate runtime or
open Roadmap 4.x.

## Purpose

Roadmap 4.x may address one bounded, evidence-backed legacy boundary after
Roadmap 3.x has been accepted. The purpose is surgical remediation of a proven
authority gap, not broad system activation or simultaneous modernization of all
36 routes.

## Preconditions inherited from Roadmap 3.x

1. B-7 acceptance exists as an explicit Direction decision.
2. The selected F-004 family has one named service owner and one authority owner.
3. Destination policy is one of `KEEP_CANONICAL`, `MIGRATE_TO_CANONICAL`,
   `REPLACE_WITH_SUCCESSOR`, `INTERNAL_ONLY` or `REMOVE`, with compatibility
   evidence; `UNKNOWN` remains valid until then.
4. Identity, authentication, authorization, ownership and tenant semantics are
   evidenced for the selected exposure, or the work remains internal/sandbox-only.
5. Payload, response, permission, confirmation, activation and lifecycle
   semantics are explicit for the selected family.
6. Persistence destination, retention, rollback and recovery owner are explicit
   for every write-capable path.
7. Provider, credential, network and deployment boundaries are either irrelevant
   to the selected family or separately authorized and evidenced.
8. Historical, canonical and negative tests are selected by risk and retain
   their existing assertions.
9. One Core, Four Surfaces remains the shared architectural authority; no product
   fork is introduced.

## Authorized surfaces for a future mission

Only after the preconditions pass may a future mission authorize:

- one F-004 family and its directly necessary route contract;
- documentation, static evidence, focused tests and one bounded implementation
  surface if Direction explicitly authorizes it;
- a reversible compatibility boundary with an explicit rollback owner;
- contract-aware internal containment where it is safer than public exposure.

The maximum first coherent block is **one family**, not all 36 routes. A second
family requires a new coherence and gate review.

## Prohibited surfaces

Unless a separate contract explicitly authorizes them, the future mission must
not change or activate:

- unrelated legacy families or the full API surface;
- P0, P1, P3 matrix, UI contract-aware widgets or Request Draft Panel;
- payload v2, new endpoints, integrations, providers or public API authority;
- runtime, execution, workforce, agent calls, DNS, HTTP, sockets or external traffic;
- secret values, live stores, production persistence or unowned tenant data;
- IA_CORE OS, mobile, kernel, drivers, AOSP or independent product forks.

## `NEXT_MACRO_MISSION_CANDIDATE`

`ARCHITECT_SELECTS_ONE_F004_FAMILY_REMEDIATION_BLOCK_AFTER_B7_ACCEPTANCE`

Candidate shape, not selection:

```text
one F-004 family
  -> authority and owner contract
  -> identity/tenant and compatibility evidence
  -> permission/confirmation/payload/lifecycle contract
  -> bounded implementation or containment decision
  -> negative bypass tests
  -> rollback and recovery proof
  -> checkpoint and publication review
```

The first candidate family must be chosen by the Architect/Direction after the
F-004 record is accepted. This document does not choose P1 through P9.

## Gates

### Entry gate

- B-7 acceptance recorded.
- selected family has complete route membership and no duplicates;
- owner, destination, compatibility obligation and stop condition are explicit;
- protected-surface diff is empty before implementation;
- no external evidence is silently substituted with source presence.

### Implementation gate

- one station, one commit;
- no authority expansion beyond the selected family;
- no adapter or payload change without an explicit contract;
- negative bypass and protected-path tests pass;
- rollback is tested in the same boundary as the change.

### Publication gate

- focal, group and targeted historical suites selected by risk pass;
- JSON/schema, secret scan, prohibited diff and `git diff --check` pass;
- working tree clean;
- fetch verifies no remote divergence;
- normal push followed by fetch verifies `HEAD == origin/main` and `0/0`.

## Rollback boundary

Rollback must be station-local and preserve all prior green checkpoints. A
failed family implementation is reverted only within that family; no reset,
rebase, squash or history rewrite is permitted. Product rollback must not be
claimed from sandbox rollback evidence.

## First expected true hard frontier

`F-004_FAMILY_AUTHORITY_AND_COMPATIBILITY_DECISION`

The expected first irreducible frontier is the point where a selected family
would gain, lose or change route authority, compatibility, tenant scope or
product semantics. The future mission must stop there unless Direction has
approved that exact bounded contract. Provider/network or deployment evidence
may become the next external frontier for P1, P2, P7, P8 or P9.

## Required human decisions

- accept or reject B-7 closure with explicit deferred frontiers;
- select one F-004 family and its destination policy;
- approve any authority, compatibility, identity, tenant, persistence or
  external-evidence change required by that family.

No human decision is needed to keep the current repository read-only and
`UNKNOWN` routes unchanged.

## Residual risks

- static route evidence cannot show actual deployment exposure or traffic;
- all 36 routes remain potential compatibility obligations;
- settings and provider paths retain secret, network and ownership boundaries;
- sandbox rollback does not establish product recovery;
- future OS/mobile documents remain reservations only.

`ROADMAP_4_X_ENTRY_CONTRACT_PREPARED_NOT_EXECUTED`
