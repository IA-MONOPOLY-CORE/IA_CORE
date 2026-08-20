# UI/UX Main Console Interaction Model 1.3

Veredicto: `UI_UX_MAIN_CONSOLE_INTERACTION_MODEL_DEFINED`

## Estado De Partida

Commit base: `aafbe87b`.

Este bloque continúa la consola estructurada en
`docs/UI_UX_MAIN_CONSOLE_STRUCTURE_1_0.md`, refinada en
`docs/UI_UX_MAIN_CONSOLE_REFINEMENT_1_1.md` y ordenada por flujo en
`docs/UI_UX_MAIN_CONSOLE_FLOW_1_2.md`. Conserva la base contractual 0.6 y no
cambia contratos backend, endpoints ni capacidad operativa.

## Auditoría Previa

La consola ya permitía releer el payload inyectado, abrir/cerrar el request
draft y entrar a utilidades administrativas preexistentes. La relectura era
local y segura, pero su apariencia podía confundirse con una acción. La ruta
1.2 explicaba el orden sin permitir foco; tampoco existía un inspector
consolidado de solo lectura.

Los controles de request/dispatch ya estaban deshabilitados y no debían
tocarse. `forbidden_actions` y `blocked_capabilities` ya eran visibles y no
debían quedar detrás de un collapse. Las utilidades `CFG`, creación y dominio
pertenecen a gestión existente: quedan fuera del modelo contract-aware 1.3 y
no se reinterpretan como permisos del contrato.

## Modelo Permitido

Veredicto: `IA_CORE_MAIN_CONSOLE_INTERACTION_CONFIRMED`

El usuario puede:

- enfocar readiness, Contract Core, señales, límites, evidencia y continuidad;
- expandir o colapsar el inspector contractual local;
- releer el payload ya inyectado para actualizar la presentación;
- inspeccionar schema, source, validation, flags, diagnósticos y límites;
- mostrar u ocultar el request draft bloqueado;
- usar teclado en controles nativos de foco e inspector.

Estas interacciones son locales, reversibles y no persisten decisiones
operativas. Enfocar no autoriza; inspeccionar no ejecuta; expandir no activa.

Veredicto: `READ_ONLY_INTERACTIONS_CONFIRMED`

## Modelo Prohibido

El modelo 1.3 no permite:

- runtime, execution, dispatch real ni controlled execution;
- ejecutar agentes o invocar models, tools o integrations;
- materializar, archivar, borrar o resetear desde controles 1.3;
- crear endpoints, APIs o routers;
- mutar payloads o contratos;
- persistir selección/foco como estado operativo;
- derivar permisos desde foco, expansión, labels o señales;
- convertir `forbidden_actions` o `blocked_capabilities` en botones.

## Estados De Interacción

Veredicto: `CONTRACT_AWARE_INTERACTION_MODEL_CONFIRMED`

Los estados locales definidos son:

- `selected`: zona elegida en la ruta de lectura;
- `focused`: foco visual/teclado temporal;
- `expanded`: detalle local visible;
- `collapsed`: detalle local oculto;
- `read_only`: contenido sin mutación;
- `inspectable`: contenido que puede leerse o enfocarse;
- `blocked_interaction`: control sin interacción operativa;
- `disabled_by_contract`: control deshabilitado por contrato.

No reemplazan los estados contractuales `ready`, `passed`, `blocked`,
`planned`, `pending`, `invalid`, `failed`, `not_available`, `no_payload` y
`contract_fixture`. Un estado de foco nunca cambia readiness ni permisos.

## Marcas Y Controles

La shell incorpora:

- `data-console-interaction="contract-aware-1.3"`;
- `data-interaction-mode="read-only"`;
- `data-interaction-control="focus"` para la ruta;
- `data-interaction-control="inspect"` para inspector/relectura;
- `data-interaction-control="collapse"` para el request draft;
- `data-interaction-state` para estados locales;
- `data-interaction-scope="existing-management"` para separar utilidades
  administrativas preexistentes del modelo 1.3.

Los controles de foco usan botones accesibles y `aria-pressed`. El inspector
usa `<details>/<summary>` y permanece colapsado por defecto. Los widgets de
acciones, prohibiciones y bloqueos continúan visibles fuera del inspector.

## Inspector Read-Only

`ui/web/console-interactions.js` copia texto ya renderizado al inspector para:

- `schema_version`, `service_kind`, source y validation;
- flags y warnings/errors;
- `allowed_actions`, `forbidden_actions` y `blocked_capabilities`.

La sincronización usa `MutationObserver` sobre Contract Core y widgets. No
contiene `fetch`, no usa almacenamiento local/sesión, no muta fuentes y no
crea una segunda autoridad de datos.

## Autoridad Y Límites

Veredicto: `MAIN_CONSOLE_INTERACTION_NO_PERMISSION_INFERENCE_CONFIRMED`

Solo backend puede declarar permiso mediante `allowed_actions`.
`forbidden_actions` permanece visible y no ejecutable. `blocked_capabilities`
permanece visible con `true = blocked`. La relectura local no cambia esas
reglas y el inspector no muestra éxito falso.

Veredicto: `MAIN_CONSOLE_INTERACTION_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este bloque confirma:

- no endpoint público, API ni router HTTP nuevo;
- no runtime, execution, dispatch ni controlled execution;
- no agentes ejecutados ni invocaciones externas;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos o integraciones;
- no identidad activa SAAOP, Lotería o Tactical HUD.

## Responsive Verificado

El modelo fue verificado en navegador real a 1440 x 1000 y 390 x 844. Foco,
selected, expansión y collapse conservaron el orden sin overflow horizontal,
IDs duplicados ni controles superpuestos. El inspector mostró nueve campos y
se apiló en una columna en móvil. El request draft inició colapsado fuera del
viewport y su disclosure respondió a click, Enter y Espacio con
`aria-expanded` sincronizado.

## Continuidad

Veredicto: `UI_READY_FOR_MAIN_CONSOLE_INTERACTION_CHECKPOINT`

Próximo prompt exacto sugerido:

`PROMPT UI/UX 1.4 - Checkpoint de interacción de consola IA_CORE contract-aware sin runtime/no-execution`
