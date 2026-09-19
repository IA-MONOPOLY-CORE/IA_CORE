# Macro 06.1 Execution Journal

All clocks below are actual observed clocks unless marked as a policy
forecast. Process CPU time is `UNKNOWN` because the wrapper does not expose a
portable process CPU measurement on this Windows run.

| station | event | start | end | wall_seconds | result |
| --- | --- | --- | --- | ---: | --- |
| S0 | mission accepted/preflight anchor | `2026-09-19T14:41:49.6841702-03:00` | same recorded anchor | 0 | accepted; preflight baseline was clean |
| S1 | red reproduction | `2026-09-19T14:45:43.5140354-03:00` | `2026-09-19T14:46:27.0338614-03:00` | 43.519826 | exit 1; 5 failed, 1 warning |
| S2 | V2.1 implementation commit | `2026-09-19T15:06:54-03:00` | same commit clock | 0 | `3e6f970` |
| S3 | historical continuity commit | `2026-09-19T15:11:07-03:00` | same commit clock | 0 | `16cf06b` |
| S4 | Level A full suite | `2026-09-19T15:11:23.212400-03:00` | `2026-09-19T15:40:55.339121-03:00` | 1772.130471 | 7266 passed, 6 skipped, 6 warnings |
| S5 | final Level B | `2026-09-19T15:41:32.631179-03:00` | `2026-09-19T15:42:38.108106-03:00` | 65.479582 | 122 passed, 0 failed, 5 warnings |
| S6 | focal receipt | `2026-09-19T15:43:56.969912-03:00` | `2026-09-19T15:44:18.154861-03:00` | 21.182239 | 27 passed, 1 warning |
| S7 | historical-impact receipt | `2026-09-19T15:44:26.514299-03:00` | `2026-09-19T15:45:50.645002-03:00` | 84.133069 | 104 passed, 5 warnings |
| S8a | canonical evidence finalization | `2026-09-19T15:57:46.439320-03:00` | same gate event | 0 | evidence SHA `310a1022042c080f58213cf35e3339d7259ded9183bb9dce220d150e0122c07f` |
| S8b | post-evidence receipt | `2026-09-19T15:57:58.240178-03:00` | `2026-09-19T15:57:59.270332-03:00` | 1.030154 | receipt SHA `8fcae0d9c980c1743f4a3a4a0d5e7fe8c47961b93933cfb2d30375f5e55403cd` |
| S8c | prelock receipt | recorded by the gate immediately before lock | recorded in the final receipt | machine-generated | hash is intentionally kept in the receipt/report, not duplicated here |
| S8d | documentary lock, push, fetch and render | recorded after S8c by machine receipts | recorded in postpublish envelope | renderer-derived | external enforcement remains NOT_PROVEN |

The S0 preflight completion is represented by the observed mission anchor
because the initial shell capture did not emit a distinct completion clock;
the zero-length representation is a limitation, not an inferred duration.

## Sequence

```text
PREFLIGHT
-> RED REPRODUCTION
-> V2.1 IMPLEMENTATION
-> HISTORICAL CONTINUITY ADAPTER
-> LEVEL A
-> FROZEN BASIS
-> FINAL LEVEL B
-> CANONICAL EVIDENCE
-> POST-EVIDENCE RECEIPT
-> PRELOCK RECEIPT
-> DOCUMENTARY LOCK
-> NORMAL PUSH
-> FRESH FETCH
-> MACHINE RENDER
```

No P3, product, runtime or external activation step occurred.
