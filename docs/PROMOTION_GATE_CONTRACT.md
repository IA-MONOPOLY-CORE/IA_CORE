# Contrato promotion gate sandbox

## 1. Que es promotion gate

`promotion gate` es una evaluacion tecnica no mutante.

Decide si un target sandbox tiene evidencia suficiente para ser considerado:

```txt
validated
```

o:

```txt
candidate_for_activation
```

No cambia el estado del target. No activa dominios, artefactos, agentes, equipos, runtime, memoria real ni herramientas reales.

Regla central:

```txt
materialized
!= validated
!= candidate_for_activation
!= active
```

## 2. Estados

- `materialized`: existe como archivo o artefacto trazado; no es usable operativo.
- `validated`: la promotion gate confirmo checks declarativos suficientes; no activa.
- `candidate_for_activation`: la promotion gate confirma que el target podria pasar a un flujo futuro de approval/activacion; no activa.
- `active`: estado operativo futuro. En esta fase siempre queda bloqueado.

En esta fase `requested_status=active` siempre devuelve:

```txt
gate_result: blocked
```

## 3. Targets

Targets soportados:

- `domain`;
- `artifact`;
- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- `agent`;
- `team`;
- `capability_policy`.

## 4. Checks

La gate evalua, segun target:

- manifest consistente;
- dependencias presentes;
- lineage de agentes;
- runtime boundary;
- legacy boundary;
- capability policy declarativa;
- rollback readiness expresada en manifest;
- regeneration history si aplica;
- existencia de archivos sandbox esperados.

## 5. Bloqueos

Bloqueos obligatorios:

- solicitud a `active`;
- target `active`;
- target `broken`;
- target `archived`;
- target `legacy`;
- `runtime_enabled=true`;
- `execution_enabled=true`;
- `execution_allowed=true`;
- `external_access=true`;
- manifest inconsistente;
- dependencias rotas;
- capability policy invalida;
- agente sin lineage valido;
- equipo con coordinacion ejecutable.

## 6. Evidencia

Cada evaluacion devuelve `checks` con forma:

```json
{
  "check": "runtime_boundary",
  "result": "passed",
  "evidence": "runtime_enabled=false"
}
```

El reporte completo incluye:

- `gate_id`;
- `domain_id`;
- `target_type`;
- `target_id`;
- `current_status`;
- `requested_status`;
- `gate_result`;
- `checks`;
- `blockers`;
- `warnings`;
- `evidence`;
- `capability_policy_result`;
- `runtime_boundary_result`;
- `legacy_boundary_result`;
- `created_at`;
- `evaluated_at`.

La evidencia debe explicar por que paso o se bloqueo. No se acepta promover por existencia de archivo.

## 7. Futuro

Queda para fases posteriores:

- promocion real;
- approval workflow;
- audit log persistente;
- activacion;
- runtime;
- UI;
- integraciones.

La promotion gate actual produce un reporte evaluable. Un flujo futuro podra consumir ese reporte, agregar approval/audit log y recien entonces cambiar estados.
