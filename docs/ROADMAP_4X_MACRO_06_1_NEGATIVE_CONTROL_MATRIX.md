# Macro 06.1 Negative Control Matrix

The matrix records adversarial intent, the real test node and the observed
outcome. A negative fixture is successful when the gate rejects the mutation;
the pytest process therefore exits `0` while the fixture gate raises
`GateFailure` as expected.

| control_id | threat | fixture | mutation | expected_failure | test_node_id | actual_exit_code | actual_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NC-POL-001 | missing policy field | in-memory policy | remove `branch` | policy validation failure | `test_v2_1_policy_and_schema_are_valid` plus required-field path | 0 | rejection exercised |
| NC-POL-002 | wrong type | policy fixture | replace list with scalar | type/shape failure | `validate_policy` contract | 0 | rejection exercised |
| NC-POL-003 | duplicate JSON key | strict loader | duplicate key | duplicate key failure | strict loader in `load_json` | 0 | rejection exercised |
| NC-POL-004 | immutable control removal | policy copy | remove `NO_EVIDENCE_FROM_THE_FUTURE` | incomplete controls | `test_invariant_control_remains_required` | 0 | rejection exercised |
| NC-POL-005 | bypass environment | process environment | set `CLOSURE_GATE_FORCE` | bypass failure | `test_bypass_environment_is_rejected` | 0 | rejection exercised |
| NC-POL-006 | remote state without action | remote fixture | NOT_PROVEN + false action | remote failure | `test_remote_not_proven_requires_operator_action` | 0 | rejection exercised |
| NC-POL-007 | incomplete PROVEN | remote fixture | omit ruleset/run fields | external evidence failure | `test_remote_proven_requires_complete_external_evidence` | 0 | rejection exercised |
| NC-GIT-001 | outside allowlist | temporary Git repo | commit `docs/evil.md` only allow `docs/allowed.md` | path outside allowlist | `test_allowlist_is_enforced_against_real_git_diff` | 0 | rejection exercised |
| NC-GIT-002 | protected path | temporary Git repo | commit `core/secret.py` | protected paths changed | `test_protected_diff_is_computed_and_blocks_core_path` | 0 | rejection exercised |
| NC-GIT-003 | false classification | temporary Git repo | declare `scripts/fake.py` documentary | classification mismatch | `test_path_classification_cannot_relabel_code_as_documentation` | 0 | rejection exercised |
| NC-GIT-004 | rename evasion | temporary Git repo | rename `docs/before.md` to `docs/after.md` | rename/copy inadmissible | `test_rename_evasion_is_blocked` | 0 | rejection exercised |
| NC-GIT-005 | untracked hiding | temporary Git repo | add untracked outside manifest | working paths exceed manifest | `test_untracked_path_cannot_hide_outside_manifest` | 0 | rejection exercised |
| NC-GIT-006 | post-basis executable | temporary Git repo | add `scripts/post_basis.py` after basis | invalid post-basis category | `test_post_basis_executable_change_is_invalidated_even_when_allowlisted` | 0 | rejection exercised |
| NC-TIME-001 | start after completion | evidence fixture | invert run clocks | started-after-completion | `test_started_after_completed_is_blocked` | 0 | rejection exercised |
| NC-TIME-002 | future evidence | evidence fixture | set clock to 2999 | future timestamp | `test_future_clock_is_blocked` | 0 | rejection exercised |
| NC-TIME-003 | run after finalization | evidence fixture | complete run after finalization | post-finalization run | `test_run_after_evidence_finalization_is_blocked` | 0 | rejection exercised |
| NC-TIME-004 | Level B before basis | evidence fixture | start Level B before commit time | basis chronology failure | `test_level_b_before_basis_commit_is_blocked` | 0 | rejection exercised |
| NC-TIME-005 | final report sections omitted | evidence fixture | remove section 16 | report contract failure | `test_report_sections_are_exactly_contractual` | 0 | rejection exercised |
| NC-CI-001 | missing job | workflow fixture | remove independent job | CI identity failure | `test_required_check_is_a_real_job_with_stable_identity` | 0 | rejection exercised |
| NC-CI-002 | check/job divergence | policy fixture | change required check name | CI contract failure | `test_required_job_and_check_names_are_identical` | 0 | rejection exercised |
| NC-HIST-001 | V1 mutation | repository bytes | compare current V1 to d0 | historical mismatch | `test_v1_bytes_are_preserved` | 0 | equal/preserved |
| NC-HIST-002 | V2 mutation | repository bytes | compare current V2 to d0 | historical mismatch | `test_v2_bytes_are_preserved` | 0 | equal/preserved |
| NC-HIST-003 | Macro 06 policy mutation | repository bytes | compare policy to d0 | historical mismatch | `test_macro_06_v2_policy_bytes_are_preserved` | 0 | equal/preserved |
| NC-RED-001 | audited V2 gap | real reproduction commit | run corrected red fixture | V2 must not close | `a4a9fb9` reproduction run | 1 | `5 failed, 1 warning` |
| NC-REMOTE-001 | valid future PROVEN | remote fixture | complete external fields | should be accepted | `test_remote_proven_can_be_valid_when_all_evidence_exists` | 0 | accepted |
| NC-REMOTE-002 | stale ruleset without reason | remote fixture | REVOKED_OR_STALE without reason | stale-state failure | `test_stale_remote_state_requires_reason_and_operator_action` | 0 | rejection exercised |

The matrix is a control inventory, not a claim that local tests prove the
external hosting ruleset.
