# UI/UX 1.198 - Microcopy contractual decision package

## 1. Result and scope

`N6_MICROCOPY_DECISION_PACKAGE_CHECKPOINT_PASSED`

`UI_UX_MICROCOPY_CONTRACTUAL_INVENTORY_CLASSIFICATION_DECISION_PACKAGE_PASSED`

This package closes the six-station deterministic block at N6. It does not
change wording, i18n, HTML, CSS, JavaScript, backend, payload, runtime,
execution, endpoints or integrations. It gives Direction a bounded set of
decisions and preserves the exact corpus needed for a future controlled review.

## 2. Initial state and baseline

| Field | Value |
| --- | --- |
| Baseline | `6b9c806` |
| Initial branch | `main` |
| Initial HEAD/origin | equal at `6b9c806` |
| Initial working tree | clean |
| Product payload | `backend_internal_ui_payload.v1` |
| Payload v2 | absent and prohibited |
| Product changes in 1.198 | `0` |
| Active wording changes | `0` |
| Stations | N1-N6 complete; N7 not executed |

## 3. Corpus and evidence

The complete N2 corpus has 1.624 non-deduplicated records:

| Source | Count |
| --- | ---: |
| HTML direct text | 1.032 |
| HTML accessible/title/placeholder/alt attributes | 52 |
| i18n leaves | 217 |
| JS potentially renderable literals | 323 |
| Total | 1.624 |

Inventory digest:
`4e5e84fbfa63aeb257813536febf91b2fc73b99e0384340b4194609ba48201ff`.

Initial corpus signals: 219 state-like records, 27 warnings, 19 errors, 93
fallback/no-payload/not-available records, 1.225 editorial-safe records under
the initial source heuristic, 714 duplicate occurrences and 1.079 records on
or near contract-aware surfaces.

N3 raised the corpus conservatively: 408 `EDITORIAL_SAFE`, 556
`CONTRACTUAL_EXACT`, 93 `CONTRACTUAL_EXPLANATORY`, 138 `BLOCKER`, 58
`READINESS_LABEL`, 31 `NO_PAYLOAD`, 52 `NOT_AVAILABLE`, 96
`AMBIGUOUS_REQUIRES_DIRECTION` and 15 `ACTION_SENSITIVE`. No legacy marker or
unknown surface was invented.

## 4. Contract surface map

Binding distribution:

| Binding | Count |
| --- | ---: |
| `DIRECT_CONTRACT_BINDING` | 831 |
| `INDIRECT_CONTRACT_CONTEXT` | 159 |
| `PRESENTATIONAL_ONLY` | 130 |
| `EDITORIAL_ONLY` | 408 |
| `DIRECTION_REQUIRED_BINDING` | 96 |
| `UNKNOWN_BINDING` | 0 |

Anchors were explicitly mapped for P0, P1/FSC-CO-01, P1/FSC-BF-02,
P1/FSC-VR-03, Request Draft/FSC-RCP-04, P2/P3/Matriz P3, widgets,
`allowed_actions`, `forbidden_actions`, `blocked_capabilities`, source/status,
fallback, `no_payload`, `not_available` and deny-by-default. No item was bound
merely because it was visually near a contract block.

## 5. Browser geometry and consistency

Browser evidence covered 1440x1000, 1280x800, 768x1024, 390x844 and 375x812.
Document `clientWidth == scrollWidth == bodyScrollWidth` at each viewport and
the console had zero warning/error entries in every pass. The audit recorded
local risks only:

- desktop schema/request value boxes showed local `OVERFLOW_RISK` without page
  overflow;
- the long blocked-state explanation wrapped 3-5 lines without clipping;
- the collapsed Request Draft drawer extended beyond the mobile viewport edge
  while the document remained contained;
- no truncation was observed;
- 714 repeated records include 145 duplicate-equivalent and 569
  duplicate-contextual occurrences;
- mixed English/Spanish labels, casing variants and token/sentence variants
  are candidates, not automatic errors.

No visual or wording fix was applied.

## 6. Complete decision matrix

The machine-readable row model is `decision_package_rows()` in the N1 helper.
Every row includes exact current text, `MICROCOPY_ID`, file/location, N3
classification, risk, reason, possible breakage, contract touched, duplicate
tag, visual issue, inconsistency and recommendation.

| Decision category | Count | Recommendation profile | Meaning |
| --- | ---: | --- | --- |
| `SAFE_TO_KEEP` | 30 | `KEEP` | No evidence justifying a change. |
| `EDITORIAL_CANDIDATE` | 295 | `REVIEW` | Possible future editorial/presentational review. |
| `CONSISTENCY_CANDIDATE` | 197 | `REVIEW` | Duplicate/context or casing/nomenclature review; no merge selected. |
| `GEOMETRY_DRIVEN_CANDIDATE` | 15 | `REVIEW` | Local browser geometry/wrapping evidence; CSS/copy decision deferred. |
| `CONTRACT_SENSITIVE_CANDIDATE` | 139 | `DIRECTION_REQUIRED` | Contract-aware, diagnostic or boundary meaning. |
| `ACTION_PERMISSION_SENSITIVE` | 15 | `DIRECTION_REQUIRED` | Action/authority interpretation cannot be inferred. |
| `READINESS_SENSITIVE` | 145 | `DIRECTION_REQUIRED` | Readiness/status/absence must not become permission. |
| `AMBIGUOUS_REQUIRES_DIRECTION` | 96 | `DIRECTION_REQUIRED` | Source evidence cannot select a safe semantic reading. |
| `MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE` | 692 | `CONTRACT_CHANGE_REQUIRED` | Exact vocabulary or direct boundary would drift if edited. |

The category count sums to 1.624. Recommendation totals are `KEEP=30`,
`REVIEW=507`, `DIRECTION_REQUIRED=395` and
`CONTRACT_CHANGE_REQUIRED=692`. No proposed wording is implemented.

## 7. SAFE_TO_KEEP

30 records have no deterministic reason to change and are recommended `KEEP`.
This is not an approval to edit other records; it is evidence that the current
text can remain intact. In addition, every current record remains unchanged in
1.198 regardless of its future category.

## 8. EDITORIAL_CANDIDATE

295 records are possible future editorial/form/navigation/placeholder cleanup
targets. A future batch can operate only on an explicit Direction-approved
allowlist and must preserve visible meaning, i18n source and accessible-name
pairing. No translation or capitalization correction was selected here.

## 9. CONSISTENCY_CANDIDATE

197 records are the deterministic consistency subset selected from repeated
contextual records after higher-risk categories were separated. Review concerns
include `readiness`/`Readiness`, `passed`/`PASSED`, English/Spanish labels and
repeated `no_payload`/`not_available` values. The package does not decide which
variant is canonical.

## 10. GEOMETRY_DRIVEN_CANDIDATE

15 exact source records correspond to the observed schema/request local value
risk, the long blocked explanation or the mobile Request Draft drawer label.
The browser evidence supports a review question, not a copy fix. Direction must
choose whether a future change is scoped CSS, a layout owner correction or a
contract-sensitive wording decision. No third visual piece is proposed.

## 11. CONTRACT_SENSITIVE_CANDIDATE

139 records require contract-owner review because they express blockers,
warnings, errors, fallbacks or explanatory contract context. A safe future
change must keep source/status/fallback, deny-by-default, blocked capabilities
and forbidden actions truthful. There are no wording alternatives here.

## 12. ACTION_PERMISSION_SENSITIVE

15 records contain action-like control vocabulary in a context where the
deterministic corpus cannot prove whether the text is a label, an anti-action
boundary or an authority statement. They require Direction. The agent must not
turn any of them into CTA, submit, dispatch, run, execute or permission.

## 13. READINESS_SENSITIVE

145 records cover readiness, state, `no_payload` and `not_available`. They must
remain visibly documentary: readiness is not permission, validation is not
execution, absence is not availability and `passed` is not operational success.

## 14. AMBIGUOUS_REQUIRES_DIRECTION

96 records remain intentionally unresolved. The package gives no single
replacement because a single replacement would be a semantic decision. For
each such record Direction must decide the intended role and whether the
contract vocabulary itself changes.

## 15. MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE

692 records are exact vocabulary or direct boundary records. Editing them would
require a contract change or an explicitly approved vocabulary version. This
includes blockers, source/status/fallback markers, no-payload/not-available
states and exact contract terms. Current recommendation is
`CONTRACT_CHANGE_REQUIRED`.

## 16. N7 boundary

N7 is the first station where a human-approved decision can modify wording. It
is not executed by this checkpoint.

| Question | Answer |
| --- | --- |
| 1. How many can change without contract alteration? | 484 deterministic editorial/presentational records: `EDITORIAL_SAFE`, navigation, form labels and placeholders. They still need an approved allowlist. |
| 2. How many require Direction? | 1.140 records are marked direction-required by N3 because of contract, readiness, authority, action or accessible-name risk. |
| 3. How many require contract modification? | 692 exact boundary/vocabulary records are `CONTRACT_CHANGE_REQUIRED` in N6; any approved edit to them must version the contract vocabulary. |
| 4. How many should stay? | All 1.624 remain unchanged for 1.198. The explicit immediate `KEEP` subset is 30; exact contract records also remain intact until a contract change. |
| 5. Can N7 split further? | Yes: editorial allowlist, consistency/nomenclature, geometry remediation, then contract-sensitive wording. |
| 6. Is there a deterministic editorial subset? | Yes, 484 records, but only after Direction approves the stable ID allowlist and accessibility/localization constraints. |
| 7. Can Direction approve a package? | Yes. Approve category + explicit `MICROCOPY_ID` allowlists, with contract-sensitive and geometry items separated. Text-by-text approval is unnecessary for deterministic editorial rows. |
| 8. What must Direction decide? | Canonical language/casing, mixed-language policy, duplicate merge policy, action/permission interpretation, readiness vocabulary, geometry remedy owner and whether any contract vocabulary version changes. |
| 9. What need not be decided? | Counts, source locations, digest, browser metrics, protected-file invariants, stable IDs, no-CTA/no-submit boundaries and the fact that 1.198 made no product change. |
| 10. What becomes automatable afterward? | Applying approved editorial IDs, generating before/after snapshots, checking i18n/HTML/ARIA parity, rerunning geometry and rejecting unapproved contract IDs. Contract changes remain owner-gated. |

## 17. What Direction receives

Direction receives a package decision, not an invitation to edit arbitrary text.
The smallest useful approval is:

1. approve or reject the 484-record deterministic editorial allowlist;
2. select the policy for English/Spanish labels and casing variants;
3. decide whether contextual duplicates remain contextual;
4. resolve the 96 ambiguous action/permission records;
5. confirm readiness/no-payload/not-available vocabulary;
6. assign geometry risks to CSS/layout versus wording review;
7. authorize a contract vocabulary version only if exact records must change.

## 18. What Direction does not receive as a decision

Direction does not need to decide inventory mechanics, stable IDs, parsing,
source registration, browser measurements, console capture, protected diff
checks, no-runtime/no-execution boundaries or whether `allowed_actions` is a
button: the evidence and inherited contract already settle those facts.

## 19. Commit and test policy

`COMMIT_SEMANTICS_POLICY_V1` was applied by real diff:

| Station | Commit | Prefix | Real diff |
| --- | --- | --- | --- |
| N1 | `7f83ecf` | `test(ui)` | Test-only registry, helper and negative guards |
| N2 | `5b135b0` | `docs(ui)` | Inventory evidence and focal guard |
| N3 | `023e3d7` | `docs(ui)` | Semantic matrix and focal guard |
| N4 | `a1c3c16` | `docs(ui)` | Surface/contract map and focal guard |
| N5 | `0be382f` | `docs(ui)` | Browser geometry/consistency evidence and focal guard |
| N6 | this checkpoint | `test(ui)` | Decision package, checkpoint, README navigation and exact historical guard adaptations |

No `feat(ui)`, `fix(ui)`, `refactor(ui)` or empty commit was used because no
product behavior changed. `test(ui)` is the honest N6 prefix because the
checkpoint includes a real historical-guard adaptation required to recognize
the exact 1.197 and 1.198 continuity artifacts without weakening product
guards. `TEST_EXECUTION_POLICY_V2` was applied as focal per station, group
after N3/N5, canonical at N6 and deep historical because historical guards
were adapted.

## 20. Final validation contract

N6 requires and records:

- focal N1-N6 tests;
- group tests after N3 and N5;
- canonical UI/UX continuity suite;
- sanity contractual checks;
- `py_compile`;
- Node checks for widgets, console interactions, admin panels and domains;
- `git diff --check`;
- protected product diff empty relative to `6b9c806`.
- sanity contractual payload/contract set: `20 passed`;
- the broader 78-test API/admin/domain probe was `76 passed, 2 failed` on
  pre-existing legacy HTML assumptions; it was not used as a product-change
  gate because HTML is read-only and the canonical contractual sanity set
  passed.

The four product JavaScript files, HTML, CSS, i18n, backend and payload remain
read-only. Deep historical execution was required because historical guards
were adapted. It ran as an explicit, no-glob manifest covering 41 exact
1.174-1.196 historical test paths: 350 tests passed and 0 failed. An earlier
attempt found a 1.174 diff-allowlist false positive; the allowlist was then extended
only with the exact 1.198 test-only/documentation continuity files and the
same manifest was rerun to completion before the N6 commit. The one historical
guard implementation file needed to make that allowlist self-consistent is
also explicit: `tests/test_ui_ux_panel_maestro_widgets_contract_aware_reconstruction_1_174.py`.

## 21. Readiness and next prompt

`ready_for_ui_ux_1_199_microcopy_direction_decision_review`

Exact next prompt:

`PROMPT UI/UX 1.199 — Revisión de Dirección y aprobación controlada del Decision Package de microcopy contractual del Panel Maestro IA_CORE`

UI/UX 1.199 is not executed here. No wording is implemented here.
