# Roadmap 4.x Macro-Mission 04.2

## Execution estimation and measurement baseline

The canonical machine-readable record is
`knowledge/global_operational/metrics/roadmap_4_x_macro_04_2_execution_metric.json`.
This document is a human-readable companion; it is not a second telemetry
source.

### Prior architectural estimate

| Estimate | Value |
| --- | --- |
| `ESTIMATED_FAST_DURATION` | `1 h 50 min` |
| `ESTIMATED_EXPECTED_MIN_DURATION` | `2 h 05 min` |
| `ESTIMATED_EXPECTED_MAX_DURATION` | `2 h 40 min` |
| `ESTIMATED_CENTRAL_DURATION` | `2 h 20 min` |
| `ESTIMATED_CONTINGENCY_CEILING` | `3 h 20 min` |

The estimate was architectural planning input, not measured runtime. The
execution record uses process timestamps and explicitly marks unavailable
markers as `UNKNOWN` or `UNAVAILABLE`; no quota or UI value is inferred.

### Measurement rules

`ESTIMATION_ERROR_IS_OPERATIONAL_LEARNING` and
`PROCESS_IMPROVEMENT_MUST_BE_MEASURED` apply to this mission. The stages are
preflight, implementation, focused validation, full suite, publication and
remote verification. A duration is measured only when both endpoints are
observable. Causes are classified as `OBSERVED`, `INFERRED`, `UNKNOWN` or
`EXTERNAL_EVIDENCE_REQUIRED`.

### Current measurement state

The validation basis is
`7f18aa14d2245f4d26aa86963f946e7a0e2b73b7`. Focused validation recorded
`25.607366 s` for `251 passed, 1 warning`; the historical allowlist repair
recorded `28 passed, 1 warning`. The final full-suite process interval was
`1564.8418513 s` (`1560.41 s` reported by pytest) with `7048 passed, 6
skipped, 6 warnings`. The complete wall-clock interval and publication state
are reported after fetch because those markers are not known before the final
push. Missing quota and UI endpoints remain `UNKNOWN`; no manual approximation
is used.
