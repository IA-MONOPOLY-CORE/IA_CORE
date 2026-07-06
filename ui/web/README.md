# HUD web principal

`ui/web/` es la interfaz principal de IA_CORE. FastAPI la sirve como contenido
estático y toda operación contra el sistema pasa por `/api/*`.

## Paneles internos migrados

| Sección | API utilizada |
|---|---|
| Memory | `GET /api/memory` |
| Logs | `GET /api/logs` |
| Hybrid | `GET /api/status?full=true` |
| Orchestration | `GET /api/agents/list`, `POST /api/debate/start`, `GET /api/debate/{id}` |
| Overview | `GET /api/status` |

`admin-panels.js` implementa estas cinco secciones del modal de configuración.
Los controles operativos existentes del HUD permanecen en `index.html`.

## Catálogo de textos

`i18n_es.json` es la fuente de referencia en español para toda pantalla o flujo
nuevo del HUD. Las incorporaciones deben reutilizar sus claves o ampliarlo antes
de agregar nuevos textos visibles; la migración del HUD existente puede hacerse
de forma incremental sin duplicar un segundo catálogo.
