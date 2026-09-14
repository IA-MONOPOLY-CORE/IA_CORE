# Roadmap 4.x Macro-Mission 03 - P4 Closure and Next Family Selection

## Result

`ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSED_ROADMAP_RECALIBRATED_NEXT_FAMILY_SELECTED_NOT_STARTED`

Macro 03 closes P4 as the first internally remediated Roadmap 4.x family,
reconciles the route and JSON universes, recalibrates the forecast and selects
P1 as the next family. P1 is not implemented, activated or exposed. Macro 04
is not started.

## Operation and repository state

- Instrumented start: `2026-09-14T09:52:36.1442206-03:00`.
- Instrumented end: `2026-09-14T11:00:56.9769665-03:00`.
- Instrumented duration: `4100.832746 s` (about `1h 08m 20.833s`) through the
  final pre-publication validation boundary.
- Baseline: `2969ed469ed482968b4db4deac7b35a855f635e2`.
- Validation basis: `c26d8faa22b10a03138feade13d2f210c570f02f`.
- Branch: `main`.
- Remote: `origin/main` is verified after normal push/fetch.
- Ahead/behind: `0/0` after publication.
- Working tree: clean after publication.
- `git diff --check`: PASS.

## Station commits

| Station | Purpose | Commit |
| --- | --- | --- |
| 1 | P4 internal closure truth | `b5ba679` |
| 2 | Canonical JSON census reconciliation | `48fcbde` |
| 3 | 36-route matrix | `f47f4bc` |
| 4 | Family scoring, P1 selection and forecast | `abfec2c` |
| 5 | GOKV/DOOL/OCI reconciliation | `9477b9a` |
| 6 | Macro 03 guard and exact historical allowlists | `c26d8fa` |
| 7 | Final checkpoint, evidence, ledger and README | recorded at publication |

All commits are station-local and normal. No reset, rebase, merge, amend,
squash or force-push was used.

## P4 closure and dual gates

P4 contains exactly seven GET routes: the three global catalogs, domain list,
profile catalog, agent presets and preset match. The capabilities remain
`global_catalogs.read`, `tenant_domains.read` and
`tenant_agent_presets.read_sanitized`.

The internal state is `INTERNAL_REMEDIATION_COMPLETE`. Existing Macro 02 and
02.1 guards pass for protection, exact capabilities, fail-closed resolver,
tenant isolation, non-enumeration, recursive sanitization and preserved
payloads. The external state remains `DEFAULT_DENIED`; all nine applicable
gates have `active_now: false` and the action
`REMAIN_DISABLED_OR_CONTAINED`. No production readiness is claimed.

## JSON and route truth

The canonical metric is `TRACKED_JSON_FILES_PARSEABLE` from
`git ls-files -- '*.json'`, parsed as UTF-8 JSON. The final evidence records
the final evidence records `252` tracked JSON files and zero failures. The historical `328` prompt count,
Macro 02's recorded `248`, and Macro 02.1's `268/269` are preserved as
different historical photographs; they are not silently made equivalent.

The route adjudication contains 36 unique route IDs and 36 unique method/path
pairs. P4 accounts for 7 internally treated routes; 29 remain deferred. The
complete matrix is in
`docs/ROADMAP_4X_MACRO_03_36_ROUTE_MATRIX.md`.

## Family decision

P1 `STATUS_OBSERVABILITY_MEMORY` is the only selected next family. It contains
exactly:

- `GET /api/status`
- `GET /api/memory`
- `GET /api/logs`
- `GET /api/metrics/dynamic`

Its score is urgency `5` plus internal readiness `4`, total `9`. It wins on
disclosure-risk reduction, centrality, deterministic internal evidence,
reversibility and lower external dependency than the alternatives. The future
entry contract is `SELECTED_NOT_STARTED`; it does not authorize product edits
in Macro 03.

P2, P3, P5, P6, P7, P8 and P9 remain evaluated and deferred. No automatic
promotion or implementation follows from the scoring table.

## Forecast and consumption

The inherited P4 durations sum to `22402.681469 s`, approximately
`6h 13m 22.681s`. The forecast distinguishes effective Codex hours from
operator calendar and external dependency time. P1 is estimated directionally
at 2-3 missions/8-14 effective hours accelerated, 3-5 missions/14-28 hours
central, or 5-8 missions/28-50 hours conservative. These are not dates,
quota conversions or production promises.

Operator-visible usage remains separate: Macro 02 `80% -> 63%` five-hour and
`47% -> 44%` weekly, shared-window attribution; Macro 02.1 `98% -> 99%` five-hour
and `43% -> 41%` weekly, `RESET_INTERRUPTED`. No token or monetary estimate is
derived.

## Quality and boundaries

GOKV validation: 38 valid items, `NO_NEW_CANDIDATE`, no promotion and no vault
write. The full suite passed `7008 passed, 6 skipped, 6 warnings` in
`1501.67 s` of pytest time (`1505.733 s` instrumented). The focused Macro 03,
historical and P4 guard run passed `50 tests, 6 warnings` in `12.35 s`.
Route census, JSON parse, py_compile, secret policy (`20 passed, 1 warning`),
protected diff and diff-check also passed. Node is
`NOT_APPLICABLE_NO_JAVASCRIPT_MODIFIED`.

The authorized diff is documentary, forecast, README, guard and test-only.
Protected product files remain unchanged: no `api.py`, P4 access module,
other product code, HTML, CSS, contractual JavaScript, i18n, backend payload,
runtime, execution, providers, integrations, stores, secrets, CORS, hosting,
P0, P1, P3 matrix, widgets or Request Draft Panel changes.

`ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSED_ROADMAP_RECALIBRATED_NEXT_FAMILY_SELECTED_NOT_STARTED`
