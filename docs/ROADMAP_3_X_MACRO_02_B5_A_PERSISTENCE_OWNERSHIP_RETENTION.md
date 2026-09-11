# Roadmap 3.x Macro-Mission 02: B5-A Persistence Ownership and Retention

`ROADMAP_3X_MACRO_02_B5_A_PERSISTENCE_OWNERSHIP_RETENTION_MATERIALIZED`

This is a read-only ownership matrix. It records what the repository can prove
about persistence families without opening databases, writing product stores,
or choosing an operational deployment policy.

| Family | Owner and root classification | Sensitivity | Retention / write mode | Tenant or deploy semantics | Secret policy | Consumer and recovery |
| --- | --- | --- | --- | --- | --- | --- |
| settings | legacy API/config owner; config roots are product-candidate, not contractually assigned | high; may contain API keys | overwrite-capable candidate; rotation/retention unresolved | deployment/tenant owner unknown | raw secret input must be blocked or isolated; values not read | legacy settings consumers; recovery owner unresolved |
| memory | legacy `memory/manager.py` and configured state file; product/legacy candidate | potentially private operational context | overwrite JSON state; retention/tenant unresolved | deploy path comes from config; tenant semantics absent | secrets must not enter shared memory | legacy orchestration consumers; backup/restore owner unresolved |
| evidence | GOKV `knowledge/global_operational/`; development evidence owner | internal development evidence | append-only items/events/metrics; immutable IDs | repository/development scope, no tenant sharing | no secret values | GOKV validators/compiler; rebuild index or preserve prior evidence |
| logs | legacy logging sinks and audit contracts; concrete deployment sink not proven | may contain request/provider metadata | append-oriented in concept; sink and retention unresolved | deployment owner unknown | redact credentials and private payloads | observability consumers; recovery/rotation owner unresolved |
| metrics | GOKV `knowledge/global_operational/metrics/` for development metrics; product metrics separate and unresolved | operational metadata, possibly sensitive | append-only evidence metrics; product retention unknown | no tenant contract proven | do not record secrets or payloads | GOKV audit and future evaluation; preserve append-only records |
| domains | `domains/` legacy stores are product candidates; sandbox domain materializers are controlled sandbox | domain data may be private/business-sensitive | legacy SQLite/files may overwrite; sandbox manifests are controlled writes | tenant/deploy owner unresolved for legacy; sandbox root explicit | domain secrets prohibited in fixtures and manifests | domain code or sandbox validators; rollback contract for sandbox |
| agents | legacy agent artifacts and runtime-adjacent state; sandbox agent roots are non-operational | prompts, configuration, private context | legacy retention unknown; sandbox artifact manifest controlled | deployment/tenant semantics not established | credentials and private reasoning excluded | agent loaders/materializers; sandbox reset or rollback |
| presets | `core/agent_preset_materializer.py` under sandbox domain root | configuration, may reference capabilities | manifest/history append or controlled update in sandbox | sandbox domain owner; product tenant unresolved | no secret material in preset artifacts | sandbox materializer and manifest validator; remove via rollback contract |
| papers | paper seed/materialization sandbox surface | generated/project content | controlled sandbox artifact writes; legacy persistence unresolved | sandbox root only; no operational tenant proof | secrets excluded from seeds | paper seed materializer; manifest rollback |
| teams | sandbox team materializer and team contracts | team topology/configuration | controlled sandbox manifest writes; lifecycle persistence not operational | sandbox scope; deployment/tenant unknown | no credentials or live membership | team validators/read models; rollback/reset |
| validation | domain validation stores and GOKV validation fields | validation evidence and domain data | legacy in-memory or product candidate; GOKV evidence append-only | domain/deployment ownership unresolved | no secrets in validation evidence | validation code and audit tests; rebuild from source evidence |
| evolution | Loteria evolution structures and future evolution contracts | domain-specific history and derived state | legacy overwrite/append behavior requires owner proof | domain deployment semantics unresolved | secrets excluded | domain evolution consumers; recovery/rollback unresolved |
| learning | GOKV DOOL/OCI events and candidates; runtime learning explicitly absent | development-origin operational knowledge | append-only events/items; lifecycle transition is explicit | repository/development scope only | no private reasoning, conversations, weights, or secrets | GOKV compiler/loop; preserve candidate state and reason if not promoted |

## Ownership conclusions

1. `knowledge/global_operational/` has the strongest current ownership and
   append-only evidence contract, but it remains development-only.
2. Sandbox materializers have explicit root containment and rollback contracts;
   they are not product persistence.
3. Legacy settings, memory, domain databases, logs, and runtime-adjacent
   artifacts remain `OWNER_PROBABLE_NOT_CONTRACTUAL` until deployment, tenant,
   retention, and authorization evidence is produced.
4. No row upgrades a probable owner to a contractual owner. No row authorizes a
   route, provider, runtime, or execution path.

## Boundary

No product store was opened or modified. No SQLite connection, external system,
provider, network, secret, payload, endpoint, UI, or runtime was touched.
