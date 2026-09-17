# Roadmap 4.x Macro-Mission 04.6 - Historical Impact Manifest

## Purpose

This manifest freezes the P1-D change surface before Level B. Historical tests
must validate their own published checkpoint; current P1-D tests validate the
current repository. No historical assertion may be removed or evaluated against
the current working tree.

## Changed-surface allowlist

```text
api.py
core/protected_dynamic_metrics_access.py
core/protected_dynamic_metrics_schema.py
tests/test_protected_dynamic_metrics_p1_d.py
tests/test_roadmap_4x_macro_04_6_p1_d.py
tests/historical_test_context.py
docs/ROADMAP_4X_MACRO_04_6_P1_D_TRUTH_MATRIX.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_PROTECTED_DYNAMIC_METRICS_CONTRACT.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_DOMAIN_NEUTRALITY_AND_TENANT_SCOPE_FUTURE_CONTRACT.md
docs/ROADMAP_4X_MACRO_04_6_HISTORICAL_IMPACT_MANIFEST.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_EXECUTION_JOURNAL.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_EXECUTION_METRICS_BASELINE.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT.md
docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json
docs/ROADMAP_4X_MACRO_04_6_P1_D_COMMIT_ACCOUNTABILITY_LEDGER.md
knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json
```

## Historical cohort

```text
tests/test_roadmap_4x_macro_04_1_cognitive_kernel.py
tests/test_roadmap_4x_macro_04_2_cognitive_kernel.py
tests/test_roadmap_4x_macro_04_3_p1_a.py
tests/test_roadmap_4x_macro_04_4_p1_b.py
tests/test_roadmap_4x_macro_04_p1_entry_review.py
tests/test_roadmap_4x_macro_04_5_p1_c.py
tests/test_platform_status_p1_a.py
tests/test_protected_memory_p1_b.py
tests/test_protected_logs_p1_c.py
tests/test_method_santi_3_2.py
tests/test_method_santi_3_2_1.py
tests/test_method_santi_3_2_2_and_one_core_four_surfaces.py
```

The adapter uses nominal checkpoint mappings only. P1-C is mapped to its
published head `e9089eb1ad04ca0bca0d6b9806bca151c487e74e`; P1-D remains live.
P1-A, P1-B, and older historical routes keep their existing mappings.

## Protected paths

```text
ui/web/index.html
ui/web/styles.css
ui/web/admin-panels.js
ui/web/i18n_es.json
core/platform_status_access.py
core/platform_status_schema.py
core/protected_memory_access.py
core/protected_memory_schema.py
core/protected_logs_access.py
core/protected_logs_schema.py
domains/
providers/
integrations/
stores/
runtime/
execution/
payload/
secrets/
```

## Gate status

```text
HISTORICAL_IMPACT_GATE: PASS
HISTORICAL_GATE_STARTED_AT: 2026-09-16T21:48:19.1410853-03:00
HISTORICAL_GATE_COMPLETED_AT: 2026-09-16T21:49:20.2817870-03:00
HISTORICAL_GATE_RESULT: 191 passed, 0 failed, 5 warnings
ASSERTIONS_REMOVED: NO
BROAD_GLOBS_ADDED: NO
WORKING_TREE_SUBSTITUTION_FOR_HISTORY: NO
UNCLASSIFIED_HISTORICAL_FAILURES: 0
```

The initial Level A run exposed three bookkeeping-only allowlist failures in
04.3, 04.4, and 04.5 because current P1-D modules were untracked while the
cohort was running. The adapter added only nominal P1-D module entries to its
documentary filter and preserved every historical assertion. The rerun was
green; no productive regression was found.
