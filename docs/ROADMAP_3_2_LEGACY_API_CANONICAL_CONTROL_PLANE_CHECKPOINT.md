# Roadmap 3.2 Checkpoint - Legacy API / Canonical Control Plane

## Identity

- Mission: `roadmap_3_2_legacy_api_canonical_control_plane_coverage_read_only_audit`
- Baseline: `2255295f5ffe4f7348476acfca606a84aa12af35`
- Branch: `main`
- Mode: `READ_ONLY_PRODUCT_AUDIT`
- Result: `ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_COVERAGE_READ_ONLY_AUDIT_PASSED`

## Scope Closure

The mission reconciled the 36 legacy API routes against the current canonical
control plane using static source and call-path evidence. It did not implement
authentication, authorization, CORS, secret storage, a legacy bridge, runtime,
provider access or any remediation.

No product code, remediation or bridge was written. No API, core, agents,
providers, domains, config, contract, schema, payload, UI, store, memory,
knowledge or deployment file was modified.

No application import, server start, endpoint call, provider call, network call,
runtime execution, agent execution, store mutation or secret-value access was
performed.

## Station Graph

| Station | Result |
| --- | --- |
| N0 Preflight + authority reconstruction | PASS; `NO_DIFF` |
| N1 Canonical control-plane census | PASS; 20 controls documented |
| N2 36-route coverage matrix | PASS; 36/36 routes |
| N3 Contract/payload/permission reconciliation | PASS |
| N4 High-risk route reconciliation | PASS; chat/settings/mutative routes covered |
| N5 Remediation readiness | PASS; 7 findings classified |
| N6 Cross-layer synthesis | PASS; apparent/true frontiers separated |
| N7 Tests/checkpoint/publication | PASS after final validation |

## Route and Coverage Summary

- Total routes: `36`
- GET: `22`
- POST: `12`
- PUT: `1`
- DELETE: `1`
- Mutative: `14`
- Canonical control-plane covered: `0`
- Partially covered: `1`
- Legacy bypass demonstrated: `2`
- Coverage not demonstrated: `33`
- Not applicable: `0`

The two positive bypass call paths are:

- `POST /api/chat`: legacy API -> Supervisor -> AgentManager -> ProviderRegistry
  -> provider adapters, with no demonstrated canonical control-plane entrypoint.
- `POST /api/settings`: legacy handler -> settings JSON/config writes, with no
  demonstrated canonical secret/request/confirmation entrypoint.

`POST /api/domains/create` is `PARTIALLY_COVERED` because local domain
validation and materialization code exists, while canonical request,
permission, confirmation and runtime coverage is not connected.

## Canonical Control Plane

The census contains 20 controls across permission, capability, secrets,
context/model/output boundaries, runtime activation, readiness, attempt and
lifecycle contracts, active contracts/executor, internal UI/exposure/request/
dispatcher/confirmation/response/payload services, sandbox validation,
audit/observability and approval workflow.

The central result is:

```text
CANONICAL_CONTRACT_EXISTS != LEGACY_ROUTE_USES_CANONICAL_CONTRACT
```

The contracts are real and tested on their own surfaces. No legacy route was
proven to call those entrypoints.

## Findings

The seven Roadmap 3.1 findings were all preserved with provenance and
reconciled. Their severities remain five P1 and two P2. No new finding was
added and no severity was changed.

| Finding | Readiness |
| --- | --- |
| F-3.1-001 route auth/authz | MORE_READ_ONLY_TRUTH_REQUIRED |
| F-3.1-002 wildcard CORS | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-003 settings secret/write | REMEDIATION_SEMANTICS_DERIVABLE_FROM_EXISTING_CONTRACT |
| F-3.1-004 chat provider path | MORE_READ_ONLY_TRUTH_REQUIRED |
| F-3.1-005 legacy mutation routes | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-006 canonical gates not global over legacy | REQUIRES_DIRECTION_POLICY_DECISION |
| F-3.1-007 provider/network reachability | REQUIRES_RUNTIME_EVIDENCE |

## Frontiers

Apparent frontiers resolved by existing contracts:

- default-deny capability and runtime semantics;
- secret redaction/blocking semantics;
- internal request safety and explicit confirmation semantics;
- stable payload and sandbox-path semantics.

True hard frontiers not crossed:

- HTTP identity, ownership and tenant/business/team/agent authorization;
- legacy destination/bridge/retirement policy;
- allowed CORS policy;
- deployment edge and external ingress evidence;
- provider/network/runtime evidence.

## GOKV / OCI / DOOL

- OCI mode: `PROMOTED_ONLY`
- Conflict rule: `CURRENT_CONTRACT_WINS`
- Minimum sufficient inheritance: active
- `conditioned_autonomy`: `VALIDATED`
- `conditioned_autonomy` promoted: `false`
- New learning: none; no append-only intake required

## Validation

Focal validation:

```text
python -m json.tool docs/ROADMAP_3_2_LEGACY_API_CANONICAL_CONTROL_PLANE_EVIDENCE.json
python -m pytest -q tests/test_roadmap_3_2_legacy_api_canonical_control_plane_audit.py
python -m pytest -q tests/test_roadmap_3_1_security_permission_activation_boundary_audit.py
git diff --check
```

The new guard checks the exact AST route census, every route's coverage
classification and evidence fields, 14 mutative routes, deep chat/settings
analysis, canonical provenance, all seven 3.1 findings, no secret values, no
remediation code and authorized diff scope.

Group/canonical/deep historical selection remained static and safe. No network,
provider, runtime, productive-write or secret-access tests were run. The
unchanged Roadmap 3.1 guard passed in a detached worktree at its published
checkpoint (`10 passed`). Its current-tree closed-world scope check rejects
legitimate Roadmap 3.2 artifacts by design; the historical guard was not
modified or relaxed.

## Publication State

- Authorized artifacts: the Roadmap 3.2 audit, evidence JSON, test and this
  checkpoint only.
- Local station commits: required and recorded in Git history.
- Remote publication: only after final fetch/divergence verification.
- Final HEAD: recorded by the post-publication Git verification in the mission
  report; it must equal `origin/main` with ahead/behind `0/0`.
- Working tree: required clean.
- `git diff --check`: required PASS.

## Handoff

This checkpoint is the self-contained handoff to the CHAT / ARCHITECT for
post-mission architectural recalculation. Do not select, compile or execute the
next roadmap from this mission.

`POST-MISSION ARCHITECTURAL RECALCULATION`
