# Contrato approval workflow y audit log

## 1. Que es approval workflow

`approval workflow` modela decisiones futuras sobre resultados de `promotion_gate`.

Regla central:

```txt
promotion_gate passed
!= approved
!= promoted
```

Una gate positiva no promueve nada automaticamente. Una decision aprobada tampoco muta estado: solo registra que un target podria ser tomado por un executor futuro.

## 2. Approval request

Campos principales:

- `approval_request_id`;
- `domain_id`;
- `target_type`;
- `target_id`;
- `requested_status`;
- `promotion_gate_result_id`;
- `promotion_gate_result`;
- `requested_by`;
- `requested_at`;
- `evidence_summary`;
- `blockers`;
- `warnings`;
- `status`.

Estados permitidos:

- `draft`;
- `submitted`;
- `under_review`;
- `approved`;
- `rejected`;
- `needs_changes`;
- `expired`;
- `revoked`.

Validaciones:

- requiere `promotion_gate_result=passed`;
- rechaza `requested_status=active`;
- requiere evidencia;
- requiere actor;
- no acepta blockers.

## 3. Approval decision

Decisiones permitidas:

- `approved_for_validation`;
- `approved_for_activation_candidate`;
- `rejected`;
- `needs_changes`;
- `expired`;
- `revoked`.

Campos principales:

- `approval_decision_id`;
- `approval_request_id`;
- `decision`;
- `decided_by`;
- `decided_at`;
- `reason`;
- `evidence_reviewed`;
- `conditions`;
- `expires_at`;
- `status`.

Regla de seguridad:

- self-approval queda bloqueado para decisiones aprobatorias;
- `approved` no equivale a `promoted`.

## 4. Audit log

Eventos soportados:

- `promotion_gate_evaluated`;
- `approval_requested`;
- `approval_decision_recorded`;
- `approval_rejected`;
- `approval_revoked`;
- `promotion_blocked`;
- `future_promotion_ready`.

Campos principales:

- `audit_event_id`;
- `event_type`;
- `domain_id`;
- `target_type`;
- `target_id`;
- `actor`;
- `actor_type`;
- `occurred_at`;
- `source`;
- `action`;
- `before_state`;
- `after_state`;
- `result`;
- `evidence`;
- `related_ids`;
- `immutable`;
- `runtime_related`;
- `external_access_related`.

Reglas obligatorias:

- `immutable=true`;
- `runtime_related=false`;
- `external_access_related=false`;
- evidencia obligatoria;
- actor obligatorio;
- target obligatorio.

## 5. Frontera operativa

Este contrato no implementa:

- promocion real;
- `active`;
- runtime;
- UI;
- integracion externa;
- permisos reales;
- auth real.

No escribe en `domains/` operativo ni toca `agents/` legacy.

## 6. Futuro

Queda para fases posteriores:

- promotion executor;
- state mutation controlada;
- auth real;
- permisos efectivos;
- UI;
- auditoria persistente avanzada;
- runtime.
