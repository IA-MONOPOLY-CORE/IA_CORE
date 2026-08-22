# UI/UX Next Block Plan 1.31

Veredicto: UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED

## Alcance

Este documento consolida el siguiente bloque UI/UX de IA_CORE despues del checkpoint Density Reduction / Information Architecture 1.30. Es una planificacion con evidencia: no implementa el bloque elegido, no redisenia la consola, no limpia frontend adicional, no cambia microcopy visible, no crea pantallas, no crea rutas, no crea componentes, no instala dependencias, no crea endpoints, no activa runtime, no habilita execution, no activa dispatch real y no implementa controlled execution.

Commit base revisado: 57201d71.

Rama esperada revisada: main.

Remoto GitHub revisado: https://github.com/IA-MONOPOLY-CORE/IA_CORE.

Relacion directa: consume docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md, que cerro el bloque 1.27 -> 1.29 y dejo PROMPT UI/UX 1.31 - Consolidar siguiente bloque UI/UX post Density IA_CORE contract-aware sin runtime/no-execution como continuidad.

## Base revisada

- docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_CHECKPOINT_1_30.md
- docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_HARDENING_1_29.md
- docs/UI_UX_DENSITY_INFORMATION_ARCHITECTURE_AUDIT_1_28.md
- docs/UI_UX_NEXT_BLOCK_PLAN_1_27.md
- docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md
- docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md
- docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md
- docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md
- docs/UI_UX_FRONTEND_INCONGRUENCE_HARDENING_1_21.md
- docs/UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md
- docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md
- docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md
- docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md
- docs/UI_UX_COMPONENT_SYSTEM_1_9.md
- docs/UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md
- docs/UI_UX_CONTRACT_DETAIL_PANELS_1_7.md
- docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md
- docs/IA_CORE_GITHUB_BACKUP_READY.md
- README.md
- ui/web/README.md

Archivos frontend revisados como contexto, sin modificarlos: ui/web/index.html, ui/web/styles.css, ui/web/backend-contract-widgets.js, ui/web/admin-panels.js, ui/web/console-interactions.js, ui/web/domains.js y ui/web/i18n_es.json.

Tests revisados como contexto: tests/test_ui_ux_density_information_architecture_checkpoint_1_30.py, tests/test_ui_ux_density_information_architecture_hardening_1_29.py, tests/test_ui_ux_density_information_architecture_audit_1_28.py, tests/test_ui_ux_next_block_plan_1_27.py, tests/test_ui_ux_operator_guidance_empty_state_checkpoint_1_26.py, tests/test_ia_core_github_backup_readiness.py y tests backend contract-aware relevantes.

## Auditoria post 1.30

Veredicto: POST_DENSITY_STATE_REVIEWED

Estado actual de la consola:

- IA_CORE sigue como identidad activa.
- backend_internal_ui_payload.v1 y backend_internal_ui_request.v1 siguen siendo la base contractual de lectura.
- allowed_actions es declaracion backend-only; la UI no concede permisos.
- forbidden_actions y blocked_capabilities siguen visibles, no ejecutables y no ocultos por density.
- request draft conserva read-only, no submit, no dispatch y no execution.
- summary/detail/raw-safe, paneles de detalle 1.7, navegacion interna 1.8 y sistema de componentes 1.9 siguen preservados.
- responsive/accessibility 1.13, admin boundary 1.17, frontend incongruence 1.21, operator guidance 1.25 y density 1.29 siguen activos como capas documentadas.
- No hay SAAOP/Loteria/Tactical HUD/U-Score como UI activa.
- No hay package.json, configuracion Playwright/Vite ni runner visual automatizado detectable.

Que quedo mas claro despues de density:

- La jerarquia P0/P1/P2 permite distinguir critical always visible, lectura primaria y detalle secundario.
- La consola ya no intenta explicar todo con el mismo peso visual.
- El disclosure seguro permite compactar glosario, raw-safe largo y evidencia extendida sin ocultar blockers.
- La lectura summary before detail hace que el operador pueda entender estado/fuente antes de entrar en detalle tecnico.
- El request draft aparece como frontera contractual bloqueada, no como campo operativo.

Narrativa visual que ya existe:

- Header e identidad IA_CORE orientan el estado global.
- Readiness/source explica si hay payload y de donde viene.
- Contract Core / Payload organiza lectura, detalle y raw-safe.
- Actions & Boundaries muestra que permitido, prohibido y bloqueado no son lo mismo.
- Evidence / Checkpoint registra el camino de prompts y checkpoints.
- Next Step funciona como continuidad planned, no workflow activo.

Que sigue sin estar suficientemente narrado:

- El recorrido completo no esta contado como historia unica de operador: estado inicial, informacion recibida, contrato, lectura, limites, evidencia, que falta y por que algo no avanza.
- Los prompts/checkpoints ya existen como bitacora visual, pero falta una narrativa formal que explique como leer esa bitacora.
- Panel Maestro y futuro User Panel todavia no tienen una separacion narrativa de que lenguaje y exposicion pertenece a cada uno.
- Las futuras pantallas secundarias todavia no tienen criterio de cuando una vista deriva de la consola principal sin esconder critical always visible.

Pantallas/vistas futuras que empiezan a asomar:

- Una vista de historia del contrato o recorrido del operador.
- Un futuro Panel Maestro con trazabilidad tecnica y lenguaje dual.
- Un futuro User Panel con lenguaje simple y exposicion reducida.
- Vistas secundarias read-only para detalle, evidencia o estado, pero solo despues de definir narrativa y readiness.

Riesgos reducidos:

- Menor riesgo de saturacion inmediata.
- Menor riesgo de esconder blockers al compactar.
- Menor riesgo de que allowed_actions parezca permiso UI.
- Menor riesgo de que Next Step parezca workflow operativo.
- Menor riesgo de abrir pantallas secundarias solo para escapar de densidad.

Riesgos vivos:

- La consola todavia puede leerse como inventario tecnico si no se ordena la historia.
- La evidencia de prompts/checkpoints puede crecer sin una narrativa que explique su lugar.
- Panel Maestro / User Panel podria separarse prematuramente si no hay relato y limites claros.
- Secondary views podrian nacer como pantallas nuevas antes de saber que historia deben contar.
- Visual polish podria maquillar estructura narrativa incompleta.
- Benchmark review externo podria distraer de criterios internos ya consolidados.
- No hay runner visual automatizado; la evidencia humana sigue siendo importante.

Evidencia humana considerada: el operador reviso localhost despues de 1.29, dijo Lo veo muy bien y En pocas palabras veo gráficamente los prompts que mandamos. La UI se percibe como bitácora visual, resumen y capa de comprensión. Esa evidencia cambia la prioridad: luego de ordenar densidad, el mayor valor no es crear pantallas, sino contar mejor el recorrido que la consola ya esta mostrando.

Criterio de metodo del operador considerado: desarmar la pieza completa, limpiar incongruencias, pulir lo existente, reensamblar y verificar primero; despues vendran mejoras, pantallas, paneles, experiencia final e integraciones. Formula: First truth, then beauty, then level.

Bloque que parece mas logico ahora: Contract Storytelling / Operator Narrative.

## Opciones candidatas evaluadas

| Opcion | Descripcion | Valor | Riesgo | Costo | Dependencia previa | UI nueva | Endpoints | Confusion operativa | Conviene | Habilita luego | Que no debe hacer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Contract Storytelling / Operator Narrative | Ordenar la consola como recorrido entendible: estado inicial, informacion recibida, contrato, lectura, detalle, limites, evidencia, proximo paso, por que algo esta bloqueado y que falta para avanzar. | Muy alto: aprovecha que la UI ya funciona como bitácora visual y aumenta claridad sin abrir pantallas. | Medio si se narra como flujo operativo o progreso ejecutable. | Medio. | Requiere density 1.29/1.30 para narrar sobre jerarquia clara. | No en auditoria; hardening futuro puede ser acotado. | No. | Media si usa verbos de accion o estados operativos. | Ahora. | Panel Maestro/User Panel, readiness for future screens y secondary views. | No representar runtime, dispatch, execution, submit ni operacion. |
| Panel Maestro vs User Panel Separation Planning | Planificar diferencias de acceso, exposicion y lenguaje entre operador interno y usuario final. | Alto futuro. | Medio-alto: puede ocultar demasiado o separar sin relato comun. | Medio. | Necesita storytelling para saber que historia se cuenta a cada publico. | No en plan. | No. | Media. | Despues. | Superficies diferenciadas y menor jerga en usuario. | No esconder blockers ni inventar permisos. |
| Readiness for Future Screens | Evaluar si la consola ya puede derivar pantallas secundarias o necesita consolidacion. | Alto antes de construir vistas. | Medio: puede leerse como permiso para crear pantallas. | Medio. | Necesita narrativa para saber que pantalla cuenta que parte. | No en auditoria. | No. | Media. | Despues de storytelling. | Secondary Console Views con criterio. | No crear rutas ni pantallas. |
| Secondary Console Views / Detail Screens | Diseñar posibles vistas derivadas read-only para detalle/evidencia/estado. | Medio-alto futuro. | Alto: abre superficie prematura y puede mover critical info fuera de la consola. | Alto. | Necesita storytelling y readiness. | Si, en bloque posterior. | No deberia. | Alta si parece modulo operativo. | Despues. | Navegacion secundaria contract-aware. | No crear hash routing, rutas, endpoints ni pantallas ahora. |
| Component Documentation / Style Reference | Profundizar reglas de componentes, tokens, estados, densidad y usos permitidos/prohibidos. | Medio. | Bajo-medio: documenta, pero no resuelve aun la historia del operador. | Bajo-medio. | Consume 1.9 y density 1.29. | No. | No. | Baja. | Despues o como soporte. | Sistema visual mas consistente. | No crear libreria, framework ni acciones fantasma. |
| Visual Polish / Premium IA_CORE Layer | Mejorar acabado, ritmo, jerarquia fina y microinteracciones sobrias. | Medio perceptivo. | Medio: polish prematuro puede embellecer una narrativa incompleta. | Medio. | Conviene despues de storytelling. | No necesariamente. | No. | Media si anima estados bloqueados como actividad. | Despues. | Experiencia mas madura. | No instalar Motion/Framer ni confundir belleza con capacidad. |
| Future Benchmark Review | Revisar 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion como benchmarks futuros. | Bajo ahora. | Medio: puede empujar templates, assets externos o dependencias. | Bajo. | Mejor con narrativa interna ya definida. | No. | No. | Baja. | Despues. | Inspiracion controlada. | No instalar, no copiar, no usar como fuente operativa. |
| Backup / Continuity Policy Review | Ajustar politica de restore points y documentacion de continuidad. | Medio transversal. | Bajo. | Bajo. | Ya existe restore point remoto 1.30. | No. | No. | Baja. | No como bloque principal. | Disciplina de restauracion. | No hacer push por cada prompt ni force push. |

## Matriz de decision

| Opcion | Continuidad post-density | Aprovecha bitácora visual | Aumenta claridad narrativa | Prepara Panel Maestro/User Panel | Prepara futuras pantallas | Evita pantallas prematuras | Evita polish prematuro | Mantiene contract-awareness | Mantiene no-runtime/no-execution | Bajo costo relativo | Impacto visual controlado | Prepara bloques futuros | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Contract Storytelling / Operator Narrative | Muy alto | Muy alto | Muy alto | Alto | Alto | Alto | Alto | Alto | Alto | Medio | Alto | Muy alto | Seleccionada |
| Panel Maestro vs User Panel Separation Planning | Medio | Medio | Medio-alto | Muy alto | Medio | Medio | Alto | Alto | Alto | Medio | Medio | Alto | Pospuesta |
| Readiness for Future Screens | Medio | Medio | Medio | Medio | Muy alto | Medio | Alto | Alto | Alto | Medio | Bajo | Alto | Pospuesta |
| Secondary Console Views / Detail Screens | Bajo | Medio | Medio | Medio | Alto | Bajo | Medio | Medio | Alto | Bajo | Bajo | Alto futuro | Pospuesta lejana |
| Component Documentation / Style Reference | Medio | Bajo | Bajo-medio | Medio | Medio | Alto | Alto | Alto | Alto | Alto | Medio | Medio | Pospuesta |
| Visual Polish / Premium IA_CORE Layer | Medio | Medio | Medio | Bajo | Medio | Medio | Bajo | Medio | Alto | Medio | Medio | Medio | Pospuesta |
| Future Benchmark Review | Bajo | Bajo | Bajo | Bajo | Bajo | Alto | Medio | Medio | Alto | Alto | Bajo | Medio | Pospuesta |
| Backup / Continuity Policy Review | Medio | Bajo | Bajo | Bajo | Bajo | Alto | Alto | Alto | Alto | Alto | Alto | Medio | Transversal |

## Bloque seleccionado

Veredicto: NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE

Seleccion: Contract Storytelling / Operator Narrative.

Por que ahora:

- Density 1.29/1.30 ya ordeno jerarquia, redujo competencia visual y establecio critical always visible, secondary readable y disclosure seguro.
- La evidencia humana confirma que el operador ya ve graficamente los prompts y checkpoints como bitacora visual.
- El siguiente riesgo no es falta de datos ni falta de density, sino falta de relato: como leer IA_CORE como sistema.
- Storytelling aumenta claridad sin crear pantallas nuevas ni tocar contrato backend.
- Permite preparar Panel Maestro / User Panel desde una historia comun antes de separar superficies.
- Permite preparar future screens desde una narrativa y no desde impulso visual.

Por que no las otras primero:

- Panel Maestro vs User Panel necesita saber que historia conserva el operador interno y cual se traduce al usuario final.
- Readiness for Future Screens necesita criterios narrativos para decidir que merece una pantalla secundaria.
- Secondary Console Views ampliaria superficie antes de definir que recorrido cuenta cada vista.
- Component Documentation ayuda, pero no responde todavia a como se entiende el sistema de punta a punta.
- Visual Polish debe esperar para no embellecer una historia incompleta.
- Future Benchmark Review debe seguir como inspiracion futura, no fuente operativa.
- Backup Policy Review queda transversal porque ya hay restore point remoto 1.30.

Riesgos que reduce:

- que la consola siga siendo inventario tecnico;
- que la bitacora visual crezca sin estructura narrativa;
- que pantallas futuras nazcan antes de saber que problema explican;
- que Panel Maestro/User Panel se separen por estetica y no por exposicion/relato;
- que polish o benchmarks externos empujen decisiones prematuras.

Que habilita despues:

- Panel Maestro vs User Panel Separation Planning con lenguaje y exposicion mejor definidos;
- Readiness for Future Screens con criterios de que historia va a que vista;
- Secondary Console Views read-only sin mover informacion critica fuera de la consola principal;
- Component Documentation orientada por narrativa real;
- Visual Polish con jerarquia y relato ya validados.

Que no debe hacer todavia:

- no implementar storytelling en 1.31;
- no crear pantallas nuevas;
- no crear rutas ni hash routing;
- no cambiar microcopy visible;
- no crear endpoints, fetches ni dependencias;
- no activar runtime, execution, dispatch ni controlled execution;
- no convertir allowed_actions en botones UI;
- no ocultar forbidden_actions ni blocked_capabilities;
- no reintroducir SAAOP/Loteria/Tactical HUD/U-Score como UI activa;
- no usar start, run, execute, dispatch, launch, operate o live como CTA activo.

Primer prompt exacto del bloque:

PROMPT UI/UX 1.32 - Auditar Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution

## Secuencia tentativa del proximo bloque

Veredicto: NEXT_BLOCK_SEQUENCE_PROPOSED

- PROMPT UI/UX 1.32 - Auditar Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution.
- PROMPT UI/UX 1.33 - Endurecer narrativa de operador IA_CORE contract-aware sin runtime/no-execution.
- PROMPT UI/UX 1.34 - Checkpoint Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution.

La secuencia mantiene un prompt por responsabilidad: auditoria, hardening acotado y checkpoint. No abre pantallas nuevas por defecto, no crea rutas, no instala dependencias, no activa runtime y no avanza a Panel Maestro/User Panel, secondary views, polish o benchmarks externos.

## Opciones pospuestas

- Panel Maestro vs User Panel Separation Planning: pospuesto porque necesita una narrativa comun y criterios de exposicion antes de separar lenguaje/acceso.
- Readiness for Future Screens: pospuesto porque conviene definir primero que historia debe sostener la consola principal.
- Secondary Console Views / Detail Screens: pospuesto porque abrir vistas ahora aumenta superficie y podria esconder critical always visible.
- Component Documentation / Style Reference: pospuesto como soporte posterior; puede formalizar componentes despues de saber que narrativa sostienen.
- Visual Polish / Premium IA_CORE Layer: pospuesto para no confundir belleza con capacidad ni maquillar relato incompleto.
- Future Benchmark Review: pospuesto; 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion permanecen como benchmarks futuros solamente, sin instalar, sin copiar, sin dependencia, sin templates externos y sin fuente operativa.
- Backup / Continuity Policy Review: tratado como politica transversal, no como bloque UI principal.

Veredicto: EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY

## Riesgos residuales

- La consola sigue siendo grande y tecnica aunque density haya reducido competencia visual.
- La narrativa todavia puede confundirse con flujo operativo si se usan verbos de accion o estados activos.
- No existe runner visual automatizado local; la validacion visual humana seguira importando.
- Panel Maestro / User Panel sigue sin separacion formal.
- Futuras pantallas secundarias siguen sin readiness especifica.
- Component documentation y polish aun estan pendientes.
- Cualquier storytelling futuro debe preservar forbidden_actions, blocked_capabilities, no_payload, no-runtime/no-execution, request draft read-only y warnings/errors.

## Politica de backup

Veredicto: BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES

IA_CORE ya tiene restore point remoto actualizado hasta 57201d71 despues del checkpoint 1.30. No hace falta push despues de cada prompt de planificacion.

Este commit 1.31 puede quedar local por defecto. El proximo backup recomendado deberia ocurrir despues del checkpoint del proximo bloque, es decir despues de PROMPT UI/UX 1.34 - Checkpoint Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution, salvo cambio critico o decision explicita del operador.

Si se hiciera push, debe ser normal y sin force push.

## Preservacion contractual

Veredicto: NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED

La planificacion preserva:

- backend_internal_ui_payload.v1;
- backend_internal_ui_request.v1;
- internal_exposure_registry;
- internal_request_validation;
- internal_dispatcher_no_runtime;
- internal_confirmation_gate;
- internal_response_adapter;
- allowed_actions;
- forbidden_actions;
- blocked_capabilities;
- warnings;
- errors;
- validation;
- flags;
- readiness;
- status;
- service_kind;
- schema_version;
- summary/detail/raw-safe;
- paneles de detalle 1.7;
- navegacion interna 1.8;
- sistema de componentes 1.9;
- responsive/accessibility hardening 1.13;
- admin boundary hardening 1.17;
- frontend incongruence hardening 1.21;
- operator guidance hardening 1.25;
- operator guidance checkpoint 1.26;
- density/information architecture hardening 1.29;
- density/information architecture checkpoint 1.30.

Confirmado:

- IA_CORE como identidad activa;
- no legacy visual activo: no SAAOP/Loteria/Tactical HUD/U-Score como UI activa;
- no endpoint publico, API ni router HTTP nuevo;
- no hash routing operativo nuevo;
- no runtime, no execution, no dispatch real y no controlled execution;
- no dependencias nuevas;
- no cambios en core/, api.py, domains/, tools/, modelos ni integraciones;
- no recomendacion de activar capacidades bloqueadas;
- no recomendacion de instalar referencias externas;
- no recomendacion de crear nuevas pantallas en 1.31.

## Veredictos

- UI_UX_NEXT_BLOCK_PLAN_1_31_DEFINED
- POST_DENSITY_STATE_REVIEWED
- NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE
- NEXT_BLOCK_SEQUENCE_PROPOSED
- OPERATOR_VISUAL_LOG_EVIDENCE_CONSIDERED
- OPERATOR_METHOD_CRITERION_CONSIDERED
- BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES
- EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY
- NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED
- UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK

## Proximo prompt exacto

PROMPT UI/UX 1.32 - Auditar Contract Storytelling / Operator Narrative IA_CORE contract-aware sin runtime/no-execution
