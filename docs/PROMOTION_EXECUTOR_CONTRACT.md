# Promotion executor controlado

## 1. Que es promotion executor

`promotion_executor` aplica una promocion aprobada hacia estados intermedios no operativos.

Flujo:

```txt
promotion_gate passed
        ->
approval decision approved
        ->
promotion executor
        ->
validated / candidate_for_activation
```

## 2. Que NO hace

No hace:

- `active`;
- runtime;
- ejecucion de agentes;
- ejecucion de equipos;
- UI;
- integraciones;
- memoria real;
- herramientas reales.

## 3. Estados permitidos

Permitidos:

- `validated`;
- `candidate_for_activation`.

Bloqueado siempre:

- `active`.

`validated` y `candidate_for_activation` no son estados operativos y no equivalen a PASSED activo.

## 4. Approval requerido

Para `validated` se requiere:

```txt
approved_for_validation
```

Para `candidate_for_activation` se requiere:

```txt
approved_for_activation_candidate
```

Se bloquean:

- approval rejected;
- approval needs_changes;
- approval expired;
- approval revoked;
- approval para otro target;
- approval para otro requested_status;
- approval sin evidencia;
- approval sin actor valido.

## 5. Audit event

Cada ejecucion aplicada crea un audit event:

```txt
promotion_executed
```

El evento registra:

- actor;
- target;
- previous_status;
- applied_status;
- approval_decision_id;
- promotion_gate_result_id;
- execution_id;
- evidence;
- `immutable=true`;
- `runtime_related=false`;
- `external_access_related=false`.

## 6. Rollback de promocion

El rollback de promocion es rollback de estado:

```txt
rollback de estado
!=
rollback de materializacion
```

Vuelve de `validated` o `candidate_for_activation` al estado anterior. No borra artefactos, no modifica dependencias, no toca runtime y no toca legacy.

## 7. Futuro

Queda para fases posteriores:

- active promotion;
- runtime activation;
- auth real;
- permission enforcement;
- UI;
- integracion;
- auditoria persistente avanzada.
