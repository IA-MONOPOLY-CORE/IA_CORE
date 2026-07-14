# Schema de dominio sandbox real

## 1. Proposito

Este documento define el contrato minimo de `domain.json` para un dominio sandbox materializado. El schema existe para impedir dominios fantasma: una carpeta no alcanza para que IA_CORE reconozca un dominio como real, trazable o seguro.

## 2. Relacion con Fase 1

PROMPT 1.0 inicia la Fase 1 del libro Backend Interno. En esta fase se define el contrato del dominio sandbox antes de materializarlo. Todavia no se crea un dominio persistente en `domains/`.

## 3. Sandbox vs dominio activo

Un dominio sandbox `materialized` significa que existe una estructura validada o lista para existir en una fase posterior. No significa que sea operativo, visible, PASSED ni `active`.

Para ser `active`, un dominio futuro debera tener validacion PASSED completa, aprobacion humana o politica equivalente, trazabilidad y cierre post-materializacion.

## 4. Campos obligatorios

El validador vive en `core/sandbox_domain_schema.py` y exige:

- `schema_version`: version del schema sandbox.
- `domain_id`: identificador tecnico estable en `snake_case`.
- `name`: nombre humano legible.
- `description`: descripcion del alcance.
- `status`: estado de `core/domain_state.py`.
- `domain_type`: debe ser `sandbox`.
- `source_request`: intencion/origen de la materializacion.
- `created_from`: origen tecnico del dominio.
- `materialization_id`: identificador del proceso de materializacion.
- `materialization_status`: estado interno del proceso.
- `artifact_state`: estado de `core/artifact_state.py`.
- `created_at`: fecha de creacion.
- `updated_at`: fecha de ultima actualizacion.
- `human_review_required`: booleano obligatorio; en esta fase debe ser `true`.
- `rollback_manifest`: contrato minimo de rollback.
- `validation`: informacion de validacion del schema.
- `warnings`: lista de advertencias.
- `metadata`: objeto libre para datos no operativos.

## 5. Campos opcionales

El schema permite agregar metadata futura dentro de objetos existentes:

- `metadata.*`
- `validation.rules`
- `validation.broken_reason`
- `created_from.preview_id`
- `created_from.artifact_state`
- `rollback_manifest.notes`

No se agregan `profile_catalog`, `agent_presets`, papers, agentes ni equipos dentro de este schema.

## 6. Ejemplo valido

```json
{
  "schema_version": "1.0",
  "domain_id": "sandbox_marketing_crm_automation",
  "name": "Sandbox Marketing CRM Automation",
  "description": "Dominio sandbox para validar materializacion controlada.",
  "status": "materialized",
  "domain_type": "sandbox",
  "source_request": {
    "area_id": "marketing_publicidad",
    "niche_id": "contenidos_redes",
    "objective": "validar schema sandbox sin materializar dominio real",
    "business_scale": "pyme"
  },
  "created_from": {
    "type": "preview",
    "preview_id": "preview_123"
  },
  "materialization_id": "mat_test_20260714_001",
  "materialization_status": "schema_validated",
  "artifact_state": "materialized",
  "created_at": "2026-07-14T00:00:00",
  "updated_at": "2026-07-14T00:00:00",
  "human_review_required": true,
  "rollback_manifest": {
    "can_rollback": true,
    "created_paths": [],
    "modified_paths": [],
    "backup_paths": [],
    "notes": []
  },
  "validation": {
    "schema": "sandbox_domain_schema",
    "schema_version": "1.0",
    "validated": true,
    "passed": false,
    "rules": ["domain_state", "artifact_state", "domain_identity", "rollback_manifest"]
  },
  "warnings": [],
  "metadata": {
    "operational": false
  }
}
```

## 7. Ejemplos invalidos

- Falta `source_request`.
- `domain_id` no esta normalizado.
- `domain_type` es distinto de `sandbox`.
- `status` es desconocido.
- `status` es `active` sin PASSED.
- `artifact_state` no coincide con `status`.
- `materialization_id` esta vacio.
- `created_from` esta vacio o tiene `type` desconocido.
- `rollback_manifest` no contiene listas de paths.
- `human_review_required` falta o es `false`.
- El payload no es serializable como JSON.
- Un fixture declara rollback sobre `domains/` real.

## 8. Relacion con domain_state

El schema reutiliza `core/domain_state.py`. Para sandbox inicial se permiten:

- `materialized`
- `archived`
- `broken`

`active` queda bloqueado en esta fase. `materialized` no aparece como activo ni visible por defecto.

## 9. Relacion con artifact_state

El campo `artifact_state` reutiliza `core/artifact_state.py` y debe coincidir con `status`.

Estados validos en este schema:

- `materialized`
- `archived`
- `broken`

`derived_preview` y `ready_to_materialize` pertenecen al preview previo, no al `domain.json` sandbox materializado. `active` queda reservado para PASSED futuro.

## 10. Relacion con preview

El schema puede recibir metadata de `core/domain_materialization_preview.py` en:

- `source_request`
- `created_from.preview_id`
- `created_from.artifact_state`

Cadena futura:

```txt
preview validado
-> schema sandbox domain.json
-> materializacion futura
-> validacion post-materializacion
-> active/PASSED solo despues de cierre
```

## 11. Relacion con rollback

`rollback_manifest` existe desde el primer schema para que la futura materializacion no cree archivos sueltos sin posibilidad de inventario.

Campos actuales:

- `can_rollback`
- `created_paths`
- `modified_paths`
- `backup_paths`
- `notes`

En fixtures de este prompt, esos paths deben estar vacios o ser temporales. El validador bloquea paths hacia `domains/` real salvo habilitacion explicita de una fase futura.

## 12. Reglas PASSED

PASSED no se declara por decoracion. Para llegar a `active` haran falta, como minimo:

- preview validado;
- materializacion controlada;
- validacion post-materializacion;
- rollback manifest completo;
- revision humana o regla de aprobacion definida;
- tests verdes;
- ausencia de duplicados/equivalencias;
- trazabilidad completa.

## 13. Que NO hace este schema

No crea dominios.
No registra dominios.
No escribe en `domains/`.
No crea `profile_catalog.json`.
No crea `agent_presets.json`.
No crea agentes, papers ni equipos.
No implementa rollback real.
No toca UI ni integraciones.

## 14. Criterios para avanzar a materializacion real

Antes de PROMPT 1.1 o fases posteriores, debe existir:

- schema validado por tests;
- ruta de materializacion que use este validador;
- manifest de rollback real;
- errores accionables;
- confirmacion de que `/api/domains/create` sigue bloqueado;
- contrato claro para UI futura.
