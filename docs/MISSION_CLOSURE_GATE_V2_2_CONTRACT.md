# Mission Closure Gate V2.2

`mission_closure_gate.v2.2` is the additive successor to V1, V2 and V2.1.
Those historical validators, policies, fixtures and evidence remain byte
preserved. V2.2 governs only closure-method infrastructure and documentary
evidence for Roadmap 4.x Macro-Mission 06.2.

## Authority boundary

V2.2 does not authorize product, backend, frontend, HTML, CSS, JavaScript,
i18n, payload, runtime, execution, endpoint, provider, integration, tenant,
VERO, FIRE, Cognitive Kernel, Enterprise Foundry, Cyber Range or
Organizational Reconstruction runtime changes. P3 remains selected and not
started. External enforcement remains `NOT_PROVEN` until provider-originated
evidence is supplied by an operator.

## Four independent Git surfaces

The gate recomputes all of the following directly:

```text
POST_BASIS_COMMITTED_DELTA
INDEX_DELTA
WORKTREE_DELTA
UNTRACKED_PATHS
```

The baseline-to-HEAD committed delta is also recomputed for the final
manifest. A path set is not treated as proof of content or state integrity.
Rename, copy, deletion, staged, unstaged, untracked and same-path
post-basis changes are all visible to the authority. Protected paths are
computed from these surfaces and cannot be self-declared empty.

## Executable diff checks

V2.2 executes and records independently:

```text
git diff --check validation_basis..HEAD
git diff --cached --check
git diff --check
```

Each receipt contains the exact command, timestamps, exit code and stdout and
stderr hashes.

## Terminal validation authority

The required order is:

```text
FOCAL VALIDATION
HISTORICAL IMPACT VALIDATION
LEVEL A COMPLETE
VALIDATION BASIS FREEZE
EXACTLY ONE SUCCESSFUL TERMINAL LEVEL B FOR THE FINAL BASIS
EVIDENCE FINALIZATION
POSTPUBLISH CLOSURE VERIFICATION
```

Failed Level B attempts may occur for earlier bases when followed by a repair
and a new basis. For the final basis, exactly one successful terminal Level B
is required. Ordinary validation after that terminal run is invalid. Only
hash, receipt, Git-state, allowlist, lineage, rendering and publication
verification may follow it.

## Receipts and deterministic rendering

Validation receipts bind commands to durable repository-relative stdout,
stderr and combined-log artifacts. The receipt hash is computed over a
canonical UTF-8 JSON payload with `receipt_sha256` excluded. The validator
recomputes the receipt hash and every referenced artifact hash.

The deterministic report payload excludes wall-clock and machine-local data.
Two independent canonical renders over the same inputs must have identical
bytes and SHA-256. A live postpublish envelope may contain volatile execution
metadata, but it does not change the deterministic report hash.

## Remote enforcement

`PROVEN` requires provider-originated source, capture time, proof commit, proof
SHA and provider response reference. A local policy, workflow or self-authored
declaration cannot elevate `NOT_PROVEN`. This mission records
`REMOTE_ENFORCEMENT: NOT_PROVEN` and `OPERATOR_ACTION_REQUIRED: YES`.

## Organizational Reconstruction preservation

The future Organizational Reconstruction and Structured Enterprise Discovery
candidate is preserved in one canonical document only. It has no tests,
schemas, runtime, stores, endpoints, services, UI, providers, integrations or
implementation scaffolding in this mission.
