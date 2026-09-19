# Mission Closure Gate V2.1 Contract

`mission_closure_gate.v2.1` is the additive, fail-closed successor used by
Roadmap 4.x Macro-Mission 06.1. V1 and the Macro 06 V2 validator remain
historical artifacts. V2.1 does not rewrite either authority.

## Authority boundary

V2.1 governs closure evidence for the repository method layer only. It does
not authorize product, backend, runtime, execution, endpoint, tenant,
provider, integration, GOKV promotion, OCI activation, VERO runtime or FIRE
runtime changes. External enforcement remains `DEFAULT_DENIED` and
`NOT_PROVEN` until host-side evidence is supplied by an operator.

## Scope enforcement

The gate computes three sets from Git:

1. baseline-to-HEAD changed paths;
2. validation-basis-to-HEAD changed paths;
3. working-tree paths, including staged and untracked files.

The final manifest must equal the computed baseline-to-HEAD set. Every path
must be in the exact policy allowlist and must match the executable
classification derived from its normalized path. Rename/copy attempts,
case-variant paths, traversal, absolute paths and untracked paths outside the
manifest fail closed.

Protected prefixes and product classifications are evaluated from Git. A
declared `protected_diff: EMPTY` is not authoritative; the gate recomputes
the protected result and rejects any protected/product path.

Post-basis changes are restricted to `DOCUMENTARY_ONLY` and `EVIDENCE_ONLY`.
Executable, test-infrastructure, configuration and product changes after the
frozen validation basis invalidate the closure.

## Causal evidence

All clocks are ISO-8601 values with offsets and cannot be in the future. The
machine-enforced station order is:

```text
MISSION_ACCEPTED
<= PREFLIGHT_COMPLETED
<= VALIDATION_BASIS_COMMITTED
<= FINAL_LEVEL_B_STARTED
<= FINAL_LEVEL_B_COMPLETED
<= CANONICAL_EVIDENCE_FINALIZED
```

Every validation run also enforces `started_at <= completed_at`, and no run
may complete after canonical evidence finalization. The validation wrapper
records actual start/end clocks, exit code, counts, wall time and output hash.

Canonical evidence contains only pre-finalization facts. Post-evidence and
prelock are separate machine-generated receipts. The documentary lock stores
the finalized evidence and receipts. The postpublish envelope is generated
after a fresh fetch and live Git equality check.

## Remote state

The policy accepts three states:

* `NOT_PROVEN`: local closure may pass, but operator action is required;
* `PROVEN`: complete host-side ruleset and observed-run evidence is required;
* `REVOKED_OR_STALE`: stale reason and operator action are required.

The mission records `NOT_PROVEN`; the existence of a workflow or a local test
does not prove a host-side required status check.

## CI contract

`.github/workflows/ci.yml` contains the independent job and check identity
`closure-policy-and-anti-weakening`. The job validates policy, runs the V2.1
focal/adversarial corpus, and runs the historical V1/V2 compatibility corpus.
The repository only proves that the job exists in workflow text; host-side
required-check enforcement remains an operator responsibility.

## Commands

```text
python scripts/validate_mission_closure_v2_1.py validate-policy --repo-root . --policy docs/ROADMAP_4X_MACRO_06_1_MISSION_POLICY.json --schema docs/MISSION_CLOSURE_POLICY_SCHEMA_V2_1.json
python scripts/run_mission_validation_v2_1.py --label <label> --validation-basis <full-hash> --receipt-output <path> --log-output <path> -- python -m pytest -q <cohort>
python scripts/validate_mission_closure_v2_1.py finalize-evidence --evidence <draft> --output <canonical>
python scripts/validate_mission_closure_v2_1.py validate-post-evidence ...
python scripts/validate_mission_closure_v2_1.py validate-prelock ...
python scripts/validate_mission_closure_v2_1.py render-postpublish ...
```

No bypass flag, bypass environment variable, narrative override or
self-declared pass is accepted.
