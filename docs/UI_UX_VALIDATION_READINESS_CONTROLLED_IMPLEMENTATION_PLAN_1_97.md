# UI/UX Validation & Readiness Controlled Implementation Plan 1.97

## Decision

`VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY`

Este documento baja los guardrails 1.96 a un plan operativo para el futuro prompt 1.98. No implementa la pantalla y no autoriza por sí solo cambios de código: la implementación requiere aprobación humana explícita mediante el prompt 1.98.

## Base y estado recibido

- Commit base esperado: `c5518a4`.
- Commit local de guardrails 1.96: `c5518a4`.
- Restore point remoto vigente: `7ad9a8b`.
- Rama: `main`.
- Estado inicial: `main` ahead de `origin/main` por 2 commits locales, con working tree limpio.
- 1.96: `VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY`.
- 1.95: `NEXT_SCREEN_VALIDATION_READINESS_SELECTED`.
- Contract Overview / `FSC-CO-01`: baseline visual/contractual 1.
- Blocked & Forbidden / `FSC-BF-02`: baseline visual/contractual 2.
- Request Contract Preview: diferido.
- Push: pospuesto.

## Objetivo

Preparar la implementación controlada de una sola `Validation & Readiness Screen` dentro del `Panel Maestro`, contract-aware, documental, final y read-only. El futuro 1.98 debe representar información declarada sin crear permiso, ejecución, delivery, runtime ni workflow activo.

## Contrato base Validation & Readiness

El contrato se apoya en la auditoría 1.76, el contrato final 1.77, el checkpoint 1.78 y el cierre de gaps menores 1.73/1.74. Esos documentos describen `Validation & Readiness` como una superficie documental futura y no como una pantalla operativa existente. La fuente contractual general es `backend_internal_ui_payload.v1`.

El id UI candidato es `FSC-VR-03`. Los documentos base no declaran otro id final explícito; por eso 1.98 podrá usarlo como identidad UI propuesta y debe conservar la distinción entre identificador visual y contrato backend.

## Alcance implementable futuro

El prompt 1.98 podrá implementar únicamente:

- Una sola sección/pantalla `Validation & Readiness Screen`.
- Un bloque hermano dentro del `Panel Maestro`, después de Blocked & Forbidden, sin reemplazar ninguna pantalla previa.
- Markup estático y estilos necesarios para una lectura documental/read-only.
- Representación de `backend_internal_ui_payload.v1` únicamente cuando el dato ya esté disponible de forma segura y declarada.
- Estados contract-bound de validation, readiness, blockers, warnings y missing requirements.
- Un estado `empty`/`deferred`/`not-available` honesto cuando no exista payload seguro.
- Evidence snapshot documental etiquetado como snapshot, nunca como log vivo.
- Límites visibles: no-runtime, no-execution, no-dispatch, no-endpoint y no-user-panel.
- Separación explícita entre readiness y permission, validation y execution, passed y operational success, warning/error y live runtime, review-required y workflow activo.
- Referencias documentales a Contract Overview, Blocked & Forbidden y Request Contract Preview diferido.
- Tests estáticos/documentales y checks de no-regresión bajo `tests/`.
- Actualización del documento 1.98 y del cursor README correspondiente.

No se permite ampliar el alcance a más de una pantalla, a navegación nueva ni a una fuente de datos nueva.

## Alcance prohibido futuro

El prompt 1.98 no podrá implementar ni introducir:

- Ejecución, run, dispatch, submit, retry o revalidación live.
- Refresh contra backend, endpoint, fetch, worker, queue, scheduler o live monitor.
- Aprobar ejecución, marcar ready operativo, marcar passed operativo, resolver ahora o auto-fix.
- Unlock, override, bypass, enable, permission escalation o cambio de autoridad.
- User Panel, rutas/hash, router, navegación operativa o workflow activo.
- Cambios en backend, `api.py`, `core/`, `domains/`, `providers/`, `tools/`, `scripts`, modelos o integraciones.
- Cambios de CI, dependencias, secretos, `.env`, tokens, API keys o credenciales.
- Live logs, runtime handles, job ids, worker ids, queue ids o execution ids.
- Raw payload/package, datos inventados, fake success o ghost actions.
- Revalidación, materialización, delivery, deployment o publicación.
- Modificaciones a Contract Overview o Blocked & Forbidden.
- Limpieza de deuda técnica o correcciones de `pyflakes`.

## Candidate future implementation files

| Archivo | Razón | Cambio permitido en 1.98 | Cambio prohibido | Riesgo |
|---|---|---|---|---|
| `ui/web/index.html` | Punto actual de las superficies contract-aware | Agregar una sección hermana estática para `FSC-VR-03` después de `FSC-BF-02`; no reescribir bloques previos | No tocar Contract Overview, Blocked & Forbidden, navegación operativa ni formularios | Duplicación, overload y CTA implícito |
| `ui/web/styles.css` | Hoja candidata para estilos aislados | Agregar estilos scoped y responsive de lectura documental | No cambiar estilos globales de pantallas cerradas ni crear señales de éxito operativo | Regresión visual o severidad ambigua |
| `ui/web/backend-contract-widgets.js` | Ya normaliza payload contractual local | Solo evaluar reutilización de helpers existentes si no agrega fuente ni fetch | No agregar endpoint, fetch, refresh backend, cálculo de permission ni runtime | Mezclar widget existente con nueva semántica |
| `ui/web/admin-panels.js` | Admin loaders existentes son sensibles a endpoints | Evitarlo; tocarlo solo con justificación de lectura local y sin loader nuevo | No agregar loader, endpoint, fetch, refresh ni acción admin | Fuga de superficie operativa |
| `ui/web/console-interactions.js` | Contiene foco/inspección local existente | Evitarlo; solo reutilizar foco local ya compatible, sin ruta/hash | No crear workflow, tab ejecutable ni navegación operativa | Affordance de checklist o navegación activa |
| `ui/web/i18n_es.json` | Fuente de copy localizado existente | Tocar solo si 1.98 requiere nuevas etiquetas documentales y el cambio es aislado | No agregar copy operativo ni cambiar estados globales existentes | Contradicción semántica de traducciones |
| `tests/test_ui_ux_validation_readiness_screen_implementation_1_98.py` | Verifica el contrato de la nueva sección | Crear tests estáticos de identidad, estados, datos, límites y preservación | No usar tests para autorizar runtime o backend | Cobertura incompleta |
| `docs/UI_UX_VALIDATION_READINESS_SCREEN_IMPLEMENTATION_1_98.md` | Registra alcance y evidencia de implementación | Crear documento de implementación, diff, tests y límites | No declarar éxito operativo ni checkpoint antes de tiempo | Cierre prematuro |
| `README.md`, `ui/web/README.md` | Mantienen el cursor visible | Registrar 1.98, decisión, límites y próximo prompt | No declarar checkpoint/push si 1.99/1.100 no pasaron | Cursor desalineado |

Los archivos preferidos son `ui/web/index.html`, `ui/web/styles.css`, el test 1.98, el documento 1.98 y los README. Los scripts JS y el archivo de i18n son secundarios y deben permanecer intactos salvo necesidad concreta, demostrable y no operativa.

## Prohibited files

| Archivo/zona | Motivo | Condición excepcional |
|---|---|---|
| `api.py` | Evitar endpoints y cambios de autoridad | Ninguna en 1.98 |
| `core/` | Evitar runtime, execution y contratos operativos | Ninguna en 1.98 |
| `domains/` | Fuera de la superficie UI documental | Ninguna en 1.98 |
| `providers/` | Evitar integraciones y routing de modelos | Ninguna en 1.98 |
| `tools/`, `scripts/` | Evitar side effects, workers y automatización | Ninguna en 1.98 |
| Modelos e integraciones | Evitar datos operativos nuevos | Ninguna en 1.98 |
| CI y dependencias | Mantener entorno y reproducibilidad | Ninguna en 1.98 |
| `.env`, secrets, tokens, API keys | Protección de información sensible | Nunca leer ni modificar |
| Contract Overview / Blocked & Forbidden | Son baselines cerrados | Ninguna; detenerse si parece necesario |

## Future placement strategy

La ubicación recomendada es una tercera sección hermana, después de `Contract Overview` y `Blocked & Forbidden` en el flujo documental del `Panel Maestro`. No reemplaza, reordena ni embebe las dos pantallas cerradas. Debe tener un contenedor propio, identidad `FSC-VR-03` y un `data-main-console-zone` específico, sin ruta ni hash.

La jerarquía de lectura será: primero contrato y fuente; después límites duros; recién después validation/readiness. La pantalla no debe verse como una variante de Blocked & Forbidden ni como un resumen duplicado de Contract Overview: explica estados declarados, requisitos faltantes y evidencia documental.

Para evitar apariencia de checklist ejecutable, los findings se muestran como filas o bloques informativos no accionables. No se agregan botones, toggles, tabs que disparen validación ni controles que parezcan completar tareas. Cualquier disclosure permitido será local, explícitamente read-only y sin fetch.

## Future visual structure

1. **Header**: `Validation & Readiness`, `FSC-VR-03`, `Panel Maestro`, `read-only` y `contract-bound`.
2. **Status strip documental**: `validation-documented`, `readiness-documented`, `ready-no-permission`, `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint` y `no-user-panel`.
3. **Readiness vs permission**: readiness es información declarada y nunca aprobación operativa.
4. **Validation vs execution**: validation es lectura contractual y nunca corre checks live.
5. **Readiness summary**: resumen documental sin CTA ni promesa de success.
6. **Validation findings**: categorías `passed`, `warning` y `error` con contexto documental, sin runtime vivo.
7. **Blockers/warnings/missing requirements**: visibles, priorizados y no convertidos en tareas clickeables.
8. **Evidence snapshot**: fuente, referencia y fecha solo si provienen del snapshot; nunca timestamp vivo inventado.
9. **No-runtime boundary**: límites no-runtime/no-execution/no-dispatch explícitos y sin CTA.
10. **Baseline references**: Contract Overview, Blocked & Forbidden y Request Contract Preview diferido.
11. **Empty/deferred state**: mensaje honesto ante ausencia de payload; no placeholders que parezcan datos reales.
12. **Anti-affordance notice**: una etiqueta de readiness o validation no es una acción.
13. **Documentation references**: referencias internas sin abrir flujo operativo.

## Data policy

### Datos permitidos

- `validation_status` y `readiness_status` documentales.
- `readiness_notes`, blockers, warnings y missing requirements declarados.
- Contract id, fuente y `backend_internal_ui_payload.v1`.
- Scope boundary, estados contract-bound y policy-bound.
- Evidence snapshot documental y referencias a checkpoints.
- Timestamps solo cuando pertenezcan al documento/payload y estén etiquetados como snapshot.
- `review_required` como estado documental, no workflow activo.
- Referencias a Contract Overview y Blocked & Forbidden como baselines.
- Etiquetas no-runtime/no-execution/no-dispatch/no-endpoint/no-user-panel.

### Datos prohibidos

- Secrets, tokens, API keys, credentials o URLs sensibles.
- Runtime handles, job ids, worker ids, queue ids o execution ids.
- Live logs, telemetría viva, métricas runtime o timestamps inventados.
- Raw payload/package o campos que permitan inferir autoridad no declarada.
- Datos operativos ejecutados, resultados de jobs o delivery.
- `passed`, `ready` o `valid` inventados, mocks que parezcan datos reales o fake success.
- Cualquier estado que habilite una acción o sugiera conexión de endpoint.

## State policy

### Estados permitidos

`documented`, `read-only`, `validation-documented`, `readiness-documented`, `ready-no-permission`, `review-required`, `blocked`, `warning-documented`, `missing-requirement`, `not-available`, `deferred`, `not implemented`, `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint`, `no-user-panel`, `contract-bound` y `policy-bound`.

### Estados prohibidos

`active`, `running`, `live`, `executing`, `dispatching`, `submitted`, `processing`, `completed operativo`, `success operativo`, `ready to run`, `ready to execute`, `validation passed` como runtime success, `enabled`, `unlocked`, `approved to execute`, `endpoint connected`, `worker active`, `queue active`, `live monitor`, `auto-resolve`, `auto-fix`, `deployment ready` y `publish ready`.

`passed`, `warning` y `error` solo podrán aparecer con contexto documental explícito. `ready-no-permission` nunca podrá abreviarse visualmente a `ready` si eso genera lectura de ready-to-run.

## Copy policy

### Copy permitido

El copy debe ser contractual, claro, sereno, educativo, read-only y orientado a estado documental. Debe decir que readiness no es permission, validation no es execution, passed no es operational success, warning/error no es live runtime y review required no es workflow activo. Debe mostrar blockers sin alarmismo y explicar un estado vacío sin inventar disponibilidad.

### Copy prohibido

No usar como copy visible: `Ejecutar`, `Correr`, `Run`, `Start`, `Launch`, `Dispatch`, `Submit`, `Enviar`, `Publicar`, `Activar`, `Aprobar ejecución`, `Ready to run`, `Ready to execute`, `Listo para ejecutar`, `Validation success`, `Success`, `Completed`, `Passed` como éxito operativo, `Live`, `Running`, `Processing`, `Endpoint connected`, `Worker active`, `Queue active`, `Revalidar en vivo`, `Refresh backend`, `Resolver ahora`, `Auto-fix`, `Enable`, `Unlock`, `Override`, `Bypass`, `User Panel activo`, `Deploy` o `Publish ready`.

## Affordance policy

### Permitidas

- Labels y chips read-only de estado documental.
- Disclosures locales para evidencia, sin endpoint, fetch ni cambio de estado.
- Referencias documentales internas.
- Notas de revisión documental.
- Foco local únicamente si ya existe el patrón y no parece una acción operativa.

### Prohibidas

- Botones, toggles o pseudo-botones dentro de la nueva superficie.
- Refresh que parezca backend, iconos clickeables no explicados o hover operativo.
- Links a User Panel, tabs que parezcan ejecutar validation o review required como flujo accionable.
- `passed`/`ready` como CTA implícito.
- Cualquier acción de resolución, aprobación, revalidación, unlock, override o bypass.

La auditoría anti-CTA/anti-affordance será obligatoria antes del checkpoint. Cada elemento que pueda parecer acción debe clasificarse; ante ambigüedad, se corrige antes de 1.99 y no se hace push.

## Controlled implementation strategy

1. Confirmar 1.97 cerrado, aprobación humana para 1.98, working tree limpio y restore point remoto disponible.
2. Crear primero la sección estática en `ui/web/index.html`, después de Blocked & Forbidden, sin modificar el markup anterior.
3. Aplicar estilos aislados y responsive en `ui/web/styles.css` o en el punto ya establecido, sin alterar la severidad de baselines cerrados.
4. Usar únicamente datos ya declarados y seguros; ante ausencia de payload, renderizar `deferred`/`not-available` honesto.
5. Evitar JS. Solo reutilizar helpers locales existentes si la interacción es estrictamente de lectura y no agrega fuente, fetch, ruta o endpoint.
6. Crear tests estáticos antes de considerar terminada la implementación.
7. Ejecutar node checks, tests contractuales, `git diff --check` y revisión de no-modificación de backend/baselines.
8. Hacer revisión visual humana y auditoría anti-affordance antes del hardening 1.99.
9. Documentar 1.98 con evidencia exacta, commit local y límites; no hacer push hasta el checkpoint 1.100.

## Future tests required

El test 1.98 deberá verificar, como mínimo:

- Existencia y visibilidad de `Validation & Readiness Screen`.
- `FSC-VR-03` o el id real si aparece uno distinto en la fuente contractual.
- `backend_internal_ui_payload.v1`, `Panel Maestro` y `read-only` visibles.
- `readiness no permission`, `validation no execution`, `passed no operational success`, `warning/error no live runtime` y `review required no workflow active`.
- Blockers, warnings y missing requirements visibles.
- No botones operativos, no ready-to-run y no CTA implícito.
- No runtime, execution, dispatch, endpoint, fetch, User Panel ni rutas/hash nuevas.
- No raw package, fake success, ghost actions ni hidden blockers.
- No identity leakage de Lotería/SAAOP.
- Contract Overview y Blocked & Forbidden preservados.
- Evidence snapshot sin live log ni timestamp inventado.
- Copy y estados prohibidos ausentes en la superficie activa.
- Auditoría anti-CTA/anti-affordance registrada.
- Responsive básico, cuatro `node --check`, `git diff --check` y tests backend contract aplicables.

## Entry criteria

La implementación 1.98 solo puede comenzar si:

- 1.97 está cerrado con decisión `VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY`.
- El operador humano aprueba explícitamente el prompt 1.98.
- Working tree limpio, HEAD esperado y restore point remoto previo disponible.
- Tests 1.96 y 1.97 verdes.
- El alcance de archivos coincide con candidate files y no hay gaps P0.
- Contract Overview y Blocked & Forbidden están disponibles como baseline doble.

## Exit criteria

La implementación 1.98 solo puede considerarse lista para 1.99 si:

- Existe una sola pantalla/sección `Validation & Readiness Screen` en Panel Maestro.
- Readiness está separado de permission; validation de execution; passed de success operativo; warning/error de runtime vivo; review required de workflow activo.
- Blockers, warnings y missing requirements son visibles y no accionables.
- No hay CTAs operativos, backend, runtime, endpoint, fetch, User Panel, ruta/hash ni dependencia nueva.
- Contract Overview y Blocked & Forbidden permanecen intactos.
- Tests, node checks y diff check pasan.
- Se hizo revisión visual humana y auditoría anti-affordance.
- Existe documento 1.98 y commit local; push permanece pospuesto.

## Rollback strategy

El rollback normal es revertir el commit local específico de 1.98, preservando los commits previos y sin reescribir historia. Se debe detener la implementación y volver al plan si aparece cualquiera de estas condiciones:

- Se necesita backend, `api.py`, endpoint, fetch, runtime, execution, dispatch, worker, queue o scheduler.
- Se necesita ruta/hash, User Panel o modificación de navegación operativa.
- Se necesita tocar Contract Overview o Blocked & Forbidden.
- Aparece `ready-to-run`, success operativo, live runtime, fake success o ghost action.
- Un blocker se oculta, una affordance parece ejecutable o el estado review-required parece workflow.
- El cambio requiere dependencias, CI, secretos, deuda residual o corrección de `pyflakes`.

## Risk register

| Riesgo | Mitigación obligatoria |
|---|---|
| Readiness interpretado como permiso | Mostrar `readiness no permission` junto al estado |
| Validation interpretada como ejecución | Mostrar `validation no execution` y ausencia de runtime |
| Passed interpretado como success operativo | Mostrar `passed no operational success` |
| Warning/error interpretado como runtime activo | Mostrar `warning/error no live runtime` |
| Review required interpretado como workflow activo | Mostrar `review required no workflow active` |
| Ready-no-permission confundido con ready-to-run | Prohibir `ready-to-run` y mantener ambas frases separadas |
| Blockers ocultos por visual positivo | Mantener blockers siempre visibles |
| Badges verdes ambiguos | Usar severidad contextual y copy documental |
| Affordance de inspección confundida con acción | Clasificar cada disclosure/foco como local y read-only |
| Refresh accidental | No crear refresh en la nueva superficie |
| Endpoint/fetch accidental | Test estático y revisión de diff |
| User Panel leakage | Identidad y scope limitados a Panel Maestro |
| Rutas/hash accidentales | Sección estática sin navegación nueva |
| Backend accidental | Lista de archivos prohibidos y stop condition |
| Fake success | No inventar passed, ready, valid, métricas ni timestamps |
| Ghost actions | Buscar botones, toggles, links y handlers ambiguos |
| Duplicación con Contract Overview | Overview resume el mapa; VR explica estados/evidencia |
| Contradicción con Blocked & Forbidden | Mantener límites duros como baseline 2 visible |
| Raw package leakage | Solo proyección segura y documental |
| Overload técnico | Mantener una sola sección y evitar JS nuevo |
| Saltar auditoría anti-affordance | Convertirla en criterio de salida antes de 1.99 |
| Push antes de checkpoint | Push prohibido hasta 1.100 |

## Final decision and next prompt

La decisión única de este plan es:

`VALIDATION_READINESS_CONTROLLED_IMPLEMENTATION_PLAN_READY`

El próximo prompt exacto es:

`PROMPT UI/UX 1.98 - Implementar Validation & Readiness Screen IA_CORE contract-aware sin runtime/no-execution`

Ese prompt implementaría la pantalla solo si el operador humano lo aprueba. No debe hacer push por defecto. El checkpoint con push corresponde a 1.100, únicamente si 1.98 y 1.99 pasan todas sus validaciones.

## Límites preservados

En 1.97 no se implementó pantalla, no se modificó UI activa, no se tocó Contract Overview, no se tocó Blocked & Forbidden, no se creó User Panel, no se crearon rutas/hash, no se tocaron backend/runtime/endpoints/CI/dependencias, no se limpió deuda residual, no se corrigieron pyflakes y no se avanzó a 1.98. No se hace push.

Marcadores literales de límite: no runtime, no execution, no dispatch, no endpoint, no fetch, no User Panel, no rutas/hash, no backend, no CI, no deuda residual, no pyflakes, no se implementó pantalla, no se modificó UI activa, no se tocó Contract Overview, no se tocó Blocked & Forbidden, no se creó User Panel, no se avanzó a 1.98. No se hace push.
