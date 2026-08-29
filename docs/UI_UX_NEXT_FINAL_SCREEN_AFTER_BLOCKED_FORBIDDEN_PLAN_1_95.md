# UI/UX Next Final Screen After Blocked & Forbidden Plan 1.95

## Decision

`NEXT_SCREEN_VALIDATION_READINESS_SELECTED`

1.95 planifica el siguiente Final Screen Contract después del cierre publicado de Blocked & Forbidden. No implementa pantalla, no modifica UI activa y no avanza al prompt siguiente.

## Base y estado recibido

- Base esperada: `7ad9a8b`.
- Restore point remoto vigente: `7ad9a8b`.
- `main` está sincronizado con `origin/main` y el working tree estaba limpio.
- 1.94 cerró `Blocked & Forbidden Capabilities Screen / FSC-BF-02` como implementada, hardenizada, aprobada visualmente y auditada.
- Auditoría 1.94: `READ_ONLY_AFFORDANCE_AUDIT_PASSED_WITH_NOTES`.
- Revisión visual: `HUMAN_VISUAL_REVIEW_APPROVED`.
- Contract Overview / `FSC-CO-01` permanece como baseline visual/contractual 1.
- Blocked & Forbidden / `FSC-BF-02` queda como baseline visual/contractual 2.

## Secuencia histórica

La secuencia 1.81/1.82 se mantiene sin contradicción:

1. Contract Overview.
2. Blocked & Forbidden.
3. Validation & Readiness.

`Request Contract Preview` permanece diferido y no se elige como próximo corte.

## Candidatas

| Candidata | Valor | Riesgos | Esfuerzo | Decisión |
| --- | --- | --- | --- | --- |
| Validation & Readiness Screen | Explica validación, readiness, flags, blockers, warnings y estado contractual apoyándose en los dos baselines cerrados | Readiness puede parecer permiso; validation puede parecer ejecución; `ready`, `passed`, `valid`, `warning`, `error` y `review required` pueden parecer runtime, resultado o CTA | Medio/alto; requiere guardrails dedicados y auditoría anti-affordance desde el inicio | Seleccionada |
| Request Contract Preview | Permitiría documentar el draft de request | Sigue demasiado cerca de submit, dispatch, permisos y mutación; mantiene riesgo de CTA ghost | Alto bajo el contrato actual | Diferida |
| Auditoría/preflight adicional | Reduciría incertidumbre si apareciera un blocker nuevo | No existe blocker nuevo en 1.94; repetir auditoría sin señal concreta no agrega valor suficiente | Bajo, pero no desbloquea una pantalla | No necesaria como bloque separado |

## Matriz de decisión

| Criterio | Validation & Readiness | Request Contract Preview | Auditoría/preflight adicional |
| --- | --- | --- | --- |
| Readiness documental | Alto, es su propósito | Bajo/indirecto | Medio |
| Dependencia con Contract Overview | Directa: reutiliza jerarquía y separación readiness/permission | Baja | Indirecta |
| Dependencia con Blocked & Forbidden | Directa: blockers y límites deben permanecer visibles | Alta, pero puede mezclar límites con request | Indirecta |
| Riesgo de ghost actions | Alto | Muy alto | Bajo |
| Confusión con permiso operativo | Muy alto | Muy alto | Bajo |
| Apariencia de runtime | Alto | Alto | Bajo |
| Apariencia de resultado de ejecución | Alto para `passed`/`valid` | Muy alto para preview/submit | Bajo |
| Valor para claridad contractual | Alto | Medio | Bajo/medio |
| Esfuerzo de implementación | Medio/alto | Alto | Bajo |
| Necesidad de guardrails | Muy alta | Muy alta | Media |
| Auditoría anti-affordance | Obligatoria desde guardrails | Obligatoria y más restrictiva | Recomendable |
| Compatibilidad con baseline visual | Alta si evita copiar contenido | Media | Alta |
| Conveniencia como próximo paso | Alta | Baja | Baja |

Marcadores literales del plan: auditoría/preflight adicional, auditoría anti-CTA/anti-affordance, no runtime y no backend.

## Justificación

Se elige `Validation & Readiness Screen` porque, después de hacer visible el contrato general y cerrar los límites duros, recién existe contexto suficiente para explicar readiness y validation sin conceder permisos. La selección no autoriza implementación: primero requiere guardrails pre-implementación específicos y una separación explícita entre readiness, permission, validation, execution y delivery.

## Secuencia futura propuesta

- 1.96: Preparar guardrails pre-implementacion Validation & Readiness Screen.
- 1.97: Preparar plan de implementacion controlada Validation & Readiness Screen.
- 1.98: Implementar Validation & Readiness Screen.
- 1.99: Hardening visual y contractual Validation & Readiness Screen.
- 1.100: Checkpoint Validation & Readiness Screen implementada y hardenizada.

Estos prompts no se ejecutan en 1.95.

## Baselines reutilizables

De Contract Overview se reutilizan la jerarquía documental, status strip, identidad contractual, evidence snapshot, separación readiness vs permission, ausencia de CTAs operativos y revisión visual humana antes del checkpoint.

De Blocked & Forbidden se reutilizan los límites primarios visibles, no-unlock/no-bypass/no-override, severidad contractual no alarmista, auditoría anti-CTA/anti-affordance, clasificación de elementos read-only y push solo en checkpoint.

Del método general se reutilizan no push hasta checkpoint, tests por bloque, documentación por bloque, commit local por prompt y revisión visual humana.

## Baseline no reutilizable

No se copia contenido textual exacto si produce redundancia, estilo que parezca error, badges que parezcan runtime, botones/pseudo-botones ambiguos, navegación nueva, rutas/hash, runtime/fetch/endpoints, `ready to run` ni ninguna affordance operativa.

## Guardrails especiales para Validation & Readiness

- `readiness no permission`.
- `validation no execution`.
- `passed no operational success`.
- `warning/error no live runtime`.
- `review required no workflow active`.
- Readiness, validation y delivery deben ser estados documentales, no permisos.
- `blocked_capabilities` y `forbidden_actions` deben permanecer visibles aun con estados positivos.
- No runtime, no execution, no dispatch, no endpoint, no fetch, no User Panel y no rutas/hash.
- No backend, no CI, no deps, no deuda residual y no pyflakes.
- Auditoría anti-CTA/anti-affordance obligatoria antes de implementar.
- Todo control de lectura debe declararse local, read-only, sin cambio de permisos y sin ocultar blockers.
- Ningún `ready`, `passed`, `valid`, `warning`, `error` o `review required` puede ser CTA implícito.

## Risk register

| Riesgo | Mitigación requerida |
| --- | --- |
| Readiness interpretado como permiso | Etiqueta y copy explícitos: readiness no permission; backend conserva autoridad |
| Validation interpretada como ejecución | validation no execution; sin runtime, job, worker o dispatcher |
| Passed interpretado como éxito operativo | passed no operational success; separar validación de delivery |
| Warning/error interpretado como runtime activo | warning/error no live runtime; usar estados documentales |
| Blockers ocultos por visual positivo | blocked/forbidden always-visible y deny-by-default |
| `ready` usado como CTA implícito | `ready` solo como dato contractual, nunca botón o enlace |
| `review required` usado como flujo operativo | review required no workflow active; solo estado documental |
| Affordances de inspección confundidas con acciones | Auditoría anti-CTA; disclosures locales y clasificación explícita |
| Duplicación con Contract Overview | Contract Overview resume el mapa; Validation & Readiness explica estados y evidencia |
| Contradicción con Blocked & Forbidden | Reusar límites y no-unlock/no-bypass/no-override sin reinterpretarlos |
| Fake success | Prohibir métricas/resultados inventados y separar validación de ejecución |
| Ghost actions | Sin submit, dispatch, execute, unlock, override, bypass, activate o enable |
| Endpoint/fetch accidental | Archivos y guardrails scoped; static checks de no endpoint/no fetch |
| User Panel leakage | Panel Maestro only y sin User Panel |
| Ruta/hash accidental | Navegación documental local, sin rutas/hash |
| Backend accidental | No tocar backend, API, core, domains, providers, tools ni integraciones |
| Push antes de checkpoint | Push pospuesto hasta checkpoint y auditoría completa |
| No aplicar auditoría anti-affordance | Criterio de salida obligatorio en cada prompt futuro |

## Límites preservados

En 1.95 no se implementó pantalla, no se modificó UI activa, no se tocó Contract Overview, no se tocó Blocked & Forbidden, no se creó User Panel, ruta/hash, endpoint o fetch, y no se activó runtime, execution o dispatch. No se tocó backend, CI o dependencias, no se limpió deuda residual, no se corrigió pyflakes y no se avanzó al prompt siguiente.

No se hace push por defecto en este prompt.

## Próximo prompt exacto

`PROMPT UI/UX 1.96 - Preparar guardrails pre-implementacion Validation & Readiness Screen IA_CORE contract-aware sin runtime/no-execution`

Todavía no implementar Validation & Readiness directamente. Primero debe ejecutarse el bloque de guardrails 1.96; Contract Overview y Blocked & Forbidden quedan como baseline visual/contractual doble.
