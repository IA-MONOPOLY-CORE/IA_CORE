# Roadmap 3.x Macro-Mission 02.1 Phantom Side-Effect Containment

## Historical finding

Macro 02 reported four repository paths changed during the safe historical
test run. The tree was restored afterward, but restoration is not evidence that
the run was side-effect free. The exact paths and call chains were:

| Path | Responsible flow | Call chain | Classification |
|---|---|---|---|
| `memoria_agentes/analyst/memoria.json` | `tests/test_scoring.py::test_orchestrate_role_agents_with_scores` | `Supervisor.orchestrate` -> role agent execution -> `RuntimeJsonAgent.run` -> `core.memoria_perpetua.cargar_memoria` / `guardar_memoria` | Agent memory state |
| `memoria_agentes/critic/memoria.json` | `tests/test_scoring.py::test_orchestrate_role_agents_with_scores` | Same role-agent learning path, for `critic` | Agent memory state |
| `memoria_agentes/optimizer/memoria.json` | `tests/test_scoring.py::test_orchestrate_role_agents_with_scores` | Same role-agent learning path, for `optimizer` | Agent memory state |
| `memory/herramientas_compartidas.json` | `tests/test_debate.py::test_debate_detects_contradiction_on_critic` | `Supervisor.orchestrate` -> `_registrar_aprendizaje_post_debate` -> contradiction persistence | Shared learning/evidence state |

The first three paths are product-style agent memory stores reached by a test
that used real JSON agents with mocked LLM responses. The fourth is a relative
shared-learning store reached when the mock critic creates a contradiction.
These are not fixtures, and they must not be changed as normal test output.

## Enforced boundary

The root `conftest.py` is loaded before repository test modules. Its audit hook
rejects writes, creates, deletes, renames, and replacements targeting tracked
files or protected product persistence roots. A rejected operation raises
`IA_CORE_TEST_WRITE_BLOCKED` immediately.

The test `tests/conftest.py` injects a per-test temporary root for legacy
persistence helpers, redirects the shared memory state and tool store, patches
the supervisor's relative shared-learning path, and redirects JSON and vector
memory roots. The root guard also redirects API test logging to a temporary
directory. Consequently, permitted test writes occur below `tmp_path` and
cannot reach the repository stores; the fixture does not change the working
directory, preserving relative UI/document test paths.

The root session hooks capture Git tracked-state status at session start and
compare it at session finish. A changed tracked state forces a failing test
session and emits `IA_CORE_REPOSITORY_TRACKED_STATE_CHANGED_DURING_TESTS`.

## Proof obligations

- `REPOSITORY_TRACKED_STATE_UNCHANGED_AFTER_TESTS` is satisfied by the session
  status comparison and the focused side-effect tests.
- `TEST_WRITES_CONTAINED_TO_TEMPORARY_ROOT` is satisfied by the injected paths
  and the focused temporary-root assertion.
- A direct attempt to write a protected path fails before the file operation.
- The product runtime was not changed to accommodate the test; only test
  isolation and test-boundary infrastructure were changed.
