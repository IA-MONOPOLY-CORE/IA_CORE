# Contrato capability_policy para sandbox

## 1. Que es capability_policy

`capability_policy` es una capa declarativa de validacion para capabilities de agentes y equipos sandbox.

No ejecuta agentes, no ejecuta equipos, no crea memoria real, no crea herramientas reales, no llama APIs y no concede permisos operativos.

Regla central:

```txt
declared
!= allowed_by_policy
!= enabled
!= runtime
!= execution
```

En esta fase solo se permite:

```txt
declared + policy validated
```

## 2. Sujetos

Sujetos soportados:

- `agent`;
- `team`.

Una policy debe apuntar a un `subject_type`, `subject_id` y `domain_id` concretos. La validacion de sujeto impide reutilizar una policy de equipo como si fuera de agente, o una policy de agente como si fuera de equipo.

## 3. Tipos de capability

Tipos soportados inicialmente:

- `memory`;
- `tool`;
- `policy`.

`memory` representa memoria futura declarativa.

`tool` representa herramientas futuras declarativas.

`policy` representa reglas futuras de gobierno declarativo.

## 4. Estados

Estados de policy:

- `declared`: capability declarada, no autorizada;
- `allowed_declared`: capability autorizada solo como declarativa;
- `blocked`: capability bloqueada;
- `forbidden`: capability prohibida;
- `future_requires_approval`: capability que requerira approval real en una fase posterior.

Reglas:

- `allowed_by_policy=true` solo puede existir con `allowed_declared`;
- `requires_approval=true` solo puede existir con `future_requires_approval`;
- `future_requires_approval` exige `approval_status=future_required`;
- `blocked` y `forbidden` no pueden ser `allowed_by_policy=true`.

## 5. Frontera runtime

Confirmado:

```txt
policy validated
!=
enabled
!=
runtime
!=
execution
```

Toda `capability_policy` valida exige:

- `declared_only=true`;
- `runtime_enabled=false`;
- `execution_allowed=false`;
- `external_access=false`.

Bloqueos por tipo:

- memory: sin storage backend real, sin vector store real, sin persistencia operativa real;
- tool: sin ejecucion, sin external access, sin API call real, sin escritura filesystem real, sin browser/email/calendar automation real;
- policy: sin self-approval, sin auto-escalation, sin runtime mutation.

## 6. Reglas de equipo

Una capability del equipo no habilita automaticamente capabilities operativas en agentes miembros.

Una policy con `subject_type=team` regula al equipo como sujeto. No hereda permisos hacia `member_agents`, no activa agentes y no concede tools/memory a los miembros.

Quedan bloqueados flags declarativos como:

- `auto_enable_members`;
- `auto_apply_to_members`;
- `grant_to_members`;
- `inherits_to_members`.

## 7. Relacion con artifact_manifest

En este prompt no se materializa `capability_policy` como artefacto operativo.

Si en una fase futura la policy necesita versionado, rollback, auditoria independiente o aprobaciones persistentes, podria corresponder:

```txt
artifact_type: capability_policy
```

No se agrega al `artifact_manifest` actual porque todavia no existe materializacion de policy ni approval workflow real.

## 8. Futuro

Queda para fases posteriores:

- approval real;
- permisos efectivos;
- audit log persistente;
- auditoria de ejecucion;
- memoria persistente;
- tools reales;
- runtime;
- UI;
- integraciones.
