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
