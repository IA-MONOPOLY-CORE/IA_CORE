# UI/UX Panel Maestro Structural Redesign Pre-Implementation Guardrails 1.122

## Base, objetivo y alcance

- Base esperada: `5a78211` (`docs(ui): documentar arquitectura visual futura panel maestro`).
- Restore point remoto vigente: `01d09ce`.
- Commits locales previos: `8843b60`, `03975b9`, `f3a2670`, `5a78211`.
- Rama: `main`, local ahead de `origin/main` por cuatro commits.

Este documento define guardrails pre-implementación para el rediseño estructural del Panel Maestro IA_CORE. Convierte la arquitectura visual futura 1.121 y la auditoría real 1.120 en límites verificables para futuras tareas. 1.122 no implementa pantalla, no modifica la UI activa y no habilita ninguna capacidad.

## Estado recibido

- `PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_PRE_IMPLEMENTATION_GUARDRAILS` es la decisión de 1.121.
- `PANEL_MAESTRO_CURRENT_ARCHITECTURE_AUDIT_READY_FOR_VISUAL_ARCHITECTURE_DOC` es la decisión de 1.120.
- El restore point remoto vigente es `01d09ce`; el restore point anterior es `ccdef7a`.
- La rama local está ahead por cuatro commits: `8843b60`, `03975b9`, `f3a2670` y `5a78211`.
- Final Screen Contracts consolidado/publicado: Contract Overview, Blocked & Forbidden, Validation & Readiness y Request Contract Preview.
- Los elementos inferiores bloqueados/publicados permanecen fuera de la baseline contractual.
- `+` y `DOMAIN` son deuda UX futura no bloqueante; no autorizan creación ni mutación.
- `DEFER_FINALIZATION` continúa vigente en Request Contract Preview.

## Principio general de implementación futura

La implementación futura del rediseño estructural será incremental. No se reemplaza toda la UI de una vez: cada bloque visual tendrá un prompt propio, archivos permitidos explícitos, validaciones propias y una revisión visual humana al cierre. No se avanza al bloque siguiente sin checkpoint; no se publica un restore point sin validación y decisión explícita; la arquitectura futura no puede usarse para activar capacidades.

Cada cambio deberá poder revertirse hasta el checkpoint anterior, conservar la baseline contractual y demostrar que su apariencia no crea una interpretación operativa. El método es de un prompt por vez: documentar, planificar, implementar solo el bloque aprobado, endurecer, revisar visualmente y decidir el restore point.

## Guardrails de archivos

### Permitidos por defecto para documentación

- `docs/`
- `tests/`
- `README.md`
- `ui/web/README.md`

### UI modificable solo con prompt futuro explícito

- `ui/web/index.html`
- `ui/web/styles.css`
- `ui/web/i18n_es.json`

El primer bloque visual futuro debería preferir `ui/web/index.html`, `ui/web/styles.css` y `ui/web/i18n_es.json` si hace falta copy, sin tocar JS salvo necesidad demostrada, documentada y aprobada.

### JavaScript con autorización fuerte

Solo un prompt futuro explícito, con razón y diff acotado, puede modificar:

- `ui/web/backend-contract-widgets.js`
- `ui/web/admin-panels.js`
- `ui/web/console-interactions.js`
- `ui/web/domains.js`

La autorización JS no permite runtime, execution, dispatch, endpoints, fetches, mutaciones ni invocación de modelos/herramientas; solo delimita quién podría revisar un cambio futuro.

### Prohibidos salvo prompt dedicado futuro

- `api.py`
- `core/`
- `domains/`
- `providers/`
- `tools/`
- `scripts/`
- modelos
- integraciones
- CI
- dependencias
- `.env`
- secrets
- cualquier backend operativo

No se leen, imprimen, revelan ni manipulan secretos, tokens, API keys, credentials, headers, auth o `.env`.

## Guardrails HTML

### Permitido en una futura implementación aprobada

- Reorganizar markup documental.
- Crear wrappers visuales.
- Crear secciones o documentary screens internas sin rutas/hash.
- Renombrar labels para claridad y bajar ambigüedad.
- Mover contenido visualmente dentro de la responsabilidad correspondiente.
- Marcar lectura, bloqueado y futuro.
- Usar atributos `data-*` de seguridad ya existentes o equivalentes documentales.
- Mantener visibles los cuatro IDs FSC, sus estados y `DEFER_FINALIZATION`.

### Prohibido

- Crear forms submiteables.
- Crear botones operativos.
- Crear enlaces con rutas/hash.
- Crear navegación real tipo app.
- Crear User Panel.
- Crear inputs de mutación.
- Crear estados activos o success operativo.
- Exponer payload crudo, raw Package o secrets.
- Crear acciones globales ambiguas.
- Convertir un disabled visual en una capability aparente.

Marcadores obligatorios de alcance HTML: no forms submiteables, no botones operativos, no rutas/hash, no User Panel, no pantalla operativa, no endpoint y no acción global ambigua.

## Guardrails CSS

### Permitido

- Mejorar jerarquía visual.
- Reducir densidad y repetición.
- Agrupar zonas por responsabilidad.
- Bajar intensidad de chips/pills.
- Mejorar lectura responsive, contraste y focus sin crear acción.
- Crear clases visuales documentales.
- Separar capas visuales y usar progressive disclosure.

### Prohibido

- Usar CSS para ocultar capacidades bloqueadas sin documentarlas.
- Hacer que controles bloqueados parezcan activos.
- Crear animaciones que sugieran ejecución, live o running.
- Crear estados visuales operativos prohibidos.
- Esconder warnings contractuales o blockers.
- Depender de CSS para seguridad funcional.

Marcador CSS: no usar CSS para ocultar warnings contractuales, blockers o capabilities bloqueadas.

El color, el movimiento, un hover, un icono o un disabled no pueden otorgar autoridad que el contrato no declara.

## Guardrails JS

### Permitido solo con autorización futura

- Disclosures locales.
- Lectura local.
- Toggles visuales sin side effect.
- Validaciones documentales.
- Helpers de render no-operativos.

### Prohibido

- Crear un fetch nuevo.
- POST/PUT/DELETE.
- `WebSocket`.
- `polling`.
- `queue`.
- `worker`.
- `scheduler`.
- `runtime`.
- `execution`.
- `dispatch`.
- `model invocation`.
- `tool invocation`.
- `submit`.
- Mutación operativa de estado.
- `localStorage` como mutación operativa.
- `window.location`, `hash` o `history` para navegación real.
- Handlers que simulen operación.
- `fake success`.
- `ghost actions`.

Marcadores obligatorios JS: no fetch nuevo, no endpoint, no runtime, no execution, no dispatch, no fake success y no ghost actions.

Los fetches heredados observados en 1.120 siguen siendo una frontera de riesgo y no se convierten en autorización por el hecho de existir detrás de guards.

## Guardrails de navegación futura

- No rutas/hash todavía.
- No User Panel.
- No navegación pública.
- La navegación futura solo puede ser documental.
- Tabs, secciones o índice interno solo podrán existir si un prompt futuro los autoriza explícitamente.
- Cualquier navegación debe mantener bloqueos visibles, sin ocultar Blocked, Validation o Request Preview.
- Toda pantalla futura debe declarar `READ_ONLY`, `BLOCKED_BY_CONTRACT`, `DOCUMENTED` o `FUTURE_ONLY` cuando corresponda.
- No se agregan endpoints, fetches, polling, loaders operativos ni sincronización remota para navegar.

## Guardrails de estados visuales

Estados permitidos:

`READ_ONLY`, `BLOCKED_BY_CONTRACT`, `DOCUMENTED`, `PLANNED`, `DEFERRED`, `NEEDS_VALIDATION`, `VALIDATED_DOCUMENTALLY`, `FUTURE_ONLY`, `NO_RUNTIME`, `NO_EXECUTION`.

Estados prohibidos:

`ACTIVE`, `RUNNING`, `LIVE`, `EXECUTING`, `DISPATCHING`, `SUBMITTED`, `PROCESSING`, `SENT`, `ENQUEUED`, `SCHEDULED`, `READY_TO_RUN`.

Los estados prohibidos no pueden reaparecer como badge, clase, tooltip, animación, botón disabled o copy calificado de forma ambigua. `validated`, `passed` y `ready` solo pueden referirse a una constatación documental explicada.

## Guardrails de copy/idioma

### Permitido

- Español consistente.
- IA_CORE como identidad visible activa.
- Lenguaje documental.
- “lectura”.
- “bloqueado por contrato”.
- “previsto”.
- “futuro”.
- “requiere contrato”.
- “evidencia”.
- “detalle”.
- “preview contractual”.

### Prohibido como promesa de operación

- SAAOP/Lotería como identidad visible activa.
- “ejecutar” como acción disponible.
- “correr” como acción disponible.
- “enviar” como acción disponible.
- “despachar” como acción disponible.
- “procesar” como acción disponible.
- “activar” como acción disponible.
- `live`.
- `running`.
- `active`.
- `submitted`.
- `ready to run`.
- Cualquier copy que prometa operación, disponibilidad o éxito real.

## Guardrails de Final Screen Contracts

- Los cuatro FSC deben preservarse: `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04`.
- Pueden reorganizarse visualmente solo con prompt explícito futuro.
- No deben perder IDs, estados, blockers, evidencia ni la distinción documental.
- Request Contract Preview debe conservar `DEFER_FINALIZATION`.
- Los FSC no deben convertirse en CTAs ni habilitar ejecución.
- No deben mezclarse con dominios/agentes como si fueran acciones.
- Cualquier cambio futuro debe pasar tests específicos y revisión humana visual.

## Guardrails de elementos inferiores

- Siguen bloqueados/read-only y no deben reactivarse.
- `CFG` futuro pertenece a Configuration Read-only.
- `DOMAIN` futuro pertenece a Domains Context.
- `+` no debe existir como acción global ambigua.
- `RELEER PAYLOAD LOCAL` solo puede conservarse como lectura local.
- `VER DETALLE` y `VER EVIDENCIA` solo pueden ser disclosures/evidence.
- Las tarjetas de agentes no invocan modelos.
- Los formularios no submitean.
- POST/PUT/DELETE siguen inaccesibles.
- Cualquier absorción o rediseño debe preservar no-runtime/no-execution.

## Guardrails de validación futura

Toda implementación futura deberá ejecutar como mínimo:

- `node --check` sobre JS tocados o relevantes.
- Un test nuevo específico.
- Tests de bloques previos relevantes.
- Test de backup readiness.
- Tests backend contract relevantes si aplica, sin modificar backend.
- `git diff --check`.
- Revisión humana visual antes de cerrar.
- Reporte de hash.
- Working tree limpio.

La validación deberá comprobar también: no quinta sección, no User Panel, no rutas/hash, no endpoints/fetches nuevos, FSC preservados, blockers visibles, `DEFER_FINALIZATION`, estados permitidos y ausencia de controles operativos.

## Guardrails de aprobación humana

Ninguna implementación visual se considera cerrada sin revisión humana. Si hay duda visual, no avanzar. Si parece operativo, bloquear o ajustar. Si se ve como User Panel, detener. Si aparece ruta/hash, detener. Si aparece endpoint/fetch nuevo, detener. Si aparece runtime/execution, detener. Si se reintroduce SAAOP/Lotería visible, detener. Si `+` parece acción global, detener. Si `DOMAIN` parece creación directa, detener.

La aprobación debe confirmar el alcance de archivos, la lectura responsive, foco/contraste, copy, estados, visibilidad de blockers, preservación de los cuatro FSC y ausencia de fake success o ghost actions.

## Primer bloque visual candidato

### Opciones evaluadas

1. `Master Shell + Overview Layer`.
2. `Final Screen Contracts Visual Rehousing`.
3. `Lower Console Absorption Planning`.
4. `Domains Context Screen Planning`.
5. `Design System / Visual Tokens Foundation`.

### Candidato elegido

`Master Shell + Overview Layer`

Es el bloque más seguro para iniciar el rediseño: organiza jerarquía general, identidad, estado global y lectura documental sin tocar todavía Final Screen Contracts ni reubicar elementos inferiores de alto riesgo.

| Criterio | Evaluación |
| --- | --- |
| Valor visual | Alto: reduce densidad y repeticiones del shell. |
| Riesgo | Bajo/medio si queda limitado a HTML/CSS/copy. |
| Archivos probables | `ui/web/index.html`, `ui/web/styles.css`, `ui/web/i18n_es.json` si hace falta. |
| Dependencia | Guardrails aprobados y contrato Master Shell/Overview. |
| Necesidad de JS | Ninguna por defecto; solo si se demuestra necesidad documental. |
| Impacto en contrato | No debe cambiar FSC, permisos ni `DEFER_FINALIZATION`. |
| Revisión humana | Directa y acotada en desktop/mobile. |
| Relación con UI actual | Reordena header, summary, índices y guidance ya auditados en 1.120. |
| Relación con `+`/`DOMAIN` | Los deja bloqueados y fuera del primer bloque. |

## Decisión final

`PANEL_MAESTRO_PRE_IMPLEMENTATION_GUARDRAILS_READY_FOR_FIRST_BLOCK_PLANNING`

## Justificación

Los guardrails definen archivos, límites HTML/CSS/JS, navegación, estados, copy, FSC, elementos inferiores, validación, aprobación humana, rollback y el primer bloque candidato. Corresponde planificar el primer bloque en un prompt dedicado antes de implementar, para conservar el método de un prompt por vez y evitar cambios grandes. 1.122 no autoriza implementación directa.

## Próximo prompt exacto

`PROMPT UI/UX 1.123 - Planificar primer bloque visual rediseño estructural Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Criterios de rollback y checkpoint

- El commit base para cualquier primer bloque será el restore point local que el prompt futuro confirme explícitamente.
- Si falla un test, aparece una affordance operativa, se pierde un FSC, se oculta un blocker o cambia `DEFER_FINALIZATION`, el bloque no se cierra.
- La revisión debe detener la publicación y conservar el árbol para diagnóstico, o revertir únicamente cambios del bloque aprobado mediante el procedimiento autorizado.
- No se hace push por defecto; solo un prompt de checkpoint puede decidirlo.

Marcador textual obligatorio: + no debe existir como acción global ambigua.

## Límites preservados

1.122 es solo definición de guardrails y test. No se implementó pantalla. No se agregó quinta sección. No se modificó UI activa. No se modificaron Final Screen Contracts. No se modificaron elementos inferiores. No se cambió contrato funcional. No se creó contrato final. No se contradijo `DEFER_FINALIZATION`. No se creó User Panel. No se crearon rutas/hash. No se crearon endpoints/fetches nuevos. No se activó runtime/execution/dispatch. No se tocó backend/runtime/endpoints/CI/dependencias. No se limpió deuda residual general. No se corrigieron pyflakes. No se hizo push. No se avanzó a 1.123.

Checklist literal: no pantalla, no quinta sección, no UI activa, no Final Screen Contracts, no elementos inferiores, no contrato funcional, no contrato final, no rutas/hash, no endpoint, no CI, no deuda residual, no pyflakes, no push y no se avanzó a 1.123.

Archivos UI protegidos y solo leídos en este prompt: `ui/web/index.html`, `ui/web/backend-contract-widgets.js`, `ui/web/admin-panels.js`, `ui/web/console-interactions.js`, `ui/web/domains.js`, `ui/web/styles.css` y `ui/web/i18n_es.json`.
