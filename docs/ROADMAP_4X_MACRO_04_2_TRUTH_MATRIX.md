# Roadmap 4.x Macro-Mission 04.2

## Evidence truth matrix

| Artifact | Location | Purpose | State | Family/generation | Authority | Mutability | Side effects | Runtime/provider/tenant/payload | Fail-closed condition | Claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cognitive Kernel graph | `docs/ROADMAP_4X_MACRO_04_1_NODE_FAMILY_AND_TYPED_EDGE_CONTRACT.json` | Canonical identities and typed relations | Materialized inert contract | GOKV/DOOL/OCI, G0 | Repository contract and Owner direction | Versioned, reviewable | None | All disabled | Invalid graph rejected | `OBSERVED` plus `OWNER_DIRECTED` |
| Kernel validator | `gokv/kernel.py` | Structural and security boundary validation | Active development validator | Composition over G0 | Tests and source contract | Code changes require tests | None | No runtime imports or calls | Invalid family, node, edge, evidence or activation rejected | `OBSERVED` |
| Security G0 contract | `docs/ROADMAP_4X_MACRO_04_2_SECURITY_NATIVE_G0_CONTRACT.md` | Place security knowledge in existing families | Materialized inert contract | GOKV/DOOL/OCI, G0 | Owner direction translated into contract | Documentation only | None | No activation | Missing evidence, fit or authorization denies inheritance | `OWNER_DIRECTED` |
| Security ingestion contract | `docs/ROADMAP_4X_MACRO_04_2_SECURITY_INGESTION_CONTRACT.md` | Bound future offensive/untrusted evidence | Future placeholder | GOKV/DOOL/OCI, future only | Future authorization required | Documentation only | None | No external corpus or target | Quarantine, default-deny, no auto-promotion | `OWNER_DIRECTED` / `EXTERNAL_EVIDENCE_REQUIRED` |
| IA_CORE OS direction | `docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md` | Preserve Linux-based AI-native OS vision | Future, not implemented | Future composition | Strategic documentation | Documentation only | None | No OS/runtime/device calls | No implementation claim | `OWNER_DIRECTED` |
| GOKV vault | `knowledge/global_operational/` | Current development-origin knowledge | Existing validated vault | GOKV, G0 | Existing schema/registry | Lifecycle-governed | No new writes | No runtime/provider/tenant use | Registry and item validation | `OBSERVED` |
| Execution metric schema | `knowledge/global_operational/schema/execution_metric.schema.json` | Reusable mission timing record | Existing canonical schema | GOKV metric | Existing GOKV protocol | Versioned JSON | No runtime telemetry | No provider/quota inference | Parse/schema failure rejects metric | `OBSERVED` |
| P1-A status | `docs/ROADMAP_4X_MACRO_04_P1_BOUNDED_REMEDIATION_EXECUTION_PLAN.md` | Next selected product boundary | `NEXT_SELECTED_NOT_STARTED` | P1-A, future | Explicit mission result | Documentation only | None | Route not invoked | Gates remain inactive/default-denied | `OWNER_DIRECTED` |

Lotería is present only where legacy/domain evidence requires it. No domain has
inherent platform or security privilege. The matrix distinguishes observed
repository state from inferred architecture and future external evidence.
