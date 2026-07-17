# Active boundary audit

## 1. Resumen ejecutivo

`active` en IA_CORE significa que un dominio, artefacto o entidad empieza a ser considerado usable por el sistema.

No es un alias de:

```txt
materialized
validated
candidate_for_activation
```

Regla central:

```txt
candidate_for_activation != active
validated != active
```

En esta etapa, `active` no debe implicar runtime automatico. Tambien sigue bloqueado como destino de `promotion_gate`, `approval_workflow`, `promotion_executor` y contratos sandbox.

Veredicto de readiness:

```txt
ACTIVE_BOUNDARY_READY_BUT_RUNTIME_MISSING
```

La frontera conceptual esta clara y testeada. Faltan contratos de runtime, execution, observability, permisos, persistencia de approvals/audit y rollback desde active antes de implementar activacion real.

## 2. Significado por target

| Target | Que significaria active | Permitido hoy | Motivo |
| --- | --- | --- | --- |
| domain | Dominio visible/usable por flujos backend y potencialmente UI | No | Falta contrato active, visibilidad, rollback y audit persistente |
| profile_catalog | Catalogo de perfiles consumible como fuente operativa del dominio | No | Falta aprobacion active y versionado operativo |
| agent_preset | Presets disponibles para crear agentes operativos | No | Falta contrato de activacion y permisos |
| paper_seed | Paper seed aprobado como insumo operativo del dominio | No | Falta aprobacion active y trazabilidad persistente |
| agent | Agente usable como entidad operativa | No | Falta runtime/execution/memory/tool contract real |
| team | Equipo usable como coordinacion operativa | No | Falta orquestacion, permisos y observabilidad |
| capability_policy | Politica aplicable por enforcement real | No | Hoy es declarativa y bloquea runtime/execution/external_access |
| memory | Memoria persistente disponible para runtime | No | Falta contrato de persistencia, scope, retencion y auditoria |
| tool | Herramienta ejecutable o invocable | No | Falta permission enforcement, sandboxing, audit y failure handling |

## 3. Capas de active

| Capa | Definicion | Estado actual |
| --- | --- | --- |
| active as visible | Puede aparecer como usable/seleccionable | No definido para sandbox active |
| active as usable | Puede ser consumido por flujos backend | No permitido por promotion executor |
| active as executable | Puede ejecutar agentes/equipos/herramientas | Bloqueado |
| active as runtime-enabled | Tiene runtime habilitado | Bloqueado |
| active as externally connected | Puede llamar sistemas externos | Bloqueado |

Decision actual:

```txt
active futuro no debe activar runtime automaticamente.
```

Si en el futuro `active` implica visibilidad o usabilidad, runtime/execution/external access deben seguir siendo permisos separados con contrato propio.

## 4. Matriz de requisitos minimos para active

| Target | Requisitos minimos antes de active |
| --- | --- |
| domain | cadena completa validada; promotion gate active especifica; approval decision valida; audit event persistente; rollback plan; no legacy contamination; contrato de visibilidad; runtime boundary definido |
| profile_catalog | dominio candidato; catalogo validado; version y checksum; approval active; audit persistente; rollback de version |
| agent_preset | profile_catalog active o equivalente aprobado; presets validados; modelo/proveedor resuelto; approval active; bloqueo de auto-runtime |
| paper_seed | paper_seed validado; lineage a dominio/agentes; approval active; politica de versionado; rollback documental |
| agent | sandbox_agent validated/candidate; lineage valido; paper_seed aprobado; capability_policy aprobada; memory/tool policies resueltas; runtime contract; execution contract; audit persistente |
| team | agentes miembros validados; coordinacion declarativa validada; capability_policy de equipo; reglas de permisos; contrato de orquestacion; rollback y observabilidad |
| capability_policy | enforcement engine definido; actor/auth real; scope de permisos; decision persistente; audit persistente; revocacion |
| memory | storage backend real; retention; ownership; privacy; rollback/revocation; observability |
| tool | permission enforcement; sandboxing; external access policy; failure handling; audit; rate limits |

## 5. Bloqueadores actuales

| Bloqueador | Clasificacion | Estado |
| --- | --- | --- |
| active promotion executor | REQUIRED_BEFORE_ACTIVE | No implementado; executor solo permite `validated` y `candidate_for_activation` |
| runtime contract | FUTURE_RUNTIME | Falta definir runtime sin activacion automatica |
| execution contract | FUTURE_RUNTIME | Falta contrato de ejecucion para agentes/equipos |
| permission enforcement | REQUIRED_BEFORE_ACTIVE | Capability policy es declarativa, no enforcement |
| persistent audit log | FUTURE_OBSERVABILITY | Audit event existe como payload, falta persistencia operacional |
| auth/actor real | FUTURE_AUTH | Approval usa actores declarativos |
| approval persistence | REQUIRED_BEFORE_ACTIVE | Approval existe como contrato, falta lifecycle persistente |
| memory persistence | FUTURE_RUNTIME | Memoria sandbox declarativa, sin storage real |
| tool execution | FUTURE_RUNTIME | Herramientas declarativas, execution_allowed=false |
| failure handling | REQUIRED_BEFORE_ACTIVE | Falta contrato de fallo/rollback desde active |
| observability | FUTURE_OBSERVABILITY | Falta metricas/eventos persistentes |
| UI visibility contract | FUTURE_UI | Falta decidir visible vs usable |
| rollback from active | REQUIRED_BEFORE_ACTIVE | Solo existe rollback de promocion intermedia |
| external integrations | FUTURE_INTEGRATION | External access bloqueado |
| legacy cleanup | NOT_REQUIRED_FOR_ACTIVE | Ya existe aislamiento, debe mantenerse como guardrail |

## 6. Evidencia de bloqueo actual

`active` aparece como estado global en `core/artifact_state.py` y `core/domain_state.py`.

Queda bloqueado por:

- `core/promotion_gate_schema.py`: `active` debe quedar `blocked`;
- `core/promotion_gate.py`: `requested_status=active` agrega blocker;
- `core/promotion_executor_schema.py`: solo acepta `validated` y `candidate_for_activation`;
- `core/promotion_executor.py`: bloquea requested_status activo o invalido;
- `core/approval_workflow.py`: no crea approval request para `active`;
- `core/approval_workflow_schema.py`: no permite requested_status `active`;
- `core/sandbox_domain_schema.py`: sandbox `active` requiere PASSED completo y queda fuera de esta fase;
- `core/sandbox_agent_schema.py`: agente sandbox no puede estar `active`;
- `core/sandbox_team_schema.py`: equipo sandbox no puede estar `active`;
- `core/capability_policy_schema.py`: runtime, execution y external access deben ser false.

## 7. Readiness

Pregunta:

```txt
IA_CORE esta listo para implementar active real?
```

Respuesta:

```txt
ACTIVE_BOUNDARY_READY_BUT_RUNTIME_MISSING
```

La frontera esta suficientemente clara para disenar un contrato `active`, pero no para implementarlo como estado operativo real.

## 8. Auditoria arquitectonica final

A. `active` significa usable/operativo por el sistema, no simplemente escrito en filesystem.

B. `active` no implica runtime ahora.

C. En el futuro, `active` tampoco deberia implicar runtime automaticamente; deberia habilitar una capa de usabilidad separada de execution/runtime/external access.

D. Podrian llegar a `active`: domain, profile_catalog, agent_preset, paper_seed, agent, team y capability_policy, con contrato especifico.

E. No deberian llegar a `active` por este flujo: memory y tool como ejecucion directa sin policy/enforcement; legacy, broken y archived.

F. Falta active promotion contract, enforcement, audit persistente, approval persistence, rollback desde active y contrato de visibilidad.

G. Antes de runtime faltan runtime contract, execution contract, memoria real, herramientas reales, permisos, sandboxing y failure handling.

H. Antes de UI falta contrato de visibilidad, estados mostrables, acciones permitidas y mensajes de bloqueo.

I. Antes de integraciones falta external access policy, secrets, rate limits, audit y revocacion.

J. Proximo paso recomendado:

```txt
active contract
```

Despues deberian venir observability/audit persistence y runtime contract. Runtime no debe ser el siguiente paso inmediato.
