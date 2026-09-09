# Roadmap 3.0.A N0 - Strategic Contract Audit

## Gate

`ROADMAP_3_0_A_N0_STRATEGIC_CONTRACT_AUDIT_PASSED`

## Mission boundary

This document records strategic requirements only. It does not create agents,
profiles, presets, papers, teams, vector databases, providers, APIs, runtime,
execution, auth, UI or hardware logic.

## Existing requirements and contracts

| Requirement | Existing evidence | Status |
| --- | --- | --- |
| Initial professional library | `catalogs/areas.json`, `niches.json`, `professional_profiles.json`; 30 areas, 200 niches, 106 profiles | `EXISTING_REQUIREMENT`, initial mass critical |
| Roles and specializations | `catalogs/roles.json`, `specializations.json`; domain `profile_catalog.json` | `EXISTING_REQUIREMENT` |
| Model policies | `catalogs/profile_model_policies.json`; 15 active policies reported by current library docs | `EXISTING_REQUIREMENT` |
| Hardware-aware model recommendation | `core/model_recommendation.py`, `config/hardware_profile.json`, professional recommendation docs | `EXISTING_REQUIREMENT`, model-level only |
| Presets and paper seeds | domain preset schemas/materializers and docs | `EXISTING_REQUIREMENT`, partly sandbox/derived |
| Team templates | team schema/materializer, generated template docs | `EXISTING_REQUIREMENT`, future/sandbox boundary |
| Permission contracts | `docs/AGENT_PERMISSION_CONTRACT.md` and core contract | `EXISTING_REQUIREMENT`, contract-only/non-operational |
| Memory metadata and policies | agent config/paper schemas and memory docs | `PARTIAL_REQUIREMENT` |
| Universal model/provider vision | provider registry plus future architecture index | `PARTIAL_REQUIREMENT`, not universal platform |
| Enterprise architecture | `docs/FUTURE_PLATFORM_EXTENSION_INDEX.md` and FUTURE_* docs | `EXISTING_REQUIREMENT`, documented future only |

## New requirements captured by 3.0.A

- Open-ended business creation without an artificial catalog ceiling.
- Coverage audit before taxonomy expansion.
- Agent Blueprint Library as the reusable workforce source.
- Conceptual `AGENT_READY_V1` contract.
- Logical memory isolation by agent, team and business without requiring one
  physical vector database per agent.
- Ideal, minimum functional and hardware-fitted organizational configurations.
- Concurrency reduction and serialization as capacity strategies that preserve
  professional quality.
- Universal model/provider alignment with workforce readiness.
- A mandatory agent/model workforce readiness gate before controlled business
  operation, placed at the correct roadmap 6.x entry point.
- A future coverage audit contract separating existing, ready, partial, missing,
  composable and expansion-required capability.

## Reconciliation decisions

`30 areas / 200 niches / 106 profiles` are preserved as current initial library
scope, not an upper bound. Current catalogs are a mass critical base; they do
not prove complete business coverage. Current model recommendation is not an
organizational capacity engine. Current presets, papers and teams do not prove
that a business can be constituted operationally. Existing future enterprise
documents are extended rather than duplicated.

## Conflicts and superseded interpretations

- **Conflict rejected:** treating current counts as a closed universe.
- **Conflict rejected:** treating a job/profile catalog as complete business
  composition.
- **Conflict rejected:** treating a JSON/config as `READY_TO_CONSTITUTE_BUSINESS`.
- **Conflict rejected:** treating logical memory ownership as a mandatory
  physical vector database per agent.
- **Superseded interpretation:** hardware-limited means lower professional
  quality. The future rule is lower concurrency or more serialization first.

## Current reality labels

`CURRENT_REAL` includes catalogs, model recommendation, permission contracts and
some sandbox materialization. `CURRENT_PARTIAL` includes profile-to-domain
coverage, presets, paper seeds, teams and model/provider routing. `CURRENT_SANDBOX`
includes derived artifacts and non-operational team/agent materialization.
`CURRENT_DOCUMENTED` includes the future enterprise architecture. The strategic
requirements below are `FUTURE_REQUIREMENT`, `FUTURE_STRATEGIC_DIRECTION` or
`FUTURE_GATE`; they are not implemented by this mission.

