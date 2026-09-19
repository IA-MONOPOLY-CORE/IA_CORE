# Roadmap 4.x Macro-Mission 05 - P1 Adversarial Assurance Contract

## Contract status

```text
CONTRACT: P1_POST_BOUNDARY_E2E_ADVERSARIAL_ASSURANCE_V1
ROUTES: EXACTLY_FOUR_GET_ROUTES
CAPABILITY_CONFUSION: BLOCKED
CLIENT_CONTROLLED_IDENTITY: BLOCKED
ZERO_SOURCE_READ_ON_DENY: REQUIRED
TENANT_INFERENCE: BLOCKED
SANITIZATION: ALLOWLIST_FIRST
BOUNDEDNESS: REQUIRED
SIDE_EFFECTS: ZERO
EXTERNAL_EXPOSURE: DEFAULT_DENIED
PRODUCT_REPAIR: NONE_UNTIL_RED_EVIDENCE
```

## Required adversarial groups

1. Route inventory and method misuse: four P1 GET routes only; other methods
   remain absent or 405; no new alias, raw view or endpoint.
2. Client identity substitution: user, tenant, capability, authorization,
   forwarding, Origin, Host, User-Agent, loopback and body values never grant
   access.
3. Malformed principal and audience: invalid type, unauthenticated state,
   whitespace, casing, newline, wrong audience and tenant-shaped principal
   fail closed.
4. Cross-capability substitution: every active capability is rejected by all
   non-owning families; future tenant capabilities never activate.
5. Zero source read: spies, counters and explosive fakes prove authorization,
   query and scope denials occur before builders, stores, log files, Loteria,
   evolution or V19 reads.
6. Tenant non-enumeration: absent, foreign, malformed and client-selected
   tenant scope reveal no identifier, existence, size, path, store or data.
7. Sanitization: synthetic secrets, PII, paths, URLs with credentials,
   tracebacks, prompts, payloads, providers, models, tools, tenant IDs,
   controls and unknown fields never cross the allowlist.
8. Bounded determinism: each contract maximum is measured, equivalent source
   snapshots produce deterministic shapes, and limits are not approximate.
9. Request isolation: an authorized request, denials, another family,
   malformed principal and resolver failure cannot contaminate later requests.
10. Side effects: providers, network, writes, mutations, runtime, execution,
    model loading, promotions, evolution changes and store writes are zero.
11. Consumers: current Overview, Hybrid, Memory and Logs consumers remain
    compatible; dynamic metrics has no UI consumer.

## Stop conditions

Any reproducible product defect must be preserved as red evidence and repaired
only in the explicitly authorized P1 files. A tooling or historical mismatch
must not be relabeled as product success. Any conflicting historical evidence
or unsafe JSON duplicate value blocks closure.
