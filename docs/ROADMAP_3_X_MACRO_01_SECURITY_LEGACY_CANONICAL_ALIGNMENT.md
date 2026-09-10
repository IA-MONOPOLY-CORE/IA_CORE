# Roadmap 3.x Macro-Mission 01

## Security Boundary + Legacy API Disposition + Canonical Alignment

Mission ID: `roadmap_3x_macro_01_security_legacy_canonical_alignment`

Baseline: `f87dbb963dacaa9a4a358da816ad78d55d37cdd8`

Authorized path: `B-1 -> B-2 -> B-3`, maximum three contiguous blocks.

Actual path: `B-1 PASS -> B-2 PASS_UNKNOWN_QUALITY_GATE -> B-3 PASS`.

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

`LEGACY_CANONICAL_DESTINATION_CONTRACT = PASS_UNKNOWN_QUALITY_GATE`

All 36 routes have an explicit disposition record, and all remain `UNKNOWN`
after route-specific reconnaissance because the evidence is insufficient for a
non-UNKNOWN destination. This is a quality-gated classification, not a missing
row. See the complete route table and the per-route evidence in
`ROADMAP_3_X_LEGACY_ROUTE_DISPOSITION.md` and
`ROADMAP_3_X_MACRO_01_ROUTE_RECONNAISSANCE.md`.

F-004 was recalculated from an undifferentiated true-hard stop to a
route-specific conditional frontier. No route was removed, migrated, wrapped
or exposed as internal-only.

## B-3 result

`CONTROL_PLANE_COVERAGE_CONTRACT = PASS_EXPLICIT_CONTRACT_ONLY_UNALIGNED_LEGACY_SURFACE`

Coverage remains `0 covered / 1 partial / 2 legacy bypass / 33 not demonstrated
/ 0 not applicable`. B-3 explicitly proves that canonical contracts are not
route authority and that no safe semantic-equivalent adapter was demonstrated.
See `ROADMAP_3_X_MACRO_01_B3_COVERAGE.md`.

## Piece records

| Piece | Routes | Commit | Tests | Rollback |
| --- | --- | --- | --- | --- |
| `PIECE_CORS_AND_SETTINGS_SECRET_BOUNDARY` | CORS middleware; POST/GET `/api/settings` | `be5986e0` | Macro focal + historical 3.1/3.2: `29 passed`; `py_compile` pass | None |
| `PIECE_LEGACY_ROUTE_RECONNAISSANCE` | All 36 routes grouped into 9 coherent pieces | `5fb0469` | Macro focal + historical 3.1/3.2: `32 passed` | None |
| `PIECE_B3_CONTROL_PLANE_COVERAGE` | Canonical contract provenance and negative bypass checks | Pending closure commit | Canonical contract focal suite plus macro guards | None |

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
