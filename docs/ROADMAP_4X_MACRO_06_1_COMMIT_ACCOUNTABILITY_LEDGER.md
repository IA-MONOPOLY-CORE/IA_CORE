# Macro 06.1 Commit Accountability Ledger

| station | commit | parent | subject | purpose | validation | bounded rollback |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | `a4a9fb9fc8ee166fcac24b9c3bb3371d186da8de` | `d0f400eb89bc21a867a1c124136575a3436f593b` | `test(closure): reproduce macro 06.1 gate gaps` | preserve the intentional red reproduction | red run exit 1, 5 failed, 1 warning | revert reproduction only; keep predecessor immutable |
| R2 | `3e6f970b00668610092da85d1e2fb16d98db1b0d` | `a4a9fb9fc8ee166fcac24b9c3bb3371d186da8de` | `feat(closure): add v2.1 scope and causality enforcement` | add V2.1 gate, wrapper, schema, policy, CI and tests | focal 27 passed; py_compile; policy; diff-check | revert method-infrastructure commit and establish new basis |
| R3 | `16cf06b9262bdef0b0e2a14baa7b351a33b639ba` | `3e6f970b00668610092da85d1e2fb16d98db1b0d` | `test(closure): preserve macro 06.1 historical continuity` | extend exact historical continuity lists and CI corpus | historical 104 passed; policy and py_compile | revert continuity adapter and invalidate later evidence |
| R4 | `DOCUMENTARY_DRAFT_COMMIT` | `16cf06b9262bdef0b0e2a14baa7b351a33b639ba` | documentary VERO/FIRE evidence package | record reports and draft canonical evidence | strict JSON and historical scope | revert documentary draft only |
| R5 | `DOCUMENTARY_LOCK_SELF_REFERENCE` | R4 | documentary lock | add finalized evidence and machine receipts | prelock, push/fetch and renderer | no force; stop if remote equality fails |

R4 and R5 are replaced by their full Git hashes in the final canonical
evidence after the commits exist. The self-reference is permitted only for
the documentary lock files that necessarily contain their own final lock
record.
