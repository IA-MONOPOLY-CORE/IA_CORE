# Roadmap 4.x Macro 05.1 Commit Accountability Ledger

The canonical evidence contains the complete ordered ledger. Each commit records
its full hash, parent, subject, station, exact files, purpose, validation, and
bounded rollback. The validation-basis commit is the last executable commit. The
documentary lock contains only `DOCUMENTARY_ONLY` and `EVIDENCE_ONLY` paths and
does not embed its own final hash.

```text
VALIDATION_BASIS_IS_REAL_HASH: REQUIRED
DOCUMENTARY_LOCK_PARENT_IS_REAL_HASH: REQUIRED
DOCUMENTARY_LOCK_SELF_HASH: EXTERNAL_POSTPUBLISH_ONLY
```

The final executable basis is `a17c37b1a69c67e65ca40e523aa0d1fc224b85e0`.
Its parent is the fixture-clock basis `c8700fb488f8e7759233b46a2384caf6b347f58d`.
The final lock parent is the same basis commit after the evidence-only content is
finalized; the live lock hash is emitted after fetch and is never inserted into its
own evidence bytes.
