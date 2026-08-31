# UI/UX Panel Maestro Final Screen Contracts Visual Rehousing Plan 1.128

## Commit base

- Base esperada: `570b18f`.
- Restore point remoto vigente: `570b18f`.
- Rama esperada: `main`.
- Estado esperado: `main` up to date con `origin/main`.
- Working tree esperado: limpio.

## Objetivo

1.128 planifica el rehousing visual de Final Screen Contracts sin implementar nada. El objetivo es definir el alcance exacto para una futura reorganizacion visual externa de las cuatro pantallas contractuales dentro del `Master Shell + Overview Layer`, preservando IDs, estados, contrato funcional, `DEFER_FINALIZATION`, no-runtime/no-execution y ausencia total de acciones operativas.

Este prompt no modifica UI activa, no modifica JS, no toca backend, no hace push y no avanza a 1.129.

## Estado recibido

- Restore point 1.127: `MASTER_SHELL_OVERVIEW_RESTORE_POINT_PUBLICATION_PUSH_COMPLETED`.
- Decision 1.126: `NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK`.
- Restore point remoto: `570b18f`.
- `main` up to date con `origin/main`.
- `Master Shell + Overview Layer` cerrado y publicado.
- Bloque recomendado: `Final Screen Contracts Visual Rehousing`.
- Mapa visual base: arquitectura 1.121.
- Mapa real base: auditoria 1.120.
- Limites base: guardrails 1.122.
- Continuidad visual: plan 1.123, implementacion 1.124 y checkpoint 1.125.

## Definición de Final Screen Contracts Visual Rehousing

`Final Screen Contracts Visual Rehousing` significa rehousing visual externo del bloque de cuatro pantallas contractuales dentro del nuevo `Master Shell + Overview Layer`, sin cambiar su contrato funcional.

Debe ser:

- rehousing visual externo;
- reorganizacion de layout;
- mejora de jerarquia;
- reduccion de densidad;
- mejor lectura de estados;
- mejor separacion entre pantallas FSC;
- mejor relacion con el shell superior;
- preservacion total del contenido contractual.

No debe ser:

- nueva funcionalidad;
- nueva pantalla operativa;
- quinta FSC;
- cambio de contrato;
- activacion de capacidades;
- nuevo router;
- User Panel;
- flujo de ejecucion;
- endpoint/fetch;
- JS nuevo.

## Las cuatro FSC a preservar

| FSC | Pantalla | Funcion visual actual | Debe preservarse | Mejora externa futura permitida | Prohibido tocar | Riesgo |
| --- | --- | --- | --- | --- | --- | --- |
| `FSC-CO-01` | Contract Overview Screen | Presenta identidad IA_CORE, source, readiness documental, acciones permitidas/prohibidas, bloqueos y evidencia como frontera contractual primaria. | ID, titulo, source, estados read-only/no-runtime/no-execution, allowed/forbidden, blocked capabilities, evidencia y relacion con IA_CORE. | Encapsularla visualmente dentro de un contenedor FSC, clarificar encabezado de grupo, reducir repeticion externa y mejorar separacion respecto del overview. | No renombrar `FSC-CO-01`, no cambiar significado contractual, no convertir overview en CTA, no cambiar estados contractuales. | Que la overview se lea como health operativo o permiso listo para ejecutar. |
| `FSC-BF-02` | Blocked & Forbidden Capabilities Screen | Hace visibles limites duros, acciones prohibidas, no-unlock/no-bypass/no-override, source y evidencia. | ID, blockers, forbidden actions, severidad contractual, no-runtime/no-execution/no-endpoint/no-user-panel y visibilidad permanente. | Mejorar jerarquia visual de bloqueo y reducir ruido sin esconder razones ni evidencia. | No suavizar u ocultar bloqueos, no agregar override/bypass/unlock, no crear CTA ni boton operativo. | Que el bloque parezca alarma accionable o invitacion a desbloquear. |
| `FSC-VR-03` | Validation & Readiness Screen | Explica validation/readiness como constatacion documental, diferenciando readiness de permiso y validacion de ejecucion. | ID, findings, warnings/errors, requirements, blockers, evidence, ready-no-permission y no-dispatch/no-endpoint. | Ordenar visualmente readiness, validation y evidencia para lectura progresiva. | No convertir validacion en aprobacion de ejecucion, no cambiar estados, no introducir success operativo. | Que un estado verde o `ready` se lea como autorizacion real. |
| `FSC-RCP-04` | Request Contract Preview Screen | Muestra preview contractual diferido, `CFD-04`, draft/not final, allowed/forbidden y evidencia safe. | ID, `CFD-04`, `draft / not final`, `DEFER_FINALIZATION`, no-submit/no-send/no-dispatch/no-runtime/no-execution/no-fetch/no-user-panel y ausencia de contrato final. | Mejorar separacion y microcopy para que el preview sea claramente documental. | No cambiar `DEFER_FINALIZATION`, no crear contrato final, no agregar submit/send/preview-and-run ni endpoint/fetch. | Que request/preview parezca envio o flujo de ejecucion. |

## Alcance futuro permitido

Para un futuro prompt de implementacion, queda permitido:

- reorganizar wrappers externos del bloque FSC;
- ordenar la secuencia visual de las cuatro FSC;
- crear contenedor visual FSC dentro del shell;
- crear encabezado documental del grupo FSC;
- agregar microcopy no operativo que explique que son contratos finales de pantalla;
- mejorar jerarquia visual entre overview, blocked/forbidden, validation/readiness y request contract preview;
- reducir densidad visual externa;
- mejorar separacion entre secciones;
- mejorar etiquetas visuales contractuales;
- mejorar responsive si aplica;
- usar CSS para layout externo si es necesario;
- mantener estados visibles;
- mantener bloqueos visibles;
- mantener `DEFER_FINALIZATION`.

## Alcance futuro prohibido

Para un futuro prompt de implementacion, queda prohibido:

- no crear quinta FSC;
- no crear quinta seccion;
- no borrar FSC existente;
- no renombrar `FSC-CO-01`;
- no renombrar `FSC-BF-02`;
- no renombrar `FSC-VR-03`;
- no renombrar `FSC-RCP-04`;
- no renombrar IDs FSC;
- no cambiar significado contractual;
- no cambiar estados contractuales;
- no cambiar `DEFER_FINALIZATION`;
- no CTA;
- no convertir FSC en CTA;
- no agregar boton operativo;
- no agregar submit/send/run/execute/dispatch;
- no agregar preview-and-run;
- no crear rutas/hash;
- no crear User Panel;
- no crear endpoint/fetch;
- no endpoints/fetches;
- no agregar JS;
- no JS;
- no tocar elementos inferiores;
- no reactivar `CFG`;
- no reactivar `+`;
- no reactivar `DOMAIN`;
- no exponer raw Package;
- no exponer payload crudo;
- no ocultar bloqueos;
- no crear fake success;
- no crear ghost actions.

## Archivos permitidos/prohibidos para futura implementación

Permitidos:

- `ui/web/index.html`;
- `ui/web/styles.css`, solo si el rehousing requiere soporte visual;
- `ui/web/i18n_es.json`, solo si hace falta copy visible;
- docs/tests/readmes.

Solo lectura:

- `ui/web/backend-contract-widgets.js`;
- `ui/web/admin-panels.js`;
- `ui/web/console-interactions.js`;
- `ui/web/domains.js`.

Prohibidos:

- `api.py`;
- `core/`;
- `domains/`;
- `providers/`;
- `tools/`;
- `scripts/`;
- modelos;
- integraciones;
- CI;
- dependencias;
- `.env`;
- secrets;
- backend operativo.

## Límites HTML futuros

Permitido:

- wrappers externos;
- contenedores documentales;
- headings del grupo FSC;
- labels no operativos;
- `data-*` documentales;
- estructura visual no-routed.

Prohibido:

- `form` nuevo;
- `button` operativo nuevo;
- `a href="#..."`;
- `a href="/..."`;
- `onclick` nuevo;
- `submit`;
- inputs de mutacion;
- navegacion real;
- raw payload.

## Límites CSS futuros

Permitido:

- layout externo;
- grid/flex;
- spacing;
- responsive;
- jerarquia;
- badges no operativos;
- claridad visual;
- reduccion de densidad;
- focus visible sin CTA operativo.

Prohibido:

- animaciones live/running/executing;
- estilos de CTA operativo;
- ocultar bloqueos;
- simular habilitacion;
- esconder warnings;
- esconder estados prohibidos;
- depender de CSS para seguridad funcional.

## Límites i18n/copy futuros

Permitido:

- `Final Screen Contracts`;
- `contrato de pantalla`;
- `lectura`;
- `bloqueado por contrato`;
- `sin runtime`;
- `sin ejecución`;
- `sin execution`;
- `no disponible`;
- `requiere validación`;
- `requiere autorización`;
- `preview contractual`;
- `DEFER_FINALIZATION`;
- `IA_CORE`.

Prohibido:

- SAAOP/Loteria como identidad visible activa;
- SAAOP/Lotería como identidad visible activa;
- ejecutar/correr/enviar/despachar/procesar/activar como accion disponible;
- live/running/active/submitted/ready to run;
- promesas operativas;
- exito operativo.

## JS futuro

No se recomienda tocar JS para este bloque. El rehousing debe ser HTML/CSS/copy. Si parece necesario tocar JS, detener y abrir prompt dedicado.

Reglas:

- no se recomienda tocar JS;
- no agregar listeners;
- no agregar fetches;
- no agregar localStorage;
- no agregar hash/history;
- no agregar handlers operativos;
- no modificar `ui/web/backend-contract-widgets.js`;
- no modificar `ui/web/admin-panels.js`;
- no modificar `ui/web/console-interactions.js`;
- no modificar `ui/web/domains.js`.

## Preservación de elementos inferiores

Los elementos inferiores no se tocan en este bloque:

- `CFG` sigue bloqueado;
- `+` sigue bloqueado;
- `DOMAIN` sigue bloqueado;
- `RELEER PAYLOAD LOCAL` sigue lectura/local si existe;
- `VER DETALLE` y `VER EVIDENCIA` siguen disclosures/lectura si existen;
- formularios siguen no submiteables;
- no POST/PUT/DELETE;
- no reactivacion.

## Preservación no-runtime/no-execution

El futuro rehousing debe preservar:

- sin runtime;
- sin execution;
- sin dispatch;
- sin worker;
- sin scheduler;
- sin queue;
- sin model invocation;
- sin tool invocation;
- sin endpoint/fetch;
- sin fake success;
- sin ghost actions.

## Criterios visuales de aprobación humana futura

La revision visual humana debera confirmar en navegador:

- el grupo FSC se entiende mejor;
- las cuatro FSC siguen reconocibles;
- no hay quinta FSC;
- no cambio contrato funcional;
- `DEFER_FINALIZATION` sigue visible/preservado;
- nada parece ejecutable;
- no aparecen botones operativos;
- no aparecen rutas/hash/User Panel;
- no aparecen endpoints/fetches;
- no se tocaron elementos inferiores;
- `CFG`, `+` y `DOMAIN` siguen bloqueados;
- la UI se ve mas ordenada, no mas confusa;
- el rehousing mejora lectura sin abrir capacidades.

## Validaciones obligatorias para futura implementación

El futuro prompt de implementacion debera ejecutar:

- `node --check ui/web/backend-contract-widgets.js`;
- `node --check ui/web/admin-panels.js`;
- `node --check ui/web/console-interactions.js`;
- `node --check ui/web/domains.js`;
- test nuevo de implementacion 1.129;
- test 1.128;
- test 1.127;
- test 1.126;
- test 1.125;
- test 1.124;
- test 1.123;
- test 1.122;
- test 1.121;
- test 1.120;
- test 1.110;
- `python -m pytest tests/test_ia_core_github_backup_readiness.py -q`;
- backend contract tests relevantes;
- `git diff --check`;
- revision visual humana obligatoria.

## Risk register

| Riesgo | Señal | Mitigacion |
| --- | --- | --- |
| Cambiar sin querer contenido contractual FSC | Cambian copy critico, estados, evidence o source | Test de marcadores FSC y diff acotado. |
| Borrar o renombrar IDs FSC | Falta `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` o `FSC-RCP-04` | Test obligatorio de IDs y revision humana. |
| Crear una quinta FSC accidental | Aparece otra seccion con semantica FSC | Prohibicion explicita y conteo visual. |
| Alterar `DEFER_FINALIZATION` | Preview deja de ser draft/not final | Test especifico sobre RCP. |
| Convertir contratos en CTAs | Encabezados, cards o badges parecen clickeables | Sin botones nuevos, sin href y copy read-only. |
| Hacer que un bloque parezca ejecutable | Estados activos o lenguaje operativo | Solo estados documentales y no-runtime/no-execution. |
| Crear botones ambiguos | Nuevo control con hover o texto de accion | No botones operativos ni pseudo-CTA. |
| Tocar JS innecesariamente | Diff en archivos JS o handlers | JS solo lectura; detener si se necesita. |
| Crear rutas/hash | `href="#..."`, `history`, `location` o router | Prohibicion y test negativo. |
| Crear User Panel | Copy o navegacion de usuario | IA_CORE como identidad activa. |
| Tocar elementos inferiores | Diff en `CFG`, `+`, `DOMAIN` o lower console | Fuera de alcance. |
| Reactivar `CFG`, `+`, `DOMAIN` | Botones habilitados, POST/PUT/DELETE o modal activo | Mantener bloqueos y no tocar lower console. |
| Ocultar bloqueos | Menos visibilidad de blockers o warnings | Bloqueos siempre visibles. |
| Aumentar densidad | Mas wrappers sin jerarquia | Rehousing externo con reduccion de ruido. |
| Romper responsive | Superposicion o overflow en mobile | Revision visual humana desktop/mobile. |
| Generar fake success | `ready` o `validated` se leen como permiso | Calificar como documental/read-only. |
| Introducir SAAOP/Loteria visible | Alias historico vuelve al shell o FSC | IA_CORE unico como identidad activa. |
| Tocar backend por error | Diff en `api.py`, `core/` o integraciones | Lista prohibida y revision de diff. |

## Decisión final

`FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_PLAN_READY_FOR_GUARDED_IMPLEMENTATION_PROMPT`

## Justificación

El restore point remoto `570b18f` ya fue publicado en 1.127. El siguiente bloque esta correctamente acotado como rehousing visual externo de las cuatro FSC, sin cambios contractuales, sin JS, sin runtime, sin rutas/hash, sin User Panel, sin endpoints/fetches y con revision visual humana obligatoria. Corresponde pasar a un prompt futuro de implementacion guardada, no implementar aqui.

## Próximo prompt exacto

`PROMPT UI/UX 1.129 - Implementar rehousing visual Final Screen Contracts Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Límites preservados

- no se implementó rehousing;
- no se implemento rehousing;
- no se implemento bloque nuevo;
- no bloque nuevo;
- no se modifico UI activa;
- no UI activa;
- no se modifico JS;
- no JS;
- no se modificaron Final Screen Contracts;
- no Final Screen Contracts;
- no se modificaron elementos inferiores;
- no elementos inferiores;
- no se modifico contrato funcional;
- no contrato funcional;
- no se creo contrato final;
- no contrato final;
- no se contradijo `DEFER_FINALIZATION`;
- no se creo User Panel;
- no User Panel;
- no se crearon rutas/hash;
- no rutas/hash;
- no se crearon endpoints/fetches nuevos;
- no endpoints/fetches nuevos;
- no se activo runtime/execution/dispatch;
- no runtime;
- no execution;
- no dispatch;
- no se toco backend/runtime/endpoints/CI/dependencias;
- no CI;
- no se limpio deuda residual general;
- no deuda residual;
- no se corrigieron pyflakes;
- no pyflakes;
- no se hizo push;
- no push;
- no se avanzó a 1.129;
- no se avanzo a 1.129.
