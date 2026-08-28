# IA_CORE Global Technical Debt Classification 1.78.B

## Commit Base

- Commit base local: `541610f`.
- Restore point remoto actual: `628ab75`.
- Auditoria base: `IA_CORE_GLOBAL_TECH_DEBT_AUDIT_1_78_A`.
- Rama esperada: `main`.
- Este bloque es clasificacion y priorizacion. No se borro nada / no se borro nada.
- No se limpio todavia / no se limpio todavia.
- No se modifico UI activa.
- No se toco backend/runtime/endpoints/CI.
- No se avanzo a 1.79.
- Push: no realizado por defecto.

## Objective

Clasificar y priorizar los 30 items de deuda tecnica detectados en 1.78.A para definir que puede entrar en una primera limpieza segura 1.78.C sin romper contratos, sin ejecutar runtime, sin tocar endpoints, sin modificar CI y sin convertir deuda historica en cambios operativos.

## Scope

- Validar los 30 items `TD-001` a `TD-030` de la auditoria 1.78.A.
- Fijar categoria final, severidad final, riesgo final, tanda, accion exacta, validacion posterior, entrada a 1.78.C y necesidad de revision humana.
- Separar deuda accionable en 1.78.C de deuda accionable posterior, revision humana y zonas confirmadas como no tocar.
- Definir el alcance exacto del prompt 1.78.C.
- Actualizar cursores documentales sin limpiar deuda todavia.

## No-Scope

- No borrar archivos, caches, fixtures, tests ni docs.
- No limpiar ni corregir deuda tecnica en 1.78.B.
- No modificar UI activa.
- No tocar backend operativo, runtime, endpoints, rutas, fetches, API, router, integraciones, modelos ni dispatch.
- No modificar CI.
- No instalar dependencias.
- No abrir 1.79 ni cambiar el cursor UI/UX diferido.
- No revelar ni editar `.env`.

## Summary 1.78.A

La auditoria 1.78.A inventario 30 items de deuda tecnica. El barrido diagnostico completo registro `5426 passed`, `22 failed`, `2 skipped`, `5 warnings`.

Conteo por categoria propuesta:

- `REUSE`: 3.
- `UPDATE`: 17.
- `ISOLATE`: 5.
- `DELETE`: 2.
- `DO_NOT_TOUCH`: 3.

Conteo por severidad propuesta:

- `P0_BLOCKER`: 0.
- `P1_HIGH`: 5.
- `P2_MEDIUM`: 13.
- `P3_LOW`: 7.
- `P4_HISTORICAL`: 5.

Conteo por riesgo propuesto:

- `SAFE_TO_DELETE_CANDIDATE`: 2.
- `SAFE_TO_UPDATE_CANDIDATE`: 13.
- `REUSE_AS_GUARDRAIL_CANDIDATE`: 3.
- `LEGACY_ARCHIVE_CANDIDATE`: 5.
- `NEEDS_HUMAN_REVIEW`: 5.
- `DO_NOT_TOUCH`: 2.

## Final Debt Matrix

Esta es la matriz final de clasificacion 1.78.B.

| debt_id | area | archivo/ruta | tipo | descripcion | evidencia | categoria final | severidad final | riesgo final | tanda | accion exacta | validacion posterior | entra en 1.78.C | requiere revision humana | motivo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TD-001 | Git/trazabilidad | repo | restore point | Estado remoto `628ab75` usado como punto de restauracion antes de deuda tecnica. | 1.78.A registra restore point remoto y preflight limpio. | DO_NOT_TOUCH | P4_HISTORICAL | DO_NOT_TOUCH | TANDA_7_FINAL_GREEN_AUDIT | Preservar sin cambios; usar solo como referencia de rollback. | `git log`, `git status`, restore point documentado. | no | no | Es infraestructura de recuperacion, no deuda a limpiar. |
| TD-002 | tests | `tests/` | fallos historicos | Barrido completo falla con 22 tests antiguos de UI/UX y cursor. | `22 failed, 5426 passed, 2 skipped`. | UPDATE | P1_HIGH | SAFE_TO_UPDATE_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Usar como item paraguas; limpiar solo subgrupos explicitados en TD-003 a TD-007 y guardrails relacionados. | Subset de tests 1.78.C y, al final, full pytest diagnostico. | si | si | Entra como tracking P1, pero cada cambio concreto debe ir por subitem seguro. |
| TD-003 | tests | `tests/test_domains.py` | assertion vieja | Espera copy de ultimo debate que ya no representa la UI actual. | Falla `Estado del ultimo debate`. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Revalidar intencion y convertir assertion en guardrail contract-aware actual sin cambiar UI. | `python -m pytest tests/test_domains.py -q`. | si | no | Test historico actualizable sin tocar runtime. |
| TD-004 | tests | `tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py` | assertion vieja | Espera microcopy exacta 1.17 sobre HTML/widgets actuales. | 5 fallos del archivo en barrido completo. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Actualizar assertions hacia semantica vigente o marcar contexto legacy documental. | `python -m pytest tests/test_ui_ux_admin_boundary_exposure_hardening_1_17.py -q`. | si | no | Puede corregirse desde tests/docs, no desde UI activa. |
| TD-005 | tests/docs | tests 1.41-1.45 | cursor viejo | Tests historicos esperan `Next pending step` 1.47 aunque el cursor vigente avanzo. | Fallos README cursor. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_3_DOCS_README_CURSORS | Sustituir expectativa rigida por politica de cursor historico tolerante al avance. | Tests README/cursor afectados y test 1.78.B. | si | no | Cambio documental/test seguro y necesario para evitar falsos rojos. |
| TD-006 | UI/UX tests | tests 0.8-1.4 | layout viejo | Assertions atadas a labels, clases y JS antiguos. | Fallos `debatePanel.classList.add` y labels viejos. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Separar guardrail semantico vigente de snapshot textual viejo. | Subset de tests UI/UX 0.8-1.4 afectados. | si | no | Seguro si no se modifica UI activa. |
| TD-007 | tests | `tests/test_ui_ux_contract_first_screen_contract_drafts_1_57.py` | bug de test | Variable `current_after_1_63` se usa antes de definirse. | `pyflakes` undefined name. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_2_STATIC_PYFLAKES_IMPORTS | Mover definicion antes de uso o ajustar fixture local del test. | `pyflakes` sobre el archivo y pytest del test 1.57. | si | no | Correccion estatica de test sin impacto operativo. |
| TD-008 | core | `core/supervisor.py` | import/runtime latent | `buscar_lecciones_utiles` usado antes de import local. | `pyflakes` undefined name line 741. | UPDATE | P1_HIGH | NEEDS_HUMAN_REVIEW | TANDA_2_STATIC_PYFLAKES_IMPORTS | No tocar en primera tanda; revisar flujo con humano antes de corregir import en core. | `pyflakes core/supervisor.py` y tests core especificos si se aprueba. | no | si | Es backend core latente; riesgo superior al alcance seguro de 1.78.C. |
| TD-009 | calidad Python | varios | higiene estatica | Imports sin uso, shadowing y f-strings sin placeholders. | Lista `pyflakes` de multiples archivos. | UPDATE | P3_LOW | SAFE_TO_UPDATE_CANDIDATE | TANDA_2_STATIC_PYFLAKES_IMPORTS | Limpiar subset mecanico seguro; excluir TD-008 y zonas con secretos/CI. | `pyflakes` subset y `git diff --check`. | si | no | Entra solo la parte mecanica no operativa. |
| TD-010 | tests | `test_debate.py`, `test_demo_generico.py`, `test_respuesta.py` | tests raiz | Tests ad hoc fuera de `tests/`. | `git ls-files` raiz. | ISOLATE | P3_LOW | LEGACY_ARCHIVE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | No mover en 1.78.C; clasificar uso antes de aislar o migrar. | Inventario git y pytest si se migra despues. | no | si | Mover tests raiz puede cambiar descubrimiento y requiere decision humana. |
| TD-011 | artifacts locales | `.testdeps`, `venv`, caches, logs, memoria vectorial | residuos locales | Arbol local pesado ignorado, no versionado. | `git ls-files --others --ignored`. | DELETE | P3_LOW | SAFE_TO_DELETE_CANDIDATE | TANDA_5_ORPHAN_DUPLICATE_FIXTURES | No borrar en 1.78.B ni 1.78.C salvo prompt explicito de limpieza local. | `git status --ignored` despues de aprobacion. | no | no | Seguro conceptualmente, pero borrar artefactos locales no es parte de 1.78.C documental/test. |
| TD-012 | seguridad | `.env` | secreto local | Existe `.env` ignorado con valor no vacio. | Auditoria de presencia sin revelar contenido. | DO_NOT_TOUCH | P1_HIGH | NEEDS_HUMAN_REVIEW | TANDA_6_SECURITY_BOUNDARIES | No leer contenido, no editar, no commitear; revisar rotacion manual si el operador lo decide. | `.gitignore`, `git status --short`, revision humana externa. | no | si | Secreto local: confirmado no tocar. |
| TD-013 | seguridad/config | `memory/user_settings.json` | config sensible | Archivo versionado contiene campo `api_key` aunque vacio. | `git ls-files`, busqueda de secrets. | UPDATE | P2_MEDIUM | NEEDS_HUMAN_REVIEW | TANDA_6_SECURITY_BOUNDARIES | No modificar en 1.78.C; definir template seguro o exclusion en prompt dedicado. | Tests de config y revision humana. | no | si | Cambia politica de secretos/config versionada. |
| TD-014 | dependencias/config | `requirements.txt`, `requirements-api.txt` | duplicacion entorno | Dos sets de dependencias con alcance distinto. | Lectura de requirements. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_7_FINAL_GREEN_AUDIT | Posponer; documentar fuente de verdad antes de tocar dependencias. | Installs/checks dedicados si se aprueba. | no | no | No corresponde a primera tanda porque puede afectar entornos. |
| TD-015 | CI/config | `.github/workflows/ci.yml` | CI estricto inconsistente | CI corre `pyflakes .`, pero pyflakes falla hoy. | `pyflakes` exit 1. | UPDATE | P1_HIGH | NEEDS_HUMAN_REVIEW | TANDA_7_FINAL_GREEN_AUDIT | No tocar CI en 1.78.C; resolver deuda estatica primero o ajustar alcance con decision humana. | CI local/simulacion y revision humana. | no | si | CI esta fuera de scope explicito. |
| TD-016 | UI/UX | `ui/web/index.html` | monolito | HTML activo muy grande con CSS/JS inline. | Inventario `ui/web`. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_7_FINAL_GREEN_AUDIT | Posponer extraccion; no tocar UI activa en 1.78.C. | Node checks y comparacion visual futura. | no | no | Refactor de UI activa requiere bloque dedicado. |
| TD-017 | UI/UX | `ui/web/styles.css` | posible stylesheet legacy | Existe y tests/docs lo referencian, pero `index.html` no lo linkea. | `rg styles.css` sin link HTML. | ISOLATE | P3_LOW | LEGACY_ARCHIVE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | No archivar aun; confirmar uso real y dependencias de tests. | `rg styles.css`, tests UI/UX historicos. | no | no | Puede quedar para tanda posterior de aislamiento. |
| TD-018 | UI/UX/backend boundary | `ui/web/admin-panels.js`, `domains.js`, `index.html` | fetch allowlist | Fetches heredados/admin deben distinguirse de fetch contract-aware nuevo. | `rg "fetch(" ui/web`. | REUSE | P2_MEDIUM | REUSE_AS_GUARDRAIL_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Convertir allowlist en guardrail documental/test sin tocar fetches. | Tests estaticos UI/UX de no endpoint/fetch nuevo. | si | no | Buen guardrail para mantener frontera contract-aware. |
| TD-019 | UI/UX identity | `ui/web/` | guardrail vigente | No hay SAAOP/Loteria/Tactical HUD/U-Score en UI activa. | `rg legacy ui/web` sin matches relevantes. | REUSE | P4_HISTORICAL | REUSE_AS_GUARDRAIL_CANDIDATE | TANDA_1_TESTS_HISTORICOS | Preservar como test anti legacy activo. | Test de identidad UI activa. | si | no | Reutiliza deuda historica como proteccion actual. |
| TD-020 | agents | `agents/prompts.py`, `agents/runtime_json_agent.py` | acoplamiento dominio | Imports directos a `domains.loteria` por compatibilidad. | `rg` legacy en agents. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | Posponer; encapsular resolver por dominio en bloque backend/domain dedicado. | Tests agents/domains si se aprueba. | no | si | Puede alterar compatibilidad y comportamiento de agentes. |
| TD-021 | core | `core/debate.py`, `core/supervisor.py`, `core/model_recommendation.py` | fallback legacy | Defaults perezosos a Loteria siguen en core. | `rg` legacy en core. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | Posponer; aislar defaults sin romper compatibilidad en bloque especifico. | Tests core/debate/supervisor. | no | si | Toca core y defaults de dominio. |
| TD-022 | domains | `domains/loteria/` | legacy versionado | Dominio Loteria preservado como legacy. | `domain.json` status legacy. | ISOLATE | P4_HISTORICAL | LEGACY_ARCHIVE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | Mantener como archivo historico no operativo. | Tests de no UI activa legacy y docs de legacy. | no | no | Clasificacion suficiente; no mover en 1.78.C. |
| TD-023 | docs | `MAPA_CORE_VS_LOTERIA.md`, `RESPONSESCORE_USOS.md` | docs legacy raiz | Docs historicas en raiz pueden confundirse con verdad vigente. | `git ls-files` raiz. | ISOLATE | P4_HISTORICAL | LEGACY_ARCHIVE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | Posponer; mover o prefijar como legacy solo con revision humana. | `rg` README/docs y links. | no | si | Puede romper referencias historicas. |
| TD-024 | docs | `README.md`, `ui/web/README.md`, docs UI/UX | cursor/documentacion larga | Timeline largo y cursores pausados en 1.78.A/1.78.B. | README y UI README leidos. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_3_DOCS_README_CURSORS | Mantener cursor actual 1.78.B y siguiente 1.78.C; 1.79 diferido. | Tests 1.78.A/1.78.B y grep de next prompt. | si | no | Cambio documental seguro y parte del prompt actual. |
| TD-025 | providers | `providers/*_provider.py` | placeholders | Proveedores cloud placeholder conviven con config real NVIDIA. | `rg placeholder providers`. | UPDATE | P2_MEDIUM | SAFE_TO_UPDATE_CANDIDATE | TANDA_6_SECURITY_BOUNDARIES | Posponer; documentar estado o aislar mocks tras revision. | Tests providers/config. | no | si | Cruza proveedores y configuracion real. |
| TD-026 | seguridad/backend | `api.py`, `config.py` | API key persistence | Endpoint settings puede escribir API key en `config.py`. | `rg api_key` / `NVIDIA_API_KEY`. | UPDATE | P1_HIGH | NEEDS_HUMAN_REVIEW | TANDA_6_SECURITY_BOUNDARIES | No tocar en 1.78.C; abrir prompt especifico de manejo de secretos. | Tests API/config y revision manual de seguridad. | no | si | Riesgo alto de seguridad/backend. |
| TD-027 | backend/contracts | `core/backend_internal_*`, docs 7.x/8.x | contrato vigente | Contratos backend internos son fuente de verdad estable. | Tests contractuales vigentes. | DO_NOT_TOUCH | P4_HISTORICAL | DO_NOT_TOUCH | TANDA_7_FINAL_GREEN_AUDIT | No tocar salvo prompt contractual especifico. | Tests backend internos 7.6/8.7. | no | no | Es autoridad vigente, no deuda limpiable. |
| TD-028 | artifacts locales | `__pycache__`, `.pytest_cache`, `.ruff_cache` | caches | Caches generados no versionados. | Ignored files listing. | DELETE | P3_LOW | SAFE_TO_DELETE_CANDIDATE | TANDA_5_ORPHAN_DUPLICATE_FIXTURES | No borrar en 1.78.B; permitir solo en limpieza local explicita. | `git status --ignored` despues de aprobacion. | no | no | Borrable, pero fuera de primera tanda contract-aware. |
| TD-029 | fixtures/data | `data/market_catalog/market_catalog.generated.json` | generated data | Archivo generado versionado necesita razon y test. | `git ls-files data/...`. | REUSE | P3_LOW | REUSE_AS_GUARDRAIL_CANDIDATE | TANDA_5_ORPHAN_DUPLICATE_FIXTURES | Posponer; documentar origen y uso como fixture contractual. | Tests de fixture/catalogo si existen. | no | no | Reutilizable, pero no prioritario para 1.78.C. |
| TD-030 | tools | `tools/modules/echo.py`, `tools/modules/uppercase.py` | ejemplos | Modulos simples pueden ser demos o residuo. | Inventario tools. | ISOLATE | P3_LOW | LEGACY_ARCHIVE_CANDIDATE | TANDA_4_LEGACY_IDENTITY_ISOLATION | Posponer; confirmar si son ejemplos, fixtures o tools vigentes. | Tests tools/registry antes de mover. | no | si | Puede romper ejemplos o registros de herramientas. |

## Classification Changes

No hay cambios de categoria, severidad ni riesgo final respecto de 1.78.A. La clasificacion 1.78.B confirma los valores propuestos y agrega prioridad operacional: tanda, accion exacta, validacion posterior, entrada a 1.78.C y revision humana.

| item | cambio | razon |
|---|---|---|
| TD-001 a TD-030 | Sin cambios en categoria/severidad/riesgo. | 1.78.A ya separo correctamente deuda segura, historica, reutilizable, eliminable y no tocable. |
| TD-002 | Entra en 1.78.C solo como tracking paraguas. | El arreglo real debe operar sobre subitems seguros para evitar maquillaje del full suite. |
| TD-008 | Excluido de 1.78.C aunque estaba propuesto para 1.78.C. | Toca `core/supervisor.py`; requiere revision humana por riesgo backend. |
| TD-010 | Excluido de 1.78.C. | Tests raiz ad hoc pueden depender de flujos no documentados. |
| TD-011 y TD-028 | Excluidos de 1.78.C. | Borrado local requiere prompt explicito de limpieza, no clasificacion. |
| TD-013, TD-015, TD-026 | Excluidos de 1.78.C. | Seguridad/CI/backend requieren decision humana. |

## Final Groups

### ACTIONABLE_IN_1_78_C

- `TD-002`: tracking paraguas de fallos historicos, sin edicion directa.
- `TD-003`: actualizar test `tests/test_domains.py` hacia guardrail actual.
- `TD-004`: actualizar test admin boundary 1.17 hacia semantica vigente.
- `TD-005`: corregir politica de cursor README en tests historicos.
- `TD-006`: desacoplar tests 0.8-1.4 de snapshots UI viejos.
- `TD-007`: corregir variable indefinida en test 1.57.
- `TD-009`: limpiar solo pyflakes mecanico seguro, excluyendo core/security/CI.
- `TD-018`: convertir fetch allowlist en guardrail.
- `TD-019`: preservar test anti legacy activo.
- `TD-024`: actualizar cursor documental a 1.78.B / 1.78.C y mantener 1.79 diferido.

### ACTIONABLE_LATER

- `TD-010`: aislar tests raiz ad hoc.
- `TD-011`: borrar residuos locales ignorados solo con prompt explicito.
- `TD-014`: ordenar dependencias y fuente de verdad.
- `TD-016`: planear extraccion del monolito UI activo.
- `TD-017`: confirmar/aislar stylesheet legacy.
- `TD-020`: resolver acoplamiento dominio en agents.
- `TD-021`: aislar fallbacks legacy en core.
- `TD-022`: mantener dominio Loteria como legacy no operativo.
- `TD-023`: aislar docs legacy raiz.
- `TD-025`: ordenar providers placeholders.
- `TD-028`: borrar caches ignorados solo con prompt explicito.
- `TD-029`: documentar fixture generado.
- `TD-030`: clasificar tools ejemplo.

### HUMAN_REVIEW_REQUIRED

- `TD-002`: solo por impacto global del full suite.
- `TD-008`: `core/supervisor.py`.
- `TD-010`: tests raiz fuera de convencion.
- `TD-012`: `.env`.
- `TD-013`: config sensible versionada.
- `TD-015`: CI.
- `TD-020`: agents/domain compatibility.
- `TD-021`: core/domain compatibility.
- `TD-023`: docs raiz con posible referencia historica.
- `TD-025`: providers/config.
- `TD-026`: API key persistence.
- `TD-030`: tools modules.

### DO_NOT_TOUCH_CONFIRMED

- `TD-001`: restore point remoto `628ab75`.
- `TD-012`: `.env` local ignorado.
- `TD-027`: contratos backend internos vigentes.

## 1.78.C Prioritization

Objetivo exacto de 1.78.C: limpiar primera tanda segura de deuda tecnica contract-aware, limitada a tests/documentacion/guardrails y pyflakes mecanico no operativo. 1.78.C debe intentar reducir fallos historicos sin tocar UI activa, backend operativo, runtime, endpoints ni CI.

Orden exacto:

1. `TD-024`: actualizar cursor documental y README policy: 1.79 sigue diferido, siguiente exacto 1.78.C, no cleanup previo.
2. `TD-007`: corregir variable indefinida en test 1.57.
3. `TD-003`: actualizar test de domains a semantica vigente.
4. `TD-004`: actualizar test admin boundary 1.17.
5. `TD-005`: corregir tests historicos de cursor README.
6. `TD-006`: actualizar tests UI/UX 0.8-1.4 para guardrails actuales.
7. `TD-018`: crear o ajustar guardrail de fetch allowlist sin tocar fetches activos.
8. `TD-019`: preservar guardrail anti legacy visible.
9. `TD-009`: aplicar limpieza pyflakes solo en archivos no operativos o tests, excluyendo `core/supervisor.py`, `api.py`, `config.py`, providers y CI.
10. `TD-002`: re-ejecutar como medicion paraguas, no como edicion directa.

Limites 1.78.C:

- No tocar `.env`.
- No modificar `core/supervisor.py` por TD-008.
- No tocar `api.py`, `config.py`, providers ni `.github/workflows/ci.yml`.
- No borrar caches ni artefactos locales.
- No mover archivos legacy.
- No modificar UI activa salvo que el prompt futuro lo autorice expresamente; para 1.78.C, cambios permitidos deben quedarse en tests/docs/guardrails.
- No avanzar a 1.79.

Validaciones esperadas 1.78.C:

- `node --check ui/web/backend-contract-widgets.js`.
- `node --check ui/web/admin-panels.js`.
- `node --check ui/web/console-interactions.js`.
- Tests especificos tocados por 1.78.C.
- Test 1.78.A y test 1.78.B.
- `python -m pytest tests/test_ui_ux_validation_readiness_final_screen_contract_checkpoint_1_78.py -q`.
- `python -m pytest tests/test_ia_core_github_backup_readiness.py -q`.
- `python -m pytest tests/test_backend_internal_future_ui_contract_plan_8_7.py tests/test_backend_internal_ui_payloads_7_6.py -q`.
- `git diff --check`.
- Full pytest diagnostico solo al cierre de tanda si el prompt 1.78.C lo solicita.

Rollback:

- Antes de 1.78.C confirmar `git status --short`.
- Si un cambio de test altera semantica vigente, revertir solo ese cambio con patch especifico.
- Restore point remoto: `628ab75`.
- Commit base local para 1.78.C: el commit de 1.78.B.

Close criteria:

- Todos los tests documentales 1.78.A/1.78.B pasan.
- Los tests tocados por 1.78.C pasan individualmente.
- No hay cambios en runtime, endpoints, CI, secretos ni UI activa.
- El reporte de 1.78.C lista que deuda queda pendiente.
- 1.79 permanece diferido.

## Cleanup Rules For 1.78.C

- Limpiar solo deuda segura incluida en `ACTIONABLE_IN_1_78_C`.
- Priorizar `P1_HIGH`/`P2_MEDIUM` solo cuando la accion sea test/doc/guardrail segura.
- Si un item requiere revision humana, no se limpia en 1.78.C.
- No usar eliminaciones masivas.
- No normalizar historia documental antigua salvo tests de cursor explicitamente incluidos.
- No cambiar contratos backend internos.
- No maquillar fallos: cada test actualizado debe conservar un guardrail valido.
- Mantener IA_CORE como identidad activa.
- Mantener SAAOP/Loteria/Tactical HUD/U-Score fuera de UI activa.
- No convertir `allowed_actions` en permisos UI.
- No convertir readiness en ejecucion ni `validation.valid` en safe-to-execute.

## Risks

| riesgo | severidad | mitigacion |
|---|---|---|
| Cambiar tests viejos y perder guardrails utiles. | Alta | Reescribir assertions hacia semantica vigente, no eliminar cobertura sin reemplazo. |
| Tocar core por resolver pyflakes rapido. | Alta | Excluir TD-008 de 1.78.C y requerir revision humana. |
| Confundir caches borrables con tarea actual. | Media | TD-011/TD-028 quedan fuera de 1.78.C. |
| Mover legacy y romper referencias historicas. | Media | TD-010/TD-017/TD-022/TD-023/TD-030 quedan para tanda posterior. |
| Abrir secretos/config sin protocolo. | Alta | TD-012/TD-013/TD-026 requieren revision humana y no se tocan. |
| Ajustar CI antes de arreglar deuda. | Alta | TD-015 queda fuera de scope. |
| Desbloquear 1.79 prematuramente. | Media | README mantiene 1.79 diferido hasta cierre de deuda tecnica. |

## Next Exact Prompt

`PROMPT IA_CORE 1.78.C - Limpiar primera tanda de deuda tecnica segura IA_CORE contract-aware sin runtime/no-execution`

## Veredictos

- `IA_CORE_GLOBAL_TECH_DEBT_CLASSIFICATION_1_78_B_COMPLETED`
- `THIRTY_TECH_DEBT_ITEMS_CLASSIFIED_CONFIRMED`
- `COMMIT_BASE_541610F_CONFIRMED`
- `REMOTE_RESTORE_POINT_628AB75_CONFIRMED`
- `BASE_AUDIT_IA_CORE_GLOBAL_TECH_DEBT_AUDIT_1_78_A_CONFIRMED`
- `NO_DEBT_CLEANUP_PERFORMED_CONFIRMED`
- `NO_FILES_DELETED_CONFIRMED`
- `NO_ACTIVE_UI_CHANGE_CONFIRMED`
- `NO_BACKEND_RUNTIME_ENDPOINTS_CI_CHANGE_CONFIRMED`
- `NO_1_79_ADVANCE_CONFIRMED`
- `ACTIONABLE_IN_1_78_C_DEFINED`
- `ACTIONABLE_LATER_DEFINED`
- `HUMAN_REVIEW_REQUIRED_DEFINED`
- `DO_NOT_TOUCH_CONFIRMED_DEFINED`
- `NEXT_PROMPT_1_78_C_DEFINED`
