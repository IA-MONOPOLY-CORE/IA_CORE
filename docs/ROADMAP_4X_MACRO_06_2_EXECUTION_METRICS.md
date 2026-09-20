# Roadmap 4.x Macro-Mission 06.2 Execution Metrics

| Metric | Value |
| --- | --- |
| Focal passed | `16` |
| Historical passed | `109` |
| Terminal Level B passed | `123` |
| Terminal Level B failed | `0` |
| Terminal Level B warnings | `5` |
| Focal wall seconds | `41.427753` |
| Historical wall seconds | `92.610074` |
| Level A wall seconds | `0.433272` |
| Terminal Level B wall seconds | `64.131317` |
| CPU time | `UNKNOWN` |
| Successful terminal Level B count for final basis | `1` |
| Ordinary validation after terminal | `0` |
| P3 implementation | `NOT_STARTED` |
| VERO runtime | `NOT_IMPLEMENTED` |
| FIRE runtime | `NOT_IMPLEMENTED` |

Warnings are inherited deprecations from the pre-existing FastAPI and
OpenTelemetry test environment; none is a test failure.

The first three closure attempts were invalidated during post-terminal
reconciliation: the first required an exact allowlist repair, the second
required explicit renderer enforcement for every durable validation receipt,
and the third required the renderer to distinguish committed documentary
delta from mutable Git surfaces. The final basis
`77ac332968ee0b908fcdc1e880b317e9505180ce` has exactly one successful
terminal Level B.
