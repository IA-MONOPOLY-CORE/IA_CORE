# Roadmap 4.x Macro-Mission 06.2.4-A

## Fail-Closed Governed Authority Resolver

This station is an additive successor to V2.2.3. It proves only governed
component resolution. It does not implement typed semantic derivation,
negative/metamorphic execution, Level-A identity, package integrity, a finalizer,
terminal integration, VERO, FIRE, or P3 execution.

The successor derives `C:\IA_CORE` from its fixed source anchor and verifies
that the derived location is the expected Git worktree on `main`. It then loads
only the fixed repository-relative authority set:

`docs/ROADMAP_4X_MACRO_06_2_4_A_AUTHORIZED_VALIDATION_INPUT_SET.json`

The caller may provide only `logical_artifact_id` and `semantic_role`. The
caller cannot select a repository root, authority set, path, expected hash,
loader, resolver, raw bytes, or component entry. The authority set is validated
before resolver construction. Component bytes are read exactly once by the
governed resolver, hashed in memory, and the same bytes are returned.

The resolver emits authorization facts only. It does not claim execution,
validation success, semantic success, or closure authority.

Historical V2.2.3 remains unchanged and is intentionally preserved as the
assertion-trusting predecessor that accepts the reproduced missing-authority
bypass. Micro A rejects the same class of input fail-closed.
