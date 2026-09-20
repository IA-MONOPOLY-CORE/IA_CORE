# Roadmap 4.x Macro-Mission 06.2 Execution Metrics

| Metric | Value |
| --- | --- |
| Focal passed | `16` |
| Historical passed | `109` |
| Terminal Level B passed | `123` |
| Terminal Level B failed | `0` |
| Terminal Level B warnings | `5` |
| Focal wall seconds | `27.895778` |
| Historical wall seconds | `80.947189` |
| Level A wall seconds | `0.688879` |
| Terminal Level B wall seconds | `81.039892` |
| CPU time | `UNKNOWN` |
| Successful terminal Level B count for final basis | `1` |
| Ordinary validation after terminal | `0` |
| P3 implementation | `NOT_STARTED` |
| VERO runtime | `NOT_IMPLEMENTED` |
| FIRE runtime | `NOT_IMPLEMENTED` |

Warnings are inherited deprecations from the pre-existing FastAPI and
OpenTelemetry test environment; none is a test failure.

The first two terminal attempts were invalidated during post-terminal
reconciliation: the first required an exact allowlist repair, and the second
required explicit renderer enforcement for every durable validation receipt.
The final basis `8bf79015deee831752f5553a083d44c9d07afbc4` has exactly one
successful terminal Level B.
