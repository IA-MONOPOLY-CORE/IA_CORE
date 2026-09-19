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
