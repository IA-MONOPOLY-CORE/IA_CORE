# UI/UX Blocked & Forbidden Pre-Implementation Guardrails 1.90

Veredicto: `BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY`

## Base Git y restore point

- Commit base esperado y confirmado: `72affc4`.
- Commit local plan 1.89: `72affc4 docs(ui): planificar siguiente final screen tras contract overview`.
- Restore point remoto vigente: `23f9185`.
- Rama esperada: `main`.
- Estado inicial confirmado: working tree limpio, `main` ahead de `origin/main` por 1 commit.
- Push: pospuesto; 1.90 no publica restore point remoto.

## Objetivo

Preparar guardrails pre-implementacion para la futura `Blocked & Forbidden Capabilities Screen` de IA_CORE. Esta fase baja el plan 1.89 y los contratos 1.68/1.69/1.70 a criterios verificables antes de escribir UI activa.

1.90 es documental y contract-aware. No implementa pantalla, no modifica UI activa, no toca `Contract Overview`, no crea componentes, no crea User Panel, no crea rutas/hash, no crea endpoints ni fetches, no activa backend, runtime, execution, dispatch ni controlled execution.

## Estado recibido

- Decision 1.89: `NEXT_SCREEN_BLOCKED_FORBIDDEN_SELECTED`.
- Baseline visual/contractual: `Contract Overview Screen` cerrada en 1.88, implementada en 1.86, hardenizada en 1.87 y aprobada visualmente por operador.
- Baseline Git: `72affc4` local, restore remoto `23f9185`, `main` ahead de `origin/main` por 1 commit.
- Secuencia futura recibida: 1.90 guardrails, 1.91 plan controlado, 1.92 implementacion, 1.93 hardening, 1.94 checkpoint/push si corresponde.
- Deuda residual heredada: `18` pyflakes documentados en 1.78.K, `0` bloquean UI/UX mientras no se toque backend/runtime/endpoints.

## Base Contract Blocked & Forbidden

- 1.68 audito `Blocked & Forbidden Capabilities Screen Draft` y decidio `BLOCKED_FORBIDDEN_FINAL_CONTRACT_DOCUMENTATION_ALLOWED_NEXT`.
- 1.69 documento `Blocked & Forbidden Final Screen Contract`, contract id `FSC-BF-02`, como contrato final documental, `not implemented`, `Panel Maestro only`.
- 1.70 cerro checkpoint del contrato documental y confirmo ausencia de pantalla activa, User Panel, rutas/hash, endpoints/fetches, runtime/execution, unlock, override, bypass y permission escalation.
- Fuente contractual primaria futura: `backend_internal_ui_payload.v1`.
- Campos criticos heredados: `blocked_capabilities`, `forbidden_actions`, `allowed_actions` como contraste, warnings, errors, validation, readiness, status, flags, summary/detail/raw-safe y referencias documentales.

## Screen identity

La futura pantalla se llama `Blocked & Forbidden Capabilities Screen`. Pertenece al Panel Maestro de IA_CORE, es internal-only, contract-aware, documental/read-only y centrada en limites duros. Su autoridad viene del contrato backend/UI, no de la UI.

Identidad obligatoria futura:

- Nombre visible: `Blocked & Forbidden Capabilities Screen` o variante equivalente sin perder `Blocked & Forbidden`.
- Contrato base: `Blocked & Forbidden Final Screen Contract` / `FSC-BF-02`.
- Surface: `Panel Maestro only`.
- Estado: `read-only`, `no-runtime`, `no-execution`, deny-by-default.
- Relacion con Contract Overview: pantalla especializada posterior, no reemplazo ni mutacion del overview.

## Diferenciacion vs Contract Overview

`Contract Overview` es el mapa general de la superficie contractual: source, status, readiness, validation, actions, blockers y evidencia. `Blocked & Forbidden Capabilities Screen` debe enfocarse en limites duros y lectura de denegaciones.

Diferencias obligatorias:

- Contract Overview resume todo el contrato; Blocked & Forbidden prioriza `blocked_capabilities` y `forbidden_actions`.
- Contract Overview puede mostrar `allowed_actions` como dato; Blocked & Forbidden solo puede usarlas como contraste subordinado y nunca como boton.
- Contract Overview establece baseline visual; Blocked & Forbidden debe usar severidad mas clara para limites, sin parecer alarma operativa ni flujo de reparacion.
- Contract Overview ya esta implementado; 1.90 no debe tocar su markup, copy, estilos ni sincronizacion local.

## Datos permitidos

Datos permitidos para la futura implementacion, siempre como lectura local/documental:

- `backend_internal_ui_payload.v1`.
- `blocked_capabilities` visibles y dominantes.
- `forbidden_actions` visibles y dominantes.
- `allowed_actions` solo como contexto comparativo, no como comandos UI.
- `warnings`, `errors`, `validation`, `readiness`, `status`, `flags` y `service_kind` cuando esten presentes en payload/fixture seguro.
- `schema_version`, contract id, source contract, doc refs y test refs.
- `summary`, `detail` y `raw-safe` sanitizado.
- Razones seguras de bloqueo/prohibicion si ya estan autorizadas por contrato y no revelan informacion sensible.

## Datos prohibidos

Quedan prohibidos para la futura pantalla:

- Secrets, `.env`, credentials, tokens, claves, configuracion privada y datos raw no sanitizados.
- Raw policy reasons sensibles, prompts internos, stack/debug interno y trazas vivas.
- Runtime handles, worker state, queue IDs, job IDs, dispatch payloads, model/tool invocation payloads e integration call metadata.
- Unlock tokens, override flags, bypass hints, escalation metadata y permission request payloads.
- User Panel data y cualquier dato publico/user-facing no contratado.
- Datos inventados para completar estados, timestamps vivos o resultados operativos.

## Estados permitidos

Estados permitidos como semantica documental/no-operativa:

- `final-documental`.
- `final-documental-not-implemented`.
- `not implemented`.
- `read-only`.
- `documented`.
- `blocked`.
- `forbidden`.
- `unavailable`.
- `not_available`.
- `no_payload`.
- `invalid`.
- `failed`.
- `warning`.
- `planned`.
- `ready-no-permission`.
- `no-runtime`.
- `no-execution`.

## Estados prohibidos

Estados prohibidos porque sugieren operacion o permiso:

- `active`.
- `running`.
- `live`.
- `operational`.
- `executing`.
- `dispatching`.
- `submitted`.
- `processing`.
- `enabled`.
- `unlockable`.
- `overridable`.
- `pending permission`.
- `escalation pending`.
- `queued`.
- `sent`.
- `approved-for-execution`.
- `tool-running`.
- `model-running`.

Si alguno aparece en datos fuente futuros, la UI debe tratarlo como texto/diagnostico contractual y no como estado operativo propio.

## Acciones UI prohibidas

La futura pantalla no puede renderizar ni exponer controles para:

- submit, send, execute, dispatch, activate, materialize, lifecycle action, run, operate o approve as operation.
- unlock, override, bypass, allow, enable, grant access, request permission o escalate permission.
- validate domain as operation, repair, retry operation, fix, auto-fix o safe-to-execute.
- mutate state, persist changes, call models, call tools, call integrations.
- create endpoint, create route, create fetch, open User Panel o deep link operativo.

Controles locales permitidos solo en una fase futura autorizada: read, focus, expand/collapse, inspect, group/sort/filter local sin ocultar significado, y copy-safe textual reference.

## Copy permitido

Copy permitido debe ser sobrio, documental y deny-by-default:

- `blocked_capabilities visible; ausencia de lista no desbloquea`.
- `forbidden_actions visibles; lista vacia declarada no concede permiso UI`.
- `read-only / no-runtime / no-execution`.
- `Panel Maestro only`.
- `ready-no-permission`.
- `dato contractual, no accion`.
- `bloqueado por contrato`.
- `prohibido por contrato`.
- `evidencia documental, no log vivo`.

## Copy prohibido

Copy prohibido porque comunica accion, permiso pendiente o desbloqueo:

- `desbloquear`, `unlock`, `habilitar`, `enable`, `allow`, `grant access`.
- `solicitar permiso`, `request permission`, `escalar permiso`, `permission escalation` como accion.
- `ejecutar igual`, `execute anyway`, `run`, `dispatch`, `submit`, `send`.
- `aprobar operacion`, `safe to execute`, `ready to run`, `activar`, `repair`, `fix now`.
- `pronto disponible`, `upgrade to unlock`, `pendiente de permiso`.

Estos terminos pueden aparecer en documentacion o tests solo para declarar prohibiciones, nunca como microcopy accionable futuro.

## Estructura visual futura

La estructura futura minima debe separar lectura critica de contexto:

1. Header compacto con IA_CORE, `FSC-BF-02`, Panel Maestro, `read-only`, `no-runtime`, `no-execution`.
2. Region critica always-visible para `blocked_capabilities`.
3. Region critica always-visible para `forbidden_actions`.
4. Contexto subordinado de `allowed_actions` como datos comparativos.
5. Bloques de warnings/errors/validation/readiness sin comunicar permiso.
6. Evidencia documental con doc refs/test refs y raw-safe sanitizado.
7. Boundary no-unlock/no-override/no-bypass visible.
8. Empty/degraded states deny-by-default.

La pantalla futura no debe ocultar blocked/forbidden por density, mobile, collapse, filtro local o summary corto.

## Visual severity

Severity visual futura:

- `blocked_capabilities`: critical/always-visible, dominante, no alarmista operativo.
- `forbidden_actions`: critical/always-visible, con lenguaje de denegacion contractual.
- warnings/errors: severidad secundaria, no reparacion automatica.
- readiness/validation: informativa, nunca verde de permiso operativo.
- `allowed_actions`: neutra/subordinada, solo dato.
- evidence: documental/snapshot, no timeline vivo.

Cualquier polish visual debe preservar el significado de limite duro. Si una mejora estetica reduce visibilidad o severidad de blocked/forbidden, debe rechazarse.

## Tests futuros minimos

La futura implementacion debe agregar tests que verifiquen:

- Identidad `Blocked & Forbidden Capabilities Screen`, `FSC-BF-02`, IA_CORE y Panel Maestro.
- `blocked_capabilities` y `forbidden_actions` always-visible en DOM.
- `allowed_actions` renderizadas como datos, sin botones ni CTAs.
- No unlock, no override, no bypass, no permission/request access.
- No runtime, no execution, no dispatch, no endpoint, no fetch, no route/hash y no User Panel.
- Estados permitidos/prohibidos y deny-by-default ante dato ausente.
- Responsive/density sin ocultar limites criticos.
- Evidence documental, no live log ni timeline operativo.
- No identidad legacy como UI activa.

## Entry criteria

Para avanzar a 1.91 deben cumplirse:

- Documento 1.90 creado y validado.
- README y `ui/web/README.md` actualizados con cursor 1.90.
- Decision unica dentro de la lista permitida.
- Validaciones requeridas verdes.
- Working tree limpio tras commit local.
- Ninguna modificacion a UI activa, Contract Overview, User Panel, rutas/hash, endpoints/fetches, backend/runtime/CI/dependencias, deuda residual o pyflakes.

## Exit criteria

1.90 queda cerrado si:

- La decision final es `BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
- El proximo prompt exacto queda registrado.
- Se crea commit local con mensaje `docs(ui): preparar guardrails blocked forbidden screen`.
- No se hace push.
- 1.91 queda solo sugerido como siguiente paso, no ejecutado.

## Risk register

| Riesgo | Severidad | Mitigacion 1.90 |
| --- | --- | --- |
| Confundir guardrails con implementacion | P0 | Documento repite no implementacion y tests lo validan. |
| Tocar Contract Overview baseline | P0 | 1.90 declara Contract Overview intocable. |
| Blocked/forbidden ocultos en implementacion futura | P0 | Always-visible como entry/exit criteria futuro. |
| Unlock/override/bypass como CTA | P0 | Acciones y copy prohibidos. |
| Permission escalation leakage | P0 | User Panel y request permission prohibidos. |
| Endpoint/fetch accidental | P0 | no endpoint/no fetch/no runtime en doc/tests. |
| Estado operativo falso | P1 | Estados prohibidos explicitados. |
| Evidence como live log | P1 | Evidence documental/snapshot solamente. |
| Deuda residual tocada fuera de alcance | P1 | 18 pyflakes quedan aceptados/diferidos. |
| Avanzar a 1.91 prematuramente | P1 | 1.91 solo queda como prompt siguiente. |

## Decision final

`BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY`

La decision se elige porque no aparecieron gaps nuevos tras releer 1.89, 1.88, 1.68, 1.69, 1.70, 1.81, 1.82 y 1.78.K. La futura pantalla puede avanzar a plan controlado sin implementar todavia.

## Proximo prompt exacto

`PROMPT UI/UX 1.91 - Preparar plan de implementacion controlada Blocked & Forbidden Capabilities Screen IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- No se implemento pantalla.
- No se modifico UI activa.
- No se toco Contract Overview.
- No se creo componente nuevo.
- No se creo User Panel.
- No se crearon rutas/hash.
- No se crearon endpoints ni fetches.
- No se toco backend operativo.
- No se activo runtime, execution, dispatch ni controlled execution.
- No se modifico `api.py`, `core/`, `domains/`, providers, tools, scripts, modelos ni integraciones.
- No se modifico CI ni dependencias.
- No se limpio deuda residual.
- No se corrigieron pyflakes.
- No se hizo push.
- No se avanzo a 1.91.

## Veredictos

- `BLOCKED_FORBIDDEN_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
- `BLOCKED_FORBIDDEN_SCREEN_IDENTITY_GUARDRAILS_DEFINED`.
- `BLOCKED_FORBIDDEN_DIFFERENTIATION_FROM_CONTRACT_OVERVIEW_DEFINED`.
- `BLOCKED_FORBIDDEN_ALLOWED_DATA_DEFINED`.
- `BLOCKED_FORBIDDEN_FORBIDDEN_DATA_DEFINED`.
- `BLOCKED_FORBIDDEN_ALLOWED_STATES_DEFINED`.
- `BLOCKED_FORBIDDEN_FORBIDDEN_STATES_DEFINED`.
- `BLOCKED_FORBIDDEN_UI_FORBIDDEN_ACTIONS_DEFINED`.
- `BLOCKED_FORBIDDEN_COPY_BOUNDARIES_DEFINED`.
- `BLOCKED_FORBIDDEN_FUTURE_VISUAL_STRUCTURE_DEFINED`.
- `BLOCKED_FORBIDDEN_VISUAL_SEVERITY_DEFINED`.
- `BLOCKED_FORBIDDEN_FUTURE_MINIMUM_TESTS_DEFINED`.
- `BLOCKED_FORBIDDEN_ENTRY_EXIT_CRITERIA_DEFINED`.
- `BLOCKED_FORBIDDEN_RISK_REGISTER_CREATED`.
- `BLOCKED_FORBIDDEN_NO_SCREEN_IMPLEMENTED_CONFIRMED`.
- `BLOCKED_FORBIDDEN_NO_ACTIVE_UI_CHANGE_CONFIRMED`.
- `BLOCKED_FORBIDDEN_CONTRACT_OVERVIEW_UNTOUCHED_CONFIRMED`.
- `BLOCKED_FORBIDDEN_NO_USER_PANEL_ROUTES_HASH_CONFIRMED`.
- `BLOCKED_FORBIDDEN_NO_BACKEND_RUNTIME_ENDPOINTS_CI_DEPENDENCIES_CONFIRMED`.
- `BLOCKED_FORBIDDEN_NO_RESIDUAL_DEBT_OR_PYFLAKES_CHANGE_CONFIRMED`.
- `UI_READY_FOR_BLOCKED_FORBIDDEN_CONTROLLED_IMPLEMENTATION_PLAN_1_91`.
