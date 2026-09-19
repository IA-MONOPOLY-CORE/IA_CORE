# Mission Closure Gate V1

`mission_closure_gate.v1` is the executable authority for future governed
repository closures. It is a standard-library Python validator, not a product
capability, runtime component, business permission, tenant authority, or GOKV
promotion mechanism.

## Authority boundary

```text
AGENT_NARRATIVE_HAS_ZERO_CLOSURE_AUTHORITY
EXECUTABLE_CLOSURE_GATE_IS_THE_ONLY_CLOSURE_AUTHORITY
NO_SELF_DECLARED_PASS
NO_NARRATIVE_CLOSURE_OVERRIDE
NO_MISSING_FIELD_DEFAULTS
NO_PLACEHOLDER_AS_FINAL_EVIDENCE
NO_PASS_STRING_AS_COMMIT_HASH
NO_POST_BASIS_EXECUTABLE_CHANGE_WITHOUT_REVALIDATION
NO_UNRENDERED_FINAL_REPORT
NO_GATE_BYPASS_FLAG
```

The agent proposes a state, structured evidence supports it, the gate adjudicates
it, and the operator accepts or rejects the next step. A report cannot manufacture
an absent hash, a missing command, an inconsistent clock, a dirty tree, or a
post-validation executable change.

## Operations

```text
python scripts/validate_mission_closure.py validate-readiness --repo-root C:\\IA_CORE --evidence docs/ROADMAP_4X_MACRO_05_1_CANONICAL_CLOSURE_EVIDENCE.json
python scripts/validate_mission_closure.py validate-prelock --repo-root C:\\IA_CORE --evidence docs/ROADMAP_4X_MACRO_05_1_CANONICAL_CLOSURE_EVIDENCE.json
python scripts/validate_mission_closure.py render-postpublish --repo-root C:\\IA_CORE --evidence docs/ROADMAP_4X_MACRO_05_1_CANONICAL_CLOSURE_EVIDENCE.json --report-output <explicit-output>
```

`validate-readiness` requires a real validation-basis commit and explicitly marked
`AWAITING_LEVEL_B` fields. `validate-prelock` requires final evidence, Level B, a
clean documentary-only working tree at the lock parent, and a complete manifest.
`render-postpublish` requires fetched `HEAD == origin/main`, `0/0`, a clean tree,
the documentary-lock parent, and an ancestor functional publication head. It
renders every report section from the canonical JSON and emits the final receipt.

The parser rejects `--force`, `--skip`, `--allow-incomplete`, `--ignore-failure`,
`--trust-agent`, and equivalent configured bypass environment variables. Duplicate
JSON keys, non-UTF-8 input, `PASS` as a hash, `PENDING`, missing `UNKNOWN` causes,
unlisted changed files, and incomplete validation runs fail closed.

## Fixed point and tamper resistance

The evidence never embeds the hash of the documentary lock commit that contains
it. The postpublish envelope reports the live hash after fetch. The final report
hash covers the exact rendered body before the receipt block; changing one byte
causes deterministic-output verification to fail. No second commit is created to
chase the lock hash.

## Future use

Every future governed mission that claims `CLOSED` must use this gate or a
compatible successor that is at least as strict. Historical closures remain
historical evidence; this rule does not rewrite them. Macro 05 is reconciled
explicitly by Macro 05.1 because its report completeness was narrative rather
than machine adjudicated.
