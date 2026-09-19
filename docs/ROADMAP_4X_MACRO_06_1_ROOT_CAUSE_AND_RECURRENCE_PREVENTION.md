# Macro 06.1 Root Cause and Recurrence Prevention

## Root cause

Macro 06 V2 combined a strong declarative vocabulary with an incomplete
execution boundary. Fields such as `allowed_change_paths`,
`protected_path_prefixes`, `protected_diff` and remote enforcement state were
present in policy/evidence, but the validator did not consistently derive
their truth from live Git or allow a legitimate state transition. The tests
also over-weighted in-memory mutation and under-tested temporary repository
state.

## Causal chain

```text
DECLARATIVE_POLICY
-> MISSING_LIVE_ADJUDICATION
-> SHALLOW_NEGATIVE_COVERAGE
-> FALSE_GREEN_CLOSURE
-> OPERATOR_FALSE_ASSURANCE
-> RECURRENCE_DEBT
```

## Prevention controls

| root-cause surface | V2.1 prevention | proof |
| --- | --- | --- |
| policy/diff disconnect | computed baseline, basis and working path sets | scope tests and final scope validator |
| self-declared protected diff | classification and prefix calculation from Git | protected-path adversarial fixture |
| evidence chronology | strict clocks and commit-time comparison | chronology corpus and receipts |
| post-finalization contamination | canonical evidence separated from receipts | post-evidence and prelock flow |
| CI identity ambiguity | independent job and exact command contract | CI contract tests/workflow |
| remote rigidity | NOT_PROVEN/PROVEN/REVOKED_OR_STALE model | remote-state tests |
| historical scope bleed | exact continuity sets in legacy guards | historical-impact cohort |
| report incompleteness | exact required section set and renderer-owned hash | report contract and render gate |

## Boundary

These controls apply to closure authority and evidence. They do not authorize
product remediation, runtime activation, external exposure or P3 execution.
