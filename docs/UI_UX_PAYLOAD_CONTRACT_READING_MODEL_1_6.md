# UI/UX Payload Contract Reading Model 1.6

Veredicto: `UI_UX_PAYLOAD_CONTRACT_READING_MODEL_DEFINED`

## Alcance

Este bloque define e implementa una regla minima de lectura
`summary -> detail -> raw-safe` para payload/contract en la consola IA_CORE.
No crea paneles grandes de detalle, no crea pantallas nuevas, no redisenia la
consola completa, no crea endpoints, no activa runtime, no habilita execution,
no activa dispatch real y no implementa controlled execution.

Commit base: `17bbb608`.

## Relacion Con 1.5

1.5 eligio `Opcion C - Modelo de lectura de payload/contract` antes de
construir paneles de detalle porque Contract Core / Payload es la zona mas
densa y la fuente de verdad de la consola. Este bloque materializa esa regla
de lectura sin avanzar a 1.7.

Va antes que paneles de detalle porque fija una jerarquia unica: summary para
orientacion humana, detail para diagnostico tecnico y raw-safe para evidencia
local segura. Asi se evita duplicar autoridad visual o sugerir permisos desde
una posicion de UI.

## Auditoria De Lectura Actual

El payload/contract aparece hoy en:

- badges de header para readiness, schema y read source;
- Readiness Global para estado, schema/request y diagnostics;
- Contract Core / Payload para `schema_version`, `service_kind`, source,
  validation, flags, warnings/errors, acciones y bloqueos;
- inspector read-only de 1.3;
- widgets contract-aware;
- request draft bloqueado;
- README y documentos 1.0 -> 1.5.

Campos leidos: `schema_version`, `service_kind`, source, readiness/status,
validation, flags, `allowed_actions`, `forbidden_actions`,
`blocked_capabilities`, warnings, errors y referencias request/response cuando
ya aparecen como dato visible.

Campos resumidos: readiness/status, schema, source, validation, cantidad de
acciones disponibles, prohibiciones, bloqueos y diagnostico visible.

Campos demasiado crudos: flags, warnings/errors y request/operation ids cuando
aparecen como texto tecnico sin capa de lectura.

Campos potencialmente ocultos: ausencia de raw seguro local, warnings vacios,
errors vacios, blocked capabilities ausentes y forbidden actions vacias. Deben
mostrarse como `not_available`, `no_payload`, `contract_fixture`, `pending` o
estado honesto equivalente.

Puede confundirse con permiso: cantidad de `allowed_actions`, foco visual,
source, service_kind, validation passed y lectura disponible. Ninguno autoriza
operacion por si mismo.

Puede confundirse con operacion: relectura local, inspector, request draft,
dispatch bloqueado y cualquier raw-safe que parezca consola de desarrollador.
Todos deben declarar read-only/no-operativo.

Falta para el operador: saber que capa esta leyendo, que campo proviene de
backend, que falta, que esta bloqueado y por que raw-safe no es modo operativo.

## Modelo Summary Detail Raw-Safe

Veredicto: `SUMMARY_DETAIL_RAW_SAFE_MODEL_CONFIRMED`

### Summary

`summary` es la capa humana breve. Responde que estado tiene el sistema, que
fuente contractual se esta leyendo, que esta permitido segun backend, que esta
prohibido, que esta bloqueado, que warnings/errors existen y que falta o esta
`planned`/`not_available`.

Campos permitidos en summary:

- readiness/status;
- schema visible;
- source visible;
- cantidad o ausencia de `allowed_actions`;
- presencia de `forbidden_actions`;
- presencia de `blocked_capabilities`;
- warnings/errors resumidos;
- estados honestos `not_available`, `no_payload`, `contract_fixture`,
  `pending`, `planned`, `blocked`, `failed`, `invalid`, `ready` o `passed`.

Summary nunca muestra raw JSON completo, nunca inventa estado, nunca suaviza
bloqueos criticos y nunca convierte ausencia de dato en permiso.

### Detail

`detail` es la capa tecnica legible. Muestra schema, servicio, source,
readiness/status, validation, flags, acciones, prohibiciones, bloqueos,
warnings/errors y relacion request/response si ya existe como dato visible.

Campos permitidos en detail:

- `schema_version`;
- `service_kind`;
- source;
- `readiness`;
- `status`;
- `validation`;
- `flags`;
- `allowed_actions`;
- `forbidden_actions`;
- `blocked_capabilities`;
- `warnings`;
- `errors`;
- request/response relationship declarada.

Detail no ejecuta, no hace fetch nuevo, no crea endpoint, no muta payload, no
crea autoridad nueva y no habilita acciones.

### Raw-Safe

`raw-safe` es la capa de inspeccion segura. Muestra una representacion local,
whitelist y read-only del payload/contract disponible. No es raw operativo ni
modo desarrollador.

Campos permitidos en raw-safe:

- `schema_version`;
- `service_kind`;
- source;
- `readiness`;
- `status`;
- `validation.flags`;
- `validation.warnings` sanitizados a code/message;
- `validation.errors` sanitizados a code/message;
- `allowed_actions` como action + available_now;
- `forbidden_actions`;
- `blocked_capabilities`.

Si no hay fuente local segura, raw-safe muestra `not_available`, `no_payload`,
`contract_fixture` o estado honesto equivalente.

## Campos Prohibidos O No Inferibles

No debe entrar en ninguna capa como permiso UI:

- foco, hover, expanded/collapsed o ubicacion visual;
- `service_kind`, source o schema;
- validation passed;
- ausencia de warnings/errors;
- cantidad de acciones;
- metadata de dominio;
- labels o estilos.

No debe mostrarse en raw-safe si apareciera:

- secretos, tokens, keys, passwords, cookies, headers sensibles;
- env vars;
- trazas completas;
- payloads externos no sanitizados;
- datos que sugieran endpoint nuevo o modo operativo.

No son estados validos de UI contract-aware: `active`, `running`, `live`,
`operational`, `executing` ni equivalentes.

## Manejo De Ausencia Y Diagnostico

Ausencia de dato se muestra como `not_available`, `no_payload`,
`contract_fixture`, `pending` o deny-by-default. No se completa con datos
decorativos.

Warnings/errors quedan visibles en summary/detail y sanitizados en raw-safe.
Un warning no autoriza; un error no se oculta; ausencia de error no habilita
runtime.

## Acciones Y Bloqueos

Veredicto: `PAYLOAD_CONTRACT_READING_IS_CONTRACT_AWARE`

`allowed_actions` se lee como dato declarado por backend. La UI puede mostrar
que existen acciones disponibles, pero no transforma esa lectura en permiso
propio ni en CTA operativo.

`forbidden_actions` permanece visible y no ejecutable en summary/detail y puede
aparecer en raw-safe como lista sanitizada.

`blocked_capabilities` permanece visible con semantica `true = blocked`.
Summary no puede suavizarlo, detail no puede invertirlo y raw-safe no puede
convertirlo en accion.

Veredicto: `PAYLOAD_READING_NO_PERMISSION_INFERENCE_CONFIRMED`

## Reglas Raw-Safe

Veredicto: `RAW_SAFE_READ_ONLY_CONFIRMED`

Raw-safe:

- es read-only;
- no edita;
- no envia;
- no ejecuta;
- no activa modo operativo;
- no contiene submit;
- no contiene botones propios;
- no habilita copia como accion operativa;
- no muestra secretos si aparecieran;
- usa proyeccion whitelist local;
- muestra `not_available` si no hay fuente local segura.

## Implementacion Minima

La UI activa agrega:

- `data-payload-reading-model="contract-aware-1.6"` en la shell principal;
- `data-reading-layer="summary"`;
- `data-reading-layer="detail"`;
- `data-reading-layer="raw-safe"`;
- microcopy minimo para explicar cada capa;
- raw-safe read-only con `id="contract-raw-safe-value"`;
- proyeccion segura local generada por `backend-contract-widgets.js` desde el
  payload ya inyectado o `not_available` ante ausencia de payload.

No se agrego fetch, endpoint, API, router, pantalla nueva, panel grande,
navegacion interna, dependencia ni referencia externa.

## Limites Confirmados

Veredicto: `PAYLOAD_READING_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este bloque confirma:

- IA_CORE como identidad visual activa;
- ausencia de legacy visual activo;
- no endpoint publico, API ni router HTTP;
- no runtime ni execution;
- no dispatch real;
- no controlled execution;
- no agentes ejecutados;
- no invocacion de models, tools o integrations;
- no cambio de contrato backend;
- no cambios en `core/`, `api.py`, `domains/`, `tools/`, modelos ni
  integraciones.

## Continuidad

Veredicto: `UI_READY_FOR_CONTRACT_DETAIL_PANELS_BLOCK`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.7 - Disenar paneles de detalle contract-aware IA_CORE sin runtime/no-execution`
