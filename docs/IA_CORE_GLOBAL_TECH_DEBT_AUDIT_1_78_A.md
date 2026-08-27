# IA_CORE Global Technical Debt Audit 1.78.A

## Commit base

- Commit base: `628ab75`.
- Restore point remoto vigente: `628ab75`.
- Rama auditada: `main`.
- Remoto auditado: `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- Estado inicial confirmado: `main` sincronizado con `origin/main`, working tree limpio.

## Objetivo

Esta auditoria global profunda prepara IA_CORE para una limpieza controlada antes de continuar con UI/UX 1.79. El objetivo no es hacer pasar tests por maquillaje: es inventariar deuda tecnica real, contradicciones, residuos historicos, fixtures muertas, deuda de naming, seguridad, documentacion y contrato, y dejar una estrategia por tandas para limpiar con evidencia.

## Scope

Scope global del repo completo:

- docs.
- tests.
- UI.
- backend.
- core.
- domains.
- tools.
- configs.
- scripts.
- fixtures.
- seguridad.
- naming.
- contratos.
- deuda historica.

## No-scope

Este prompt no borro nada, no modifico codigo productivo, no limpio todavia, no modifico UI activa, no toco backend operativo, no creo endpoints, no activo runtime, no instalo dependencias, no modifico CI y no avanzo a 1.79.

Tambien queda explicitamente declarado: no se modifico UI activa; no se toco backend/runtime/endpoints/CI; no se avanzo a 1.79.

## Metodologia

Comandos usados:

- `git status --short`
- `git rev-parse --short HEAD`
- `git branch --show-current`
- `git remote -v`
- `git fetch origin`
- `git status`
- `git log --oneline -10`
- `Get-ChildItem -Force`
- `rg --files docs tests ui core domains tools scripts configs .github`
- `git ls-files`
- `git ls-files --others --ignored --exclude-standard`
- `rg -n -i "SAAOP|Loter[ií]a|Tactical HUD|U-Score|Cazador|Espejo|combinatoria"`
- `rg -n -i "unlock|override|bypass|permission escalation|validate now|allowed_actions|forbidden_actions|blocked_capabilities"`
- `rg -n -i "fetch\\(|@app\\.|@router\\.|route\\(|requests\\.|httpx|urllib|FastAPI|APIRouter|endpoint|localhost|127\\.0\\.0\\.1"`
- `rg -n -i "api[_-]?key|secret|token|password|credential|bearer|OPENAI|ANTHROPIC|GITHUB|env"`
- `python -m pytest tests/ -q`
- `python -m pyflakes api.py core agents providers tools scripts domains tests`
- `python -m compileall -q api.py core agents providers tools scripts domains tests`
- `node --check ui/web/backend-contract-widgets.js`
- `node --check ui/web/admin-panels.js`
- `node --check ui/web/console-interactions.js`
- `python -m pytest tests/test_ia_core_global_tech_debt_audit_1_78_a.py -q`
- `python -m pytest tests/test_ui_ux_validation_readiness_final_screen_contract_checkpoint_1_78.py -q`
- `python -m pytest tests/test_ui_ux_validation_readiness_final_screen_contract_1_77.py -q`
- `python -m pytest tests/test_ui_ux_validation_readiness_final_screen_contract_audit_1_76.py -q`
- `python -m pytest tests/test_ia_core_github_backup_readiness.py -q`
- `python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q`
- `git diff --check`

Criterios de clasificacion:

- `REUSE`: convertir deuda util en test vigente, fixture, guardrail, warning contractual, matriz o referencia arquitectonica.
- `UPDATE`: actualizar material todavia util pero desfasado.
- `ISOLATE`: aislar como legacy/historico para que no actue como contrato vigente.
- `DELETE`: candidato a borrar en un prompt posterior con evidencia.
- `DO_NOT_TOUCH`: preservar por contrato o porque requiere revision humana antes de cambiar.

Limitaciones:

- El barrido historico completo puede fallar y de hecho fallo; se interpreta como diagnostico de deuda, no como fracaso de este prompt.
- No se revelo el contenido de `.env`; solo se verifico que existe localmente, esta ignorado y contiene un valor no vacio.
- No se corrigieron fallos antiguos, imports, cursores ni UI activa.
- Las rutas ignoradas grandes (`venv`, `.testdeps`, caches, logs, memorias vectoriales) fueron inventariadas como residuos locales, no como archivos versionados.
- El barrido completo genero efectos colaterales temporales en memorias de test; los JSON versionados se restauraron a HEAD y las carpetas no versionadas `memoria_agentes/test_agent` y `memoria_agentes/test_agent_context` se movieron a `.pytest_cache/audit_temp/` para preservar evidencia sin borrar archivos ni dejar rutas prohibidas por los tests backend.

## Estado de tests

### Tests contractuales vigentes

Los tests de alcance 1.78.A y los tests contractuales pedidos para 1.78/1.77/1.76/backend backup/backend UI deben pasar como condicion de cierre de este prompt.

### Barrido historico completo diagnostico

Resultado del comando `python -m pytest tests/ -q`:

- Total observado: 5450 resultados.
- Passed: 5426.
- Failed: 22.
- Skipped: 2.
- Warnings: 5.
- Duracion: 1234.97s.

Archivos fallidos:

- `tests/test_domains.py`
- `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py`
- `tests/test_ui_ux_component_documentation_style_reference_1_45.py`
- `tests/test_ui_ux_component_documentation_style_reference_audit_1_44.py`
- `tests/test_ui_ux_contract_aware_checkpoint_0_6.py`
- `tests/test_ui_ux_future_screens_readiness_1_41.py`
- `tests/test_ui_ux_future_screens_readiness_checkpoint_1_42.py`
- `tests/test_ui_ux_main_console_flow_1_2.py`
- `tests/test_ui_ux_main_console_interaction_checkpoint_1_4.py`
- `tests/test_ui_ux_main_console_interaction_model_1_3.py`
- `tests/test_ui_ux_main_console_refinement_1_1.py`
- `tests/test_ui_ux_main_console_structure_1_0.py`
- `tests/test_ui_ux_next_block_plan_1_43.py`
- `tests/test_ui_ux_superior_layout_0_8.py`
- `tests/test_ui_ux_visual_base_checkpoint_0_9.py`

Tests fallidos:

- `tests/test_domains.py::test_widgets_are_functional_and_not_decorative`
- `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py::test_request_draft_controls_are_explicitly_read_only_and_blocked`
- `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py::test_allowed_actions_copy_does_not_grant_ui_permission`
- `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py::test_internal_exposure_is_read_only_not_public_control`
- `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py::test_next_step_points_to_1_18_as_evidence_not_runtime_flow`
- `tests/test_ui_ux_component_documentation_style_reference_1_45.py::test_readmes_reference_style_reference_1_45_and_next_prompt_1_46`
- `tests/test_ui_ux_component_documentation_style_reference_audit_1_44.py::test_readmes_reference_audit_1_44_and_next_prompt_1_45`
- `tests/test_ui_ux_contract_aware_checkpoint_0_6.py::test_widgets_are_contract_aware_without_endpoint_permission_sources`
- `tests/test_ui_ux_future_screens_readiness_1_41.py::test_readmes_reference_readiness_1_41_and_next_prompt_1_42`
- `tests/test_ui_ux_future_screens_readiness_checkpoint_1_42.py::test_readmes_reference_checkpoint_1_42_and_next_prompt_1_43`
- `tests/test_ui_ux_main_console_flow_1_2.py::test_main_console_keeps_identity_and_marks_contract_aware_flow`
- `tests/test_ui_ux_main_console_flow_1_2.py::test_flow_does_not_infer_permissions_or_enable_operations`
- `tests/test_ui_ux_main_console_flow_1_2.py::test_flow_documents_and_implements_responsive_reading_order`
- `tests/test_ui_ux_main_console_interaction_checkpoint_1_4.py::test_widgets_remain_contract_aware_and_honest_without_payload`
- `tests/test_ui_ux_main_console_interaction_model_1_3.py::test_interactions_do_not_infer_permissions_or_enable_execution`
- `tests/test_ui_ux_main_console_refinement_1_1.py::test_refinement_reduces_ornament_and_improves_semantic_rows`
- `tests/test_ui_ux_main_console_refinement_1_1.py::test_refinement_documents_and_implements_responsive_contract`
- `tests/test_ui_ux_main_console_structure_1_0.py::test_main_console_keeps_contract_fields_actions_and_blocks_visible`
- `tests/test_ui_ux_next_block_plan_1_43.py::test_readmes_reference_plan_1_43_and_next_prompt_1_44`
- `tests/test_ui_ux_superior_layout_0_8.py::test_active_ui_contains_superior_contract_aware_layout_zones`
- `tests/test_ui_ux_superior_layout_0_8.py::test_layout_keeps_contract_actions_and_blocks_visible`
- `tests/test_ui_ux_visual_base_checkpoint_0_9.py::test_widgets_actions_and_blocks_remain_contract_aware`

Causa probable por grupo:

- Grupo UI activa vieja: assertions de strings y microcopy que ya no existen en `ui/web/index.html` o `ui/web/backend-contract-widgets.js`.
- Grupo cursor README historico: tests antiguos esperan `Next pending step` de 1.47 aunque el cursor vigente avanzo hasta 1.78 y ahora queda pausado en 1.78.A/1.78.B.
- Grupo widget no-payload: tests antiguos esperan copy exacta vieja para `backend_internal_ui_payload.v1`; el widget conserva semantica contract-aware pero cambio el texto.
- Grupo layout/interaccion: tests 0.8-1.4 esperan fragmentos JS antiguos como `debatePanel.classList.add('collapsed')` y labels viejos.

Categoria propuesta para el barrido: `UPDATE` para tests recuperables, `ISOLATE` para assertions que deben convertirse en memoria historica, y `REUSE` para los guardrails que siguen teniendo valor.

## Inventario global de deuda

| debt_id | area | archivo/ruta | tipo | descripcion | evidencia | severidad | categoria propuesta | riesgo | accion recomendada | bloque recomendado | requiere revision humana |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TD-001 | Git/trazabilidad | repo | restore point | Estado limpio y sincronizado que no debe tocarse durante limpieza | HEAD `628ab75`, `main` up to date | P4_HISTORICAL | DO_NOT_TOUCH | DO_NOT_TOUCH | Preservar como punto de restauracion | 1.78.D | no |
| TD-002 | tests | `tests/` | fallos historicos | Barrido completo falla con 22 tests UI/UX historicos | `22 failed, 5426 passed, 2 skipped` | P1_HIGH | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Actualizar o aislar por grupo, sin maquillaje | 1.78.C | si |
| TD-003 | tests | `tests/test_domains.py` | assertion vieja | Espera copy de ultimo debate no presente en UI actual | fallo `Estado del ultimo debate` | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Revalidar intencion y convertir en guardrail actual | 1.78.C | no |
| TD-004 | tests | `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py` | assertion vieja | Espera microcopy exacta 1.17 en HTML/widgets actuales | 5 fallos del archivo | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Actualizar a semantica vigente o aislar como legacy | 1.78.C | no |
| TD-005 | tests/docs | tests 1.41, 1.42, 1.43, 1.44, 1.45 | cursor viejo | Tests esperan `Next pending step` 1.47 | fallos README cursor | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Rehacer politica de cursor historico tolerante al avance | 1.78.C | no |
| TD-006 | UI/UX tests | tests 0.8-1.4 | layout viejo | Assertions atadas a labels/JS antiguos | fallos `debatePanel.classList.add` y labels viejos | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Separar guardrail semantico de snapshot textual viejo | 1.78.C | no |
| TD-007 | tests | `tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py` | bug de test | Variable `current_after_1_63` usada antes de definirse | `pyflakes` undefined name | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Mover definicion antes de uso | 1.78.C | no |
| TD-008 | core | `core/supervisor.py` | import/runtime latent | `buscar_lecciones_utiles` usado antes de import local | `pyflakes` undefined name line 741 | P1_HIGH | UPDATE | NEEDS_HUMAN_REVIEW | Revisar flujo y corregir import sin cambiar contrato | 1.78.C | si |
| TD-009 | calidad Python | varios | higiene estatica | Imports sin uso, shadowing y f-strings sin placeholders | `pyflakes` lista multiples archivos | P3_LOW | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Limpieza mecanica en tanda controlada | 1.78.C | no |
| TD-010 | tests | `test_debate.py`, `test_demo_generico.py`, `test_respuesta.py` | tests raiz | Tests ad hoc fuera de `tests/` | `git ls-files` raiz | P3_LOW | ISOLATE | LEGACY_ARCHIVE_CANDIDATE | Mover a legacy o convertir a tests formales | 1.78.C | si |
| TD-011 | artifacts locales | `.testdeps`, `venv`, caches, logs, memoria vectorial | residuos locales | Arbol local pesado ignorado, no versionado | `git ls-files --others --ignored` | P3_LOW | DELETE | SAFE_TO_DELETE_CANDIDATE | Borrar solo en prompt de limpieza local aprobado | 1.78.C | no |
| TD-012 | seguridad | `.env` | secreto local | Existe `.env` ignorado con valor no vacio | auditoria de lineas sin revelar contenido | P1_HIGH | DO_NOT_TOUCH | NEEDS_HUMAN_REVIEW | Mantener ignorado; revisar rotacion/manual si corresponde | 1.78.B | si |
| TD-013 | seguridad/config | `memory/user_settings.json` | config sensible | Archivo versionado contiene campo `api_key` aunque vacio | `git ls-files`, rg secrets | P2_MEDIUM | UPDATE | NEEDS_HUMAN_REVIEW | Evaluar template seguro o exclusion futura | 1.78.C | si |
| TD-014 | dependencias/config | `requirements.txt`, `requirements-api.txt` | duplicacion entorno | Dos sets: uno enorme runtime local y otro API/CI minimo | lectura de requirements | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Separar prod/dev/test y documentar fuente de verdad | 1.78.C | no |
| TD-015 | CI/config | `.github/workflows/ci.yml` | CI estricto inconsistente | CI corre `pyflakes .`, pero pyflakes falla hoy en repo | pyflakes exit 1 | P1_HIGH | UPDATE | NEEDS_HUMAN_REVIEW | Arreglar deuda o ajustar alcance CI con criterio | 1.78.C | si |
| TD-016 | UI/UX | `ui/web/index.html` | monolito | HTML activo pesa 190015 bytes con CSS/JS inline | inventario `Get-ChildItem ui/web` | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Planear extraccion sin cambiar comportamiento | posterior a 1.79 | no |
| TD-017 | UI/UX | `ui/web/styles.css` | posible stylesheet legacy | Existe y tests/docs lo referencian, pero `index.html` no lo linkea | `rg styles.css` sin link HTML | P3_LOW | ISOLATE | LEGACY_ARCHIVE_CANDIDATE | Confirmar uso real y archivar/documentar si no aplica | 1.78.C | no |
| TD-018 | UI/UX/backend boundary | `ui/web/admin-panels.js`, `domains.js`, `index.html` | fetch allowlist | Fetches heredados/admin existen y deben distinguirse de fetch contract-aware nuevo | `rg "fetch(" ui/web` | P2_MEDIUM | REUSE | REUSE_AS_GUARDRAIL_CANDIDATE | Convertir allowlist en guardrail central | 1.78.C | no |
| TD-019 | UI/UX identity | `ui/web/` | guardrail vigente | No hay SAAOP/Loteria/Tactical HUD/U-Score en UI activa | `rg legacy ui/web` sin matches | P4_HISTORICAL | REUSE | REUSE_AS_GUARDRAIL_CANDIDATE | Preservar test anti legacy activo | 1.78.C | no |
| TD-020 | agents | `agents/prompts.py`, `agents/runtime_json_agent.py` | acoplamiento dominio | Imports directos a `domains.loteria` por compatibilidad | rg legacy core/agents | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Encapsular resolver por dominio | post limpieza inicial | si |
| TD-021 | core | `core/debate.py`, `core/supervisor.py`, `core/model_recommendation.py` | fallback legacy | Defaults perezosos a Loteria siguen en core | rg legacy core | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Mantener compat pero aislar defaults | post limpieza inicial | si |
| TD-022 | domains | `domains/loteria/` | legacy versionado | Dominio Loteria preservado como `legacy` | `domain.json` status legacy | P4_HISTORICAL | ISOLATE | LEGACY_ARCHIVE_CANDIDATE | Mantener como archivo historico no operativo | 1.78.B | no |
| TD-023 | docs | `MAPA_CORE_VS_LOTERIA.md`, `RESPONSESCORE_USOS.md` | docs legacy raiz | Docs historicas en raiz pueden confundirse con verdad vigente | `git ls-files` raiz | P4_HISTORICAL | ISOLATE | LEGACY_ARCHIVE_CANDIDATE | Mover o referenciar como legacy en tanda docs | 1.78.C | si |
| TD-024 | docs | `README.md`, `ui/web/README.md`, docs UI/UX | cursor/documentacion larga | Timeline muy largo y cursores deben pausarse en 1.78.A/1.78.B | README leido | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Mantener cursor actual y separar historial de estado actual | 1.78.A/1.78.B | no |
| TD-025 | providers | `providers/*_provider.py` | placeholders | Proveedores cloud placeholder conviven con config real NVIDIA | rg placeholder providers | P2_MEDIUM | UPDATE | SAFE_TO_UPDATE_CANDIDATE | Documentar estado o aislar mocks | post limpieza inicial | si |
| TD-026 | seguridad/backend | `api.py`, `config.py` | API key persistence | Endpoint settings puede escribir API key en `config.py` | rg `api_key`/`NVIDIA_API_KEY` | P1_HIGH | UPDATE | NEEDS_HUMAN_REVIEW | Revisar manejo de secretos antes de exposicion | 1.78.B | si |
| TD-027 | backend/contracts | `core/backend_internal_*`, docs 7.x/8.x | contrato vigente | Contratos backend internos son fuente de verdad estable | tests contractuales vigentes | P4_HISTORICAL | DO_NOT_TOUCH | DO_NOT_TOUCH | No tocar en limpieza salvo prompt especifico | todos | no |
| TD-028 | artifacts locales | `__pycache__`, `.pytest_cache`, `.ruff_cache` | caches | Caches generados no versionados | ignored files listing | P3_LOW | DELETE | SAFE_TO_DELETE_CANDIDATE | Borrar en tanda local segura si se decide | 1.78.C | no |
| TD-029 | fixtures/data | `data/market_catalog/market_catalog.generated.json` | generated data | Archivo generado versionado debe tener razon y test | `git ls-files data/...` | P3_LOW | REUSE | REUSE_AS_GUARDRAIL_CANDIDATE | Mantener si es fixture contractual; documentar origen | 1.78.B | no |
| TD-030 | tools | `tools/modules/echo.py`, `tools/modules/uppercase.py` | ejemplos | Modulos herramienta simples pueden ser demos o residuo | inventario tools | P3_LOW | ISOLATE | LEGACY_ARCHIVE_CANDIDATE | Confirmar uso; aislar como examples si no son core | 1.78.C | si |

## Clasificacion por area

- Git/trazabilidad: 1 item.
- tests: 7 items.
- UI/UX: 5 items.
- backend/contracts: 3 items.
- core: 2 items.
- domains: 1 item.
- tools: 1 item.
- docs: 2 items.
- fixtures: 1 item.
- naming/identity: 2 items.
- security/boundaries: 4 items.
- dependencies/config: 3 items.
- orphan/duplicate files: 1 item.

## Clasificacion por destino

- `REUSE`: 3.
- `UPDATE`: 17.
- `ISOLATE`: 5.
- `DELETE`: 2.
- `DO_NOT_TOUCH`: 3.

## Clasificacion por severidad

- `P0_BLOCKER`: no se detectaron bloqueadores P0 nuevos para cerrar esta auditoria.
- `P1_HIGH`: deuda que puede romper CI, seguridad o runtime latente.
- `P2_MEDIUM`: deuda recuperable que afecta mantenimiento, contrato o tests.
- `P3_LOW`: higiene, caches, ejemplos o residuos controlables.
- `P4_HISTORICAL`: material historico valido que debe permanecer contextualizado.

Conteo:

- `P0_BLOCKER`: 0.
- `P1_HIGH`: 5.
- `P2_MEDIUM`: 13.
- `P3_LOW`: 7.
- `P4_HISTORICAL`: 5.

## Clasificacion por riesgo

- `SAFE_TO_DELETE_CANDIDATE`: candidato a borrar con baja incertidumbre en prompt posterior.
- `SAFE_TO_UPDATE_CANDIDATE`: candidato a actualizar si se conserva la semantica vigente.
- `REUSE_AS_GUARDRAIL_CANDIDATE`: deuda util para convertir en guardrail o regression test.
- `LEGACY_ARCHIVE_CANDIDATE`: material historico que debe aislarse.
- `NEEDS_HUMAN_REVIEW`: requiere decision humana o revision de seguridad/arquitectura.
- `DO_NOT_TOUCH`: no tocar en limpieza general.

Conteo:

- `SAFE_TO_DELETE_CANDIDATE`: 2.
- `SAFE_TO_UPDATE_CANDIDATE`: 13.
- `REUSE_AS_GUARDRAIL_CANDIDATE`: 3.
- `LEGACY_ARCHIVE_CANDIDATE`: 5.
- `NEEDS_HUMAN_REVIEW`: 5.
- `DO_NOT_TOUCH`: 2.

## Clasificacion por destino detallada

### REUSE

- TD-018: fetch allowlist como guardrail anti endpoint/fetch nuevo.
- TD-019: ausencia de legacy visible en UI activa como guardrail de identidad IA_CORE.
- TD-029: catalogo generado como fixture contractual si se documenta su origen.

### UPDATE

- TD-002 a TD-009: tests historicos, assertions y pyflakes.
- TD-013 a TD-016: seguridad/config, dependencias, CI e index monolitico.
- TD-020, TD-021, TD-024, TD-025, TD-026: acoplamientos legacy, docs/cursors, providers y manejo de secretos.

### ISOLATE

- TD-010: tests raiz ad hoc.
- TD-017: stylesheet posiblemente legacy.
- TD-022: dominio Loteria legacy.
- TD-023: docs legacy raiz.
- TD-030: herramientas ejemplo.

### DELETE

- TD-011: residuos locales pesados ignorados.
- TD-028: caches generados ignorados.

### DO_NOT_TOUCH

- TD-001: restore point `628ab75`.
- TD-012: `.env` local no revelado.
- TD-027: contratos backend internos vigentes.

## Plan maestro de limpieza

- Tanda 1: tests historicos fallidos y assertions viejas. Actualizar o aislar los 22 fallos del barrido completo sin tocar UI activa.
- Tanda 2: docs/cursors/READMEs contradictorios. Separar estado actual, historial y cursores futuros; evitar que tests viejos exijan cursores cerrados.
- Tanda 3: fixtures/archivos huerfanos. Revisar tests raiz, generated data, memory config y local artifacts ignorados.
- Tanda 4: naming/legacy visible. Mantener IA_CORE como identidad activa; encapsular Loteria/SAAOP en legacy o domain-specific.
- Tanda 5: seguridad/limites. Revisar `.env`, `memory/user_settings.json`, API key settings y escritura de secretos en config.
- Tanda 6: consolidacion final. Normalizar dependencias, CI, pyflakes, pyproject y docs de entorno.
- Tanda 7: auditoria final verde. Reejecutar tests de alcance, full suite, static checks, node checks, `git diff --check`, commit y checkpoint/push solo despues de bloque estable.

## Reglas de limpieza posterior

- Borrar solo con evidencia.
- Actualizar solo con contrato vigente.
- Aislar legacy sin hacerlo visible.
- Convertir deuda util en guardrail.
- Cada tanda debe tener tests y commit.
- Checkpoint/push solo despues de bloque estable.
- No mezclar limpieza con implementacion de pantalla, runtime, endpoints o backend operativo.

## Riesgos

- Borrar algo util.
- Actualizar tests ocultando bug real.
- Romper memoria historica.
- Confundir docs historicas con actuales.
- Mezclar limpieza con implementacion.
- Tocar backend operativo.
- Reintroducir runtime.
- Crear falsa sensacion de verde.

## Proximos prompts sugeridos

- `PROMPT IA_CORE 1.78.B - Clasificar y priorizar deuda tecnica global IA_CORE contract-aware sin runtime/no-execution`
- `PROMPT IA_CORE 1.78.C - Limpiar primera tanda de deuda tecnica segura IA_CORE contract-aware sin runtime/no-execution`
- `PROMPT IA_CORE 1.78.D - Checkpoint limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution`

## Cierre 1.78.A

Esta auditoria global profunda queda como inventario inicial para priorizacion posterior. No se borro nada; no se borro nada en minuscula queda repetido como marcador contractual. No se limpio todavia. No se modifico UI activa. No se toco backend operativo. No se toco runtime. No se tocaron endpoints. No se modifico CI. No se instalaron dependencias. No se avanzo a 1.79.

El siguiente prompt exacto queda:

`PROMPT IA_CORE 1.78.B - Clasificar y priorizar deuda tecnica global IA_CORE contract-aware sin runtime/no-execution`
