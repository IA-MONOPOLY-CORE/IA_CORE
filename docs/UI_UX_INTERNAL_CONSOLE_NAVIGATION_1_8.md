# UI/UX Internal Console Navigation 1.8

Veredicto: `UI_UX_INTERNAL_CONSOLE_NAVIGATION_DEFINED`

## Alcance

Este bloque define e implementa una navegacion interna local y read-only para
la consola IA_CORE. Permite mover foco y scroll entre siete zonas de lectura
sin crear rutas, hashes, pantallas secundarias, una app multi-pantalla,
endpoints, runtime, execution, dispatch real ni controlled execution.

Commit base: `512a3391`.

## Auditoria De Orientacion Actual

Antes de 1.8 el operador se movia mediante scroll y los seis controles de foco
de 1.3 construidos sobre la ruta conceptual 1.2. Readiness, Contract Core,
Internal Signals, Actions & Boundaries, Evidence y Next Step eran faciles de
ubicar desde esa ruta.

Las zonas densas o enterradas aparecieron despues: el modelo
summary/detail/raw-safe 1.6 y los siete paneles 1.7 viven dentro de Contract
Core, pero no tenian destino directo. Para llegar a ellos habia que enfocar
Contract Core y continuar con scroll manual.

Zonas que necesitaban foco directo:

- Payload Reading para summary/detail/raw-safe;
- Detail Panels para readiness, payload, validation, actions, blocked,
  warnings/errors y evidence;
- Actions & Boundaries para revisar autoridad y bloqueos;
- Evidence y Next Step para separar respaldo de continuidad planned.

Controles con posible ambiguedad operativa: foco de la ruta, relectura local,
inspector, request draft y dispatch bloqueado. La navegacion 1.8 usa microcopy
propio: navegar mueve la lectura, foco no selecciona una operacion y zona no
significa modulo ejecutable.

Reutilizacion segura:

- Flow 1.2 conserva orden, semantica y sus siete data-flow-step.
- Interaction 1.3 aporta botones, foco temporal, scroll local y estado
  read_only sin persistencia.
- Reading model 1.6 aporta destinos separados para summary/detail/raw-safe.
- Detail panels 1.7 aporta un destino compacto para los siete paneles.

## Tipo De Navegacion Elegido

Se implementa un indice interno compacto dentro de la misma pagina. Usa siete
botones nativos que mueven foco y scroll hacia marcas data-nav-section. No usa
anchors con hash, URL, history API, router, rutas reales, menu de producto ni
pantallas secundarias.

La ruta 1.2 sigue siendo el mapa conceptual de lectura. El indice 1.8 agrega
granularidad para moverse entre zonas existentes. No reemplaza el flujo ni
crea una jerarquia de modulos ejecutables.

Veredicto: `INTERNAL_NAVIGATION_IS_READ_ONLY_CONFIRMED`

## Zonas Y Orden

Orden de navegacion:

1. Readiness: estado global, fuente y limite pre-runtime.
2. Contract Core: envelope contractual y widgets estables.
3. Payload Reading: capas summary, detail y raw-safe.
4. Detail Panels: paneles contract-aware 1.7.
5. Actions & Boundaries: allowed, forbidden y blocked capabilities.
6. Evidence: checkpoints, veredictos y trazabilidad.
7. Next Step: continuidad planned, no accion.

Marcas de control:

- data-nav-target="readiness";
- data-nav-target="contract-core";
- data-nav-target="payload-reading";
- data-nav-target="detail-panels";
- data-nav-target="actions-boundaries";
- data-nav-target="evidence";
- data-nav-target="next-step".

Cada destino usa data-nav-section con el mismo nombre. La shell declara
data-internal-navigation="contract-aware-1.8" y el nav declara
data-nav-state="read_only".

## Relacion Con Los Bloques Previos

### Flow 1.2

La navegacion mantiene el orden readiness -> contract -> boundaries ->
evidence -> next step. No elimina ni duplica data-flow-step. El indice ofrece
acceso adicional a Payload Reading y Detail Panels, que son subdivisiones
posteriores de Contract Core.

### Interaction 1.3

Se reutilizan botones nativos, scrollIntoView, foco temporal, prefers-reduced-
motion y helpers de estado local. La navegacion no persiste foco, no usa
storage y no cambia readiness, contrato ni permisos.

El estado current_section se sincroniza con el flow step relacionado para no
mostrar dos zonas actuales. Payload Reading y Detail Panels se vinculan con
Contract Core porque son subdivisiones de esa zona, no modulos nuevos.

### Reading Model 1.6

Payload Reading apunta al bloque que conserva exactamente las tres capas
summary/detail/raw-safe. Navegar hacia raw-safe no cambia su estado read-only,
no copia datos, no muta payload y no habilita modo operativo.

### Detail Panels 1.7

Detail Panels apunta a la grilla existente completa. La navegacion no colapsa
ni oculta forbidden_actions, blocked_capabilities, warnings o errors. Los siete
paneles conservan data-detail-state="read_only".

Veredicto: `INTERNAL_NAVIGATION_CONTRACT_AWARE_CONFIRMED`

## Estados Visuales

Estados permitidos:

- `current_section`: destino actual del indice;
- `focused`: foco temporal despues de navegar;
- `read_only`: navegacion y destino sin mutacion;
- `inspectable`: zona legible/enfocable;
- `collapsed` y `expanded`: disclosures locales existentes;
- `not_available`: ausencia honesta;
- `planned`: continuidad no operativa;
- `blocked`: frontera contractual.

Estados prohibidos para navegacion:

- `active` como operacion;
- `running`;
- `executing`;
- `live`;
- `operational`;
- `dispatching`;
- `submitted`;
- `processing`.

current_section y focused no son permisos. aria-current solo comunica ubicacion
dentro de la lectura y no altera allowed_actions.

## Accesibilidad Y Responsive

Los controles son button type=button, tienen foco visible y aria-current. El
orden DOM coincide con el orden visual. El destino recibe tabindex=-1 solo al
navegar, se enfoca sin persistencia y respeta prefers-reduced-motion.

La grilla usa siete columnas en escritorio, cuatro en ancho intermedio y dos
en movil. No es sticky ni flotante, por lo que no tapa contenido. Labels y
tokens permiten wrap. La navegacion debe verificarse a 1440 x 1000 y
390 x 844 sin overflow horizontal, IDs duplicados ni superposiciones.

Paneles 1.7, raw-safe, forbidden_actions y blocked_capabilities permanecen
visibles. Request/dispatch siguen deshabilitados por contrato.

## Autoridad Y Limites

La navegacion no lee ni escribe permisos. allowed_actions sigue viniendo solo
de backend; forbidden_actions permanece visible/no ejecutable y
blocked_capabilities conserva true = blocked. Orden, foco, current_section,
aria-current, estilo o ubicacion no conceden capacidad.

Veredicto: `INTERNAL_NAVIGATION_NO_PERMISSION_INFERENCE_CONFIRMED`

No se agrega fetch, endpoint, API, router, hash routing, history mutation,
storage, contrato backend, dependencia, template ni asset externo.

Veredicto: `INTERNAL_NAVIGATION_NO_RUNTIME_NO_EXECUTION_CONFIRMED`

Este bloque confirma:

- IA_CORE como identidad visual activa;
- no endpoint publico, API ni router HTTP;
- no runtime ni execution;
- no dispatch real ni controlled execution;
- no agentes ejecutados;
- no invocacion de models, tools o integrations;
- no app multi-pantalla ni rutas;
- no sistema global de componentes;
- no cambios en core/, api.py, domains/, tools/, modelos ni integraciones.

## Continuidad

Veredicto: `UI_READY_FOR_COMPONENT_SYSTEM_BLOCK`

Proximo prompt exacto sugerido:

`PROMPT UI/UX 1.9 - Definir sistema de componentes IA_CORE contract-aware sin runtime/no-execution`
