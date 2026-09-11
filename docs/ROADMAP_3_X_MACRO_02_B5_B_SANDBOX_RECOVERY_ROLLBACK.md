# Roadmap 3.x Macro-Mission 02: B5-B Sandbox Recovery and Rollback

`ROADMAP_3X_MACRO_02_B5_B_SANDBOX_RECOVERY_ROLLBACK_MATERIALIZED`

## Contract inventory

| Obligation | Current evidence | Result |
| --- | --- | --- |
| sandbox root containment | `core/domain_materialization_rollback.py` resolves the declared sandbox root and rejects outside paths | proven by contract/tests |
| path traversal and symlink escape | traversal, operational domain roots, symlink escape, globs, and undeclared paths are blocked | proven by negative tests |
| materialization lineage | domain and artifact manifests declare created paths and materialization identity | proven for sandbox artifacts |
| rollback | declared paths are removed and rollback records are retained | proven in temporary fixtures |
| archive | no product archive contract is present | not demonstrated; remains blocked |
| restore | regeneration can materialize a new generation after rollback; independent product restore is absent | sandbox-only, not product restore |
| reset/delete | delete scope is manifest-declared and bounded to sandbox paths | proven for sandbox rollback only |
| partial failure | blocked/skipped/preserved paths and JSON-safe reports are represented | contract evidence; operational failure not exercised |
| idempotency | second rollback reports `already_rolled_back_integral` without new deletion | proven by checkpoint tests |

## Boundary

The existing 6.1 test suite uses `tmp_path` fixtures and hashes operational roots
before and after the exercise. It does not modify product domains, agents,
catalogs, memory, stores, UI, or integrations. The rollback contract declares
`operational=false`, `runtime_enabled=false`, and `execution_enabled=false`.

This station does not add archive/restore APIs, operational deletion, external
recovery, or a product data migration. A future mission may decide whether
archive and restore are required; until then they remain an explicit unknown.
