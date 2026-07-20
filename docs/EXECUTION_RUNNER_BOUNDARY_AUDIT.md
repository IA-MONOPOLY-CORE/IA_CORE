# Execution Runner Boundary Audit

## 1. Que es execution_runner

`execution_runner` sera un modulo futuro responsable de coordinar una corrida controlada despues de que la cadena declarativa ya haya pasado.

En primera fase no debe invocar modelos reales, no debe ejecutar tools reales y no debe persistir memoria real. Su primer alcance seguro debe ser contractual: verificar precondiciones, construir un attempt record declarativo y registrar eventos seguros.

Separacion de componentes:

| Componente futuro | Alcance |
| --- | --- |
| `execution_runner_contract` | contrato/schema del runner, sin ejecucion |
| `execution_runner_dry_run` | validacion de flujo sin efectos reales |
| `execution_runner_simulation` | simulacion controlada con datos declarativos |
| `execution_runner_no_model` | plan/attempt sin model invocation |
| `execution_runner_execute_future` | ejecucion futura, bloqueada hoy |
| `model_invocation_future` | adaptador futuro de modelos |
| `tool_execution_future` | adaptador futuro de tools |
| `memory_persistence_future` | motor futuro de memoria persistente |

## 2. Que NO es execution_runner

`execution_runner` no es:

- model invocation real;
- tool execution real;
- memory persistence real;
- external access;
- UI trigger;
- integration runner;
- autonomous agent loop;
- scheduler;
- worker queue.

Tampoco debe significar `execution_enabled=true` en esta fase.

## 3. Relacion con piezas existentes

Debe depender de:

- `active_executor` passed;
- `runtime_contract` passed;
- `execution_contract` passed;
- `runtime_executor_contract` passed;
- `runtime_executor prepare-only` con status `prepared`;
- observability context valido;
- audit_store verified;
- capability_policy valida;
- memory/tool contracts declarativos;
- idempotency/lock/concurrency;
- abort/rollback plan.

La pieza inmediatamente anterior validada es `runtime_executor prepare-only`: prepara, registra audit/observability y mantiene runtime/execution/model/tool/memory/external boundaries en false.

## 4. Fronteras

| Frontera | Estado para primer execution runner futuro |
| --- | --- |
| `execution_enabled` | bloqueado |
| `execution_runner_enabled` | bloqueado |
| `model_invocation_enabled` | bloqueado |
| `tool_execution_enabled` | bloqueado |
| `memory_persistence_enabled` | bloqueado |
| `external_access` | bloqueado |
| `agent_executed` | bloqueado |
| `team_executed` | bloqueado |

El primer runner futuro no debe cruzar ninguna de estas fronteras. Debe crear solo metadata declarativa y eventos seguros.

## 5. Requisitos minimos antes de execution runner

| Requisito | Agent | Team |
| --- | --- | --- |
| Target active interno | requerido | requerido |
| Runtime contract passed | requerido | requerido |
| Execution contract passed | requerido | requerido |
| Runtime executor contract passed | requerido | requerido |
| Runtime prepare-only `prepared` | requerido | requerido |
| `preparation_id` valido | requerido | requerido |
| Audit store verified | requerido | requerido |
| Observability context valido | requerido | requerido |
| Capability policy valida | requerido | requerido |
| Memory/tool contracts declarativos | requerido | requerido |
| Input/output/prompt/model contracts declarativos | requerido | requerido |
| Timeout/retry/cancellation/failure policies | requerido | requerido |
| Idempotency key | requerido | requerido |
| Lock/concurrency policy | requerido | requerido |
| Abort/rollback plan | requerido | requerido |
| Miembros compatibles | no aplica | requerido |
| Coordination model declarativo | no aplica | requerido |
| No external access | requerido | requerido |
| No tool execution real | requerido | requerido |
| No memory persistence real | requerido | requerido |
| No model invocation real | requerido | requerido |

## 6. Modos futuros

| Modo | Estado |
| --- | --- |
| `contract_only` | recomendado como primer paso |
| `dry_run_only` | despues del contrato |
| `simulation_only` | futuro, despues de dry-run |
| `no_model_execution_plan` | futuro, sin modelos/tools/memoria |
| `model_invocation_future` | bloqueado |
| `tool_execution_future` | bloqueado |
| `memory_persistence_future` | bloqueado |
| `full_execution_future` | bloqueado |

Decision: el primer modo seguro es `contract_only`.

Motivo: ya existe prepare-only operativo, pero aun falta schema del runner, attempt record, politicas de input/output de runner, eventos especificos del runner y reglas de no-ejecucion propias.

## 7. Bloqueadores actuales

| Bloqueador | Clasificacion |
| --- | --- |
| execution runner schema | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| execution runner dry-run semantics | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| execution attempt record | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| execution input validation | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| execution output validation | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| prompt assembly boundary | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| model invocation adapter | REQUIRED_BEFORE_MODEL_INVOCATION |
| model policy enforcement | REQUIRED_BEFORE_MODEL_INVOCATION |
| hardware-aware policy | REQUIRED_BEFORE_MODEL_INVOCATION |
| tool permission enforcement | REQUIRED_BEFORE_TOOL_EXECUTION |
| memory persistence engine | REQUIRED_BEFORE_MEMORY_PERSISTENCE |
| cancellation runtime | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| failure recovery | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| audit store write policy during execution | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| event stream | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |
| concurrency/locking real | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| idempotency real | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| queue/scheduler | NOT_REQUIRED_FOR_EXECUTION_RUNNER |
| secrets handling | REQUIRED_BEFORE_MODEL_INVOCATION |
| auth/actor real | REQUIRED_BEFORE_EXECUTION_RUNNER_DRY_RUN |
| UI trigger policy | REQUIRED_BEFORE_UI_TRIGGER |
| integration boundary | FUTURE_INTEGRATION |
| sandbox-to-runtime artifact access | REQUIRED_BEFORE_EXECUTION_RUNNER_CONTRACT |

## 8. Readiness

Veredicto: `EXECUTION_RUNNER_READY_FOR_CONTRACT_ONLY`.

IA_CORE esta listo para disenar el contrato de `execution_runner`, pero no para implementar runner, dry-run operativo, model invocation, tools reales, memoria real, external access, UI ni integraciones.

## 9. Proximo paso

Proximo subprompt recomendado: disenar `execution_runner_contract` en modo `contract_only`, sin ejecucion real.
