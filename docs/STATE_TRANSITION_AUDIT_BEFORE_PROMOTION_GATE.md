# Auditoria de estados antes de promotion gate

## 1. Veredicto

Resultado: `PASSED_STATE_TRANSITION_AUDIT`.

IA_CORE tiene una semantica de estados suficientemente consistente para disenar luego un promotion gate seguro, con una condicion importante: `active` existe como estado global, pero los contratos sandbox actuales lo bloquean. La promotion gate todavia no existe y no debe inferirse desde `materialized`.

## 2. Mapa canonico de estados

| Estado | Fuente | Uso actual | Clasificacion |
|---|---|---|---|
| `empty` | `core/domain_state.py` | dominio sin contenido operativo | CODE_AND_DOC |
| `draft` | `core/domain_state.py` | definicion inicial de dominio | CODE_AND_DOC |
| `derived_preview` | `core/artifact_state.py` | salida derivada no materializada | CODE_AND_DOC |
| `preview` | `core/domain_state.py`, docs | vista previa de dominio | CODE_AND_DOC |
| `ready_to_materialize` | `core/artifact_state.py` | artefacto derivado listo para materializar | CODE_AND_DOC |
| `materialized` | domain/artifact/agent/team schemas | escrito o trazado, no operativo por si mismo | CODE_AND_DOC |
| `validated` | `core/artifact_state.py`, `core/domain_state.py`, docs | estado intermedio no operativo formalizado en PROMPT 2.11 | CODE_AND_DOC |
| `candidate_for_activation` | `core/artifact_state.py`, `core/domain_state.py`, docs | estado intermedio no operativo formalizado en PROMPT 2.11 | CODE_AND_DOC |
| `active` | domain/artifact enums | operativo PASSED, bloqueado en sandbox | CODE_AND_DOC |
| `archived` | domain/artifact enums | retirado del flujo activo | CODE_AND_DOC |
| `legacy` | domain/artifact enums | historico fuera del flujo nuevo | CODE_AND_DOC |
| `broken` | domain/artifact enums | inconsistente, no usable | CODE_AND_DOC |
| `blocked` | `core/capability_policy_schema.py` | capability bloqueada | CODE_AND_DOC |
| `forbidden` | `core/capability_policy_schema.py` | capability prohibida | CODE_AND_DOC |
| `future_requires_approval` | `core/capability_policy_schema.py` | approval futuro declarativo | CODE_AND_DOC / FUTURE |
| `declared` | memory/tool/team policy/capability policy | capability declarativa | CODE_AND_DOC |
| `allowed_declared` | `core/capability_policy_schema.py` | permitida solo como declarativa | CODE_AND_DOC |
| `missing` | `core/capability_policy_schema.py` | policy no evaluada para capability | CODE_ONLY |
| `not_evaluated` | `core/capability_policy_schema.py` | approval/policy no evaluado | CODE_ONLY |
| `not_required` | `core/capability_policy_schema.py` | approval no requerido | CODE_ONLY |
| `future_required` | `core/capability_policy_schema.py` | approval requerido en futuro | CODE_ONLY / FUTURE |

No se detecto necesidad real de inventar estados nuevos antes de promotion gate.

## 3. Matriz por entidad

| Entidad | Permitidos hoy | Bloqueados hoy | Futuros | Transicion inicial | Final permitido hoy | `active` |
|---|---|---|---|---|---|---|
| domain | `empty`, `draft`, `preview`, `materialized`, `active`, `archived`, `legacy`, `broken` en contrato general | `active` sin trazabilidad; `legacy -> active` por restore | `validated`, `candidate_for_activation` | `empty` o `preview` | `archived`, `broken`, `materialized`; `active` solo fuera de sandbox con PASSED | permitido en contrato general, bloqueado en sandbox |
| artifact | `derived_preview`, `ready_to_materialize`, `materialized`, `active`, `archived`, `legacy`, `broken` | estados no enum | `validated`, `candidate_for_activation` | `derived_preview` | `active`, `archived`, `broken` segun helper global | permitido globalmente, no por sandbox |
| profile_catalog | `materialized` como artefacto sandbox | `active` por materializadores actuales | `validated`, `candidate_for_activation`, `active` via gate | `materialized` | `materialized`/rollback | bloqueado por fase |
| agent_preset | `materialized` como artefacto sandbox | `active` por materializadores actuales | `validated`, `candidate_for_activation`, `active` via gate | `materialized` | `materialized`/rollback | bloqueado por fase |
| paper_seed | `materialized` como artefacto sandbox | `active` por materializadores actuales | `validated`, `candidate_for_activation`, `active` via gate | `materialized` | `materialized`/rollback | bloqueado por fase |
| sandbox_agent | `ready_to_materialize`, `materialized`, `archived`, `broken` | `active`, `legacy`, `derived_preview` | `validated`, `candidate_for_activation` | `ready_to_materialize` | `materialized`, `archived`, `broken` | bloqueado |
| sandbox_team | `materialized` | `active`, `archived`, `broken`, `ready_to_materialize` para team root | `validated`, `candidate_for_activation` | `materialized` | `materialized`/rollback | bloqueado |
| memory_contract | `declared` | todo runtime o storage real activo | `allowed_declared`, `future_requires_approval`, approval real | `declared` | `declared` | no aplica |
| tool_contract | `declared` | execution/runtime/external access | `allowed_declared`, `future_requires_approval`, approval real | `declared` | `declared` | no aplica |
| capability_policy | `declared`, `allowed_declared`, `blocked`, `forbidden`, `future_requires_approval` segun tipo | runtime/execution/external access/self-approval/auto-escalation | approval real, audit log real | `declared` | declarativo validado | no aplica |

## 4. Transiciones actuales confirmadas

### `core/artifact_state.py`

- `derived_preview -> ready_to_materialize`
- `derived_preview -> broken`
- `ready_to_materialize -> materialized`
- `ready_to_materialize -> broken`
- `materialized -> active`
- `materialized -> archived`
- `materialized -> broken`
- `active -> archived`
- `active -> broken`
- `archived -> broken`
- `legacy -> ready_to_materialize`
- `legacy -> broken`
- `broken -> derived_preview`
- `broken -> ready_to_materialize`

Nota critica: `materialized -> active` existe como transicion global de artefacto, pero no hay promotion gate y los schemas sandbox bloquean `active`.

### `core/domain_state.py`

- `empty -> draft|preview|materialized|archived|broken`
- `draft -> preview|materialized|archived|broken`
- `preview -> materialized|archived|broken`
- `materialized -> active|archived|broken`
- `active -> archived|broken`
- `archived -> materialized|broken`
- `legacy -> preview|materialized|broken`
- `broken -> draft|preview|archived`

Nota critica: `restore_domain()` rechaza activar dominios; `legacy -> active` no existe como transicion directa.

## 5. Transiciones futuras esperadas

Estas transiciones quedaron implementadas como estados intermedios en PROMPT 2.11:

- `materialized -> validated`
- `validated -> candidate_for_activation`

Permanece como futuro no implementado:

- `candidate_for_activation -> active`
- `active -> archived`

Tambien quedan futuras:

- approval real;
- audit log real;
- evidence bundle de promocion;
- permisos efectivos de capabilities;
- validacion de runtime antes de activacion.
- active promotion.

## 6. Reglas criticas antes de promotion gate

| Regla | Resultado | Evidencia |
|---|---|---|
| `active` bloqueado en sandbox | PASSED | `sandbox_domain_schema`, `sandbox_agent_schema`, `sandbox_team_schema` rechazan `active` |
| runtime bloqueado | PASSED | agent/team/capability/memory/tool contracts exigen flags false |
| execution bloqueado | PASSED | team/tool/capability policy rechazan execution |
| external access bloqueado | PASSED | tool/capability policy rechazan external access |
| capabilities declarativas | PASSED | memory/tool solo `declared`; capability_policy separa allowed/runtime |
| team no habilita miembros | PASSED | `validate_team_policy_member_boundary` bloquea auto grants |
| materialized no equivale a usable | PASSED | `is_operational(materialized)=false`; docs lo repiten |
| validated no se usa como active | PASSED | no existe estado enum `validated`; solo booleano documental |
| legacy no vuelve activo por accidente | PASSED | restore bloquea active; legacy no transiciona directo a active |
| broken no puede promoverse | PASSED | no transiciona a active ni candidate implementado |
| archived no puede ejecutarse | PASSED | no hay runtime para archived; operational helper requiere active |

## 7. Inconsistencias detectadas

No hay contradiccion bloqueante.

Observaciones:

- `validated` aparece como concepto en docs y como `validation.validated` booleano, pero no como estado canonico implementado.
- `candidate_for_activation` aun no existe en codigo; debe nacer con promotion gate si se decide usarlo.
- `ArtifactState` permite `materialized -> active` a nivel global. Esto no activa nada por si solo, pero la futura promotion gate debe envolver esa transicion con evidencia, approval y auditoria.

## 8. Decision

El sistema queda listo para `PROMPT 2.9 - promotion gate`.

No se recomienda subprompt de refuerzo previo. El proximo prompt debe implementar la puerta sin reutilizar `can_activate()` como autorizacion suficiente.
