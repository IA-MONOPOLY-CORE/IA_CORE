# Execution Contract Sin Ejecucion

## 1. Que es execution contract

`execution_contract` define readiness declarativa para una ejecucion futura de `agent` o `team`. Evalua precondiciones, contratos de entrada/salida, politicas de operacion, observability y audit store antes de permitir que exista un runtime executor.

En esta fase el resultado es solo un reporte:

```txt
passed | blocked
```

## 2. Que NO hace

- No ejecuta agentes.
- No ejecuta equipos.
- No llama modelos.
- No ejecuta tools reales.
- No persiste memoria real.
- No habilita external access.
- No toca UI.
- No toca integraciones.
- No muta targets.

## 3. Diferencia runtime vs execution

```txt
runtime_contract:
  readiness declarativa para runtime futuro

execution_contract:
  readiness declarativa para una corrida futura

runtime_executor:
  todavia no existe
```

`execution_contract` depende de `runtime_contract` passed, pero no habilita runtime ni execution.

## 4. Targets permitidos

Permitidos:

- `agent`
- `team`

Bloqueados como execution directo:

- `domain`
- `profile_catalog`
- `agent_preset`
- `paper_seed`
- `capability_policy`
- `tool_contract`
- `memory_contract`
- `runtime_contract`

## 5. Requisitos agent/team

Agent:

- target existe y esta `active`;
- no esta `legacy`, `broken` ni `archived`;
- `runtime_contract` existe y esta `passed`;
- `active_execution` existe y esta `passed`;
- capability policy declarativa valida;
- memory contract declarativo valido y sin persistencia real;
- tool contract declarativo valido y sin execution/external access;
- correlation id presente;
- audit store verificable.

Team:

- target existe y esta `active`;
- miembros existen y son compatibles;
- coordination model declarativo;
- `runtime_contract` y `active_execution` corresponden al team;
- capability/memory/tool contracts validos;
- correlation id y audit store verificable.

## 6. Input/output contract

`input_contract` minimo:

```txt
schema_version
input_type
required_fields
optional_fields
max_payload_size
validation_mode
```

`output_contract` minimo:

```txt
schema_version
output_type
required_fields
allowed_formats
max_output_size
validation_mode
```

Son declarativos. No procesan input real ni generan output real.

## 7. Prompt/model contract

`prompt_contract` minimo:

```txt
system_prompt_ref
user_prompt_schema
allowed_context_refs
forbidden_context_refs
safety_constraints
```

`model_invocation_contract` minimo:

```txt
model_policy_ref
model_required
local_or_remote_policy
hardware_policy_ref
fallback_policy
invocation_enabled=false
```

`invocation_enabled=true` bloquea el contrato.

## 8. Timeout/retry/cancellation/failure

Politicas minimas:

```txt
timeout_policy:
  max_duration_ms
  on_timeout

retry_policy:
  max_retries
  retry_on
  backoff_strategy

cancellation_policy:
  cancellable
  cancellation_window_ms
  on_cancel

failure_policy:
  on_error
  rollback_required
  audit_required
  escalation_required
```

No se implementa scheduler, executor, retry runner ni cancellation runtime.

## 9. Observability/audit store

Execution contract exige:

- `observability_required=true`;
- `audit_store_required=true`;
- `required_correlation_id` presente;
- audit store append-only verificable con `verify_audit_store`.

Sin audit store valido, el contrato queda `blocked`.

## 10. Futuro

- Execution contract E2E checkpoint.
- Runtime executor.
- Execution runner.
- Model invocation.
- Tool execution.
- Memory persistence.
- UI trigger.
- Integrations.
