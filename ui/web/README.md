# Consola web principal

`ui/web/` es la consola principal de IA_CORE. FastAPI la sirve como contenido
estático; la superficie 1.0 mantiene sus lecturas preexistentes separadas de
la autoridad contractual que decide acciones y bloqueos.

## Paneles internos migrados

| Sección | API utilizada |
|---|---|
| Memory | `GET /api/memory` |
| Logs | `GET /api/logs` |
| Hybrid | `GET /api/status?full=true` |
| Request contract | lectura de sources declaradas; dispatch bloqueado sin `allowed_actions` |
| Overview | `GET /api/status` |
| Backend contract widgets | payload inyectado `backend_internal_ui_payload.v1` |

`admin-panels.js` implementa estas secciones del modal de configuración. Los
controles de dispatch visibles quedan bloqueados si no hay contrato backend
que los declare en `allowed_actions`.

## Layout superior 0.8

La superficie activa incorpora una shell `data-layout-contract-aware="superior-0.8"`
para ordenar la UI alrededor de identidad IA_CORE, readiness global,
contrato/payload, servicios internos, acciones permitidas/prohibidas,
blocked capabilities, evidencia y próximos pasos.

Esta capa no agrega endpoints, no ejecuta requests operativos y no cambia el
contrato backend. Solo organiza visualmente el estado pre-runtime/no-execution
ya confirmado en `docs/UI_UX_CONTRACT_AWARE_CHECKPOINT_0_6.md` y
`docs/UI_UX_VISUAL_ARCHITECTURE_0_7.md`.

## Consola principal 1.0

La shell conserva `data-layout-contract-aware="superior-0.8"` y agrega
`data-main-console="contract-aware-1.0"`. La pantalla principal se organiza en
identidad IA_CORE, readiness global, Contract Core / Payload, señales de
servicios internos, Actions & Boundaries y Evidence / Checkpoint.

Los widgets de `backend_internal_ui_payload.v1` viven ahora en Contract Core /
Payload de la consola principal. El cambio reutiliza los mismos IDs y el mismo
renderer, sin agregar fetches ni fuentes de permiso. La sección de configuración
solo conserva una referencia de navegación a su ubicación principal.

La consola declara `pre-runtime / no-execution`, mantiene deny-by-default ante
`no_payload`, muestra `forbidden_actions` y `blocked_capabilities`, y no habilita
acciones fuera de `allowed_actions`.

## Refinamiento de consola 1.1

La marca `data-console-refinement="1.1"` identifica el refinamiento visual de
la consola principal sin crear una pantalla nueva. Readiness y Contract Core
reflejan el mismo payload inyectado que consumen los widgets; ante ausencia o
invalidez mantienen `no_payload`, `pending`, `invalid` o `failed` sin inferir
capacidades.

Internal Services / Signals usa filas de lectura para distinguir registry,
validation, dispatcher no-runtime, confirmation gate, response adapter y
stable payloads. Actions & Boundaries separa permiso declarado, prohibicion y
capacidad bloqueada sin agregar CTAs.

La capa visual reduce efectos ornamentales, mejora contraste y espaciado, y
mantiene responsive a 1440 px y 390 px. En movil el request contract inicia
colapsado, no hay overflow horizontal y los controles bloqueados conservan su
estado.

## Flujo principal de consola 1.2

La marca `data-console-flow="contract-aware-1.2"` identifica el recorrido de
lectura de la consola: orientación IA_CORE y límite pre-runtime, readiness,
Contract Core / Payload, Internal Services / Signals, Actions & Boundaries,
Evidence / Checkpoint y siguiente paso documentado.

Los pasos usan marcas `data-flow-step` testeables y una ruta visual no
interactiva. La secuencia no agrega permisos, endpoints ni acciones: los
widgets conservan el payload inyectado como autoridad, `allowed_actions` sigue
siendo backend only y `forbidden_actions`/`blocked_capabilities` permanecen
visibles. El siguiente bloque se presenta como continuidad `planned`, no como
CTA operativo.

## Modelo de interacción 1.3

La shell agrega `data-console-interaction="contract-aware-1.3"` y declara
`data-interaction-mode="read-only"`. La ruta 1.2 permite enfocar cada zona de
forma local, sin inferir permisos ni persistir selección.

Contract Core incorpora un `<details>` read-only que replica valores ya
renderizados de schema, servicio, source, validation, flags, diagnósticos,
acciones y bloqueos. `console-interactions.js` sincroniza ese inspector desde
el DOM mediante `MutationObserver`; no usa fetch, no muta payloads y no activa
runtime/execution.

Los controles de relectura se marcan como inspección local, los botones de
request/dispatch conservan `disabled_by_contract` y las utilidades de gestión
preexistentes quedan fuera del modelo contract-aware 1.3. Los bloques críticos
de `forbidden_actions` y `blocked_capabilities` siguen visibles aunque el
inspector esté colapsado.

## Checkpoint de interaccion 1.4

`docs/UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md` cierra el bloque
1.0 -> 1.3 como auditoria documental y de pruebas. Confirma que la consola
principal, el refinamiento, el flujo y el modelo de interaccion read-only
siguen contract-aware, locales y no operativos.

El checkpoint preserva IA_CORE como identidad visual activa, bloquea legacy
visual como UI activa, mantiene visibles
`forbidden_actions` y `blocked_capabilities`, y confirma ausencia de endpoints,
runtime, execution, dispatch real y controlled execution.

## Plan de siguiente bloque 1.5

`docs/UI_UX_NEXT_CONSOLE_BLOCK_PLAN_1_5.md` define como siguiente bloque el
modelo de lectura de payload/contract. El plan no construye UI nueva: ordena
summary/detail/raw-safe para reducir permisos inferidos antes de crear paneles,
navegacion adicional o sistema de componentes.

21st.dev, UI UX Pro Max Skill y Framer Motion / Motion quedan registrados como
benchmarks futuros; no se instalan ahora, no se copian, no agregan
dependencias y no reemplazan IA_CORE.

## Modelo de lectura payload/contract 1.6

La consola agrega `data-payload-reading-model="contract-aware-1.6"` y separa
la lectura en `summary/detail/raw-safe`. Summary orienta al operador, detail
expone contrato tecnico legible y raw-safe muestra una proyeccion local
read-only del payload seguro disponible.

Raw-safe no edita, no envia, no ejecuta, no copia como accion operativa y no
activa modo de desarrollo. Si no hay fuente local segura muestra
`not_available` o `no_payload`. Este bloque no crea paneles 1.7, no runtime,
no execution y no dispatch.

## Paneles de detalle contract-aware 1.7

La shell agrega `data-contract-detail-panels="contract-aware-1.7"` y siete
paneles compactos read-only para readiness, payload/contract, validation,
actions, blocked capabilities, warnings/errors y evidence. Cada panel declara
su relacion con `summary/detail/raw-safe` y reutiliza lecturas ya renderizadas;
no crea una fuente paralela de autoridad.

Los paneles preservan empty states honestos, separan warnings de errors,
mantienen visibles `forbidden_actions` y `blocked_capabilities`, y no convierten
`allowed_actions` en permiso propio de UI. Este bloque no crea endpoints, no
runtime, no execution, no dispatch y no implementa navegacion interna. El
bloque 1.8 queda solamente como continuidad `planned`.

## Widgets backend contract

`backend-contract-widgets.js` no crea ni consulta endpoints. Renderiza payloads
estables ya normalizados por backend desde `window.IA_CORE_BACKEND_INTERNAL_UI_PAYLOADS`,
`window.iaCoreBackendInternalUIPayloads`, un script JSON con id
`backend-internal-ui-payloads`, o el evento
`ia-core-backend-internal-payloads-updated`.

Los widgets muestran `allowed_actions`, `forbidden_actions`,
`blocked_capabilities`, `warnings`, `errors`, `readiness` y flags
no-operativas. Si no hay payload estable, quedan en deny-by-default. Si el
payload viola `true = blocked`, flags false o status no operativo, se muestra
error contractual y no se renderizan acciones activas.

## Catálogo de textos

`i18n_es.json` es la fuente de referencia en español para toda pantalla o flujo
nuevo de la consola. Las incorporaciones deben reutilizar sus claves o ampliarlo antes
de agregar nuevos textos visibles; la migración de la superficie existente puede hacerse
de forma incremental sin duplicar un segundo catálogo.
