# Sandbox Safe Regeneration 6.2

Estado: `SANDBOX_SAFE_REGENERATION_PASSED`

Veredicto: `SANDBOX_REGENERATION_NO_OPERATIONAL_CONFIRMED`

Readiness: `ready_for_phase_6_3_materialization_audit_pack`

Proximo prompt recomendado: `PROMPT 6.3 - Audit pack y trazabilidad de materializacion sandbox`

## Proposito

Este documento cierra `PROMPT 6.2` validando que IA_CORE puede reconstruir una cadena sandbox completa despues de rollback integral, sin residuos, duplicados ni activacion operativa.

## Relacion Con 6.0

`PROMPT 6.0` valido la cadena sandbox completa: `domain sandbox -> artifact_manifest -> profile_catalog -> agent_presets -> paper_seed -> sandbox agents -> sandbox team -> team read model`.

## Relacion Con 6.1

`PROMPT 6.1` definio rollback integral basado en `artifact_manifest`, `created_paths` y `sandbox_root` controlado. `PROMPT 6.2` reutiliza ese rollback como precondicion de regeneracion segura.

## Contrato De Regeneracion Segura

El contrato queda definido en `core/domain_materialization_rollback.py` mediante:

- `regenerate_sandbox_domain_after_integral_rollback()`
- `validate_sandbox_domain_safe_regeneration_result()`
- `compare_sandbox_domain_materializations()`

El ciclo validado es:

`materializar -> rollback integral -> regenerar -> reconstruir cadena sandbox -> comparar estructura`

## Ciclo Validado

1. Materializa cadena sandbox completa bajo `tmp_path`.
2. Captura snapshot estructural inicial.
3. Ejecuta rollback integral 6.1.
4. Confirma limpieza post-rollback.
5. Regenera dominio sandbox con nuevo `materialization_id`.
6. Reconstruye profile catalog, agent presets, paper seed, sandbox agents y sandbox team.
7. Valida team read model regenerado.
8. Compara primera materializacion y regeneracion.

## Que Se Compara

- identidad logica del dominio;
- familia de artefactos;
- cantidad de artefactos;
- `artifact_type`;
- `artifact_kind`;
- dependencies;
- read model shape;
- flags no-operativas;
- ausencia de duplicados.

## Que Puede Cambiar

- `materialization_id`;
- timestamps;
- `regeneration_id`;
- paths re-creados despues de rollback;
- registros nuevos de `_rollback_records`.

## Que Debe Permanecer Equivalente

- `domain_id`;
- estructura de artifacts;
- `artifact_manifest` valido;
- lineage/dependencies;
- read model interno;
- `operational=false`;
- `passed=false`;
- `runtime_enabled=false`;
- `execution_enabled=false`;
- `tool_execution_enabled=false`;
- `model_invocation_enabled=false`;
- `external_integrations_enabled=false`.

## Seguridad De Paths

La regeneracion solo opera bajo `sandbox_root` controlado. Antes de regenerar, bloquea residuos no declarados dentro del dominio sandbox y reutiliza los bloqueos de 6.1 para repo root, `domains/` operativo, `.git/`, `core/`, `docs/`, `tests/`, `agents/`, path traversal, globs y symlink escapes.

## Uso De Rollback Integral

La regeneracion segura no pisa una materializacion existente. Primero ejecuta rollback integral validado y solo despues crea una nueva materializacion.

## Uso De Artifact Manifest Y Created Paths

`artifact_manifest` y `created_paths` siguen siendo la fuente para decidir limpieza previa y detectar residuos. La cadena regenerada vuelve a producir manifests validos.

## No-Operatividad Post-Regeneracion

La regeneracion no activa runtime, execution, dry-run real, tools, modelos, contexto operativo, output delivery, UI, integraciones, stores/memory operativos, Market Catalog runtime, Business Composition Layer runtime ni OBLITERATUS.

## Manejo De Residuos

Si existe un archivo no declarado dentro del dominio sandbox previo, la regeneracion falla con error controlado `residual_paths_detected` y no borra ese residuo.

## Duplicados Bloqueados

Una materializacion nueva sobre el mismo `sandbox_root` sin rollback previo queda bloqueada por el materializador. La comparacion estructural tambien detecta artifact ids duplicados.

## Errores Esperados

- rollback incompleto o sin `artifact_manifest`;
- manifest inconsistente;
- path residual no declarado;
- duplicados de artifact ids;
- flags operativas alteradas.

## Fuera De Alcance

- audit pack 6.3;
- runtime real;
- execution real;
- dry-run real operativo;
- tools/model invocation;
- context injection;
- output delivery;
- UI/UX;
- integraciones;
- Market Catalog runtime;
- Business Composition Layer runtime;
- OBLITERATUS;
- raw Package directo a User Panel.

## Riesgos

- confundir regeneracion con continuidad de ejecucion;
- exigir igualdad bit a bit aunque cambien ids y timestamps;
- regenerar encima de residuos;
- duplicar artifacts sin pasar por rollback integral.

## Veredicto

`SANDBOX_SAFE_REGENERATION_PASSED`

`SANDBOX_REGENERATION_NO_OPERATIONAL_CONFIRMED`

`structural_match=true`

## Readiness

`ready_for_phase_6_3_materialization_audit_pack`

## Proximo Prompt Recomendado

`PROMPT 6.3 - Audit pack y trazabilidad de materializacion sandbox`
