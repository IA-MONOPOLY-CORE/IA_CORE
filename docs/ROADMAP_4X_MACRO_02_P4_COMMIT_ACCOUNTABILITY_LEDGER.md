# Roadmap 4.x Macro-Mission 02 - P4 Accountability Ledger

## Live ledger state

- Result: `ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`.
- Baseline: `3c90529abf5e130624653a247084d773d6620dcb`.
- Branch: `main`.
- `VALIDATION_BASIS_HEAD`: `4a8b6a381a5c57e55286e4cd784a1e7f967996bd`.
- External exposure: `DEFAULT_DENIED`.
- Production readiness: `NOT_AUTHORIZED`.
- Macro-Mission 03: `NOT_STARTED`.
- Material station policy: `ONE_MATERIAL_STATION_ONE_COMMIT`.

Each implementation or test station below has one independent commit. Station
5 required no repository change because GOKV/DOOL/OCI produced
`NO_NEW_CANDIDATE`.

## Station ledger

| Station | Commit | Responsibility | Files / result | Verdict |
| --- | --- | --- | --- | --- |
| 1 | `7bb08015e31c8a89ced143acd8b659f685428ee0` | Direction acceptance, reconciled plan and dual gate matrix | Three P4 roadmap documents; internal/external dimensions separated | PASS |
| 2 | `91d911af226bade30dad5d2d83182678d8d03963` | Pure human access boundary | `core/p4_request_access.py` and unit tests; fail-closed resolver and sanitizer | PASS |
| 3 | `7e8416179c4e7cb14ba6fa92c62bd7539567ccd0` | Exclusive P4 wiring | `api.py` only on the seven handlers; filtering, authorization and sanitization | PASS |
| 4 | `9898af723d449126ce46934fdf60a4106c22cc90` | Historical compatibility | Controlled dependency overrides and exact historical allowlists; assertions retained | PASS |
| 4R | `d273c77523b04a232405b31e388e18c0f6a884a8` | Route census continuity repair | Historical route census tolerates legitimate line displacement while preserving method/path/function | PASS |
| 4R2 | `4a8b6a381a5c57e55286e4cd784a1e7f967996bd` | Historical allowlist continuity repair | Macro 01.1 accepts the exact route-census test touched by this mission | PASS |
| 5 | no commit | GOKV/DOOL/OCI consultation | `NO_NEW_CANDIDATE`; vault unchanged and no promotion | PASS |
| 6/7 | documentary closeout reference | Checkpoint, evidence, ledger, README and index; Level B after closeout | Documentary-only publication station; containing hash is verified externally | PASS after publication |

## Validation basis and repairs

The immutable Level A basis is `4a8b6a381a5c57e55286e4cd784a1e7f967996bd`:

- `6986 passed, 6 skipped, 5 warnings` in `1537.34 s` for the full suite.
- `20 passed` in the Macro 02 focal access/remediation suites.
- `27 passed` in the historical relevant replay.
- `18 passed` in catalog/domain compatibility tests.
- `11 passed` in route census replay.
- `20 passed, 1 warning` in secret policy.
- JSON parse, Python compile, Node checks, CORS comparison, protected diff and
  `git diff --check`: PASS.

The first two full-suite replays exposed only historical guard/allowlist
continuity mismatches caused by legitimate file and line displacement. The
repairs were exact and local: no assertion was deleted, no global guard was
relaxed, and no product/protected surface was broadened. The third replay is
the valid green basis.

## Protected surface accounting

The six-commit implementation/test range changes only `api.py`, one P4 core
module, approved tests, the reconciled plan and Direction/gate documents. It
does not change HTML, CSS, contractual JavaScript, i18n, unrelated backend,
payload v2, runtime, execution, endpoints, integrations, providers, secrets,
productive stores, P0, P1, P3, widgets or Request Draft Panel. CORS is bytewise
preserved against the baseline comparison used for this mission.

## Stable publication accounting

The evidence intentionally uses role references rather than a precomputed
self-hash:

- `VALIDATION_BASIS_HEAD` is the exact full-suite-tested code/test candidate.
- `DOCUMENTARY_CLOSEOUT_COMMIT` is identified after the documentation-only
  commit is created.
- `POST_FETCH_PUBLICATION_VERIFICATION` is identified after normal push and
  fetch confirm the remote state.

This is the repository's `publication_metadata_must_not_chase_its_own_head`
protocol. No amend, rebase, merge, reset, squash, tag, force-push or history
rewrite is part of this ledger.

`ROADMAP_4X_MACRO_02_P4_BOUNDED_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
