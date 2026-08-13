# Sandbox Integral Rollback 6.1

Estado: `SANDBOX_INTEGRAL_ROLLBACK_PASSED`

Veredicto: `SANDBOX_ROLLBACK_IDEMPOTENT_CONFIRMED`

Readiness: `ready_for_phase_6_2_safe_regeneration`

Proximo prompt recomendado: `PROMPT 6.2 - Regeneracion segura sandbox completa`

## Proposito

Este documento cierra `PROMPT 6.1` validando rollback integral de un dominio sandbox completo materializado con la cadena E2E de 6.0. El rollback opera solo sobre paths declarados por manifests, bajo `sandbox_root` controlado y sin activar runtime ni borrar activos operativos.

## Relacion Con 6.0

`PROMPT 6.0` valido la cadena `domain sandbox -> artifact_manifest -> profile_catalog -> agent_presets -> paper_seed -> sandbox agents -> sandbox team -> team read model`. `PROMPT 6.1` toma esa misma cadena y valida que pueda revertirse de forma segura, trazable e idempotente.

## Piezas Reutilizadas

- `core/domain_materialization_rollback.py`
- `core/domain_materializer.py`
- `core/artifact_manifest_schema.py`
- `core/profile_catalog_materializer.py`
- `core/agent_preset_materializer.py`
- `core/paper_seed_materializer.py`
- `core/sandbox_agent_materializer.py`
- `core/sandbox_team_materializer.py`
- `core/sandbox_team_read_model.py`
- `tests/test_sandbox_end_to_end_full_checkpoint_6_0.py`
- `tests/test_domain_materialization_rollback.py`

## Contrato De Rollback Integral

El contrato queda definido en `core/domain_materialization_rollback.py` mediante:

- `build_sandbox_domain_integral_rollback_plan()`
- `validate_sandbox_domain_integral_rollback_plan()`
- `rollback_sandbox_domain_integral()`
- `validate_sandbox_domain_integral_rollback_result()`

El contrato declara `operational=false`, `runtime_enabled=false` y `execution_enabled=false`.

## Rollback Plan

El rollback plan incluye `domain_id`, `materialization_id`, `rollback_id`, `rollback_scope=sandbox_domain_integral`, `sandbox_root`, `manifest_path`, `artifact_manifest_path`, `planned_paths`, `removed_paths`, `preserved_paths`, `skipped_paths`, `blocked_paths`, `validation`, `idempotent`, `operational=false`, `runtime_enabled=false`, `execution_enabled=false` y `warnings`.

## Seguridad De Paths

El plan bloquea cualquier path fuera de `sandbox_root`, `domains/` operativo, repo root, `.git/`, `core/`, `docs/`, `tests/`, `agents/`, `memoria_agentes/` fuera de temporales permitidos, path traversal, globs destructivos y symlink/path resuelto fuera del sandbox.

## Uso De Artifact Manifest Y Created Paths

El rollback integral combina `created_paths` del `materialization_manifest.json` con `rollback_info.created_paths` de cada artifact del `artifact_manifest`. Solo esos paths declarados entran en `planned_paths`.

## Idempotencia

La primera ejecucion elimina los paths declarados y registra reporte en `_rollback_records`. La segunda ejecucion no borra nada nuevo, reporta paths ya ausentes como `skipped_paths` y devuelve `already_rolled_back_integral`.

## Que Elimina

- `domain.json`
- `materialization_manifest.json`
- `manifests/artifact_manifest.json`
- `profile_catalog`
- `agent_presets`
- `paper_seed`
- `sandbox_agents`
- `sandbox_teams`
- manifests secundarios declarados
- directorio del dominio sandbox temporal cuando corresponde

## Que Preserva

- archivos no declarados fuera del dominio sandbox dentro de la raiz temporal;
- `_rollback_records`;
- `domains/` operativo;
- repo root;
- `core/`, `docs/`, `tests/`, `.git/`;
- memoria/stores operativos;
- UI e integraciones.

## Que Bloquea

- manifest inconsistente;
- missing `artifact_manifest`;
- `created_paths` vacio;
- path fuera de sandbox;
- path a `domains/` operativo;
- path traversal;
- symlink escape si el entorno lo permite;
- path no declarado para borrado.

## Reporte De Rollback

El reporte es JSON-safe, no contiene secretos, env, runtime handles, tool configs ni model configs. Conserva `removed_paths`, `skipped_paths`, `preserved_paths`, `blocked_paths`, `rollback_record_path` y flags no-operativas.

## Relacion Con Futura Regeneracion 6.2

La regeneracion segura de 6.2 debe partir de esta garantia: un sandbox completo puede revertirse por manifests y paths declarados antes de crear una nueva generacion.

## Fuera De Alcance

- regeneracion segura;
- runtime real;
- execution real;
- dry-run real operativo;
- tools/model invocation;
- context injection operativo;
- output delivery;
- UI/UX;
- integraciones;
- Market Catalog runtime;
- Business Composition Layer runtime;
- OBLITERATUS;
- raw Package directo a User Panel.

## Riesgos

- borrar por patron amplio en lugar de paths declarados;
- confundir rollback sandbox con limpieza de repo;
- aceptar manifests inconsistentes;
- borrar `domains/` operativo por path traversal o symlink escape.

## Veredicto

`SANDBOX_INTEGRAL_ROLLBACK_PASSED`

`SANDBOX_ROLLBACK_IDEMPOTENT_CONFIRMED`

## Readiness

`ready_for_phase_6_2_safe_regeneration`

## Proximo Prompt Recomendado

`PROMPT 6.2 - Regeneracion segura sandbox completa`
