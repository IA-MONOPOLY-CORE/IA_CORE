# PROMPT 8.7 - Plan de futura UI visual sobre contrato estable

## 1. Proposito

`PROMPT 8.7 - Plan de futura UI visual sobre contrato estable` define como una
futura UI visual podra consumir la exposicion interna controlada de IA_CORE sin
inferir permisos, estados, acciones, confirmaciones ni capabilities.

Este plan cierra la preparacion conceptual de Fase 8 y deja el libro Backend
Interno listo para continuidad del libro UI/UX.

## 2. Alcance

El alcance es documental y de contrato conceptual. Se auditan 8.0-8.6, 7.0,
7.6 y 7.7, se definen reglas para una UI futura y se actualizan planes de
continuidad.

No se implementa UI visual. No se crean frontend, componentes, paginas,
endpoints, API/router HTTP, runtime ni integraciones.

## 3. Estado Previo

Estado previo cerrado:

- `PROMPT 8.6 - Exposure audit checkpoint`
- Commit: `3e0ca8fa`
- Veredicto: `BACKEND_INTERNAL_EXPOSURE_AUDIT_CHECKPOINT_PASSED`
- Readiness: `ready_for_phase_8_7_future_ui_contract_plan`

La cadena confirmada por 8.6 es:

```txt
8.0 plan exposicion
-> 8.1 registry
-> 8.2 request envelope
-> 8.3 dispatcher no-runtime
-> 8.4 confirmation gate
-> 8.5 response adapter
-> 8.6 exposure audit checkpoint
-> 8.7 future UI contract plan
```

## 4. Base Backend Disponible

La futura UI tendra como base:

- `backend_internal_ui_payload.v1`
- `backend_internal_ui_request.v1`
- `internal_exposure_registry`
- `internal_request_validation`
- `internal_dispatcher_no_runtime`
- `internal_confirmation_gate`
- `internal_response_adapter`
- `stable_response_adapter`

La UI futura debe consumir estos campos del payload estable:

- `status`
- `readiness`
- `summary`
- `data`
- `warnings`
- `errors`
- `validation`
- `allowed_actions`
- `forbidden_actions`
- `blocked_capabilities`
- `flags`
- `meta`
- `request_id`
- `operation_id`

## 5. Boundary Backend/UI

Backend decide permisos, readiness, estados, acciones, confirmation rules,
path safety, lifecycle safety, payloads y errores.

La UI futura renderiza solamente lo declarado por backend. La UI no debe
derivar permisos desde texto, nombres de servicio, presencia de componentes,
botones visibles ni nombres de archivos.

En terminos operativos: la UI no debe derivar permisos ni capabilities desde
la forma visual de una pantalla.

## 6. Que Decide Backend

Backend decide:

- que servicio existe;
- si esta `available_now`;
- si esta `planned`;
- si esta bloqueado;
- que action se permite;
- que action se prohibe;
- si requiere confirmation;
- si requiere `validation_payload`;
- si requiere `preview_payload`;
- si requiere `allow_delete` o `allow_reset`;
- si el request es valido;
- si el dispatcher acepta o bloquea;
- si el gate pasa o falla;
- que payload se devuelve;
- que readiness aplica.

## 7. Que Renderiza UI

La UI futura solo renderiza:

- estados declarados por backend;
- acciones declaradas por backend;
- errores declarados por backend;
- warnings declarados por backend;
- confirmations requeridas por backend;
- blocked capabilities declaradas por backend;
- readiness declarado por backend;
- request_id y operation_id si existen.

## 8. Que UI No Puede Inferir

La UI no puede inferir:

- permisos;
- acciones;
- disponibilidad;
- ejecucion;
- confirmaciones;
- readiness;
- capabilities;
- path safety;
- lifecycle safety;
- operational state.

## 9. Stable Payload Contract

La UI futura debe consumir `backend_internal_ui_payload.v1`.

Reglas:

- `allowed_actions` es la unica fuente de acciones renderizables como activas.
- `forbidden_actions` tiene prioridad sobre cualquier accion.
- `blocked_capabilities` usa semantica `true = blocked`.
- `flags` debe mantener `runtime_enabled=false`, `execution_enabled=false`,
  `tools_enabled=false`, `models_enabled=false`, `integrations_enabled=false`,
  `ui_visual=false`, `public_endpoint=false` y `operational=false`.
- `errors` y `warnings` se muestran como backend los entrega.

## 10. Request Envelope Contract

La UI futura solo puede construir requests compatibles con
`backend_internal_ui_request.v1`.

Reglas:

- todo request debe tener `service_id`, `caller`, `payload`, `confirmation`,
  `safety` y `meta`;
- la UI no crea requests manuales fuera de schema;
- la UI no envia flags `*_allowed=true` para desbloquear capabilities;
- la UI no toca paths directamente;
- la UI no toca `domains/` operativo;
- backend valida y decide si el request es aceptado.

## 11. Action Rendering Rules

Una accion visual solo puede mostrarse activa si aparece en `allowed_actions`.

Reglas:

- action no declarada como allowed no se muestra como activa;
- action forbidden nunca se muestra activa;
- action que requiere confirmation abre flujo de confirmacion, no ejecuta
  directo;
- action controlled-write/lifecycle nunca se dispara sin request envelope y
  confirmation gate;
- UI no decide que una accion es segura por nombre.

## 12. Forbidden Action Rules

La UI futura debe ocultar, deshabilitar o marcar como bloqueada toda accion que
aparezca en `forbidden_actions`.

Acciones operativas prohibidas incluyen:

- `activate_runtime`
- `execute_agents`
- `invoke_models`
- `call_tools`
- `use_integrations`
- `open_public_endpoint`
- `open_ui_runtime`
- `touch_operational_domains`

## 13. Blocked Capabilities Rendering

La UI debe mostrar bloqueos desde `blocked_capabilities`.

Regla central:

```txt
true = capability blocked
```

La UI no puede invertir esa semantica ni convertir un capability bloqueado en
accion disponible.

## 14. State/Readiness Rendering

La UI solo puede renderizar estados conocidos por contrato y entregados por
backend.

Estados permitidos:

- `draft`
- `preview_ready`
- `sandbox_materialized`
- `sandbox_validated`
- `sandbox_audited`
- `rollback_ready`
- `rolled_back`
- `regeneration_ready`
- `regenerated`
- `audit_pack_ready`
- `invalid`
- `blocked`
- `pending`
- `ready`
- `passed`
- `failed`
- `planned`
- `not_available`

Estados prohibidos/no renderizables como operativos:

- `active`
- `running`
- `live`
- `operational`
- `executing`
- `production_ready`

Si aparecen, la UI debe renderizar un error contractual o estado bloqueado.

## 15. Confirmation UX Contract

Si backend declara `requires_confirmation=true`, la UI debe pedir confirmacion
humana explicita y construir un envelope con:

- `confirmation.confirmed=true`
- `human_confirmation_required=true`
- `confirmation_scope`
- `confirmed_by`
- `confirmation_id`

Para `delete_sandbox_domain` y `reset_sandbox_domain`, la UI debe pedir
confirmacion fuerte. Delete requiere `allow_delete=true`. Reset requiere
`allow_reset=true`.

Para `materialize_sandbox`, la UI debe mostrar `preview_payload`.

Para lifecycle, la UI debe mostrar `validation_payload`.

La UI no decide si la confirmacion alcanza. Backend valida con
`internal_confirmation_gate`.

## 16. Error/Warning UX Contract

La UI futura debe:

- mostrar errores backend sin inventar causa;
- no mostrar tracebacks crudos;
- mostrar warnings como warnings;
- diferenciar `blocked`, `invalid`, `pending`, `planned` y `not_available`;
- mostrar `request_id` y `operation_id` si existen;
- mostrar readiness;
- mostrar blocked capabilities;
- no transformar errores en permisos.

## 17. Pantallas Conceptuales Futuras

Estas pantallas son conceptuales y no se implementan en 8.7.

| Zona conceptual | Source backend | Payload esperado | Acciones permitidas | Acciones prohibidas | States | Confirmations | Blocked capabilities | Riesgo | Fuera de alcance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Domain/status overview | `list_domains_status` | `backend_internal_ui_payload.v1` | `allowed_actions` read-only | runtime/execution/tools/models | estados backend | no por defecto | mostrar | botones inventados | componentes UI |
| Domain detail / materialization state | status + validation | `backend_internal_ui_payload.v1` | ver detalle | lifecycle directo | contract states | segun backend | mostrar | inferir readiness | pagina real |
| Preview materialization panel | `preview_materialization` | `backend_internal_ui_payload.v1` | ver preview | escribir sin confirmation | `preview_ready`, `invalid` | no ejecuta | mostrar | materializar directo | widget real |
| Validation panel | `validate_domain` | `backend_internal_ui_payload.v1` | ver reporte | reparar/escribir | `sandbox_validated`, `invalid` | no por defecto | mostrar | autocorregir | UI real |
| Team/read model panel | read models sandbox | `backend_internal_ui_payload.v1` | ver equipos | ejecutar equipo | `ready`, `blocked` | no por defecto | mostrar | multiagent real | componentes |
| Audit pack / exposure audit panel | audit pack + 8.6 | `backend_internal_ui_payload.v1` | ver evidencia | abrir runtime | `passed`, `failed` | no por defecto | mostrar | raw Package directo | panel real |
| Controlled action confirmation panel | confirmation gate | `backend_internal_ui_request.v1` + gate result | confirmar segun backend | ejecutar directo | `pending`, `blocked` | si backend requiere | mostrar | bypass gate | modal real |
| Errors/warnings/readiness panel | stable payload | `backend_internal_ui_payload.v1` | ver errores | convertir en permisos | `blocked`, `invalid` | no decide | mostrar | ocultar errores criticos | UI real |
| Blocked capabilities panel | stable payload | `backend_internal_ui_payload.v1` | ver bloqueos | desbloquear | `blocked` | no decide | `true=blocked` | invertir semantica | UI real |
| Developer/internal diagnostics panel | meta/errors | `backend_internal_ui_payload.v1` | ver diagnostico sanitizado | tracebacks/env/secrets | `planned`, `not_available` | no decide | mostrar | filtrar secrets mal | UI real |

## 18. Security/No-Operativity Para UI

La UI futura no puede:

- activar runtime;
- ejecutar agentes;
- invocar modelos;
- llamar tools;
- tocar integraciones;
- abrir endpoints;
- crear API;
- usar browser/network automation;
- tocar env/secrets;
- tocar `domains/` operativo;
- activar Market Catalog runtime;
- activar Business Composition Layer runtime;
- activar OBLITERATUS;
- usar raw Package directo al User Panel.

## 19. Controlled-Write/Lifecycle Desde UI

`materialize_sandbox`, `rollback_sandbox`, `archive_sandbox_domain`,
`delete_sandbox_domain` y `reset_sandbox_domain` pueden aparecer en UI futura
solo como acciones declaradas por backend.

La UI debe construir request envelope, pedir confirmation humana y esperar
validacion de confirmation gate. No ejecuta servicios por si misma.

## 20. No Endpoint/API/Router

8.7 no crea endpoint publico, API real, router HTTP ni private HTTP endpoint.
Cualquier exposicion HTTP futura requiere prompt y contrato aparte.

## 21. No Runtime/Execution/Tools/Models/Integrations

8.7 no activa runtime, execution, dry-run real, agentes, model invocation, tool
invocation ni integrations.

## 22. No `domains/` Operativo

8.7 no toca `domains/` operativo. La UI futura tampoco puede leer ni escribir
paths operativos de dominio por cuenta propia.

## 23. Relacion Con Libro UI/UX

Fase 8 deja listo el contrato backend para retomar el libro UI/UX. El trabajo
UI/UX debe consumir:

- `backend_internal_ui_payload.v1`
- `backend_internal_ui_request.v1`
- action rendering rules;
- confirmation UX contract;
- blocked capabilities;
- readiness;
- backend authority.

## 24. Relacion Con Prompt UI/UX 0.5.3 Widgets

Situacion conocida del libro UI/UX:

- Prompt 0 cerrado.
- Prompt 0.5.1 cerrado.
- Prompt 0.5.2 cerrado.
- Pendiente original: `Prompt 0.5.3 - reconstruir Widgets`.
- Punto extra pendiente: presets automaticos por combinacion
  Rol+Especializacion.

El proximo trabajo recomendado es:

`PROMPT UI/UX 0.5.3 - Reconstruir Widgets con datos reales sobre contrato backend estable`

No se implementa ese prompt en 8.7.

## 25. Riesgos

- Botones fantasma por acciones inferidas.
- Estados visuales no declarados por backend.
- Confundir `true = blocked`.
- Convertir UI en dispatcher operativo.
- Enviar requests fuera de schema.
- Saltar confirmation gate.
- Mostrar tracebacks, env o secrets.
- Exponer raw Package directo al User Panel.

## 26. Deudas No Bloqueantes

- Retomar libro UI/UX desde 0.5.3.
- Definir componentes visuales reales en un prompt separado.
- Definir si habra adapter HTTP futuro sin romper backend authority.
- Documentar presets automaticos Rol+Especializacion en el libro UI/UX.

## 27. Veredicto

`BACKEND_INTERNAL_FUTURE_UI_CONTRACT_PLAN_READY`

`BACKEND_INTERNAL_UI_BOUNDARY_CONFIRMED`

`BACKEND_INTERNAL_UI_NO_INFERENCE_CONFIRMED`

`BACKEND_INTERNAL_PHASE_8_READY_FOR_UI_UX_CONTINUATION`

## 28. Readiness

`ready_for_ui_ux_book_continuation`

## 29. Proximo Prompt Exacto

`PROMPT UI/UX 0.5.3 - Reconstruir Widgets con datos reales sobre contrato backend estable`
