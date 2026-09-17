# Roadmap 4.x Macro-Mission 04.6 - P1-D Execution Metrics Baseline

## Forecast

```text
FORECAST_VERSION: PRE_EXECUTION_V1
ESTIMATE_CENTRAL_SECONDS: 5400
ESTIMATE_CENTRAL_HUMAN: 1 h 30 min
EXPECTED_RANGE_SECONDS: 3900-7800
EXPECTED_RANGE_HUMAN: 1 h 05 min - 2 h 10 min
CONTINGENCY_CEILING_SECONDS: 10800
CONTINGENCY_CEILING_HUMAN: 3 h 00 min
```

The forecast was recorded before code modification. It assumes a clean exact
baseline, no UI work, no external dependency, one endpoint, reusable P1
patterns, a green historical gate before Level B, and no new Method Santi
version.

## Required final measurements

The final metric must record the three clocks separately:

```text
FUNCTIONAL_PUBLICATION_TIME
DOCUMENTARY_CLOSURE_TIME
OPERATOR_VISIBLE_COMPLETION_TIME
```

It must include every Level B attempt, start/end timestamps, wall time,
process time when available, counters, warnings, skips, exit code, cause,
repair, validation cost, timing percentage, forecast comparison, interruption
count, payload byte measurement, quota evidence, GOKV/DOOL/OCI reconciliation,
Git publication, and explicit `UNKNOWN` values.

## Quota evidence policy

```text
PRE_MISSION_WEEKLY_RESET_OBSERVED_BY_OPERATOR: NO_RESET_REPORTED_BEFORE_MISSION
START_5H_QUOTA_REMAINING: UNKNOWN
END_5H_QUOTA_REMAINING: UNKNOWN
START_WEEKLY_QUOTA_REMAINING: UNKNOWN
END_WEEKLY_QUOTA_REMAINING: UNKNOWN
RESET_OCCURRED_DURING_MISSION: UNKNOWN
QUOTA_DELTA_5H: UNKNOWN
QUOTA_DELTA_WEEKLY: UNKNOWN
MEASUREMENT_SOURCE: EXTERNAL_OPERATOR_STATEMENT_AND_LOCAL_REPOSITORY
MEASUREMENT_QUALITY: PARTIAL
```

No quota value is inferred as a percentage, token amount, monetary amount, or
reset timestamp.

## Validation basis rule

`VALIDATION_BASIS` may be created only after P1-D focal tests, affected
historical tests, P1 family preservation tests, static checks, and the
protected-diff check are green.

## Validation basis evidence

```text
VALIDATION_BASIS_STATUS: FOCAL_GREEN_HISTORICAL_COHORT_GREEN_LEVEL_A_GREEN
FOCAL_FINAL: 37 passed, 0 failed, 5 warnings
LEVEL_A_STARTED_AT: 2026-09-16T21:47:04.0469924-03:00
LEVEL_A_COMPLETED_AT: 2026-09-16T21:48:03.7965589-03:00
LEVEL_A_WALL_SECONDS: 59.7495665
LEVEL_A: 167 passed, 0 failed, 5 warnings
HISTORICAL_GATE_STARTED_AT: 2026-09-16T21:48:19.1410853-03:00
HISTORICAL_GATE_COMPLETED_AT: 2026-09-16T21:49:20.2817870-03:00
HISTORICAL_GATE_WALL_SECONDS: 61.1407017
HISTORICAL_GATE: 191 passed, 0 failed, 5 warnings
PY_COMPILE: PASS
NODE_CHECK: PASS
JSON_PARSE: PASS - 268 files including two P1-D evidence files
SYNTHETIC_PAYLOAD_BYTES: 413
GIT_DIFF_CHECK: PASS
PROTECTED_DIFF: EMPTY
```

The first Level A attempt had three historical bookkeeping failures because
the current P1-D modules appeared in prior allowlists. The nominal adapter
repair was applied, and the complete Level A cohort was rerun successfully.
No production regression, assertion removal, broad glob, or protected-surface
change was introduced.
