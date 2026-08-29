# UI/UX Panel Maestro First Visual Block Plan 1.123

## Commit base, objetivo y estado recibido

- Base esperada: `886efe6` (`docs(ui): definir guardrails pre implementacion panel maestro`).
- Restore point remoto vigente: `01d09ce`.
- Commits locales previos: `8843b60`, `03975b9`, `f3a2670`, `5a78211`, `886efe6`.
- Rama: `main`, local ahead de `origin/main` por cinco commits al inicio.

1.123 planifica el primer bloque visual del rediseño estructural del Panel Maestro IA_CORE sin implementarlo. Usa los guardrails 1.122, la arquitectura futura 1.121 y la auditoría actual 1.120 para fijar un alcance pequeño, revisable y sin runtime/no-execution.

Estado documental recibido:

- `PANEL_MAESTRO_PRE_IMPLEMENTATION_GUARDRAILS_READY_FOR_FIRST_BLOCK_PLANNING`.
- `PANEL_MAESTRO_FUTURE_VISUAL_ARCHITECTURE_READY_FOR_PRE_IMPLEMENTATION_GUARDRAILS`.
- Restore point remoto vigente `01d09ce`.
- Local ahead por cinco commits.
- Primer bloque candidato: `Master Shell + Overview Layer`.
- Final Screen Contracts preservados y fuera del alcance de implementación de este plan.
- elementos inferiores bloqueados y fuera del alcance de implementación de este plan.
- `+`/`DOMAIN` son deuda UX futura no bloqueante; no se reactivan.

## Bloque elegido y motivo

El bloque elegido es `Master Shell + Overview Layer`.

Es el primer paso más seguro porque organiza la jerarquía general, ordena la identidad IA_CORE, ordena el estado global, introduce una lectura documental clara y reduce ambigüedad en la parte superior. No toca todavía Final Screen Contracts como contrato funcional, no reubica elementos inferiores, no requiere JS y permite una revisión visual humana clara en una superficie acotada.

## Alcance del primer bloque visual futuro

El próximo prompt de implementación, si se aprueba, podrá trabajar solo sobre:

- Estructura visual superior/general.
- Shell maestro.
- Encabezado e identidad IA_CORE.
- Estado global visible como lectura.
- Overview documental.
- Introducción visible de capas visuales futuras como estructura, sin convertirlas en rutas.
- Agrupación inicial del resumen.
- Reducción de ambigüedad en la parte superior.
- Mejora de jerarquía, spacing y lectura responsive.
- Copy documental.
- Estados `READ_ONLY`, `DOCUMENTED`, `BLOCKED_BY_CONTRACT`, `NO_RUNTIME` y `NO_EXECUTION`.

El bloque no incluye la reorganización interna de los cuatro FSC, la lógica de Request Contract Preview, los elementos inferiores, formularios, agent cards operativas, `CFG`, `+`, `DOMAIN`, endpoints/fetches, rutas/hash, User Panel, backend o runtime.

### Resultado visual esperado

Al finalizar una eventual implementación, el primer viewport debe comunicar:

1. IA_CORE como identidad principal.
2. Un shell superior ordenado y documental.
3. Un overview que explique qué se lee y cuál es el estado contractual.
4. Estados visibles sin affordances de ejecución.
5. Un límite claro entre overview y los cuatro FSC existentes.
6. La continuidad de la evidencia y de los bloqueos sin abrir acciones.

## Archivos permitidos para futura implementación 1.124

### Permitidos si se elige implementación

- `ui/web/index.html`
- `ui/web/styles.css`
- `ui/web/i18n_es.json`, solo si hace falta ajustar copy visible.
- `docs/`
- `tests/`
- `README.md`
- `ui/web/README.md`

### Permitidos solo como lectura

- `ui/web/backend-contract-widgets.js`
- `ui/web/admin-panels.js`
- `ui/web/console-interactions.js`
- `ui/web/domains.js`

### Prohibidos

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

El prompt 1.124 deberá repetir la lista exacta de archivos permitidos y prohibidos antes de editar. Un archivo no listado queda fuera del alcance.

## Cambios HTML futuros

### Permitidos en el prompt dedicado

- Crear o ajustar el wrapper de `Master Shell`.
- Crear o ajustar el bloque `Overview Layer`.
- Ordenar encabezado, identidad y estado global.
- Agregar copy documental.
- Agregar marcas visuales de lectura, bloqueo y no-runtime.
- Agrupar el resumen superior.
- Mejorar jerarquía de secciones.
- Agregar atributos documentales `data-*` no operativos.
- Preservar IDs y anchors críticos existentes si los hay.

### Prohibidos

- forms.
- submit.
- Botones operativos.
- Enlaces reales, rutas o hash.
- User Panel.
- Navegación real.
- Inputs de mutación.
- fake success.
- Preview que envía.
- Botones con promesa de ejecución.
- Payload crudo o Package.
- Quinta sección o cambios internos de Final Screen Contracts.

Marcadores HTML obligatorios: no forms, no submit, no botones operativos, no rutas/hash y no User Panel.

## Cambios CSS futuros

### Permitidos en el prompt dedicado

- Mejorar layout superior, spacing y jerarquía.
- Reducir densidad.
- Crear clases de shell/overview.
- Mejorar tarjetas documentales.
- Bajar intensidad visual de estados sin ocultarlos.
- Mejorar responsive.
- Mejorar foco y legibilidad sin simular acción.

### Prohibidos

- Ocultar bloqueos.
- Hacer parecer activo lo bloqueado.
- Animaciones live/running/executing.
- Estilos de CTA operativo.
- Estilos que simulen submit/run/send.
- Esconder warnings contractuales.
- Usar CSS como seguridad funcional.

Marcador CSS obligatorio: no ocultar bloqueos y no animaciones live.

## Cambios i18n/copy futuros

### Permitidos

- Español claro y consistente.
- IA_CORE como identidad.
- Lectura/documental.
- Bloqueado por contrato.
- No runtime.
- No execution.
- Preview contractual.
- Evidencia.
- Detalle.
- Futuro.
- Previsto.
- Requiere contrato.

### Prohibidos

- SAAOP/Lotería como identidad visible activa.
- Ejecutar, correr, enviar, despachar, procesar o activar como acción disponible.
- `live`, `running`, `active`, `submitted` o `ready to run`.
- Promesas operativas.
- Éxito operativo.

## JS futuro

No se recomienda tocar JS para este primer bloque. Si el próximo prompt detecta necesidad de JS, debe detenerse y reportar o abrir un prompt dedicado.

Regla literal: no se recomienda tocar JS.

Guardrails explícitos:

- no listeners nuevos.
- no fetches nuevos.
- no localStorage nuevo.
- no navegación hash/history.
- no handlers operativos.
- no POST/PUT/DELETE.
- no runtime, execution, dispatch, workers, schedulers ni queues.
- Los disclosures existentes pueden quedar intactos si no se modifican.

## Preservación obligatoria

- Final Screen Contracts quedan intactos.
- Request Contract Preview mantiene `DEFER_FINALIZATION`.
- Elementos inferiores quedan intactos/bloqueados.
- `CFG`, `+` y `DOMAIN` no se tocan.
- `RELEER PAYLOAD LOCAL`, `VER DETALLE` y `VER EVIDENCIA` permanecen como lectura/disclosures no operativos.
- No se reactiva nada.
- No se cambia contrato funcional.
- No se crea contrato final.
- No se crea User Panel.
- No se crean rutas/hash.
- No se crean endpoints/fetches.
- No se toca backend.
- No se toca CI/dependencias.
- No se corrige pyflakes.
- No se hace push salvo futuro checkpoint explícito.

## Criterios visuales para aprobación humana futura

La persona revisora debe poder verificar visualmente que:

- Se entiende IA_CORE como identidad principal.
- El shell superior ordena la lectura.
- El overview comunica estado documental.
- Nada parece ejecutable.
- No hay botones ambiguos.
- No aparecen rutas/hash ni User Panel.
- No aparecen endpoints/fetches.
- No aparece runtime/execution/dispatch.
- No aparece SAAOP/Lotería como identidad visible.
- Final Screen Contracts siguen reconocibles.
- Elementos inferiores siguen bloqueados.
- `+` y `DOMAIN` no se reinterpretan como activos.
- La UI se ve más ordenada, no más confusa.

Marcador de aprobación: nada parece ejecutable; revisión humana visual obligatoria.

La revisión debe cubrir desktop y mobile, jerarquía, foco, contraste, wrapping, copy, estados, blockers, densidad y ausencia de ghost actions/fake success. Una duda visual detiene el checkpoint.

## Validaciones obligatorias para implementación futura

El próximo prompt de implementación deberá ejecutar como mínimo:

- `node --check ui/web/backend-contract-widgets.js`
- `node --check ui/web/admin-panels.js`
- `node --check ui/web/console-interactions.js`
- `node --check ui/web/domains.js`
- Un test nuevo específico de implementación visual.
- Tests 1.123, 1.122, 1.121, 1.120, 1.117, 1.115, 1.114.A y 1.110.
- `python -m pytest tests/test_ia_core_github_backup_readiness.py -q`.
- Tests backend contract relevantes si aplica, sin tocar backend.
- `git diff --check`.
- Revisión humana visual obligatoria antes de cerrar checkpoint.
- Reporte de hash y working tree limpio.

La validación deberá confirmar además: una sola superficie superior cambiada, no quinta sección, no User Panel, no rutas/hash, no endpoints/fetches nuevos, FSC preservados, blockers visibles, `DEFER_FINALIZATION` intacto y ausencia de controles operativos.

## Risk register

| Riesgo | Señal | Mitigación |
| --- | --- | --- |
| Tocar más UI de la permitida | Diff en FSC, lower console o archivos no listados | Lista cerrada de archivos y revisión de diff. |
| Modificar Final Screen Contracts por accidente | Cambian IDs, estados o copy contractual | Tests FSC y límite de alcance superior. |
| Modificar elementos inferiores por accidente | Cambian `CFG`, `+`, `DOMAIN`, forms o cards | Elementos inferiores solo lectura/bloqueados. |
| Reactivar `CFG`, `+`, `DOMAIN` | Aparece affordance o handler | No tocar; validación visual y diff. |
| `+` parece activo | Icono global con apariencia de alta | Mantenerlo fuera del bloque. |
| `DOMAIN` parece creación directa | Selector/formulario de dominio visible | Mantenerlo fuera del bloque. |
| Crear rutas/hash | `history`, `location` o enlaces reales | Prohibición y test negativo. |
| Crear User Panel | Copy o navegación de usuario | IA_CORE único y revisión humana. |
| Agregar fetch/endpoint | Nuevo acceso remoto | JS solo lectura; inspección de diff. |
| Tocar JS sin necesidad | Cambio en handlers o listeners | Detener y abrir prompt dedicado. |
| Introducir estado operativo | `ACTIVE`, `RUNNING`, `LIVE` o equivalente | Estados documentales permitidos. |
| Crear CTA operativo | Botón, submit o hover accionable | No botones operativos. |
| Crear fake success | `ready`, `passed` o success sin calificador | Copy documental y evidencia. |
| Crear ghost action | Control visible sin acción autorizada | Remover o no introducir control. |
| Romper `DEFER_FINALIZATION` | Preview parece envío/finalización | Mantener Request Contract Preview intacto. |
| Esconder bloqueos contractuales | Lower console o Blocked pierde visibilidad | Blockers siempre visibles. |
| Introducir SAAOP/Lotería visible | Alias histórico en identidad | IA_CORE como única identidad activa. |
| Aumentar densidad visual | Más duplicación en shell/overview | Una fuente por estado y progressive disclosure. |
| Implementación demasiado grande | Cambios en múltiples responsabilidades | Un bloque, archivos cerrados y checkpoint. |
| Acumular commits locales sin push | Muchos cambios sin checkpoint | Un commit por prompt; no push por defecto. |
| Romper restore point `01d09ce` | Base o rollback no reproducible | Referencia y hash reportados siempre. |

## Decisión final

`PANEL_MAESTRO_FIRST_VISUAL_BLOCK_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT`

## Justificación

El primer bloque está suficientemente acotado para una implementación guardada, incremental y revisable: solo reorganiza Master Shell + Overview Layer, prioriza HTML/CSS/copy, evita JS nuevo, preserva los cuatro FSC y mantiene bloqueados los elementos inferiores. La implementación no queda autorizada por este documento; requiere un prompt propio, diff limitado, validaciones y revisión visual humana.

## Próximo prompt exacto

`PROMPT UI/UX 1.124 - Implementar primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Límites preservados

1.123 es solo planificación. No se implementó pantalla. No se implementó `Master Shell + Overview Layer`. No se agregó quinta sección. No se modificó UI activa. No se modificaron Final Screen Contracts. No se modificaron elementos inferiores. No se cambió contrato funcional. No se creó contrato final. No se contradijo `DEFER_FINALIZATION`. No se creó User Panel. No se crearon rutas/hash. No se crearon endpoints/fetches nuevos. No se activó runtime/execution/dispatch. No se tocó backend/runtime/endpoints/CI/dependencias. No se limpió deuda residual general. No se corrigieron pyflakes. No se hizo push. No se avanzó a 1.124.

Checklist literal: no pantalla, no Master Shell + Overview Layer, no quinta sección, no UI activa, no Final Screen Contracts, no elementos inferiores, no contrato funcional, no contrato final, no rutas/hash, no endpoint, no CI, no deuda residual, no pyflakes, no push y no avance a 1.124.
