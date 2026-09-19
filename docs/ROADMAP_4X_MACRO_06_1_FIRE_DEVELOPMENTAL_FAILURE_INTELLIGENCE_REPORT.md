# Roadmap 4.x Macro-Mission 06.1 - FIRE Developmental Failure Intelligence Report

Status: `DEVELOPMENTAL_DOCUMENTARY_ONLY`. FIRE runtime is not implemented.

The failure profile below converts the audited Macro 06 V2 weaknesses into
bounded controls and regression nodes. It does not attribute intent to any
agent or system.

## Failure classes

| failure_case | failure_fingerprint | failure_locality | failure_propagation | common_mode_risk | coverage_gap | resilience_debt | existing_defense | failed_defense | repair_control | regression_test | residual_risk | applicability_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FAILURE_CLASS_1: DECLARATIVE_ENFORCEMENT_GAP | allowlist/prefix declared but not applied to Git | V2 manifest/policy boundary | policy field declared -> executable does not enforce -> tests do not mutate real state -> pass can be accepted | all declarative controls share the same blind spot | no real temporary-repo diff fixtures | policy-to-execution drift | V2 policy validation | V2 did not adjudicate live diff | V2.1 computes baseline/head/working sets and classification | `test_allowlist_is_enforced_against_real_git_diff`, `test_untracked_path_cannot_hide_outside_manifest` | a new path class may require future policy extension | closure method files only |
| FAILURE_CLASS_2: CAUSAL_CHRONOLOGY_GAP | future or inverted run clocks can be embedded in evidence | evidence timeline | impossible clock -> evidence appears complete -> operator receives false temporal assurance | all station clocks can drift together | no strict run/finalization/basis order | event provenance was narrative | V2 run shape checks | V2 accepted incompatible chronology | V2.1 rejects future clocks, inversion, post-finalization runs and basis-before-commit | `test_started_after_completed_is_blocked`, `test_run_after_evidence_finalization_is_blocked`, `test_level_b_before_basis_commit_is_blocked` | local clocks can still be wrong if host time is wrong | evidence lifecycle only |
| FAILURE_CLASS_3: CI_IDENTITY_GAP | requested check exists only as a step | workflow identity | step -> no selectable job -> required-check instruction cannot bind -> operator could accept false assurance | all checks named in prose but not job identity | no parser for independent job block | CI contract not executable | workflow text contained a step | no stable job contract | V2.1 checks job/check equality and exact commands | `test_required_check_is_a_real_job_with_stable_identity`, `test_workflow_has_independent_job_block` | hosting provider may still rename or disable the check | local CI contract only |
| FAILURE_CLASS_4: NON_EVOLVABLE_REMOTE_STATE | validator only accepts NOT_PROVEN | remote evidence state model | valid future proof -> validator rejects -> state cannot evolve -> operator loses accurate status | hardcoded state transitions | no positive PROVEN/STALE fixtures | remote truth model cannot mature | V2 state restriction | no complete external fields path | V2.1 validates NOT_PROVEN, PROVEN and REVOKED_OR_STALE requirements | `test_remote_proven_can_be_valid_when_all_evidence_exists`, `test_stale_remote_state_requires_reason_and_operator_action` | V2.1 does not obtain external evidence itself | remote metadata only |
| FAILURE_CLASS_5: SELF_VALIDATION_COVERAGE_GAP | negative tests mutate dictionaries but not repository state | adversarial corpus | shallow mutation -> blind spot -> false green -> future mission inherits weak control | all controls tested in memory only | missing rename/untracked/post-basis corpus | test confidence exceeds exercised reality | V2 unit tests | no real Git fixtures | V2.1 temporary Git repos and compatibility corpus | `test_protected_diff_is_computed_and_blocks_core_path`, `test_rename_evasion_is_blocked`, `test_post_basis_executable_change_is_invalidated_even_when_allowlisted` | untested path forms may remain | closure test infrastructure |

## Common propagation chain

```text
POLICY_FIELD_DECLARED
-> EXECUTABLE_DOES_NOT_ENFORCE
-> TEST_DOES_NOT_MUTATE_REAL_REPOSITORY_STATE
-> GATE_REPORTS_PASS
-> OPERATOR_COULD_ACCEPT_FALSE_ASSURANCE
-> FUTURE_MISSION_INHERITS_WEAK_CONTROL
```

## FIRE output

The repair is deliberately bounded: V2.1 controls only closure method
infrastructure, test infrastructure, configuration and documentary evidence.
It does not become a product control plane. The residual risk is the gap
between local proof and host-side enforcement, which remains explicitly
`NOT_PROVEN` and requires operator action.
