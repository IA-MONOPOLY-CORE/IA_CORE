# Observability y audit persistence antes de runtime executor

Estado: `OBSERVABILITY_AUDIT_PERSISTENCE_CONTRACT_DEFINED`.

Este contrato define observability y audit persistence antes de cualquier runtime executor. No implementa runtime, no ejecuta agentes/equipos, no habilita tools reales, no persiste memoria real, no toca UI y no conecta integraciones.

## 1. Por que antes de runtime

Runtime necesita trazabilidad antes de existir. IA_CORE debe poder responder que paso, quien lo pidio, sobre que target, con que contrato, con que evidencia, que decision se tomo, que cambio, que no cambio, que bloqueo, por que bloqueo y como se revierte.

Audit sin persistencia es insuficiente. Runtime sin observability es peligroso.

## 2. Eventos minimos

Eventos obligatorios:

- `promotion_gate_evaluated`;
- `approval_requested`;
- `approval_decision_recorded`;
- `promotion_executed`;
- `promotion_rollback_recorded`;
- `active_contract_evaluated`;
- `active_executed`;
- `active_rollback_recorded`;
- `runtime_contract_evaluated`;
- `runtime_contract_blocked`;
- `runtime_boundary_violation`;
- `mutation_scope_verified`;
- `snapshot_recorded`;
- `rollback_plan_recorded`.

Cada evento exige: `event_id`, `correlation_id`, `event_type`, `timestamp`, `source_module`, `target_type`, `target_id`, `domain_id`, `operation`, `operation_phase`, `result_status`, `evidence_refs`, `mutation_scope`, flags runtime/execution/external/tools-memory, immutability y politicas de redaction/retention.

## 3. Correlation policy

No alcanza con que un evento exista. Debe pertenecer al mismo flujo:

- same `correlation_id`;
- same `target_type`;
- same `target_id`;
- same `domain_id`;
- same `operation`;
- same `requested_status` cuando aplique;
- same contract reference cuando aplique.

Esto evita evidencia cruzada entre otro target, otro dominio, otra operacion, otra decision, otro status u otro contrato.

## 4. Snapshot policy

Snapshots requeridos para mutaciones futuras:

- `before_snapshot`;
- `after_snapshot`;
- `diff_summary`;
- `mutation_scope`;
- `rollback_snapshot`;
- `checksum`.

Aplica conceptualmente a promotion executor, active executor, runtime contract evaluation y runtime executor futuro. En esta fase el contrato define la forma y valida checksums; no migra todos los executors.

## 5. Mutation scope policy

Cada evento declara `mutation_scope`.

Scopes permitidos:

- `none`;
- `status_only`;
- `status_and_artifact_state`;
- `manifest_status_only`;
- `in_memory_status_only`.

Un evento `mutation_scope_verified` puede registrar violaciones si una operacion muta mas de lo permitido. Runtime contract debe usar `none`.

## 6. Runtime boundary observability

Las violaciones se observan con flags separados:

- `runtime_flags`;
- `execution_flags`;
- `external_access_flags`;
- `tool_memory_flags`.

Esto permite distinguir runtime, execution, external access, tool execution y memory persistence sin mezclar fronteras.

## 7. Audit persistence

El contrato de store local seguro exige:

- `store_mode`;
- `root_path`;
- `write_mode=append_only`;
- `append_only=true`;
- `immutable_records=true`;
- `checksum`;
- `event_count`;
- timestamps de creacion/actualizacion.

La persistencia real del event log queda para fase posterior. El contrato actual define el formato y valida append-only/immutability.

## 8. Metricas minimas

Metricas internas minimas:

- `events_total`;
- `events_by_type`;
- `blocked_operations_total`;
- `successful_operations_total`;
- `rollback_operations_total`;
- `runtime_boundary_violations_total`;
- `mutation_scope_violations_total`;
- `missing_evidence_total`;
- `invalid_correlation_total`;
- `last_event_at`.

No se crea UI ni dashboard.

## 9. Futuro

Queda para fases posteriores:

- audit store real;
- persistent event log;
- observability reports;
- runtime executor;
- execution contract;
- UI dashboard futuro;
- integraciones externas bajo contrato.

Antes de runtime executor hace falta un checkpoint end-to-end de observability/audit persistence sobre la cadena sandbox activa.
