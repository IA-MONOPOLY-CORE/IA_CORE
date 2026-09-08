# GOKV 0.3 - PROMOTED_ONLY Evaluation

## N5 gate

`N5_GOKV_PROMOTED_ONLY_FIRST_REAL_PACK_PASSED`

All packs below are development-only compile artifacts. No mission was
executed, no model/provider was invoked, and no runtime, payload, endpoint or
integration was activated.

## Deterministic general comparison

Request fixture:
`knowledge/global_operational/requests/gokv_0_3_general_capability_comparison.json`.
The allowlist contains the seven promoted items plus `conditioned_autonomy`.

| field | PROMOTED_ONLY | DEVELOPMENT_VALIDATED |
|---|---|---|
| pack ID | `gokv.pack.85b7bddb034cdc7c` | `gokv.pack.c134f9a6da1aad99` |
| pack size | 7 items / 9690 bytes | 8 items / 10759 bytes |
| available promoted | 7 | 7 |
| selected promoted | 7 | 7 |
| validated excluded by mode | `conditioned_autonomy` | none |
| candidate excluded | 7 global candidates | 7 global candidates |
| conflicts | 0 | 0 |
| runtime/execution/payload | false/false/false | false/false/false |

`PROMOTED_ONLY` returns all seven promoted items for this deterministic
allowlist. `DEVELOPMENT_VALIDATED` adds exactly one item:
`conditioned_autonomy`.

## UI/UX 1.202 equivalent comparison

Request fixture:
`knowledge/global_operational/requests/gokv_0_3_ui_ux_1_202_comparison.json`.
This is a compile request only; it does not execute UI/UX 1.202.

| field | PROMOTED_ONLY | DEVELOPMENT_VALIDATED |
|---|---|---|
| pack ID | `gokv.pack.c886fbab561dee9a` | `gokv.pack.247d953d36141636` |
| pack size | 6 items / 8432 bytes | 7 items / 9501 bytes |
| available promoted | 6 | 6 |
| selected promoted | 6 | 6 |
| validated selected | 0 | `conditioned_autonomy` |
| validated excluded by mode | `conditioned_autonomy` | none |
| promoted excluded by mission allowlist | `compress_occurrences_into_decisions` | same |
| candidate excluded | 7 global candidates | 7 global candidates |
| conflicts | 0 | 0 |

The six selected promoted items are:

```text
evidence_before_closure
focal_group_canonical_deep_test_policy
preserve_contract_until_explicit_change
real_diff_over_planned_commit_name
station_local_commits
true_hard_frontier
```

The previous development pack ID `gokv.pack.247d953d36141636` is preserved as
historical context but is not assumed to be the new post-promotion pack. The
new promoted-only pack is `gokv.pack.c886fbab561dee9a`.

## Sufficiency decision

For the known UI/UX 1.202 scope, `PROMOTED_ONLY` is sufficient for the six
deterministic read-only/test-only stations already defined by UI/UX 1.201:
continuity and diff inspection, CSS cascade inventory, responsive/resize
audit, visible accessibility review, protected-surface preservation and
checkpoint/manifest preparation.

The absence of `conditioned_autonomy` is not critical for this specific
read-only mission because the mission contract already explicitly forbids
product, contract, backend, payload, runtime, execution, endpoint and
integration changes and defines the hard frontier. It is still critical as a
general autonomy capability: it is not silently promoted, and it must not be
treated as present in `PROMOTED_ONLY`.

The exact capacity gap is therefore:

```text
PROMOTED_ONLY: no conditioned_autonomy
DEVELOPMENT_VALIDATED: conditioned_autonomy available explicitly
```

If UI/UX 1.202 changes from read-only audit/preparation into a new
authorization, contract, semantic, product or runtime decision, this
sufficiency conclusion expires and the mission must stop for Direction rather
than infer permission. For the current known scope, the recommended mode is
`PROMOTED_ONLY`.
