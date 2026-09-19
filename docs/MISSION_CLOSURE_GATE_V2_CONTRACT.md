# Mission Closure Gate V2

`mission_closure_gate.v2` is an additive, generic successor to V1. V1 remains
the historical authority for Macro 05.1 and is not rewritten. V2 receives
mission identity, baseline, cursor, protected paths, report sections and
validation gates from a strict versioned policy.

## Authority

```text
AGENT_PROPOSES_CLOSURE
EVIDENCE_SUPPORTS_CLOSURE
EXECUTABLE_GATE_V2_ADJUDICATES_CLOSURE
OPERATOR_ACCEPTS_OR_REJECTS_NEXT_STEP
```

V2 preserves the V1 controls: no self-declared pass, no report-only closure, no
evidence by omission, no missing-field defaults, no placeholders as final
evidence, no `PASS` hash, no post-basis executable change, no unrendered report,
no bypass flags, and no narrative override.

## Operations

```text
validate-policy
validate-readiness
validate-prelock
render-postpublish
```

`validate-policy` checks the policy schema, immutable controls, protected
frontier and explicit remote enforcement state. Readiness and prelock consume
the same policy and canonical evidence. Postpublish performs a fresh
`git fetch origin --prune`, then separately reports local tracking equality,
remote fetch verification and remote ruleset enforcement.

The renderer is the only producer of the final report receipt. A documentary
lock may contain the evidence bytes while the final report hash is produced
after fetch, avoiding a self-referential commit.

## Post-validation invalidation

Only `DOCUMENTARY_ONLY` and `EVIDENCE_ONLY` changes are allowed after the final
Level B basis. Executable, test-infrastructure, configuration and product
changes invalidate the basis. The exact post-Level-B list is recorded in the
manifest; it cannot be replaced with a broad directory exclusion.

## External frontier

Repo-local CI integration is provided. Branch protection, required checks and
remote rulesets are not observable from this repository mission. The canonical
state therefore remains `REMOTE_ENFORCEMENT: NOT_PROVEN` and requires operator
configuration described in the companion action document.
