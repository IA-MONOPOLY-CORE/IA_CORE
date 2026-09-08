# Roadmap 3.0 N0 - Backend Surface Census

## Gate

`ROADMAP_3_0_N0_BACKEND_SURFACE_CENSUS_PASSED`

## Scope and method

This is a static, read-only census performed from the Roadmap 3.0 baseline
`82d309f00ab99dfa9eb100e5594bf1d8d0559f5a`. It inventories source presence,
not activation. Tests, documentation, fixtures, and the GOKV vault are counted
separately from product source. No server, provider, model, worker, scheduler,
queue, tool, integration, or filesystem mutation was started.

## Repository surface

| Surface | Files | Python | JSON | Classification |
| --- | ---: | ---: | ---: | --- |
| `core/` | 132 | 131 | 0 | mixed contracts, legacy services, sandbox and stores |
| `agents/` | 17 | 17 | 0 | callable agent definitions and runners |
| `providers/` | 12 | 12 | 0 | provider adapters and registry |
| `domains/` | 26 | 15 | 9 | domain definitions, legacy loteria and preset data |
| `catalogs/` | 8 | 0 | 7 | definitions and catalog inputs |
| `memory/`, `memoria_*`, `logs/`, `data/` | 51 | 7 | 35 | persistence and evidence surfaces |
| `tests/` | 594 | 585 | 9 | test-only surface, excluded from product reachability |
| `knowledge/`, `gokv/` | 129 | 14 | 110 | documentary/knowledge and validators |
| `api.py`, `config.py`, `tools/`, `scripts/`, `ui/` | 53 | 33 | 1 | API, config, helpers, scripts and UI boundary |
| **Repository total** | **1,598** | **802** | **179** | excludes cache/virtualenv directories |

The non-test Python surface is 217 files. The counts above are census evidence,
not a claim that every file is reachable from the API.

## Surface classification

| Family | Representative paths | Read/write or activation finding |
| --- | --- | --- |
| API and legacy application entry | `api.py`, `core/supervisor.py`, `agents/manager.py` | callable when the application is started; includes mutation routes and legacy orchestration |
| Internal contract plane | `core/*_contract.py`, `core/*_schema.py`, `core/backend_internal_*` | predominantly contract/read-model code; explicit deny-by-default gates appear in several modules |
| Sandbox materialization | `core/domain_materializer.py`, `core/agent_preset_materializer.py`, `core/paper_seed_materializer.py`, `core/sandbox_team_materializer.py` | writes only to validated sandbox paths when called; operational roots are rejected |
| Runtime/execution preparation | `core/runtime_activation_gate.py`, `core/attempt_factory.py`, `core/execution_runner.py`, `core/active_executor.py` | source exists; dedicated runtime/execution flags are disabled or dry-run/gated |
| Providers and network | `providers/nvidia_provider.py`, `providers/ollama_provider.py`, `core/herramientas.py`, `core/hybrid/connectivity.py` | network-capable code exists; no provider/network call was made in this audit |
| Agents and domain data | `agents/`, `domains/loteria/agent_presets.json`, `catalogs/` | definitions and legacy JSON are present; sandbox/domain activation remains conditional |
| Operational persistence candidates | `api.py`, `core/memoria_perpetua.py`, `core/supervisor.py`, `domains/loteria/database_loteria.py` | static write paths exist and require a separate reachability/security audit |
| Audit/knowledge only | `docs/`, `knowledge/global_operational/`, `gokv/` | evidence and validators; not operational application state |

## Static side-effect inventory

The scan found 60 non-test write/side-effect candidates across 30 Python files:
24 `json.dump`, 13 `open(..., "w")`, 11 `shutil.rmtree`, 4
`sqlite3.connect`, 3 SQL `cursor.execute`, 1 `shutil.move`, 1 `open(..., "x")`,
1 `subprocess.run`, 1 `os.replace`, and 1 `subprocess.check_output`.
Serialization via `json.dumps` and ordinary reads are excluded from this total.
This is a candidate count, not proof that all candidates are reachable.

The scan found 9 conservative network-capable references in non-test source,
covering requests/urllib/socket/provider registry/helper paths. No network call
was executed. Dangerous primitive presence is limited to 13 static calls,
including `shutil.rmtree` and two subprocess families; no exploitation was
attempted.

## N0 conclusion

The backend is not empty and is not a single homogeneous runtime. It contains a
legacy callable application path, a broad contract/read-model plane, sandbox
materializers, disabled/dry-run runtime preparation, and provider/network code.
The next stations must therefore distinguish source existence, caller reachability,
activation gates, and side effects instead of treating file presence as runtime.

