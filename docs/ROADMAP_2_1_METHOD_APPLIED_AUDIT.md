# Roadmap 2.1 - Method Applied Audit

## Gate

ROADMAP_2_1_METHOD_APPLIED_AUDIT_PASSED

## Scope

This inventory describes the method actually applied by the recent UI/UX 1.203,
UI/UX 1.204 and Roadmap 2.0 work. It does not rewrite the global method book.
Historical prompts remain historical evidence; the current repository, current
contract and Git state have precedence.

## Method inventory

| rule_id | rule | classification | source | evidence | current status | mandatory future | gokv relation | update needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| METHOD-001 | Exact preflight of branch, HEAD, origin, ahead/behind and clean tree | ACTIVE_CANONICAL | Roadmap 2.x prompt section 10 | N0 commands and test | Applied and green | Every major mission | evidence_before_closure | No |
| METHOD-002 | Product read-only boundary is explicit before work | ACTIVE_CANONICAL | 1.204 prompt sections 8-10 | Protected diff and N0/N2 | Applied | Every read-only mission | preserve_contract_until_explicit_change | No |
| METHOD-003 | Major stations run sequentially with work, evidence, tests, gate and local commit | ACTIVE_CANONICAL | Roadmap 2.x prompt section 11 | N0 completed; N1-N3 planned | Active | Preserve station boundaries | station_local_commits | No |
| METHOD-004 | Evidence must precede closure claims | ACTIVE_CANONICAL | GOKV item and UI/UX 1.204 N4/N6 | Focal/group/canonical/deep results | Active | No PASS by intention or name | evidence_before_closure | No |
| METHOD-005 | Test depth scales focal -> group -> canonical -> deep historical | ACTIVE_CANONICAL | GOKV item and 1.204 N4 | 1.204 regression matrix | Active | Classify historical and external failures | focal_group_canonical_deep_test_policy | No |
| METHOD-006 | Historical guards validate their own horizon | ACTIVE_EVOLVED | UI/UX 1.192 authorization and 1.204 N4 | 8 historical failures classified | Active with explicit temporal boundary | Preserve assertions; no global relaxation | focal_group_canonical_deep_test_policy | Documented in N4 |
| METHOD-007 | Local recovery reverts only the invalid station | ACTIVE_CANONICAL | Roadmap 2.x section 17 | Prompt rule; no rollback required in N0 | Active | No global reset or destructive checkout | station_local_commits | No |
| METHOD-008 | Reset, rebase, squash, amend and force are prohibited | ACTIVE_CANONICAL | Roadmap 2.x sections 16-17 | Git history and clean push | Active | Preserve traceability | real_diff_over_planned_commit_name | No |
| METHOD-009 | Commit semantics follow the real diff | ACTIVE_CANONICAL | GOKV item and prompt section 16 | `docs(core)`, `test(core)`, `docs(knowledge)` | Active | No feature/fix labels for documentation work | real_diff_over_planned_commit_name | No |
| METHOD-010 | A true hard frontier stops autonomous continuation | ACTIVE_CANONICAL | GOKV item and UI/UX 1.204 handoff | UI semantic boundary preserved | Active | Require Direction for contract/runtime change | true_hard_frontier | No |
| METHOD-011 | Conditioned autonomy executes only scoped, reversible, preauthorized work | ACTIVE_EVOLVED | GOKV item and 1.204 evidence | 0 interventions; no product changes | Validated, not promoted | Keep STOP boundaries explicit | conditioned_autonomy | No |
| METHOD-012 | PROMOTED_ONLY is the first OCI mode | ACTIVE_EVOLVED | 1.204 handoff and Roadmap 2.x section 6 | 7 promoted selected; validated/candidate 0 | Applied | Use DEVELOPMENT_VALIDATED only with evidence of insufficiency | GOKV OCI | No |
| METHOD-013 | OCI compiler selects knowledge deterministically | ACTIVE_CANONICAL | `gokv/compiler.py` and pack records | Compiled 1.204 pack; no hardcoded selection in current pack | Active | Record pack id, size and selection state | GOKV OCI | No |
| METHOD-014 | Development-Origin learning loop is execute, validate, capture, distill, assess, store, compile next | ACTIVE_CANONICAL | GOKV DOOL docs and loop schema | 1.204 post-block loop | Active | `NO_LEARNING_FOUND` remains valid | DOOL/GOKV | No |
| METHOD-015 | No automatic promotion or candidate invention | ACTIVE_CANONICAL | GOKV promotion governance | 23-item registry; 0 new candidates | Active | Direction required for promotion | promotion governance | No |
| METHOD-016 | Operator-reported telemetry is append-only and not reconstructed | ACTIVE_EVOLVED | GOKV supplement schema and 1.204 prompt | 1.204 supplement records RESET_INTERRUPTED note | Active with schema limitation documented | Preserve measurement quality explicitly | GOKV capture | Note schema sentinel limitation |
| METHOD-017 | Current contract wins over conflicting historical knowledge | ACTIVE_CANONICAL | OCI authority precedence | Current baseline preserved | Active | Exclude conflicting knowledge and record event | CURRENT_CONTRACT_WINS | No |
| METHOD-018 | Compress repeated observations into decisions only when contract-compatible | ACTIVE_CANONICAL | GOKV promoted item | N0 mismatch table and method audit | Active | Do not group by textual similarity alone | compress_occurrences_into_decisions | No |
| METHOD-019 | `REPORT_FINAL_AUTOCONTENIDO_PARA_CONTINUIDAD`: report must be self-contained enough to write the next prompt | ACTIVE_CANONICAL | UI/UX 1.204 report requirement and Roadmap 2.x section 21 | 1.204 report and this audit | Newly institutionalized | Include all continuity-critical fields | evidence_before_closure | No |
| METHOD-020 | Push only after gates, then fetch and verify exact alignment | ACTIVE_CANONICAL | Roadmap 2.x section 20 | 1.204 push: HEAD equals origin, 0/0 | Active | Final checkpoint must publish | station_local_commits | No |
| METHOD-021 | Development-Origin learning is not field-operation learning | ACTIVE_CANONICAL | GOKV architecture and registry | Runtime/execution remain disabled | Active | Never infer runtime learning | GOKV DOOL | No |
| METHOD-022 | Historical documentation may be true historically but not current | ACTIVE_EVOLVED | Roadmap 2.x section 8 and N0 | README and roadmap drift table | Active | Mark historical cursor and current authority | evidence_before_closure | README sync at N3 |

## Classification totals

- `ACTIVE_CANONICAL`: 17
- `ACTIVE_EVOLVED`: 5
- `LEGACY`: 0 rules used as current authority
- `SUPERSEDED`: 0
- `EXPERIMENTAL`: 0
- `FUTURE`: 0 current method rules; future architecture remains separate
- `METHOD_RULES_INVENTORIED`: 22

## Drift and evolution

The method has evolved in application, not by silently rewriting its global
definition. Recent evolution is the explicit temporal treatment of historical
guards, the promoted-only-first OCI selection, the append-only operator metric
quality note, and the mandatory self-contained continuity report. These are
documented as active/evolved rules and do not authorize product or runtime work.

## Gate conclusion

ROADMAP_2_1_METHOD_APPLIED_AUDIT_PASSED
