# IA_CORE Security Layer — Attack Surface Audit

Estado: `IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED`

Veredicto: `SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT`

Readiness: `ready_for_agent_permission_contract`

Proximo paso: `PROMPT 3.22 — Contrato de permisos por agente`

## Objective

Esta auditoría identifica la superficie de ataque actual y futura de IA_CORE antes de habilitar runtime, tools, memoria persistente, external access, API/UI, writes reales, stores operativos o integraciones externas.

La auditoría es defensiva.
No implementa capacidades ofensivas.
No habilita ejecución real.
No prueba targets externos.
No incorpora repos externos.
No activa conectores.

## Current attack surface

| Componente | propósito actual | estado actual | superficie de ataque | riesgo si se activa antes de tiempo | boundary actual | controles necesarios antes de runtime |
| --- | --- | --- | --- | --- | --- | --- |
| ExecutionIntent | representar intención operacional futura | contract-only | intent metadata, constraints, target refs | crear intención ejecutable sin permisos | no runtime, no attempt creation | permission contract, lineage validation, default deny policy |
| attempt factory contract | construir attempts contractuales en memoria | contract-only | intent-to-attempt derivation, idempotency, lineage | generar attempts operativos o estados queued/running | in-memory only, disabled flags | agent identity, capability registry, approval gate |
| ExecutionAttempt en memoria | schema de intento futuro | schema-only | attempt_id, status, metadata, lineage | persistir intento no autorizado | no persistence | idempotency validation, write policy, lineage validation |
| ExecutionAttempt state machine | validar estados y transiciones | contract-only | transitions, future runtime states | aceptar queued/running sin scheduler seguro | runtime states blocked | permission contract, runtime gate, audit trail |
| attempt store write-safe contract | simular would_write sin persistir | contract-only | write_ref conceptual, idempotency, duplicate policy | convertir would_write en write real | persisted False, no store writes | write policy, rollback/compensation policy, immutable audit trail |
| lifecycle writer contract | simular would_emit sin emitir | contract-only | lifecycle event metadata, state transition refs | emitir eventos reales o mutar lifecycle_store | emitted False, no lifecycle_store writes | event permission, idempotency validation, audit trail |
| OperationalReadinessGate contract-only | evaluar readiness pre-operational | read-only/contract-only | gate decision, blockers, readiness labels | abrir operación sin Security Layer | no operational gate enabled | runtime gate, approval gate, risk report |
| ExecutionResult contract | representar resultado futuro | read-only contract | result_id, summary, artifacts metadata | crear resultados con payload real o output_ref sensible | no result store, no output_ref | output policy, secret redaction, result store policy |
| execution result projection | proyectar resultados seguros en memoria | read-only projection | history/read model fields | filtrar payload sensible a vistas | no projection writes | projection policy, field denylist, provenance tracking |
| execution history view | vista derivada desde stores preflight | derived-only/read-only | timeline, refs, summaries | crear history store o exponer payload real | no history store, no JSONL history | read model policy, payload filter, audit trail |
| internal backend read model | snapshot interno read-only | read-only | source refs, domain refs, summaries | abrir API/dashboard o mutar estado | no API, no mutation, no store | source verification, output policy, access gate |
| attempt_store | store operativo de attempts | absent/not_active | future persistent attempt records | corrupción, replay o writes no auditados | no file present | write policy, append-only/idempotency, rollback |
| lifecycle_store | store operativo lifecycle | absent/not_active | future transition/event records | lineage tampering o event replay | no file present | immutable audit trail, transition policy |
| dry_run_store | JSONL append-only de dry-run result-only | limited append-only/preflight | dry-run entries, checksum, store path | confundir dry-run con execution attempt | no attempts, no agents, no runtime | store path policy, checksum, idempotency, audit refs |
| Market Catalog planned_not_active | database no activa de mercados | planned_not_active | external market categories, mappings | activar mercado como runtime/BCL | no runtime, not_evaluated entries | activation gate, provenance, risk scoring |
| Business Composition Layer futura/no operativa | composición futura de unidades de negocio | future/non-operational | markets + niches + profiles + teams | crear negocio/equipo operativo sin permisos | no module/runtime | permission contract, approval gate, security E2E checkpoint |

## Future attack surface

| Superficie | rol futuro | riesgo principal | ataque posible | impacto | controles mínimos requeridos | estado actual |
| --- | --- | --- | --- | --- | --- | --- |
| runtime runner | ejecutar attempts aprobados | ejecución no autorizada | activar ejecución desde contrato incompleto | critical | runtime gate, permission contract, audit trail, kill switch | blocked |
| scheduler | programar ejecución | tareas persistentes indebidas | schedule sin aprobación | high | schedule policy, approval gate, audit trail | blocked |
| worker | procesar jobs | ejecución fuera de permisos | worker procesa payload no confiable | high | worker sandbox, capability registry | blocked |
| queue | encolar attempts | replay o queue poisoning | insertar job mal clasificado | high | queue policy, idempotency validation | blocked |
| model invocation | llamar modelos | fuga de secretos o prompt no aprobado | prompt con datos sensibles | high | prompt policy, secret redaction, permission contract | blocked |
| tool execution | ejecutar tools | abuso de capacidades | tool fuera de allowlist | critical | tool allowlist, tool denylist, sandbox policy | blocked |
| memory persistence | guardar memoria | memory poisoning | persistir instrucción maliciosa | high | memory write policy, provenance tracking | blocked |
| external access | red/red externa | fuga o acción externa indebida | request no aprobado | critical | external access gate, data classification | blocked |
| API | interfaz programática | bypass de UI/gate | endpoint crea operación directa | high | auth, permission contract, audit trail | blocked |
| UI | interfaz humana | bypass visual o estado engañoso | acción irreversible sin approval | high | UI permission mapping, approval gate | blocked |
| UI-TARS runtime | operador visual / GUI operator | acciones no autorizadas sobre pantalla | prompt injection visual o click irreversible | critical | sandbox, permisos explícitos, screen redaction, action allowlist, audit trail, kill switch | future_only |
| Hermes runtime | orquestador subordinado | orquestación no autorizada | skill/cron fuera de permisos | critical | permisos por skill, agent identity, schedule policy, kill switch | future_only |
| n8n workflows reales | workflows/conectores | abuso de webhooks y conectores | envío de datos sensibles | high | connector allowlist, secrets policy, approval gate | future_only |
| Home Assistant actions reales | puente físico/local | acción física insegura | automatización peligrosa | critical | physical safety policy, device allowlist, approval gate, kill switch | future_only |
| agent teams | equipos de agentes | escalamiento lateral entre roles | agente asume rol ajeno | high | team permission map, role binding | future_only |
| agent presets | presets de agente | preset con capacidades excesivas | preset activa tool no permitida | medium | preset validation, capability registry | future_only |
| professional library | biblioteca profesional | perfil mal mapeado a permisos | rol recibe capability incorrecta | medium | role/specialization binding, review gate | not_active_for_runtime |
| Business Composition Layer runtime | componer negocios/equipos | activación comercial sin control | mercado crea unidad operativa automática | critical | BCL gate, approval gate, risk report | future_only |
| Market Catalog runtime | activar mercados | market activation bypass | rubro externo dispara flujos | high | activation gate, provenance, risk scoring | blocked |
| document ingestion | ingerir documentos | document injection | documento malicioso altera instrucciones | high | document trust level, parser sandbox | future_only |
| web ingestion | ingerir web | webpage/UI injection | contenido web intenta cambiar políticas | high | web trust level, prompt injection filter | future_only |
| image/screenshot ingestion | leer imágenes/pantallas | malicious screenshots | texto visual induce acción | high | screenshot trust level, screen redaction | future_only |
| prompt templates | plantillas | injection persistente | template incluye instrucciones no permitidas | high | template review, provenance tracking | future_only |
| approval flows | aprobaciones | approval bypass | acción se marca aprobada sin humano | critical | human-in-the-loop policy, audit trail | future_only |
| human-in-the-loop actions | intervención humana | ambigüedad o bypass | confirmación falsa o fuera de contexto | high | explicit approval, irreversible action policy | future_only |
| secrets/config/env | configuración sensible | secret leakage | secreto entra en prompt/log | critical | secret storage policy, secret redaction | blocked |
| logs/audit trail | trazabilidad | audit trail tampering | borrar o alterar evidencia | critical | immutable audit trail, append-only policy | future_only |
| rollback/compensation | reversión | rollback failure | write sin compensación | high | rollback/compensation policy, idempotency | future_only |
| kill switch | apagado de emergencia | kill switch failure | no poder detener runtime | critical | kill switch always available, tested controls | future_only |

## Threat categories

| Amenaza | descripción | superficie afectada | ejemplo defensivo/controlado | impacto potencial | control mínimo requerido | requiere permiso explícito |
| --- | --- | --- | --- | --- | --- | --- |
| prompt injection | input intenta alterar instrucciones del sistema | prompts, documents, web, UI | fixture con texto no confiable intenta cambiar reglas | policy bypass | prompt injection filter | yes |
| jailbreak attempts | input intenta evadir restricciones | model invocation, prompt templates | caso de prueba pide ignorar límites | unsafe behavior | model policy + refusal checks | yes |
| tool abuse | uso de herramienta fuera de propósito | tool execution, UI-TARS, Hermes | tool simulado solicita acción fuera de allowlist | side effects | tool allowlist/denylist | yes |
| permission bypass | saltar permisos por rol | all runtime surfaces | agente intenta capability ajena en sandbox | privilege escalation | permission contract | yes |
| secret leakage | exponer secretos en prompts/logs | secrets/config/env, logs, model calls | fixture contiene token falso y debe redactarse | data exposure | secret redaction/storage policy | yes |
| memory poisoning | contaminar memoria persistente | memory persistence | entrada no confiable intenta persistir regla falsa | long-term compromise | memory provenance and write gate | yes |
| document injection | documento con instrucciones maliciosas | document ingestion | documento de prueba intenta cambiar rol | policy bypass | document trust level | yes |
| webpage/UI injection | página o UI intenta dirigir acciones | web ingestion, UI | HTML de prueba contiene instrucciones hostiles | unauthorized action | web trust level + filter | yes |
| malicious screenshots | imagen contiene texto adversarial | image/screenshot ingestion, UI-TARS | screenshot fixture pide click irreversible | visual prompt injection | screenshot trust level | yes |
| malicious external content | contenido externo no confiable | web, connectors, APIs | payload externo marcado untrusted | data/control injection | provenance tracking | yes |
| unsafe writes | escritura sin política | stores, files, DB | write simulado sin rollback es bloqueado | corruption | write policy | yes |
| store corruption | datos persistidos inválidos | attempt/result/lifecycle stores | JSONL fixture con checksum roto | integrity loss | checksum + validation | yes |
| lineage tampering | alterar origen o relación | attempts, results, audit | intento con lineage inconsistente | attribution failure | lineage validation | yes |
| audit trail tampering | modificar evidencia | logs/audit trail | log fixture con hash previo inválido | accountability loss | immutable audit trail | yes |
| runtime activation bypass | activar ejecución sin gate | runtime runner, gate | metadata intenta abrir runtime | critical side effect | runtime gate | yes |
| scheduler misuse | programar tareas indebidas | scheduler | schedule simulado sin approval | persistent abuse | schedule policy | yes |
| worker misuse | worker ejecuta job no autorizado | worker | job fixture sin permission ref | unauthorized execution | worker sandbox | yes |
| queue misuse | cola acepta payload malicioso | queue | replay de idempotency_key | duplicate execution | queue policy + idempotency | yes |
| model invocation misuse | llamada a modelo fuera de permiso | model invocation | prompt con datos no aprobados | leakage/unsafe output | model permission contract | yes |
| tool execution outside permissions | tool corre fuera de capabilities | tool execution | tool request no listada | system side effects | tool allowlist | yes |
| external access outside permissions | salida externa no permitida | external access, n8n | request simulado a conector no aprobado | exfiltration/side effect | external access gate | yes |
| UI-TARS unauthorized actions | operador GUI actúa sin approval | UI-TARS runtime | acción visual irreversible en sandbox | user/system impact | approval gate + kill switch | yes |
| Hermes unauthorized orchestration | orquestador ejecuta fuera de rol | Hermes runtime | cron/skill no autorizado | persistent side effects | skill permissions | yes |
| n8n workflow abuse | workflow mueve datos indebidamente | n8n workflows reales | webhook de prueba sin allowlist | data exfiltration | connector allowlist | yes |
| Home Assistant physical-world unsafe actions | acción física riesgosa | Home Assistant actions reales | device action fixture sin safety policy | physical impact | physical safety policy | yes |
| approval bypass | aprobar sin humano válido | approval flows | approval_ref falso | irreversible action | human approval gate | yes |
| human-in-the-loop bypass | saltar revisión humana | HITL actions | acción sensible sin reviewer | governance failure | HITL policy | yes |
| rollback failure | no poder revertir | writes, stores, BCL | write simulado sin compensación | persistent corruption | rollback/compensation policy | yes |
| kill switch failure | no poder detener ejecución | runtime, tools, integrations | runtime simulado sin stop path | uncontrolled operation | kill switch | yes |
| Market Catalog activation bypass | activar mercados sin gate | Market Catalog runtime | entry pasa de planned a active sin approval | business drift | activation gate | yes |
| Business Composition Layer activation bypass | activar composición de negocio | BCL runtime | unidad operativa creada sin contrato | operational drift | BCL permission gate | yes |

## Risk matrix

| Superficie | Estado actual | Amenaza principal | Impacto | Probabilidad | Riesgo | Controles mínimos | Próximo contrato necesario |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ExecutionIntent | contract-only | permission bypass | high | medium | high | permission contract, default deny policy | Contrato de permisos por agente |
| attempt factory | contract-only | runtime activation bypass | high | medium | high | agent identity, lineage validation | Contrato de permisos por agente |
| attempt store write-safe | contract-only | unsafe writes | high | medium | high | write policy, idempotency validation | Contrato de permisos por agente |
| lifecycle writer | contract-only | lifecycle events reales | high | medium | high | event permission, immutable audit trail | Contrato de permisos por agente |
| OperationalReadinessGate | contract-only | gate bypass | critical | medium | critical | runtime gate, approval gate | Contrato de permisos por agente |
| runtime runner | blocked | runtime activation bypass | critical | medium | critical | runtime gate, kill switch | Contrato de permisos por agente |
| scheduler | blocked | scheduler misuse | high | medium | high | schedule policy, audit trail | Contrato de permisos por agente |
| worker | blocked | worker misuse | high | medium | high | worker sandbox, queue policy | Contrato de permisos por agente |
| queue | blocked | queue misuse | high | medium | high | idempotency validation, queue policy | Contrato de permisos por agente |
| model invocation | blocked | model invocation misuse | high | high | critical | model permission, prompt filter | Contrato de permisos por agente |
| tool execution | blocked | tool abuse | critical | high | critical | tool allowlist, sandbox policy | Contrato de permisos por agente |
| memory persistence | blocked | memory poisoning | high | medium | high | memory write gate, provenance | Contrato de permisos por agente |
| external access | blocked | external access outside permissions | critical | medium | critical | external access gate, data classification | Contrato de permisos por agente |
| API/UI | blocked | approval bypass | high | medium | high | auth, approval gate, audit trail | Contrato de permisos por agente |
| UI-TARS | future_only | UI-TARS unauthorized actions | critical | medium | critical | sandbox, screen redaction, kill switch | Contrato de permisos por agente |
| Hermes | future_only | Hermes unauthorized orchestration | critical | medium | critical | skill permissions, schedule policy | Contrato de permisos por agente |
| n8n | future_only | n8n workflow abuse | high | medium | high | connector allowlist, secrets policy | Contrato de permisos por agente |
| Home Assistant | future_only | Home Assistant physical-world unsafe actions | critical | low | high | physical safety policy, device allowlist | Contrato de permisos por agente |
| Market Catalog | planned_not_active | Market Catalog activation bypass | high | medium | high | activation gate, risk report | Contrato de permisos por agente |
| Business Composition Layer | future/non-operational | Business Composition Layer activation bypass | critical | medium | critical | BCL gate, approval flow | Contrato de permisos por agente |
| documents/web/images/screenshots | future_only | injection from untrusted content | high | high | critical | trust levels, prompt injection filter | Contrato de permisos por agente |
| secrets/config/env | blocked | secret leakage | critical | medium | critical | secret storage policy, redaction | Contrato de permisos por agente |
| audit trail/logs | future_only | audit trail tampering | critical | medium | critical | immutable audit trail | Contrato de permisos por agente |
| kill switch | future_only | kill switch failure | critical | low | high | kill switch tests, runtime gate | Contrato de permisos por agente |

Risk levels used: low, medium, high, critical.

## Minimum controls by surface

```txt
permission contract
capability registry
default deny policy
least privilege policy
agent identity
agent role/specialization binding
approval gate
human-in-the-loop policy
sandbox policy
tool allowlist
tool denylist
secret redaction
secret storage policy
prompt injection filter
input provenance tracking
document trust level
web trust level
screenshot trust level
lineage validation
idempotency validation
write policy
rollback/compensation policy
immutable audit trail
runtime gate
external access gate
kill switch
risk report
security E2E checkpoint
```

## Relation with next contract

El próximo paso es `PROMPT 3.22 — Contrato de permisos por agente`.

Antes de auditar secretos, prompt injection, tools, sandbox o runtime, IA_CORE necesita una forma formal de declarar qué puede hacer cada agente, bajo qué rol, con qué capacidades, con qué límites, con qué approvals y con qué surfaces bloqueadas por default.

El contrato de permisos por agente es el primer contrato de Security Layer porque todo runtime futuro depende de saber quién puede hacer qué.

## Future integrations risk map

UI-TARS:
- rol futuro: operador visual / GUI operator.
- riesgo: acciones no autorizadas sobre pantalla, lectura de datos sensibles, clicks irreversibles, prompt injection visual.
- controles mínimos: sandbox, permisos explícitos, approval gate, screen redaction, action allowlist, audit trail, kill switch.
- estado actual: future_only / not_active.

Hermes:
- rol futuro: herramienta/orquestador operativo subordinado a IA_CORE.
- riesgo: orquestación no autorizada, ejecución persistente fuera de permisos, skills peligrosas, cron no controlado.
- controles mínimos: permisos por skill, agent identity, approval gates, audit trail, schedule policy, kill switch.
- estado actual: future_only / not_active.

n8n:
- rol futuro: automatizador de workflows/conectores.
- riesgo: abuso de webhooks, conectores externos, envío de datos sensibles, workflows no aprobados.
- controles mínimos: connector allowlist, data classification, secrets policy, audit trail, approval gate.
- estado actual: future_only / not_active.

Home Assistant:
- rol futuro: puente físico/local.
- riesgo: acciones físicas inseguras, sensores sensibles, automatizaciones irreversibles o peligrosas.
- controles mínimos: physical safety policy, approval gate, local sandbox, device allowlist, kill switch.
- estado actual: future_only / not_active.

OBLITERATUS:
- no es integración de IA_CORE.
- no es dependencia.
- no forma parte del roadmap operativo.
- no debe usarse para IA_CORE runtime.
- cualquier mención queda fuera del producto y no activa componentes.

## Defensive Red Team / Adversarial Lab

Futuro Red Team Agent defensivo: solo contra agentes propios, solo en sandbox, solo con fines de hardening.

Pruebas defensivas futuras:

```txt
jailbreak regression tests
prompt injection regression tests
permission bypass tests
secret leakage tests
tool abuse tests
memory poisoning tests
malicious document tests
malicious webpage/UI tests
malicious screenshot tests
agent boundary regression tests
approval bypass tests
runtime activation bypass tests
```

Prohibiciones:

```txt
ataques contra terceros
exfiltración real
bypass operativo sobre servicios externos
uso ofensivo fuera de sandbox
uso para romper restricciones de modelos con fines dañinos
```

## Security invariants

```txt
default deny
least privilege
explicit permission required
no runtime without Security Layer
no tool execution without permission contract
no model invocation without permission contract
no memory persistence without permission contract
no external access without permission contract
no UI operator without sandbox and approval
no physical-world action without approval and safety policy
no secrets in prompts
no secrets in logs
every action must have lineage
every sensitive action must have idempotency
every write must have rollback or compensation policy
every external action must have audit trail
kill switch must remain available
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
```

## Blocked boundaries

Siguen bloqueados:

```txt
runtime execution
scheduler
worker
queue
model invocation
tool execution
memory persistence
external access
API
UI
UI-TARS runtime
Hermes runtime
n8n workflows reales
Home Assistant actions reales
attempt store writes reales
lifecycle events reales
lifecycle_store writes
result store writes
history writes
read model writes
projection writes
Market Catalog runtime
Business Composition Layer runtime
```

## Non-activation statement

Esta auditoría no crea módulos operativos nuevos. No se crea Security Layer ejecutable, permission contract ejecutable, runtime runner, scheduler, worker, queue, tool executor, model invoker, adaptador UI-TARS, adaptador Hermes, adaptador n8n ni adaptador Home Assistant.
