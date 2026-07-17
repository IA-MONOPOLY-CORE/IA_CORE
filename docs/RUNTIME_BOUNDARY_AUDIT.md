# Auditoria de frontera runtime antes de ejecucion real

Estado: `RUNTIME_READY_FOR_CONTRACT_ONLY`.

Esta auditoria cierra la frontera entre `active` interno y runtime real. No implementa runtime, no habilita ejecucion de agentes o equipos, no crea adapters, no activa herramientas, no crea memoria persistente, no agrega UI ni integraciones externas.

## Definicion de runtime

En este sistema, runtime significa cualquier capacidad que permita preparar, iniciar, coordinar o ejecutar comportamiento operativo real de un agente o equipo.

Flags y conceptos bloqueados en esta fase:

- `runtime_enabled=true`;
- `execution_enabled=true`;
- `execution_allowed=true`;
- `external_access=true`;
- memoria persistente real;
- adapters o clients de herramientas reales;
- invocacion real de modelos desde agentes/equipos;
- orquestacion ejecutable entre miembros de equipo;
- acceso a APIs, navegador, filesystem operativo, calendario, email o bases de datos;
- triggers UI o integraciones que disparen ejecucion.

## Active vs runtime vs execution vs external access

`active` interno:

- estado administrativo aprobado;
- reversible mediante rollback;
- muta solo `status`, `artifact_state` o status de artifact manifest;
- no ejecuta agentes, equipos, tools ni memoria;
- exige approval y audit evidence.

`runtime`:

- fase futura para preparar componentes ejecutables;
- requiere contrato especifico antes de existir;
- no esta implementado ni habilitado.

`execution`:

- fase futura para correr agentes/equipos o coordinar tareas reales;
- requiere runtime contract, execution contract, permisos, auditoria persistente, observabilidad y rollback operacional.

`external_access`:

- cualquier salida fuera de la frontera interna: tools reales, APIs, filesystem operativo, navegador, email, calendario, bases de datos, internet o integraciones;
- requiere politica y autorizacion explicita futura;
- permanece bloqueado.

## Lugares donde aparece la frontera runtime

| Archivo | Rol | Estado |
| --- | --- | --- |
| `core/active_contract.py` | Detecta flags runtime/execution/external antes de `active` | Bloquea |
| `core/active_executor.py` | Aplica `active` interno | Bloquea y no muta runtime |
| `core/capability_policy_schema.py` | Politica declarativa de capabilities | Bloquea runtime/execution/external |
| `core/sandbox_agent_memory_contract.py` | Contrato de memoria futura | Declarativo, sin persistence real |
| `core/sandbox_agent_tool_contract.py` | Contrato de herramienta futura | Declarativo, sin ejecucion |
| `core/promotion_executor.py` | Promueve estados intermedios | Bloquea `requested_status=active` |
| `core/promotion_gate.py` | Gate previo a promotion | Bloquea runtime flags y estados no operativos |

## Targets runtime futuros

Targets con runtime directo futuro:

- `agent`: puede requerir runtime contract antes de cualquier ejecucion real.
- `team`: puede requerir runtime contract y orquestacion antes de coordinar miembros.

Targets con impacto indirecto:

- `domain`: agrupa artefactos y estado, pero no debe ejecutar por si mismo.
- `capability_policy`: declara permisos futuros, pero no concede ejecucion.
- `memory_contract`: declara memoria futura, pero no crea almacenamiento real.
- `tool_contract`: declara herramientas futuras, pero no crea adapters ni clients.

Targets sin runtime directo:

- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- artifacts documentales o seed data.

## Matriz de requisitos antes de runtime

| Requisito | Dominio | Agente | Equipo | Tools/Memoria | Estado |
| --- | --- | --- | --- | --- | --- |
| Runtime contract | Indirecto | Requerido | Requerido | Requerido para adapters/storage | `REQUIRED_BEFORE_RUNTIME` |
| Execution contract | Indirecto | Requerido | Requerido | Requerido para llamadas reales | `REQUIRED_BEFORE_EXECUTION` |
| Approval persistente | Requerido | Requerido | Requerido | Requerido | `REQUIRED_BEFORE_RUNTIME` |
| Audit log persistente | Requerido | Requerido | Requerido | Requerido | `FUTURE_OBSERVABILITY` |
| Observabilidad | Requerida | Requerida | Requerida | Requerida | `FUTURE_OBSERVABILITY` |
| Permisos por actor | Requeridos | Requeridos | Requeridos | Requeridos | `FUTURE_AUTH` |
| Politica de external access | Indirecta | Requerida si aplica | Requerida si aplica | Requerida | `REQUIRED_BEFORE_EXTERNAL_ACCESS` |
| Secrets handling | Indirecto | Requerido si aplica | Requerido si aplica | Requerido | `REQUIRED_BEFORE_EXTERNAL_ACCESS` |
| Timeouts, cancelacion y rate limits | Indirecto | Requeridos | Requeridos | Requeridos | `REQUIRED_BEFORE_EXECUTION` |
| Rollback/disable runtime | Requerido | Requerido | Requerido | Requerido | `REQUIRED_BEFORE_RUNTIME` |

## Bloqueadores clasificados

| Bloqueador | Clasificacion |
| --- | --- |
| No existe runtime contract | `REQUIRED_BEFORE_RUNTIME` |
| No existe execution contract | `REQUIRED_BEFORE_EXECUTION` |
| No existe runtime executor | `REQUIRED_BEFORE_RUNTIME` |
| No existe execution executor | `REQUIRED_BEFORE_EXECUTION` |
| Audit log persistente no consolidado | `FUTURE_OBSERVABILITY` |
| Observabilidad operacional no definida | `FUTURE_OBSERVABILITY` |
| Permisos reales por actor no definidos | `FUTURE_AUTH` |
| Politica de herramientas reales no definida | `REQUIRED_BEFORE_EXECUTION` |
| Memoria persistente real no definida | `REQUIRED_BEFORE_RUNTIME` |
| Secrets handling no definido | `REQUIRED_BEFORE_EXTERNAL_ACCESS` |
| External access policy no definida | `REQUIRED_BEFORE_EXTERNAL_ACCESS` |
| Failure handling/cancelacion/timeouts/rate limits no definidos | `REQUIRED_BEFORE_EXECUTION` |
| Invocacion de modelos por agente no definida | `REQUIRED_BEFORE_RUNTIME` |
| Contrato de input/output runtime no definido | `REQUIRED_BEFORE_RUNTIME` |
| Orquestacion ejecutable de equipos no definida | `REQUIRED_BEFORE_EXECUTION` |
| UI trigger contract no definido | `FUTURE_UI` |
| Integraciones externas no definidas | `FUTURE_INTEGRATION` |

## Respuestas de arquitecto

A. Que es runtime:

Runtime es la capa futura que permitiria preparar o ejecutar comportamiento operativo real. Incluye ejecucion de agentes/equipos, tools reales, memoria persistente, adapters, clients, integraciones externas, invocacion de modelos, orquestacion ejecutable y triggers UI.

B. Que no es runtime:

No es `active` interno, no es un preset, no es un profile catalog, no es un paper seed, no es una capability policy declarativa, no es un contrato de memoria/tool declarado, y no es un estado administrativo reversible.

C. Targets que podrian tener runtime:

`agent` y `team` son los targets principales. `domain`, `capability_policy`, `memory_contract` y `tool_contract` participan como contexto o guardrails.

D. Targets que no deberian tener runtime directo:

`profile_catalog`, `agent_preset`, `paper_seed` y artefactos documentales.

E. Que queda bloqueado hoy:

`runtime_enabled=true`, `execution_enabled=true`, `execution_allowed=true`, `external_access=true`, `runtime_active_future`, `external_active_future`, `requested_status=active` via promotion executor, tools reales, memoria persistente real, UI triggers e integraciones.

F. Donde se bloquea:

`active_contract`, `active_executor`, `capability_policy_schema`, `sandbox_agent_memory_contract`, `sandbox_agent_tool_contract`, `promotion_gate` y `promotion_executor`.

G. Diferencia entre active y runtime:

`active` es estado interno aprobado y reversible. Runtime es capacidad futura de preparacion/operacion ejecutable. Estar `active` no implica poder ejecutar.

H. Diferencia entre runtime y execution:

Runtime prepara o habilitaria componentes ejecutables bajo contrato. Execution es la corrida efectiva de agentes, equipos, herramientas o procesos.

I. Diferencia entre execution y external access:

Execution puede ser interna. External access es cualquier cruce fuera del sistema interno hacia tools, APIs, filesystem operativo, internet o integraciones.

J. Memoria:

La memoria actual es declarativa. `runtime_enabled=false`, `persistence=none` y `storage_backend=none` son la frontera actual. Memoria persistente real requiere contrato futuro.

K. Herramientas:

Las herramientas actuales son declarativas. `runtime_enabled=false`, `execution_allowed=false` y `external_access=false` bloquean ejecucion y acceso externo.

L. Politicas:

Las capability policies no conceden runtime. Solo declaran posibilidad futura y validan que runtime, execution y external access permanezcan false.

M. Readiness:

El sistema queda `RUNTIME_READY_FOR_CONTRACT_ONLY`: listo para disenar el contrato runtime, no para ejecutar runtime.
