# UI/UX Next Console Block Plan 1.5

Veredicto: `UI_UX_NEXT_CONSOLE_BLOCK_PLAN_DEFINED`

## Alcance

Este documento consolida el siguiente bloque de consola IA_CORE despues del
checkpoint `1.4`. No construye el bloque elegido, no crea pantallas nuevas, no
redisenia la UI activa, no agrega interacciones, no crea endpoints, no activa
runtime, no habilita execution, no activa dispatch real y no implementa
controlled execution.

Commit base: `ee7323d5`.

## Resumen 1.0 -> 1.4

Veredicto: `IA_CORE_CONSOLE_BLOCK_CONTINUITY_CONFIRMED`

1.0 estructuro la consola principal con
`data-main-console="contract-aware-1.0"`, identidad IA_CORE, readiness,
Contract Core / Payload, Internal Services / Signals, Actions & Boundaries y
Evidence / Checkpoint.

1.1 refino la consola con `data-console-refinement="1.1"`, redujo lectura
legacy/HUD, reforzo `PRE-RUNTIME / NO-EXECUTION`, mantuvo los bloqueos visibles
y separo seniales internas de operacion.

1.2 definio el flujo con `data-console-flow="contract-aware-1.2"` y siete
`data-flow-step`: orientation, readiness, contract-core, service-signals,
actions-boundaries, evidence-checkpoint y next-step.

1.3 definio el modelo de interaccion con
`data-console-interaction="contract-aware-1.3"` y
`data-interaction-mode="read-only"`: foco local, relectura local, disclosure
accesible e inspector read-only.

1.4 cerro el checkpoint de interaccion y confirmo que el bloque 1.0 -> 1.3
quedo contract-aware, local, read-only, no operativo, sin permisos inferidos,
sin endpoints nuevos y sin runtime/execution/dispatch/controlled execution.

Base contractual que el siguiente bloque debe respetar:

- `backend_internal_ui_payload.v1`;
- `backend_internal_ui_request.v1`;
- `internal_exposure_registry`;
- `internal_request_validation`;
- `internal_dispatcher_no_runtime`;
- `internal_confirmation_gate`;
- `internal_response_adapter`;
- `allowed_actions`;
- `forbidden_actions`;
- `blocked_capabilities`;
- `warnings`;
- `errors`;
- `validation`;
- `flags`;
- `readiness`;
- `status`;
- `service_kind`;
- `schema_version`.

## Estado Actual De Consola

Solido:

- IA_CORE es la identidad visual activa.
- La consola conserva marcas 1.0, 1.1, 1.2 y 1.3.
- El flujo principal esta definido y testeado.
- El inspector read-only existe y sincroniza desde DOM local.
- Los widgets siguen consumiendo `backend_internal_ui_payload.v1` inyectado o
  fixture contractual explicito.
- `allowed_actions`, `forbidden_actions` y `blocked_capabilities` mantienen
  autoridad de backend y visibilidad.
- Los controles de request/dispatch siguen bloqueados por contrato.

Debil:

- Contract Core / Payload sigue siendo la zona con mayor densidad tecnica.
- La relacion entre summary, detalle y raw-safe todavia no esta normalizada.
- Warnings, errors, validation, flags y source necesitan una lectura mas
  guiada para operadores.
- Los paneles de detalle futuros podrian duplicar informacion si no existe
  antes un modelo de lectura.
- La navegacion interna puede parecer multi-pantalla si se agrega antes de
  fijar que significa leer cada capa.

Falta para mayor usabilidad:

- Un modelo de lectura que explique que se ve primero, que se puede desplegar
  como detalle y que queda como raw-safe de solo lectura.
- Reglas para no convertir contract/payload en permisos UI.
- Criterios para distinguir datos declarados, diagnostico, ausencia honesta de
  payload y bloqueo.
- Preparacion para paneles de detalle sin duplicar autoridades.

Partes densas: Contract Core / Payload, flags, validation, warnings/errors y
acciones/bloqueos. Partes que requieren detalle: payload, services, blockers y
evidence. Partes que requieren navegacion: las zonas del flujo una vez que el
modelo de lectura este fijado. Partes que requieren componentes reutilizables:
status, chips, empty states, panels y detalles, pero despues de estabilizar el
modelo de lectura.

No deben tocarse todavia: endpoints, runtime, execution, dispatch, controlled
execution, contratos backend, `core/`, `api.py`, `domains/`, `tools/`, modelos
e integraciones.

## Opciones Evaluadas

### Opcion A - Navegacion interna de consola

Objetivo: definir navegacion lateral/superior o indice interno para moverse
entre zonas sin crear pantallas nuevas.

Valor: mejora orientacion y reduce desplazamiento manual.

Riesgo: puede parecer app multi-pantalla o accion operativa si se exagera.

Lectura: conviene despues de fijar como se lee contract/payload, porque la ruta
1.2 y el foco 1.3 ya cubren el minimo actual.

### Opcion B - Paneles de detalle contract-aware

Objetivo: crear detalle read-only para readiness, payload, services, actions,
blockers y evidence.

Valor: mejora profundidad y lectura.

Riesgo: puede duplicar informacion y crear una segunda autoridad si no hay un
modelo de lectura previo.

Lectura: buen segundo paso despues de normalizar summary/detail/raw-safe.

### Opcion C - Modelo de lectura de payload/contract

Objetivo: hacer que contract/payload sea mas entendible con capas
summary/detail/raw-safe, sin mutar datos ni activar operacion.

Valor: fortalece la verdad del sistema, reduce permisos inferidos, prepara
detalle y componentes, y mejora claridad para el operador.

Riesgo: puede volverse demasiado tecnico si no se acota a lectura UI y a
criterios de presentacion.

Lectura: es la opcion que mas reduce riesgo antes de construir mas UI.

### Opcion D - Sistema de componentes IA_CORE

Objetivo: normalizar cards, badges, status, chips, panels y empty states.

Valor: evita inconsistencia visual futura.

Riesgo: prematuro si todavia falta fijar el modelo de lectura y detalle.

Lectura: debe venir despues de saber que patrones necesita la consola real.

### Opcion E - Primera pantalla secundaria

Objetivo: separar una vista especifica, como Contract Detail o Evidence.

Valor: inicia arquitectura multi-vista.

Riesgo: temprano para el estado actual; puede crear navegacion y permisos
aparentes antes de cerrar lectura y detalle.

Lectura: no recomendada todavia.

### Opcion F - Benchmark visual externo futuro

Objetivo: comparar IA_CORE contra referencias visuales externas sin copiar ni
instalar.

Valor: eleva criterio visual mas adelante.

Riesgo: distrae si se hace antes de cerrar lectura, detalle y accesibilidad
base.

Lectura: registrado como benchmark futuro, no como dependencia actual.

## Opcion Recomendada

Veredicto: `NEXT_CONSOLE_BLOCK_SELECTED_WITH_EVIDENCE`

La opcion recomendada es:

`Opcion C - Modelo de lectura de payload/contract`

Va primero porque contract/payload es la fuente de verdad de la consola. Antes
de crear mas navegacion, paneles o componentes, IA_CORE necesita definir como
presenta summary, detail y raw-safe sin inferir permisos, sin ocultar bloqueos
criticos y sin crear una segunda autoridad visual.

## Alcance Del Proximo Bloque

Objetivo: definir el modelo de lectura de `backend_internal_ui_payload.v1` y
`backend_internal_ui_request.v1` en la consola activa, con capas
summary/detail/raw-safe de solo lectura.

Puede tocar:

- documentacion del modelo de lectura;
- tests UI del modelo de lectura;
- microcopy minimo en README si queda desactualizado;
- revision de `ui/web/index.html`, `backend-contract-widgets.js`,
  `console-interactions.js`, `admin-panels.js`, `i18n_es.json` y `styles.css`;
- correcciones minimas solo si una prueba demuestra inconsistencia.

No puede tocar:

- endpoints, API o router HTTP;
- runtime, execution, dispatch real o controlled execution;
- contratos backend;
- `core/`, `api.py`, `domains/`, `tools/`, modelos o integraciones;
- pantallas nuevas, app nueva, dependencias, templates externos o assets
  externos;
- acciones fuera de `allowed_actions`;
- visibilidad de `forbidden_actions` o `blocked_capabilities`.

Archivos probables:

- `docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md`;
- `tests/test_ui_ux_payload_contract_reading_model_1_6.py`;
- `ui/web/README.md` si requiere una nota minima.

Tests esperados:

- `node --check ui/web/backend-contract-widgets.js`;
- `node --check ui/web/admin-panels.js`;
- `node --check ui/web/console-interactions.js`;
- pruebas UI 1.4;
- prueba nueva 1.6;
- pruebas backend contractuales 8.7/7.6;
- `git diff --check`.

Criterio de cierre:

- modelo summary/detail/raw-safe documentado;
- no se construyen paneles nuevos;
- `allowed_actions` sigue backend only;
- `forbidden_actions` y `blocked_capabilities` permanecen visibles;
- no endpoints/API/router;
- no runtime/execution/dispatch/controlled execution;
- tests pasan;
- commit y working tree limpio.

## Riesgos Y Mitigacion

Riesgo: volver la consola demasiado tecnica.

Mitigacion: limitar el bloque a reglas de lectura, labels y pruebas, sin
expandir UI funcional.

Riesgo: duplicar informacion entre widgets, inspector y futuros detalles.

Mitigacion: fijar una sola jerarquia: summary para orientacion, detail para
diagnostico y raw-safe para evidencia de solo lectura.

Riesgo: sugerir permisos por posicion visual.

Mitigacion: repetir que solo `allowed_actions` declara acciones y que focus,
detalle, raw-safe, warnings, source o service_kind no autorizan nada.

## Secuencia Sugerida

1.6 - Modelo de lectura de payload/contract.

1.7 - Paneles de detalle contract-aware basados en ese modelo.

1.8 - Navegacion interna de consola si los detalles ya requieren mejor
recorrido.

1.9 - Sistema de componentes IA_CORE para normalizar estados, chips, cards y
empty states.

1.10 - Checkpoint del segundo bloque de consola.

## Referencias Externas Futuras

Veredicto: `EXTERNAL_REFERENCES_REGISTERED_AS_BENCHMARKS_ONLY`

Referencias registradas para benchmark futuro:

- 21st.dev;
- UI UX Pro Max Skill;
- Framer Motion / Motion.

Estas referencias son benchmarks futuros de calidad visual, componentes, UX,
accesibilidad y microinteracciones. No se instalan ahora, no se copian, no
definen identidad, no reemplazan IA_CORE, no agregan dependencias y no
habilitan templates externos. Se revisaran cuando consola, flujo, interaccion,
responsive y accesibilidad base esten cerrados.

Registro explicito:

- no se copian;
- no definen identidad;
- no reemplazan IA_CORE;
- no agregan dependencias;
- no habilitan templates externos.

## Limites Confirmados

Veredicto: `NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este plan confirma:

- IA_CORE como identidad visual activa;
- ausencia de legacy visual activo;
- no endpoint publico, API ni router HTTP;
- no runtime ni execution;
- no dispatch real;
- no controlled execution;
- no agentes ejecutados;
- no invocacion de models, tools o integrations;
- no cambio de contrato backend;
- no instalacion de librerias, templates ni dependencias externas;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni
  integraciones.

## Continuidad

Veredicto: `UI_READY_FOR_SELECTED_NEXT_CONSOLE_BLOCK`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.6 - Definir modelo de lectura de payload/contract IA_CORE contract-aware sin runtime/no-execution`
