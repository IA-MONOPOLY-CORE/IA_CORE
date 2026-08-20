# HUD web principal

`ui/web/` es la interfaz principal de IA_CORE. FastAPI la sirve como contenido
estático y toda operación contra el sistema pasa por `/api/*`.

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
nuevo del HUD. Las incorporaciones deben reutilizar sus claves o ampliarlo antes
de agregar nuevos textos visibles; la migración del HUD existente puede hacerse
de forma incremental sin duplicar un segundo catálogo.
