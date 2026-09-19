# Roadmap 4.x Macro-Mission 06 - Execution Metrics

```text
FORECAST_VERSION: PRE_EXECUTION_V1
FORECAST_CENTRAL_SECONDS: 5400
FORECAST_RANGE_SECONDS: 3600-9000
CONTINGENCY_CEILING_SECONDS: 12600
```

The forecast covers policy-driven gate design, the repository adjudication and
one full suite. Process CPU time is recorded as `UNKNOWN` when the PowerShell
wrapper does not expose it; wall time remains measured. Usage percentages are
not inferred from wall time or tokens.

The canonical evidence records every validation attempt, repair, invalidation,
retry, interruption and rollback. The final report computes total operation
time from the first accepted mission anchor through the postpublish fetch.
