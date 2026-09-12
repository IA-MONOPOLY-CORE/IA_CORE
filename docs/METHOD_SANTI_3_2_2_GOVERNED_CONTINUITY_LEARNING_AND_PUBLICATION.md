# Method Santi 3.2.2 - Governed Continuity, Learning and Publication

## Status and authority

`METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION` is an
additive evolution of Method Santi 3.2.1. It preserves the authority layers,
contract-first behavior, safety boundaries, station model, frontier model,
learning lifecycle, and publication discipline already established by
Methods 3.0, 3.2, and 3.2.1.

The current repository, current contracts, executable tests, and published
checkpoints win over historical prose. This document is a method contract for
governed engineering. It does not create product authority, runtime authority,
execution authority, provider access, network access, or automatic promotion.

`METHOD_SANTI_3_2_2_MATERIALIZED`

## 1. Mission scale

Mission scale is governed surface throughput, not prompt count and not raw
volume. The objective is to cover the largest coherent and governable surface
in the shortest reasonable time with regulated consumption, bounded risk,
reviewable evidence, and recoverable work.

Do not optimize for fewer prompts. Do not maximize work by volume. A prompt may
contain many stations when those stations share a coherent objective, have
explicit inputs and postconditions, are independently verifiable, and remain
rollbackable. A mission extends only as far as coherence, evidence,
dependencies, and distance to the first irreducible human frontier justify.

The route must be recalculated when new evidence changes the classification of
a frontier. A shorter prompt sequence is not evidence of better engineering;
correct closure and useful evidence are.

## 2. Block, station and commit

```text
BLOQUE = sección importante completa
ESTACIÓN = pieza arquitectónica terminada y verificable
COMMIT = preservación exacta de una estación aprobada
```

A block contains every station required to satisfy its postcondition. A
material station is one coherent architectural piece with an input contract,
bounded files, validation evidence, a rollback boundary, and a next safe route.

`ONE_STATION_ONE_COMMIT` is mandatory. Every material station produces one
non-empty commit of its own. A repair caused by evidence produces a separate
repair commit and is recorded as a repair; it is not silently relabeled as the
original station. Do not split one indivisible piece merely to increase commit
count, and do not merge independent pieces until traceability is lost.

`EVERY_COMMIT_IS_ACCOUNTABLE`: a subject line is not evidence. Each commit is
checked by full hash, parent, real diff, files, tests, dependencies, side
effects, rollback, and verdict. The README follows current truth and need not
repeat every commit.

## 3. Dynamic frontier engineering

A frontier is not a permanent property of a roadmap. Earlier stations may
produce owners, contracts, adapters, tests, evidence, or learning that mature
or dissolve it. Arrival at a frontier therefore triggers a fresh evaluation
against current evidence.

Continue when the remaining behavior is already derivable from current
contracts and evidence. Pause only when a genuinely new human decision,
external fact, authority, or irreducible risk remains. If one branch is blocked,
continue other independent and safe branches when their contracts and rollback
boundaries remain clear.

For every frontier record:

- `FRONTIER_AT_MISSION_START`;
- evidence produced by each preceding station;
- current owner and governing contract;
- remaining unknowns and dependencies;
- `FRONTIER_AT_TIME_OF_ARRIVAL`;
- route recalculation result;
- safe pause condition and next candidate block.

Do not preserve a hard classification by documentary inertia. Do not dissolve a
hard frontier by optimism, naming, or a convenient test result.

## 4. Learning without model-weight retraining

IA_CORE does not depend on changing language-model weights to accumulate
operational experience. Experience is preserved through governed knowledge and
learning artifacts inside the system:

- GOKV preserves governed knowledge, provenance, scope, lifecycle, evidence,
  limitations, contradictions, and replacement history.
- DOOL preserves development-origin observations and operational experience
  without silent loss or retroactive rewriting.
- OCI delivers knowledge pertinent to a mission or agent within explicit
  resource, privacy, scope, and risk boundaries.

`PERTINENT` means neither arbitrarily minimal nor indiscriminately total. OCI
must select relevant knowledge and record bounded omissions with reasons when
resources require them. It must exclude irrelevant, stale, duplicate, private,
out-of-scope, or risk-incompatible material.

There is no artificial quota of promotable learnings. Any learning that meets
Promotion Governance criteria is eligible for review. No learning is promoted
merely because it is recent, persuasive, numerous, or useful to the current
author. Promotion is explicit, evidence-based, and never automatic.

## 5. Governed continuity across chats, agents and projects

Every close produces a self-sufficient handoff. A new chat, agent, mission, or
project should not reconstruct the entire history merely to continue. The
handoff inherits the current state, decisions, contracts, evidence, unknowns,
frontiers, commit chain, rollback point, protected boundaries, and next safe
point.

Inheritance must be sufficient and pertinent. It must not load irrelevant,
private, stale, duplicate, risky, or out-of-scope history just because that
history exists. The repository and versioned artifacts are part of the
operational intelligence and remain the authoritative recovery surface.

## 6. Full report by default

Every operational prompt must request one self-contained final report from the
start. The report must be concrete and detailed enough that Direction and the
conversational architect do not need a second interaction whose only purpose
is explanation.

When applicable, the report includes:

- exact operational result and any deviation;
- initial and final Git state;
- sources read and contract authorities;
- baseline, collection, focal, historical, global, compile, secret, and
  boundary validation;
- every failure, node, cluster, classification, and resolution;
- files changed and files protected;
- each block, station, postcondition, rollback boundary, and next route;
- every commit and its purpose, files, tests, dependencies, and verdict;
- every repair commit, explicitly named;
- skips, xfails, optional dependencies, and their reasons;
- learning reused, created, promoted, not promoted, or intentionally not
  preserved;
- frontier disposition, unknowns, capabilities not demonstrated, and human
  decisions still required;
- local and remote Git state;
- the next technical recommendation without executing it.

## 7. Checkpoints and governed publication

The publication rules are:

- `PUSH_ONLY_AT_PUBLISHABLE_CHECKPOINT`;
- `GREEN_STATIONS_MAY_BE_PUBLISHED_AT_TRUE_FRONTIER`;
- `REMOTE_VERIFICATION_IS_PART_OF_PUBLICATION`;
- `README_FOLLOWS_CURRENT_TRUTH_NOT_EVERY_COMMIT`.

A push is not justified by elapsed time, prompt count, or a fixed number of
commits. It is justified only by a coherent, green, traceable, useful restore
point with closed stations, an updated ledger, required validation, a clean
working tree, `git diff --check` PASS, secret and prohibited-diff checks PASS,
and no remote divergence.

The publication sequence is:

```text
final validation
-> final checkpoint commit
-> git fetch origin
-> verify divergence
-> git push origin main
-> git fetch origin
-> verify HEAD == origin/main
-> verify ahead/behind 0/0
-> verify working tree clean
```

If the remote diverges, do not pull, merge, rebase, reset, or force-push.
Preserve the local evidence and safe-pause with the exact state mismatch.

## 8. Station execution contract

Before a station starts, state its input, scope, authority, protected paths,
expected postcondition, tests, side-effect boundary, rollback action, and
frontier hypothesis. During the station, inspect real files and real diffs;
do not rely on planned commit names or optimistic status text. At closure,
record the observed result and recalculate the next route.

The minimum station gate is:

```text
preflight
-> materialize one coherent piece
-> focal validation
-> regression validation
-> boundary and side-effect validation
-> real diff review
-> ledger/evidence update
-> one station commit
```

Historical tests validate their own checkpoint contract. Current tests validate
the current contract. A historical failure is not a current product defect,
and a green result obtained by silencing an assertion is not convergence.

## 9. Safety and stop conditions

Stop and report when closure would require a real provider, network, credential
value, runtime, payload, endpoint, integration, product semantic change without
contract authority, or unresolved human decision. Do not add skips or xfails to
lower a counter, delete assertions, mass-regenerate snapshots, widen guards,
mock the exact unit under test, or change production to satisfy an
unauthoritative historical expectation.

`TEST_SAFETY_MUST_BE_ENFORCED_NOT_ASSUMED` remains active. Collection must be
side-effect free. Test writes must be temporary or sandbox-injected before the
write. Restore is recovery evidence, not hermeticity proof. External probes
remain explicit and opt-in.

The method never authorizes implementation of IA_CORE OS, mobile products,
kernel, drivers, AOSP, workforce activation, new integrations, providers, or
product execution. Those are separate future decisions and contracts.

## 10. Reusable handoff template

```text
MISSION_ID:
ENTRY_HEAD / ENTRY_ORIGIN:
CURRENT_STATION:
BLOCK_AND_POSTCONDITION:
CONTRACT_AUTHORITY:
PROTECTED_SURFACES:
EVIDENCE_AND_TESTS:
FAILURES_AND_CLASSIFICATIONS:
LEARNING_REUSED_OR_CANDIDATE:
FRONTIER_AT_ARRIVAL:
ROLLBACK_BOUNDARY:
COMMIT:
NEXT_SAFE_ROUTE:
HUMAN_DECISION_REQUIRED:
```

An empty field must be declared `NOT_APPLICABLE` with a reason; it must not be
silently omitted. The handoff is complete only when another authorized worker
can resume from the recorded checkpoint without guessing.

## 11. Closure statement

Method Santi 3.2.2 is a governed continuity, learning, and publication layer.
It expands operational clarity without expanding product authority. It keeps
human direction explicit, makes evidence reusable, treats frontiers as dynamic,
and makes publication a verified restore point rather than a ceremonial push.

`METHOD_SANTI_3_2_2_GOVERNED_CONTINUITY_LEARNING_AND_PUBLICATION_PASSED`

The print-ready companion is
`docs/generated/METHOD_SANTI_3_2_2_ONE_CORE_FOUR_SURFACES_PRINT_READY.html`.
The Markdown remains the canonical source. No deterministic local PDF renderer was available
in this environment and no dependency was installed; the HTML fallback is therefore the
verified exportable artifact for this checkpoint.
