# UI/UX Panel Maestro Design System Density Refinement Plan 1.132

## Commit base

- Base esperada: `9e8ea7c`.
- Restore point remoto vigente: `570b18f`.
- Commits locales previos:
  - `469d963`.
  - `a47a4f8`.
  - `fd15a84`.
  - `9e8ea7c`.

## Objetivo

1.132 planifica Design System y Density Refinement sin implementar. El alcance define reglas visuales, tokens, densidad, jerarquia, spacing, badges, bordes, colores semanticos, patrones contract-aware, criterios responsive, validaciones y fases futuras para estabilizar el lenguaje visual del Panel Maestro IA_CORE antes de tocar otra UI activa.

## Estado recibido

- Checkpoint 1.130: `FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING`.
- Decision 1.131: `NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED`.
- Revision visual humana: `FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED`.
- Restore point remoto `570b18f`.
- Estado local esperado: local ahead por 4 commits.
- `Master Shell + Overview Layer` publicado.
- `Final Screen Contracts Visual Rehousing` cerrado.
- densidad visual como deuda menor no bloqueante.

`Master Shell + Overview Layer` esta implementado, aprobado, checkpoint cerrado y publicado en GitHub. `Final Screen Contracts Visual Rehousing` esta planificado, implementado, aprobado visualmente y checkpoint cerrado. No hay push pendiente obligatorio inmediato, pero debe evaluarse antes de implementar cambios visuales activos.

## Proposito del Design System / Density Refinement

El Proposito del Design System / Density Refinement es estabilizar el lenguaje visual del Panel Maestro antes de tocar zonas mas riesgosas. Debe servir para reducir densidad sin borrar verdad contractual, ordenar jerarquia, unificar lectura de estados, evitar CTAs operativos falsos, diferenciar lectura/documentacion de accion, diferenciar bloqueado de disponible, diferenciar futuro de activo, hacer que no-runtime/no-execution sea visualmente claro y preparar proximos bloques sin improvisar polish.

No debe servir para activar funciones, crear pantallas ejecutables, ocultar bloqueos, maquillar de operativo algo bloqueado, cambiar contratos, tocar runtime, tocar backend, crear User Panel, crear rutas/hash ni crear endpoints/fetches.

## Reglas de densidad visual

- Cada card deberia tener como recomendacion maxima 3 badges visibles; si hay mas estados, agrupar badges por familia contractual.
- Agrupar badges cuando comparten funcion semantica: lectura, bloqueo, deferred, evidencia o futuro.
- Usar texto auxiliar cuando el estado necesita explicar causa o frontera; no sumar otro badge para cada matiz.
- Mover detalle a disclosure/documentacion cuando no sea P0 visible, siempre sin payload crudo y sin convertir disclosure en accion.
- Priorizar lectura primaria/secundaria/terciaria: P0 para identidad, bloqueo, `DEFER_FINALIZATION` y no-runtime/no-execution; P1 para source/readiness/evidence; P2 para metadata historica o notas de proceso.
- Evitar bloques con demasiadas columnas visuales: si una grilla exige columnas estrechas, usar stack o filas de lectura.
- Tratar pantallas read-only densas con encabezado claro, una linea de estado y detalle progresivo.
- Tratar contratos y bloqueos sin ocultarlos: reducir repeticion, no eliminar blockers ni prohibiciones.
- Reducir ruido sin borrar restricciones: consolidar labels repetidos, mantener una fuente visible por restriccion critica.
- Registrar deuda de densidad cuando no pueda resolverse en el bloque actual, incluyendo causa, zona, riesgo y prompt futuro sugerido.

## Tokens visuales conceptuales

Estos tokens visuales conceptuales no crean variables CSS todavia; son nombres de contrato visual para un futuro prompt.

| Token | Uso conceptual | Riesgo que evita |
| --- | --- | --- |
| token de superficie principal | Shell y zonas P0 de orientacion. | Mezclar prioridad primaria con detalle. |
| token de superficie secundaria | Cards y grupos P1. | Saturar el core visual. |
| token de superficie documental | Bloques de lectura, docs y facts. | Que documentacion parezca consola activa. |
| token de borde sutil | Separacion baja entre grupos. | Ruido por bordes fuertes repetidos. |
| token de borde contractual | FSC, contratos y limites formales. | Diluir autoridad contractual. |
| token de borde bloqueado | Bloqueos, forbidden y deny-by-default. | Confundir bloqueo con warning leve. |
| token de texto primario | Titulos y datos P0. | Perder foco de lectura. |
| token de texto secundario | Contexto, ledes y soporte. | Competencia con datos primarios. |
| token de texto tecnico | IDs, source contracts, schema y code labels. | Hacer que metadatos parezcan CTA. |
| token de estado read-only | Estado documental inspeccionable. | Interpretar lectura como permiso. |
| token de estado blocked | Estado bloqueado por contrato. | Suavizar prohibiciones. |
| token de estado no-runtime | Ausencia de runtime. | Parecer entorno ejecutable. |
| token de estado no-execution | Ausencia de ejecucion. | Parecer lista para correr. |
| token de warning documental | Riesgo o nota no operativa. | Crear alarma accionable falsa. |
| token de evidencia/documentacion | Evidencia, checkpoint y trazabilidad. | Exponer payload crudo o live log. |
| token de futuro/no disponible | Future-only, planned o not available. | Presentar futuro como activo. |
| token anti-CTA operativo | Estilo neutral para controles bloqueados o labels. | Sugerir click/ejecucion. |

## Jerarquia tipografica

- Titulo de shell: identidad IA_CORE y alcance del Panel Maestro; maxima jerarquia, sin sonar a producto publico.
- Titulo de grupo: nombre de bloque visual o contrato; jerarquia alta pero menor que shell.
- Titulo de card: responsabilidad local de una pieza; breve y escaneable.
- Subtitulo contextual: explica lectura o frontera sin competir con estados.
- Etiqueta contractual: IDs FSC, labels de contrato, source y estado.
- Meta tecnica: schema, backend source, hashes, checkpoint o path documental.
- Copy de advertencia: riesgos, restricciones y deny-by-default; corto, visible y no alarmista.
- Copy de evidencia: referencia verificable, no live log y sin payload crudo.
- Copy de estado: una frase por estado compuesto, evitando pilas de sinonimos.
- Microcopy read-only: deja claro que inspeccionar no ejecuta.
- Microcopy blocked: deja claro que bloqueado no es error reparable desde UI.

## Spacing/layout

- Separacion shell -> overview: amplia y consistente para que identidad/orientacion respiren antes del resumen.
- Separacion overview -> FSC: suficiente para leer cambio de capa, sin aislar los contratos del shell.
- Separacion entre grupos: usar bandas o gaps estables, no cards anidadas.
- Separacion entre cards: gap constante, con margen suficiente para evitar columnas comprimidas.
- Padding interno de card: medio, legible y menor que padding de seccion.
- Gap de badges: compacto; si hay wrap excesivo, agrupar.
- Ancho maximo recomendado: mantener line length legible y evitar paneles hiperanchos con texto estirado.
- Usar grid cuando las cards tienen peso equivalente y contenido similar.
- Usar stack cuando hay jerarquia narrativa, texto largo, mobile/tablet o estados criticos.
- Mobile/tablet: colapsar grillas temprano, preservar orden P0, reducir badges visibles y mover metadata a linea secundaria.
- Evitar columnas demasiado angostas cuando el contenido contiene IDs, estados largos o copy contractual.
- Paneles derechos: tratarlos como soporte/documentacion, no como accion paralela.

## Badges y estados

| Badge | Significado | Cuando usarlo | Cuando no usarlo | Riesgo de confusion | Alternativa si hay demasiados badges |
| --- | --- | --- | --- | --- | --- |
| `READ_ONLY` | Lectura sin mutacion. | Superficies inspeccionables/documentales. | Acciones, formularios activos o confirmaciones. | Que lectura parezca permiso. | Frase breve "solo lectura". |
| `NO_RUNTIME` | No hay runtime habilitado. | Bloques que podrian parecer entorno vivo. | Metadata historica sin riesgo operativo. | Que parezca estado tecnico reparable. | Agrupar en "sin runtime/ejecucion". |
| `NO_EXECUTION` | No hay ejecucion. | Cualquier zona cercana a run/dispatch/request. | Cuando el contexto ya lo deja claro y no es P0. | Que parezca ready to run si falta. | Texto auxiliar de frontera. |
| `BLOCKED_BY_CONTRACT` | Bloqueo por contrato/politica. | Controles deshabilitados, forbidden y deny-by-default. | Warning menor o deuda futura. | Que se interprete como error solucionable. | "bloqueado por contrato" en copy. |
| `DEFER_FINALIZATION` | Finalizacion diferida, no contrato final. | Request Contract Preview y derivados. | Cualquier contrato ya finalizado o pantalla no relacionada. | Que preview parezca envio. | Mantener label unico visible. |
| `REQUIRES_VALIDATION` | Necesita validacion documental. | Planes o estados previos a checkpoint. | Permiso operativo. | Que validacion parezca ejecucion. | Copy "validacion documental". |
| `REQUIRES_AUTHORIZATION` | Requiere autorizacion humana/contractual. | Pasos bloqueados hasta decision explicita. | Acciones disponibles. | Que parezca boton de autorizacion. | Nota textual sin estilo CTA. |
| `FUTURE` | Futuro/no implementado. | Roadmap, deuda y fases posteriores. | Funcionalidad actual. | Presentar futuro como activo. | "future-only" en metadata. |
| `NOT_AVAILABLE` | Dato no disponible. | Fuentes, payload o read model ausente. | Error fatal o bloqueo P0. | Confundir ausencia con falla operativa. | Empty state documental. |
| `DOCUMENTATION_ONLY` | Es documentacion, no control. | Planes, contratos, evidence docs. | Controles UI. | Que parezca pantalla funcional. | Label de seccion. |
| `EVIDENCE_ONLY` | Evidencia/trazabilidad. | Checkpoints, snapshots y pruebas. | Logs vivos o payload crudo. | Confundir con monitoreo live. | Summary verificable. |

## Patrones read-only / blocked / no-runtime

- patron visual read-only: superficie neutral, texto inspeccionable, cursor no operativo, copy claro y ausencia de affordance primaria.
- patron visual blocked: borde/estado contractual, control disabled si existe, causa visible y sin promesa de desbloqueo desde UI.
- patron visual no-runtime: label P0 cuando la zona podria parecer viva, copy "no runtime" y ausencia de animacion/progreso vivo.
- patron visual no-execution: label P0 en request/dispatch/preview, texto "no execution" y sin botones de run/send.
- patron visual documentation-only: aspecto de documento o facts, no formulario, no CTA.
- patron visual evidence-only: muestra referencia, checkpoint o summary; sin payload crudo, sin mutacion y sin live log.
- patron visual future/not available: etiqueta `FUTURE` o `NOT_AVAILABLE`, copy future-only y no estado activo.
- patron visual requires validation: indica pendiente documental, no permiso operativo.
- patron visual requires authorization: indica gate humano/contractual, no boton de autorizacion implicito.

## Reglas anti-CTA operativo

Prohibiciones para futuros cambios visuales:

- botones que parezcan ejecutar;
- labels ambiguos como iniciar/activar/procesar/despachar/enviar;
- colores/estilos que parezcan accion primaria;
- affordances clickables sin accion real;
- cards que parezcan seleccionables si no lo son;
- hover que sugiera operacion;
- iconos de play/run/send;
- `ready to run`;
- success operativo falso;
- progreso vivo falso;
- active/running/live/submitted/dispatching/executing como estados de ejecucion.

## Patrones evidence/documentation

- Mostrar evidencia sin payload crudo: summary, referencia documental, checkpoint, hash o source seguro.
- Mostrar detalle sin mutacion: disclosure o panel de lectura con `read-only`, sin submit ni fetch nuevo.
- Mostrar contract facts: pares clave/valor estables, IDs, estado y fuente.
- Mostrar blocked facts: blocker, causa, forbidden action y alcance; no remediation CTA.
- Mostrar readiness facts: readiness como dato documental, no permiso de ejecucion.
- Mostrar previews contractuales: `draft / not final`, `DEFER_FINALIZATION`, no submit, no send, no dispatch.
- Mostrar futuras capacidades sin venderlas como presentes: `FUTURE`, `NOT_AVAILABLE`, planned y copy future-only.
- Separar documentacion de accion: labels y facts no deben compartir estilo con controles ejecutables.
- Todo evidence/documentation debe quedar sin payload crudo y sin mutacion.

## Criterios responsive

- desktop ancho: mantener P0 visible, no expandir texto en lineas excesivamente largas, usar grid solo si las cards respiran.
- desktop medio: priorizar stack parcial y agrupar badges.
- Tablet: reducir columnas, mover metadata a linea secundaria y mantener bloques de contrato en orden.
- Mobile: una columna, copy corto, badges agrupados y sin overflow de IDs/estados largos.
- Colapsar grids cuando el ancho fuerce columnas demasiado angostas.
- Reducir badges visibles cuando el wrap desplaza contenido principal.
- Priorizar texto cuando un badge no aporta informacion nueva.
- Mover metadatos a linea secundaria si compiten con titulo o estado.

Nunca debe ocultarse:

- bloqueos;
- `DEFER_FINALIZATION`;
- no-runtime/no-execution;
- identificacion de FSC;
- identidad IA_CORE;
- ausencia de acciones operativas.

## Aplicacion futura por fases

1. Planificar reglas/tokens.
2. Implementar tokens/layout base de baja invasion.
3. Revisar visualmente.
4. Checkpoint.
5. Aplicar a otras zonas mas riesgosas solo despues.

La futura implementacion debe evitar refactor masivo, cambio simultaneo de muchas zonas, JS, backend, elementos inferiores, rutas/hash y User Panel.

## Evaluacion restore point

Decision: no publicar en este prompt.

El ultimo restore point remoto `570b18f` es seguro. Desde entonces hay cuatro commits locales: plan FSC rehousing, implementacion FSC rehousing, checkpoint FSC rehousing y planificacion post FSC rehousing. Este prompt es documental; despues de este prompt habra cinco commits locales. Antes de implementar cambios visuales activos de density/tokens, probablemente convenga publicar restore point. Este prompt NO debe hacer push.

Recomendacion: si este plan queda aprobado, el proximo paso debe decidir/publicar restore point antes de implementar tokens/density.

## Decision final

`DESIGN_SYSTEM_DENSITY_REFINEMENT_PLAN_READY_FOR_RESTORE_POINT_DECISION`

## Justificacion

La planificacion queda suficientemente cerrada para pasar a una decision de restore point. Antes de implementar cambios visuales activos de density/tokens conviene decidir/publicar restore point porque, despues de este commit, habra cinco commits locales sobre `origin/main`.

## Proximo prompt exacto

`PROMPT UI/UX 1.133 - Decidir publicación restore point antes de implementar Design System Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento bloque nuevo;
- no se implemento polish visual;
- no se modifico UI activa;
- no se modifico JS;
- no se modificaron Final Screen Contracts;
- no se modificaron elementos inferiores;
- no se modifico contrato funcional;
- no se creo contrato final;
- no se contradijo `DEFER_FINALIZATION`;
- no se creo User Panel;
- no se crearon rutas/hash;
- no se crearon endpoints/fetches nuevos;
- no se activo runtime/execution/dispatch;
- no runtime;
- no se toco backend/runtime/endpoints/CI/dependencias;
- no CI;
- no se limpio deuda residual general;
- no deuda residual;
- no se corrigieron pyflakes;
- no pyflakes;
- no se hizo push;
- no push;
- no se avanzo a 1.133.
