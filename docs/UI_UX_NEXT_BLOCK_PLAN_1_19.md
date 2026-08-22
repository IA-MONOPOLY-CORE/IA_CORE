# UI/UX Next Block Plan 1.19

Veredicto: `UI_UX_NEXT_BLOCK_PLAN_1_19_DEFINED`

## Alcance

Este documento consolida el siguiente bloque UI/UX de IA_CORE despues del checkpoint Admin Boundary / Exposure Review `1.18`. Es una planificacion con evidencia: no implementa el bloque elegido, no crea pantallas nuevas, no redisenia la consola, no crea rutas, no agrega componentes, no instala dependencias, no crea endpoints, no activa runtime, no habilita execution, no activa dispatch real y no implementa controlled execution.

Commit base: `bd4e370e`.

## Relacion Con 1.18

`docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md` cerro el bloque `1.15 -> 1.17` y confirmo:

- request draft read-only, no-submit, no-dispatch, no-execution;
- `allowed_actions` como backend-declared, no permiso UI;
- `forbidden_actions` visible y no ejecutable;
- `blocked_capabilities` visible con `true = blocked`;
- internal exposure como lectura interna, no endpoint publico;
- evidence y next step como trazabilidad/planned, no operacion;
- navegacion, foco y componentes sin permisos inferidos;
- naming heredado `start-btn` / `runOrchestration` neutralizado en UI activa;
- no endpoints, dependencias, runtime, execution, dispatch ni controlled execution;
- IA_CORE como identidad visual activa sin legacy visual activo.

Veredicto: `POST_1_18_STATE_REVIEWED`

## Estado Post-Checkpoint

### Fortalezas

- IA_CORE permanece como identidad activa.
- La consola conserva `data-payload-reading-model="contract-aware-1.6"`, `data-contract-detail-panels="contract-aware-1.7"`, `data-internal-navigation="contract-aware-1.8"`, `data-component-system="ia-core-contract-aware-1.9"` y `data-responsive-hardening="contract-aware-1.13"`.
- La frontera administrativa ya no es el mayor riesgo inmediato: request draft, actions/boundaries, internal exposure, evidence y next step quedaron explicitamente read-only.
- `forbidden_actions`, `blocked_capabilities`, warnings, errors, validation, flags, readiness, status, service_kind, schema_version y `summary/detail/raw-safe` siguen visibles o preservados.
- `backend-contract-widgets.js` y `console-interactions.js` siguen sin fetch propio.

### Deudas Visibles

- La consola sigue siendo densa y mezcla shell, widgets contract-aware, paneles 1.7, inspector, request draft, modal administrativo y configuracion legacy.
- Quedan nombres historicos no operativos como `debate-panel`, `btn-debate`, `orchestration-task`, `orchestration-status`, `logs-runtime` y `activeAgentProfileCatalog`.
- `.active` sigue presente en skins/sidebar/tabs como estado visual legacy aislado.
- Conviven estilos inline, clases historicas, marcas `ia-*` y estilos duplicados en `index.html`/`styles.css`.

### Deudas UX

- El operador ya tiene boundaries seguros, pero aun puede percibir ruido por etiquetas heredadas y patrones duplicados.
- La guia/empty-state seria valiosa, pero si se construye antes de auditar incongruencias puede pegar copy nuevo sobre estructura vieja.
- La densidad necesita trabajo, pero reducir informacion antes de mapear duplicados puede ocultar datos contractuales criticos.

### Deudas De Orientacion

- El recorrido estado -> contrato -> lectura -> detalle -> limites -> evidencia -> siguiente paso existe y es seguro, pero todavia hay vocabulario viejo alrededor de ese recorrido.
- Request/admin ya estan bloqueados; ahora el riesgo esta en mantenimiento futuro y lectura de codigo/DOM, no en CTAs visibles.

### Deudas De Densidad

- Contract Core / Payload concentra summary, detail, raw-safe, widgets, inspector, actions, forbidden, blocked y diagnostics.
- Los paneles administrativos preexistentes aumentan carga cognitiva aunque no abren permiso.
- La reduccion de densidad conviene despues de saber que nombres, clases y patrones estan vivos, muertos o solo historicos.

### Deudas De Documentacion

- El sistema 1.9 define vocabulario minimo, pero no hay todavia un inventario extendido de patrones heredados vs canonicos.
- README registra la secuencia, pero no clasifica incongruencias del frontend hecho a mano.

### Deudas De Frontend Hecho A Mano

Veredicto: `FRONTEND_RESIDUAL_RISKS_RECORDED`

Riesgos observados y no bloqueantes:

- clases `.active` usadas fuera del contrato;
- nombres legacy no operativos (`debate`, `orchestration`, `logs-runtime`, `activeAgentProfileCatalog`);
- estilos duplicados o historicos entre `index.html` y `styles.css`;
- patrones de botones/read-only con clases historicas y marcas `ia-*` simultaneas;
- fetches administrativos preexistentes separados del modelo contract-aware;
- i18n y microcopy historica que podria necesitar inventario antes de guidance;
- posible CSS muerto o fragmentos JS legacy no-operativos.

Estos riesgos no abren runtime ni endpoints, pero pueden hacer mas fragil cualquier bloque futuro.

## Riesgos De Crecimiento

- UI Frankenstein por sumar guidance, polish o pantallas sobre patrones no inventariados.
- Permisos inferidos por incongruencias de nombres, clases o copy que vuelvan a parecer operativos.
- Saturacion visual si se agrega narrativa sin limpiar duplicaciones.
- Pantallas demasiado pronto: una vista secundaria podria cristalizar deuda legacy como API visual nueva.
- Polish prematuro: puede hacer mas elegante una estructura todavia incongruente.
- Panel Maestro vs User Panel prematuro: puede introducir jerarquia aparente de permisos.
- Benchmarks externos prematuros: pueden distraer de criterios IA_CORE propios.

## Criterios De Decision

La decision pondera:

- continuidad con 1.18;
- reduccion de riesgo inmediato;
- claridad para operador y mantenedor;
- riesgo de permisos inferidos;
- riesgo de UI Frankenstein;
- riesgo de saturacion visual;
- riesgo de abrir pantallas demasiado pronto;
- costo de implementacion;
- compatibilidad con no-runtime/no-execution;
- necesidad de UI nueva o endpoints;
- si conviene guiar antes de auditar incongruencias;
- si conviene reducir densidad antes de inventariar duplicaciones;
- si conviene pulir antes de estabilizar vocabulario.

## Opciones Evaluadas

### Opcion 1 - Operator Guidance / Empty-State Intelligence

Descripcion: mejorar guia sobre que significa cada estado, que falta, que esta bloqueado, que mirar primero y como leer empty states sin ejecutar.

Valor: alto para operador. Riesgo: medio si el frontend mantiene incongruencias y la guia se apoya en nombres/clases viejas. Costo: medio. Dependencia: 1.6, 1.7, 1.8, 1.9, 1.13 y 1.17. UI nueva: no necesariamente. Endpoints: no. Confusion operativa: media si el copy suena a instruccion. Decision: pospuesta cercana.

### Opcion 2 - Density Reduction / Information Architecture

Descripcion: reducir carga visual, agrupar senales, priorizar lo critico y mejorar escaneo sin ocultar datos contractuales.

Valor: alto. Riesgo: medio-alto si se recorta antes de saber que patrones son canonicos, duplicados o legacy. Costo: medio-alto. Dependencia: requiere inventario de incongruencias. UI nueva: no necesariamente. Endpoints: no. Confusion operativa: media. Decision: pospuesta cercana.

### Opcion 3 - Contract Storytelling / Operator Narrative

Descripcion: ordenar la narrativa estado -> contrato -> lectura -> detalle -> limites -> evidencia -> siguiente paso.

Valor: alto para comprension. Riesgo: medio si convierte una auditoria en flujo pseudo-operativo o si narra sobre etiquetas inconsistentes. Costo: medio. Dependencia: boundaries 1.18 y frontend audit. UI nueva: no necesariamente. Endpoints: no. Confusion operativa: media. Decision: pospuesta cercana.

### Opcion 4 - Secondary Console Views / Detail Screens

Descripcion: disenar vistas derivadas read-only y contract-aware.

Valor: medio-alto para separar densidad. Riesgo: alto: crea nueva superficie visual y puede parecer modulo con autoridad propia. Costo: alto. Dependencia: requiere readiness for future screens e inventario de incongruencias. UI nueva: si. Endpoints: no deberia, pero sube presion. Confusion operativa: alta. Decision: pospuesta.

### Opcion 5 - Visual Polish / Premium IA_CORE Layer

Descripcion: mejorar acabado, ritmo, espaciado, jerarquia y microinteracciones sobrias.

Valor: medio-alto. Riesgo: medio: puede decorar deuda, suavizar blockers o volver accionables controles read-only. Costo: medio. Dependencia: mejor despues de incongruence audit y density/guidance. UI nueva: no necesariamente. Endpoints: no. Confusion operativa: media. Decision: pospuesta.

### Opcion 6 - Panel Maestro vs User Panel Separation

Descripcion: evaluar separacion futura de lectura/exposicion entre paneles.

Valor: alto a largo plazo. Riesgo: alto: sugiere roles, privilegios o permisos no declarados. Costo: alto. Dependencia: requiere contratos y readiness for future screens. UI nueva: probable. Endpoints: no deberia, pero presiona contratos. Confusion operativa: alta. Decision: pospuesta lejana.

### Opcion 7 - Component Documentation / Style Reference

Descripcion: profundizar tokens, componentes, estados, usos permitidos/prohibidos y ejemplos.

Valor: medio-alto para crecimiento. Riesgo: bajo-medio si documenta patrones antes de separar canonico/legacy. Costo: bajo-medio. Dependencia: conviene despues de inventario de incongruencias. UI nueva: no. Endpoints: no. Confusion operativa: baja. Decision: pospuesta cercana.

### Opcion 8 - Future Benchmark Review

Descripcion: revisar 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion solo como benchmarks futuros.

Valor: medio. Riesgo: medio: puede distraer o empujar dependencias externas. Costo: bajo-medio. Dependencia: criterios IA_CORE propios mas maduros. UI nueva: no. Endpoints: no. Confusion operativa: baja, dependencia visual media. Decision: pospuesta.

### Opcion 9 - Frontend Incongruence Audit

Descripcion: auditar incongruencias restantes del frontend hecho a mano: nombres heredados, clases ambiguas, microcopy vieja, patrones duplicados, IDs inconsistentes, estilos muertos, JS legacy no-operativo y fragmentos que podrian confundirse con features activas.

Valor: alto para reducir riesgo antes de sumar guidance, density, storytelling o pantallas. Riesgo: bajo si se mantiene como auditoria documental/test sin refactor. Costo: medio-bajo. Dependencia: consume 1.18 porque boundaries ya estan cerrados. UI nueva: no. Endpoints: no. Confusion operativa: baja; precisamente la reduce. Decision: seleccionada.

### Opcion 10 - Readiness for Future Screens

Descripcion: evaluar si la consola esta lista para pantallas secundarias segun contrato, navegacion, boundaries, componentes, responsive, densidad y guia.

Valor: alto antes de abrir vistas. Riesgo: medio si se formula como permiso para construir pantallas demasiado pronto. Costo: medio. Dependencia: requiere primero Frontend Incongruence Audit y posiblemente Density/Guidance. UI nueva: no en auditoria. Endpoints: no. Confusion operativa: media. Decision: pospuesta.

## Matriz De Decision

| Opcion | Reduce riesgo ahora | Claridad operador | Protege mantenimiento | Requiere UI nueva | Riesgo permiso inferido | Decision |
|---|---:|---:|---:|---|---|---|
| Operator Guidance / Empty-State Intelligence | Medio-alto | Alto | Medio | No | Medio | Pospuesta cercana |
| Density Reduction / Information Architecture | Medio-alto | Alto | Medio | No | Medio | Pospuesta cercana |
| Contract Storytelling / Operator Narrative | Medio-alto | Alto | Medio | No | Medio | Pospuesta cercana |
| Secondary Console Views / Detail Screens | Medio | Medio | Medio | Si | Alto | Pospuesta |
| Visual Polish / Premium IA_CORE Layer | Medio | Medio | Bajo-medio | No | Medio | Pospuesta |
| Panel Maestro vs User Panel Separation | Medio | Alto futuro | Medio | Probable | Alto | Pospuesta lejana |
| Component Documentation / Style Reference | Medio | Medio | Alto | No | Bajo-medio | Pospuesta cercana |
| Future Benchmark Review | Bajo-medio | Medio | Bajo | No | Bajo-medio | Pospuesta |
| Frontend Incongruence Audit | Alto | Medio-alto | Alto | No | Bajo | Seleccionada |
| Readiness for Future Screens | Medio-alto | Medio-alto | Medio | No | Medio | Pospuesta |

## Opcion Seleccionada

Veredicto: `NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE`

La opcion seleccionada es:

`Frontend Incongruence Audit`

### Por Que Ahora

Despues de 1.18, los boundaries administrativos ya estan cerrados. El riesgo mas importante antes de crecer no es agregar guia, pantallas o polish, sino entender que incongruencias sobreviven en el frontend hecho a mano. Auditar esos restos reduce riesgo de mantenimiento, evita que guidance copie nombres viejos, evita que density esconda datos criticos y evita que pantallas futuras hereden patrones ambiguos.

### Por Que No Las Otras Primero

Operator Guidance y Contract Storytelling son valiosas, pero dependen de un vocabulario limpio. Density Reduction necesita saber que duplicaciones son seguras de tocar y que datos no pueden perder prioridad. Component Documentation gana precision despues de separar canonico/legacy. Secondary Views, Panel Maestro/User Panel y Readiness for Future Screens amplian superficie conceptual demasiado pronto. Polish y benchmarks externos convienen despues de estabilizar el frontend interno.

### Riesgos Que Reduce

- reintroduccion de permisos inferidos por nombres o clases viejas;
- acumulacion de UI Frankenstein;
- duplicacion de estilos y patrones read-only;
- confusiones entre admin legacy y lectura contract-aware;
- guidance futura redactada sobre estructuras inconsistentes;
- density reduction que recorte datos equivocados;
- pantallas futuras con autoridad visual inventada.

### Que Habilita Despues

- Operator Guidance / Empty-State Intelligence mas precisa;
- Density Reduction / Information Architecture con inventario de piezas criticas;
- Contract Storytelling sobre vocabulario estable;
- Component Documentation / Style Reference con ejemplos reales;
- Readiness for Future Screens con menos riesgo;
- polish premium sobre una base consistente.

### Que No Debe Hacer Todavia

- no refactorizar ni redisenar;
- no crear pantallas;
- no crear rutas;
- no crear componentes;
- no instalar dependencias;
- no tocar backend operativo;
- no activar runtime, execution, dispatch ni controlled execution;
- no ocultar `forbidden_actions` ni `blocked_capabilities`;
- no convertir auditoria en cleanup amplio sin evidencia.

Primer prompt exacto del bloque:

`PROMPT UI/UX 1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution`

## Secuencia Tentativa Del Proximo Bloque

Veredicto: `NEXT_BLOCK_SEQUENCE_PROPOSED`

1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution.

1.21 - Endurecer o documentar incongruencias frontend segun auditoria IA_CORE contract-aware sin runtime/no-execution.

1.22 - Checkpoint Frontend Incongruence IA_CORE contract-aware sin runtime/no-execution.

La secuencia mantiene un prompt por responsabilidad: auditoria, hardening/documentacion acotada si corresponde y checkpoint. No abre pantallas nuevas ni avanza a guidance, density, storytelling, polish o separacion de paneles.

## Opciones Pospuestas

- Operator Guidance / Empty-State Intelligence: pospuesta cercana hasta tener inventario de vocabulario, estados y patrones heredados.
- Density Reduction / Information Architecture: pospuesta cercana hasta saber que duplicaciones pueden tocarse sin ocultar blockers.
- Contract Storytelling / Operator Narrative: pospuesta cercana hasta estabilizar nombres/copy base.
- Secondary Console Views / Detail Screens: pospuestas hasta evitar autoridad visual inventada.
- Visual Polish / Premium IA_CORE Layer: pospuesto para no decorar inconsistencias.
- Panel Maestro vs User Panel Separation: pospuesto porque puede sugerir roles o privilegios no declarados.
- Component Documentation / Style Reference: pospuesta cercana; debe consumir el inventario de incongruencias.
- Future Benchmark Review: 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion quedan benchmarks futuros solamente.
- Readiness for Future Screens: pospuesta hasta cerrar incongruencias y probablemente density/guidance.

Veredicto: `EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY`

## Limites Confirmados

Veredicto: `NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Esta planificacion confirma:

- IA_CORE como identidad visual activa;
- ausencia de SAAOP, S.A.A.O.P., Loteria, lottery, Tactical HUD, U-Score, CAZADOR, ESPEJO y combinatoria como UI activa;
- `backend_internal_ui_payload.v1` y `backend_internal_ui_request.v1` preservados;
- `internal_exposure_registry`, `internal_request_validation`, `internal_dispatcher_no_runtime`, `internal_confirmation_gate` e `internal_response_adapter` preservados como lectura interna;
- `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, warnings, errors, validation, flags, readiness, status, service_kind y schema_version preservados;
- `summary/detail/raw-safe`, paneles 1.7, navegacion 1.8, sistema 1.9, responsive/accessibility 1.13 y admin boundary 1.17 preservados;
- no endpoint publico, API ni router HTTP;
- no hash routing operativo;
- no runtime ni execution;
- no dispatch real;
- no controlled execution;
- no agentes ejecutados;
- no invocacion de models, tools o integrations;
- no cambio de contrato backend;
- no dependencias nuevas;
- no assets externos, templates externos ni referencias instaladas;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones.

## Veredictos Finales

- `UI_UX_NEXT_BLOCK_PLAN_1_19_DEFINED`
- `POST_1_18_STATE_REVIEWED`
- `FRONTEND_RESIDUAL_RISKS_RECORDED`
- `NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE`
- `NEXT_BLOCK_SEQUENCE_PROPOSED`
- `EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY`
- `NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED`
- `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK`

## Continuidad

Veredicto: `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.20 - Auditar incongruencias restantes del frontend IA_CORE contract-aware sin runtime/no-execution`
