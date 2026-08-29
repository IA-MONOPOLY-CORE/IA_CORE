# UI/UX Panel Maestro Current Architecture Audit 1.120

## Commit base y objetivo

- Base esperada: `03975b9`.
- Restore point remoto vigente: `01d09ce`.
- Commits locales previos: `8843b60` y `03975b9`.
- Rama auditada: `main`, local ahead de `origin/main` por 2 commits.

1.120 audita la arquitectura actual real del Panel Maestro IA_CORE para que el futuro documento visual 1.121 se base en evidencia del repositorio y no en supuestos. El resultado describe archivos, zonas, bloques, componentes, comportamiento, datos, copy, densidad, deuda UX y fronteras contract-aware. No es una implementación.

## Estado recibido

- `PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT` recibido desde 1.119.
- `NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED` recibido desde 1.118.
- Restore point remoto vigente: `01d09ce`.
- Local ahead por 2 commits: `8843b60` y `03975b9`.
- Final Screen Contracts consolidado/publicado: Contract Overview, Blocked & Forbidden, Validation & Readiness y Request Contract Preview.
- Los elementos inferiores están bloqueados/publicados: elementos inferiores bloqueados, fuera de la baseline contractual de cuatro secciones.
- `+` y `DOMAIN` son deuda UX futura no bloqueante; no habilitan creación operativa.

## Alcance y método

La auditoría revisó como lectura los siete archivos UI declarados: `ui/web/index.html`, `ui/web/backend-contract-widgets.js`, `ui/web/admin-panels.js`, `ui/web/console-interactions.js`, `ui/web/domains.js`, `ui/web/styles.css` y `ui/web/i18n_es.json`. Se relevaron selectores, ids, atributos contract-aware, texto visible, listeners, handlers, formularios, loaders, fetches existentes, almacenamiento local y puntos de inicialización.

El snapshot observable de `index.html` contiene 16 `section`, 55 `article`, 4 `details`, 1 `form`, 41 `button`, 10 marcas `data-main-console-zone`, 7 `data-nav-section` y 64 marcas `data-component`. El CSS visual dominante está inline en `index.html`; `ui/web/styles.css` existe como stylesheet histórico, pero no aparece enlazado por el HTML actual.

La palabra “actual” se usa con una distinción necesaria:

- Presente en el markup o en el código no significa activo en la etapa actual.
- `LOWER_CONSOLE_READ_ONLY = true` bloquea la inicialización de las superficies administrativas y de dominio.
- Los handlers y fetches heredados siguen siendo deuda de frontera y riesgo futuro, aunque no se ejecuten por el camino actual.

## Inventario de archivos UI actuales

| Archivo | Propósito y responsabilidad | Relación con Panel Maestro / Final Screen Contracts | Elementos inferiores | HTML/estado/handlers/estilos/copy | Decisión futura | Riesgos |
| --- | --- | --- | --- | --- | --- | --- |
| `ui/web/index.html` | Shell principal; markup contractual, CSS inline y script inline de inicialización | Contiene header, baseline de cuatro FSC, lectura summary/detail/raw-safe, widgets, navegación y evidencia | Contiene `CFG`, `+`, `DOMAIN`, request draft, modales y gestión heredada | Contiene todo: HTML, estado local, handlers, estilos y copy hardcodeado | Preservar identidad y contratos; absorber estructura en zonas; separar gestión y modales; rediseñar densidad | Archivo monolítico, responsabilidades mezcladas y código operativo heredado detrás de guards |
| `ui/web/backend-contract-widgets.js` | Renderer de `backend_internal_ui_payload.v1`, estados, chips, validación negativa y proyección raw-safe | Alimenta Contract Core, widgets, detalle y summary; no crea contrato ni permiso | No pertenece a elementos inferiores | Estado derivado de payload inyectado, render DOM y listener de actualización; sin fetch | Preservar como adaptador de read model; reutilizar patrones en design system | Duplicación de lectura con summary/detail/widgets y riesgo de mostrar nombres técnicos con demasiado peso |
| `ui/web/admin-panels.js` | Paneles históricos de memoria, logs, hybrid, request contract y service map | No es parte de los cuatro FSC; sirve como superficie administrativa/técnica lateral | Vive en la configuración inferior heredada | Render, loaders, handlers y fetches GET definidos; initializer corta por read-only | Separar como Diagnostics/Read Models futuro o retirar de la superficie principal | IDs y copy como `orchestration`, `runtime`, `active` pueden parecer workflow operativo |
| `ui/web/console-interactions.js` | Foco, navegación interna, disclosures, sincronización de detalle e inspector | Organiza la lectura de Contract Core y zonas relacionadas sin cambiar autoridad | No ejecuta gestión inferior | Listeners locales, `scrollIntoView`, `MutationObserver`, aria y atributos de estado | Preservar como navegación local; extraer contrato de navegación visual futuro | Doble mapa de flujo/índice y riesgo de confundir foco con navegación de pantalla |
| `ui/web/domains.js` | Catálogo, selector, tema y creación de dominios; puente hacia agentes | No es FSC; `DOMAIN` y formulario pertenecen a gestión heredada | Superficie inferior; bloqueada por guard actual | Estado local, i18n, handlers y fetches GET/POST definidos; initializer retorna temprano | Separar como Domains Screen futura bajo contrato propio; no activar ahora | La presencia de POST, formulario y `DOMAIN` mantiene apariencia de capability |
| `ui/web/styles.css` | Stylesheet histórico con sidebar, tabs, agents, request draft, modales y utilidades | No gobierna el HTML actual observado; no es fuente canónica de FSC | Contiene estilos legacy de administración y draft | Solo estilos CSS; no link activo desde `index.html` | Aislar/documentar como legacy; verificar consumidores antes de retirar | Duplicación, reglas muertas y clases `.active`/`.status-dot.active` ambiguas |
| `ui/web/i18n_es.json` | Catálogo `es-AR` para common, status, flow, navegación, request, agentes, providers, memoria, logs, hybrid, overview, appearance y domains | Copy contractual disponible, pero gran parte del FSC está hardcodeada en HTML | Keys de gestión y dominio corresponden a superficie inferior | JSON de copy; se consume por `data-i18n` de dominio y por `domains.js` cuando se habilita | Separar copy contractual, administrativo y futuro; preservar compatibilidad de keys | Claves `debate.*`, `orchestration.*`, `execute` y mensajes técnicos pueden conservar semántica operativa heredada |

## Mapa de zonas actuales

| Zona | Ubicación aproximada / archivo | Propósito y tipo | Datos y acciones aparentes/reales | Estado contractual y no-runtime | Futuro | Prioridad / riesgo |
| --- | --- | --- | --- | --- | --- | --- |
| Header / identidad IA_CORE | `index.html:2289-2303` | Orientación, estado global y tipo documental | IA_CORE, límite pre-runtime, readiness, schema y source; no acción real | read-only/inspectable; no ejecución | Conservar como Master Header | P0; tres badges compiten por atención |
| Estado global | `index.html:2301-2303` | Indicadores/chips/labels de readiness, schema y conexión; bloque de indicadores/chips/labels | `no_payload`, `backend_internal_ui_payload.v1`, `not_available`; conexión queda `blocked_by_contract` | Estado declarado, no health operativo | Absorber en un único estado global jerarquizado | P0; “conexión” puede sugerir disponibilidad de backend |
| Índice de cuatro secciones | `index.html:2307-2318` | Resumen estático de Contract Overview, Blocked & Forbidden, Validation & Readiness y Request Contract Preview | IDs `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03`, `FSC-RCP-04` | read-only y static documentation | Conservar como índice contractual, sin quinta sección | P0; repetición con títulos posteriores |
| Contract Overview | `index.html:2321-2405` | Vista documental de identidad, readiness, source, acciones, bloqueos, evidencia y estados | `backend_internal_ui_payload.v1`, `allowed_actions`, `forbidden_actions`, `blocked_capabilities` | `FSC-CO-01`, documental, read-only, no-runtime/no-execution | Conservar como frontera contractual primaria | P0; nueve cards con repetición de metadata |
| Blocked & Forbidden | `index.html:2407-2486` | Límites duros, acciones prohibidas, no-unlock, source y evidencia | Blockers, forbidden, no bypass/override, estado documental | `FSC-BF-02`, siempre visible, documental/read-only | Conservar separado de dominios y agentes | P0; severidad roja repetida puede parecer alarma operativa |
| Strip de densidad | `index.html:2488-2491` | Explica P0/P1/P2 de la narrativa | Prioridad visible, lectura, detalle y trazabilidad | Documental; no control | Absorber en arquitectura visual futura, no necesariamente visible | P1; agrega meta-copy a una pantalla ya densa |
| Validation & Readiness | `index.html:2493-2604` | Explica readiness versus permiso, validation versus execution, findings, blockers y evidence | `readiness`, `validation`, warnings/errors, missing requirements | `FSC-VR-03`, documental/read-only, no-dispatch/no-endpoint | Conservar; ordenar una sola jerarquía de estado | P0; muchos badges y bloques de explicación |
| Request Contract Preview | `index.html:2606-2716` | Contrato diferido, draft, summary seguro y límites de submit/send/dispatch | `CFD-04`, `draft-not-final`, allowed/forbidden y evidence snapshot | `FSC-RCP-04`, `DEFER_FINALIZATION`, read-only, no contrato final | Conservar como superficie diferida; no convertir en ejecución | P0; “preview” y “request” mantienen affordance ambigua |
| Ruta narrativa / flow map | `index.html:2718-2732` | Índice de seis pasos de lectura | Readiness, Contract Core, Internal Signals, Actions & Limits, Evidence, Next Step | Local, focus-only, no workflow | Absorber o simplificar en navegación única | P1; duplica índice interno y puede parecer pipeline |
| Guidance de operador | `index.html:2735-2738` | Explicación de lectura, orden y límite | Copy sobre Panel Maestro y no Panel Usuario final | Documental, no action operativa | Absorber en ayudas contextuales breves | P1; compite con header y strip de densidad |
| Navegación interna / índice | `index.html:2740-2753` | Mueve foco entre zonas locales | Readiness, Contract Core, Payload Reading, Detail Panels, Actions & Boundaries, Evidence y Next Step | read-only, `aria-current`, no rutas/hash | Conservar como navegación local unificada | P1; existe además flow map con conceptos superpuestos |
| Readiness global | `index.html:2756-2780` | Primer bloque del modelo `01` | `no_payload`, schema, request draft, validation pending | read-only, pre-runtime | Absorber en Contract Status / Validation | P0; repite Contract Overview y headers |
| Contract Core / Payload | `index.html:2782-2948` | Rail de schema/source/flags, estados, summary/detail/raw-safe, panels e inspector | Payload inyectado, campos seguros, warnings/errors y blocked | read-only; raw-safe local y sin secrets | Conservar como read model y separar summary de detalle | P0; mayor densidad y repetición del sistema |
| `RELEER PAYLOAD LOCAL` | `index.html:2946`, widgets | Refresh del payload ya inyectado | Relee arrays locales/window/script y actualiza DOM/timestamp | `data-local-only`, `data-no-fetch`, no runtime/no execution | Conservar como acción de inspección, renombrar visualmente si hace falta | P1; palabra “releer” puede confundirse con fetch |
| Contract widgets | `index.html:2951-3002` + `backend-contract-widgets.js` | Cuatro widgets de status/actions/blocked/diagnostics | Estados, chips, safe projection y validación negativa | read-only; sin fetch propio | Absorber con Contract Core o reducir duplicación | P1; repetición con detail panels |
| Internal service signals | `index.html:3008-3018` | Señales técnicas internas | Provider, model, tools, integrations y policy declarados | read-only, datos técnicos, no ejecución | Separar en Diagnostics/Service Signals | P2; puede parecer service dashboard |
| Actions & boundaries | `index.html:3021-3041` | Visualiza autoridad backend, forbidden y blocked | `backend only`, `forbidden`, `blocked` | Documental/read-only, no bypass | Conservar cerca de Blocked & Forbidden | P0; requiere alto contraste sin CTA |
| Evidence checkpoint | `index.html:3043-3090` | Commits/checkpoints, siguiente paso y evidencia extendida | Trazabilidad documental, `passed`, `planned`, logs-sanitized | read-only, no live log | Conservar como evidencia secundaria | P1; “passed” debe seguir sin éxito operativo |
| `VER DETALLE` | `index.html:2925-2944` | Abre inspector local | Copia valores desde fuentes DOM con `data-inspector-source` | `<details>`, local/read-only | Conservar como disclosure secundaria | P1; repetición de detail panels |
| `VER EVIDENCIA` | `index.html:3065-3090` | Abre evidencia extendida | Texto de commits, logs-sanitized y checkpoints | `<details>`, no timeline operativo | Conservar como disclosure | P1; copy técnico largo |
| Elementos inferiores | `index.html:3096-3404` | Utilidades, request draft, config, admin y modales heredados | `CFG`, `+`, `DOMAIN`, formularios y acciones administrativas aparentes | Bloqueados por contrato durante init; no acción actual | Separar completamente del Contract Core | P0; frontera visual confusa |
| `CFG` | `index.html:3097` | Entrada a configuración heredada | Parece abrir config; actualmente disabled | `aria-disabled`, `data-contract-blocked`, no mutation | Separar en Configuration Read-only futura o eliminar del Panel | P1; etiqueta corta con semántica activa |
| `+` | `index.html:3098` | Entrada heredada de crear agente | disabled; no abre modal en etapa actual | contract-blocked/no-runtime/no-execution/no-mutation | Eliminar, contextualizar o mover a flujo futuro contractual | P1; affordance ambigua |
| `DOMAIN` | `index.html:3099`, `domains.js` | Entrada heredada de dominio | disabled; creación y catálogo no se ejecutan | contract-blocked; POST existente detrás de guard | Separar en Domains Screen futura | P1; duplicidad con `+` |
| Request draft lateral | `index.html:3107-3123` | Draft contractual visible con estado blocked | toggle local, status badge, synthesis; control principal disabled | no submit/no dispatch/no execution | Absorber en Request Contract Preview o dejar solo referencia | P0; `REQUEST CONTRACT PREVIEW` aparece dos veces |
| Footer | `index.html:3103` | Cierre de identidad HUD | `IA_CORE // Contract-Aware HUD` | Copy estático | Conservar o absorber en shell | P2; no agrega decisión operacional |
| Configuración modal | `index.html:3125-3245` | Sidebar de sources, service signals, read models, logs, request contract, theme, identity, widgets y display | Inputs, sliders, refresh buttons, file upload, apply/accept | Controles bloqueados por `admin-panels.js`/inline init salvo cierre; estado heredado | Separar por dominio de responsabilidad | P0; mezcla diagnóstico, identidad y mutación visual |
| Agent modal / tarjetas | `index.html:3094`, `3258-3360`, inline JS | Plantilla de cards, checklist y crear/editar agente | Actualmente grid muestra bloqueo; plantilla conserva editar/eliminar y campos | Buttons disabled; fetch/POST/PUT/DELETE quedan detrás de guard | Separar Agents Screen futura | P0; template code parece capability aunque no se renderiza activo |
| Domain modal | `index.html:3363-3404` | Formulario de área, nicho, nombre, instrucciones y tema | Un `form`, inputs, `CREAR DOMINIO` disabled | submit cancelado y `domains.js` retorna por read-only | Separar Domains Screen futura | P0; formulario visible en código y modal potencial |

## Mapa de bloques y componentes

Nombre de control documental: Mapa de bloques/componentes.

| Bloque / selector | Archivo y uso | Ligado a JS/CSS/i18n | Reutilización futura | Decisión / riesgo |
| --- | --- | --- | --- | --- |
| `.ia-core-shell`, `.layout-section`, `.hud-panel` | `index.html`; shell y paneles principales | CSS inline; estado por `data-*` | Sí, como contenedor visual contract-aware | Preservar, pero reducir anidamiento |
| `.main-console-header`, `.logo-area`, `.badges-container`, `.badge` | Header e identidad | CSS inline y localStorage de branding | Sí, Master Header | Mantener IA_CORE; evitar dashboard status ambiguo |
| `.four-screen-baseline-summary`, `.four-screen-baseline-list` | Índice de cuatro FSC | CSS inline; estático | Sí, índice contractual | Conservar sin agregar quinta sección |
| `.contract-overview-*` | Cards y status de FSC-CO-01 | CSS inline; DOM source sync | Sí, tokens/cards | Absorber repetición sin modificar contrato |
| `.blocked-forbidden-*` | Bloques críticos de FSC-BF-02 | CSS inline; badges | Sí, bloqueos y límites | Preservar severidad y no-unlock |
| `.validation-readiness-*` | Bloques de FSC-VR-03 | CSS inline; status | Sí, validation/readiness | Unificar jerarquía de estados |
| `.request-contract-preview-*` | Bloques de FSC-RCP-04 | CSS inline; copy static | Sí, draft diferido | Preservar `DEFER_FINALIZATION` |
| `.visual-state`, `.ia-status-badge`, `.ia-chip`, `.contract-chip` | Pills, chips, labels y badges | CSS inline; widgets JS | Sí, design tokens de estado | Reducir cantidad y diferenciar peso |
| `.density-critical`, `.density-primary`, `.density-secondary` | Escala visual de densidad | CSS inline | Sí, sistema de prioridad | Documentar tokens, no esconder blockers |
| `.console-flow-map`, `.flow-focus-control` | Ruta narrativa y foco | `console-interactions.js` + CSS inline | Parcial | Absorber con navegación única; no crear workflow |
| `.internal-console-nav`, `.internal-nav-control` | Índice de foco interno | `console-interactions.js` + CSS inline | Sí, navegación local | Conservar si no se duplica flow map |
| `.safe-disclosure`, `.contract-inspector`, `details/summary` | Accordions/disclosures seguros | `console-interactions.js` + CSS inline | Sí, disclosure read-only | Conservar; `+` del summary no es FAB de creación |
| `.payload-reading-model`, `.reading-layer` | Summary/detail/raw-safe | widgets + DOM source sync | Sí, read model | Preservar orden summary -> detail -> raw-safe |
| `.contract-detail-panels`, `.contract-detail-panel` | Detalle de readiness, payload, validation, actions, blockers, warnings y evidence | widgets/console interaction | Sí, con menos duplicación | Absorber por responsabilidad |
| `.data-widget`, `widget-contract-*` | Status/actions/blocked/diagnostics | `backend-contract-widgets.js` | Sí, como subcomponentes | Reusar sin convertir chips en controles |
| `.evidence-card`, `.evidence-disclosure` | Evidence y next step | estático + disclosure | Sí, zona secundaria | Mantener trazabilidad sin live log |
| `.request-draft-panel`, `.request-draft-control` | Draft lateral bloqueado | inline JS + CSS inline | Parcial | Absorber en FSC-RCP-04; no submit |
| `.floating-settings`, `.floating-add`, `.floating-domain` | FABs inferiores | inline JS + `domains.js` | No como acciones actuales | Eliminar o rediseñar bajo decisión futura |
| `.agents-grid`, `.agent-panel`, `.agent-header`, `.agent-output`, `.agent-footer-metrics` | Cards de agentes heredadas | inline JS + CSS inline | Sí, solo en Agents Screen futura | No activar; separar de contratos |
| `.config-sidebar`, `.config-sidebar-item`, `.config-section` | Tabs/sidebar de configuración | inline JS + admin-panels | Parcial | Separar read models, appearance y management |
| `.admin-card`, `.admin-grid`, `.admin-toolbar`, `.admin-pre`, `.admin-status` | Componentes técnicos de admin | `admin-panels.js` + CSS inline | Sí, Diagnostics futuro | Renombrar semántica para no sugerir runtime |
| `.modal`, `.config-modal`, `.domain-modal`, `#agent-modal`, `#response-modal` | Modales y formularios | inline JS, domains/admin | No en Panel Maestro actual | Separar/eliminar de shell contractual |
| `data-i18n`, `i18n_es.json` | Copy traducible, principalmente dominio | `domains.js`; carga bloqueada en etapa actual | Sí, con namespaces | Separar contract/admin/future y preservar keys |
| `ui/web/styles.css` legacy | Sidebar/tabs/agents/request draft/modals | No link activo encontrado | Solo como referencia histórica | Aislar; no borrar sin consumidores confirmados |

## Mapa de comportamiento actual

### Inicialización y listeners

Se relevaron `addEventListener`, `onclick`, `disabled`, `aria-disabled` y `forms` como parte del comportamiento actual.

- `index.html` registra `window.onload`, aplica `applyLowerConsoleBlockers()`, llama `cargarAgentes()`, inicializa `domainUI`, widgets, logo banner y listeners locales.
- `console-interactions.js` registra `addEventListener` para foco de flow, navegación interna, `toggle` de inspector, sincronización por `MutationObserver` y teclado del request disclosure.
- `backend-contract-widgets.js` registra refresh local de widgets y el evento `ia-core-backend-internal-ui-payloads-updated`; no contiene fetch.
- `admin-panels.js` define listeners para refresh/load de paneles, pero `initialize()` retorna antes de registrarlos si `LOWER_CONSOLE_READ_ONLY` es true.
- `domains.js` registra únicamente el submit guardado del formulario antes del return; no registra listeners de creación, catálogo o modal cuando la superficie está read-only.

### Flags de bloqueo y estados de lectura

- `disabled`, `aria-disabled` y `data-contract-blocked` están presentes en `CFG`, `+`, `DOMAIN`, save-agent, save-domain y controles de request.
- `data-no-runtime`, `data-no-execution`, `data-no-dispatch` y `data-no-mutation` se agregan por `markLowerConsoleControlBlocked()` y se usan en elementos inferiores.
- `data-no-fetch`, `data-local-only` identifican `RELEER PAYLOAD LOCAL`.
- Las cuatro FSC declaran `data-interaction-mode="read-only"`; las zonas inferiores se bloquean con estado de contrato.
- `aria-current`, `aria-pressed`, `data-nav-state` y `data-interaction-state` representan foco/selección local, no autoridad.

### Fetches y mutaciones heredadas

La auditoría encontró fetches estáticos en el código, pero no nuevos ni activos en el camino actual:

| Origen | Operaciones/endpoint observados | Estado actual |
| --- | --- | --- |
| `index.html` | Catálogos de roles/especializaciones, `/api/agents/list`, `/api/status`, `/api/agents/{id}`, creación/edición de agentes con `POST`/`PUT`, eliminación `DELETE` | Funciones de agentes y conexión retornan temprano con `LOWER_CONSOLE_READ_ONLY`; handlers operativos no se habilitan |
| `domains.js` | `/i18n_es.json`, `/api/catalogs/domain-creation`, `/api/domains/list`, `/api/domains/create` con `POST` | `fetchJson`, catálogo, listado y submit están bloqueados; `loadCatalog` no se alcanza porque initialize retorna |
| `admin-panels.js` | `/api/memory`, `/api/logs`, `/api/status?full=true`, `/api/status`, `/api/agents/list` | `fetchJson` lanza antes del fetch y `initialize` retorna por read-only |
| `backend-contract-widgets.js` | Payload desde arrays globales o script local | No fetch; renderiza localmente |
| `console-interactions.js` | Ningún endpoint/fetch | Solo navegación/foco/disclosure local |

No se encontraron `history.pushState`, `history.replaceState`, `location.hash`, `hashchange` ni asignaciones de navegación. `window.location.origin` solo construye bases de API en módulos heredados.

### Formularios, localStorage y estado local

- Existe un `#domain-form`; su submit se cancela y muestra copy de bloqueo.
- El modal de agente usa campos y botones, pero `save-agent-btn` queda disabled y `guardarAgente()` retorna por guard.
- `localStorage` conserva preferencias visuales y selección local: `ia_core_selected`, `ia_core_active_domain`, `ia_core_skin`, `ia_core_brand`, `brand_input`, `ia_core_wallpaper` e `ia_core_logos`.
- `agentes`, `selectedAgents`, estados de request draft, catálogos de perfiles y estado de dominio son memoria local JS.
- `setInterval(checkConnection, 5000)` solo se registra en la rama no-read-only; la rama actual marca conexión `blocked_by_contract`.
- `is-updating`, loaders y estados `pending` describen render/lectura o copy heredado; no deben interpretarse como ejecución.

## Mapa de datos, copy e i18n

Nombre de control documental: Mapa de datos/copy/i18n.

- `IA_CORE` es la identidad visible activa en title, header, footer y copy de consola.
- No se encontró `SAAOP` ni `Lotería/SAAOP` en los siete archivos UI auditados; esa identidad no aparece visible activa.
- El copy contractual está mayormente hardcodeado en `index.html`: `no_payload`, `ready-no-permission`, `blocked`, `forbidden`, `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint`, `no-user-panel`, `DEFER_FINALIZATION` y `read-only`.
- `backend-contract-widgets.js` conserva `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, warnings/errors y una proyección raw-safe sanitizada; no expone raw Package, payload crudo ni secrets.
- `i18n_es.json` está en `es-AR` y contiene copy de estados, navegación, request, agentes, providers, memoria, logs, hybrid, overview, appearance y domains.
- Solo se observaron marcas `data-i18n` en el modal de dominio. En el camino actual el catálogo no se carga porque `domains.js` retorna por read-only.
- El copy técnico mezcla español con labels en inglés: `Contract Core`, `Internal Signals`, `Actions & Limits`, `Request Contract`, `Service Map`, `Read models`, `allowed_actions` y `blocked_capabilities`.
- La ambigüedad principal es `+`/`DOMAIN`: dos affordances visuales cercanas que representan gestión futura bloqueada y no una operación actual.

## Mapa de densidad visual actual

La densidad es alta por acumulación vertical y repetición semántica, aunque el sistema declara una jerarquía P0/P1/P2.

- El header, baseline summary, cuatro FSC, flow map, guidance e índice interno repiten la orientación antes de llegar al read model.
- Contract Overview, Contract Core, widgets y detail panels repiten schema, source, readiness, actions, blockers y evidence.
- Hay muchos chips/pills/status badges para estados cercanos: `documented`, `ready-no-permission`, `blocked`, `forbidden`, `no-runtime`, `no-execution`, `pending`, `planned` y `no_payload`.
- `Blocked & Forbidden` y `Validation & Readiness` usan bloques critical siempre visibles, correctamente prioritarios pero visualmente intensos.
- `raw-safe`, inspector, `VER DETALLE` y `VER EVIDENCIA` agregan capas de lectura secundaria dentro de una página extensa.
- Las 55 cards/HTML articles favorecen escaneo por bloques, pero la repetición de headings técnicos debilita la jerarquía global.
- El request draft lateral queda cerca de la zona inferior y repite Request Contract Preview, aumentando la ambigüedad.
- El CSS inline tiene grids de 3/4/6/7 columnas y varios `@media` hasta una columna en mobile; el scroll total sigue siendo largo por la cantidad de secciones.
- Existen `overflow`, `max-height` y disclosures para raw-safe, modales y lectura técnica; deben probarse con contenido real en la arquitectura futura.
- Los botones bloqueados conservan clases visuales fuertes (`btn-primary`, colores de warning/error), por lo que la señal de bloqueo puede competir con el contenido documental.

## Mapa de deuda UX actual

| Deuda | Evidencia | Impacto | Tratamiento futuro |
| --- | --- | --- | --- |
| Duplicidad `+`/`DOMAIN` | FABs inferiores y `domains.js` | Intención de creación ambigua | Decidir eliminar, contextualizar o separar en Domains/Agents Screen |
| UI intermedia/de transición | Shell monolítico con FSC y gestión legacy | Difícil distinguir baseline, read models y administración | Separar zonas por responsabilidad en arquitectura 1.121 |
| Densidad técnica | Summary/detail/raw-safe/widgets/detail panels | Lectura lenta y repetida | Definir una jerarquía única y capas secundarias |
| Zonas inferiores heredadas | Config, admin, request draft y modales junto al core | Frontera contractual poco visible | Separar sin reactivar elementos inferiores |
| Nombres confusos | `debate`, `orchestration`, `runtime`, `active`, `Service Map` | Sugieren workflow o ejecución | Renombrar solo en tarea futura con migración documentada |
| Controles bloqueados visibles | `CFG`, `+`, `DOMAIN`, buttons `RELEER` administrativos | Ghost action potencial | Mantener bloqueo; redefinir affordance en arquitectura futura |
| Copy técnico mixto | Inglés estructural y español explicativo | Aumenta carga cognitiva | Crear namespaces y glosario visual |
| Mezcla dominio/agente/config/evidencia | Modal de configuración agrupa 11 áreas | Mezcla de ownership | Separar screens/zones sin tocar contratos |
| CSS legacy no enlazado | `ui/web/styles.css` no está linkeado en `index.html` | Duplicación y mantenimiento incierto | Verificar consumidores y aislar; no borrar en esta auditoría |
| Estado local no namespaced | `brand_input` y preferencias varias | Migración futura puede perder settings | Tratar como compatibilidad explícita, no limpiar ahora |

## Mapa de preservación contractual

- Final Screen Contracts no se toca: `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04` siguen siendo la baseline publicada.
- Los elementos inferiores no se tocan y permanecen bloqueados/read-only.
- `DEFER_FINALIZATION` se preserva; `CFD-04` continúa draft/not final y sin contrato final.
- No hay User Panel, rutas/hash ni navegación de pantalla nueva.
- No se agregan endpoints/fetches nuevos; los fetches heredados quedan documentados como riesgo y permanecen detrás de guards.
- No se activa runtime, execution, dispatch, workers, schedulers ni colas.
- No se exponen raw Package, payload crudo, secrets, tokens, credentials, headers ni auth.
- `passed`, `ready` y `readiness` no equivalen a éxito operativo ni permiso.
- No fake success: la ausencia de payload permanece `no_payload`/`not_available` y el bloqueo no se suaviza.
- No ghost actions: `allowed_actions` son datos declarados, no botones; los controles bloqueados no conceden permiso.

## Inventario de decisiones futuras

| Zona/bloque | Conservar | Absorber | Separar | Eliminar | Rediseñar | Motivo | Dependencia | Riesgo | Prioridad |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header IA_CORE | Sí | Estado global | No | No | Sí | Mantener identidad y orientación | Arquitectura visual | Parecer dashboard | P0 |
| Baseline de cuatro FSC | Sí | Índice contractual | No | No | Sí | Mantener trazabilidad y orden | Contratos publicados | Repetición | P0 |
| Contract Core/read model | Sí | Widgets y detail | raw-safe secundario | No | Sí | Reducir duplicación | Payload contract | Exceso técnico | P0 |
| Blocked & Forbidden | Sí | Límites compartidos | No | No | Sí | Mantener no-unlock | `FSC-BF-02` | Ocultar blockers | P0 |
| Validation & Readiness | Sí | Status global | No | No | Sí | Readiness no es permiso | `FSC-VR-03` | Verde como éxito | P0 |
| Request Contract Preview | Sí | Request draft lateral | Draft auxiliar | No | Sí | Preservar deferencia | `FSC-RCP-04`, `DEFER_FINALIZATION` | Preview como ejecución | P0 |
| Flow map + internal nav | Sí | En una navegación | No | Posible duplicado | Sí | Unificar foco local | `console-interactions.js` | Parecer workflow | P1 |
| Evidence/checkpoints | Sí | Evidence extendida | No | No | Sí | Mantener historia verificable | Restore points | Live log aparente | P1 |
| `CFG`/config modal | Copy segura | Widgets contract-aware | Appearance/admin/read models | No decidido | Sí | Separar responsabilidades | Arquitectura de screens | Mutación aparente | P1 |
| `+`/agent management | Guardrails | No | Agents Screen | Posible `+` | Sí | Quitar affordance ambigua | Contrato futuro | Reactivar POST/PUT/DELETE | P1 |
| `DOMAIN`/domain modal | Guardrails | No | Domains Screen | Posible FAB | Sí | Separar contexto de creación | Contrato de dominio | Reactivar POST | P1 |
| `styles.css` legacy | No borrar | No | Legacy stylesheet | No ahora | Aislar | Confirmar consumidores | Auditoría posterior | Romper referencias | P2 |
| `i18n_es.json` | Sí | Copy por namespaces | Contract/admin/future | No ahora | Renombrar gradualmente | Compatibilidad `data-i18n` | Copy inconsistente | P2 |

## Riesgos para rediseño futuro

- Perder trazabilidad al mover evidencia o separar las cuatro FSC.
- Rediseñar sin respetar contratos publicados.
- Confundir lectura con acción y `allowed_actions` con botones.
- Reactivar elementos inferiores o reabrir modales de gestión.
- Crear rutas/hash o un User Panel por una separación visual mal entendida.
- Crear endpoints/fetches nuevos o reusar los heredados sin guardrails.
- Introducir runtime/execution/dispatch en una pantalla documental.
- Mezclar Final Screen Contracts con dominios, agentes, configuración o evidencia.
- Resolver `+`/`DOMAIN` como parche aislado y conservar la ambigüedad.
- Ocultar bloqueos críticos dentro de disclosures o reducir su prioridad visual.
- Exponer payload crudo, raw Package o información sensible en una futura capa de detalle.
- Reintroducir identidad Lotería/SAAOP en copy o navegación.
- Romper el restore point `01d09ce` o perder la continuidad local `8843b60`/`03975b9`.
- Interpretar `pending`, `running`, `active`, `passed` o `planned` como operación cuando son datos heredados o estados documentales.
- Mantener dos fuentes visuales para la misma semántica: CSS inline y `styles.css` legacy.
- Aplicar el futuro design system a modales/admin antes de definir ownership de cada zona.

## Decisión final

`PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC`

## Justificación

La arquitectura actual queda suficientemente mapeada: existe un shell único con una baseline contractual clara, un read model contract-aware, navegación local, evidencia, elementos inferiores y superficies administrativas/legacy identificables. No se detecta acción operativa activa en el camino actual: `LOWER_CONSOLE_READ_ONLY` corta agentes, dominios y paneles admin; widgets e interacciones solo actualizan lectura local y foco. Los handlers y fetches heredados están documentados como riesgo, no como capabilities activas. No hay blocker que obligue a otra auditoría de zonas antes de documentar la arquitectura visual futura.

## Próximo prompt exacto

`PROMPT UI/UX 1.121 - Documentar arquitectura visual futura Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Límites preservados

Este documento es auditoría, no implementación.

Conclusión de etapa: no UI activa, no User Panel, no rutas/hash, no endpoints/fetches nuevos, no runtime, no execution, no dispatch, no raw Package, no payload crudo, no secrets, no fake success, no ghost actions, no pantalla, no quinta sección, no Final Screen Contracts, no elementos inferiores, no contrato funcional, no contrato final, no endpoint, no CI, no deuda residual, no pyflakes y no push.

- No se implementó pantalla.
- No se agregó quinta sección.
- No se modificó UI activa.
- No se modificó Final Screen Contracts.
- No se modificaron elementos inferiores.
- No se cambió contrato funcional.
- No se creó contrato final.
- No se contradijo `DEFER_FINALIZATION`.
- No se creó User Panel.
- No se crearon rutas/hash.
- No se crearon endpoints/fetches nuevos.
- No se activó runtime/execution/dispatch.
- No se tocó backend/runtime/endpoints/CI/dependencias.
- No se limpió deuda residual general.
- No se corrigieron pyflakes.
- No se hizo push.
- No se avanzó a 1.121.
