# Roadmap 4.x Macro-Mission 04.1

## Ecosystem inheritance, privacy and recovery

## Two planes

`GLOBAL_INHERITABLE_CAPABILITY_PLANE`

The global plane may contain distilled, sanitized, versioned, authorized and
compatible capability with provenance. It may include successful patterns,
failed approaches, limits, contradictions, recovery strategies and model-fit
conditions. It does not contain raw enterprise material.

`ENTERPRISE_CONFIDENTIAL_PLANE`

The enterprise plane retains raw data, secrets, credentials, positions,
exclusive strategy, PII, private memory and any content that identifies or
exposes a tenant. It is not an OCI inheritance source by default.

The transfer from enterprise experience to the global plane is a future,
explicit, auditable and one-way extraction into safe abstractions. It never
copies secrets or private content between enterprises.

Required invariants:

- `GLOBAL_LEARNING_NEVER_EQUALS_RAW_TENANT_DATA_SHARING`;
- `ENTERPRISE_SECRETS_REMAIN_ENTERPRISE_EXCLUSIVE`;
- `INHERIT_CAPABILITY_NOT_CONFIDENTIAL_CONTENT`.

## Owner-native identity

The future Enterprise Foundry may identify an enterprise with:

```text
enterprise_ownership_class: OWNER_NATIVE
enterprise_genesis: OWNER_CREATED | AGENT_FOUNDED_UNDER_OWNER_CHARTER
```

This is durable ownership metadata, not a read grant. `OWNER_NATIVE` cannot
bypass tenant isolation, reveal secrets, inherit private content or authorize
external execution.

## Authority without universal visibility

The Owner retains maximum governance authority over IA_CORE. That authority
does not imply unilateral plaintext visibility into enterprise secrets. A
future governance surface may manage lifecycle, infrastructure and encrypted
backup recovery while preserving content boundaries.

`MAXIMUM_GOVERNANCE_AUTHORITY_WITHOUT_UNIVERSAL_CONTENT_VISIBILITY`

`GLOBAL_ROOT_DOES_NOT_IMPLY_TENANT_SECRET_READ`

Agents should consume secrets through bounded adapters/capabilities under a
future approved contract, never as raw prompt content. No such adapter is
created here.

## Recovery contract

`HUMAN_MEMORY_IS_NOT_A_RECOVERY_DEPENDENCY`

`RECOVERY_MUST_BE_TESTED_NOT_ASSUMED`

`NO_SINGLE_PARTY_CAN_RECOVER_AND_DECRYPT_ALONE`

`RECOVERY_WITHOUT_PLAINTEXT_VISIBILITY`

Future evaluation may compare quorum, key fragmentation and multiple-custody
options. This mission chooses and implements none of them. Recovery must
distinguish lost device from compromised device, support revocation, preserve
audit evidence and never restore revoked permissions or cross tenant limits.
An encrypted backup is not proof of restore; a restore test is not permission
to expose content.

## Current boundary

The current repository has future strategic recovery/access documents and
development-only GOKV privacy classes. It has no demonstrated production
tenant recovery or universal secret visibility contract. Accordingly, all
future recovery and enterprise transfer capabilities remain
`PREPARED_NOT_STARTED`; no secrets, tenant stores, backups or external systems
were read or changed.
