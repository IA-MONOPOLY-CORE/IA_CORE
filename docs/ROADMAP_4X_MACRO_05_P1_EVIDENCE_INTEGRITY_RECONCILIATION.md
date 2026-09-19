# Roadmap 4.x Macro-Mission 05 - Evidence Integrity Reconciliation

## Initial strict scan

```text
TRACKED_JSON_BEFORE: 268
STRICT_DUPLICATE_SCAN: 2 FAILURES
CONFLICTING_VALUES: NONE
```

The two failing files are exactly:

- `docs/ROADMAP_4X_MACRO_04_6_P1_D_CHECKPOINT_EVIDENCE.json`
- `knowledge/global_operational/metrics/roadmap_4_x_macro_04_6_execution_metric.json`

Both files contained repeated publication fields with identical values. The
duplicate field set was:

```text
evidence_sync_commit
evidence_sync_push_started_at
evidence_sync_push_completed_at
evidence_sync_push_wall_seconds
evidence_sync_push_exit_code
final_fetch_completed_at
final_head_before_documentary_lock
```

The authorized normalization removes only redundant second occurrences from
those two historical files. The values retained are byte-for-byte identical
to their duplicate counterparts; no timestamp, hash, result or state is
selected or rewritten.

## Clock reconciliation

Macro 04.6 historically used `documentary_closure_time` for content
completion even though that timestamp preceded functional publication. Macro
05 preserves the historical value and treats it as content-finalized evidence,
not as documentary lock completion.

Macro 05 uses four unambiguous anchors:

```text
FUNCTIONAL_PUBLICATION_FETCH_VERIFIED_TIME
DOCUMENTARY_CONTENT_FINALIZED_TIME
DOCUMENTARY_LOCK_FETCH_VERIFIED_TIME
OPERATOR_VISIBLE_COMPLETION_TIME
```

The documentary lock is the published and fetched state of checkpoint,
evidence, metric, ledger and final documentation. Operator-visible completion
is `UNKNOWN_EXTERNAL_OPERATOR_EVIDENCE_REQUIRED` unless the operator supplies
an external timestamp.

## Fixed point

Evidence may report the baseline, validation basis, functional publication head
and documentary-lock parent. It must not chase the hash of the commit that
contains its own final content. The live HEAD and `origin/main` are reported
externally after fetch verification. No self-referential commit chain is
authorized.
