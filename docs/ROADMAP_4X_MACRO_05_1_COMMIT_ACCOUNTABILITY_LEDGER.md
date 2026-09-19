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
