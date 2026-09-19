# Roadmap 4.x Macro 05.1 Execution Metrics Baseline

```text
FORECAST_VERSION: PRE_EXECUTION_V1
ESTIMATE_CENTRAL_SECONDS: 7200
EXPECTED_RANGE_SECONDS: 5400-10800
CONTINGENCY_CEILING_SECONDS: 14400
```

The forecast assumes no product repair, a 28-30 minute full suite, a reusable
gate with negative controls, and an acotada historical reconciliation. The final
canonical evidence records every measured station, retry, interruption, rollback,
Level B share, and variance. Process CPU time is `UNKNOWN` only when the wrapper
does not expose it, with a cause recorded beside the run.

Quota evidence for Macro 05 is copied exactly from explicit operator evidence with
`EXPLICIT_OPERATOR_EVIDENCE` provenance and `UI_ROUNDED_PERCENTAGES` precision.
No token, seconds, or monetary inference is made.

The prior `1737.4484887` second Level B run is retained as an invalidated attempt
because the final documentary anchor exposed stale fixture chronology afterward.
The definitive Level B measurement on
`a17c37b1a69c67e65ca40e523aa0d1fc224b85e0` is `1787.9722017` seconds, against
the central forecast of `7200` seconds. It completed with `7230 passed, 6 skipped,
6 warnings`, exit `0`.
