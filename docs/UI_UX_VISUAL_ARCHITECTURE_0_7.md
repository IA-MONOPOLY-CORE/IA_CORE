# UI/UX Visual Architecture 0.7

Veredicto: `UI_UX_VISUAL_ARCHITECTURE_DEFINED`

## Estado De Partida

Commit base: `166a7c01`.

IA_CORE llega a este bloque con la base contract-aware validada por el
checkpoint 0.6. La identidad activa esta limpia, los widgets consumen el
contrato estable `backend_internal_ui_payload.v1`, los drafts se mantienen
alineados con `backend_internal_ui_request.v1` y la UI permanece en estado
pre-runtime/no-execution.

Este documento no crea pantallas nuevas, no redisenia la aplicacion, no crea
endpoints, no activa runtime y no habilita execution. Define la direccion
visual superior para que las siguientes capas de UI se construyan con una
imagen externa alineada con la estructura interna del framework.

## Auditoria Visual Inicial

Partes que todavia se sienten prototipo:

- Algunas etiquetas conservan nombres internos o heredados como "HUD",
  "widgets" y "request contract" sin una jerarquia visual superior que explique
  el sistema como framework general.
- La organizacion actual funciona como consola tecnica, pero todavia no separa
  con suficiente peso visual identidad, readiness, contrato, servicios,
  bloqueos y evidencia.
- Hay controles bloqueados correctos desde contrato, aunque el siguiente nivel
  visual debera distinguir con mas claridad entre lectura, validacion y accion
  no disponible.

Partes que ya reflejan IA_CORE:

- Identidad activa IA_CORE.
- Navegacion general contract-aware.
- Widgets basados en `backend_internal_ui_payload.v1`.
- Ausencia de branding legacy en UI activa.
- Bloqueos visibles para `forbidden_actions` y `blocked_capabilities`.
- Empty states honestos como `no_payload` y deny-by-default.

Partes que necesitan jerarquia:

- Readiness global debe ser el primer nivel de confianza.
- Contrato/payload debe aparecer como fuente de autoridad antes que cualquier
  accion o modulo.
- Servicios internos deben leerse como mapa de exposicion, no como operaciones.
- Warnings/errors y evidencia deben quedar cerca del estado que explican.

Partes que podrian confundir bloqueo con operacion:

- Cualquier control visible con forma de boton debe mantenerse deshabilitado si
  no existe `allowed_actions`.
- Los textos de request/dispatch deben sostener que son draft o lectura hasta
  que backend declare permisos.
- Los estados tecnicos leidos desde APIs existentes no deben convertirse en
  readiness operativa de UI.

Labels/copy que requieren vigilancia futura:

- "HUD" puede seguir como nombre de superficie tecnica actual, pero no debe
  derivar en estetica gamer ni tactical.
- "Request contract" debe permanecer como borrador o contrato declarado, no
  como promesa de dispatch.
- "Ready" solo puede significar readiness declarada por backend, no capacidad
  operativa inferida por la UI.

## Decision De Identidad

Veredicto: `IA_CORE_VISUAL_DIRECTION_CONFIRMED`

IA_CORE es la identidad madre del sistema y la razon visual del framework.
Debe presentarse como framework profesional general, consola de direccion
inteligente, sistema interno de IA y centro de control contract-aware.

Veredicto: `LEGACY_VISUAL_LANGUAGE_BLOCKED`

Loteria, SAAOP, S.A.A.O.P., Tactical HUD, U-Score, CAZADOR, ESPEJO,
combinatoria y sorteos quedan fuera de la UI activa. Pueden existir como
historia, fixtures o documentacion legacy, pero no como producto, tema visual,
metrica principal, navegacion ni lenguaje de componentes nuevos.

## Principios Visuales

La arquitectura visual superior de IA_CORE se rige por:

- claridad: cada seccion debe responder que estado muestra y de donde viene;
- precision: labels, badges y estados no deben sugerir permisos inexistentes;
- sobriedad: menos ornamentacion, mas informacion legible;
- profundidad: la UI debe revelar capas de sistema sin saturar;
- trazabilidad: cada dato relevante debe apuntar a contrato, payload o lectura;
- jerarquia: identidad, readiness y contrato van antes que detalle operativo;
- confianza: estados bloqueados, invalidos o pendientes deben verse como tales;
- control: ninguna accion aparece como disponible si backend no la declara;
- honestidad de estado: sin exito falso, sin demo tratada como dato real;
- no-operatividad explicita: mientras no haya runtime, la UI lo declara.

## Lenguaje Visual Recomendado

Veredicto: `CONTRACT_AWARE_VISUAL_SYSTEM_CONFIRMED`

Direccion visual:

- base oscura o neutra tecnica, sin estetica gamer;
- contraste controlado para lectura sostenida;
- acentos frios y profesionales para foco, no decoracion;
- rojo reservado para bloqueo/fallo, ambar para espera/no payload, verde solo
  para readiness declarada y no para permiso implicito;
- componentes con bordes, escala y espaciado consistentes;
- menos efectos ornamentales y mas jerarquia por densidad, agrupacion y ritmo;
- datos reales o estados honestos, nunca decorativos;
- cero lenguaje visual legacy.

## Jerarquia De UI

Las futuras pantallas y ajustes deben ordenar la experiencia en estas capas:

1. Identidad/sistema: IA_CORE como marco general.
2. Readiness global: estado declarado del sistema o payload.
3. Contrato/payload: schema, version, flags, validation y source.
4. Servicios internos: service map, service_kind y exposicion controlada.
5. Acciones permitidas/prohibidas: `allowed_actions` y `forbidden_actions`.
6. Blocked capabilities: bloqueos visibles con `true = blocked`.
7. Warnings/errors: diagnostico cercano a la causa.
8. Evidencia/test/checkpoint: trazabilidad de validacion.
9. Proximos pasos: solo recomendaciones, nunca operacion activa.

## Sistema De Estados Visuales

Estados permitidos y criterio:

- `ready`: backend declara readiness no operativa o lectura disponible;
- `passed`: validacion/checkpoint superado sin implicar execution;
- `blocked`: accion/capability explicitamente bloqueada;
- `planned`: capacidad futura documentada, no disponible ahora;
- `pending`: espera de payload, diagnostico o validacion;
- `invalid`: contrato o payload no valido;
- `failed`: error declarado, visible y no oculto;
- `not_available`: ausencia honesta de dato/capacidad;
- `no_payload`: no hay payload estable inyectado;
- `contract_fixture`: fixture contractual explicito, no dato operativo.

La UI no debe presentar `active`, `running`, `live`, `operational`,
`executing` ni equivalentes como estados validos de UI contract-aware.

## Criterios Para Componentes Futuros

Todo componente futuro debe:

- ser contract-aware por defecto;
- leer contratos backend antes de mostrar acciones;
- no inferir permisos desde nombres, estilos, ubicacion o servicio;
- no ocultar `forbidden_actions`;
- no ocultar `blocked_capabilities`;
- no mostrar exito falso;
- no simular ejecucion;
- no usar datos decorativos como datos reales;
- no depender de dominios legacy;
- declarar empty states honestos;
- distinguir lectura, validacion, draft y accion no disponible.

## Limites Explicitos

Veredicto: `UI_PRE_RUNTIME_NO_EXECUTION_CONFIRMED`

Este bloque confirma:

- no endpoint/API/router;
- no runtime/execution;
- no tools/models/integrations;
- no agentes ejecutando;
- no dominios operativos;
- no pantallas nuevas grandes;
- no controlled execution;
- no cambio de contrato backend.

## Continuidad

Veredicto: `UI_READY_FOR_NEXT_VISUAL_STRUCTURE_BLOCK`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 0.8 - Estructurar layout superior contract-aware sin runtime/no-execution`
