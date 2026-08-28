# UI/UX Contract Overview Pre-Implementation Guardrails 1.83

## Base y estado

- Base esperada: `476831e`.
- Punto de restauracion: `476831e`.
- Rama: `main`.
- Remoto: `origin` (`https://github.com/IA-MONOPOLY-CORE/IA_CORE`).
- Checkpoint previo: `UI_UX_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_CHECKPOINT_1_82`.
- El arbol debe permanecer limpio antes y despues de este bloque.

Este documento convierte el plan 1.81 y el checkpoint 1.82 en guardrails verificables antes de cualquier implementacion futura de Contract Overview. Es un contrato documental previo; no habilita implementacion por si solo.

## Objetivo

Preparar una especificacion pre-implementacion para `Contract Overview Final Screen Contract` en IA_CORE, manteniendo la pantalla dentro del Panel Maestro, contract-aware, documental y de solo lectura. El objetivo es reducir ambiguedad antes de autorizar una futura implementacion, sin activar runtime, execution, dispatch, endpoints ni fetches nuevos.

## Estado recibido

Las decisiones previas que este bloque conserva son:

- `FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_PLAN_DOCUMENTED`.
- `EXISTING_FINAL_SCREEN_CONTRACTS_READY_FOR_IMPLEMENTATION_PLAN`.
- `NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS`.
- `READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT`.
- Orden futuro: Contract Overview, luego Blocked & Forbidden, luego Validation & Readiness.
- La auditoria previa registra 18 hallazgos residuales de pyflakes, 0 bloqueantes; quedan fuera de este bloque.
- UI activa y backend se conservan intactos.
- Request Contract Preview queda diferido.

## Alcance

Este bloque cubre exclusivamente los guardrails previos de `Contract Overview Screen` y su futura implementacion documental en el Panel Maestro. La identidad contractual es `FSC-CO-01`, con fuente `backend_internal_ui_payload.v1`, orientada a operador/admin interno de IA_CORE.

La pantalla futura debe ser una vista final-documental-no-implementada, de solo lectura, con estados honestos y sin insinuar una operacion ejecutable. No es User Panel, no es una pantalla publica, no es una consola de runtime y no es una vista de resultados o ejecuciones.

## Fuera de alcance obligatorio

- No se implemento pantalla.
- No se modifico UI activa.
- No se creo componente nuevo.
- No se creo User Panel.
- No se crearon rutas/hash.
- No se crearon endpoints.
- No se crearon fetches.
- No se activo runtime.
- No se activo execution.
- No se activo dispatch.
- No se toco backend.
- No se tocaron backend/runtime/endpoints/CI/dependencias.
- No se limpio deuda residual.
- No se corrigieron pyflakes.
- No se modifico CI/dependencias.
- No se hizo push.
- No se avanzo a 1.84.

Las referencias a acciones operativas en este documento son exclusivamente prohibiciones o datos declarados por contrato. No autorizan controles activos.

## Identidad contractual futura

La futura pantalla debe declarar de forma visible:

- Nombre: `Contract Overview Final Screen Contract`.
- ID: `FSC-CO-01`.
- Dominio: IA_CORE.
- Superficie: Panel Maestro.
- Audiencia: operador/admin interno.
- Fuente esperada: `backend_internal_ui_payload.v1`.
- Naturaleza: documental, final, no implementada y de solo lectura.
- Relacion con `backend_internal_ui_request.v1`: solo referencia contractual sin submit ni ejecucion.

No debe presentarse como dashboard operativo, monitor en vivo, launcher, dispatcher, User Panel ni canal publico.

## Datos permitidos

La futura vista puede mostrar solamente datos contractuales, declarados, sanitizados y compatibles con el contrato:

- `schema_version`, `service_kind`, `contract_id`, `source`, `status` y `readiness`.
- Flags contractuales y resultados de validacion.
- `warnings`, `errors` y blockers sanitizados.
- `allowed_actions` como datos declarados por backend, nunca como autorizacion implícita ni como botones operativos.
- `forbidden_actions` y `blocked_capabilities`.
- Resumen, detalle y evidencia documental en forma raw-safe.
- Referencias documentales locales si son seguras y ya existen.

El minimo informativo futuro es: identidad del contrato, fuente, estado, readiness, acciones permitidas declaradas, acciones prohibidas, capacidades bloqueadas, blockers, notas de readiness y evidencia documental. El estado `ready-no-permission` debe seguir siendo visible como falta de permiso para ejecutar, no como invitacion a ejecutar.

Una futura implementacion puede usar fixture o muestra documental local si el prompt de implementacion lo autoriza. No puede agregar endpoint, payload nuevo, fetch ni integracion de backend como parte de este bloque.

## Datos prohibidos

Queda prohibida la exposicion de:

- Secrets, tokens, API keys, `.env`, credentials y configuracion privada raw.
- Handles de runtime, IDs de job, IDs de ejecucion, colas, workers, logs vivos, resultados u outputs operativos.
- Detalles de modelo, tool, provider o integracion que no formen parte del contrato seguro.
- Paquetes raw enviados a User Panel o a una superficie publica.
- Identidad de Loteria, SAAOP u otros dominios legacy como identidad activa de esta pantalla.
- Datos publicos o user-safe no contratados.
- Cualquier valor no declarado, no sanitizado o inventado para llenar un estado vacio.

## Estados visuales permitidos

Los estados permitidos son documentales y de disponibilidad contractual:

`documented`, `ready`, `readiness`, `ready-no-permission`, `blocked`, `forbidden`, `unavailable`, `degraded`, `empty`, `review-required`, `deferred`, `contract-only`, `not-implemented`, `no_payload`, `not_available`, `planned`, `invalid`, `warning`, `error`.

Cuando no haya payload, la pantalla debe explicar que el dato no esta disponible y conservar la identidad contractual. Un estado de validacion no equivale a permiso de ejecucion.

## Estados operativos prohibidos

No se puede mostrar Contract Overview como `active`, `running`, `live`, `executing`, `dispatching`, `submitted`, `processing`, `queued`, `worker-active`, `endpoint-connected`, `user-submitted`, `ready-to-run`, `run-now` o `enabled-runtime`.

Tampoco se permiten `success` o `completed` con significado operacional, ni cualquier estado que sugiera job, worker, endpoint, ejecucion o resultado en vivo. Esas palabras pueden aparecer solo dentro de una lista documental de prohibiciones o en una prueba negativa; nunca como estado activo de la pantalla.

## Acciones visuales permitidas

La futura pantalla puede ofrecer acciones locales, reversibles y de lectura:

- Ver detalles del contrato.
- Ver capacidades bloqueadas.
- Ver acciones prohibidas.
- Ver acciones permitidas cuando esten declaradas como datos.
- Ver notas de readiness y referencias documentales.
- Expandir o contraer informacion local.
- Enfocar, desplazar o filtrar localmente sin ocultar limites criticos.
- Copiar o ver una referencia textual segura y local.

Estas acciones no constituyen autorizacion operacional. `allowed_actions` no se convierte automaticamente en un CTA ni en un boton de ejecucion.

## Acciones prohibidas

La futura pantalla no puede ejecutar, disparar ni habilitar:

- Run, execute, dispatch, submit, send, publish, deploy, trigger o schedule.
- Aprobar ejecucion operacional, unlock, override, bypass o conectar endpoint.
- Probar runtime, generar paquetes operativos o enviar datos a User Panel.
- Mutar backend, entidades, configuracion, providers, tools o integraciones.
- Crear, editar o eliminar recursos.
- Cualquier accion no declarada en el contrato.

Los CTA `Ejecutar`, `Correr`, `Run`, `Start`, `Launch`, `Dispatch`, `Submit`, `Enviar`, `Publicar`, `Activar`, `Desbloquear`, `Override`, `Bypass`, `Procesando`, `En vivo`, `Live`, `Running`, `Success`, `Completed`, `Conectar endpoint`, `Enviar al usuario` y `User Panel` no pueden aparecer como controles activos de Contract Overview.

## Elementos visuales minimos futuros

Una implementacion futura, si se autoriza expresamente, debe contemplar:

- Encabezado contractual y alcance IA_CORE.
- Identidad FSC-CO-01, fuente y naturaleza documental.
- Estado contractual y readiness visible.
- Resumen de capacidades y acciones declaradas.
- Forbidden actions y blockers visibles, no escondidos en un tooltip.
- Distincion explicita entre validacion, readiness y permiso de ejecucion.
- Estado `ready-no-permission` visible cuando corresponda.
- Estado vacio honesto y estado deferred sin datos inventados.
- Referencias documentales seguras.
- Evidencia snapshot documental, nunca live log.
- Nota visible de no-runtime/no-execution.

## Archivos candidatos y archivos vedados

Los candidatos de una futura implementacion, solo con autorizacion explicita, son `ui/web/index.html`, `ui/web/styles.css`, `ui/web/backend-contract-widgets.js`, `ui/web/admin-panels.js`, `ui/web/console-interactions.js`, `ui/web/domains.js`, `ui/web/i18n_es.json`, el test especifico futuro y las referencias de README. La revision actual de esos archivos fue solo contextual; no se modificaron.

Quedan vedados para este bloque y para una futura implementacion Contract Overview sin autorizacion adicional: `api.py`, `core/`, `domains/`, `providers/`, `tools/`, `scripts/`, modelos, integraciones, `.github/workflows/`, `.env`, secrets y manifiestos de dependencias. No se debe ampliar el alcance a backend, runtime, endpoints, CI, dependencias, User Panel, rutas, hash o Request Contract Preview.

## Pruebas minimas futuras

Antes de una implementacion futura se deben exigir pruebas que verifiquen:

- Existencia del documento y del contrato FSC-CO-01.
- IA_CORE y Panel Maestro como identidad activa.
- SAAOP/Loteria y legacy sin identidad activa.
- Ausencia de runtime, execution, dispatch, endpoint, fetch y submit en la superficie futura.
- Ausencia de User Panel y de rutas/hash no autorizados.
- Ausencia de estados operativos y CTA prohibidos.
- Presencia visible de blockers, forbidden actions y `ready-no-permission`.
- Acciones declaradas como datos, sin acciones inventadas ni botones operativos.
- Estado vacio, deferred, invalid, warning y error honestos.
- Evidencia documental snapshot, no log vivo.
- Sintaxis JS, saneamiento CSS y DOM si se llega a tocar HTML/CSS/JS.

Los checks de ausencia de fetch o endpoint deben estar acotados a la futura superficie Contract Overview. La UI activa existente contiene integraciones previas fuera de este alcance; este documento no declara que el repo completo sea fetch-free.

## Criterios de entrada

No se puede iniciar implementacion hasta que:

- El checkpoint 1.82 este publicado y este documento 1.83 este cerrado.
- El arbol este limpio y los tests documentales esten verdes.
- No existan P0/P1 abiertos para este contrato.
- La deuda residual este aceptada como no bloqueante o separada en un prompt propio.
- Un prompt futuro autorice expresamente implementacion de Contract Overview.
- La superficie este limitada al Panel Maestro y a IA_CORE.
- No se agreguen backend, endpoints, fetches, runtime, execution, dispatch, User Panel, rutas ni hash.

## Criterios de salida

Una futura implementacion solo puede cerrarse si:

- No deja ghost UI, CTA ambiguos ni estados operativos insinuados.
- Conserva blockers y forbidden actions visibles.
- Representa readiness y validacion sin convertirlos en permiso.
- Mantiene acciones como datos contractuales, no como autorizacion.
- No agrega endpoint, fetch, runtime, User Panel, ruta o hash fuera de autorizacion.
- Pasa pruebas especificas, checks de sintaxis pertinentes y `git diff --check`.
- Recibe revision visual humana del Panel Maestro.
- Se documenta y se commitea sin push por defecto.

## Registro de riesgos

| ID | Riesgo | Severidad | Bloquea | Mitigacion |
| --- | --- | --- | --- | --- |
| CO-GR-183-001 | Convertir la vista en dashboard operativo | P0 | Si | Identidad documental y estados no operativos visibles |
| CO-GR-183-002 | Convertir `allowed_actions` en CTA | P0 | Si | Mostrar como datos; prohibir botones operativos |
| CO-GR-183-003 | Tratar `ready-no-permission` como permiso | P0 | Si | Separar readiness, validacion y autorizacion |
| CO-GR-183-004 | Agregar endpoint o fetch | P0 | Si | Fixture/documentacion local; checks acotados |
| CO-GR-183-005 | Filtrar datos hacia User Panel | P0 | Si | Mantener Panel Maestro y raw-safe |
| CO-GR-183-006 | Exponer runtime, jobs o logs vivos | P0 | Si | Evidencia snapshot documental |
| CO-GR-183-007 | Ocultar blockers o forbidden actions | P1 | Si | Secciones visibles y estados honestos |
| CO-GR-183-008 | Inventar datos en empty/no-payload | P1 | Si | Empty state explicito y no inferido |
| CO-GR-183-009 | Reintroducir identidad Loteria/legacy | P1 | Si | Assert de identidad IA_CORE y exclusion legacy |
| CO-GR-183-010 | Scope creep hacia Request Contract Preview | P2 | No | Mantenerlo diferido |
| CO-GR-183-011 | Tocar backend, deuda, CI o dependencias | P1 | Si | Lista de archivos vedados y alcance documental |
| CO-GR-183-012 | Presentar estado de validacion como ejecucion | P1 | Si | Texto `validation-not-execution` y `ready-no-permission` |

## Decision

La unica decision final de este bloque es:

`CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`

Este resultado deja listo el contrato previo, no autoriza implementacion directa.

## Siguiente bloque

El siguiente prompt exacto es:

`PROMPT UI/UX 1.84 - Checkpoint guardrails pre-implementacion Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution`

El checkpoint 1.84 debe verificar este documento, su test, la limpieza del arbol, la ausencia de implementacion y la preservacion de todos los limites antes de cualquier autorizacion posterior.

## Veredicto de alcance

- Implementacion: no realizada.
- UI activa: intacta.
- Backend/runtime/endpoints/CI/dependencias: intactos.
- User Panel: no creado.
- Rutas/hash: no creados.
- Push: no realizado.
- Deuda residual: no modificada.
- Pyflakes: no corregidos.
- Decision: `CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
