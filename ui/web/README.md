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

## Navegacion interna de consola 1.8

La shell agrega `data-internal-navigation="contract-aware-1.8"` y un indice interno
read-only para Readiness, Contract Core, Payload Reading, Detail
Panels, Actions & Boundaries, Evidence y Next Step. Los botones mueven foco y
scroll dentro de la misma consola; no crean rutas, hashes ni una app
multi-pantalla.

La navegacion reutiliza flow 1.2 e interaccion 1.3, apunta al modelo 1.6 y a los
paneles 1.7, y no modifica payloads, permisos ni bloqueos. No agrega endpoints,
no runtime, no execution y no dispatch. El bloque 1.9 queda `planned`; 1.8 no
implementa el sistema global de componentes.

## Sistema de componentes IA_CORE 1.9

La shell agrega `data-component-system="ia-core-contract-aware-1.9"` y un
vocabulario minimo para panels, detail panels, status badges, chips, empty
states, warnings, errors, blockers, evidence, nav buttons y controles
read-only. La implementacion conserva las clases existentes y suma marcas
canonicas; no reescribe el layout ni crea un paquete de componentes.

Los renderers dinamicos aplican las marcas segun estado contractual y mantienen
`allowed_actions`, `forbidden_actions` y `blocked_capabilities` como autoridad
backend. No hay dependencias nuevas, endpoints, runtime, execution ni dispatch.
21st.dev, UI UX Pro Max Skill y Framer Motion / Motion siguen como benchmarks futuros
solamente. 1.9 no cierra el checkpoint.

## Checkpoint segundo bloque de consola 1.10

`docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md` cierra el bloque
`1.6 -> 1.9` como checkpoint documental y de pruebas. Confirma que el modelo
summary/detail/raw-safe, los siete paneles de detalle, la navegacion interna y
el sistema minimo de componentes siguen coherentes, contract-aware, read-only y
sin permisos inferidos.

El checkpoint preserva IA_CORE como identidad visual activa, mantiene visibles
`forbidden_actions` y `blocked_capabilities`, no agrega dependencias, endpoints,
runtime, execution, dispatch ni controlled execution, y deja el veredicto
`UI_READY_FOR_NEXT_UI_UX_BLOCK`. El bloque 1.11 queda como continuidad de
planificacion; 1.10 no implementa el siguiente bloque.

## Planificacion siguiente bloque UI/UX 1.11

`docs/UI_UX_NEXT_BLOCK_PLAN_1_11.md` audita el estado post-1.10, compara las
opciones candidatas y selecciona `Responsive / Accessibility Hardening` como
siguiente bloque UI/UX. La decision prioriza reducir riesgo responsive,
accesibilidad, foco, teclado, contraste, legibilidad movil y densidad antes de
crear pantallas secundarias, polish premium, benchmarks externos o separacion
Panel Maestro vs Panel Usuario.

La planificacion deja el veredicto `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK` y
el proximo prompt exacto sugerido:
`PROMPT UI/UX 1.12 - Auditar responsive/accesibilidad de consola IA_CORE contract-aware sin runtime/no-execution`.
1.11 no implementa el bloque elegido, no crea endpoints, no agrega
dependencias, no activa runtime, no activa execution y conserva 21st.dev, UI UX
Pro Max Skill y Framer Motion / Motion como benchmarks futuros solamente.

## Auditoria responsive/accesibilidad 1.12

`docs/UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md` registra la auditoria de
viewports 1440 x 1000, 1280 x 800, 1024 x 768, 768 x 1024, 430 x 932,
390 x 844 y 360 x 740. Confirma la consola IA_CORE contract-aware, las marcas
1.6 -> 1.9, raw-safe read-only, `forbidden_actions` y
`blocked_capabilities` visibles, no endpoints, sin dependencias, runtime ni
execution.

La matriz P0/P1/P2/P3 deja hallazgos responsive/accesibilidad priorizados y no
implementa hardening en 1.12. Veredicto:
`UI_READY_FOR_RESPONSIVE_ACCESSIBILITY_HARDENING`. Proximo prompt exacto
sugerido: `PROMPT UI/UX 1.13 - Endurecer responsive, foco y lectura movil de
consola IA_CORE contract-aware sin runtime/no-execution`.

## Hardening responsive/accesibilidad 1.13

`docs/UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md` aplica hardening
quirurgico sobre el commit base `a7c03874`, consumiendo la auditoria 1.12 sin
redisenar la consola. La shell conserva marcas 1.6 -> 1.9 y agrega
`data-responsive-hardening="contract-aware-1.13"` como trazabilidad del
ajuste.

El hardening verifica 1440x1000, 1280x800, 1024x768, 768x1024, 430x932,
390x844 y 360x740; refuerza lectura movil, foco visible, areas tactiles,
raw-safe read-only, chips/badges, paneles y request draft colapsado. Mantiene
`forbidden_actions`, `blocked_capabilities`, warnings y errors visibles, no
endpoints, no runtime, no execution y sin dependencias. Proximo prompt exacto
sugerido: `PROMPT UI/UX 1.14 - Checkpoint responsive/accesibilidad IA_CORE
contract-aware sin runtime/no-execution`.

## Checkpoint responsive/accesibilidad 1.14

`docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md` cierra el bloque
1.11 -> 1.13 como checkpoint documental, visual y de pruebas. Confirma que la
consola mantiene IA_CORE, marcas 1.6 -> 1.9 y hardening 1.13 en viewports
1440x1000, 1280x800, 1024x768, 768x1024, 430x932, 390x844 y 360x740.

El checkpoint mantiene `forbidden_actions`, `blocked_capabilities`,
warnings/errors y raw-safe read-only visibles, no endpoints, no runtime, no
execution y sin dependencias. Veredicto:
`UI_READY_FOR_NEXT_UI_UX_BLOCK_PLANNING`. Proximo prompt exacto sugerido:
`PROMPT UI/UX 1.15 - Consolidar siguiente bloque UI/UX IA_CORE contract-aware
sin runtime/no-execution`.

## Planificacion siguiente bloque UI/UX 1.15

`docs/UI_UX_NEXT_BLOCK_PLAN_1_15.md` revisa el estado post-1.14 y selecciona
`Admin Boundary / Exposure Review` como siguiente bloque UI/UX. La decision
prioriza auditar limites entre consola visible, contratos internos, request
draft, controles bloqueados, acciones permitidas/prohibidas, blocked
capabilities, paneles administrativos y exposicion interna antes de abrir
pantallas secundarias, guidance, polish premium, benchmarks externos o
separacion Panel Maestro vs Panel Usuario.

La planificacion deja el veredicto `UI_READY_FOR_SELECTED_NEXT_UI_UX_BLOCK`.
1.15 no implementa el bloque elegido, no crea endpoints, no agrega
dependencias, no activa runtime, no activa execution y conserva 21st.dev, UI UX
Pro Max Skill y Framer Motion / Motion como benchmarks futuros solamente.
Proximo prompt exacto sugerido: `PROMPT UI/UX 1.16 - Auditar boundaries administrativos y exposicion interna de consola IA_CORE contract-aware sin runtime/no-execution`.

## Auditoria admin boundary/exposure 1.16

`docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_1_16.md` audita boundaries
administrativos y exposicion interna despues del plan 1.15. Revisa Contract
Reading, Request Draft, Actions, Blocked Capabilities, Internal Exposure,
Evidence, Navigation/Focus, Component, Responsive y Language/Microcopy sin
implementar hardening ni crear UI nueva.

La auditoria deja el veredicto `UI_READY_FOR_ADMIN_BOUNDARY_HARDENING` y
clasifica hallazgos P0/P1/P2/P3 para 1.17. Mantiene IA_CORE como identidad
activa, conserva `forbidden_actions` y `blocked_capabilities` visibles, no
activa runtime, no activa execution, no crea dispatch real, sin endpoints y
sin dependencias. Proximo prompt exacto sugerido: `PROMPT UI/UX 1.17 - Endurecer boundaries administrativos y exposicion interna de consola IA_CORE contract-aware sin runtime/no-execution`.

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
