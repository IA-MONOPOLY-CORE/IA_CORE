# Roadmap 4.x Macro-Mission 03 - Commit Accountability Ledger

| Station | Commit | Purpose | Scope | Validation |
| --- | --- | --- | --- | --- |
| 1 | `b5ba679` | Close P4 internally | P4 checkpoint, evidence and ledger | P4 guards: `26 passed` |
| 2 | `48fcbde` | Establish canonical JSON census | JSON reconciliation document | JSON evidence parse: PASS |
| 3 | `f47f4bc` | Reconcile legacy routes | 36-route matrix | Route facts derived from canonical adjudication |
| 4 | `abfec2c` | Recalibrate and select next family | selection matrix, P1 contract and forecast | scoring and forecast documented |
| 5 | `9477b9a` | Reconcile operational learning | GOKV/DOOL/OCI document only | 38-item GOKV validation |
| 6 | `c26d8fa` | Add Macro 03 guard and exact historical allowlists | guard plus exact historical allowlists | focal and historical guard suite: `50 passed` |
| 7 | final publication | Close evidence and README | checkpoint, evidence, ledger and README | final Level B, fetch and clean tree |

## Publication accountability

- `VALIDATION_BASIS_HEAD` is the station 6 commit, not the final documentary
  commit, so the evidence does not chase its own publication hash.
- The final commit contains no product code and no new family implementation.
- A normal `git push origin main` followed by `git fetch origin` is required;
  force operations are forbidden.
- The final result is valid only if full suite, focal guards, canonical JSON,
  py_compile, secret policy, protected diff, diff-check and repository state
  all pass.
