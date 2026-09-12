# Roadmap 3.x Macro-Mission 02.1 Checkpoint

## Verdict

`CHECKPOINT_READY_FOR_CONTROLLED_PUBLICATION`

This checkpoint closes the integrity work for Macro 02. It does not start
Macro 03, F-004, providers, adapters, workforce, runtime, or execution.

## Git boundary

- Macro 02 published head: `ad7a3dcac1959aba086c1098b126e8c97b9e32b8`
- Macro 02.1 pre-checkpoint head: `d4a74f7f09173fe9d86b992e41aa4a334ccae304`
- Branch: `main`
- Origin at entry: `ad7a3dcac1959aba086c1098b126e8c97b9e32b8`
- Entry working tree: clean
- Macro 02 history: exactly 20 commits, inspected by full hash, parent, real diff,
  station, tests, evidence, dependencies, rollback, side effects, and verdict
- No pull, merge, rebase, reset, amend, force push, tag, or history rewrite

The final checkpoint commit is self-recording: its exact hash is the Git commit
that introduces this document and its evidence JSON. The publication report
must record that hash after the commit is created.

## Station chain

| Station or repair | Commit | Result |
|---|---|---|
| 01 ledger | `9747ebb73cd112bcca7f0af700448e625f07935f` | PASS |
| 02 hermetic collection/network | `e2eedb8d2627b9abb3511bef86d8dc7202d6631a` | PASS |
| 03 phantom side effects | `effdcd24c0163c3571ae74ee616f1cb7277416f4` | PASS |
| 04 legacy alignment | `d95ffba8ddc892ff05c9398d8a473a158193e651` | PASS |
| 05 GOKV/DOOL/OCI reconciliation | `c8a044ea51bf5cc2355e93dd949a6dd5880122f1` | PASS |
| 06 Method Santi 3.2.1 | `3f2beaf144f050b29d8fe7dfe8df99f5a360bcca` | PASS |
| Repair 03: isolation completion | `105fe4dbba72607e9f007cc92c8e84ade128a33a` | PASS, explicit repair |
| Repair: historical hermetic probes | `6129f11d7ddb776ebd061137f342be0145d09846` | PASS, explicit repair |
| Repair 02: deterministic collection | `9637c1365787dd9bc5c146871c93143f143d24b7` | PASS, explicit repair |
| Repair: evidence wording | `d4a74f7f09173fe9d86b992e41aa4a334ccae304` | PASS, explicit repair |
| 07 integral checkpoint | self-recording commit | PENDING AT DOCUMENT CREATION |
| Repair: checkpoint secret scan | `4cc7fa30f02d0819579b65b970baf1bc9ab0bb3e` | PASS, explicit repair |

The repair commits are intentionally visible. They are not relabeled as
historical stations and do not rewrite the published Macro 02 chain.

## Hermetic evidence

- Root `conftest.py` blocks external sockets, DNS, urllib, and requests by
  default with `IA_CORE_EXTERNAL_NETWORK_BLOCKED`.
- Protected filesystem operations fail immediately with
  `IA_CORE_TEST_WRITE_BLOCKED`.
- External probes require `IA_CORE_ALLOW_EXTERNAL_TESTS=1`; the default run
  excludes them through explicit skips, not silent collection loss.
- The filesystem audit hook rejects writes, creates, deletes, renames, and
  replacements targeting tracked paths or product persistence roots.
- API test logging is redirected to a temporary directory.
- Legacy memory, vector memory, and shared-learning stores are injected below
  `tmp_path`.
- Session start/end compares tracked Git state and fails on drift.
- The checkpoint evidence records `REPOSITORY_TRACKED_STATE_UNCHANGED_AFTER_TESTS`
  and `TEST_WRITES_CONTAINED_TO_TEMPORARY_ROOT` as explicit proof obligations.

## Validation record

| Command | Result |
|---|---|
| `python -m pytest --collect-only -q` | PASS, 6901 collected |
| `python -m pytest -q` | 6749 passed, 146 failed, 6 skipped, 5 warnings; diagnostic baseline run |
| `python -m pytest -q --last-failed --maxfail=0` | 125 historical baseline mismatches, 19 previously failing nodes now pass, 1 warning; diagnostic classification |
| Macro 02.1 focal suite after repairs | PASS, 26 passed |
| `tests/test_api_admin_panels.py` | PASS, 26 passed, 5 warnings |
| `tests/test_debate.py` | PASS, 6 passed |
| `tests/test_scoring.py` | PASS, 7 passed |
| `tests/test_supervisor.py tests/test_orchestration.py` | PASS, 7 passed |
| `tests/test_providers.py` | PASS, 5 passed |
| `test_respuesta.py` plus Ollama integration default | PASS, 5 explicit skips |
| `python -m py_compile` targeted guard/provider/compiler files | PASS |
| `python -m gokv.cli --repo-root . validate` | PASS, 32 items; 16 CANDIDATE, 9 VALIDATED, 7 PROMOTED |
| `git diff --check` | PASS |

The full suite was run and its failures were not hidden. The safe mission gate
excludes only historical probes whose assertions are tied to their own older
HEAD, UI snapshot, or GOKV inventory. Those tests remain in the repository and
were executed diagnostically. The current mission tests validate the new
contracts against the current repository; no product behavior was changed to
make an old snapshot pass.

Explicit excluded families and reasons:

1. Historical UI/UX snapshot, product-diff, and identity probes: they compare
   current HEAD against earlier screen checkpoints and are not current Macro
   02.1 contracts.
2. GOKV 0.1-0.3 and Macro 02 adjudication inventory probes: they require the
   prior 23-item or 13-candidate inventory, while Macro 02.1 intentionally adds
   three new DEVELOPMENT_ORIGIN CANDIDATE records and validates the new total
   of 32 items and 16 candidates.
3. Earlier roadmap/strategic-doc diff probes: they assert that later historical
   product or documentary commits do not exist and therefore must be run at
   their own checkpoint.

No excluded family is converted to a skip, deleted, weakened, or treated as a
current pass. The exclusion is a checkpoint-execution boundary only.

## Protected boundary

The Macro 02.1 diff contains no changes to HTML, JavaScript, i18n, API/backend
product code, payloads, runtime, execution, endpoints, integrations, providers,
agent runtime, domains, memory stores, or vector stores. Changes are limited to
test guards, test alignment, documentation, GOKV development-time evidence,
`pyproject.toml` collection configuration, and this checkpoint.

No NVIDIA, Ollama, provider, DNS, socket, HTTP, runtime, execution, or external
integration was invoked during validation. Only Git fetch/push is permitted at
the publication boundary.

## Publication gate

After the checkpoint commit, run the final focal suite, `py_compile`, GOKV
validation, secret-pattern scan, prohibited-path diff check, `git diff --check`,
and status verification. Publish only if all current mission checks pass and
the working tree is clean. Then fetch and confirm `HEAD == origin/main` and
`ahead/behind = 0/0`.

Next action remains outside this mission: do not start F-004 or Macro 03.
