# Macro-Mission 06.2 Negative Control Matrix

The matrix is bounded to closure-method infrastructure. A control is only
credited when a V2.2 test or executable validator observes the relevant state.

| ID | Threat | V2.2 control | Evidence class |
| --- | --- | --- | --- |
| N-01 | Same path changed before and after basis | Direct post-basis committed delta | executable |
| N-02 | Protected commit after basis | Four-surface protected delta | executable |
| N-03 | Protected staged change | Independent index delta | executable |
| N-04 | Protected unstaged change | Independent worktree delta | executable |
| N-05 | Protected untracked path | Independent untracked surface | executable |
| N-06 | Rename into protected surface | Rename source and destination records | executable |
| N-07 | Rename out of protected surface | Rename source and destination records | executable |
| N-08 | Protected deletion | Deletion status record and protected check | executable |
| N-09 | PROVEN with empty provider source | Required provider proof fields | executable |
| N-10 | PROVEN with empty capture time | Required provider proof fields | executable |
| N-11 | PROVEN with empty proof commit | Commit resolution and required field | executable |
| N-12 | PROVEN with empty proof SHA | SHA-256 validation | executable |
| N-13 | Local declaration elevates remote state | Provider-originated source rule | executable |
| N-14 | NOT_PROVEN rendering is static | Dynamic policy state renderer | executable |
| N-15 | PROVEN rendering is unavailable | Positive remote-state test path | executable |
| N-16 | Diff PASS is hardcoded | Three live diff-check commands | executable |
| N-17 | Log altered after receipt | Artifact SHA recomputation | executable |
| N-18 | Receipt self-hash ambiguity | Self field excluded from canonical payload | executable |
| N-19 | Receipt altered after hash | Canonical receipt recomputation | executable |
| N-20 | Non-deterministic report | Two canonical renders and byte comparison | executable |
| N-21 | Absolute or temporary deterministic path | Repository-relative path validation | executable |
| N-22 | Ordinary validation after terminal | Terminality chronology guard | executable |
| N-23 | Multiple terminal attempts for final basis | Exactly one successful terminal Level B | executable |
| N-24 | Candidate mutated after terminal | Exact post-terminal allowlist | executable |

The preserved red reproduction is recorded in
`ROADMAP_4X_MACRO_06_2_RED_REPRODUCTION.md`. The final evidence records the
executed tests and their durable logs; it does not replace the historical
V2.1 evidence.
