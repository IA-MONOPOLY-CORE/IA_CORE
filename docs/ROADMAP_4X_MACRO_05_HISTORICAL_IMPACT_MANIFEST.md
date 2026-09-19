# Roadmap 4.x Macro-Mission 05 - Historical Impact Manifest

## Baseline and planned scope

```text
BASELINE: 9148f023f4df8e642f396f08a6386f8967d70efb
CURRENT_HISTORICAL_ADAPTER: tests/historical_test_context.py
PRODUCT_REPAIR: NONE_UNTIL_RED_EVIDENCE
WORKING_TREE_SUBSTITUTION: FORBIDDEN
ASSERTION_REMOVAL: FORBIDDEN
BROAD_GLOBS: FORBIDDEN
```

The mission may add only exact nominal mappings for Macro 05 artifacts and
must preserve each historical checkpoint's own contract. Current tests read
current truth. Historical tests read their ledgered checkpoint context.

## Required historical cohort

The gate covers the P1-A, P1-B, P1-C and P1-D focal suites, Macro 04 entry,
Macro 04.3, Macro 04.4, Macro 04.5, Macro 04.6, API admin consumers, Macro 05
guards, Method Santi 3.2.3/3.2.4, the P4 post-boundary precedent when shared
history is touched, and every exact guard discovered by manifest search.

## Protected history

No Macro 03 historical document is rewritten. P4 remains internally closed.
P1-A/B/C/D implementation files are read-only unless a new E2E test produces a
reproducible product defect and the repair remains inside the authorized list.

## Gate result

The first attempt ran the frozen cohort and returned `115 passed, 2 failed,
5 warnings`. Both failures were historical-context mismatches in the 04.6
guard: its scope allowlist still observed Macro 05 commits, and its JSON census
still expected the pre-Macro-05 count of 268. No product assertion failed.

The only adapter change was the exact nominal mapping:

```text
tests/test_roadmap_4x_macro_04_6_p1_d.py
  -> 9148f023f4df8e642f396f08a6386f8967d70efb
```

The second attempt then passed:

```text
HISTORICAL_IMPACT_GATE: PASS
HISTORICAL_GATE_STARTED_AT: 2026-09-19T06:52:15.5039519-03:00
HISTORICAL_GATE_COMPLETED_AT: 2026-09-19T06:53:20.7351859-03:00
HISTORICAL_GATE_WALL_SECONDS: 65.231234
HISTORICAL_GATE_RESULT: 117 passed, 0 failed, 5 warnings
ASSERTIONS_REMOVED: NO
BROAD_GLOBS_ADDED: NO
WORKING_TREE_SUBSTITUTION_FOR_HISTORY: NO
UNCLASSIFIED_HISTORICAL_FAILURES: 0
```

The final documentary update was checked once before the adapter's working-tree
filter was extended and returned `113 passed, 4 failed, 5 warnings`. The four
failures were the same scope-allowlist assertion in the 04.3, 04.4, 04.5 and
04.6 guards; all were caused by visible Macro 05 documentary files still
being modified before the lock commit. The adapter now filters the exact
Macro 05 documentary paths listed in its frozen set, and the accepted retry
returned `117 passed, 0 failed, 5 warnings` with no assertion removal, no
glob expansion and no product change.
