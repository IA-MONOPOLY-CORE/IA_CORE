# Roadmap 3.0 N2 - Persistence and Side-Effect Graph

## Gate

`ROADMAP_3_0_N2_PERSISTENCE_SIDE_EFFECT_GRAPH_PASSED`

## Static result

The non-test source scan found **60 write/side-effect candidates in 30 Python
files**. The total counts operations that can mutate state or invoke a process;
it excludes `json.dumps` serialization and ordinary file reads.

| Primitive | Candidates |
| --- | ---: |
| `json.dump` | 24 |
| `open(..., "w")` | 13 |
| `shutil.rmtree` | 11 |
| `sqlite3.connect` | 4 |
| SQL `cursor.execute` | 3 |
| `shutil.move` | 1 |
| `open(..., "x")` | 1 |
| `subprocess.run` | 1 |
| `os.replace` | 1 |
| `subprocess.check_output` | 1 |
| **Total** | **60** |

## Write graph

| Node/family | Representative paths | Classification | Boundary |
| --- | --- | --- | --- |
| API settings and agent/domain handlers | `api.py` | potential operational write | route callable if server is started; no auth evidence |
| legacy memory/orchestration | `core/memoria_perpetua.py`, `core/supervisor.py` | potential operational write | reachable from legacy chat/orchestration path |
| legacy domain database | `domains/loteria/database_loteria.py` | potential operational write | SQLite lifecycle; reachability depends on legacy domain flow |
| sandbox domain/artifact materializers | `core/domain_materializer.py`, `core/agent_preset_materializer.py`, `core/paper_seed_materializer.py` | controlled sandbox write | path validation rejects operational domain roots |
| sandbox agents/teams | `core/sandbox_agent_materializer.py`, `core/sandbox_team_materializer.py` | controlled sandbox write | declarative, non-operational artifact manifest and rollback metadata |
| backend-internal lifecycle/rollback services | `core/backend_internal_*`, `core/*rollback*.py` | controlled/internal write candidate | explicit service contract and confirmation/gate requirements |
| execution stores and projections | `core/*execution*store*.py`, `core/*result*store*.py` | contract-only or gated write | runtime/execution flags and write-safe contracts remain disabled/gated |
| GOKV vault | `knowledge/global_operational/`, `gokv/` | development-origin evidence write | this mission may append evidence only; not product state |
| scripts and tests | `scripts/`, `tests/` | test/tooling-only write | excluded from operational reachability |

## Filesystem and ownership findings

- Sandbox materializers resolve target paths and reject operational domain paths;
  they produce manifests, versions, rollback paths and `operational: false`
  metadata when used in their intended boundary.
- The API's settings route accepts an API key and writes configuration. This is
  a real secret-bearing side-effect candidate and is not protected by evidence
  of route authentication in this repository.
- Agent/domain create, update, delete and paper regeneration routes expose
  JSON/filesystem mutation candidates. `DELETE` includes a `rmtree` path.
- Memory and orchestration records are not the same ownership class as GOKV
  evidence. The former belong to legacy application state; the latter belongs
  to development-origin audit history.
- The audit did not create, modify, delete, rename, or migrate any product
  filesystem path. No SQLite connection was opened.

## N2 conclusion

The repository has a meaningful write surface. The strongest static boundary is
the sandbox path rejection and contract gates; the weakest visible boundary is
the legacy API mutation surface, especially settings/secrets and delete paths.
Reachability and authorization must be resolved before a runtime or execution
mission can be considered safe.

