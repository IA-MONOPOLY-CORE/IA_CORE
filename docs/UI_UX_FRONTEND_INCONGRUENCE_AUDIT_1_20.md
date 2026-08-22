
# UI/UX Frontend Incongruence Audit 1.20

Veredicto: `UI_UX_FRONTEND_INCONGRUENCE_AUDIT_COMPLETED`

## Alcance

Esta auditoria extrema inventaria incongruencias restantes del frontend hecho a mano de IA_CORE despues del plan `1.19`. No limpia, no endurece todavia, no redisenia la consola, no crea pantallas, no crea rutas, no crea endpoints, no instala dependencias, no activa runtime, no habilita execution, no activa dispatch real y no implementa controlled execution.

Commit base: `19e68c32`.

Relacion con plan 1.19: `docs/UI_UX_NEXT_BLOCK_PLAN_1_19.md` selecciono `Frontend Incongruence Audit` para mapear nombres heredados, clases ambiguas, microcopy vieja, patrones duplicados, estilos muertos y JS legacy no-operativo antes de avanzar a guidance, density, storytelling, polish o pantallas secundarias.

Veredictos esperados registrados:

- `FRONTEND_STRUCTURE_INVENTORY_COMPLETED`
- `FRONTEND_HTML_AUDITED`
- `FRONTEND_CSS_AUDITED`
- `FRONTEND_JAVASCRIPT_AUDITED`
- `FRONTEND_MICROCOPY_NAMING_AUDITED`
- `FRONTEND_FETCH_ROUTE_STORAGE_AUDITED`
- `FRONTEND_TEST_DOC_COVERAGE_AUDITED`
- `FRONTEND_LEGACY_PATTERNS_CLASSIFIED`
- `FRONTEND_RESIDUAL_INCONGRUENCES_PRIORITIZED`
- `FRONTEND_NO_RUNTIME_NO_EXECUTION_CONFIRMED`
- `UI_READY_FOR_FRONTEND_INCONGRUENCE_HARDENING`

## Fase 0 - Preflight Y Criterios

Preflight confirmado antes de editar:

- `git status --short` inicial: sin salida.
- `git rev-parse --short HEAD`: `19e68c32`.
- working tree limpio.

1.20 es auditoria, no limpieza. No se corrige hardening 1.21 en este prompt.

Archivos leidos o auditados:

- `docs/UI_UX_NEXT_BLOCK_PLAN_1_19.md`
- `docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_CHECKPOINT_1_18.md`
- `docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_HARDENING_1_17.md`
- `docs/UI_UX_ADMIN_BOUNDARY_EXPOSURE_AUDIT_1_16.md`
- `docs/UI_UX_NEXT_BLOCK_PLAN_1_15.md`
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_CHECKPOINT_1_14.md`
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_HARDENING_1_13.md`
- `docs/UI_UX_RESPONSIVE_ACCESSIBILITY_AUDIT_1_12.md`
- `docs/UI_UX_SECOND_CONSOLE_BLOCK_CHECKPOINT_1_10.md`
- `docs/UI_UX_COMPONENT_SYSTEM_1_9.md`
- `docs/UI_UX_INTERNAL_CONSOLE_NAVIGATION_1_8.md`
- `docs/UI_UX_CONTRACT_DETAIL_PANELS_1_7.md`
- `docs/UI_UX_PAYLOAD_CONTRACT_READING_MODEL_1_6.md`
- `docs/UI_UX_MAIN_CONSOLE_INTERACTION_CHECKPOINT_1_4.md`
- `ui/web/index.html`
- `ui/web/styles.css`
- `ui/web/backend-contract-widgets.js`
- `ui/web/admin-panels.js`
- `ui/web/console-interactions.js`
- `ui/web/domains.js`
- `ui/web/i18n_es.json`
- `ui/web/README.md`
- tests UI/UX `1.4 -> 1.19`
- `tests/test_api_admin_panels.py`
- `tests/test_backend_internal_future_ui_contract_plan_8_7.py`
- `tests/test_backend_internal_ui_payloads_7_6.py`

Criterios usados: `vivo_contract_aware`, `vivo_ambiguo`, `vivo_heredado`, `vivo_mal_nombrado`, `no_visible_referenciado`, `muerto_probable`, `duplicado`, `historico_test_fixture`, `falso_positivo`, `preservar`, `requiere_hardening_1_21` y `posponer`.

Prioridades: P0 bloqueante; P1 importante; P2 recomendable; P3 polish/deuda posterior.

## Fase 1 - Inventario De Archivos Frontend

| Archivo | Rol actual | Fuente activa | Riesgo | Auditoria profunda |
|---|---|---:|---|---:|
| `ui/web/index.html` | shell IA_CORE, CSS inline y JS legacy/admin | Si | alto por mezcla de contrato, admin, estilos y naming historico | Si |
| `ui/web/styles.css` | CSS historico no enlazado desde `index.html` observado | Dudoso | medio por duplicacion y posibles estilos muertos | Si |
| `ui/web/backend-contract-widgets.js` | renderer de `backend_internal_ui_payload.v1` | Si | bajo; constantes prohibidas defensivas | Si |
| `ui/web/admin-panels.js` | paneles admin de lectura/gestion preexistentes | Si | medio; fetches admin y naming `orchestration` | Si |
| `ui/web/console-interactions.js` | foco, navegacion, inspector y disclosure local | Si | bajo-medio; `block: 'start'` falso positivo | Si |
| `ui/web/domains.js` | gestion de dominios y catalogo i18n | Si | medio; POST preexistente fuera del modelo 1.6-1.9 | Si |
| `ui/web/i18n_es.json` | catalogo de microcopy ES | Referenciado | medio; claves `debate.execute`/`orchestration.execute` heredadas | Si |
| `ui/web/README.md` | documentacion viva de consola | Si | bajo; debe registrar 1.20 | Si |
| `docs/UI_UX_*` | cadena documental UI/UX | Documentacion | bajo; menciones historicas permitidas | Si |
| `tests/test_ui_ux*.py` | regresiones contract-aware | Tests | bajo-medio; legacy como fixtures negativos | Si |

Archivos historicos: `docs/legacy/loteria/README.md` es historico y no forma parte de `ui/web` activo. No se detecto `package.json`.

## Fase 2 - Auditoria HTML / Estructura Activa

| Elemento | Ubicacion aprox. | Evidencia | Clasificacion | Riesgo | Prioridad | Recomendacion 1.21 | No tocar |
|---|---:|---|---|---|---|---|---|
| Shell principal | `ui/web/index.html:1289` | `data-layout-contract-aware`, `data-main-console`, `data-payload-reading-model`, `data-contract-detail-panels`, `data-internal-navigation`, `data-component-system`, `data-responsive-hardening` | `vivo_contract_aware` | Bajo | P3 | Preservar | Marcas 1.6/1.7/1.8/1.9/1.13 |
| Header IA_CORE | `1295-1309` | `IA_CORE`, `READINESS: no_payload`, `SCHEMA: backend_internal_ui_payload.v1` | `vivo_contract_aware` | Bajo | P3 | Preservar | Identidad IA_CORE |
| Flow controls | `1320-1325` | `data-focus-step`, `data-interaction-mode="read-only"` | `vivo_contract_aware` | Bajo | P3 | Preservar | No rutas |
| Nav interna | `1335-1341` | siete `data-nav-target`, `aria-current`, `ia-nav-button` | `vivo_contract_aware` | Bajo | P3 | Preservar | No hash routing |
| Summary/detail/raw-safe | `1391-1406` | `data-reading-layer`, `contract-raw-safe-value` | `vivo_contract_aware` | Bajo | P3 | Preservar | Raw-safe read-only |
| Detail panels | `1409-1483` | siete `data-detail-panel` | `vivo_contract_aware` | Bajo | P3 | Preservar | Paneles 1.7 |
| Inspector | `1502` | `contract-read-only-inspector`, `ia-readonly-control` | `vivo_contract_aware` | Bajo | P3 | Preservar | Inspector local |
| Widgets | `1523-1566` | `widgets-refresh-btn`, `data-widget` | `vivo_contract_aware` | Bajo | P3 | Preservar | Relectura local |
| Internal signals | `1585-1592` | `internal_dispatcher_no_runtime` | `vivo_contract_aware` | Bajo | P3 | Preservar | Texto no-runtime |
| Actions & Boundaries | `1598-1613` | `forbidden`, `blocked` | `vivo_contract_aware` | Bajo | P3 | Preservar | Forbidden/blocked visibles |
| Evidence / Next Step | `1620-1639` | `passed`, `planned` | `vivo_contract_aware` | Bajo | P3 | Preservar | Evidencia, no CTA |
| Request draft panel | `1676-1686` | `id="debate-panel"`, `debate-input`, `debate-metrics`, `debate-synthesis` | `vivo_heredado` | Nombre `debate` puede parecer feature historica | P1 | Renombrar a `request-draft-*` o documentar alias legacy | No habilitar draft |
| Request blocked control | `1680` | `id="request-draft-blocked-control" disabled` | `vivo_contract_aware` | Clase `btn-debate` alrededor | P2 | Mantener id; renombrar clase si se toca | No habilitar |
| Config tabs | `1697-1710` | `config-sidebar-item active`, `config-section active` | `vivo_ambiguo` | `.active` visual legacy | P2 | Renombrar `is-selected`/`is-visible` | No alterar admin tabs |
| Logs admin | `1740` | `id="logs-runtime"` | `vivo_mal_nombrado` | `runtime` en logs sanitizados | P1 | Renombrar `logs-sanitized` | No cambiar `/api/logs` |
| Request contract admin | `1753-1763` | `orchestration-task`, `orchestration-status`, `orchestration-scores`, `orchestration-steps`, `orchestration-agents` | `vivo_heredado` | Sugiere workflow operativo | P1 | Renombrar a `request-contract-*` | No crear dispatch |
| Role option | `1862` | `<option value="orchestrator">Orquestador</option>` | `falso_positivo` | Rol/catalogo, no runtime | P3 | Posponer/documentar | No cambiar catalogo |
| Domain submit | `1969` | `type="submit"` en `domain-form` | `vivo_ambiguo` | Gestion preexistente fuera del modelo contract-aware | P2 | Documentar frontera admin/domains | No tocar backend |

No se detectaron `SAAOP`, `Loteria`, `Lotería`, `lottery`, `Tactical HUD`, `U-Score`, `CAZADOR`, `ESPEJO` ni `combinatoria` en `ui/web`.
## Fase 3 - Auditoria CSS / Estilos

CSS inline en `index.html` es la fuente visual dominante. `ui/web/styles.css` conserva estilos historicos similares y no aparece enlazado desde `index.html`; se clasifica como `no_visible_referenciado` o `muerto_probable` hasta verificar consumidores.

| Clase | Archivo | Ubicacion aprox. | Uso aparente | Estado | Riesgo | Prioridad | Recomendacion |
|---|---|---:|---|---|---|---|---|
| `.nav-item.active` | `ui/web/styles.css` | `132` | sidebar historica | `muerto_probable` | Patron `active` fuera de sistema 1.9 | P2 | Verificar referencia; retirar o documentar |
| `.tab-content.active` | `ui/web/styles.css` | `180` | tabs historicas | `muerto_probable` | Duplicado con config inline | P2 | Verificar uso; preferir `is-visible` |
| `.status-dot.active` | `ui/web/styles.css` | `278` | estado verde activo | `vivo_ambiguo` si se usa | Estado operativo aparente | P1 | Reemplazar por `ready/read_only` si esta vivo |
| `.skin-card.active` | `ui/web/styles.css` | `366` | skin seleccionada | `muerto_probable` | `active` visual no contractual | P3 | Posponer o documentar |
| `.debate-panel` | `styles.css:512`, `index.html:1098` | panel draft | `duplicado` | Doble definicion inline/external | P2 | Declarar fuente canonica |
| `.btn-debate` | `styles.css:559`, `index.html:1150` | boton bloqueado | `vivo_heredado` | CTA de debate aparente | P1 | Renombrar clase visual |
| `.debate-metrics` | `styles.css:582`, `index.html:1157` | metricas ocultas | `vivo_heredado` | Resultado operativo futuro aparente | P2 | Retirar si muerto o renombrar |
| `.config-sidebar-item.active` | `index.html:1175` | tab seleccionada | `vivo_ambiguo` | `.active` legacy | P2 | Renombrar `is-selected` |
| `.config-section.active` | `index.html:1178` | seccion visible | `vivo_ambiguo` | `.active` legacy | P2 | Renombrar `is-visible` |
| `.skin-option.active` | `index.html:1225` | skin seleccionada | `vivo_ambiguo` | Estado visual no contractual | P3 | Documentar o renombrar |

No hay contradiccion P0 con sistema 1.9; el problema es vocabulario doble (`hud-panel`, `debate-*`, `.active`) junto a `ia-*`.

## Fase 4 - Auditoria JavaScript / Comportamiento Local

### `backend-contract-widgets.js`

| Funcion/constante | Ubicacion aprox. | Rol | Invocacion | Fetch/storage | Clasificacion | Riesgo | Recomendacion |
|---|---:|---|---|---|---|---|---|
| `REQUIRED_FALSE_FLAGS` | `8-15` | flags no-operativas | validation | No | `preservar` | Bajo | Preservar |
| `PROHIBITED_ACTIVE_STATUSES` | `16-23` | bloquea `active/running/live/operational/executing` | `validateStablePayload` | No | `falso_positivo` | Bajo | Preservar |
| `PROHIBITED_ALLOWED_ACTIONS` | `24-33` | bloquea acciones prohibidas | `validateStablePayload` | No | `falso_positivo` | Bajo | Preservar |
| `renderChips` | `123` | render local sanitizado | widgets | No | `vivo_contract_aware` | Bajo | Preservar |
| `safeRawProjection` | `141` | whitelist raw-safe | `setRawSafe` | No | `vivo_contract_aware` | Bajo | Preservar |
| `validateStablePayload` | `244` | valida contrato | `renderPayload` | No | `vivo_contract_aware` | Bajo | Preservar |
| `renderNoPayload` | `280` | deny-by-default | refresh | No | `vivo_contract_aware` | Bajo | Preservar |
| `renderContractError` | `319` | error contractual | validation | No | `vivo_contract_aware` | Bajo | Preservar |
| `renderPayload` | `356` | render payload estable | refresh/update | No | `vivo_contract_aware` | Bajo | Preservar |
| `refresh/update/init` | `416-437` | relectura local/eventos | onload/event | No | `vivo_contract_aware` | Bajo | Preservar |

No contiene `fetch(`, `localStorage` ni `sessionStorage`. Las palabras `active`, `running`, `live`, `execute` y `runtime` son falsos positivos defensivos.

### `admin-panels.js`

| Funcion | Ubicacion aprox. | Rol | Se invoca desde | Fetch/storage | Clasificacion | Riesgo | Recomendacion |
|---|---:|---|---|---|---|---|---|
| `fetchJson` | `16` | wrapper admin | loaders | Fetch | `vivo_ambiguo` | P2 | Documentar endpoints permitidos/preexistentes |
| `loadMemory` | `42` | lee `/api/memory` | refresh/tab | GET | `vivo_ambiguo` | P2 | Preservar como admin read |
| `loadLogs` | `89` | lee `/api/logs` | refresh/tab | GET | `vivo_mal_nombrado` por `logs-runtime` | P1 | Renombrar ids `logs-runtime` |
| `loadHybrid` | `110` | lee `/api/status?full=true` | refresh/tab | GET | `vivo_ambiguo` | P2 | Documentar `active_provider/model` |
| `loadOrchestrationAgents` | `134` | lista sources declaradas | tab request | GET `/api/agents/list` | `vivo_heredado` | P1 | Renombrar `loadRequestContractSources` |
| `inspectRequestContractBoundary` | `154` | inspeccion local bloqueada | click disabled/read-only | No | `vivo_contract_aware` con ids heredados | P1 | Mantener comportamiento; renombrar ids |
| `loadOverview` | `160` | lee `/api/status` | refresh/tab | GET | `vivo_ambiguo` | P2 | Preservar |
| `initialize` | `189` | bind listeners | load | No directo | `vivo_contract_aware` | Bajo | Preservar |

No usa `/api/debate/start`, `/api/dispatch`, `/api/runtime` ni `/api/execution`.

### `console-interactions.js`

| Funcion | Ubicacion aprox. | Rol | Se invoca desde | Fetch/storage | Clasificacion | Riesgo | Recomendacion |
|---|---:|---|---|---|---|---|---|
| `stateTokens`, `setState` | `17-27` | estado local `data-interaction-state` | helpers | No | `vivo_contract_aware` | Bajo | Preservar |
| `markNavigationCurrent` | `41` | `aria-current` local | navigation | No | `vivo_contract_aware` | Bajo | Preservar |
| `selectFlowStep` | `52` | foco/scroll local | click | No | `vivo_contract_aware` | Bajo; `block: 'start'` falso positivo | Documentar |
| `selectNavigationTarget` | `75` | foco/scroll local | click | No | `vivo_contract_aware` | Bajo; `block: 'start'` falso positivo | Documentar |
| `syncInspector` | `109` | replica texto DOM | observer/toggle | No | `vivo_contract_aware` | Bajo | Preservar |
| `bindRequestDisclosure` | `159` | disclosure `debate-panel` | init | No | `vivo_heredado` por ids | P2 | Renombrar al completar ids |
| `init` | `182` | bind local | DOMContentLoaded | No | `vivo_contract_aware` | Bajo | Preservar |

No contiene fetch, storage, router, hash routing ni mutacion de payload.

### JS inline de `index.html`

| Funcion/estado | Ubicacion aprox. | Rol | Fetch/storage | Clasificacion | Riesgo | Recomendacion |
|---|---:|---|---|---|---|---|
| `fetchJson` | `2129` | wrapper admin/catalogos | Fetch | `vivo_ambiguo` | P2 | Documentar frontera admin/catalog |
| `buildLegacyProfileCatalog` | `2151` | fallback catalogo agente | No | `vivo_heredado` | P2 | Renombrar o documentar `legacy` tecnico |
| `consultarPresetAgente` | `2315` | match preset dominio | GET | `vivo_ambiguo` | P2 | Mantener fuera de permissions |
| `consultarModelRecommendation` | `2341` | recomendacion modelo | POST | `vivo_ambiguo` | P2 | Documentar no-runtime |
| `consultarModelCompatibility` | `2442` | compatibilidad modelo | POST | `vivo_ambiguo` | P2 | Documentar |
| `activeAgentProfileCatalog` | `2110`, `2539-2628` | catalogo activo local | No | `vivo_mal_nombrado` | P2 | Renombrar `currentAgentProfileCatalog` |
| `cargarAgentes` | `2637` | lista agentes | GET | `vivo_ambiguo` | P2 | Separar de dispatch |
| `eliminarAgente` | `2838` | gestion agent | DELETE | `vivo_ambiguo` | P2 | Documentar admin management |
| `guardarAgente` | `2907` | crear/editar agente | POST/PUT | `vivo_ambiguo` | P2 | No tocar backend |
| `initLogoBanner` | `2996` | logos locales | localStorage | `vivo_ambiguo` | P3 | Posponer |
| `aplicarConfiguracion` | `3053` | skins/brand/opacity/font | localStorage | `vivo_ambiguo` | P2 | Renombrar `.active` |
| `inspectRequestDraftBoundary` | `3075` | bloqueo local | No | `vivo_contract_aware` | Bajo | Preservar |
| `checkConnection` | `3094` | lectura status | GET | `vivo_ambiguo` | P2 | Mantener `lectura_disponible` |
| `window.onload` | `3108` | binds | varios | `vivo_ambiguo` | P2 | No refactor amplio |

## Fase 5 - Auditoria Microcopy / Lenguaje Visible

| Termino | Archivo | Ubicacion | Contexto | Visible | Estado | Riesgo | Prioridad | Recomendacion |
|---|---|---:|---|---:|---|---|---|---|
| `debate` | `index.html`, `styles.css`, `admin-panels.js`, `console-interactions.js`, `i18n_es.json` | varias | ids/clases/catalogo para request draft | Parcial | `vivo_heredado` | Feature historica | P1 | Renombrar o aislar |
| `orchestration` | `index.html`, `admin-panels.js`, `i18n_es.json` | `1753-1763`, `134-156`, `188-211` | request contract/admin/historial | Parcial | `vivo_heredado` | Workflow aparente | P1 | Renombrar a request contract |
| `runtime` | `index.html`, `README`, `i18n_es.json`, `backend-contract-widgets.js` | varias | negativo no-runtime o logs sanitizados | Si | mixto | `logs-runtime` ambiguo | P1/P3 | Renombrar id de logs; preservar copy negativo |
| `execute/executing` | `i18n_es.json:101-107`, `188-194` | valores bloqueados | No siempre | `vivo_heredado` | Claves viejas | P2 | Renombrar claves si se toca i18n |
| `dispatch` | `index.html`, `README`, `admin-panels.js`, `i18n_es.json` | varias | copy negativo/blocked | Si | `vivo_contract_aware` | Bajo si negativo | P3 | Preservar copy negativo |
| `start` | `console-interactions.js:70,93`, i18n `start_error` | scroll option / error key | No/indirecto | `falso_positivo` y `vivo_heredado` | Bajo | P3 | Documentar; no tocar scroll option |
| `active` | `.active`, `activeAgentProfileCatalog`, `active_provider` | varias | visual selected / backend data | Si/No | `vivo_ambiguo` | Estado operativo aparente | P2 | Renombrar visual/catalog locals |
| `processing` | `index.html:175`, tests historicos | CSS pulse-dot | No principal | `vivo_ambiguo` | Estado no permitido por 1.9 | P2 | Verificar uso |
| `materialize/lifecycle` | docs/tests | historico negativo | No UI activa | `historico_test_fixture` | Bajo | P3 | Preservar como regresion negativa |

## Fase 6 - Inventario Naming / Identificadores

Busquedas explicitas realizadas: `active`, `.active`, `is-active`, `start`, `start-btn`, `run`, `execute`, `dispatch`, `launch`, `operate`, `live`, `orchestration`, `orchestrator`, `runOrchestration`, `debate`, `runtime`, `logs-runtime`, `saaop`, `loteria`, `lotería`, `lottery`, `tactical`, `u-score`, `cazador`, `espejo`, `combinatoria`, `materialize`, `lifecycle`, `submit`, `send`, `process`, `processing`.

Resumen: `start-btn`, `runOrchestration`, `orchestration-run-btn` y `startDebate` no aparecen como controles/handlers activos; sobreviven en docs/tests historicos. `.active` vive en config/skin/sidebar CSS. `is-active`, `launch` y `operate` no aparecen como UI activa. `/api/debate/start` y `/api/dispatch` no aparecen en frontend activo. `saaop`, `loteria`, `lotería`, `lottery`, `tactical`, `u-score`, `cazador`, `espejo` y `combinatoria` no aparecen en `ui/web`.

## Fase 7 - Inventario Fetches / Rutas / Endpoints

| Archivo | Ubicacion aprox. | Endpoint/ruta | Metodo | Estado | Riesgo | Recomendacion |
|---|---:|---|---|---|---|---|
| `ui/web/index.html` | `2168-2169` | `/api/catalogs/roles`, `/api/catalogs/specializations` | GET | preexistente catalogo | P2 | Documentar |
| `ui/web/index.html` | `2327` | `/api/domains/{id}/agent-presets/match` | GET | preexistente dominio | P2 | Documentar |
| `ui/web/index.html` | `2359` | `/api/agents/model-recommendation` | POST | preexistente admin | P2 | Documentar no-runtime |
| `ui/web/index.html` | `2456` | `/api/system/model-compatibility` | POST | preexistente admin | P2 | Documentar no-runtime |
| `ui/web/index.html` | `2614` | `/api/domains/{id}/profile-catalog` | GET | preexistente dominio | P2 | Documentar |
| `ui/web/index.html` | `2639` | `/api/agents/list` | GET | preexistente admin | P2 | Preservar |
| `ui/web/index.html` | `2776`, `3096` | `/api/status` | GET | lectura status | P2 | Preservar |
| `ui/web/index.html` | `2841` | `/api/agents/{id}` | DELETE | management admin | P2 | No mezclar con request contract |
| `ui/web/index.html` | `2924-2962` | `/api/agents/create`, `/api/agents/{id}` | POST/PUT | management admin | P2 | No tocar backend |
| `ui/web/admin-panels.js` | `47` | `/api/memory` | GET | lectura admin | P2 | Documentar |
| `ui/web/admin-panels.js` | `93` | `/api/logs` | GET | lectura admin | P1 por `logs-runtime` id | Renombrar id |
| `ui/web/admin-panels.js` | `113`, `162` | `/api/status?full=true`, `/api/status` | GET | lectura admin | P2 | Preservar |
| `ui/web/admin-panels.js` | `138` | `/api/agents/list` | GET | sources declaradas | P1 por naming `orchestration` | Renombrar wrapper |
| `ui/web/domains.js` | `37` | `/i18n_es.json` | GET | catalogo texto | P3 | Preservar |
| `ui/web/domains.js` | `56`, `233`, `286` | `/api/catalogs/domain-creation`, `/api/domains/list`, `/api/domains/create` | GET/POST | dominio admin | P2 | Documentar |

Confirmado: no `/api/debate/start`; no `/api/dispatch`; no endpoint nuevo; no router nuevo; no `location.hash`, `hashchange`, `history.pushState` ni `history.replaceState`; no hash routing operativo; no materialize/lifecycle activo desde UI; `backend-contract-widgets.js` y `console-interactions.js` siguen sin fetch.

La auditoria no recomienda endpoints, no recomienda dependencias nuevas y no recomienda runtime/execution.

## Fase 8 - Inventario Storage / Estado Local

| Key | Archivo | Ubicacion aprox. | Uso | Estado | Riesgo | Recomendacion |
|---|---|---:|---|---|---|---|
| `ia_core_selected` | `index.html` | `2661`, `2845`, `3058` | seleccion visual de agentes listados | `vivo_ambiguo` | Puede confundirse con seleccion operativa | P2 | Documentar o renombrar `ia_core_visible_sources` |
| `ia_core_logos` | `index.html` | `2998-3048` | logos/banner local | `vivo_ambiguo` | Personalizacion visual local | P3 | Posponer |
| `ia_core_skin` | `index.html` | `3061`, `3126-3134` | skin visual | `vivo_ambiguo` | Usa `.active` | P2 | Renombrar estado visual |
| `ia_core_brand` | `index.html` | `3064`, `3138` | nombre visual | `vivo_ambiguo` | Puede cambiar identidad visible | P2 | Revisar limite IA_CORE active |
| `brand_input` | `index.html` | `3140`, `3162` | input historico sin prefijo IA_CORE | `vivo_mal_nombrado` | Key no namespaced | P2 | Migrar a `ia_core_brand_input` |
| `ia_core_wallpaper` | `index.html` | `3173`, `3179` | fondo local | `vivo_ambiguo` | Visual, no operativo | P3 | Posponer |
| `ia_core_active_domain` | `domains.js` | `186`, `216`, `299` | dominio UI activo | `vivo_ambiguo` | `active` puede sugerir dominio operativo | P2 | Documentar como dominio seleccionado |

No se detecto `sessionStorage`. No se detectaron keys `saaop_*`.
## Fase 9 - Inventario Tests / Cobertura

Protegen identidad IA_CORE y ausencia de legacy visual activo: tests 1.4, 1.6, 1.10, 1.12, 1.14, 1.15, 1.18 y 1.19.

Protegen no-runtime/no-execution/no-dispatch: tests 1.6, 1.7, 1.8, 1.9, 1.10, 1.13, 1.17, 1.18, `tests/test_backend_internal_future_ui_contract_plan_8_7.py` y `tests/test_backend_internal_ui_payloads_7_6.py`.

Tests con naming heredado permitido: 1.12/1.13/1.14 mencionan `start-btn` como historia responsive; 1.16/1.17/1.18 mencionan `start-btn`, `runOrchestration` u `orchestration-run-btn` como regresion negativa; 1.19 menciona `debate`, `orchestration`, `.active` y `logs-runtime` como deudas registradas.

Gaps: no hay test que obligue a renombrar `logs-runtime`; no hay test que obligue a reemplazar `.active`; no hay test que inventarie `domains.js`; no hay test que proteja migracion de `brand_input` o `ia_core_active_domain`.

## Fase 10 - Inventario Docs / README

Coherencia: 1.4 cerro interaccion local read-only; 1.10 cerro summary/detail/raw-safe, paneles, navegacion y componentes; 1.14 cerro responsive/accesibilidad; 1.18 cerro admin boundaries; 1.19 selecciono `Frontend Incongruence Audit`.

Contradicciones: no hay contradiccion P0. Menciones de SAAOP/Loteria, Tactical HUD, `start-btn` y `runOrchestration` en docs/tests son historicas o regresiones negativas permitidas. `ui/web/README.md` no registraba 1.20 antes de este prompt.

Deudas documentadas: `.active`, `debate`, `orchestration`, `logs-runtime`, fetches administrativos preexistentes, densidad y estilos duplicados. Deudas no suficientemente documentadas hasta 1.20: `domains.js`, `i18n_es.json`, keys localStorage no namespaced (`brand_input`) y posible estado muerto de `styles.css`.

## Fase 11 - Mapa Frontend Vivo / Legacy / Muerto

| Item | Tipo | Archivo | Ubicacion aprox. | Estado | Evidencia | Riesgo | Prioridad | Recomendacion 1.21 | Preservar/no tocar |
|---|---|---|---:|---|---|---|---|---|---|
| Shell IA_CORE | HTML | `index.html` | `1289` | `vivo_contract_aware` | `data-...1.6/1.7/1.8/1.9/1.13` | Bajo | P3 | Preservar | No tocar marcas |
| Request draft `debate-*` | HTML/CSS/JS | `index.html`, `styles.css`, `console-interactions.js` | `1098`, `1676`, `3151` | `vivo_heredado` | `debate-panel`, `debate-toggle` | Confusion feature | P1 | Renombrar request draft | No habilitar control |
| `btn-debate` | CSS/HTML | `index.html`, `styles.css` | `1150`, `559` | `vivo_heredado` | boton bloqueado con clase debate | CTA aparente | P1 | Renombrar clase | No cambiar disabled |
| `orchestration-*` admin | HTML/JS/i18n | `index.html`, `admin-panels.js` | `1755`, `134` | `vivo_heredado` | ids y loader | Workflow aparente | P1 | Renombrar request contract | No crear dispatch |
| `logs-runtime` | HTML/JS | `index.html`, `admin-panels.js` | `1740`, `91` | `vivo_mal_nombrado` | logs sanitizados | Runtime aparente | P1 | Renombrar `logs-sanitized` | No tocar `/api/logs` |
| `.active` config/skin | CSS/JS | `index.html` | `1175`, `1225`, `3060`, `3184` | `vivo_ambiguo` | classList active | Estado operativo aparente | P2 | Renombrar `is-selected/is-visible` | No tocar readiness |
| `.active` styles.css | CSS | `styles.css` | `132`, `180`, `278`, `366` | `muerto_probable`/`duplicado` | reglas no enlazadas | Deuda visual | P2 | Verificar referencia | No borrar sin verificar |
| `activeAgentProfileCatalog` | JS | `index.html` | `2110` | `vivo_mal_nombrado` | variable local | Activo operativo aparente | P2 | `currentAgentProfileCatalog` | No cambiar catalogo |
| `status.running` | JS | `admin-panels.js` | `50`, `165` | `falso_positivo` | dato backend status | Bajo | P3 | Documentar | No cambiar contrato backend |
| `active_provider/model` | JS | `admin-panels.js` | `118-119` | `falso_positivo` | fields backend | Bajo | P3 | Documentar | No cambiar payload |
| `PROHIBITED_ACTIVE_STATUSES` | JS | `backend-contract-widgets.js` | `16` | `falso_positivo` | lista defensiva | Bajo | P3 | Preservar | No tocar |
| `block: 'start'` | JS | `console-interactions.js` | `70`, `93` | `falso_positivo` | scrollIntoView option | Bajo | P3 | Documentar | No tocar |
| `styles.css` completo | CSS | `styles.css` | todo | `muerto_probable` | no enlazado por index | Deuda tecnica | P2 | Verificar consumidores | No borrar en 1.20 |
| i18n `debate.execute` | JSON | `i18n_es.json` | `98-107` | `no_visible_referenciado` | valor bloqueado | Clave heredada | P2 | Renombrar claves si hay migracion | No romper data-i18n |
| domain form POST | JS/HTML | `domains.js`, `index.html` | `286`, `1969` | `vivo_ambiguo` | submit dominio | Admin management | P2 | Documentar frontera | No tocar backend |

## Fase 12 - Matriz P0/P1/P2/P3

| ID | Prioridad | Archivo | Descripcion | Evidencia | Riesgo | Recomendacion 1.21 | Restriccion de no tocar |
|---|---|---|---|---|---|---|---|
| P0-001 | P0 | `ui/web/*` | No se detecta endpoint/runtime/dispatch activo nuevo | ausencia `/api/debate/start`, `/api/dispatch`, hash routing | Sin bloqueo actual | Mantener tests | No abrir endpoints |
| P0-002 | P0 | `ui/web/*` | No se detecta legacy visual IA_CORE activo | rg sin SAAOP/Loteria/Tactical HUD en `ui/web` | Sin bloqueo actual | Mantener regresion | No reintroducir legacy |
| P1-001 | P1 | `index.html`, `styles.css`, `console-interactions.js` | `debate-*` vive como request draft | `debate-panel`, `debate-toggle`, `btn-debate` | Feature vieja aparente | Renombrar a request draft | No habilitar draft |
| P1-002 | P1 | `index.html`, `admin-panels.js`, `i18n_es.json` | `orchestration-*` vive en Request Contract | `orchestration-task`, `orchestration-status`, `orchestration-agents` | Workflow operativo aparente | Renombrar request contract | No crear dispatch |
| P1-003 | P1 | `index.html`, `admin-panels.js` | `logs-runtime` | logs sanitizados | Runtime aparente | Renombrar `logs-sanitized` | No tocar endpoint |
| P1-004 | P1 | `styles.css` | `.status-dot.active` podria representar activo operativo | clase verde active | Estado prohibido si vivo | Verificar y renombrar | No asumir uso |
| P2-001 | P2 | `index.html` | `.active` en config/sidebar/skin | classList add/remove active | Estado visual legacy | Renombrar `is-selected/is-visible` | No tocar readiness |
| P2-002 | P2 | `styles.css` | CSS externo duplicado/probablemente muerto | no link desde index | Deuda, regresion futura | Verificar consumidores | No borrar a ciegas |
| P2-003 | P2 | `index.html` | `activeAgentProfileCatalog` | variable local | Naming confuso | `currentAgentProfileCatalog` | No cambiar catalogo |
| P2-004 | P2 | `index.html`, `domains.js` | fetches admin/domain POST/DELETE fuera de modelo | `/api/agents/create`, `/api/domains/create` | Frontera confusa | Documentar management preexistente | No tocar backend |
| P2-005 | P2 | `i18n_es.json` | claves `debate.execute` y `orchestration.execute` | valores bloqueados | Naming heredado | Migrar claves o documentar | No romper data-i18n |
| P2-006 | P2 | `index.html`, `domains.js` | storage con `active` y `brand_input` | `ia_core_active_domain`, `brand_input` | Estado operativo aparente/namespacing | Migracion conservadora | No perder preferencias |
| P3-001 | P3 | `console-interactions.js` | `block: 'start'` | scrollIntoView | Falso positivo | Documentar | No tocar |
| P3-002 | P3 | `admin-panels.js` | `active_provider`, `active_model`, `status.running` | campos backend | Falso positivo | Documentar | No cambiar backend schema |
| P3-003 | P3 | docs/tests | menciones historicas legacy | tests negativos | Falso positivo | Preservar regression coverage | No limpiar historia |

No hay P0 bloqueante.

## Fase 13 - Plan Quirurgico Para 1.21

1. Renombrar `logs-runtime` a `logs-sanitized` en HTML/JS/tests, preservando `/api/logs` y copy de registros sanitizados.
2. Renombrar IDs/classes `orchestration-*` de Request Contract a `request-contract-*`; renombrar `loadOrchestrationAgents` a `loadRequestContractSources`.
3. Renombrar `debate-panel`, `debate-toggle`, `debate-input`, `btn-debate`, `debate-metrics` y `debate-synthesis` a nombres `request-draft-*` si el cambio se mantiene acotado; si no, documentar alias legacy y migrar copy visible/test.
4. Reemplazar `.active` vivo de config/skins por `is-selected`/`is-visible` o `data-ui-state`, manteniendo que no es readiness ni status backend.
5. Renombrar `activeAgentProfileCatalog` a `currentAgentProfileCatalog` y documentar campos backend `active_provider/active_model` como falsos positivos.
6. Inventariar consumidores de `ui/web/styles.css`; si no hay link activo, marcarlo como legacy stylesheet o reducirlo en prompt futuro.
7. Actualizar `i18n_es.json` solo si las claves `debate.*` y `orchestration.*` estan efectivamente usadas por `data-i18n`; preservar valores bloqueados.
8. Documentar que `domains.js` y agent management son admin management preexistente, no parte del modelo de permisos contract-aware 1.6-1.9.

Archivos probables a tocar en 1.21: `ui/web/index.html`, `ui/web/admin-panels.js`, `ui/web/console-interactions.js`, `ui/web/i18n_es.json`, `ui/web/README.md`, tests UI/UX afectados y documento 1.21. Tocar `ui/web/styles.css` solo despues de verificar consumidores.

Que no tocar: `core/`, `api.py`, `domains/`, `tools/`, modelos, integraciones, contratos backend, endpoints, routers, dependencias, runtime, execution, dispatch real, controlled execution, `backend_internal_ui_payload.v1`, `backend_internal_ui_request.v1`, `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `warnings`, `errors`, `validation`, `flags`, `readiness`, `status`, `service_kind`, `schema_version`, `summary/detail/raw-safe`, paneles 1.7, nav 1.8, sistema 1.9 y hardening 1.13.

Como evitar rediseño: cambiar nombres/copy/tests por grupos pequenos, mantener layout, no reordenar paneles, no agregar vistas ni animaciones, no instalar librerias y ejecutar regresiones UI/backend.

## Hallazgos Pospuestos

- Density reduction e information architecture.
- Operator guidance/empty-state intelligence.
- Contract storytelling.
- Secondary console views.
- Visual polish premium.
- Component documentation extendida.
- Benchmarks externos 21st.dev, UI UX Pro Max Skill y Framer Motion / Motion: benchmarks futuros solamente, sin instalacion ni dependencia.
- Limpieza profunda de `styles.css` hasta probar consumidores activos fuera de `index.html`.

## Falsos Positivos Registrados

- `PROHIBITED_ACTIVE_STATUSES` y `PROHIBITED_ALLOWED_ACTIONS` en `backend-contract-widgets.js`: listas defensivas, no permisos.
- `block: 'start'` en `console-interactions.js`: opcion de scroll, no accion start.
- `active_provider`, `active_model` y `status.running` en `admin-panels.js`: datos backend/status, no estados UI contract-aware.
- `runtime`, `execution` y `dispatch` en copy negativo: validos cuando declaran no-runtime/no-execution/no-dispatch o blocked capabilities.
- Legacy en docs/tests: historico o fixture de regresion, permitido.
- `orchestrator` como opcion de rol: catalogo/agente, no workflow runtime.

## Confirmaciones Contractuales

IA_CORE permanece como identidad visual activa.

No hay SAAOP, S.A.A.O.P., Loteria, Lotería, lottery, Tactical HUD, U-Score, CAZADOR, ESPEJO ni combinatoria como UI activa en `ui/web`.

Se preservan: `backend_internal_ui_payload.v1`, `backend_internal_ui_request.v1`, `internal_exposure_registry`, `internal_request_validation`, `internal_dispatcher_no_runtime`, `internal_confirmation_gate`, `internal_response_adapter`, `allowed_actions`, `forbidden_actions`, `blocked_capabilities`, `warnings`, `errors`, `validation`, `flags`, `readiness`, `status`, `service_kind`, `schema_version`, `summary/detail/raw-safe`, paneles de detalle 1.7, navegacion interna 1.8, sistema de componentes 1.9, responsive/accessibility hardening 1.13 y admin boundary hardening 1.17.

Confirmado: no endpoint publico nuevo; no API/router nuevo; no hash routing operativo; no `/api/debate/start`; no `/api/dispatch`; no runtime; no execution; no dispatch real; no controlled execution; no materialize/lifecycle activo desde UI; no dependencias nuevas; no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni integraciones.

## Proximo Prompt Exacto Sugerido

`PROMPT UI/UX 1.21 - Endurecer o documentar incongruencias frontend segun auditoria IA_CORE contract-aware sin runtime/no-execution`

