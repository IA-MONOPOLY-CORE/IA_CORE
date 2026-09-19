# Roadmap 4.x Macro-Mission 06.2 Red Reproduction

## Purpose

This document preserves the executable red reproduction captured before the
V2.2 repair. The runner exercises the published V2.1 implementation against
three concrete gaps. It is evidence of the predecessor defect state, not an
ordinary green validation command.

## Execution receipt

| Field | Value |
| --- | --- |
| Command | `python scripts/run_mission_closure_v2_2_red_reproduction.py` |
| Started | `2026-09-19T19:50:57.5127071-03:00` |
| Finished | `2026-09-19T19:51:00.1438585-03:00` |
| Exit code | `1` |
| Wall time | `2.631151` seconds |
| Combined log SHA-256 | `a70ac0e7c16fc00601d84da11355a20263faaaad18a22b90f9b842f34e47b371` |
| Repository head | `66f809c` (`test(closure): reproduce macro 06.2 v2.1 gaps`) |
| Policy under test | Published Macro 06.1 V2.1 policy and validator |

Exit code `1` is the expected red outcome: all three predecessor gaps were
reproduced. The earlier harness-only import failure is not part of this
receipt and was corrected before the captured run.

## Reproduced defects

| Identifier | Result | Actual cause |
| --- | --- | --- |
| `RED-062-001` | `REPRODUCED` | V2.1 accepted a path modified before and after `validation_basis` because it compared path sets rather than direct post-basis content/state. |
| `RED-062-002` | `REPRODUCED` | V2.1 accepted `PROVEN` without provider-originated source, capture time, proof commit, proof SHA or provider response reference. |
| `RED-062-003` | `REPRODUCED` | V2.1 accepted two successful Level B runs for the same basis and selected only the last one. |

The reproduction was committed before the V2.2 implementation:

```text
66f809c test(closure): reproduce macro 06.2 v2.1 gaps
```

The red corpus remains preserved and is not rewritten by the successor gate.
