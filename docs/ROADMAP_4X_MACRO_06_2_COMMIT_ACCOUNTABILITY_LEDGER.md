# Roadmap 4.x Macro-Mission 06.2 Commit Accountability Ledger

| Station | Commit | Purpose | Validation |
| --- | --- | --- | --- |
| R1 red reproduction | `66f809c` | Preserve the executable V2.1 red corpus | Expected exit `1`; three gaps reproduced |
| R1 red evidence | `b793fcf` | Preserve the red execution receipt | Red log SHA recorded |
| R2 V2.2 implementation and continuity | `252ba8b915b7ff67868a50917d7858ee8ff8b9f8` | Install V2.2, policy, workflow, tests and documentary candidate | Focal/historical/static validation passed |
| R3 basis repair | `5d69f70be0847ff4f28fa3bcc2cdcb9dc6c8372a` | Bind all durable preterminal logs and receipts to the exact post-terminal allowlist | New basis revalidated before terminal run |
| R3B receipt-lineage repair | `8bf79015deee831752f5553a083d44c9d07afbc4` | Require renderer validation of every durable validation and special closure receipt | Final focal, historical, Level A and terminal runs passed |
| Invalidated terminal attempt 1 | `5d69f70be0847ff4f28fa3bcc2cdcb9dc6c8372a` | Historical reconciliation record | Allowlist omission invalidated the attempt |
| Invalidated terminal attempt 2 | `8bf79015deee831752f5553a083d44c9d07afbc4` | Historical reconciliation record | Receipt-lineage enforcement gap invalidated the attempt |
| Documentary lock | `DOCUMENTARY_LOCK_SELF_REFERENCE` | Add final evidence, receipts, checkpoint, logs and closure documents | Parent is `8bf79015deee831752f5553a083d44c9d07afbc4`; postpublish renderer resolves final head |

No force push, pull, merge, rebase, reset or tag was used.
