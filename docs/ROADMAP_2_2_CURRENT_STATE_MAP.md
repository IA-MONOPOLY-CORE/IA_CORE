# Roadmap 2.2 - Current State Map

## Gate

ROADMAP_2_2_CURRENT_STATE_MAP_PASSED

## Reading rule

This map distinguishes source presence, controlled behavior, read-only
contracts, sandbox writes and future documentation. `REAL_ACTIVE` means that a
source surface or route exists in the repository; it does not mean that a
server, provider or runtime was started by this mission.

## Current state by layer

| component | classification | evidence | current truth | risk | debt | audit required in 3.x | priority |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UI/UX contract-aware console | REAL_READ_ONLY | `ui/web/index.html`, 1.204 checkpoint | Four FSC surfaces, widgets and Request Draft are documentary/read-only | Contract confusion if extended | Historical snapshots | Verify backend/UI boundary only | P0 |
| FastAPI application and legacy routes | REAL_ACTIVE | `api.py` route decorators and write handlers | Routes and mutation code exist in source; server was not started | High boundary ambiguity | Legacy route and write surface | Full route, side-effect and auth inventory | P0 |
| Legacy orchestration/domain services | REAL_ACTIVE | `api.py`, `core/orchestration.py`, `domains/` | Existing application code and domain flows remain in repository | High if confused with pre-operational core | Historical coupling | Trace entry points and writes | P0 |
| Internal UI contract | REAL_CONTROLLED | `core/backend_internal_ui_contract.py`, tests 7.0/7.7 | Contract and JSON-safe boundaries exist; not public API | Payload/endpoint leakage | Long contract history | Verify exposure boundary | P1 |
| Internal backend read model | REAL_READ_ONLY | `core/internal_backend_read_model.py` and E2E tests | Read-only snapshot path with no public dashboard adapter | Misread as operational read model | Future persistence | Inventory consumers and storage | P1 |
| Domain status/list services | REAL_READ_ONLY | `core/backend_internal_domain_status_service.py` | Explicit sandbox-root read-only listing and status payloads | Operational-domain confusion | Deferred integration | Check roots and consumers | P1 |
| Preview and validation services | REAL_READ_ONLY | preview/validate modules and tests | Preview/no-write and validation-only contracts exist | Preview mistaken for materialization | Documentation drift | Boundary inventory | P1 |
| Sandbox materialization | REAL_SANDBOX | `core/domain_materializer.py`, artifact modules | Controlled writes are scoped to explicit sandbox roots | Path escape or product-domain mutation | Scale and fixture debt | Audit path safety and manifests | P0 |
| Sandbox rollback/regeneration | REAL_SANDBOX | rollback/lifecycle modules and E2E tests | Rollback and regeneration exist for sandbox artifacts | False equivalence with operational rollback | Benchmark debt | Verify idempotency and scope | P0 |
| Sandbox agents, presets, papers and teams | REAL_SANDBOX | `core/sandbox_*`, generators, team tests | Materialized sandbox structures exist without runtime authority | Active-agent confusion | Naming and fixture complexity | Audit lineage and activation gates | P1 |
| Runtime governance/state contracts | REAL_CONTROLLED | runtime contract modules and tests | Contract-only/pre-operational flags exist; runtime activation is not established by this map | Premature activation | Verbose historical chain | Audit all enablement flags | P0 |
| Execution intent/attempt/lifecycle | REAL_CONTROLLED | execution modules and preflight tests | Preflight/prepare-only and contract surfaces exist; operational execution truth remains unresolved | Major boundary risk | Historical naming drift | First 3.0 frontier | P0 |
| History and result projections | REAL_READ_ONLY | history view/result projection modules | Derived/read-only views exist; no conclusion about operational result store | Store confusion | Deferred persistence | Verify source and mutability | P1 |
| Providers and provider registry | REAL_ACTIVE | `providers/` adapters and registry | Provider adapter source and network-capable paths exist; no provider invoked here | External access and secrets | External suite policy exclusions | Full provider invocation audit | P0 |
| Tools/network helpers | REAL_ACTIVE | `core/herramientas.py`, boundary modules | Helpers contain request-capable code and boundary classifiers | Side effects if reached | Legacy coupling | Trace callers and credentials | P0 |
| Agent runners and manager | REAL_ACTIVE | `agents/` runners and manager | Agent source and runner paths exist; execution status is not inferred | Runtime/permission ambiguity | Legacy runner debt | Agent execution inventory | P0 |
| Product domains and data | REAL_ACTIVE | `domains/demo_generico`, `domains/loteria` | Domain code, JSON, DB and memory-related data exist | Operational mutation and data ownership | Legacy domain surface | Audit domain writes and entry points | P0 |
| Catalogs and configuration | REAL_ACTIVE | `catalogs/`, `config/` | Catalog and hardware/config data are present | Sensitive config assumptions | Schema/version drift | Trace read/write consumers | P1 |
| Memory, logs and local data | REAL_ACTIVE | `memory/`, `memoria_*`, `logs/`, `data/` | Local persistence surfaces exist | Retention, privacy and writes unknown | No unified inventory | Memory/evidence audit | P0 |
| GOKV registry and OCI | REAL_CONTROLLED | `gokv/`, `knowledge/global_operational/` | Development-time validation, packs and append-only captures exist | Promotion/runtime confusion | Supplement schema limitation | Preserve development-only boundary | P1 |
| Roadmap and architecture documents | DOCUMENTED_ONLY | `docs/` roadmap/backend books | Documents describe historical and future states; Git/current map wins | Documentation drift | Several successor cursors | Reconcile before each phase | P1 |
| Continuity and checkpoint tests | TEST_ONLY | `tests/test_roadmap_2_0_continuity_preflight.py`, UI/GOKV tests | Guards assertions and boundaries; tests are not runtime capability | False product inference | Historical expected failures | Keep classification explicit | P1 |
| Fixtures and visual matrices | FIXTURE_ONLY | `tests/fixtures/` | Test data and viewport matrices only | Fixture/product confusion | Snapshot drift | Validate fixture provenance | P2 |
| Strategic future architecture | FUTURE | `docs/FUTURE_*`, strategic docs | Vision only; no implementation authority | Scope expansion | Future-only breadth | None until authorized | P3 |
| README historical cursor | LEGACY | `README.md` pre-N3 | Visible cursor is older than current 1.204 line | Continuity confusion | Minimal sync required | Verify final README cursor | P1 |
| Dedicated public `backend/`, `runtime/`, `execution/`, `integrations/` trees | UNKNOWN_REQUIRES_AUDIT | Directory inventory plus core modules | Absence of these exact trees does not prove absence of equivalent paths | Hidden equivalent surface | Needs targeted inventory | 3.0 read-only audit | P0 |
| Security, provider and secret consumption | UNKNOWN_REQUIRES_AUDIT | boundary contracts plus legacy routes/providers | Boundaries exist, but full path-to-side-effect truth is not established here | Critical if opened | No deep audit in 2.x | 3.0 first-pass scope | P0 |
| Agent/preset/paper/team activation chain | UNKNOWN_REQUIRES_AUDIT | source and sandbox artifacts | Sandbox structures exist; activation equivalence is unresolved | High | Needs lineage audit | 3.0 targeted audit | P0 |

## Closed layers

- UI/UX 1.x current contract-aware line and its 1.204 closure.
- GOKV 0.3 registry/promotion governance baseline.
- Read-only visual and contract checkpoint evidence.
- Historical UI/UX debt classification.

## Active layers

- Legacy FastAPI/application/domain source.
- Core contract, sandbox, provider, agent and persistence source surfaces.
- Development-time GOKV capture and test infrastructure.

## Reality categories

- `REAL_ACTIVE`: source routes, legacy application, domains, providers, tools,
  agent runners, catalogs/config and local persistence exist in the repository.
- `REAL_CONTROLLED`: internal contracts, GOKV, runtime/execution preflight and
  confirmation-gated services exist with explicit boundaries.
- `REAL_SANDBOX`: materialization, rollback, agents, presets, papers and teams
  are scoped to sandbox artifacts and manifests.
- `REAL_READ_ONLY`: UI contract surfaces, previews, validation, status and
  derived read models.
- `DOCUMENTED_ONLY`: roadmap, architecture and strategic documents.
- `TEST_ONLY`: continuity, contract and E2E guards.
- `FIXTURE_ONLY`: fixture JSON and visual matrices.
- `LEGACY`: stale README cursor and historical route/documentation assumptions.
- `FUTURE`: strategic OS, learning, router, permission and integration vision.
- `UNKNOWN_REQUIRES_AUDIT`: exact side-effect, provider, security, activation
  and equivalent-tree boundaries not audited by this read-only map.

## Known and historical debt

- Known current debt: documentation drift, legacy routes, extensive contracts,
  provider-capable code, local persistence, heavy suites and unclear ownership
  between legacy application and pre-operational core.
- Historical debt: UI/UX snapshots and temporal scope guards classified in
  1.204; old roadmap cursors remain evidence, not current authority.
- External dependency debt: policy-excluded Ollama integration coverage.
- Security unknowns: complete route/auth/secret/network call graph.
- Contract unknowns: exact relation between legacy API contracts and internal
  backend contract-only services.
- Memory/evidence unknowns: write ownership, retention and separation of local
  application memory from GOKV evidence.
- Provider unknowns: invocation paths, credentials, retries, network effects
  and provider lifecycle.
- Agent/preset/paper/team unknowns: activation boundaries and equivalence to
  sandbox artifacts.

## Backend entry condition

`BACKEND_ENTRY_CONDITION = READ_ONLY_INVENTORY_FIRST`

Roadmap 3.x can start in read-only mode: inventory routes, callers, writes,
providers, agents, stores, runtime flags, execution boundaries and security
conditions. It must not implement or enable any of them during the first audit.

`CAN_START_ROADMAP_3_X = YES`

Reason: the UI line is closed, Git and GOKV are coherent, the current map has
zero continuity blockers, and the unresolved backend questions are precisely
the subject of an elite read-only inventory. This is not permission to start
runtime, execution, API expansion, provider calls or operational writes.

## Gate conclusion

ROADMAP_2_2_CURRENT_STATE_MAP_PASSED
