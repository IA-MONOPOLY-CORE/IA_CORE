# Runtime Executor Contract Prepare-Only

## 1. Que es runtime executor contract prepare-only

`runtime_executor_contract` en modo `prepare_only` define la preparacion contractual del futuro runtime executor. Valida precondiciones, arma un plan declarativo, exige abort/rollback plan, idempotency, lock/concurrency policy, observability y audit store.

No es un runtime executor real. Es un contrato previo.

## 2. Que NO hace

- No habilita `runtime_enabled`.
- No habilita `execution_enabled`.
- No implementa execution runner.
- No ejecuta agentes.
- No ejecuta equipos.
- No invoca modelos.
- No ejecuta tools reales.
- No persiste memoria real.
- No habilita external access.
- No toca UI.
- No toca integraciones.

## 3. Dependencias

Exige:

```txt
active passed
runtime_contract passed
execution_contract passed
audit_store verified
observability context
correlation_id
capability/memory/tool policies declarativas
abort/rollback plan
idempotency_key
lock_policy
concurrency_policy
mutation_policy
boundary_policy
```

Targets soportados: `agent`, `team`.

Targets bloqueados: `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `capability_policy`, `tool_contract`, `memory_contract`, `runtime_contract`, `execution_contract`.

## 4. Preparation plan

Estructura minima:

```txt
plan_id
mode=prepare_only
target_type
target_id
required_contracts
required_inputs
required_outputs
required_policies
required_evidence
preflight_checks
blocked_actions
expected_no_mutation=true
created_at
```

`blocked_actions` debe incluir runtime execution, execution runner, model invocation, tool execution, memory persistence, external access, UI trigger e integration runner.

## 5. Abort/rollback plan

`abort_plan` minimo:

```txt
abortable
abort_conditions
abort_result
audit_required
observability_required
```

`rollback_plan` minimo:

```txt
rollback_required
rollback_scope
rollback_allowed_mutations
audit_required
observability_required
```

En prepare-only, `rollback_allowed_mutations` debe estar vacio. No se implementa rollback real.

## 6. Idempotency/lock/concurrency

`idempotency_key` es obligatorio.

`lock_policy` debe declarar bloqueo de doble preparacion simultanea, pero `real_lock_enabled=false`; no hay lock real todavia.

`concurrency_policy` debe declarar `single_target_preparation`, con queue y scheduler deshabilitados.

## 7. Boundaries

La `boundary_policy` debe mantener en `false`:

- runtime;
- execution;
- model invocation;
- tool execution;
- memory persistence;
- external access;
- UI trigger;
- integration runner.

El evaluador tambien bloquea esos flags si aparecen en el target.

## 8. Futuro

Proximos pasos posibles:

- E2E runtime executor contract prepare-only;
- runtime executor prepare-only implementation;
- runtime executor prepare-only E2E;
- execution runner contract;
- model invocation contract;
- tool execution contract;
- memory persistence contract;
- external access contract.
