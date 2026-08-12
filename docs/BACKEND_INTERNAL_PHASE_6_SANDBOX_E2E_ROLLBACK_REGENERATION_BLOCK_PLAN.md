# Backend Interno Phase 6 Sandbox E2E Rollback Regeneration Block Plan

Estado: `NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED`

Veredicto: `NEXT_ARCHITECTURE_BLOCK_SELECTED`

Readiness: `ready_for_phase_6_sandbox_e2e_checkpoint`

Proximo prompt exacto: `PROMPT 6.0 - Validacion end-to-end sandbox completa`

Compatibilidad de nombre: `PROMPT 6.0 — Validación end-to-end sandbox completa`

## Proposito Del Bloque

Fase 6 valida la cadena sandbox end-to-end despues del cierre minimo de Fase 5. Su proposito es comprobar, con evidencia reutilizable del repo, que IA_CORE puede recorrer preview, schema, materializacion, artefactos derivados, agentes sandbox, equipos sandbox, manifest, rollback, regeneracion y lectura interna sin activar runtime real.

Fase 6 no abre runtime, no ejecuta agentes, no crea UI, no crea integraciones y no convierte equipos sandbox en equipos operativos.

## Estado Previo Heredado De Fases 0-5

- Fase 0 fijo contratos derivados vs operativos, estados internos y preview antes de materializacion.
- Fase 1 materializo dominio sandbox con rollback y regeneracion de dominio.
- Fase 2 materializo artefactos derivados: `profile_catalog`, `agent_presets`, `paper_seed`, agentes sandbox y equipos historicos.
- Fase 3 y Fase 4 mantuvieron runtime, execution, dry-run real, stores operativos, tools, modelos, contexto, outputs, UI e integraciones bloqueados.
- Fase 5 cerro el bloque minimo de equipos reales sandbox: schema, materializacion declarativa desde `team_template`, auditoria y read model interno.

## Que Ya Existe

| Pieza | Clasificacion | Uso En Fase 6 |
|---|---|---|
| `core/sandbox_lifecycle_validation.py` | vigente reutilizable | Base para lifecycle de dominio: preview, materializacion, rollback y regeneracion. |
| `core/domain_materialization_rollback.py` | vigente reutilizable | Rollback seguro e idempotente de dominio sandbox. |
| `tests/test_sandbox_lifecycle.py` | vigente reutilizable | Evidencia de lifecycle de dominio sin tocar `domains/`. |
| `tests/test_domain_materialization_rollback.py` | vigente reutilizable | Evidencia de rollback seguro y proteccion de `domains/` operativo. |
| `tests/test_sandbox_chain_checkpoint.py` | parcial a extender | Cadena minima hasta agente sandbox, rollback selectivo y total. |
| `tests/test_sandbox_chain_maximum_checkpoint.py` | parcial a extender | Stress acotado 12 dominios; util como antecedente de escala, no como Fase 6 completa. |
| `tests/test_sandbox_chain_with_team_checkpoint.py` | vigente reutilizable | Mejor base actual para 6.0: cadena completa con `sandbox_team`, rollback selectivo/total y regeneracion de equipo. |
| `docs/SANDBOX_TEAM_CHAIN_CHECKPOINT.md` | documento de antecedente | Documenta checkpoint con equipo y `PASSED_TEAM_CHAIN`. |
| `docs/SANDBOX_LIFECYCLE.md` | documento de antecedente | Documenta lifecycle inicial de dominio y sus limites. |
| `docs/SANDBOX_ARCHITECTURE_AUDIT.md` | historico compatible | Explica huecos antiguos; debe leerse como antecedente, no como estado final despues de Fase 5. |
| `tests/test_sandbox_chain_full_benchmark.py` | fixture/benchmark largo | No debe entrar en suite rapida; usar solo bajo politica de suite larga. |

## Que Falta

- Reconciliar la cadena historica `domain -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agents -> sandbox_team` con el read model de Fase 5.
- Confirmar que el checkpoint de equipo no duplica el nuevo contrato `core/sandbox_team_read_model.py`.
- Definir evidencia formal de que rollback selectivo y rollback total siguen funcionando despues de Fase 5.
- Confirmar regeneracion segura para dominio/equipo sin sobrescritura destructiva.
- Clasificar claramente benchmark largo como validacion opcional, no como requisito de cada prompt.
- Producir reporte o checkpoint Fase 6 sin activar runtime ni ejecutar agentes.

## Que NO Debe Hacerse

- No implementar runtime real.
- No ejecutar agentes ni equipos.
- No crear agentes nuevos.
- No crear equipos nuevos persistentes.
- No crear un segundo `sandbox_chain` paralelo.
- No crear UI, endpoints publicos ni integraciones.
- No invocar modelos ni llamar tools.
- No escribir en `domains/` operativo.
- No habilitar Market Catalog runtime.
- No habilitar Business Composition Layer runtime.
- No incorporar OBLITERATUS.

## Riesgos Principales

- Duplicar checkpoints existentes en vez de extenderlos.
- Confundir E2E sandbox con runtime operativo.
- Tratar rollback de test como rollback productivo.
- Ejecutar benchmark largo dentro de una suite focal sin presupuesto.
- Reabrir decisions historicas de `artifact_type: team` vs `artifact_kind: sandbox_team`.
- Exponer raw Package directo al User Panel antes del contrato backend/UI.

## Dependencias

- `PROMPT 5.3` cerrado formalmente en commit `495670f5`.
- `SANDBOX_TEAM_READ_MODEL_READY`.
- `SANDBOX_TEAM_INTERNAL_LISTING_NO_OPERATIONAL_CONFIRMED`.
- `ready_for_next_architecture_block_after_phase_5`.
- Checkpoints 4.8 y 4.9 verdes.
- Tests de equipo sandbox verdes: schema, materializacion, auditoria y read model.

## Subprompts Probables

1. `PROMPT 6.0 - Validacion end-to-end sandbox completa`
2. `PROMPT 6.1 - Rollback integral de dominio sandbox completo`
3. `PROMPT 6.2 - Regeneracion segura sandbox completa`
4. `PROMPT 6.3 - Audit pack / trazabilidad de materializacion`
5. `PROMPT 6.4 - Checkpoint integral Fase 6`

Compatibilidad de nombres:

1. `PROMPT 6.0 — Validación end-to-end sandbox completa`
2. `PROMPT 6.1 — Rollback integral de dominio sandbox completo`
3. `PROMPT 6.2 — Regeneración segura sandbox completa`
4. `PROMPT 6.3 — Audit pack / trazabilidad de materialización`
5. `PROMPT 6.4 — Checkpoint integral Fase 6`

## Tests Esperados

- Test de planificacion 5.4.
- Tests focales de Fase 5.
- Checkpoints 4.8 y 4.9.
- Reutilizacion/extension de `tests/test_sandbox_chain_with_team_checkpoint.py`.
- Reutilizacion/extension de `tests/test_sandbox_lifecycle.py`.
- Reutilizacion/extension de `tests/test_domain_materialization_rollback.py`.
- Suite larga o validacion equivalente por bloques segun `docs/LONG_TEST_SUITE_VALIDATION_POLICY.md`.

## Criterios De Cierre De Fase 6

Fase 6 cierra cuando exista evidencia de:

- cadena sandbox completa validada despues de Fase 5;
- rollback selectivo validado por dependencias;
- rollback total validado sin residuos;
- regeneracion segura validada;
- manifest y lineage coherentes;
- read model de equipo consumible en la cadena;
- errores legibles para casos negativos;
- no modificacion de `domains/`, `agents/`, `catalogs/` ni papers globales;
- runtime, execution, dry-run real, tools, modelos, UI e integraciones bloqueados.

## Restricciones De No-Operatividad

Runtime, execution, dry-run real, tools, model invocation, context injection, output delivery, writes/stores/memory operativos, network, browser, filesystem runtime, env, secrets, API runtime, UI runtime, UI-device control, integrations, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo a User Panel permanecen bloqueados.

## Relacion Con Runtime Execution Preparation

Runtime Execution Preparation cerro un bloque no-operativo de preparation/package/read model/projection. Fase 6 no consume ese bloque para activar runtime. Solo conserva sus restricciones: preparar evidencia y contracts sin abrir ejecucion real.

## Relacion Con Futuro Contrato Backend Para UI

Fase 6 prepara evidencia para Fase 7. La UI futura no debe inferir rollback, regeneracion, estados ni next actions. Fase 6 debe producir una base validada que luego pueda exponerse por contrato backend/UI, pero no crea ese contrato ni endpoints.

## Evaluacion De Subprompt Intermedio

- Fase 5 quedo suficientemente cerrada: si.
- El read model de equipos no necesita refuerzo previo a 6.0: si, pasa tests y es read-only.
- `artifact_manifest` quedo suficientemente fuerte para iniciar un E2E completo: si, aunque Fase 6 debe auditar dependencias integrales.
- El chain checkpoint existente ya cubre parte de 6.0: si, especialmente `tests/test_sandbox_chain_with_team_checkpoint.py`.
- Hay riesgo de duplicar `sandbox_chain`: si; 6.0 debe reutilizar o extender lo existente.
- Hace falta subprompt 5.4.1 antes de 6.0: no. La planificacion deja readiness directa a 6.0.

## Veredicto De Readiness

`NEXT_ARCHITECTURE_BLOCK_PLANNING_COMPLETED`

`NEXT_ARCHITECTURE_BLOCK_SELECTED`

`ready_for_phase_6_sandbox_e2e_checkpoint`

## Proximo Prompt Exacto

`PROMPT 6.0 - Validacion end-to-end sandbox completa`

Compatibilidad de nombre esperado:

`PROMPT 6.0 — Validación end-to-end sandbox completa`
