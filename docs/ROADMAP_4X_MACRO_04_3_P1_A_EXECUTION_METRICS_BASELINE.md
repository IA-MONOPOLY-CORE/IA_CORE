# Roadmap 4.x Macro-Mission 04.3

## P1-A execution metrics

The canonical machine-readable record is
`knowledge/global_operational/metrics/roadmap_4_x_macro_04_3_execution_metric.json`.
This document explains the measurement boundaries and does not create a
second telemetry source.

### Architectural estimate

| Estimate | Value |
|---|---|
| `ESTIMATED_FAST_DURATION` | `1 h 50 min` |
| `ESTIMATED_EXPECTED_MIN_DURATION` | `2 h 20 min` |
| `ESTIMATED_EXPECTED_MAX_DURATION` | `3 h 15 min` |
| `ESTIMATED_CENTRAL_DURATION` | `2 h 40 min` |
| `ESTIMATED_CONTINGENCY_CEILING` | `4 h 15 min` |

The estimate is planning input, not a runtime gate. Wall-clock and process
durations are recorded only when both endpoints are observable. The execution
started at `2026-09-15T01:27:14.4966151-03:00`. The preflight completion marker
was recorded immediately after the clean baseline verification; the first
implementation artifact was created at `2026-09-15T01:34:35-03:00`.

### Cost comparison

The legacy handler statically performed domain-state reads, provider listing
and per-provider health/model probes, Hybrid snapshot work, memory reads,
agent/tool inventory reads and runtime metric reads on every status request.
The remediated minimal handler performs one bounded local Supervisor lifecycle
read and response validation. The detailed handler performs the same local
read plus fixed in-process projection and validation. Neither view performs
provider, model, network, domain, memory, tool, runtime-metric or mutation
work. This is a structural cost improvement; no fragile latency percentage is
claimed.

### Required evidence

The controlled measurements record payload sizes, repeated/concurrent read
behavior, forbidden-call counters, state mutation checks and all full-suite
attempts. UI visual validation is `TOOLING_UNAVAILABLE` in this context; Node
syntax checking and API/static consumer tests are the fallback. Quota values
after start are not observable from the repository and are therefore
`END_QUOTA_EXTERNAL_OPERATOR_EVIDENCE_REQUIRED`.

### Observed execution

The execution started at `2026-09-15T01:27:14.4966151-03:00`. Level B became
green at `2026-09-15T04:35:29.4763730-03:00`, for an observed
`11294.979758 s` (`3 h 8 min 14.979758 s`) from start to Level B completion.
The central estimate was `9600 s`; observed error was `+1694.979758 s`.

The exact canonical command was `python -m pytest -q`, run single-process with
Python `3.11.9`, pytest `9.0.3`, no xdist, and `.pytest_cache`. Four attempts
were recorded: attempt 1 was interrupted after partial output when the host
closed stdout; attempt 2 returned `7054 passed, 9 failed, 6 skipped, 6
warnings` in `1536.861839 s` wall / `1536.856369 s` process; attempt 3 returned
`7060 passed, 3 failed, 6 skipped, 6 warnings` in `1525.397725 s` wall /
`1525.393179 s` process; attempt 4 returned `7063 passed, 6 skipped, 6
warnings` in `1534.532847 s` wall / `1534.528251 s` process with exit `0`.

The speed variation is observed rather than attributed to a single cause: the
suite is serial and includes slow integration/guard sections, while the first
attempt has no observable end marker. No worker parallelism or reduced command
was used.
