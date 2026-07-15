# Diseno de artifact_manifest sandbox

## Proposito

`artifact_manifest.json` es el contrato de inventario, lineage, dependencias y rollback de artefactos internos de un dominio sandbox.

El dominio no es solo una carpeta: contiene artefactos relacionados. Cada artefacto debe poder explicar que es, de donde viene, que version tiene, de que depende y como puede revertirse.

## Relacion Dominio / Artefactos

`domain.json` describe la identidad y estado del dominio sandbox.

`materialization_manifest.json` describe la materializacion del dominio.

`artifact_manifest.json` describe los artefactos internos del dominio.

En Fase 2, `artifact_manifest.json` debe vivir dentro del sandbox, preferentemente bajo:

```txt
<sandbox>/<domain_id>/manifests/artifact_manifest.json
```

## Estructura

Manifest minimo:

```json
{
  "artifact_manifest_version": "1.0",
  "domain_id": "sandbox_marketing_crm_automation",
  "artifacts": []
}
```

Cada artefacto contiene:

```json
{
  "artifact_id": "profile_catalog_main",
  "artifact_type": "profile_catalog",
  "name": "Profile Catalog Main",
  "version": "1.0.0",
  "status": "materialized",
  "created_from": {
    "source_type": "sandbox_materialization",
    "materialization_id": "mat_..."
  },
  "created_by": "core.service",
  "dependencies": [],
  "created_at": "2026-07-15T00:00:00",
  "updated_at": "2026-07-15T00:00:00",
  "rollback_info": {
    "created_paths": [],
    "depends_on": [],
    "safe_remove": true
  }
}
```

## Tipos Permitidos

- `profile_catalog`
- `agent_preset`
- `paper_seed`
- `agent`
- `team`
- `memory`
- `model_recommendation`

Estos tipos quedan declarados para Fase 2 y fases posteriores. Este contrato no crea artefactos reales.

## Lineage

`created_from` debe registrar el origen del artefacto. Puede apuntar a:

- preview;
- materializacion sandbox;
- catalogo global;
- otro artefacto interno;
- regeneracion futura.

`created_by` indica el servicio o test que genero el registro.

## Dependencias

`dependencies` lista otros `artifact_id` del mismo manifest. Esto permite representar cadenas como:

```txt
profile_catalog
-> agent_preset
-> agent
-> team
```

El validador rechaza dependencias inexistentes y autoreferencias.

## Rollback Futuro

`rollback_info` prepara rollback por artefacto:

- `created_paths`: paths creados por ese artefacto.
- `depends_on`: artefactos que deben considerarse antes de remover.
- `safe_remove`: indica si el artefacto podria removerse de forma segura.

PROMPT 1.4.1 no implementa rollback parcial. Solo define el contrato.

## Relacion con PASSED

Un artefacto `materialized` no equivale a PASSED. PASSED futuro requiere validacion especifica, trazabilidad, dependencias coherentes y aprobacion segun corresponda.

## Relacion con artifact_state

El campo `status` usa `core/artifact_state.py`.

Estados disponibles:

- `derived_preview`
- `ready_to_materialize`
- `materialized`
- `active`
- `archived`
- `legacy`
- `broken`

Para Fase 2 inicial se recomienda usar `materialized` o estados no operativos. `active` debe quedar reservado para PASSED.

## Que No Hace

Este contrato no:

- crea `profile_catalog`;
- crea `agent_presets`;
- crea papers;
- crea agentes;
- crea equipos;
- escribe en `domains/`;
- implementa rollback parcial;
- toca UI o integraciones.
