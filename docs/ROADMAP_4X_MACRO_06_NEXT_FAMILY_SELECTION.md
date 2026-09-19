# Roadmap 4.x Macro-Mission 06 - Next Family Selection

## Candidate scoring

Scores are directional five-point assessments grounded in current repository
evidence. They select a future entry contract, not implementation permission.

| Family | Beta criticality | Dependency order | Risk reduction | Value unlocked | Maturity | Readiness | Reversibility | Testability | Validation cost | Implementation cost | Security exposure | External dependency | Dev symmetry | Debt reduction | Total | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P3 `LOTERIA_VALIDATION_EVOLUTION` | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 4 | 4 | 4 | 52 | SELECTED |
| P2 `CHAT_ORCHESTRATION` | 4 | 3 | 4 | 5 | 2 | 2 | 2 | 3 | 2 | 2 | 1 | 1 | 3 | 3 | 40 | defer |
| P7 `SETTINGS` | 5 | 3 | 5 | 4 | 2 | 2 | 2 | 3 | 2 | 2 | 1 | 1 | 3 | 4 | 39 | defer |
| P5 `DOMAIN_MATERIALIZATION` | 4 | 3 | 4 | 4 | 2 | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 3 | 4 | 39 | defer |
| P6 `WORKFORCE_AGENT_LIFECYCLE` | 4 | 3 | 4 | 5 | 2 | 2 | 2 | 3 | 2 | 1 | 1 | 1 | 3 | 4 | 37 | defer |
| P8 `PROVIDER_HARDWARE` | 4 | 2 | 3 | 4 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 2 | 3 | 28 | defer |
| P9 `HOSTING_ROOT` | 4 | 2 | 4 | 3 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 26 | defer |
| VERO/FIRE runtime | 2 | 1 | 2 | 4 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 13 | reject for this cursor |

The sum is a decision aid, not a permission model. P3 wins because existing
domain validation/lifecycle modules, compatibility routes and tests provide a
bounded internal evidence base; it is more reversible and less externally
dependent than provider, settings, workforce and hosting families.

## Selected cursor

```text
NEXT_EXECUTION_FAMILY: P3_LOTERIA_VALIDATION_EVOLUTION
NEXT_STATE: SELECTED_NOT_STARTED
```

## Entry conditions

1. Freeze the P3 route and payload universe from the existing 36-route matrix.
2. Define lifecycle authority, compatibility and recovery contracts before any
   product mutation.
3. Prove server-side identity, audience, scope and tenant behavior or keep the
   routes contained/default-denied.
4. Preserve existing validation semantics and use a new validation basis.
5. Use focal, historical, Level A, Level B and post-evidence closure gates.

## Explicit non-goals

No VERO runtime, FIRE runtime, new endpoint, payload v2, tenant activation,
provider integration, external exposure, product UI, autonomous execution,
chaos engineering, GOKV promotion or OCI activation is authorized by this
selection.

## Why not the other candidates

P2, P5 and P6 carry provider, orchestration or mutation blast radius. P7 has
secret, storage and rotation ownership gaps. P8 and P9 require external
provider/network or hosting evidence unavailable in this repository mission.
VERO/FIRE are architecture candidates and must not be selected as a runtime
family before their deferred contracts exist.
