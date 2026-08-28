# IA_CORE Global Technical Debt Cleanup 1.78.C

## Commit Base

- Commit base local: `08755a0`.
- Restore point remoto vigente: `628ab75`.
- Clasificacion base: `IA_CORE_GLOBAL_TECH_DEBT_CLASSIFICATION_1_78_B`.
- Rama: `main`.
- Remoto: `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- Estado inicial: working tree limpio, local ahead de `origin/main` por 2 commits esperados.
- 1.79 sigue diferido.
- No se avanzo a 1.79.
- No push por defecto.

## Objetivo

Ejecutar solo la primera limpieza segura definida en 1.78.B. Esta fase reduce deuda real en tests historicos, cursores documentales y guardrails reutilizables sin tocar UI activa funcional, backend operativo, runtime, endpoints, CI, dependencias, secretos ni grupos excluidos.

## Scope

- Items `ACTIONABLE_IN_1_78_C`.
- Limpieza segura de tests historicos.
- Assertions desfasadas convertidas a guardrails vigentes.
- Cursores/docs si estaban autorizados.
- Pyflakes/imports solo si estaban autorizados y eran test/doc/no-operativos.
- Sin backend operativo salvo correccion estatica segura explicita; en esta ejecucion no se toco backend operativo.
- Sin UI activa funcional.
- Sin runtime/endpoints/CI.

## No-Scope

- No 1.79.
- No limpieza total.
- No `DO_NOT_TOUCH`.
- No se toco `DO_NOT_TOUCH`.
- No `NEEDS_HUMAN_REVIEW`.
- No se toco `NEEDS_HUMAN_REVIEW`.
- No `ACTIONABLE_LATER`.
- No secrets ni `.env`.
- No endpoints.
- No runtime.
- No CI.
- No dependencias.
- No User Panel.
- No pantallas.
- No se toco backend/runtime/endpoints/CI.
- No se modifico UI activa funcional.

## Items autorizados para 1.78.C

| debt_id | area | archivo | categoria | severidad | riesgo | accion autorizada | validacion esperada |
|---|---|---|---|---|---|---|---|
| TD-002 | tests | `tests/` | UPDATE | P1_HIGH | SAFE_TO_UPDATE_CANDIDATE | Tracking paraguas de los fallos historicos, sin edicion directa. | Subset historico y full pytest diagnostico. |
| TD-003 | tests | `tests/test_domains.py` | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Actualizar assertion de widgets hacia guardrail actual. | `python -m pytest tests/test_domains.py -q`. |
| TD-004 | tests | `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py` | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Actualizar microcopy assertions a semantica vigente. | Pytest del archivo y subset historico. |
| TD-005 | tests/docs | tests 1.41, 1.42, 1.43, 1.44, 1.45 | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Reemplazar cursor rigido 1.47 por cursor actual 1.78.C/1.79 diferido. | Tests README/cursor afectados. |
| TD-006 | UI/UX tests | tests 0.8-1.4 | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Actualizar snapshots textuales viejos a guardrails actuales. | Subset UI/UX 0.8-1.4. |
| TD-007 | tests | `tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py` | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Corregir referencia a `current_after_1_63` antes de definicion. | `python -m pyflakes tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py`. |
| TD-009 | calidad Python | tests/docs subset | UPDATE | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | Aplicar solo limpieza estatica segura en tests; excluir core/security/CI. | Pyflakes diagnostico posterior. |
| TD-018 | UI/UX/backend boundary | tests UI/UX | REUSE | P2_MEDIUM | REUSE_AS_GUARDRAIL_CANDIDATE | Reusar fetch allowlist/no-fetch widgets como guardrail. | Tests `fetch(` no widgets/interactions y no endpoints nuevos. |
| TD-019 | UI/UX identity | tests UI/UX | REUSE | P4_HISTORICAL | REUSE_AS_GUARDRAIL_CANDIDATE | Preservar guardrail anti legacy activo. | Tests de identidad IA_CORE y no SAAOP/Loteria/Tactical HUD/U-Score activo. |
| TD-024 | docs | `README.md`, `ui/web/README.md`, tests cursor | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | Actualizar cursor a 1.78.C/1.78.D y mantener 1.79 diferido. | Tests 1.78.A/B/C y grep de next prompt. |

## Items excluidos

| debt_id | motivo | grupo |
|---|---|---|
| TD-001 | Restore point remoto; referencia de rollback. | DO_NOT_TOUCH_CONFIRMED |
| TD-008 | `core/supervisor.py` requiere revision humana aunque pyflakes lo detecta. | HUMAN_REVIEW_REQUIRED |
| TD-010 | Tests raiz ad hoc requieren decision humana antes de mover/aislar. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |
| TD-011 | Borrado local requiere prompt explicito; no entra en 1.78.C. | ACTIONABLE_LATER |
| TD-012 | `.env` local ignorado; no leer, no editar, no revelar. | DO_NOT_TOUCH_CONFIRMED / HUMAN_REVIEW_REQUIRED |
| TD-013 | Config sensible versionada requiere protocolo de seguridad. | HUMAN_REVIEW_REQUIRED |
| TD-014 | Dependencias requieren bloque dedicado. | ACTIONABLE_LATER |
| TD-015 | CI fuera de scope. | HUMAN_REVIEW_REQUIRED |
| TD-016 | UI activa monolitica fuera de scope. | ACTIONABLE_LATER |
| TD-017 | Stylesheet legacy requiere confirmacion posterior. | ACTIONABLE_LATER |
| TD-020 | Agents/domain compatibility requiere revision humana. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |
| TD-021 | Core/domain compatibility requiere revision humana. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |
| TD-022 | Dominio Loteria legacy se preserva como historico no operativo. | ACTIONABLE_LATER |
| TD-023 | Docs legacy raiz pueden romper referencias historicas. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |
| TD-025 | Providers/config requiere revision humana. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |
| TD-026 | API key persistence requiere revision de seguridad. | HUMAN_REVIEW_REQUIRED |
| TD-027 | Contratos backend internos vigentes son fuente de verdad. | DO_NOT_TOUCH_CONFIRMED |
| TD-028 | Caches generados no se borran en 1.78.C. | ACTIONABLE_LATER |
| TD-029 | Fixture generado requiere documentacion posterior. | ACTIONABLE_LATER |
| TD-030 | Tools ejemplo requieren confirmacion de uso. | ACTIONABLE_LATER / HUMAN_REVIEW_REQUIRED |

## Cambios ejecutados

| debt_id | archivo | accion realizada | tipo | evidencia | validacion |
|---|---|---|---|---|---|
| TD-003 | `tests/test_domains.py` | El test de widgets dejo de exigir widgets domain-specific viejos y valida widgets backend-contract vigentes: estado estable, acciones declaradas, warnings/errors, capabilities bloqueadas, dominio activo y providers. | UPDATE | El fallo `Estado del ultimo debate` fue reemplazado por guardrail actual. | Subset historico pasa. |
| TD-004 | `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py` | Se actualizaron strings read-only/admin boundary a copy vigente con acentos, contract preview, no-submit/no-dispatch/no-execution, internal exposure y next step documental actual. | UPDATE | 5 fallos del archivo quedan resueltos sin tocar UI activa. | Subset historico pasa. |
| TD-005 | `tests/test_ui_ux_future_screens_readiness_1_41.py`, `tests/test_ui_ux_future_screens_readiness_checkpoint_1_42.py`, `tests/test_ui_ux_next_block_plan_1_43.py`, `tests/test_ui_ux_component_documentation_style_reference_audit_1_44.py`, `tests/test_ui_ux_component_documentation_style_reference_1_45.py` | Cursor rigido 1.47 reemplazado por cursor actual de deuda tecnica 1.78.C con 1.79 diferido permitido. | UPDATE | Tests historicos dejan de exigir un next step obsoleto. | Subset historico pasa. |
| TD-006 | `tests/test_ui_ux_contract_aware_checkpoint_0_6.py`, `tests/test_ui_ux_main_console_structure_1_0.py`, `tests/test_ui_ux_main_console_refinement_1_1.py`, `tests/test_ui_ux_main_console_flow_1_2.py`, `tests/test_ui_ux_main_console_interaction_model_1_3.py`, `tests/test_ui_ux_main_console_interaction_checkpoint_1_4.py`, `tests/test_ui_ux_superior_layout_0_8.py`, `tests/test_ui_ux_visual_base_checkpoint_0_9.py` | Assertions de layout/copy viejas se actualizaron a `requestDraftPanel`, copy de allowed_actions como dato, no CTA UI, no_payload honesto, true=blocked y evidencia actual. | UPDATE | Fallos de snapshot textual viejo quedan convertidos en guardrails vigentes. | Subset historico pasa. |
| TD-007 | `tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py` | Se elimino el uso de `current_after_1_63` antes de definicion. | UPDATE | `pyflakes` ya no reporta undefined name en ese archivo. | Pyflakes targeted pasa. |
| TD-009 | tests subset | Se hizo limpieza estatica minima solo en test autorizado; no se toco core/backend/security/CI. | UPDATE | Pyflakes global baja el error de `current_after_1_63`; quedan 65 diagnosticos fuera de scope. | Pyflakes diagnostico posterior ejecutado. |
| TD-018 | tests UI/UX | Guardrails actualizados para distinguir no-fetch widgets/interactions, fetches admin heredados y allowed_actions como dato backend-declared. | REUSE | La deuda util se preserva como proteccion anti endpoints/fetches nuevos. | Subset historico pasa. |
| TD-019 | tests UI/UX | Se preservaron checks de identidad IA_CORE y exclusion de SAAOP/Loteria/Tactical HUD/U-Score como UI activa. | REUSE | Legacy sigue documentado como no activo sin tocar UI. | Subset historico pasa. |
| TD-024 | `README.md`, `ui/web/README.md` | Se registrara 1.78.C como limpieza primera tanda segura, 1.79 diferido y proximo prompt 1.78.D. | UPDATE | Cursor documental actualizado por este bloque. | Tests 1.78.C y README/cursor. |

No hubo acciones `ISOLATE` ejecutadas. No hubo acciones `DELETE` ejecutadas. No se borraron archivos.

## Tests/fallos impactados

Antes, segun 1.78.A:

- `5426 passed`.
- `22 failed`.
- `2 skipped`.
- `5 warnings`.

Subset historico antes de la limpieza 1.78.C:

- `22 failed`, `108 passed`, `5 warnings`.

Subset historico despues de la limpieza 1.78.C:

- `130 passed`.
- `5 warnings`.
- Fallos eliminados en subset: 22.

Full pytest diagnostico despues de la limpieza:

- `5461 passed`, `2 skipped`, `5 warnings` en `1200.13s` (`20:00`).
- No hubo fallos en la suite completa.

Fallos que quedan:

- No quedan fallos pytest en `tests/` tras esta tanda.
- Pyflakes conserva 65 diagnosticos fuera de scope, incluyendo `core/supervisor.py`, `api.py`, providers, domains legacy, scripts y tests no priorizados.

## Deuda restante

Restante por categoria:

- `DO_NOT_TOUCH`: TD-001, TD-012, TD-027.
- `HUMAN_REVIEW_REQUIRED`: TD-002 tracking global, TD-008, TD-010, TD-012, TD-013, TD-015, TD-020, TD-021, TD-023, TD-025, TD-026, TD-030.
- `ACTIONABLE_LATER`: TD-010, TD-011, TD-014, TD-016, TD-017, TD-020, TD-021, TD-022, TD-023, TD-025, TD-028, TD-029, TD-030.
- `REUSE` pendiente: TD-029.
- `DELETE` pendiente: TD-011, TD-028, sin borrar en 1.78.C.
- `ISOLATE` pendiente: TD-010, TD-017, TD-022, TD-023, TD-030.

Restante por severidad:

- `P1_HIGH` pendiente: TD-008, TD-012, TD-015, TD-026.
- `P2_MEDIUM` pendiente: TD-013, TD-014, TD-016, TD-020, TD-021, TD-023, TD-025.
- `P3_LOW` pendiente: TD-010, TD-011, TD-017, TD-028, TD-029, TD-030.
- `P4_HISTORICAL` pendiente: TD-001, TD-022, TD-027.

Restante por riesgo:

- `NEEDS_HUMAN_REVIEW`: queda para prompt especifico.
- `LEGACY_ARCHIVE_CANDIDATE`: queda para tanda posterior.
- `SAFE_TO_DELETE_CANDIDATE`: queda para limpieza local explicita.
- `DO_NOT_TOUCH`: confirmado no tocado.

Lo que pasa a 1.78.D: checkpoint de la limpieza, verificacion de resultados, deuda restante y decision de proxima tanda sin abrir 1.79.

## Riesgos y rollback

Riesgos mitigados:

- Tests historicos atados a copy obsoleto.
- Cursor README rigido y atrasado.
- Bug pyflakes de variable indefinida en test 1.57.
- Guardrails anti endpoints/fetches/legacy preservados como tests actuales.

Riesgos residuales:

- Pyflakes global sigue fallando por items fuera de scope.
- Seguridad/config/CI/backend core siguen pendientes.
- Legacy roots, caches, providers y fixtures generados no se movieron ni borraron.
- La suite completa genero cambios locales en archivos de memoria/artefactos de test; quedan preservados fuera del commit por estar fuera del alcance autorizado.

Criterio de rollback:

- Revertir solo el patch del archivo/test que falle.
- No tocar restore point remoto `628ab75`.
- No revertir commits ajenos ni historia git.
- Si una assertion actualizada pierde valor contractual, restaurar la version anterior y documentar exclusion.

Como revertir si algo falla:

- Usar patch especifico sobre el archivo afectado.
- Reejecutar el test asociado al `debt_id`.
- Confirmar `git diff --check`.

## Validaciones

Validaciones de preflight y durante el bloque:

- `git status --short` de preflight: limpio.
- `git rev-parse --short HEAD`: `08755a0`.
- `git branch --show-current`: `main`.
- `git remote -v`: `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- `git fetch origin`: OK.
- `git status`: local ahead de `origin/main` por 2 commits, working tree limpio.
- Subset historico autorizado: `130 passed`, `5 warnings`.
- Pyflakes targeted `tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py tests/test_domains.py tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py`: OK.
- Pyflakes global diagnostico: 65 diagnosticos restantes fuera de scope.

Validaciones finales obligatorias:

- `node --check ui/web/backend-contract-widgets.js`: OK.
- `node --check ui/web/admin-panels.js`: OK.
- `node --check ui/web/console-interactions.js`: OK.
- Tests 1.78.A/B/C: OK (`3`, `5` y `5 passed`).
- Checkpoint UI 1.78: OK (`5 passed`).
- Backup readiness: OK (`2 passed`).
- Contratos backend internos 7.6/8.7: OK (`22 passed`).
- `git diff --check`: OK, con advertencias normales de conversión LF/CRLF de Git en archivos editados.
- Full pytest diagnostico `python -m pytest tests/ -q`: OK (`5461 passed, 2 skipped, 5 warnings`).

## Proximo prompt exacto

`PROMPT IA_CORE 1.78.D - Checkpoint limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution`

## Veredictos

- `IA_CORE_GLOBAL_TECH_DEBT_CLEANUP_1_78_C_COMPLETED`
- `ACTIONABLE_IN_1_78_C_CLEANED_ONLY_CONFIRMED`
- `ACTIONABLE_LATER_NOT_TOUCHED_CONFIRMED`
- `HUMAN_REVIEW_REQUIRED_NOT_TOUCHED_CONFIRMED`
- `DO_NOT_TOUCH_NOT_TOUCHED_CONFIRMED`
- `NO_ACTIVE_UI_FUNCTIONAL_CHANGE_CONFIRMED`
- `NO_BACKEND_RUNTIME_ENDPOINTS_CI_CHANGE_CONFIRMED`
- `NO_ENDPOINT_ROUTE_FETCH_CREATED_CONFIRMED`
- `NO_RUNTIME_EXECUTION_DISPATCH_CONFIRMED`
- `NO_CI_DEPENDENCIES_CHANGE_CONFIRMED`
- `NO_SECRETS_ENV_TOUCHED_CONFIRMED`
- `NO_DELETE_ACTIONS_EXECUTED_CONFIRMED`
- `NO_1_79_ADVANCE_CONFIRMED`
- `NEXT_PROMPT_1_78_D_DEFINED`
