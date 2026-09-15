# Roadmap 4.x Macro-Mission 04.5 - Historical Impact Manifest

## Purpose

This manifest was frozen before Level B. It separates current P1-C contract
tests from historical tests that must continue validating their own published
checkpoint. It does not change an historical assertion or make a current
working tree a substitute for an historical snapshot.

## Changed-surface manifest

```text
api.py
core/protected_logs_access.py
core/protected_logs_schema.py
ui/web/admin-panels.js
ui/web/README.md
tests/test_api_admin_panels.py
tests/test_protected_logs_p1_c.py
tests/test_roadmap_4x_macro_04_5_p1_c.py
tests/test_method_santi_3_2_3.py
tests/historical_test_context.py
docs/FUTURE_PLATFORM_EXTENSION_INDEX.md
docs/METHOD_SANTI_3_2_3_VERIFIED_ADAPTIVE_EXECUTION_FEEDBACK_ENGINEERING.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_TRUTH_MATRIX.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_PROTECTED_LOGS_EVENTS_CONTRACT.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_RETENTION_OWNERSHIP_AND_SUPPORT_FUTURE_CONTRACT.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_EXECUTION_JOURNAL.md
docs/ROADMAP_4X_MACRO_04_5_HISTORICAL_IMPACT_MANIFEST.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_EXECUTION_METRICS_BASELINE.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_CHECKPOINT.md
docs/ROADMAP_4X_MACRO_04_5_P1_C_CHECKPOINT_EVIDENCE.json
docs/ROADMAP_4X_MACRO_04_5_P1_C_COMMIT_ACCOUNTABILITY_LEDGER.md
knowledge/global_operational/metrics/roadmap_4_x_macro_04_5_execution_metric.json
```

The checkpoint/evidence/metric paths were reserved in this frozen manifest and
are created only after the implementation and validation gates.

## Historical guard cohort

The following directly governs the roadmap boundary and was required to pass:

```text
tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py
tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py
tests/test_roadmap_4x_macro_04_3_p1_a.py
tests/test_roadmap_4x_macro_04_4_p1_b.py
tests/test_roadmap_4x_macro_04_p1_entry_review.py
```

The historical adapter is also exercised by every ledgered historical module
that reads snapshot prefixes (`api.py`, `ui/web/`, `docs/`,
`knowledge/global_operational/`, and fixtures), every module listed in
`tests/historical_test_context.py` under `_OVERRIDES` or
`_SECONDARY_HISTORICAL_FILES`, and the current continuity modules that inspect
the UI shell. This is the complete adapter-defined historical cohort, not a
glob-based exemption.

## Direct current consumers and UI guards

```text
tests/test_api_admin_panels.py
tests/test_catalogs.py
tests/test_method_santi_3_2.py
tests/test_method_santi_3_2_1.py
tests/test_method_santi_3_2_2_and_one_core_four_surfaces.py
tests/test_method_santi_3_2_3.py
tests/test_protected_logs_p1_c.py
tests/test_roadmap_4x_macro_04_5_p1_c.py
```

UI/UX historical modules that read `ui/web/admin-panels.js` remain snapshot
bound through the adapter. They are not reinterpreted as P1-C current tests.
No unrelated UI file is included in the implementation allowlist.

## Gate commands and evidence

The pre-Level-B gate executes the direct current consumers, the Macro 04.1,
04.2, 04.3, 04.4 and entry guards, and the complete adapter-defined historical
cohort. The validation basis is not frozen until all of these are green.

```text
HISTORICAL_IMPACT_GATE: PASS
HISTORICAL_IMPACT_GATE_COMPLETED_AT: UNKNOWN - the terminal capture did not emit an end timestamp
HISTORICAL_IMPACT_GATE_RESULT: 158 passed, 0 failed, 5 warnings
UNEXPECTED_HISTORICAL_FAILURE: NONE
ASSERTIONS_REMOVED: NO
BROAD_GLOBS_ADDED: NO
WORKING_TREE_SUBSTITUTION_FOR_HISTORY: NO
```

The command was:

```text
python -m pytest -q tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py tests/test_roadmap_4x_macro_04_3_p1_a.py tests/test_roadmap_4x_macro_04_4_p1_b.py tests/test_roadmap_4x_macro_04_p1_entry_review.py tests/test_api_admin_panels.py tests/test_catalogs.py tests/test_method_santi_3_2.py tests/test_method_santi_3_2_1.py tests/test_method_santi_3_2_2_and_one_core_four_surfaces.py tests/test_method_santi_3_2_3.py tests/test_protected_logs_p1_c.py tests/test_roadmap_4x_macro_04_5_p1_c.py
```

Two historical bookkeeping defects were found and resolved without changing
their assertions: P1-A/P1-B JSON census commands now use each checkpoint's
tree, and the P1-B guard is mapped to its published functional checkpoint.

If a historical guard fails, the failure must be classified as bookkeeping or
productive regression, and any checkpoint mapping repair must be nominal and
separately accountable.
