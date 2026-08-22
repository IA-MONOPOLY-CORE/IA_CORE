# UI/UX Next Block Plan 1.27

Veredicto: `UI_UX_NEXT_BLOCK_PLAN_1_27_DEFINED`

## Alcance

Este documento consolida el siguiente bloque UI/UX de IA_CORE despues del checkpoint Operator Guidance / Empty-State Intelligence `1.26`. Es una planificacion con evidencia: no implementa el bloque elegido, no reduce densidad todavia, no limpia frontend adicional, no redisenia la consola, no crea pantallas, no crea rutas, no agrega componentes, no instala dependencias, no crea endpoints, no activa runtime, no habilita execution, no activa dispatch real y no implementa controlled execution.

Commit base revisado: `a62c7c01`.

Rama esperada revisada: `main`.

Remoto GitHub revisado: `https://github.com/IA-MONOPOLY-CORE/IA_CORE`.

Relacion directa: consume `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md`, que cerro el bloque `1.23 -> 1.25` y dejo `PROMPT UI/UX 1.27 - Consolidar siguiente bloque UI/UX post Operator Guidance IA_CORE contract-aware sin runtime/no-execution` como continuidad.

## Base revisada

- `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_CHECKPOINT_1_26.md`
- `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_HARDENING_1_25.md`
- `docs/UI_UX_OPERATOR_GUIDANCE_EMPTY_STATE_AUDIT_1_24.md`
- `docs/UI_UX_NEXT_BLOCK_PLAN_1_23.md`
- `docs/UI_UX_FRONTEND_INCONGRUENCE_CHECKPOINT_1_22.md`
- `docs/UI_UX_FRONTEND_INCONGRUENCE_HARDENING_1_21.md`
- `docs/UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md`
- `docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md`
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md`
- `docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md`
- `docs/UI_UX_COMPONENT_SYSTEM_1_9.md`
- `docs/UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md`
- `docs/UI_UX_CONTRACT_DETAIL_PANELS_1_7.md`
- `docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md`
- `docs/IA_CORE_GITHUB_BACKUP_READY.md`
- `README.md`
- `ui/web/README.md`

Archivos frontend revisados como contexto, sin modificarlos: `ui/web/index.html`, `ui/web/styles.css`, `ui/web/backend-contract-widgets.js`, `ui/web/admin-panels.js`, `ui/web/console-interactions.js`, `ui/web/domains.js` y `ui/web/i18n_es.json`.

## Estado post Operator Guidance

Veredicto: `POST_OPERATOR_GUIDANCE_STATE_REVIEWED`

Despues de 1.26 la consola IA_CORE esta mas explicada y menos ambigua:

- `no_payload`, `not_available`, `pending`, `planned`, `blocked` y `read-only` tienen guidance visible o documentada;
- `allowed_actions` se mantiene como lectura backend-declared, no permiso UI;
- `forbidden_actions` y `blocked_capabilities` permanecen visibles y no ejecutables;
- request draft queda bloqueado, sin submit, sin dispatch y sin execution;
- internal exposure queda explicado como lectura interna read-only, no endpoint publico;
- raw-safe/detail panels explican ausencia honesta, limites y omisiones seguras;
- Panel Maestro aplica lenguaje claro + termino tecnico entre parentesis;
- Panel Usuario queda documentado como futuro, no implementado.

Que guia mejor al operador ahora:

- el header orienta que la consola lee contrato y senales declaradas;
- la tira de operator guidance explica que se mira, que falta y que esta bloqueado;
- los estados honestos tienen causa, consecuencia o limite;
- Next Step se lee como continuidad planned, no workflow activo;
- los blockers ya no dependen solo de color o badge.

Que sigue denso:

- una sola pantalla acumula orientacion, ruta de lectura, navigation, summary/detail/raw-safe, detail panels, widgets, internal signals, boundaries, evidence, request draft y paneles administrativos;
- conteo contextual de `ui/web/index.html`: `<section=11`, `<article=19`, `hud-panel=26`, `data-widget=52`, `layout-section=12`, `contract-detail-panel=16`, `config-section=15`, `admin-block=16`, `visual-state=16`, `layout-token=20`;
- los textos de guidance ayudan, pero pueden competir con datos contractuales si se siguen sumando;
- mobile ya esta protegido por 1.14/1.13, pero la densidad sigue siendo deuda conocida.

Que compite por atencion:

- badges de estado, tarjetas de readiness, widgets contractuales y detail panels explican informacion cercana;
- evidence/checkpoint y Next Step conviven con datos de contrato, por lo que pueden parecer otra prioridad de lectura;
- admin panels preexistentes aportan valor interno, pero amplian ruido visual si se mezclan con lectura contract-aware principal;
- estilos historicos no enlazados o duplicados siguen como deuda documentada, no bloqueo inmediato.

Riesgos reducidos:

- menor riesgo de interpretar naming heredado como runtime;
- menor riesgo de acciones fantasma;
- menor riesgo de leer `planned` como workflow disponible;
- menor riesgo de ocultar `forbidden_actions` o `blocked_capabilities`;
- menor riesgo de que Panel Maestro use jerga sin traduccion minima.

Riesgos vivos:

- saturacion por exceso de guidance en una pantalla unica;
- doble explicacion entre summary/detail/widgets/detail panels;
- jerarquia visual aun no prioriza con suficiente fuerza que mirar primero;
- abrir pantallas secundarias ahora podria esconder deuda de arquitectura de informacion;
- polish prematuro podria embellecer una estructura aun densa;
- separacion Panel Maestro / Panel Usuario necesita mapa de exposicion antes de implementarse;
- no hay runner visual automatizado detectable: `package.json=False`, Playwright=False y Vite=False.

Evidencia humana considerada: el operador observo que el frontend en `localhost` empieza a reflejar lo trabajado como resumenes y se siente interesante. Se registra como evidencia de que IA_CORE empieza a funcionar como bitacora visual / capa de comprension, no solo como pantalla estatica. Esa misma evidencia sugiere no correr a nuevas pantallas: primero conviene ordenar lo que la bitacora muestra.
## Opciones candidatas evaluadas

| Opcion | Descripcion | Valor | Riesgo | Costo | Dependencia previa | UI nueva | Endpoints | Confusion operativa | Conviene | Habilita luego | Que no debe hacer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Density Reduction / Information Architecture | Reducir carga visual, agrupar senales, ordenar jerarquia y mejorar escaneo sin ocultar contrato. | Muy alto: ataca la deuda residual mas visible post-guidance. | Medio si recorta verdad contractual o esconde blockers. | Medio. | Requiere 1.25/1.26 para saber que texto conservar. | No necesariamente. | No. | Baja si mantiene read-only y blockers visibles. | Ahora. | Contract Storytelling, future screens y polish. | No ocultar `forbidden_actions`, `blocked_capabilities`, warnings, errors ni raw-safe. |
| Contract Storytelling / Operator Narrative | Convertir la consola en un recorrido entendible: estado, payload, contrato, limites, evidencia y que falta. | Alto para comprension. | Medio: puede parecer flujo operativo si se narra como progreso. | Medio. | Necesita density para no narrar sobre saturacion. | No necesariamente. | No. | Media si usa verbos de accion. | Despues de density. | Pantallas futuras y User Panel. | No representar runtime, dispatch ni execution. |
| Readiness for Future Screens | Evaluar si la consola esta lista para abrir vistas secundarias. | Alto antes de construir pantallas. | Medio: puede leerse como permiso para crear vistas. | Medio. | Necesita density y storytelling. | No en auditoria. | No. | Media. | Despues. | Secondary Console Views. | No crear rutas ni pantallas. |
| Panel Maestro vs User Panel Separation Planning | Planificar acceso, exposicion y lenguaje para operador interno vs usuario final. | Alto futuro. | Medio-alto: puede introducir ocultamiento prematuro o privilegios visuales confusos. | Medio. | Necesita mapa de informacion y narrativa. | No en plan. | No. | Media. | Despues de density/storytelling. | Experiencia final con menor jerga. | No ocultar bloqueos ni inventar permisos. |
| Secondary Console Views / Detail Screens | Disenar vistas derivadas read-only. | Medio-alto para separar complejidad. | Alto: amplia superficie antes de resolver jerarquia. | Alto. | Necesita readiness y separacion de informacion. | Si. | No deberia. | Alta si parece modulo operativo. | Despues. | Navegacion secundaria contract-aware. | No crear rutas, hash routing ni pantallas ahora. |
| Component Documentation / Style Reference | Documentar tokens, componentes, estados y usos permitidos/prohibidos. | Medio. | Bajo-medio: puede volverse documentacion sin impacto visual inmediato. | Bajo-medio. | Consume 1.9 y checkpoints posteriores. | No. | No. | Baja. | Despues o en paralelo menor. | Sistema visual mas consistente. | No crear libreria ni framework. |
| Visual Polish / Premium IA_CORE Layer | Mejorar ritmo, espaciado, microinteracciones sobrias y percepcion premium. | Medio-alto perceptivo. | Medio: polish prematuro puede maquillar densidad. | Medio. | Conviene despues de density. | No necesariamente. | No. | Media si parece activar controles. | Despues. | Capa visual madura. | No instalar Motion/Framer ni teatralizar estados. |
| Future Benchmark Review | Revisar 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion como referencias futuras. | Medio-bajo ahora. | Medio: puede empujar templates/dependencias externas. | Bajo. | Mejor con criterios internos mas claros. | No. | No. | Baja. | Despues. | Inspiracion controlada. | No instalar, no copiar, no usar como fuente operativa. |
| Backup / Continuity Policy Review | Revisar politica de backup y restore points. | Medio transversal. | Bajo. | Bajo. | Ya existe backup hasta 1.26. | No. | No. | Baja. | No como bloque principal. | Disciplina de restauracion. | No hacer push por cada prompt ni force push. |

## Matriz de decision

| Opcion | Reduce riesgo | Aumenta claridad | Mejora escaneo | Reduce saturacion | Utilidad operador | Evita doble trabajo | Evita pantallas prematuras | Contract-aware | No-runtime/no-execution | Bajo costo relativo | Impacto visual controlado | Prepara futuros bloques | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Density Reduction / Information Architecture | Alto | Alto | Muy alto | Muy alto | Alto | Alto | Alto | Alto | Alto | Medio | Alto | Alto | Seleccionada |
| Contract Storytelling / Operator Narrative | Medio | Alto | Medio | Medio | Alto | Medio | Medio | Alto | Alto | Medio | Medio | Alto | Pospuesta inmediata |
| Readiness for Future Screens | Medio | Medio | Medio | Bajo | Medio | Medio | Bajo | Alto | Alto | Medio | Bajo | Alto | Pospuesta |
| Panel Maestro vs User Panel Separation Planning | Medio | Medio-alto | Medio | Medio | Alto futuro | Medio | Medio | Alto | Alto | Medio | Bajo | Alto | Pospuesta |
| Secondary Console Views / Detail Screens | Bajo | Medio | Medio | Medio futuro | Medio | Bajo | Bajo | Medio | Alto | Bajo | Bajo | Alto futuro | Pospuesta lejana |
| Component Documentation / Style Reference | Medio | Medio | Bajo | Bajo | Medio | Medio | Alto | Alto | Alto | Alto | Medio | Medio | Pospuesta |
| Visual Polish / Premium IA_CORE Layer | Bajo | Medio | Medio | Bajo | Medio | Bajo | Medio | Medio | Alto | Medio | Medio | Medio | Pospuesta |
| Future Benchmark Review | Bajo | Bajo | Bajo | Bajo | Bajo | Bajo | Alto | Medio | Alto | Alto | Bajo | Medio | Pospuesta |
| Backup / Continuity Policy Review | Medio | Bajo | Bajo | Bajo | Medio | Medio | Alto | Alto | Alto | Alto | Alto | Medio | Transversal |

## Bloque seleccionado

Veredicto: `NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE`

Seleccion: `Density Reduction / Information Architecture`.

Por que ahora:

- 1.25/1.26 ya explicaron estados y empty states; el riesgo principal deja de ser falta de guidance y pasa a ser exceso de senales compitiendo;
- la consola ya funciona como bitacora visual / capa de comprension, pero una bitacora util necesita jerarquia: que mirar primero, que queda secundario y que es evidencia;
- density reduction evita que la ayuda agregada se transforme en manual gigante;
- mejora escaneo en desktop y mobile sin crear pantallas nuevas;
- prepara storytelling porque primero ordena piezas, luego se narra el recorrido;
- prepara future screens porque permite saber que debe quedarse en la consola principal y que podria derivarse despues;
- mantiene contract-awareness porque no recorta blockers ni convierte acciones en permisos.

Por que no las otras primero:

- Contract Storytelling necesita una arquitectura de informacion mas clara para no parecer flujo operativo;
- Readiness for Future Screens seria prematuro antes de resolver jerarquia y densidad;
- Panel Maestro vs User Panel necesita mapa de exposicion y lenguaje estable despues de ordenar la consola;
- Secondary Console Views ampliaria superficie y podria esconder deuda en vez de resolverla;
- Component Documentation ayuda, pero no reduce la saturacion del operador en la pantalla real;
- Visual Polish puede mejorar percepcion, pero no arregla prioridad informativa;
- Future Benchmark Review debe esperar criterios internos mas maduros y sigue solo como benchmark futuro;
- Backup Policy Review queda transversal, no como bloque UI principal.

Riesgos que reduce:

- saturacion por guidance acumulada;
- lectura dispersa entre widgets, details y admin panels;
- competencia visual entre evidence, Next Step y estado contractual;
- necesidad falsa de crear pantallas para aliviar complejidad;
- polish prematuro sobre estructura densa.

Que habilita despues:

- `Contract Storytelling / Operator Narrative` con menos ruido;
- `Readiness for Future Screens` con inventario de que mover o conservar;
- eventual `Panel Maestro vs User Panel Separation Planning` con mapa de exposicion mas limpio;
- `Visual Polish / Premium IA_CORE Layer` con jerarquia ya definida.

Que no debe hacer todavia:

- no implementar reduccion de densidad en 1.27;
- no ocultar `forbidden_actions`, `blocked_capabilities`, warnings, errors ni raw-safe;
- no crear pantallas nuevas;
- no crear rutas ni hash routing;
- no crear endpoints, fetches ni dependencias;
- no activar runtime, execution, dispatch ni controlled execution;
- no convertir `allowed_actions` en botones UI;
- no reintroducir legacy visual activo.

Primer prompt exacto del bloque:

`PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution`
## Secuencia tentativa del proximo bloque

Veredicto: `NEXT_BLOCK_SEQUENCE_PROPOSED`

- `PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution`.
- `PROMPT UI/UX 1.29 - Endurecer densidad y arquitectura de informacion IA_CORE contract-aware sin runtime/no-execution`.
- `PROMPT UI/UX 1.30 - Checkpoint Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution`.

La secuencia mantiene un prompt por responsabilidad: auditoria, hardening acotado y checkpoint. No abre pantallas nuevas, no crea rutas, no instala dependencias, no activa runtime y no avanza a storytelling, polish o separacion de paneles.

## Opciones pospuestas

- Contract Storytelling / Operator Narrative: pospuesto hasta que la arquitectura de informacion reduzca ruido y determine la ruta de lectura principal.
- Readiness for Future Screens: pospuesto porque conviene saber primero que debe mantenerse en la consola principal.
- Panel Maestro vs User Panel Separation Planning: pospuesto porque necesita mapa de exposicion, densidad y narrativa antes de decidir diferencias de lenguaje/acceso.
- Secondary Console Views / Detail Screens: pospuesto porque ampliar superficie ahora aumenta costo y riesgo de autoridad visual nueva.
- Component Documentation / Style Reference: pospuesto; puede venir despues de ver que componentes sobreviven al ajuste de densidad.
- Visual Polish / Premium IA_CORE Layer: pospuesto para no maquillar saturacion estructural.
- Future Benchmark Review: pospuesto; 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion permanecen como benchmarks futuros solamente, sin instalar, sin copiar, sin dependencia y sin fuente operativa.
- Backup / Continuity Policy Review: tratado como politica transversal, no como bloque UI principal.

Veredicto: `EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY`

## Riesgos residuales

- La densidad visual sigue alta aunque sea comprensible.
- La UI activa todavia mezcla consola principal, evidence, request draft y paneles administrativos en una superficie grande.
- `styles.css` conserva reglas historicas o posiblemente no enlazadas que no deben limpiarse sin auditoria especifica.
- Admin/domain fetches preexistentes siguen siendo frontera a documentar como gestion/lectura, no permiso contract-aware.
- No hay runner visual automatizado; la revision humana seguira siendo importante para desktop/mobile hasta que exista infraestructura visual.
- La separacion futura Panel Maestro / Panel Usuario todavia no tiene contrato visual propio.
- Cualquier reduccion de densidad debe evitar esconder blockers o errores.

## Politica de backup

Veredicto: `BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES`

IA_CORE ya tiene backup remoto actualizado hasta `a62c7c01` despues del checkpoint 1.26. No hace falta push despues de cada prompt de planificacion.

Este commit 1.27 puede quedar local por defecto. El proximo backup recomendado deberia ocurrir despues del checkpoint del proximo bloque, es decir despues de `PROMPT UI/UX 1.30 - Checkpoint Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution`, salvo cambio critico o decision explicita del operador.

Si se hiciera push, debe ser normal y sin force push.

## Preservacion contractual

Veredicto: `NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

La planificacion preserva:

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
- `schema_version`;
- `summary/detail/raw-safe`;
- paneles de detalle 1.7;
- navegacion interna 1.8;
- sistema de componentes 1.9;
- responsive/accessibility hardening 1.13;
- admin boundary hardening 1.17;
- frontend incongruence hardening 1.21;
- checkpoint frontend incongruence 1.22;
- operator guidance hardening 1.25;
- checkpoint operator guidance 1.26.

Confirmado:

- IA_CORE como identidad activa;
- no legacy visual activo: no SAAOP/Loteria/Tactical HUD/U-Score como UI activa;
- no endpoint publico, API ni router HTTP nuevo;
- no hash routing operativo nuevo;
- no runtime, no execution, no dispatch real y no controlled execution;
- no dependencias nuevas;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones;
- no recomendacion de activar capacidades bloqueadas.

Veredicto: `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK`

## Veredictos finales

- `UI_UX_NEXT_BLOCK_PLAN_1_27_DEFINED`
- `POST_OPERATOR_GUIDANCE_STATE_REVIEWED`
- `NEXT_UI_UX_BLOCK_SELECTED_WITH_EVIDENCE`
- `NEXT_BLOCK_SEQUENCE_PROPOSED`
- `BACKUP_POLICY_RECORDED_FOR_BLOCK_CLOSURES`
- `EXTERNAL_REFERENCES_REMAIN_BENCHMARKS_ONLY`
- `NEXT_BLOCK_PLAN_NO_RUNTIME_NO_EXECUTION_CONFIRMED`
- `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK`

## Cierre

Este prompt planifica y no avanza al bloque elegido. El siguiente bloque seleccionado es `Density Reduction / Information Architecture`.

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.28 - Auditar Density Reduction / Information Architecture IA_CORE contract-aware sin runtime/no-execution`