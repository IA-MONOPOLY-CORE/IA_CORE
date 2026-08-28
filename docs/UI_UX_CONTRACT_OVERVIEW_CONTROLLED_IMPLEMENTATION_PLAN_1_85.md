# UI/UX Contract Overview Controlled Implementation Plan 1.85

## Commit base

- Base esperada: `d20a5d1`.
- Restore point remoto vigente: `d20a5d1`.
- Checkpoint base: `UI_UX_CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_CHECKPOINT_1_84`.
- Rama de referencia: `main`.
- Este documento prepara el trabajo futuro; no modifica la UI activa ni autoriza por si solo una implementacion.

## Objetivo

Preparar el plan de implementacion controlada de la futura `Contract Overview Screen` de IA_CORE. El plan baja los guardrails 1.83 y el checkpoint 1.84 a una superficie implementable, verificable y reversible, limitada al Panel Maestro, documental, contract-aware y de solo lectura.

La implementacion futura solo podra comenzar mediante un prompt posterior que la autorice expresamente y con aprobacion humana. Este bloque no implementa pantalla.

## Estado recibido

- Decision vigente de 1.83/1.84: `CONTRACT_OVERVIEW_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
- Contrato base: `FSC-CO-01`.
- Fuente contractual: `backend_internal_ui_payload.v1`.
- Superficie: Panel Maestro.
- Vista futura: vista documental, final y de solo lectura.
- Restore point: `d20a5d1`.
- UI activa intacta.
- Backend operativo intacto.
- `allowed_actions` son datos contractuales y no son botones de ejecucion.
- Blockers y `forbidden_actions` deben ser visibles.
- La evidencia es snapshot documental, no log vivo.
- User Panel, runtime, endpoints y fetches siguen fuera de alcance.

## Alcance implementable futuro

El futuro prompt de implementacion podra implementar exclusivamente:

- La superficie visual de `Contract Overview Screen` dentro del Panel Maestro existente.
- Lectura de datos contract-aware ya disponibles o de fixtures/documentos estaticos y documentales existentes.
- Resumen de identidad, fuente, contrato, status, readiness, validation, warnings y errors sanitizados.
- `blocked_capabilities` visibles y con lectura deny-by-default.
- `forbidden_actions` visibles.
- `allowed_actions` como datos declarados en un bloque de solo lectura, nunca como botones.
- Estado `ready-no-permission` con explicacion de que readiness no es permiso de ejecucion.
- Evidencia como snapshot documental.
- Empty state honesto, degraded, deferred y review required.
- Referencias documentales locales y controles locales de inspeccion, expandir/contraer o foco.
- Copy contractual en espanol reutilizando el catalogo existente cuando corresponda.

El alcance no incluye nueva fuente de datos. Si no hay payload seguro, la pantalla debe mostrar `no_payload`, `not_available` o un estado equivalente sin inventar datos ni inferir permisos.

## Alcance prohibido futuro

El futuro prompt no podra implementar ni introducir:

- Ejecucion, run, dispatch, submit, trigger, publish, deploy, unlock, override o bypass.
- Endpoint, fetch, worker, queue, scheduler, polling, live refresh o runtime.
- User Panel, superficie publica o envio de datos fuera del Panel Maestro.
- Rutas/hash nuevas, salvo autorizacion futura explicita y separada.
- Cambios de backend, `api.py`, `core/`, `domains/`, providers, scripts, tools, modelos o integraciones.
- Cambios de CI o dependencias.
- Datos inventados, mocks que parezcan reales, logs vivos o resultados operativos.
- Estados `running`, `live`, `executing`, `dispatching`, `submitted`, `processing`, `job queued`, `worker active`, `endpoint connected`, `success` operativo o `completed` operativo.
- Cambios en Blocked & Forbidden, Validation & Readiness o Request Contract Preview.
- Navegacion global nueva o un componente compartido amplio.

## Candidate future implementation files

La futura implementacion debe limitarse a estos archivos candidatos, solo cuando el cambio este justificado por el contrato:

| Archivo | Razon | Cambio permitido | Cambio prohibido | Riesgo |
| --- | --- | --- | --- | --- |
| `ui/web/index.html` | Contiene la superficie documental existente y sus puntos de insercion | Marcar o ajustar markup local de Contract Overview, secciones semanticas y estados | Crear pantalla paralela, User Panel, ruta/hash, otros final contracts o CTAs operativos | Medio |
| `ui/web/styles.css` | Aloja estilos de consola y puede soportar la jerarquia visual | Estilos scoped para header, estados, blockers, evidencia y empty state | Rediseño global, estilos operativos ambiguos o ocultar limites criticos | Medio |
| `ui/web/backend-contract-widgets.js` | Ya normaliza datos contract-aware locales | Ajustar lectura/render read-only de payload ya disponible y deny-by-default | Agregar fetch, endpoint, runtime, polling, dispatch o permiso UI | Alto |
| `ui/web/admin-panels.js` | Puede contener el contenedor interno del Panel Maestro | Integrar inspeccion local dentro del contenedor existente si es necesario | Crear User Panel, submit, backend mutation, request preview o navegacion nueva | Alto |
| `ui/web/console-interactions.js` | Contiene interacciones de consola existentes | Bindings locales de collapse, focus, scroll o inspeccion sin mutacion | Rutas, hash, acciones operativas, dispatch o controles de ejecucion | Medio |
| `ui/web/i18n_es.json` | Es el catalogo de copy de la consola | Agregar o reutilizar textos documentales, read-only y contract-aware | Copy de activacion, exito operativo, live state o permiso implicito | Medio |
| `tests/test_ui_ux_contract_overview_controlled_implementation_*.py` | Verifica el contrato y los limites de la futura implementacion | Tests documentales, estaticos, DOM y de regresion scoped | Tests que habiliten runtime o requieran backend nuevo | Bajo |

`ui/web/domains.js` se reviso solo como contexto. No es candidato de 1.86 salvo autorizacion explicita y separada; no se debe tocar para resolver una necesidad visual de Contract Overview.

## Prohibited files

| Archivo/zona | Motivo | Condicion excepcional |
| --- | --- | --- |
| `api.py` | Podria introducir endpoints o comportamiento operativo | Ninguna dentro de este plan |
| `core/` | Contiene logica de dominio/runtime fuera de la vista | Ninguna dentro de este plan |
| `domains/` | Cambiaria dominios y contratos operativos | Solo otro prompt con alcance propio |
| `providers/` | Podria activar integraciones o proveedores | Solo otro prompt con alcance propio |
| `tools/` | Podria activar herramientas o dispatch | Solo otro prompt con alcance propio |
| `scripts/` | Podria introducir automatizacion o ejecucion | Solo otro prompt con alcance propio |
| Modelos e integraciones | Alterarian contratos o runtime | Solo otro prompt con contrato aprobado |
| `.github/workflows/` y CI | Cambiaria automatizacion del repositorio | Solo otro prompt de CI |
| `.env`, secrets, tokens y API keys | Son datos sensibles fuera de la vista | Nunca leer, revelar ni manipular |
| Manifiestos de dependencias | Cambiarian el entorno y el alcance | Solo otro prompt explicito |

## Future visual structure

La estructura futura prevista, sin implementarla en 1.85, es:

1. Header contractual: nombre `Contract Overview`, `FSC-CO-01`, IA_CORE y etiqueta Panel Maestro.
2. Status strip: status, readiness y validation en lenguaje documental.
3. Contract identity block: contract ID, service kind, source y naturaleza final/documental.
4. Data source block: `backend_internal_ui_payload.v1`, alcance de lectura y estado del payload.
5. Readiness vs permission explanation: `ready-no-permission` visible y separado de cualquier permiso operacional.
6. Allowed actions read-only block: acciones declaradas como datos, sin botones de ejecucion.
7. Forbidden actions block: prohibiciones visibles y sin ocultamiento.
8. Blocked capabilities block: capacidades bloqueadas, `true = blocked` y deny-by-default.
9. Evidence snapshot block: evidencia documental sanitizada, nunca log vivo.
10. No-scope / not-runtime block: no runtime, no execution, no dispatch, no endpoint y no User Panel.
11. Empty/degraded/deferred state: estados honestos, sin datos inventados.
12. Documentation references: referencias locales seguras y trazables.
13. Footer note: vista de solo lectura y validacion no equivalente a ejecucion.

La implementacion futura debe reutilizar el contenedor y patrones existentes cuando sea posible, sin crear una navegacion global nueva ni un componente compartido amplio.

## Future states

Estados contractuales permitidos:

- Normal/documented.
- Empty / `no_payload` / `not_available`.
- Degraded.
- Review required.
- Blocked.
- Forbidden.
- Deferred.
- Not implemented.
- Ready documental.
- `ready-no-permission`.
- Invalid, warning y error declarados.

Estados prohibidos:

- Active.
- Running.
- Live.
- Executing.
- Dispatching.
- Submitted.
- Processing.
- Completed operativo.
- Success operativo.
- Job queued.
- Worker active.
- Endpoint connected.
- Ready to run.

Ningun estado visual puede sugerir que el sistema esta ejecutando, esperando ejecucion, conectado a un endpoint o listo para correr una operacion.

## Copy policy

Copy permitido:

- Claro, breve, documental, contractual y de solo lectura.
- Orientado a explicar fuente, estado, readiness, blockers y limites.
- Honesto frente a ausencia de payload, datos diferidos o validacion pendiente.
- Explicitamente separado de permiso de ejecucion.
- Compatible con IA_CORE, Panel Maestro y `FSC-CO-01`.

Copy prohibido como control o estado activo:

`Ejecutar`, `Correr`, `Run`, `Start`, `Launch`, `Dispatch`, `Submit`, `Enviar`, `Publicar`, `Activar`, `Desbloquear`, `Override`, `Bypass`, `Procesando`, `En vivo`, `Live`, `Running`, `Success`, `Completed`, `Conectar endpoint`, `Enviar al usuario`, `User Panel`, `Listo para ejecutar` y `Ready to run`.

Estas expresiones solo pueden aparecer en una prueba negativa o en una declaracion de prohibicion; nunca como CTA, estado activo o promesa visual.

## Future tests required

La futura implementacion debe incluir como minimo:

- Test documental de implementacion y de identidad `FSC-CO-01`.
- Static test de no fetch en la superficie Contract Overview.
- Static test de no endpoint.
- Static test de no runtime words y no estados operativos.
- Static test de no User Panel.
- Static test de no prohibited CTAs.
- Static test de `allowed_actions` read-only y sin botones de ejecucion.
- Static test de `blocked_capabilities` visible.
- Static test de `forbidden_actions` visible.
- Static test de identidad IA_CORE y exclusion activa de Loteria/SAAOP.
- DOM test si se toca HTML.
- `node --check` en los JS tocados.
- `git diff --check`.
- Backend contract tests solo si aplican a datos ya existentes, sin crear backend.
- Pruebas de empty, degraded, deferred, blocked, forbidden y `ready-no-permission`.
- Prueba de evidencia snapshot y no log vivo.

Los static checks de no fetch/no endpoint deben ser scoped a la nueva superficie o a los cambios del futuro prompt. No deben declarar que la UI completa es fetch-free.

## Controlled implementation strategy

El prompt futuro debe implementar solamente Contract Overview Screen y seguir esta secuencia:

1. Confirmar preflight, HEAD esperado, rama, arbol limpio y aprobacion humana.
2. Identificar el contenedor existente del Panel Maestro y el punto de insercion local.
3. Implementar primero la estructura semantica y los estados documentales.
4. Conectar solo datos ya disponibles o fixture/documento estatico expresamente autorizado.
5. Renderizar `allowed_actions`, `forbidden_actions` y `blocked_capabilities` como lectura.
6. Añadir copy seguro, evidencia snapshot y empty/degraded/deferred states.
7. Aplicar estilos scoped sin alterar otros dominios ni pantallas.
8. Ejecutar pruebas estaticas, DOM, sintaxis y regresion contractual.
9. Hacer revision visual humana del Panel Maestro.
10. Commitear el resultado sin push por defecto.

No se debe tocar navegacion global salvo el contenedor documental existente si fuera estrictamente necesario. No se debe crear componente compartido amplio, ni modificar Blocked & Forbidden, Validation & Readiness o Request Contract Preview.

## Entry criteria

La implementacion futura solo puede comenzar si:

- El checkpoint 1.84 esta publicado.
- Este plan 1.85 esta cerrado y commiteado.
- El working tree esta limpio.
- El HEAD esperado y el remoto estan confirmados.
- Los tests 1.83, 1.84 y 1.85 estan verdes.
- Existe un prompt explicito de implementacion.
- El operador humano aprueba implementar.
- El alcance de archivos esta limitado a la tabla de candidatos.
- No hay P0/P1 abierto para Contract Overview.
- User Panel, runtime, endpoints, fetches y backend permanecen prohibidos.

## Exit criteria

La implementacion futura solo puede considerarse cerrada si:

- Contract Overview queda visible dentro del Panel Maestro y con identidad IA_CORE.
- No existe CTA operativo ni permiso implicito.
- `allowed_actions` son lectura y blockers/`forbidden_actions` permanecen visibles.
- `ready-no-permission` no se presenta como listo para ejecutar.
- No existe User Panel, runtime, endpoint, fetch, ruta o hash no autorizado.
- No hay datos inventados, mocks engañosos ni logs vivos.
- Pasan tests documentales, static, DOM, Node y contract tests aplicables.
- La revision visual humana aprueba jerarquia, estados, copy y limites.
- Se crea commit y el working tree queda limpio.
- El push se posterga para un checkpoint posterior.

## Rollback strategy

El rollback normal es por commit: identificar el commit de implementacion, registrar el hash y revertirlo con una operacion Git revisada si la implementacion viola el contrato. No se deben borrar archivos ni usar reset destructivo.

Se debe detener inmediatamente si aparece cualquiera de estas señales:

- fetch, endpoint, polling, runtime, execution, dispatch, worker, queue o scheduler.
- User Panel leakage o datos fuera del Panel Maestro.
- CTA fantasma, estado live/running/executing o success operativo.
- `allowed_actions` convertidas en botones.
- blockers o `forbidden_actions` ocultos.
- evidencia tratada como log vivo.
- necesidad de modificar backend, `api.py`, CI, dependencias o secretos.

Ante una necesidad de backend, el futuro prompt debe detenerse, conservar el arbol, documentar el bloqueo y abrir otro prompt con alcance contractual separado. Si un cambio parcial ya fue aplicado, se revierte por commit o se deja preparado para revision, sin push.

## Future prompt sequence

- 1.86: implementar Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution, solo con aprobacion humana explicita y sin push por defecto.
- 1.87: hardening visual y contractual de Contract Overview, si 1.86 se implementa y pasa revision.
- 1.88: checkpoint y push, solo despues de validacion completa y decision humana.

Blocked & Forbidden y Validation & Readiness permanecen fuera de esta secuencia hasta que Contract Overview quede revisado. Request Contract Preview sigue diferido.

## Risk register

| risk_id | Riesgo | Severidad | Mitigacion | Condicion de stop |
| --- | --- | --- | --- | --- |
| CO-PLAN-185-001 | Convertir Contract Overview en dashboard operativo | P0 | Header contractual y estados documentales | Cualquier estado operativo visible |
| CO-PLAN-185-002 | Convertir `allowed_actions` en botones | P0 | Bloque read-only y test estatico | Aparece CTA de ejecucion |
| CO-PLAN-185-003 | Interpretar readiness como permiso | P0 | Copy `ready-no-permission` explicito | Se promete ejecucion |
| CO-PLAN-185-004 | Agregar fetch o endpoint | P0 | Datos existentes/fixture autorizado | Aparece red nueva |
| CO-PLAN-185-005 | Fuga hacia User Panel | P0 | Panel Maestro unico y raw-safe | Payload sale de la superficie |
| CO-PLAN-185-006 | Exponer runtime o log vivo | P0 | Snapshot documental | Se muestran jobs, workers o logs live |
| CO-PLAN-185-007 | Ocultar blockers | P1 | Bloques visibles y prioridad critica | Blocker queda escondido |
| CO-PLAN-185-008 | Inventar datos en empty state | P1 | `no_payload` honesto | Se completa un dato ausente |
| CO-PLAN-185-009 | Reintroducir Loteria/SAAOP | P1 | Assert de identidad IA_CORE | Legacy aparece como identidad activa |
| CO-PLAN-185-010 | Crear ruta/hash prematura | P1 | Contenedor existente y sin navegacion nueva | Cambia URL o navegacion |
| CO-PLAN-185-011 | Tocar backend, CI o dependencias | P1 | Lista de archivos prohibidos | Se solicita cambio fuera de UI |
| CO-PLAN-185-012 | Scope creep a otros contratos | P2 | Unico foco Contract Overview | Se toca otra pantalla |

## Decision

`CONTRACT_OVERVIEW_CONTROLLED_IMPLEMENTATION_PLAN_READY`

El plan queda listo para que el proximo prompt implemente de forma controlada, pero solo con aprobacion humana explicita. Este documento no implementa pantalla, no modifica UI activa y no autoriza push.

## Proximo prompt exacto

`PROMPT UI/UX 1.86 - Implementar Contract Overview Screen IA_CORE contract-aware sin runtime/no-execution`

El prompt 1.86 debe implementar pantalla solo si el operador humano lo aprueba, no debe hacer push por defecto y debe dejar el checkpoint con push para despues del hardening y la validacion 1.88.

## Cierre de alcance

No se implemento pantalla. No se modifico UI activa. No se creo componente nuevo. No se creo User Panel. No se crearon rutas/hash. No se crearon endpoints ni fetches. No se activo runtime, execution ni dispatch. No se toco backend operativo, CI ni dependencias. No se limpio deuda residual. No se corrigieron pyflakes. No se hizo push.

Marcadores de limite verificables: no pantalla; no UI activa; no componente nuevo; no User Panel; no rutas/hash; no endpoints; no fetches; no runtime; no execution; no backend operativo; no CI; no dependencias; no deuda residual; no pyflakes. No se crearon fetches. No se activo runtime. No se activo execution. No se activo dispatch.
