# Roadmap 3.x Direction Acceptance Record

## Decision identity

- Decision source: `PROMPT IA_CORE - ROADMAP 3.x MACRO-MISSION 05`.
- Decision authority: `DIRECTION`.
- Accepted package: Macro 04 true-completion technical evidence package.
- Baseline consumed: `5f50de92330fff60d7998c4af59fef64ed4820bd`.
- Decision state: `DIRECTION_ACCEPTED_AND_ADOPTED`.
- Policy: `DEFAULT_DENY_UNTIL_REQUIRED_EVIDENCE_EXISTS`.
- Common future gate action: `MISSING_EVIDENCE = REMAIN_DISABLED_OR_CONTAINED`.

## Explicit acceptance

Direction accepts the Macro 04 technical evidence package and declares:

`B7_ACCEPTED_WITH_EXPLICIT_LIMITS`

This acceptance closes the 3.x decision gate only within the documented
responsibility boundary. It does not claim production readiness, deployment
exposure, live traffic, tenant enforcement, provider reachability, secret
ownership, product-store recovery or active workforce.

Direction adopts the route-by-route policy recommendations from
`docs/ROADMAP_3_X_DIRECTION_DECISION_PACKET.md`. The historical
`Current destination = UNKNOWN` field remains a preserved pre-decision
photograph. The post-decision authoritative layer is the separate legacy route
adjudication register; no technical successor is inferred from policy.

## Direction limits

1. No runtime, provider, workforce, external network, secret, store or public exposure
   may be activated by this record.
   No external network calls are authorized.
   No secret values may be read or exposed.
2. No adapter, bridge, migration, retirement, deletion, payload v2 or endpoint
   change is authorized by this record.
3. Every missing external fact becomes a governed future gate and remains
   disabled or contained by default.
4. Direction remains the final gate owner until an explicit delegation to a
   functional owner is recorded.
5. A route disposition is a policy decision, not proof that implementation or
   compatibility evidence exists.

## First future block

Direction delegates Architecture to prepare the first bounded 4.x entry block:

`P4_CATALOG_DOMAIN_READS`

The selection is limited to the seven catalog/domain read routes. It is not an
implementation authorization. The future contract is recorded in
`docs/ROADMAP_4X_MACRO_01_P4_CATALOG_DOMAIN_READS_AUTHORITY_COMPATIBILITY_AND_BOUNDED_REMEDIATION.md`.

## Closure predicates

The acceptance record establishes the following current predicates:

| Predicate | Result |
| --- | --- |
| `OPEN_DIRECTION_DECISIONS` | `0` |
| `UNCONTROLLED_UNKNOWNS` | `0` |
| `UNOWNED_GATES` | `0` |
| `ROUTES_ACCOUNTED` | `36` |
| `ROUTES_WITH_ACTIVE_DIRECTION_DISPOSITION` | `36` |
| `PRODUCT_CHANGES` | `0` |
| `ROADMAP_4X_EXECUTED` | `0` |
| `PRODUCTION_READY` | `0` |

`ROADMAP_3_X_TRUE_COMPLETION_ACCEPTED_AND_CLOSED_WITH_EXPLICIT_FUTURE_GATES`

This result means 3.x is closed within its responsibility with governed
future obligations. It does not mean that any future gate passed or that P4
implementation started.
