# Roadmap 4.x Macro-Mission 04.1

## Domain module parity audit

## Finding

The current backend status surface contains a legacy domain-specific branch and
field naming in its process-global diagnostic response. The route matrix and
`api.py` source establish that this is an implementation detail of the legacy
surface; they do not establish privileged status, superior quality or special
product treatment.

This is recorded as `legacy singled-out domain status`, or
`deuda de paridad de modulo de dominio`. It is not a feature, promotion, health
proof or product hierarchy.

## Classification of references

| Reference class | Treatment in 04.1 |
| --- | --- |
| Historical checkpoints and closed evidence | Preserve exactly as immutable lineage |
| Technical identifiers required by compatibility | Preserve until a versioned migration exists |
| Current backend branch/field | Audit only; no endpoint modification in 04.1 |
| Current route matrix and P1 plan | Update the future contract to generic module representation |
| Tests and allowlists | Keep exact historical expectations; add only mission paths |
| UI/presentation | No product UI change and no new prominence |
| Unproven/dead references | Keep classified as unknown until separately proven |

## Future P1-A obligation

When P1-A is separately started, its status projection must represent
`domain modules` through a generic `domain_module_status` structure with
parity of fields, visibility and authority. The migration must be versioned,
consumer-tested, sanitized and reversible. It must not turn the old identifier
into an alias for a privileged module, and it must not alter the other three P1
subfamilies.

P1-A remains `SELECTED_NOT_STARTED` and is temporarily paused behind this
cognitive-kernel reconciliation. The four existing P1 routes remain unchanged;
no route is invoked or exposed by this audit.

## Invariants

`NO_DOMAIN_MODULE_HAS_INHERENT_PRIVILEGED_OR_FEATURED_STATUS`

`LOTTERY_IS_AN_ORDINARY_DOMAIN_MODULE`

No module receives special access, model priority, retention, observability,
inheritance or Owner bypass from its name. Domain capability remains governed
by the same evidence, privacy, ownership and compatibility rules as every other
module.
