# GOKV 0.1 - Arquitectura y boundary del Cofre Global de Capacidad Operacional

## Gate

`N1_GOKV_ARCHITECTURAL_BOUNDARY_PASSED`

## Resultado ejecutivo

IA_CORE no tenía un GOKV equivalente al inicio de este bloque. El repositorio
sí tiene piezas que deben reutilizarse como fuentes o boundaries: memoria de
agentes, boundary contractual de contexto, audit trail append-only,
observabilidad, lifecycle writer, registries de dominios y schemas de
artefactos. Ninguna de esas piezas representa por sí sola conocimiento
operacional versionado, portable, seleccionable por misión y separado de la
experiencia que lo originó.

La ubicación canónica elegida es:

```text
knowledge/global_operational/
```

Los helpers de desarrollo viven en:

```text
gokv/
```

`gokv/` no se importa desde `api.py`, UI, runtime, execution, providers,
integrations ni agentes productivos. Su única responsabilidad en 0.1 es
validar, almacenar, capturar y compilar artefactos de desarrollo.

## Auditoría de piezas existentes

| Pieza existente | Evidencia | Se reutiliza como | No se reutiliza como |
| --- | --- | --- | --- |
| `memory/`, `memoria_agentes/`, `core/memoria_perpetua.py` | Memoria de usuario/agente y memoria vectorial | Boundary y fuente privada | Knowledge global o registry GOKV |
| `core/context_boundary.py` | Clasificación contractual, redaction y sandbox | Regla de frontera y seguridad | Retrieval, RAG o expansión de conocimiento |
| `core/audit_store.py`, `core/audit_log_schema.py` | Audit trail append-only de decisiones | Principio de inmutabilidad y evidencia | Storage de knowledge items |
| `core/observability.py`, `core/observability_schema.py` | Observabilidad de operaciones internas | Referencia para métricas y trazabilidad | Learning event o promoción |
| `core/lifecycle_writer.py` | Escritura de lifecycle de artefactos | Referencia de transiciones explícitas | Lifecycle epistemológico GOKV |
| `core/domain_registry.py`, `core/catalog_registry.py` | Registry de dominios y catálogos | Patrón de registry tipado | Registry de conocimiento |
| `core/*_schema.py` | Schemas machine-readable existentes | Convenciones de validación | Contrato GOKV completo |
| `domains/*/agents/papers/` | Identidad y material de agentes por dominio | Fuente privada con scope declarado | Knowledge global |
| `catalogs/`, `presets` y snapshots | Catálogos y salidas derivadas | Evidencia contextual | Principios operacionales universales |

## Boundary table

| Concepto | Qué conserva | Autoridad | Persistencia | Puede alimentar GOKV |
| --- | --- | --- | --- | --- |
| `MEMORY` | Información de usuario/agente, preferencias o historial privado | Agente/usuario/dominio | Memoria privada | Solo como experiencia sanitizada y abstraída |
| `CONTEXT` | Material que podría entrar en una tarea o decisión | Boundary contractual | No implica persistencia | Solo como referencia de regla, nunca como expansión automática |
| `EVIDENCE` | Prueba, test, commit, diff o checkpoint observable | Repositorio/Git/tests | Inmutable por referencia | Sí, es requisito de validación |
| `LOG` | Registro temporal o operacional de eventos | Sistema de observabilidad | Append-only según store | Sí, como fuente de `LEARNING_EVENT`, no como knowledge |
| `PAPER` | Identidad, rol e instrucciones de un agente | Dominio/agente | Archivo de dominio | No global por defecto; scope privado |
| `PRESET` | Configuración o recomendación derivada | Catálogo/dominio | Versionada por catálogo | Solo como evidencia de diseño, no como principio global |
| `OPERATIONAL_KNOWLEDGE` | Regla, procedimiento, patrón, recovery o criterio reutilizable | GOKV y su lifecycle | Git, versionado, registry e índices | Es el destino de la abstracción validada |

## Ownership table

| Artefacto | Owner | Puede crear | Puede promover |
| --- | --- | --- | --- |
| Observación/experiencia | Proceso de captura | Helper GOKV | Nadie automáticamente |
| `LEARNING_EVENT` | IA_CORE build | Pipeline development-only | No promueve knowledge |
| `KNOWLEDGE_ITEM` | IA_CORE/GOKV | Curador o captura validada | Solo transición explícita con evidencia |
| Evidence reference | Git/tests/checkpoints | Validator | No se edita desde GOKV |
| Registry/index | GOKV | Rebuild determinista | No cambia estados por inferencia |
| Execution Pack | Compiler development-only | Selector determinista | No activa agentes ni runtime |
| Scope/privacy | Owner del dato | Validator + revisión humana | Nunca por similitud o conveniencia |

## Data classification table

| Clase | Permitida en GOKV global | Tratamiento |
| --- | --- | --- |
| Regla abstraída de IA_CORE_BUILD | Sí | `GLOBAL` o `IA_CORE_BUILD`, con commits y checkpoints |
| Experiencia de una misión | No directamente | Capturar como event; abstraer antes de globalizar |
| Datos de empresa, cliente o dominio privado | No | Mantener `BUSINESS`, `TEAM`, `AGENT` o `TASK` |
| Credenciales, secretos o payload privado | Nunca | Rechazar y no persistir |
| Conversation completa o chain-of-thought | Nunca | Solo resultados reutilizables, no razonamiento privado |
| Test/diff/commit público del repo | Sí, si es relevante | Referencia de evidencia, sin copiar secretos |

## Scope model

Los scopes disponibles son `GLOBAL`, `IA_CORE_BUILD`, `DOMAIN`, `BUSINESS`,
`TEAM`, `AGENT` y `TASK`.

- `GLOBAL`: abstracción generalizable y sin datos privados.
- `IA_CORE_BUILD`: conocimiento válido para construir IA_CORE.
- `DOMAIN`: específico de un dominio operativo.
- `BUSINESS`: privado de una empresa.
- `TEAM`: privado de un equipo.
- `AGENT`: privado de un agente.
- `TASK`: limitado a una misión.

La ruta empresa → experiencia → abstracción → validación → conocimiento global
queda diseñada como frontera futura, pero no se implementa en 0.1.

## Status model

GOKV separa experiencia de conocimiento. Un evento observado puede producir una
propuesta, pero nunca salta silenciosamente a `PROMOTED`.

```text
OBSERVED -> CANDIDATE -> VALIDATED -> PROMOTED
PROMOTED -> REVISED
PROMOTED -> DEPRECATED
DEPRECATED -> REPLACED
```

`REPLACED` exige referencia explícita al reemplazo. No se borra historia y una
versión nueva no puede retroceder silenciosamente.

## Colisiones evitadas

- Memory conserva datos de agente; GOKV conserva reglas abstraídas.
- Context boundary decide si un contexto podría usarse; GOKV no recupera ni inyecta contexto.
- Evidence demuestra; GOKV interpreta esa evidencia en un item versionado.
- Logs registran ocurrencias; GOKV registra aprendizaje estructurado.
- Papers describen identidad; GOKV no reemplaza instrucciones de agentes.
- Presets configuran; GOKV no habilita capacidades.

## Non-goals de GOKV 0.1

- Runtime learning.
- Invocación de modelos o agentes.
- Embeddings, vector DB, Chroma o RAG.
- APIs nuevas, endpoints, network o integrations.
- Promoción autónoma.
- Comunicación multiempresa o multi-tenant.
- Modificación de memory, UI, backend, payload, runtime o execution.
- Presentar una experiencia como verdad universal.

## Superficies protegidas

GOKV 0.1 no modifica estas superficies productivas:

- `ui/web/index.html`
- `ui/web/styles.css`
- `ui/web/i18n_es.json`
- `ui/web/backend-contract-widgets.js`
- `core/backend_internal_ui_payloads.py`
- `api.py`
- `backend/`, `runtime/`, `execution/`, `providers/` e `integrations/`
- memory, papers, presets y dominios productivos.

## Tree target

```text
knowledge/global_operational/
  schema/
  items/
  events/
  metrics/
  packs/
  registry.json
gokv/
  __init__.py
  schema.py
  storage.py
  capture.py
  compiler.py
```

El árbol es development-time, legible por Git y portable. La ausencia de
runtime integration es deliberada y forma parte del contrato.

## Primary evidence

- `core/context_boundary.py` y `docs/CONTEXT_BOUNDARY_POLICY.md`.
- `core/audit_store.py`, `core/audit_log_schema.py` y `docs/AUDIT_STORE_APPEND_ONLY.md`.
- `core/observability*.py` y `docs/OBSERVABILITY_CONTRACT.md`.
- `core/lifecycle_writer.py` y `docs/LIFECYCLE_WRITER_CONTRACT.md`.
- `core/domain_registry.py`, `core/catalog_registry.py` y `ARCHITECTURE_DECISIONS.md`.
- UI/UX 1.194-1.199, especialmente el Decision Sheet y el grafo post-Dirección.

## Gate result

`N1_GOKV_ARCHITECTURAL_BOUNDARY_PASSED`

No se modifican las ocho decisiones de UI/UX 1.199 ni se ejecuta UI/UX 1.200.
