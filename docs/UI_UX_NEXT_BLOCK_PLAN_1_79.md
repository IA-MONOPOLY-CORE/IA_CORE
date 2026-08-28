# UI/UX Next Block Plan 1.79 — Post Global Technical Debt Cleanup

## Commit Base

- Base esperada: `605bad2`.
- Restore point remoto vigente: `bb4852e`.
- Readiness base: `IA_CORE_TECH_DEBT_RESIDUAL_READINESS_AUDIT_1_78_K`.
- Rama esperada: `main`.
- Remoto esperado: `origin https://github.com/IA-MONOPOLY-CORE/IA_CORE`.
- Estado esperado al iniciar: working tree limpio y `main` ahead de `origin/main` por el commit local 1.78.K.

## Objetivo

1.79 consolida el siguiente bloque UI/UX despues de la limpieza tecnica global. Este documento revisa contratos finales, deuda residual, readiness, candidatos posibles, limites contract-aware y decide el proximo bloque exacto sin ejecutar la secuencia futura.

1.79 es planificacion documental. No se implemento pantalla. No se modifico UI activa. No se creo User Panel. No se tocaron backend/runtime/endpoints/CI/dependencias. No se limpio deuda residual.

## Estado Recibido

- Decision 1.78.K: `READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT`.
- Pyflakes residual: `18`.
- Diagnosticos que bloquean 1.79: `0`.
- Diagnosticos que no bloquean 1.79: `18`.
- Deuda residual: documentada, protegida y diferida para revision futura.
- Restore point remoto vigente: `bb4852e`.
- local ahead por commit 1.78.K: `605bad2 docs(core): auditar readiness deuda residual`.
- Suite historica verde desde checkpoint previo: `5465 passed`, `2 skipped`, `5 warnings`.
- Fallos historicos eliminados: `22`.
- Pyflakes global reducido: `65 -> 26 -> 18`.
- UI activa intacta.
- Backend operativo intacto.
- Runtime/endpoints/CI/dependencias intactos.
- No hay User Panel.
- 1.78.K no avanzo a 1.79.

## Alcance

- Planificacion UI/UX.
- Consolidacion de estado post limpieza tecnica global.
- Revision de Final Screen Contracts ya cerrados.
- Evaluacion comparativa de candidatos de proximo bloque.
- Seleccion de un unico proximo bloque UI/UX.
- Secuencia sugerida 1.80 -> 1.82.
- Test documental de 1.79.
- Actualizacion de README/cursor si corresponde.
- Sin implementacion.

## No-Scope

- No pantalla.
- No UI activa.
- No User Panel.
- No endpoints.
- No runtime.
- No execution.
- No dispatch.
- No rutas/hash.
- No fetches.
- No backend operativo.
- No limpieza deuda.
- No pyflakes.
- No CI/dependencias.
- No push.

Marcadores de cierre:

- No se implemento pantalla.
- No se modifico UI activa.
- No se creo User Panel.
- No se tocaron backend/runtime/endpoints/CI/dependencias.
- No se limpio deuda residual.

## Estado De Final Screen Contracts

Los tres Final Screen Contracts existentes estan cerrados como documentos y checkpoints. Ninguno esta implementado como pantalla activa.

| Final Screen Contract | Estado | Implementacion | Limite principal |
|---|---|---|---|
| `Contract Overview Final Screen Contract` | Documental cerrado y checkpointed en 1.65/1.66 | No implementado | `allowed_actions` como datos; `forbidden_actions` y `blocked_capabilities` visibles; no endpoint/fetch/runtime |
| `Blocked & Forbidden Final Screen Contract` | Documental cerrado y checkpointed en 1.69/1.70 | No implementado | blocked/forbidden visibles; no unlock, override, bypass ni permission escalation |
| `Validation & Readiness Final Screen Contract` | Documental cerrado y checkpointed en 1.77/1.78 | No implementado | `validation.valid=true` no implica safe-to-execute; ready no significa permiso; allowed_actions no son CTAs |

`Request Contract Preview` sigue diferido. Su riesgo principal es parecer submit/dispatch si se planifica antes de fijar un orden de implementacion y una checklist visual/read-only para los contratos finales existentes.

Relacion con future screens: los contratos existentes son base interna del Panel Maestro. Future screens siguen no implementadas, User Panel sigue fuera de alcance y cualquier variante user-safe futura requiere contrato separado.

## Candidate Matrix

| Candidato | Valor | Riesgo | Dependencias | Requiere implementacion | Toca UI activa | Toca backend | Toca endpoint/runtime | Compatibilidad con deuda residual | Recomendacion |
|---|---|---|---|---|---|---|---|---|---|
| `Request Contract Preview Final Contract Readiness` | Alto para cerrar el cuarto candidato historico | Alto: puede confundirse con submit/dispatch o draft operativo | Separacion fuerte de preview vs request real | No | No | No | No | Compatible si queda documental | Diferir hasta tener readiness de implementacion de contratos existentes |
| `Existing Final Screen Contracts Implementation Readiness` | Muy alto: prepara pasar de contratos documentales a futura implementacion sin saltos | Bajo/medio: sigue sin implementar y ordena riesgos antes de tocar UI | Tres Final Screen Contracts cerrados y 1.78.K ready | No | No | No | No | Compatible: los 18 pyflakes no bloquean este bloque documental | Seleccionar |
| `Final Screen Contracts Integration Plan` | Alto para navegacion futura entre contratos | Medio: puede acercarse a rutas/hash prematuras | Readiness de implementacion previo seria util | No | No | No | No | Compatible | Postergar despues de readiness de implementacion |
| `Residual Debt Acceptance Gate` | Medio: refuerza deuda no bloqueante | Bajo | 1.78.K ya cumple el gate | No | No | No | No | Compatible | No seleccionar; seria redundante ahora |
| `Contract-First Screen Implementation Plan` | Alto para preparar primera pantalla concreta | Medio/alto: puede saltar a implementacion antes de criterios visuales y orden de set | Requiere readiness de implementacion del set existente | No | No | No | No | Compatible si documental | Postergar hasta despues de readiness del set |
| `Panel Maestro Future Screen Roadmap` | Medio/alto para roadmap amplio | Medio: puede mezclar User Panel o pantallas futuras demasiado pronto | Boundaries Panel Maestro/User Panel y contratos finales existentes | No | No | No | No | Compatible | Postergar; mantener User Panel fuera |

## Decision

Decision unica:

`NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS`

## Justification

La decision correcta ahora es consolidar readiness de implementacion de los tres Final Screen Contracts existentes. 1.78.K habilito retomar UI/UX con deuda residual documentada y no bloqueante, pero no autorizo implementar pantalla. El estado actual tiene mas valor si primero define orden, limites visuales, checklist contract-aware, criterios de lectura read-only, pruebas esperadas y primer candidato implementable.

Este bloque reduce el riesgo de convertir `allowed_actions` en CTAs, ocultar `forbidden_actions` o `blocked_capabilities`, transformar readiness en permiso operativo, crear rutas/hash por conveniencia o abrir User Panel por fuga de alcance. Tambien deja `Request Contract Preview` diferido hasta que la implementacion de contratos existentes tenga un marco claro.

## Recommended Sequence

1. `PROMPT UI/UX 1.80 - Auditar readiness de implementacion de Final Screen Contracts existentes IA_CORE contract-aware sin runtime/no-execution`
2. `PROMPT UI/UX 1.81 - Documentar readiness de implementacion de Final Screen Contracts existentes IA_CORE contract-aware sin runtime/no-execution`
3. `PROMPT UI/UX 1.82 - Checkpoint readiness de implementacion de Final Screen Contracts existentes IA_CORE contract-aware sin runtime/no-execution`

La secuencia sugerida no se ejecuta en 1.79.

## Guardrails

- No runtime.
- No execution.
- No dispatch.
- No endpoints.
- No fetches.
- No rutas/hash.
- No User Panel.
- No ghost CTAs.
- No active actions fuera de `allowed_actions`.
- `allowed_actions` son datos backend-declared, no autoridad UI.
- `blocked_capabilities` visibles.
- `forbidden_actions` visibles.
- `Validation & Readiness` no convierte `valid=true` en safe-to-execute.
- `ready` no significa permiso operativo.
- IA_CORE identidad activa.
- SAAOP/Loteria/Tactical HUD/U-Score no son UI activa.
- Deuda residual documentada.

## Risks

- Implementar demasiado pronto.
- Tocar UI activa sin plan.
- Reabrir deuda tecnica.
- Confundir final-documental con pantalla activa.
- `Request Contract Preview` puede parecer submit/dispatch.
- User Panel leakage.
- Endpoint/fetch leakage.
- Route/hash leakage.
- CTA ghost desde `allowed_actions`.
- Ocultar `blocked_capabilities` o `forbidden_actions` en layouts compactos.

## Proximo Prompt Exacto

`PROMPT UI/UX 1.80 - Auditar readiness de implementacion de Final Screen Contracts existentes IA_CORE contract-aware sin runtime/no-execution`

## Veredictos

- `UI_UX_NEXT_BLOCK_PLAN_1_79_COMPLETED`
- `POST_GLOBAL_TECH_DEBT_CLEANUP_STATE_REVIEWED`
- `READY_TO_RESUME_UI_UX_1_79_WITH_DOCUMENTED_RESIDUAL_DEBT_CONFIRMED`
- `PYFLAKES_REMAINING_18_NON_BLOCKING_CONFIRMED`
- `BLOCKING_DIAGNOSTICS_FOR_1_79_ZERO_CONFIRMED`
- `FINAL_SCREEN_CONTRACTS_THREE_DOCUMENTAL_CONFIRMED`
- `REQUEST_CONTRACT_PREVIEW_DEFERRED_CONFIRMED`
- `CANDIDATE_MATRIX_CREATED`
- `NEXT_BLOCK_EXISTING_FINAL_SCREEN_CONTRACTS_IMPLEMENTATION_READINESS_SELECTED`
- `NO_SCREEN_IMPLEMENTED_CONFIRMED`
- `NO_ACTIVE_UI_CHANGE_CONFIRMED`
- `NO_USER_PANEL_CONFIRMED`
- `NO_BACKEND_RUNTIME_ENDPOINTS_CI_DEPENDENCIES_CHANGE_CONFIRMED`
- `NO_RESIDUAL_DEBT_CLEANUP_CONFIRMED`
- `PUSH_POSTPONED_CONFIRMED`