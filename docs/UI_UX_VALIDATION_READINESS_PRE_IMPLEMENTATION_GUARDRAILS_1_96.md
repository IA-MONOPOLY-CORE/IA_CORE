# UI/UX Validation & Readiness Pre-Implementation Guardrails 1.96

## Decision

`VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY`

Este documento prepara los guardrails pre-implementación de `Validation & Readiness Screen`. No implementa pantalla, no modifica UI activa y no autoriza ejecución. La implementación futura solo podrá comenzar con un prompt posterior y un plan controlado.

## Base y estado recibido

- Base esperada: `4299b0b`.
- Commit local del plan 1.95: `4299b0b`.
- Restore point remoto vigente: `7ad9a8b`.
- Rama: `main`.
- Estado inicial: working tree limpio y `main` ahead de `origin/main` por 1 commit.
- 1.95: `NEXT_SCREEN_VALIDATION_READINESS_SELECTED`.
- Contract Overview / `FSC-CO-01`: baseline visual/contractual 1.
- Blocked & Forbidden / `FSC-BF-02`: baseline visual/contractual 2.
- Request Contract Preview: diferido.
- Push: pospuesto.

## Contrato base Validation & Readiness

La base documental revisada incluye el cierre de gaps menores 1.73/1.74, la auditoría final 1.76, el contrato final 1.77 y el checkpoint publicado 1.78. Esos documentos dejan `Validation & Readiness Screen` como candidato documental listo para guardrails e implementación futura, no como pantalla activa.

La fuente contractual general es `backend_internal_ui_payload.v1`. La superficie futura es `Panel Maestro`, con naturaleza documental, final, contract-aware y read-only. La UI futura solo podrá representar datos declarados; no podrá calcular permisos ni convertir readiness o validation en operación.

## Identidad de pantalla

- Nombre oficial: `Validation & Readiness Screen`.
- Identidad UI propuesta: `FSC-VR-03`.
- `FSC-VR-03` es un identificador operativo propuesto para la futura UI y no se presenta como contrato backend existente.
- Superficie: `Panel Maestro`.
- Fuente: `backend_internal_ui_payload.v1`.
- Estado: documental/read-only, contract-bound y policy-bound.
- Propósito: mostrar validación, readiness, warnings, blockers y estados contractuales sin habilitar ejecución, permisos ni delivery.
- Identidad activa: IA_CORE. Lotería/SAAOP no pueden aparecer como identidad activa.

## Diferenciación frente a los dos baselines

`Contract Overview` resume el mapa contractual general, su identidad, procedencia, readiness contextual y separación entre datos y permisos.

`Blocked & Forbidden` explicita límites duros, `blocked_capabilities`, `forbidden_actions`, no-unlock/no-bypass/no-override y la auditoría anti-CTA.

`Validation & Readiness` explicará preparación y validación documental: qué requisitos están declarados, cuáles faltan, qué warnings existen y por qué un estado no equivale a permiso, ejecución o entrega. No debe duplicar el mapa de Contract Overview ni repetir la pantalla Blocked & Forbidden como una variante de error.

## Separación semántica obligatoria

- `readiness no permission`.
- `validation no execution`.
- `passed no operational success`.
- `warning/error no live runtime`.
- `review required no workflow active`.
- `blocked no broken system`.
- `ready-no-permission no ready-to-run`.
- `valid contract no active operation`.
- `checklist no task runner`.
- `evidence no live log`.

Toda implementación futura debe mostrar estas separaciones cerca de los estados correspondientes. Readiness, validation y delivery no son sinónimos.

## Datos permitidos

- `validation_status` documental.
- `readiness_status` documental.
- `readiness_notes`.
- `blockers`.
- `warnings`.
- `missing_requirements`.
- Contract id y fuente.
- `backend_internal_ui_payload.v1`.
- Scope boundary.
- Evidence snapshot documental.
- `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint`, `no-user-panel`.
- Referencias a Contract Overview y Blocked & Forbidden como baselines.
- Timestamps solo si provienen del documento/payload, etiquetados como snapshot y no como señal viva.
- Status labels contract-bound.
- `review_required` como estado documental, no workflow activo.

## Datos prohibidos

- Secretos, tokens, API keys y credenciales.
- URLs sensibles.
- Runtime handles, job ids, worker ids, queue ids y execution ids reales.
- Live logs, payloads crudos y Package directo al User Panel.
- Resultados de ejecución y métricas runtime inventadas.
- Timestamps vivos inventados.
- `passed`, `ready` o `valid` inventados.
- Mocks que parezcan datos reales.
- Estados o metadata que habiliten acciones.

## Estados permitidos

`documented`, `read-only`, `validation-documented`, `readiness-documented`, `ready-no-permission`, `review-required`, `blocked`, `warning-documented`, `missing-requirement`, `not-available`, `deferred`, `not implemented`, `no-runtime`, `no-execution`, `no-dispatch`, `no-endpoint`, `no-user-panel`, `contract-bound` y `policy-bound`.

## Estados prohibidos

`active`, `running`, `live`, `executing`, `dispatching`, `submitted`, `processing`, `completed operativo`, `success operativo`, `ready to run`, `ready to execute`, `validation passed` como runtime success, `enabled`, `unlocked`, `approved to execute`, `endpoint connected`, `worker active`, `queue active`, `live monitor`, `auto-resolve`, `auto-fix`, `deployment ready` y `publish ready`.

## Acciones UI prohibidas

La futura pantalla no puede ofrecer ejecutar, correr, `run`, `start`, `launch`, `dispatch`, `submit`, enviar, publicar, activar, aprobar ejecución, resolver ahora, `auto-fix`, `retry`, `enable`, `unlock`, `override`, `bypass`, conectar endpoint, enviar a User Panel, marcar como `passed`, marcar como `ready`, iniciar validación runtime, revalidar en vivo, refrescar contra backend, abrir flujo de revisión activo o hacer delivery.

## Copy permitido

El tono debe ser contractual, claro, sereno, educativo, read-only y orientado a estado documental. Debe separar explícitamente readiness/permission y validation/execution, mostrar blockers sin alarmismo, declarar ausencia de habilitación y evitar cualquier promesa de activación o resolución desde la pantalla.

## Copy prohibido

No usar `Ejecutar`, `Correr`, `Run`, `Start`, `Launch`, `Dispatch`, `Submit`, `Enviar`, `Publicar`, `Activar`, `Aprobar ejecución`, `Ready to run`, `Ready to execute`, `Listo para ejecutar`, `Validation success`, `Success`, `Completed`, `Live`, `Running`, `Processing`, `Endpoint connected`, `Worker active`, `Queue active`, `Revalidar en vivo`, `Refresh backend`, `Resolver ahora`, `Auto-fix`, `Enable`, `Unlock`, `Override`, `Bypass`, `User Panel activo`, `Deploy` o `Publish ready` como copy visible de la pantalla.

## Affordances permitidas/prohibidas

Permitidas: labels read-only, disclosures locales no operativos justificados, referencias documentales, chips de estado documental, evidence snapshot colapsable sin fetch/endpoint y notas de revisión documental.

Prohibidas: botones, toggles, refresh que parezca backend, iconos clickeables no explicados, pseudo-botones, hover operativo, links al User Panel, tabs que parezcan iniciar validation, `review required` como flujo accionable y `passed/ready` como CTA implícito.

Toda affordance futura deberá clasificarse como `READ_ONLY_LABEL`, `READ_ONLY_DISCLOSURE`, `LOCAL_INSPECTION_ONLY`, `DOCUMENTATION_REFERENCE`, `NON_OPERATIONAL_STATUS`, `AMBIGUOUS_AFFORDANCE` u `OPERATIONAL_CTA_BLOCKER`. Una affordance ambigua bloquea la salida hasta ser eliminada o documentada como no-operativa.

## Estructura visual futura

La siguiente estructura es un plan, no una implementación:

1. Header con identidad, `FSC-VR-03` propuesto, Panel Maestro y read-only.
2. Status strip documental con readiness, validation y no-permission/no-execution.
3. Bloque readiness vs permission.
4. Bloque validation vs execution.
5. Readiness summary documental.
6. Validation findings.
7. Blockers, warnings y missing requirements siempre visibles.
8. Evidence snapshot documental.
9. Bloque no-runtime/no-execution/no-dispatch.
10. Referencias a Contract Overview y Blocked & Forbidden.
11. Empty/deferred state honesto.
12. Anti-affordance notice y referencias documentales.

La placement strategy futura debe ubicarse después de los dos baselines o en una zona hermana claramente diferenciada, sin reordenarlos ni duplicarlos.

## Visual severity

- `passed` y `ready` no deben usar verde de éxito operativo sin contexto; si aparecen, deben convivir con `no permission` y `documental`.
- `warning` no debe parecer runtime fallando.
- `error` debe etiquetarse como documental o contract-bound cuando exista.
- Blockers deben ser visibles, claros y no alarmistas.
- Readiness debe mostrarse junto a no-permission.
- Validation debe mostrarse junto a no-execution.
- La severidad nunca debe ocultar blockers ni sugerir un siguiente paso operativo.

## Tests futuros mínimos

La futura implementación debe probar existencia y visibilidad de `Validation & Readiness Screen`, `backend_internal_ui_payload.v1`, Panel Maestro, readiness no permission, validation no execution, passed no operational success, warning/error no live runtime, review required no workflow active, blockers/warnings/missing requirements visibles, ausencia de botones operativos, ausencia de ready-to-run, no runtime activo, no execution activo, no dispatch activo, no endpoint/fetch, no User Panel, no rutas/hash, no fake success, no ghost actions, no hidden blockers, no raw package, no identity leakage Lotería/SAAOP, Contract Overview preservado, Blocked & Forbidden preservado, auditoría anti-CTA/anti-affordance, responsive básico, node checks, diff check y backend contract tests aplicables.

## Entry criteria futuro

1.96 debe estar cerrado; working tree limpio; tests 1.96 verdes; 1.95 y 1.94 preservados; operador autoriza continuar; alcance de archivos limitado; no existen gaps P0; y hay restore point remoto previo disponible. 1.97/1.98 no pueden avanzar si falta cualquiera de estas condiciones.

## Exit criteria futuro

La pantalla solo podrá implementarse con prompt explícito. Debe separar readiness de permission, validation de execution, passed de success operativo y warning/error de runtime vivo. Debe tener cero CTAs operativos, cero backend/runtime/endpoints/fetches, revisión visual humana antes del checkpoint y auditoría anti-affordance antes del push. El push solo ocurre en checkpoint.

## Risk register

| Riesgo | Mitigación |
| --- | --- |
| Readiness interpretado como permiso | Copy y estado `readiness no permission`; autoridad backend fuera de UI |
| Validation interpretada como ejecución | `validation no execution`; sin runtime ni jobs |
| Passed interpretado como success operativo | `passed no operational success`; separar delivery |
| Warning/error interpretado como runtime activo | `warning/error no live runtime`; estados documentales |
| Review required interpretado como workflow activo | `review required no workflow active` |
| Ready-no-permission confundido con ready-to-run | Mostrar ambos conceptos separados y prohibir ready-to-run |
| Blockers ocultos por visual positivo | Always-visible, deny-by-default y bloque dedicado |
| Badges verdes ambiguos | Contexto contractual y severidad no operativa |
| Affordance de inspección confundida con acción | Clasificación obligatoria y auditoría anti-CTA |
| Refresh accidental | Solo lectura local explícita; sin refresh backend |
| Endpoint/fetch accidental | Static checks y archivos scoped |
| User Panel leakage | Panel Maestro only y no User Panel |
| Rutas/hash accidentales | Sin router, route, hash o deep link |
| Backend accidental | No tocar API, core, domains, providers ni integraciones |
| Fake success | No inventar passed, ready, valid, métricas o timestamps |
| Ghost actions | No botones, pseudo-botones ni CTA implícito |
| Duplicación con Contract Overview | Contrato general allí; preparación/validación aquí |
| Contradicción con Blocked & Forbidden | Reutilizar límites y mantenerlos visibles |
| Raw package leakage | Solo proyección segura y documental |
| Saltar auditoría anti-affordance | Convertirla en entry/exit criterion obligatorio |
| Push antes de checkpoint | Push prohibido hasta checkpoint completo |

## Decisión final y próximo prompt

`VALIDATION_READINESS_PRE_IMPLEMENTATION_GUARDRAILS_READY`

Próximo prompt exacto:

`PROMPT UI/UX 1.97 - Preparar plan de implementacion controlada Validation & Readiness Screen IA_CORE contract-aware sin runtime/no-execution`

## Límites preservados

En 1.96 no se implementó pantalla, no se modificó UI activa, no se tocó Contract Overview, no se tocó Blocked & Forbidden, no se creó User Panel, no se crearon rutas/hash, endpoints o fetches, y no se activó runtime, execution o dispatch. No se tocó backend/runtime/endpoints/CI/dependencias, no se limpió deuda residual, no se corrigieron pyflakes y no se avanzó a 1.97. No se hace push.

Marcadores literales de límite: no runtime, no execution, no dispatch, no endpoint, no fetch, no User Panel, no rutas/hash, no backend, no CI, no deuda residual, no pyflakes, no se implementó pantalla, no se modificó UI activa, no se tocó Contract Overview, no se tocó Blocked & Forbidden, no se creó User Panel, no se avanzó a 1.97. No se hace push.
