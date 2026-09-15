# Roadmap 4.x Macro-Mission 04.3

## P1-A Platform Status Health checkpoint

### Result

`ROADMAP_4X_MACRO_04_3_P1_A_PLATFORM_STATUS_HEALTH_INTERNAL_REMEDIATION_COMPLETE_VERSIONED_TIERED_DOMAIN_NEUTRAL_NO_PROVIDER_SIDE_EFFECTS_EXTERNAL_EXPOSURE_DEFAULT_DENIED_NEXT_SUBFAMILY_SELECTED_NOT_STARTED`

`P1-A_STATE = INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`

This checkpoint is the post-remediation record for baseline
`6dd040e0985da134f18f2bc85a338aa1bf770d3f`. The route remains a local read;
the checkpoint does not declare productive exposure, identity activation or
runtime readiness.

### What changed

- `GET /api/status` now returns exact `platform_status.v1` minimal fields.
- `GET /api/status?full=true` is retained as a compatibility alias and is
  denied by the default unconfigured resolver.
- The detailed contract is prepared behind
  `platform_status.read_detailed` and a trusted server-side principal.
- Recursive sanitization, strict view separation and component failure
  isolation are implemented and tested.
- Overview, Hybrid and the Providers panel no longer depend on unsafe status
  inventories or raw diagnostics.
- Historical 04.1/04.2 guards now validate their own published checkpoints;
  no historical assertion was removed or globally relaxed.

### Preserved boundaries

No provider, model, network, memory, log, dynamic-metric, domain computation,
runtime, execution, mutation, promotion, tenant, secret, payload, P0, P3, P4,
Request Draft Panel, unrelated widget, integration or endpoint outside status
was changed or activated. GOKV/DOOL/OCI remain the same three inert families;
there is no new candidate, promotion, event, pack or vault write:
`NO_NEW_CANDIDATE`.

The invariant `STATUS_READS_STATE_STATUS_DOES_NOT_PROBE_THE_WORLD` is enforced
by the route and adversarial tests. The invariant
`DOMAIN_MODULES_HAVE_PARITY_NO_DOMAIN_HAS_INHERENT_PLATFORM_PRIVILEGE` is
preserved: detailed status uses generic `domain_modules`; Lotería has no
special position.

### Level and publication state

`LEVEL_A = PASS` and `LEVEL_B = PENDING_UNTIL_FULL_SUITE_AND_REMOTE_FETCH`
until the final evidence is populated. Visual browser validation is
`TOOLING_UNAVAILABLE`; Node checks and frontend/backend integration assertions
are the recorded fallback. The validation basis and post-publication HEAD are
recorded in the machine evidence and commit ledger.

### Next selection only

Scoring of urgency/readiness selects
`P1-B_PROTECTED_MEMORY_SELECTED_NOT_STARTED`. P1-C Protected Logs/Events and
P1-D Domain Dynamic Metrics remain `DEFERRED_NOT_STARTED`. No next subfamily is
implemented. Macro-Mission 05 no comenzó. Enterprise Foundry, Cyber Range and
IA_CORE OS remain future-only and not implemented.

Selection labels: `P1-B_PROTECTED_MEMORY_SELECTED_NOT_STARTED`,
`P1-C_PROTECTED_LOGS_EVENTS_DEFERRED_NOT_STARTED` and
`P1-D_DOMAIN_DYNAMIC_METRICS_DEFERRED_NOT_STARTED`.

### Evidence

- [status contract](ROADMAP_4X_MACRO_04_3_P1_A_STATUS_CONTRACT.md)
- [truth matrix](ROADMAP_4X_MACRO_04_3_P1_A_TRUTH_MATRIX.md)
- [consumer compatibility](ROADMAP_4X_MACRO_04_3_P1_A_CONSUMER_COMPATIBILITY.md)
- [execution metrics](ROADMAP_4X_MACRO_04_3_P1_A_EXECUTION_METRICS_BASELINE.md)
- [machine evidence](ROADMAP_4X_MACRO_04_3_P1_A_CHECKPOINT_EVIDENCE.json)
- [commit ledger](ROADMAP_4X_MACRO_04_3_P1_A_COMMIT_ACCOUNTABILITY_LEDGER.md)
