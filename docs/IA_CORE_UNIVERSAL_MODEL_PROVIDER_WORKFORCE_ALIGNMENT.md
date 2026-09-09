# IA_CORE - Universal Model and Provider Workforce Alignment

## Gate

`ROADMAP_3_0_A_N4_MODEL_PROVIDER_ALIGNMENT_PASSED`

## Future alignment contract

An `AGENT_READY_V1` candidate must declare a `MODEL_POLICY`, but readiness must
not imply that a particular model is installed. Business materialization should
resolve against `AVAILABLE_MODEL_CAPACITY`, subject to task quality, hardware,
privacy, provider availability, budget, latency and human review constraints.

The future platform should support:

- an extensible universal model/provider catalog;
- local, cloud and hybrid execution preferences;
- hardware-aware compatibility and a future visual status/semaphore;
- `installed` as a state separate from `compatible`, `available` and
  `recommended`;
- controlled installation, discovery and provider registry extension;
- safe credential boundaries;
- dynamic model and provider recommendation;
- fallback and escalation policies by workload and hierarchy.

## Workforce relationship

The model/provider choice is downstream of professional capability, not a
replacement for it. A blueprint declares workload, reasoning need, privacy and
quality requirements. A future capacity planner then maps those requirements to
model tiers, provider policies and hardware-fitted organization.

`USE_THE_SMALLEST_SUFFICIENT_MODEL_WITHOUT_SACRIFICING_REQUIRED_QUALITY` is the
guiding rule. A small model may be correct for a narrow micro/execution task and
incorrect for a strategic decision; the platform must not flatten all roles to
one model tier.

## Current reality

Current repository capabilities include model policy catalog entries, profile
model recommendation, hardware profile/config, provider registry and local/cloud
compatibility concepts. They are partial and provider adapters are not a
universal installed/available/discovered catalog. Existing provider code must
not be interpreted as a safe activated platform.

## Future phases

Model/provider discovery, installation, credential vaulting, capacity planning,
dynamic recommendation, hardware semaphore and provider fallback require their
own contracts, security review, tests and runtime authorization. None is
implemented by Roadmap 3.0.A.

