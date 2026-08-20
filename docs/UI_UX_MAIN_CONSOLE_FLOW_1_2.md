# UI/UX Main Console Flow 1.2

Veredicto: `UI_UX_MAIN_CONSOLE_FLOW_STRUCTURED`

## Estado De Partida

Commit base: `bd133fe1`.

Este bloque continúa la estructura definida en
`docs/UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md` y el refinamiento validado en
`docs/UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md`. Conserva la autoridad contractual
del checkpoint 0.6 y la base visual cerrada en 0.9. No crea una pantalla nueva,
no cambia contratos backend y no habilita operación.

## Auditoría Previa

El orden DOM ya seguía identidad, readiness, contrato, señales, límites y
evidencia. Sin embargo, el usuario debía deducir ese recorrido: no existía una
ruta de lectura explícita, servicios y límites compartían una capa sin número
de paso, y evidencia/continuidad tenían el mismo peso visual.

Readiness era lo primero que se entendía después del header, pero el payload
y su validación podían perderse entre tarjetas. Las filas internas ya eran
señales, aunque faltaba reforzar que no representan servicios operativos. La
evidencia mencionaba 0.6, 0.9 y 1.1, pero no mostraba 1.0 y 1.1 juntos como
respaldo del estado actual.

Los cambios mínimos seguros fueron: agregar una ruta no interactiva, numerar
la lectura, marcar semánticamente los pasos, clarificar microcopy y separar el
siguiente bloque como continuidad `planned`. No se modificó el renderer ni la
lógica de widgets.

## Flujo Principal Definido

Veredicto: `IA_CORE_MAIN_CONSOLE_FLOW_CONFIRMED`

La consola sigue esta secuencia:

1. IA_CORE y límite `PRE-RUNTIME / NO-EXECUTION`.
2. Readiness global como estado declarado.
3. Contract Core / Payload como fuente y validación.
4. Internal Services / Signals como señales de lectura.
5. Actions & Boundaries como autoridad, prohibición y bloqueo.
6. Evidence / Checkpoint como respaldo verificable.
7. Next Step como continuidad documentada, no como acción.

La ruta compacta visible usa `data-flow-target` y no contiene links, botones ni
handlers. El orden del documento preserva la misma secuencia en 1440 x 1000 y
390 x 844.

## Marcas Semánticas

La shell incorpora `data-console-flow="contract-aware-1.2"`. Los bloques usan:

- `data-flow-step="orientation"`;
- `data-flow-step="readiness"`;
- `data-flow-step="contract-core"`;
- `data-flow-step="service-signals"`;
- `data-flow-step="actions-boundaries"`;
- `data-flow-step="evidence-checkpoint"`;
- `data-flow-step="next-step"`.

Las marcas son declarativas y testeables. No crean dependencias ni activan
lógica operativa.

## Microcopy Y Prioridad

Veredicto: `CONTRACT_AWARE_FLOW_CONFIRMED`

El header aclara que la consola lee contrato y señales declaradas y no ejecuta
operaciones. Readiness pide leer estado declarado; Contract Core presenta la
fuente con deny-by-default; las señales internas se distinguen de ejecución;
Actions & Boundaries contrasta permiso backend, prohibición no ejecutable y
capacidad bloqueada.

Evidence registra 0.6/0.9 como checkpoints base y 1.0/1.1 como estructura y
refinamiento del estado actual. El siguiente bloque se muestra `planned` como
continuidad posterior a 1.2, sin CTA.

## Autoridad Y Límites

Veredicto: `MAIN_CONSOLE_FLOW_NO_PERMISSION_INFERENCE_CONFIRMED`

La UI no infiere permisos desde conexión, orden, copy, estilo, servicio o
estado visual. Solo `allowed_actions` declarado por backend puede autorizar una
acción. `forbidden_actions` permanece visible y no ejecutable;
`blocked_capabilities` permanece visible con `true = blocked`.

Los widgets siguen consumiendo `backend_internal_ui_payload.v1` inyectado o
`contract_fixture`, mantienen deny-by-default y no incorporan fetch propio,
datos decorativos ni éxito falso.

Veredicto: `MAIN_CONSOLE_FLOW_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este bloque confirma:

- no endpoint público, API ni router HTTP nuevo;
- no runtime, execution, dispatch real ni controlled execution;
- no agentes ejecutados;
- no invocación de models, tools o integrations;
- no cambio de contrato backend;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos o integraciones;
- no identidad activa SAAOP, Lotería o Tactical HUD.

## Responsive Verificado

El flujo fue verificado en navegador real a 1440 x 1000 y 390 x 844. La ruta
pasa de seis a tres y luego a una columna, conserva el orden lógico y mantiene
legibles los tokens técnicos. No hay overflow horizontal, IDs duplicados ni
controles sobre el contenido. El request contract queda fuera del área de
lectura en escritorio y colapsado fuera del viewport en móvil; los controles
de request/dispatch preservan su estado deshabilitado.

## Continuidad

Veredicto: `UI_READY_FOR_MAIN_CONSOLE_INTERACTION_MODEL_BLOCK`

Próximo prompt exacto sugerido:

`PROMPT UI/UX 1.3 - Definir modelo de interacción de consola IA_CORE contract-aware sin runtime/no-execution`
