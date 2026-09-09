# Roadmap 3.x Macro-Mission 01

## Security Boundary + Legacy API Disposition + Canonical Alignment

Mission ID: `roadmap_3x_macro_01_security_legacy_canonical_alignment`

Baseline: `f87dbb963dacaa9a4a358da816ad78d55d37cdd8`

Authorized path: `B-1 -> B-2 -> B-3`, maximum three contiguous blocks.

Actual path: `B-1 PASS -> B-2 BLOCKED at F-004 -> B-3 NOT ENTERED`.

## Authority reconstruction

The current 3.x graph authorizes deterministic contract-preserving work inside
B-1/B-2/B-3, but does not authorize a new identity system, deployment, runtime,
provider, agent or operational store. Direction supplied `TRUST_MODEL_V1` and
the six legacy destinations. It did not select a concrete bridge, owner,
successor or retirement path for all live legacy routes.

The historical ZIP remains excluded. Git, current source, published 3.x graph,
Roadmap 3.2 route evidence and current canonical contracts remain authoritative
in that order.

## B-1 result

`LEGACY_EXPOSURE_SECURITY_BOUNDARY_DECISION = PASS`

- F-001: local startup evidence exists (`start_api.bat` uses localhost:8000
  documentation and binds 0.0.0.0:8000 when started); no current API process or
  8000 listener was observed; external deployment/traffic remains unknown.
- F-002: `TRUST_MODEL_V1` is enforced in `api.py`. Wildcard origins, methods and
  headers are gone. The default is `http://localhost:8000`; an explicit
  `IA_CORE_CORS_ALLOW_ORIGINS` list is accepted; wildcard or invalid values
  fail closed; credentials remain disabled.
- Identity/auth/authz/ownership/tenant: not demonstrated route-locally and not
  invented. This remains a separate frontier.
- F-003: raw `api_key` input is rejected before settings writes; persisted
  legacy `api_key` fields are removed from GET responses; no key is written to
  `config.py` by this route. Non-secret settings ownership and route auth remain
  unresolved.

## B-2 result

`LEGACY_CANONICAL_DESTINATION_CONTRACT = BLOCKED`

All 36 routes have an explicit disposition record, but all remain `UNKNOWN`.
That is a complete and honest classification, not a missing row. The current
evidence does not prove the owner, external consumer boundary, canonical
successor, semantic equivalence or retirement preconditions needed for a
non-UNKNOWN destination. See the complete table in
`ROADMAP_3_X_LEGACY_ROUTE_DISPOSITION.md`.

The true hard frontier is `F-004`: selecting a bridge, containment, successor
or retirement authority for the live legacy surface requires Direction/Architect
input. No route was removed, migrated, wrapped or exposed as internal-only.

## B-3 result

`NOT_ENTERED_DUE_TO_B_2_TRUE_HARD_FRONTIER`

Coverage remains `0 covered / 1 partial / 2 legacy bypass / 33 not demonstrated
/ 0 not applicable`. The security piece does not create canonical coverage.

## Piece records

| Piece | Routes | Commit | Tests | Rollback |
| --- | --- | --- | --- | --- |
| `PIECE_CORS_AND_SETTINGS_SECRET_BOUNDARY` | CORS middleware; POST/GET `/api/settings` | `be5986e0` | Macro focal + historical 3.1/3.2: `29 passed`; `py_compile` pass | None |
| `PIECE_LEGACY_ROUTE_DISPOSITION` | All 36 routes | Pending checkpoint commit | Evidence/manifest guards pending final run | None |

## Learning gate

`PIECE_CORS_AND_SETTINGS_SECRET_BOUNDARY` produced `OBSERVED`, not promoted:

- Pattern: historical security guards must read their published checkpoint
  source rather than the mutable current product source.
- Evidence: guards now use `git show FINAL_CHECKPOINT:api.py` and no longer
  include the current working tree in historical diff assertions.
- Reuse: apply to later checkpoint-bound guards before any product mutation.
- Failure mode: current-source assertions retroactively fail when an approved
  security change removes the historical condition.
- Stop condition: do not broaden the guard to accept weakened security; keep
  the original checkpoint assertions intact.
- Provenance: Roadmap 3.1/3.2 published guard scope and this macro focal test.

GOKV/DOOL intake: no new promotion or vault item. The learning remains in this
mission evidence until governance review.

## Protected boundaries

No provider/runtime/agent execution, external service call, model invocation,
network operation, deployment action, UI redesign, new endpoint, new identity
system, API v2, business semantic or B-4/B-5/B-6/B-7 work occurred.
