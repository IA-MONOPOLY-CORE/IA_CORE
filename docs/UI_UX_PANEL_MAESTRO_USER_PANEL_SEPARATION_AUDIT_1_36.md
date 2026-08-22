# UI/UX Panel Maestro / User Panel Separation Audit 1.36

Veredicto: UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_COMPLETED

## Preflight

- Commit base esperado y confirmado: `ec39e9ac`.
- Rama esperada y confirmada: `main`.
- Remoto esperado y confirmado: `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- Working tree inicial: limpio antes de crear esta auditoria.
- Relacion con 1.35: `docs/UI_UX_NEXT_BLOCK_PLAN_1_35.md` selecciono `Panel Maestro vs User Panel Separation Planning` y propuso 1.36 auditoria, 1.37 documentacion/boundaries y 1.38 checkpoint.
- Relacion con 1.34: `docs/UI_UX_CONTRACT_STORYTELLING_OPERATOR_NARRATIVE_CHECKPOINT_1_34.md` cerro storytelling, confirmo narrativa documental/no-operativa, evidencia visual humana, no botones operativos, no runtime/execution y `UI_READY_FOR_NEXT_BLOCK_PLANNING`.

Esta auditoria no implementa separacion, no crea User Panel, no modifica UI activa, no cambia microcopy visible, no crea pantallas, no crea rutas, no crea endpoints, no instala dependencias, no activa runtime, no activa execution, no activa dispatch real y no implementa controlled execution.

## Objetivo Del Bloque

Auditar la separacion futura entre Panel Maestro y User Panel en IA_CORE, definiendo fronteras iniciales de exposicion, lenguaje, estados, permisos, evidencia, componentes y documentacion para que 1.37 pueda documentar boundaries sin construir una nueva superficie.

Veredicto: POST_STORYTELLING_SURFACE_SEPARATION_REVIEWED

## Definiciones

### Panel Maestro

Superficie interna actual para operador/constructor/admin del sistema. Puede mostrar contratos, payload, schema, validation, allowed_actions, forbidden_actions, blocked_capabilities, no-runtime/no-execution, request contract preview, evidence/logs como trazabilidad, raw-safe, glosario tecnico, lenguaje claro + termino tecnico entre parentesis, warnings/errors tecnicos, prompts/checkpoints y limites internos.

No puede activar runtime, ejecutar, despachar, invocar modelos/tools, parecer operativo ni esconder bloqueos.

### User Panel

Superficie futura para usuario final. Debe mostrar lenguaje simple, estados entendibles, resultados o informacion final cuando exista contrato real, acciones futuras solo si estan explicitamente permitidas por backend, limites explicados sin jerga y experiencia limpia.

No debe mostrar por defecto payload, schema, raw-safe, internal registry, adapter, dispatcher, validation traces internos, allowed_actions/forbidden_actions/blocked_capabilities como objetos tecnicos, logs internos, stack/debug, fixtures tecnicas, nombres de contratos internos sin traduccion, jerga innecesaria, capacidades no disponibles como botones ni prompts/checkpoints internos salvo modo educativo/documental futuro explicito.

### shared contract boundary

Ambos paneles deben respetar lo declarado por backend. Ninguno puede inventar permisos, ocultar bloqueos criticos, convertir planned/pending/no_payload en disponibilidad ni sugerir runtime/execution si no existe contrato operativo aprobado.

### translation layer

Mecanismo conceptual futuro para traducir datos tecnicos del Panel Maestro a lenguaje simple del User Panel. En 1.36 solo se audita y documenta; no se implementa.

## Estado Post Storytelling

La UI actual corresponde a Panel Maestro. El header dice `Panel Maestro / operador interno`; guidance dice `Panel Maestro read-only: historia contractual, no Panel Usuario final`; la shell mantiene `data-contract-storytelling="contract-aware-1.33"`; request draft queda como REQUEST CONTRACT PREVIEW read-only; evidence/logs-sanitized quedan como trazabilidad; Next Step queda documental.

Evidencia humana considerada: "Lo veo muy bien", "Veo graficamente los prompts que mandamos", "ES TODO VISUAL", "NO HAY NINGUN BOTON", "TODO BIEN ORDENADO PROLIJO". Esta evidencia confirma experiencia visual/no-operativa; no reemplaza guardrails contract-aware.

## Areas Auditadas

1. Superficie actual.
2. Exposicion de datos.
3. Lenguaje.
4. Acciones/permisos.
5. Estados.
6. Evidence/logs/bitacora visual.
7. Request Contract Preview.
8. Raw-safe/detail.
9. Navigation/components.
10. Mobile/responsive.
11. Documentacion/README.

## Auditoria Por Zonas

### Superficie actual

La UI activa se presenta como Panel Maestro: orienta al operador interno, expone contratos, estados, limites, evidence y request preview. No existe User Panel implementado. No hay P0: la UI no declara una experiencia de usuario final ni oculta que es interna/read-only.

Riesgo vivo: algunos controles administrativos preexistentes (`CFG`, `+`, `DOMAIN`, paneles admin, crear agente/dominio) conviven en la misma app y podrian confundirse con producto final si en el futuro se extraen sin boundary. Recomendacion 1.37: documentar estos controles como Panel Maestro/admin-only o fuera del futuro User Panel por defecto.

### Exposicion de datos

Panel Maestro puede ver payload, schema, validation, registry, dispatcher no-runtime, adapter, confirmation gate, allowed_actions, forbidden_actions, blocked_capabilities, warnings/errors, raw-safe, logs-sanitized y prompts/checkpoints.

User Panel podria recibir traducciones de estado, limite, falta de informacion, no disponibilidad, resultado final y warnings importantes. User Panel no debe recibir objetos contractuales crudos, raw-safe, registros internos, trazas de validacion, fixtures tecnicas ni logs internos.

### Lenguaje

Terminos tecnicos visibles actuales son correctos para Panel Maestro: payload, schema, raw-safe, registry, adapter, dispatcher, validation, allowed_actions, forbidden_actions, blocked_capabilities, no_payload, planned, pending, not_available, read-only, backend-only, contract_fixture, request contract preview y evidence/logs.

Para User Panel deben traducirse o bloquearse:

| Termino actual | Panel Maestro | User Panel | Equivalente simple | Riesgo |
| --- | --- | --- | --- | --- |
| payload | Permitido | Traducir | informacion recibida | jerga tecnica |
| schema | Permitido | Ocultar/traducir | formato interno esperado | exposicion tecnica |
| raw-safe | Permitido | Prohibido por defecto | no aplica / detalle interno | parecer consola tecnica |
| registry | Permitido | Prohibido | registro interno | exposicion interna |
| adapter | Permitido | Prohibido | preparacion interna de respuesta | exposicion interna |
| dispatcher | Permitido solo negado no-runtime | Prohibido | no disponible | falsa operacion |
| validation | Permitido | Traducir | revision del sistema | jerga tecnica |
| allowed_actions | Permitido | Traducir bajo contrato | acciones disponibles | permiso inferido |
| forbidden_actions | Permitido | Traducir | acciones no permitidas | ocultar limite |
| blocked_capabilities | Permitido | Traducir | funciones no disponibles | disabled CTA ambiguo |
| no_payload | Permitido | Traducir | todavia no hay informacion disponible | parecer error |
| planned | Permitido | Traducir | todavia no disponible | parecer disponible |
| pending | Permitido | Traducir | pendiente, no en ejecucion | parecer proceso vivo |
| not_available | Permitido | Traducir | no disponible en este estado | hueco mudo |
| read-only | Permitido | Traducir | solo lectura | confundir formulario |
| backend-only | Permitido | Traducir | definido por el sistema interno | autoridad mal entendida |
| contract_fixture | Permitido | Prohibido | dato de prueba interno | dato falso como real |
| request contract preview | Permitido | Traducir parcialmente | vista previa interna, no formulario | submit falso |
| evidence/logs | Permitido | Traducir resumen, no logs | trazabilidad interna / estado explicado | live log falso |

### Acciones y permisos

`allowed_actions` se entiende como backend-declared y no concede permiso UI. `forbidden_actions` y `blocked_capabilities` siguen visibles. Los botones de foco/releer son inspeccion local/read-only; request contract control esta disabled. Los controles admin preexistentes no pertenecen al modelo User Panel por defecto.

Regla: acciones futuras solo pueden aparecer en User Panel si backend las declara para esa superficie, la capability no esta bloqueada, existe contrato de request aceptado y el copy no convierte forbidden/blocked en CTA.

### Estados

| Estado | Lectura Panel Maestro | Lectura User Panel | Traduccion simple | Riesgo | Regla de exposicion |
| --- | --- | --- | --- | --- | --- |
| ready | lectura disponible | listo si aplica a dato final | disponible para leer | parecer operativo | no usar como capacidad ejecutable |
| passed | validacion/documento confirmado | completado/validado si corresponde | confirmado | parecer ejecucion final | usar solo para evidencia/validacion |
| blocked | frontera contractual | no disponible por seguridad/contrato | bloqueado / no disponible | disabled CTA ambiguo | mantener limite visible |
| planned | continuidad documental | todavia no disponible | todavia no disponible | parecer roadmap usable | no CTA, no cola |
| pending | espera de dato/validacion | pendiente, no en ejecucion | pendiente | parecer proceso corriendo | negar ejecucion |
| invalid | contrato invalido | no se puede mostrar | informacion no valida | parecer error tecnico | traducir causa segura |
| failed | fallo/errores declarados | no se pudo completar/mostrar | fallo seguro | exponer stack | sanitizar |
| not_available | dato no disponible | no disponible en este estado | no disponible | hueco mudo | explicar causa si se puede |
| no_payload | sin envelope estable | todavia no hay informacion disponible | sin informacion cargada | falla general | deny-by-default |
| contract_fixture | fixture tecnica | no mostrar por defecto | dato de prueba interno | dato falso como real | Panel Maestro only |
| read-only/backend-only | lectura/autoridad backend | solo lectura / definido por el sistema | solo lectura | parecer formulario | sin submit ni permiso local |

### Evidence / logs / bitacora visual

Panel Maestro puede ver evidencia tecnica, commits, prompts/checkpoints, logs-sanitized y trazabilidad documental. User Panel no debe ver logs internos ni timeline de prompts por defecto. Puede ver una explicacion simple del estado o resultado si existe contrato futuro. Prompts/checkpoints quedan internos salvo modo educativo/documental futuro explicito. Evidence no debe parecer live log.

### Request Contract Preview

Pertenece al Panel Maestro. User Panel no debe heredar el textarea tecnico, `backend_internal_ui_request.v1`, `allowed_actions`, `blocked_capabilities` ni control disabled como formulario. Si en el futuro existe una accion de usuario, debe nacer desde contrato especifico para User Panel, con copy simple, permiso declarado y bloqueo visible sin jerga. Mantener read-only/no-submit/no-dispatch/no-execution.

### Raw-safe / detail

Raw-safe es Panel Maestro only. Detail tecnico es Panel Maestro by default. Summary puede traducirse parcialmente a User Panel si se extrae como resultado/estado simple. Nunca deben cruzar secretos, env, payload externo crudo, tracebacks, internal registry, adapter, dispatcher, validation traces ni fixtures tecnicas.

### Navigation / components

Componentes internos actuales: `ia-detail-panel`, `ia-readonly-control`, `ia-evidence`, contract inspector, internal nav, raw-safe disclosure, request draft panel, admin panels y data widgets contract-aware. Reutilizables con variante user-safe: `ia-panel`, `ia-status-badge`, `ia-chip`, `ia-empty-state`, `ia-warning`, `ia-error`, `ia-blocker`, siempre con copy simple y sin objetos crudos.

Nombres/clases como `internal-nav`, `contract-inspector`, `raw-safe`, `request-contract`, `admin-*` no deben trasladarse al User Panel sin renombrado conceptual o wrapper user-safe.

### Mobile / responsive

Panel Maestro puede sostener mayor densidad tecnica con disclosure seguro. User Panel futuro deberia ser mas simple, menos denso y con menos capas. Riesgo mobile: el request draft lateral y admin panels pueden ocupar mucho espacio; si se compartiera estructura con User Panel podria exponer dato interno o parecer formulario. 1.37 debe documentar responsive distinto por superficie.

### Documentacion / README

README y `ui/web/README.md` ya registran que la consola activa es Panel Maestro y que User Panel es futuro. Falta registrar la auditoria 1.36, el proximo prompt 1.37 y que no se implemento User Panel. No hay P0 documental.

## Hallazgos Clasificados

Veredicto: PANEL_MAESTRO_USER_PANEL_BOUNDARY_GAPS_IDENTIFIED

| ID | Zona | Severidad | Descripcion | Riesgo | Recomendacion 1.37 | Clasificacion | Equivalente simple | Archivos probables 1.37 | Tests sugeridos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PMUP-P0-001 | Global | P0 | No se detecta User Panel activo ni exposicion final directa. | Ninguno directo hoy. | Mantener no implementacion. | shared contract boundary | no aplica | docs/tests | test no User Panel implementado |
| PMUP-P1-001 | Superficie | P1 | Controles admin y consola interna conviven; futuro User Panel podria heredar superficie si no se documenta. | Mezcla operador/usuario. | Matriz de ownership por zona. | Panel Maestro only | panel interno | docs 1.37, README | test matriz contiene admin-only |
| PMUP-P1-002 | Lenguaje | P1 | Terminos contractuales son correctos para operador pero no user-safe. | Jerga tecnica al usuario final. | Tabla de traducciones obligatoria. | User Panel translated / prohibited | lenguaje simple | docs 1.37 | test traducciones por termino |
| PMUP-P1-003 | Acciones | P1 | `allowed_actions` puede malinterpretarse como permiso si se traslada al User Panel. | Permiso inferido. | Regla: acciones user solo con contrato especifico por superficie. | Future contract required | accion disponible | docs/tests | test no heredar allowed_actions |
| PMUP-P1-004 | Request preview | P1 | REQUEST CONTRACT PREVIEW parece formulario tecnico si se reutiliza. | Submit falso o expectativa operativa. | Marcar Panel Maestro only; User Panel requiere patron nuevo. | Panel Maestro only | no formulario tecnico | docs 1.37 | test request preview internal only |
| PMUP-P1-005 | Evidence/logs | P1 | Prompts/checkpoints/logs son valiosos pero no user-safe por defecto. | Live log falso o exposicion interna. | Regla: logs internos no cruzan; solo resumen traducido. | Panel Maestro only / User Panel translated | estado explicado | docs/tests | test logs internos prohibidos |
| PMUP-P2-001 | Estados | P2 | Estados permitidos necesitan traduccion por superficie. | Confusion de disponibilidad. | Tabla ready/passed/blocked/planned/pending/etc. | User Panel translated | ver tabla estados | docs 1.37 | test reglas de estados |
| PMUP-P2-002 | Raw-safe/detail | P2 | Summary puede traducirse, detail/raw-safe no. | Exposicion tecnica. | Matriz summary/detail/raw-safe por superficie. | Panel Maestro only / translated summary | resumen simple | docs 1.37 | test raw-safe prohibited |
| PMUP-P2-003 | Componentes | P2 | Componentes internos requieren variantes user-safe antes de reuso. | Reuso con jerga/admin. | Mapa componentes internos/reutilizables/prohibidos. | shared safe / Panel Maestro only | componente seguro | docs/tests | test component map |
| PMUP-P2-004 | Mobile | P2 | Futuro User Panel deberia tener densidad y disclosure distintos. | Saturacion y exposicion accidental. | Criterios responsive separados. | User Panel translated | vista simple | docs 1.37 | test responsive criteria |
| PMUP-P2-005 | README | P2 | Falta registrar auditoria 1.36 y continuidad 1.37. | Continuidad incompleta. | Actualizar README raiz y UI. | shared contract boundary | no aplica | README, ui/web/README.md | test README 1.36 |
| PMUP-P3-001 | Polish | P3 | Polish premium y benchmarks siguen pospuestos. | Estetica antes de boundary. | Mantener pospuesto hasta checkpoint. | Future contract required | no aplica | docs | test benchmarks not operative |

## Matriz Inicial De Exposicion

Veredicto: PANEL_EXPOSURE_MATRIX_INITIALIZED

| Categoria | Contenido | Regla |
| --- | --- | --- |
| Panel Maestro only | payload, schema, raw-safe, detail tecnico, internal registry, adapter, dispatcher no-runtime, confirmation gate, response adapter, validation traces, logs internos, prompts/checkpoints, request contract preview, admin panels, contract inspector | Permitido solo en superficie interna. |
| User Panel translated | estado, ausencia de informacion, bloqueo, no disponibilidad, resultado/resumen, warnings importantes, limites, acciones futuras declaradas | Traducir a lenguaje simple sin ocultar blockers. |
| Shared safe | IA_CORE identidad, limites contractuales en lenguaje simple, solo lectura cuando aplique, estado no-operativo, mensajes de seguridad, errores sanitizados de alto nivel | Puede compartirse si no expone objeto tecnico. |
| Prohibited for User Panel | raw-safe crudo, payload/schema crudos, registry/adapter/dispatcher, stack/debug, env/secrets, logs internos, fixtures tecnicas, allowed/forbidden/blocked como objetos, endpoints internos, prompts/checkpoints internos por defecto | No cruzar sin modo futuro explicito y contrato. |
| Future contract required | acciones de usuario, resultados finales, formularios reales, submit, workflows, permisos, integraciones, modelo/tool invocation, pantalla user-safe | Requiere contrato backend especifico y no blocked. |
| Fixture/test only | contract_fixture, payload de prueba, snapshots de auditoria, datos de test, prompts/checkpoints como evidencia de desarrollo | Solo documentacion/test o Panel Maestro educativo interno. |

## Reglas De Lenguaje Por Superficie

Veredicto: SURFACE_LANGUAGE_RULES_DEFINED

- Panel Maestro: lenguaje claro + termino tecnico cuando aporte trazabilidad.
- Panel Maestro puede enseñar terminos tecnicos.
- User Panel: lenguaje simple, humano y directo.
- User Panel no debe mostrar objetos contractuales crudos.
- User Panel no debe mostrar logs internos.
- User Panel no debe mostrar `allowed_actions`, `forbidden_actions` ni `blocked_capabilities` como nombres tecnicos.
- User Panel debe traducir limites sin ocultarlos.
- User Panel debe ocultar complejidad tecnica innecesaria.
- Ambos paneles deben preservar exactitud contract-aware.

## Reglas De Estados Por Superficie

Veredicto: SURFACE_STATE_RULES_DEFINED

- `no_payload` -> todavia no hay informacion disponible.
- `planned` -> todavia no disponible.
- `pending` -> pendiente, no en ejecucion.
- `not_available` -> no disponible en este estado.
- `blocked` -> bloqueado/no disponible por seguridad o contrato.
- `forbidden_actions` -> acciones no permitidas.
- `blocked_capabilities` -> funciones no disponibles.
- `read-only` -> solo lectura.
- `backend-only` -> definido por el sistema interno.
- `contract_fixture` -> dato de prueba / ejemplo tecnico solo interno.

Ningun estado puede convertirse en `active`, `running`, `live`, `operational`, `executing`, `dispatching`, `submitted`, `processing` ni equivalente como estado valido de UI.

## Reglas De Acciones Y Permisos

Veredicto: SURFACE_ACTION_PERMISSION_RULES_DEFINED

- Acciones futuras solo si backend las declara para la superficie correspondiente.
- User Panel no hereda `allowed_actions` internos por defecto.
- No mostrar forbidden como botones.
- No mostrar blocked como disabled CTA ambiguo.
- Ausencia de lista no concede permiso.
- Request preview no se convierte en formulario.
- Ningun panel activa runtime, execution, dispatch, controlled execution, modelos, tools ni integraciones.
- `allowed_actions` backend-declared no es CTA UI.
- `forbidden_actions` y `blocked_capabilities` no se ocultan.

## Reglas De Evidence / Logs

- Panel Maestro puede ver trazabilidad tecnica y documental.
- User Panel no ve logs internos.
- User Panel puede ver explicacion simple de estado si corresponde.
- Prompts/checkpoints quedan internos salvo futuro modo educativo/documental explicito.
- Evidence no debe parecer live log, timeline activo, proceso vivo, workflow, pipeline ni tarea en cola.

## Recomendacion Concreta Para 1.37

1.37 deberia crear `docs/UI_UX_PANEL_MAESTRO_USER_PANEL_BOUNDARIES_1_37.md` o equivalente documental con:

- matriz Panel Maestro/User Panel por zona;
- reglas de exposicion;
- tabla de traducciones;
- datos prohibidos para User Panel;
- estados traducidos;
- reglas de acciones/permisos;
- reglas de evidence/logs;
- componentes internos vs reutilizables vs user-safe;
- criterios mobile/responsive por superficie;
- README updates;
- tests documentales.

## Limites Para 1.37

1.37 no debe implementar User Panel, crear pantallas nuevas, crear rutas, crear endpoints, crear fetches, instalar dependencias, activar runtime, activar execution, activar dispatch, activar controlled execution, tocar backend operativo, cambiar contratos backend ni modificar UI activa salvo documentacion/README/tests estrictamente necesarios.

## Riesgos Residuales

- Separacion aun no documentada como boundary formal hasta 1.37.
- User Panel sigue futuro y sin contrato de datos especifico.
- Componentes user-safe aun no existen.
- Admin controls preexistentes deben quedar claramente fuera del futuro User Panel.
- Visual polish, secondary views y benchmarks externos siguen pospuestos.

## Confirmaciones De Alcance

- IA_CORE sigue como identidad activa.
- No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa.
- User Panel no implementado.
- No se modifico UI activa.
- No se recomienda activar blocked_capabilities.
- No se recomienda ocultar forbidden_actions ni blocked_capabilities.
- Sin endpoints, sin API/router, sin fetch nuevo y sin dependencias nuevas.
- Sin runtime, sin execution, sin dispatch y sin controlled execution.
- Backend operativo untouched: no `core/`, no `api.py`, no `domains/`, no `tools/`, no modelos, no integraciones.

Veredicto: USER_PANEL_NOT_IMPLEMENTED_CONFIRMED
Veredicto: PANEL_SEPARATION_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED
Veredicto: UI_READY_FOR_PANEL_BOUNDARIES_DOCUMENTATION

## Proximo Prompt Exacto

PROMPT UI/UX 1.37 - Documentar boundaries Panel Maestro / User Panel IA_CORE contract-aware sin runtime/no-execution

## Veredictos

- UI_UX_PANEL_MAESTRO_USER_PANEL_SEPARATION_AUDIT_COMPLETED
- POST_STORYTELLING_SURFACE_SEPARATION_REVIEWED
- PANEL_MAESTRO_USER_PANEL_BOUNDARY_GAPS_IDENTIFIED
- PANEL_EXPOSURE_MATRIX_INITIALIZED
- SURFACE_LANGUAGE_RULES_DEFINED
- SURFACE_STATE_RULES_DEFINED
- SURFACE_ACTION_PERMISSION_RULES_DEFINED
- USER_PANEL_NOT_IMPLEMENTED_CONFIRMED
- PANEL_SEPARATION_AUDIT_NO_RUNTIME_NO_EXECUTION_CONFIRMED
- UI_READY_FOR_PANEL_BOUNDARIES_DOCUMENTATION
