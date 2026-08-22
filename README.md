# IA_CORE

IA_CORE is a local, contract-aware multi-agent framework in construction. Its current focus is a stable internal backend, a global professional library, and a non-operative UI/UX console that reads contracts without runtime or execution authority.

Current GitHub backup target: `https://github.com/IA-MONOPOLY-CORE/IA_CORE`

## Current State

- Last reference commit before this backup: `8d889369`.
- UI/UX cerrado hasta 1.22; `PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution` cierra Frontend Incongruence como checkpoint documental/test.
- UI/UX planificado hasta 1.23; `PROMPT UI/UX 1.23 - Consolidar siguiente bloque UI/UX post Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution` selecciona Operator Guidance / Empty-State Intelligence como proximo bloque.
- UI/UX auditado hasta 1.24; `PROMPT UI/UX 1.24 - Auditar Operator Guidance / Empty-State Intelligence IA_CORE contract-aware sin runtime/no-execution` identifica gaps de guidance/empty states sin implementar cambios activos.
- Next pending step: `PROMPT UI/UX 1.25 - Endurecer guidance y empty states de operador IA_CORE contract-aware sin runtime/no-execution`.
- The internal backend is prepared for UI/UX exposure through stable contracts, but runtime remains non-operative.
- IA_CORE is the active identity.
- SAAOP/Loteria remain only as historical/internal legacy material where present; they are not active UI identity.
- No new public endpoints, no runtime, no execution, no real dispatch, no new dependencies, and no backend operative changes were introduced by the latest UI/UX block.

## Project Principles

- One prompt at a time.
- Real tests before closing a block.
- One commit per closed block.
- Clean working tree after each closure.
- no-runtime/no-execution until formally enabled by contract.
- No phantom actions.
- No unauthorized endpoints.
- No impulse dependencies.
- Contract before interface.
- First truth, then beauty, then level.

## Project Map

- `api.py`: FastAPI app serving API routes and `ui/web/` static assets.
- `core/`: contract, boundary, backend-internal, runtime-preparation, sandbox, memory, permission, response, and security logic.
- `agents/`: generic agent definitions, roles, loaders, lightweight runners, and runtime JSON agent support.
- `catalogs/`: professional roles, specializations, archetypes, areas, niches, and model policy catalogs.
- `domains/`: domain definitions and legacy domain material. `domains/loteria/` is historical/internal legacy context, not active UI identity.
- `providers/`: provider abstractions and provider implementations.
- `tools/`: tool boundary/catalog support.
- `ui/web/`: current web console served statically by FastAPI; there is no detected `package.json` or Node frontend runner.
- `docs/`: architecture, backend-internal, security, UI/UX, checkpoint, audit, and legacy documentation.
- `tests/`: pytest regression suite covering contracts, boundaries, backend-internal payloads, UI/UX checkpoints, and backup readiness.
- `scripts/`: generation, audit, and benchmark helper scripts.
- `data/`: generated market catalog data.
- `memory/`, `memoria_agentes/`: local memory/state artifacts; selected volatile state is ignored by Git.

## Documentation Map

Key project documentation includes:

- Initial/security audits: `docs/IA_CORE_SECURITY_SURFACE_AUDIT.md`, `docs/IA_CORE_SECURITY_LAYER_PLAN.md`, `docs/SECURITY_LAYER_FINAL_CHECKPOINT.md`.
- Prompt/unification and architecture history: `ARCHITECTURE_DECISIONS.md`, `docs/NEXT_ARCHITECTURE_BLOCK_PLAN.md`, `docs/POST_SECURITY_LAYER_ARCHITECTURE_AUDIT.md`.
- Reverse-engineering and boundary manuals: `docs/CONTEXT_BOUNDARY_POLICY.md`, `docs/OUTPUT_BOUNDARY_POLICY.md`, `docs/MODEL_INVOCATION_BOUNDARY_POLICY.md`, `docs/TOOL_BOUNDARY_POLICY.md`, `docs/SANDBOX_BOUNDARY_POLICY.md`, `docs/RUNTIME_ACTIVATION_GATE_POLICY.md`.
- Backend internal book and phases: `docs/BACKEND_INTERNAL_BOOK_DESIGN.md`, `docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md`, `docs/BACKEND_INTERNAL_PHASE_4_RUNTIME_EXECUTION_PREPARATION_PLAN.md`, `docs/BACKEND_INTERNAL_PHASE_5_TEAM_SANDBOX_BLOCK_PLAN.md`, `docs/BACKEND_INTERNAL_PHASE_6_SANDBOX_E2E_ROLLBACK_REGENERATION_BLOCK_PLAN.md`, `docs/BACKEND_INTERNAL_PHASE_7_UI_CONTRACT_BLOCK_PLAN.md`, `docs/BACKEND_INTERNAL_PHASE_8_CONTROLLED_INTERNAL_EXPOSURE_BLOCK_PLAN.md`.
- Backend UI contract: `docs/BACKEND_INTERNAL_UI_CONTRACT_7_0.md`, `docs/BACKEND_INTERNAL_STABLE_UI_PAYLOADS_7_6.md`, `docs/BACKEND_INTERNAL_UI_CONTRACT_CHECKPOINT_7_7.md`, `docs/BACKEND_INTERNAL_EXPOSURE_REGISTRY_8_1.md`, `docs/BACKEND_INTERNAL_REQUEST_ENVELOPE_8_2.md`, `docs/BACKEND_INTERNAL_DISPATCHER_8_3.md`, `docs/BACKEND_INTERNAL_CONFIRMATION_GATE_8_4.md`, `docs/BACKEND_INTERNAL_RESPONSE_ADAPTER_8_5.md`, `docs/BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_8_6.md`, `docs/BACKEND_INTERNAL_FUTURE_UI_CONTRACT_PLAN_8_7.md`.
- UI/UX book and checkpoints from 0.5.3 onward: `docs/UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md`, `docs/UI_UX_VISUAL_ARCHITECTURE_0_7.md`, `docs/UI_UX_SUPERIOR_LAYOUT_0_8.md`, `docs/UI_UX_VISUAL_BASE_CHECKPOINT_0_9.md`, `docs/UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md`, `docs/UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md`, `docs/UI_UX_MAIN_CONSOLE_FLOW_1_2.md`, `docs/UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_1_3.md`, `docs/UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md`.
- Current UI/UX chain: `docs/UI_UX_NEXT_BLOCK_PLAN_1_19.md`, `docs/UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md`, `docs/UI_UX_FRONTEND_INCONGRUENCE_HARDENING_1_21.md`, `docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md`, `docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md`, `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md`.
- GitHub backup readiness: `docs/IA_CORE_GITHUB_BACKUP_READY.md`.

## Current UI/UX State

The active UI is the IA_CORE console in `ui/web/`. It includes:

- backend contract widgets over `backend_internal_ui_payload.v1`;
- cleaned IA_CORE active identity;
- visual architecture and superior layout;
- main console flow and read-only interaction model;
- payload reading model with summary/detail/raw-safe layers;
- contract detail panels;
- internal navigation without hash routing;
- minimal IA_CORE component system;
- responsive/accessibility hardening;
- admin boundary/exposure hardening;
- frontend incongruence audit 1.20;
- hardening 1.21 for `request-draft-*`, `request-contract-*`, `logs-sanitized`, and non-operative visual state naming;
- checkpoint 1.22 closes Frontend Incongruence and confirms GitHub restore point;
- plan 1.23 selects Operator Guidance / Empty-State Intelligence as the next no-runtime/no-execution UI/UX block;
- audit 1.24 maps operator guidance and empty-state gaps before hardening 1.25.

The UI does not grant permissions. `allowed_actions` is backend-declared only; `forbidden_actions` and `blocked_capabilities` remain visible and non-executable.

## Current Backend State

At a high level, the backend contains:

- global professional library and catalogs for roles, specializations, archetypes, areas, niches, and generated professional profiles;
- domain profile catalogs and agent presets where applicable;
- `backend_internal_ui_payload.v1` and stable UI payload projections;
- internal exposure registry;
- request envelope `backend_internal_ui_request.v1`;
- dispatcher no-runtime boundary;
- confirmation gate;
- response adapter;
- read-only internal backend read models;
- security and boundary policies for secrets, context, output, tools, model invocation, sandbox, and runtime activation.

Runtime/execution preparation exists as contract and read-model work, but no operative runtime/execution is active.

## Current Limits

- No runtime.
- No execution.
- No real dispatch.
- No new public endpoints for runtime or execution.
- No tool or model invocation from the UI.
- No active integrations for production operation.
- No production deployment yet.
- No Git history rewrite or force push for backup.

## Tests Principales

Known quick checks:

```powershell
node --check ui/web/backend-contract-widgets.js
node --check ui/web/admin-panels.js
node --check ui/web/console-interactions.js
python -m pytest tests/test_api_admin_panels.py -q
python -m pytest tests/test_ui_ux_frontend_incongruence_hardening_1_21.py -q
python -m pytest tests/test_ui_ux_next_block_plan_1_23.py -q
python -m pytest tests/test_ui_ux_operator_guidance_empty_state_audit_1_24.py -q
python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q
python -m pytest tests/test_ia_core_github_backup_readiness.py -q
```

When using this Codex workspace, pytest may need `PYTHONPATH` pointing to `.testdeps` if project dependencies are already staged there.

## Continuation Workflow

1. Run `git status --short` and confirm the tree is clean.
2. Run `git rev-parse --short HEAD` and compare it with the documented latest commit.
3. Read the latest docs: `docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md`, `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md`, then this README.
4. Continue only with the exact next prompt: `PROMPT UI/UX 1.25 - Endurecer guidance y empty states de operador IA_CORE contract-aware sin runtime/no-execution`.
5. Run the relevant tests.
6. Commit the completed block.
7. Confirm `git status --short` is clean again.

## Restoration And Continuidad

General restoration steps for another PC:

1. Clone `https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
2. Read this `README.md` and `docs/IA_CORE_GITHUB_BACKUP_READY.md`.
3. Create a Python environment if needed.
4. Install dependencies from the existing dependency files, for example `requirements-api.txt` or `requirements.txt` according to the task being resumed.
5. Run the principal tests listed above.
6. Start the local API/UI with the existing project method, for example `python api.py` from an activated Python environment if dependencies are installed.
7. Open the UI served by FastAPI at the local server URL.
8. Continue from the next prompt documented above.

No `package.json` is currently detected; the active UI appears to be static files served by FastAPI rather than a Node/Vite app.

## Backup And GitHub Safety

- GitHub target: `https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- Prefer a private repository while the project contains internal architecture, historical domain material, and local development context.
- No subir secretos; do not commit secrets.
- Do not commit `.env` or `.env.*`.
- Review `.gitignore` before every backup.
- Keep local caches, virtual environments, logs, and build outputs out of Git.
- Use clean commits.
- Push after important block/checkpoint closures; routine planning commits may remain local until the next restore point unless the operator asks for an update.
- Verify `git remote -v` before pushing.
- Use normal push only, for example `git push -u origin main`.
- Do not force push.
