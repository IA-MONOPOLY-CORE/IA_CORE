# Roadmap 4.x Macro-Mission 06 - Commit Accountability Ledger

This ledger is completed in the canonical evidence after the hashes exist. The
documentary lock is the final commit and is represented by the fixed-point
postpublish envelope rather than a self-referential hash inside its own file.

| Station | Purpose | Category | Validation | Rollback |
| --- | --- | --- | --- | --- |
| 1 | Install generic V2, policy schema, Macro 06 policy, anti-weakening tests and CI repo-local step | executable/test/configuration | focal, py_compile, policy validation, diff check | revert one method infrastructure commit and establish a new basis |
| 2 | Record repository truth, VERO/FIRE/Developmental Symmetry adjudications, ownership and family selection | documentary | strict Markdown/JSON census and historical impact | revert documentary adjudication commit without touching product |
| 3 | Publish canonical evidence and closure checkpoint | evidence/documentary | prelock V2, post-evidence gate | revert only the documentary lock; preserve executable basis |
| 4 | Normal publication and fresh fetch | remote operation | HEAD/origin equality, 0/0, clean, diff check | no force; operator may stop without destructive recovery |

Every file is enumerated in the machine evidence with exact path, category,
commit, purpose, validation and rollback. No product file is authorized.
