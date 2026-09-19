# Roadmap 4.x Macro-Mission 05 - P1 Execution Journal

## Mission start

```text
MISSION_ACCEPTED_AT: 2026-09-19T06:30:55.6332332-03:00
PREFLIGHT_COMPLETED_AT: 2026-09-19T06:30:56.9336245-03:00
BASELINE: 9148f023f4df8e642f396f08a6386f8967d70efb
BRANCH: main
ORIGIN_MAIN: 9148f023f4df8e642f396f08a6386f8967d70efb
AHEAD_BEHIND: 0/0
WORKTREE: CLEAN
QUOTA: UNKNOWN_EXTERNAL_OPERATOR_EVIDENCE_REQUIRED
```

## Stations

1. Truth freeze and cross-boundary contract.
2. Adversarial E2E suite for four P1 routes.
3. Strict JSON and evidence clock reconciliation.
4. Method Santi 3.2.4 documentation and guard.
5. Historical Impact Gate.
6. Level A and Level B validation.
7. Internal family closure, publication and fixed-point evidence.

No product file is modified before a reproducible red E2E case. No Macro 06
work begins in this mission.

## Focal validation attempts

The first focal attempt used the exact new E2E, closure and Method 3.2.4
tests. It produced 56 passed, 6 failed and 5 warnings. The failures were
classified as harness/documentation defects: the synthetic memory fixture
omitted its required `running` attribute; the log canary did not use the
sanitizer's explicit labeled forms; the route-matrix assertion selected the
wrong column and initially counted only identifiers beginning with `api_`;
the duplicate-key scan exposed all seven repeated fields in each of the two
historical JSON files; and the historical Method 3.2.3 read used the shell's
default encoding instead of UTF-8. No product file was changed.

The second focal attempt produced 60 passed, 2 failed and 5 warnings. The
remaining failures were the route-matrix Path-column index and an assertion
that treated the safe `[REDACTED_PATH]` marker as an exposed path. No product
file was changed.

The third focal attempt passed with:

```text
62 passed, 0 failed, 5 warnings
py_compile: PASS
exit_code: 0
started_at: 2026-09-19T06:47:01.8525342-03:00
completed_at: 2026-09-19T06:47:17.2200159-03:00
wall_seconds: 15.368
```

The first two wrapper timestamps were not emitted by the interrupted command
wrappers and remain `UNKNOWN_COMMAND_WRAPPER_TIMING`; their result counts and
failure classifications are preserved above rather than inferred.

## Validation basis

```text
FOCAL_FINAL: 62 passed, 0 failed, 5 warnings
FOCAL_STARTED_AT: 2026-09-19T06:47:01.8525342-03:00
FOCAL_COMPLETED_AT: 2026-09-19T06:47:17.2200159-03:00
FOCAL_WALL_SECONDS: 15.368
HISTORICAL_IMPACT_GATE: 117 passed, 0 failed, 5 warnings
HISTORICAL_GATE_STARTED_AT: 2026-09-19T06:52:15.5039519-03:00
HISTORICAL_GATE_COMPLETED_AT: 2026-09-19T06:53:20.7351859-03:00
HISTORICAL_GATE_WALL_SECONDS: 65.231234
LEVEL_A: 194 passed, 0 failed, 5 warnings
LEVEL_A_STARTED_AT: 2026-09-19T06:54:31.2635800-03:00
LEVEL_A_COMPLETED_AT: 2026-09-19T06:55:38.0425234-03:00
LEVEL_A_WALL_SECONDS: 66.7789434
PY_COMPILE: PASS
NODE_CHECK: PASS
STRICT_JSON: PASS - 270 files, zero duplicate keys
GIT_DIFF_CHECK: PASS
PROTECTED_DIFF: EMPTY
PRODUCT_REPAIR: NONE
```

The final-document update was rechecked against history. That post-lock
attempt returned `113 passed, 4 failed, 5 warnings` because four 04.x guards
observed the still-modified Macro 05 documentary files through their working
tree listing. The exact Macro 05 documentary paths were then added to the
historical adapter's nominal filter. The accepted retry passed:

```text
POST_LOCK_HISTORICAL_RETRY_STARTED_AT: 2026-09-19T07:30:23.9567313-03:00
POST_LOCK_HISTORICAL_RETRY_COMPLETED_AT: 2026-09-19T07:31:56.8253095-03:00
POST_LOCK_HISTORICAL_RETRY_WALL_SECONDS: 92.8685782
POST_LOCK_HISTORICAL_RETRY_RESULT: 117 passed, 0 failed, 5 warnings
POST_LOCK_HISTORICAL_RETRY_EXIT_CODE: 0
```

## Level B

```text
LEVEL_B_ATTEMPT_1_STARTED_AT: 2026-09-19T06:56:05.1921403-03:00
LEVEL_B_ATTEMPT_1_COMPLETED_AT: 2026-09-19T07:24:20.1661427-03:00
LEVEL_B_ATTEMPT_1_WALL_SECONDS: 1694.9740024
LEVEL_B_ATTEMPT_1_RESULT: 7199 passed, 6 skipped, 6 warnings
LEVEL_B_ATTEMPT_1_EXIT_CODE: 0
LEVEL_B_ATTEMPT_1_PROCESS_SECONDS: UNKNOWN
LEVEL_B_ATTEMPTS_TOTAL: 1
INTERRUPTIONS: 0
```

The six skips are pre-existing conditional tests. The six warnings are the
known FastAPI `on_event`, Starlette cookie persistence and OpenTelemetry
importlib metadata deprecations. No Level B failure or product repair occurred.

## Closure and fixed point

```text
OFFICIAL_VARIANT: A_NO_PRODUCT_REPAIR
CHECKPOINT_STATUS: INTERNALLY_CLOSED
P1_FAMILY: INTERNALLY_CLOSED
EXTERNAL_EXPOSURE: DEFAULT_DENIED
MACRO_06: SELECTED_NOT_STARTED
DOCUMENTARY_LOCK_PARENT: 26fef3b83529aef93cd7afdfc6cafef7b435fedb
DOCUMENTARY_LOCK_COMMIT_HASH: REPORTED_EXTERNALLY_AFTER_FETCH
```

The final documentary lock is created only after this journal is complete.
Its own hash is not written into this journal or its evidence; the live HEAD,
remote equality and fetch time are reported after publication.
