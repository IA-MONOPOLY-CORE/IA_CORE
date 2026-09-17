# Roadmap 4.x Macro-Mission 04.6 - Domain Neutrality and Tenant Scope Future Contract

## Purpose

P1-D separates a protected internal aggregate from the legacy Lotería source.
The source may be adapted internally, but Lotería vocabulary, state, phase,
version, strategy, and execution details do not become platform contracts.

## Future-only capabilities

```text
tenant_metrics.read: FUTURE_INACTIVE_UNTIL_OWNERSHIP_PROVEN
TENANT_BUSINESS_AGGREGATION: UNKNOWN_DEFAULT_DENY
OWNER_OR_OPERATOR_DETAIL: PROPOSED_NOT_PRODUCTION_ACTIVE
EXTERNAL_METRICS_READ: DEFAULT_DENIED
```

No current principal, tenant identifier, or client selector proves ownership.
The presence of `tenant_id` is therefore rejected with a non-enumerative 404
after authority checks and before any source read.

## Required future evidence

Before tenant access can be activated, a later mission must prove:

- authoritative tenant identity and ownership;
- isolation of source records and aggregate cardinality;
- safe aggregation across time and scopes;
- no cross-tenant activity, strategy, provider, cost, infrastructure, or
  execution inference;
- classification and redaction of every metric descriptor;
- retention, deletion, backup, audit, and cost attribution policy;
- external consumer and deployment compatibility;
- a separate exact capability and authorization decision.

Until that evidence exists, all tenant and external paths remain denied.

## Domain-neutral projection rules

The active summary may contain only bounded semantic aggregates: observation
count, observed rate, relative index, snapshot availability, and fixed
projection metadata. It must not expose `forward_test`, draw counts, hit
levels, structural chance, advantage labels, `v19`, `congelado`, `razon`,
`version`, `fase_actual`, domain identifiers, or exact request time.

No arbitrary source dictionary, free-form source label, phase, reason, tenant,
provider, model, execution, prompt, payload, or strategy field may cross the
projection boundary.

## Retention and support

P1-D does not implement retention, rotation, deletion, backup, support access,
cost attribution, customer support tooling, or incident export. These remain
`FUTURE_CONTRACT_ONLY` and require an Owner-approved contract with independent
tests.

## Explicit non-activation

```text
TENANCY_PRODUCTIVA: NOT_IMPLEMENTED
PUBLIC_EXPOSURE: DEFAULT_DENIED
EXTERNAL_CONSUMER: UNKNOWN_EXTERNAL_EVIDENCE_REQUIRED
METRIC_OWNER: UNKNOWN
RETENTION: FUTURE_CONTRACT_ONLY
P1_D_TENANT_CAPABILITY: INACTIVE
```
