# IA_CORE - Libro Backend Interno - Diseno

## 1. Proposito del libro

Este libro define el backend interno que debe convertir propuestas derivadas en artefactos operativos reales de forma controlada, testeable y reversible.

El libro no materializa nada por si mismo. Fija reglas, estados, contratos y criterios para una fase posterior donde IA_CORE pueda crear un dominio sandbox real, `profile_catalog`, `agent_presets`, papers, agentes, equipos, rollback, regeneracion segura y contrato backend estable para UI.

La UI no debe resolver logica de negocio, materializacion, validacion, rollback ni estados. La UI consume un backend interno estable.

## 2. Estado base posterior a CORE 01

La base auditada queda asi:

- La Biblioteca Profesional Global esta cerrada y documentada.
- `catalogs/professional_profiles.json` es fuente de verdad para perfiles profesionales globales.
- Matriz, recomendaciones, `profile_catalog`, `agent_presets`, team templates y validacion end-to-end son artefactos derivados y no operativos.
- RESET 01 archivo la identidad legacy de Loteria y movio arquetipos reutilizables a `catalogs/agent_archetypes.json`.
- CORE 01 agrego unicidad de dominios y bloqueo de dominios duplicados/equivalentes.
- `domains/loteria/domain.json` esta marcado como `status=legacy`, `legacy=true` y `visible_en_hud=false`.
- `domains/loteria/profile_catalog.json` y `domains/loteria/agent_presets.json` son estructuras minimas no operativas.
- Los snapshots legacy de dominios y Loteria viven en `docs/legacy/`.
- No hay dominio sandbox real materializado para este libro.

## 3. Principio PASSED aplicado al backend interno

Nada operativo puede quedar como fantasma.

Un artefacto operativo PASSED debe ser:

- validado;
- coherente;
- trazable;
- no duplicado;
- no legacy activo por accidente;
- no decorativo;
- ejecutable o consumible por el backend segun corresponda;
- cubierto por tests o validaciones;
- reversible cuando aplica;
- con errores legibles si falla.

`activo=true` o `status=active` no son decoracion: significan que el artefacto puede entrar en flujo operativo real.

## 4. Artefacto derivado vs artefacto operativo real

Artefacto derivado, preview o propuesta:

- Puede existir como simulacion, recomendacion, salida previa o fixture documental.
- No es operativo.
- No debe ser tratado como materializado.
- Puede contener gaps, warnings y riesgos.
- Puede vivir en `docs/`, `docs/generated/` o una salida temporal segura.
- No crea dominios, agentes, papers, presets ni equipos.

Artefacto operativo real:

- Existe en filesystem o registry operativo.
- Tiene estado.
- Tiene trazabilidad.
- Tiene validacion previa y posterior.
- Tiene rollback cuando aplica.
- Puede ser consumido por servicios internos o UI mediante contrato backend.
- Debe poder explicar su origen, version, dependencias y errores.

## 4.1 Contrato derivado vs operativo real

El contrato tecnico vive en `core/artifact_state.py`. Su objetivo es impedir que una salida calculada, sugerida o previsualizada sea confundida con un artefacto real de IA_CORE.

Estados definidos:

- `derived_preview`: salida generada para revision. No escribe artefacto operativo. No puede ser consumida como materializada.
- `ready_to_materialize`: salida derivada validada y lista para materializacion posterior. Todavia no es operativa.
- `materialized`: artefacto escrito en filesystem o registry sandbox con manifest o trazabilidad minima. No necesariamente activo.
- `active`: artefacto operativo PASSED, usable por backend o flujo correspondiente.
- `archived`: artefacto retirado del flujo activo, conservado por trazabilidad.
- `legacy`: artefacto historico conservado, no parte del flujo nuevo salvo recuperacion formal.
- `broken`: artefacto inconsistente, incompleto o fallido. No puede usarse.

Transiciones validas:

- `derived_preview -> ready_to_materialize`
- `ready_to_materialize -> materialized`
- `materialized -> active`
- `active -> archived`
- `materialized -> archived`
- `legacy -> ready_to_materialize` solo mediante recuperacion formal
- cualquier estado relevante puede pasar a `broken` si falla validacion critica
- `broken -> derived_preview` o `broken -> ready_to_materialize` solo mediante regeneracion validada

Transiciones invalidas:

- `derived_preview -> active`
- `ready_to_materialize -> active` sin materializacion
- `legacy -> active` sin recuperacion formal
- `broken -> active` sin reparacion
- `archived -> active` sin restore y validacion

Relacion con PASSED:

Solo `active` con trazabilidad completa equivale a PASSED operativo y puede aparecer como usable. `derived_preview`, `ready_to_materialize`, `materialized`, `archived`, `legacy` y `broken` no son opciones usables por defecto. Estados desconocidos, incluidos valores transicionales historicos como `proposed` o `draft`, no pasan como operativos.

Impacto sobre UI:

La UI puede mostrar previews, warnings y proximas acciones, pero no debe inferir que una propuesta existe operativamente. La UI debe consumir estado y permisos desde backend. Si un helper genera un `profile_catalog`, ese resultado es `derived_preview` o `ready_to_materialize`; no se vuelve real hasta escribirse bajo un sandbox con manifest y validacion.

Ejemplos:

- `profile_catalog` generado por helper: `derived_preview` / `ready_to_materialize`, no operativo.
- `profile_catalog` escrito dentro de `domains/sandbox_x/profile_catalog.json` con manifest: `materialized`.
- `profile_catalog` validado, consistente y usable: `active` / PASSED.
- `paper_seed_expected`: derivado, no paper real.
- paper real escrito y validado: `materialized` o `active` segun estado.

## 4.2 Inventario de artefactos actuales y previstos

Artefactos derivados detectados hoy:

- `derived_profile_catalog`: generado por `core/professional_profile_catalog_generator.py`; existe como salida derivada, no como catalogo operativo.
- `derived_agent_presets`: generado por `core/professional_agent_preset_generator.py`; existe como salida derivada, no como presets reales.
- `derived_team_template`: generado por `core/professional_team_template_generator.py`; existe como plantilla derivada, no como equipo real.
- `derived_model_recommendation`: generado por `core/professional_model_recommendation.py` y usado en generadores; recomendacion, no seleccion operativa obligatoria.
- `derived_paper_seed`: presente como `paper_seed_expected` y `paper_seed` en presets derivados; no es paper real.
- `derived_end_to_end_output`: generado por `core/professional_domain_end_to_end.py`; valida cadena completa sin modificar dominios.

Artefactos operativos reales detectados o previstos:

- `domain_registry_entry`: `domains/*/domain.json`, cargado por `core/domain_registry.py`; puede ser visible o interno segun estado/metadata.
- `materialized_domain`: previsto para Fase 1 bajo sandbox; no existe todavia para este libro.
- `materialized_profile_catalog`: previsto para Fase 2 bajo `domains/<sandbox>/profile_catalog.json`; no existe todavia para este libro.
- `materialized_agent_presets`: previsto para Fase 2 bajo `domains/<sandbox>/agent_presets.json`; no existe todavia para este libro.
- `materialized_paper`: previsto para Fase 3 bajo `domains/<sandbox>/agents/papers/`; no se crea en Fase 0.
- `materialized_agent`: previsto para Fase 4 bajo `domains/<sandbox>/agents/config/`; no se crea en Fase 0.
- `materialized_team`: previsto para Fase 5 mediante manifest de equipo; no existe todavia.

Artefactos historicos o no operativos:

- `legacy_artifact`: Loteria historica y arquetipos recuperados en `docs/legacy/loteria/` y `catalogs/agent_archetypes.json`.
- `archived_artifact`: snapshots de dominios y legacy en `docs/legacy/`.
- `broken_artifact`: categoria reservada para artefactos incompletos, invalidos o fallidos; no debe aparecer como usable.

## 5. Alcance del libro

Este libro cubre solo backend interno:

- estados internos de artefactos;
- preview y validacion;
- aprobacion interna o humana cuando corresponda;
- materializacion sandbox;
- manifest de materializacion;
- trazabilidad;
- rollback;
- regeneracion segura;
- errores accionables;
- contrato backend estable para UI;
- fixtures y tests de contrato.

## 6. Fuera de alcance explicito

Quedan fuera de este libro o de este prompt:

- UI/UX final;
- HUD final;
- n8n;
- Hermes Agent;
- Home Assistant;
- WhatsApp;
- Gmail;
- Sheets;
- Calendar;
- Drive;
- CRM;
- APIs externas;
- dominios productivos reales sin sandbox previo;
- ejecucion externa sin aprobacion;
- recuperacion completa del legacy historico de Loteria;
- orquestador principal futuro;
- automatizaciones externas;
- integraciones con providers en vivo salvo validaciones posteriores explicitamente aprobadas.

Las integraciones futuras pueden quedar como direccion conceptual, no como implementacion.

## 7. Fases del libro

### Fase 0 - Reglas internas, estados y contrato de materializacion

- Objetivo: definir estados, tipos de artefacto, invariantes, permisos y contrato conceptual.
- Entregable esperado: documento tecnico y tests unitarios de estados/contrato si se implementa codigo.
- Puede tocar: docs, constantes/modelos internos si un prompt posterior lo autoriza.
- No debe tocar: dominios reales, UI final, integraciones externas.
- Criterio de cerrado: estados y transiciones quedan definidos, testeados si hay codigo, y sin ambiguedad entre derivado y operativo.
- Tests esperables: validacion de estados, transiciones invalidas, errores legibles.
- Riesgos: sobredisenar antes de materializar; mezclar preview con operacion.
- Posibles subprompts: `PROMPT 0.1 - Estados internos y contrato de materializacion`.

### Fase 1 - Dominio sandbox real

- Objetivo: crear un dominio sandbox controlado para probar materializacion sin afectar dominios historicos.
- Entregable esperado: dominio sandbox con manifest, estado, trazabilidad y no equivalencia con dominios existentes.
- Puede tocar: carpeta sandbox bajo `domains/` solo cuando el prompt lo autorice.
- No debe tocar: Loteria legacy, dominios productivos, snapshots legacy.
- Criterio de cerrado: dominio visible solo segun estado definido, no duplicado, con rollback o limpieza documentada.
- Tests esperables: unicidad, visibilidad, estado, schema de `domain.json`.
- Riesgos: crear otro dominio vacio que parezca operativo.
- Posibles subprompts: `PROMPT 1.0 - Crear dominio sandbox real`.

### Fase 2 - Materializacion de profile_catalog y presets

- Objetivo: convertir derivados aprobados en `profile_catalog.json` y `agent_presets.json` sandbox reales.
- Entregable esperado: archivos operativos sandbox validados contra catalogos globales.
- Puede tocar: `domains/<sandbox>/profile_catalog.json`, `domains/<sandbox>/agent_presets.json`.
- No debe tocar: catalogos globales salvo bug bloqueante reportado, dominios productivos.
- Criterio de cerrado: cada perfil usable tiene preset, trazabilidad a perfil global, policy de modelo y estado PASSED.
- Tests esperables: consistencia profile/preset, schemas, active_only, gaps rechazados.
- Riesgos: copiar outputs derivados sin aprobacion; perder source ids.
- Posibles subprompts: `PROMPT 2.0 - Materializar profile_catalog sandbox`.

### Fase 3 - Papers reales y memoria documental

- Objetivo: materializar papers minimos reales para agentes sandbox aprobados.
- Entregable esperado: papers versionados, trazables a preset/profile y validables.
- Puede tocar: `domains/<sandbox>/agents/papers/` y manifest documental del sandbox.
- No debe tocar: papers legacy, memoria externa, integraciones.
- Criterio de cerrado: cada paper requerido existe, tiene origen, alcance, limites, criterios y estado.
- Tests esperables: existencia, schema, referencias a preset/agente, no placeholders.
- Riesgos: generar papers decorativos o demasiado generales.
- Posibles subprompts: `PROMPT 3.0 - Materializar papers sandbox`.

### Fase 4 - Agentes reales sandbox

- Objetivo: crear agentes ejecutables dentro del sandbox desde presets y papers PASSED.
- Entregable esperado: configs de agentes sandbox con metadata, modelo, paper y policy coherentes.
- Puede tocar: `domains/<sandbox>/agents/config/`.
- No debe tocar: agentes legacy, UI final, providers externos.
- Criterio de cerrado: agentes cargan, validan y no dependen de defaults criticos ocultos.
- Tests esperables: schema de agente, carga runtime, referencias paper/preset, errores.
- Riesgos: crear agentes con prompts genericos o sin paper real.
- Posibles subprompts: `PROMPT 4.0 - Materializar agentes sandbox`.

### Fase 5 - Equipos reales sandbox

- Objetivo: componer agentes sandbox en equipos operativos minimos.
- Entregable esperado: team manifest con roles, dependencias, objetivo y criterios.
- Puede tocar: manifest de equipos sandbox si se define ubicacion.
- No debe tocar: orquestador futuro principal ni automatizaciones externas.
- Criterio de cerrado: cada equipo referencia agentes reales, tiene objetivo, limites, outputs y estado.
- Tests esperables: referencias cruzadas, roles obligatorios, ausencia de agentes inexistentes.
- Riesgos: llamar equipo a una lista decorativa de agentes.
- Posibles subprompts: `PROMPT 5.0 - Materializar equipos sandbox`.

### Fase 6 - End-to-end operativo, rollback y regeneracion

- Objetivo: probar el ciclo completo desde intencion hasta artefactos reales con rollback y regeneracion segura.
- Entregable esperado: flujo backend interno reproducible, manifest y reporte de validacion.
- Puede tocar: servicios backend internos y sandbox.
- No debe tocar: UI final ni integraciones externas.
- Criterio de cerrado: puede materializar, validar, revertir y regenerar sin duplicar ni pisar cambios manuales.
- Tests esperables: e2e sandbox, rollback parcial/total, idempotencia, conflictos.
- Riesgos: rollback incompleto; regeneracion destructiva.
- Posibles subprompts: `PROMPT 6.0 - End-to-end sandbox con rollback`.

### Fase 7 - Contrato backend para UI

- Objetivo: exponer endpoints o funciones internas estables para que la UI consuma previews, estados y acciones.
- Entregable esperado: contrato versionado para preview, validation, materialization, status, rollback y next_actions.
- Puede tocar: backend/API interno y documentacion de contrato.
- No debe tocar: UI final salvo fixtures o smoke minimo autorizado.
- Criterio de cerrado: la UI no necesita inferir estados ni reglas de negocio.
- Tests esperables: contrato de respuestas, codigos de error, payloads estables.
- Riesgos: filtrar decisiones de negocio hacia frontend.
- Posibles subprompts: `PROMPT 7.0 - Contrato backend/UI`.

### Fase 8 - Tests de contrato, errores y fixtures

- Objetivo: fijar fixtures y pruebas de errores legibles para UI.
- Entregable esperado: suite de contrato con casos PASSED, warnings, conflicts y failures.
- Puede tocar: tests, fixtures y helpers internos.
- No debe tocar: dominios productivos ni integraciones.
- Criterio de cerrado: los errores son accionables y los fixtures representan estados reales.
- Tests esperables: snapshots/payloads, errores por duplicado, falta de aprobacion, rollback no disponible.
- Riesgos: tests que solo congelan forma sin validar significado.
- Posibles subprompts: `PROMPT 8.0 - Fixtures y errores de contrato`.

### Fase 9 - Cierre del backend interno

- Objetivo: consolidar evidencia, deuda futura y criterio de salida hacia UI/productivo.
- Entregable esperado: reporte de cierre, tests verdes, commit limpio.
- Puede tocar: documentacion de cierre y decisiones arquitectonicas reales.
- No debe tocar: nuevas features laterales.
- Criterio de cerrado: sandbox demuestra operacion controlada y la UI tiene contrato estable.
- Tests esperables: suite completa relevante, contrato, e2e sandbox.
- Riesgos: cerrar por relato sin evidencia.
- Posibles subprompts: `PROMPT 9.0 - Cierre Backend Interno`.

## 8. Criterios de cierre por fase

Cada fase cierra solo si:

- sus entregables existen;
- no materializa piezas fuera de su alcance;
- conserva trazabilidad;
- tiene tests reales o validaciones ejecutables acordes al riesgo;
- reporta gaps, warnings y riesgos;
- deja `git status --short` limpio despues del commit;
- no introduce dominios duplicados o legacy activo por accidente.

## 9. Criterios de cierre para dominio sandbox

Un dominio sandbox cierra PASSED si:

- no es equivalente a dominios activos, legacy o archivados;
- tiene `domain.json` valido;
- declara estado explicito;
- su visibilidad no confunde sandbox con productivo;
- tiene manifest de origen;
- no depende de Loteria ni de defaults legacy;
- puede eliminarse o revertirse segun politica del libro.

## 10. Criterios de cierre para profile_catalog sandbox

`profile_catalog` sandbox cierra PASSED si:

- deriva de `catalogs/professional_profiles.json` o de una fuente aprobada;
- conserva `source_profile_id`;
- valida `role_id` y `specialization_id`;
- no expone perfiles sin preset esperable;
- separa activos de inactivos;
- no contiene proposed/draft usables;
- tiene errores legibles ante referencias invalidas.

## 11. Criterios de cierre para agent_presets sandbox

`agent_presets` sandbox cierra PASSED si:

- cada preset corresponde a un perfil activo del sandbox;
- conserva trazabilidad a perfil global y profile_catalog;
- incluye system prompt revisado, decision criteria, avoid, memory policy y paper seed;
- incluye policy o recomendacion de modelo;
- no promete resultados garantizados;
- no queda como semilla decorativa tratada como agente real.

## 12. Criterios de cierre para papers

Un paper real cierra PASSED si:

- existe como archivo operativo en el sandbox;
- referencia agente, preset, perfil y dominio;
- contiene identidad, alcance, metodologia, limites, riesgos y criterios de actualizacion;
- no copia legacy como identidad activa;
- no es un placeholder;
- puede validarse por schema o reglas internas.

## 13. Criterios de cierre para agentes reales sandbox

Un agente sandbox cierra PASSED si:

- tiene config ejecutable;
- referencia paper existente;
- referencia preset/profile validos;
- declara provider/model o policy resuelta;
- conserva metadata de origen;
- carga desde backend sin ambiguedad;
- falla con error legible si falta una dependencia.

## 14. Criterios de cierre para equipos reales sandbox

Un equipo sandbox cierra PASSED si:

- referencia agentes reales existentes;
- declara objetivo, roles, interaccion, outputs, limites y riesgos;
- no depende de agentes decorativos;
- puede validarse sin ejecutar integraciones externas;
- tiene manifest y estado.

## 15. Criterios de cierre para end-to-end operativo sandbox

El e2e sandbox cierra PASSED si demuestra:

- input/intencion;
- preview;
- validacion;
- aprobacion cuando corresponda;
- materializacion;
- manifest;
- validacion post-materializacion;
- exposicion por contrato backend;
- rollback disponible;
- regeneracion segura;
- errores legibles para casos negativos.

## 16. Criterios de cierre para rollback

Rollback cierra PASSED si:

- conoce exactamente que archivos y registros creo o modifico;
- puede revertir por manifest;
- distingue rollback total y parcial si aplica;
- no borra artefactos preexistentes no creados por la operacion;
- reporta estado final y fallas;
- tiene tests de conflicto e idempotencia.

## 17. Criterios de cierre para regeneracion segura

Regeneracion segura cierra PASSED si:

- compara origen, version y manifest previo;
- detecta cambios manuales;
- no sobrescribe sin aprobacion;
- conserva historial o snapshot cuando aplica;
- no duplica dominios ni artefactos;
- deja evidencia auditable.

## 18. Criterios de cierre para contrato backend/UI

El contrato backend/UI cierra PASSED si:

- versiona endpoints o funciones internas;
- entrega `status`, `artifact_type`, `operational`, `traceability`, `warnings`, `errors` y `next_actions` cuando aplique;
- separa preview, validation, materialization, status, rollback y regeneration;
- no exige que la UI infiera reglas de negocio;
- cubre errores esperables con payload estable;
- tiene tests de contrato.

## 19. Criterios de errores legibles para UI

Un error legible para UI debe incluir:

- codigo estable;
- mensaje humano claro;
- severidad;
- artefacto afectado;
- estado actual;
- causa probable;
- accion recomendada;
- si la accion es reintentable;
- si requiere aprobacion humana;
- referencias de trazabilidad disponibles.

La UI puede mostrar el error, pero no resolver la regla que lo produjo.

## 20. Contrato conceptual de materializacion controlada

Flujo esperado:

```text
input/intencion
-> preview
-> validacion
-> aprobacion interna/humana cuando corresponda
-> materializacion sandbox
-> manifest
-> validacion post-materializacion
-> rollback disponible
-> regeneracion segura
-> exposicion por contrato backend
```

Este flujo queda disenado, no implementado en este prompt.

## 21. Limites UI/backend

La UI puede:

- pedir previews;
- mostrar estados;
- mostrar errores;
- pedir validaciones;
- pedir materializacion cuando el backend lo permita;
- mostrar `next_actions`.

La UI no debe:

- decidir reglas de negocio;
- crear archivos por su cuenta;
- inferir estados;
- reparar inconsistencias;
- materializar sin backend;
- saltear validaciones;
- inventar defaults criticos;
- resolver rollback.

## 22. Riesgos principales

- Confundir artefactos derivados con operativos.
- Crear un sandbox vacio visible como producto real.
- Activar legacy por accidente.
- Copiar seeds como prompts finales.
- Materializar sin rollback.
- Sobrescribir trabajo manual durante regeneracion.
- Dejar a la UI interpretando reglas internas.
- Agregar integraciones externas antes de cerrar el core interno.

## 23. Subprocesos esperables

- Definir modelo de estados internos.
- Definir manifest de materializacion.
- Definir formato de preview.
- Definir politica de aprobacion humana.
- Crear dominio sandbox real.
- Materializar `profile_catalog` sandbox.
- Materializar `agent_presets` sandbox.
- Materializar papers reales.
- Crear agentes reales sandbox.
- Crear equipos sandbox.
- Implementar rollback y regeneracion segura.
- Versionar contrato backend/UI.
- Crear fixtures de contrato y errores.

## 24. Deudas futuras documentadas

- Panel admin de dominios con archivar, restaurar, resetear, eliminar y ver dependencias.
- Recuperacion legacy de Loteria solo como libro o subprompt separado.
- Validacion de providers/modelos en vivo.
- Integracion n8n y automatizaciones externas.
- Orquestador principal futuro.
- UI/UX final sobre contrato backend estable.
- Politicas de permisos por usuario o rol.
- Versionado formal de manifests y migraciones.

## 25. Inconsistencias detectadas durante el diseno

No se detecto una inconsistencia bloqueante para crear este documento.

Condicionantes no bloqueantes:

- El documento externo de Direccion de Producto no aparece como archivo versionado dentro del repo; el diseno usa el prompt adjunto como fuente vigente de direccion.
- Existen archivos legacy de Loteria en `domains/loteria/`, pero el dominio esta oculto y marcado como legacy, coherente con CORE 01.
- El README del repo se considera documento tecnico viejo, no brujula estrategica.

No corresponde abrir `PROMPT 0.0.1` antes de cerrar este prompt.
