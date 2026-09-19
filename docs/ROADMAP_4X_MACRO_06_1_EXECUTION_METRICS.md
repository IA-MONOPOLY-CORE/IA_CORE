# Macro 06.1 Execution Metrics

## Forecast

```text
FORECAST_VERSION: PRE_EXECUTION_V1
FORECAST_CENTRAL_SECONDS: 5400
FORECAST_RANGE_SECONDS: 3600-9000
CONTINGENCY_CEILING_SECONDS: 12600
```

The forecast was carried forward from the predecessor closure method and was
not treated as a result. The measured Level A wall time was `1772.130471 s`
and the measured final Level B wall time was `65.479582 s`.

## Measured validation metrics

| gate | passed | failed | skipped | warnings | wall_seconds | process_seconds |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| focal | 27 | 0 | 0 | 1 | 21.182239 | UNKNOWN |
| historical-impact | 104 | 0 | 0 | 5 | 84.133069 | UNKNOWN |
| level-a | 7266 | 0 | 6 | 6 | 1772.130471 | UNKNOWN |
| level-b | 122 | 0 | 0 | 5 | 65.479582 | UNKNOWN |

## Evidence station metrics

```text
CANONICAL_EVIDENCE_SHA256: 310a1022042c080f58213cf35e3339d7259ded9183bb9dce220d150e0122c07f
POST_EVIDENCE_RECEIPT_SHA256: 8fcae0d9c980c1743f4a3a4a0d5e7fe8c47961b93933cfb2d30375f5e55403cd
PRELOCK_RECEIPT_SHA256: RECORDED_IN_MACHINE_RECEIPT_AND_RENDERED_REPORT
CANONICAL_FINALIZED_AT: 2026-09-19T15:57:46.439320-03:00
POST_EVIDENCE_COMPLETED_AT: 2026-09-19T15:57:59.270332-03:00
PRELOCK_COMPLETED_AT: RECORDED_IN_MACHINE_RECEIPT_AND_RENDERED_REPORT
```

The Level A console summary reports `1767.19 s`; the wrapper wall clock is
authoritative for the receipt and includes process startup/teardown. No usage,
token or cost value is inferred.

## Warnings

Warnings were deprecation warnings from FastAPI/Starlette and the local
OpenTelemetry dependency. They did not alter exit status or closure decision.
