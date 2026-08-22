# UI/UX Frontend Incongruence Hardening 1.21

Veredicto: `UI_UX_FRONTEND_INCONGRUENCE_HARDENING_COMPLETED`

## Alcance

Este hardening consume `docs/UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md` desde el commit base `b2c2c1ce`. El objetivo fue endurecer o documentar incongruencias P1/P2 del frontend hecho a mano sin redisenar la consola, sin crear pantallas, sin crear rutas, sin agregar endpoints, sin instalar dependencias, sin activar runtime, sin habilitar execution, sin dispatch real y sin controlled execution.

No se tocaron `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones. Se preservaron `backend_internal_ui_payload.v1`, `backend_internal_ui_request.v1`, `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, warnings, errors, validation, flags, readiness, status, service_kind, schema_version, summary/detail/raw-safe, paneles 1.7, navegacion 1.8, sistema 1.9, responsive/accessibility 1.13 y admin boundary 1.17.

## Cambios Aplicados

Veredicto: `FRONTEND_P1_INCONGRUENCES_HARDENED`

- `debate-*` vivo en `index.html`, `styles.css` y `console-interactions.js` fue renombrado a `request-draft-*`.
- `orchestration-*` vivo del panel administrativo fue renombrado a `request-contract-*`.
- `logs-runtime` fue renombrado a `logs-sanitized`, preservando `GET /api/logs` como lectura administrativa preexistente.
- `.status-dot.active` en el stylesheet historico fue reemplazado por `.status-dot.ready`.
- `.active` vivo en tabs/sections/skins de configuracion fue reemplazado por `is-selected` e `is-visible`.
- `activeAgentProfileCatalog` fue renombrado a `currentAgentProfileCatalog`.

Veredictos:

- `DEBATE_LEGACY_FRONTEND_BOUNDARY_HARDENED`
- `ORCHESTRATION_LEGACY_FRONTEND_BOUNDARY_HARDENED`
- `LOGS_RUNTIME_FRONTEND_BOUNDARY_HARDENED`
- `STATUS_DOT_ACTIVE_OPERATIONAL_AMBIGUITY_REMOVED`

## Falsos Positivos Preservados

Veredicto: `FRONTEND_FALSE_POSITIVES_PRESERVED`

- `PROHIBITED_ACTIVE_STATUSES` y listas defensivas equivalentes en `backend-contract-widgets.js` siguen siendo validacion negativa, no estados operativos.
- `block: 'start'` en `console-interactions.js` sigue siendo opcion de `scrollIntoView`, no accion `start`.
- `active_provider`, `active_model`, `status.running`, `overview.orchestrations` y `last_orchestration_ms` en `admin-panels.js` siguen siendo datos backend/status historicos, no autoridad UI.
- Claves i18n historicas `debate.*` y `orchestration.*` no estan enlazadas desde `data-i18n` activo; se preservan para evitar migracion amplia.
- Menciones en docs y tests anteriores siguen siendo historia, fixtures negativos o evidencia de auditoria.

## Limites Confirmados

Veredicto: `FRONTEND_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este hardening no crea endpoint publico, API, router HTTP, hash routing operativo, `/api/debate/start`, `/api/dispatch`, `/api/runtime` ni `/api/execution`. No activa runtime, execution, dispatch real, controlled execution, agentes, models, tools ni integrations.

IA_CORE permanece como identidad visual activa. No se reintroducen SAAOP, S.A.A.O.P., Loteria, lottery, Tactical HUD, U-Score, CAZADOR, ESPEJO ni combinatoria como UI activa.

## Pospuesto

- Limpieza profunda de `ui/web/styles.css` hasta confirmar consumidores fuera de `index.html`.
- Migracion de storage keys como `brand_input` o `ia_core_active_domain`.
- Migracion completa de claves i18n no enlazadas.
- Density reduction, operator guidance, contract storytelling, secondary console views y polish premium.

## Continuidad

Veredicto: `UI_READY_FOR_FRONTEND_INCONGRUENCE_CHECKPOINT`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution`