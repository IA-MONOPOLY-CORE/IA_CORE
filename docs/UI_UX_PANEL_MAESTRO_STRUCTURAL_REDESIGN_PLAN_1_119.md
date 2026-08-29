# UI/UX Panel Maestro Structural Redesign Plan 1.119

## Commit base y objetivo

- Base esperada: `8843b60`.
- Restore point remoto vigente: `01d09ce`.
- Restore point remoto anterior: `ccdef7a`.
- Commit local previo: `8843b60`.

1.119 planifica el rediseño/restyling estructural futuro del Panel Maestro IA_CORE. Es una planificación de arquitectura y responsabilidades visuales, no una implementación. El objetivo es saber qué se conserva, qué se absorbe, qué se separa y qué se elimina antes de tocar la UI activa.

## Estado recibido

- `NEXT_STEP_PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLANNING_SELECTED` seleccionado en 1.118.
- `RESTORE_POINT_PUBLICATION_PUSH_COMPLETED` confirmado en `01d09ce`.
- Local y remoto quedaron sincronizados en el restore point publicado.
- Final Screen Contracts consolidado/publicado: `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04`.
- Elementos inferiores bloqueados, auditados, checkpointeados y publicados.
- `+` y `DOMAIN` son deuda UX futura no bloqueante: duplican intención visual/semántica, pero no habilitan creación operativa.

## Alcance del rediseño estructural

El futuro rediseño deberá planificar:

- jerarquía general del Panel Maestro;
- separación entre bloques y pantallas;
- navegación documental futura;
- organización de Final Screen Contracts;
- organización de elementos inferiores;
- lectura del estado de dominios y agentes;
- tratamiento visual de acciones bloqueadas;
- tratamiento futuro de `CFG`, `+` y `DOMAIN`;
- reducción de ambigüedad y densidad visual;
- lenguaje contract-aware;
- soporte para futuras pantallas correspondientes;
- preservación no-runtime/no-execution;
- IA_CORE como identidad visible activa.

El alcance no crea una pantalla nueva ni modifica la UI actual. Primero se audita la arquitectura existente, luego se documenta la arquitectura visual futura y recién después se preparan guardrails de implementación.

## Estado actual resumido

La UI actual es una UI intermedia/de transición. La baseline de Final Screen Contracts es documental, read-only y contract-aware. La zona inferior permanece como elementos inferiores bloqueados, en lectura, con no acción operativa. `CFG`, `+`, `DOMAIN`, formularios y tarjetas no deben reinterpretarse como capabilities activas. La deuda UX de `+`/`DOMAIN` queda registrada para el rediseño estructural.

## Principios rectores

- Fórmula de decisión: primero verdad, después belleza, después nivel.
- Primero verdad, después belleza, después nivel.
- Nada visible incompleto debe parecer operativo.
- Todo lo que parezca acción debe estar respaldado por contrato.
- Si está bloqueado, debe verse bloqueado.
- Si es lectura, debe verse lectura.
- Si es futuro, debe verse futuro.
- No ghost actions.
- No fake success.
- No raw Package.
- No payload crudo.

Forma verificable de los principios: primero verdad, después belleza, después nivel; no ghost actions, no fake success, no raw Package y no payload crudo.
- No endpoints/fetches nuevos.
- No runtime/execution.
- No User Panel prematuro.
- No rutas/hash prematuras.
- IA_CORE como identidad activa.
- Lotería/SAAOP no son identidad visible activa.
- No corregir deuda visual aislada si pertenece al rediseño estructural.

## Zonas futuras candidatas

Estas zonas son una lista inicial, no definitiva. Todas deben conservar lectura contractual y no habilitar operación por ausencia de datos.

| Zona | Propósito | Tipo | Datos permitidos | Acciones prohibidas | Riesgo principal | Dependencia |
| --- | --- | --- | --- | --- | --- | --- |
| Master Header / Estado global IA_CORE | Identidad, estado y contexto global | Estado/documental | IA_CORE, readiness declarado, límites | Run, execute, unlock | Parecer dashboard operativo | Arquitectura global |
| Contract Status / Final Screen Contracts | Ordenar `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03`, `FSC-RCP-04` | Documental/lectura | Estados, IDs, evidencia segura | Convertir status en permiso | Mezclar contrato con CTA | Baseline publicada |
| Domain Context / Dominio seleccionado | Mostrar contexto de dominio | Lectura/estado | Dominio declarado, fuente, ausencia honesta | Crear, editar, borrar, activar | Selector con semántica operativa | Contrato de datos futuro |
| Agent Context / Agentes y roles | Explicar agentes y roles | Lectura/documental | Identidad, rol, estado declarado | Ejecutar, editar, eliminar | Tarjeta como acción | Modelo visual futuro |
| Readiness & Validation | Comunicar validación y readiness | Documental/estado | Warnings, errors, readiness | Checks vivos, workflow, submit | Passed como éxito operativo | `FSC-VR-03` |
| Blocked Capabilities | Mostrar límites y bloqueos | Bloqueado/documental | Capabilities bloqueadas y razones | Unlock, override, bypass | Bloqueo ambiguo | `FSC-BF-02` |
| Request Preview / Contract Preview | Representar solicitud diferida | Futuro/documental | `CFD-04`, draft, summary seguro | Submit, send, dispatch, run | Preview como ejecución | `FSC-RCP-04` |
| Evidence / Details | Exponer trazabilidad local | Lectura/documental | Evidence snapshot y detalles | Live log, fetch, timeline operativo | Evidencia como runtime | Contrato de evidencia |
| Configuration Read-only | Explicar configuración declarada | Lectura/bloqueado | Valores seguros y estado | Guardar, aplicar, mutar | Formulario accionable | Guardrails futuros |
| Future Actions Blocked | Reservar espacio para futuro | Futuro/bloqueado | Intenciones y límites | Habilitar CTA sin contrato | Ghost action | Contrato explícito |
| System Notes / Deuda UX / Roadmap | Registrar notas y próximos pasos | Documental/futuro | Deuda, decisiones, roadmap | Convertir nota en task activo | Roadmap como workflow | Gobernanza documental |
| Navigation / Screen Index | Ordenar navegación futura | Documental | Índice, foco, relación entre pantallas | Crear rutas/hash prematuras | Navegación como User Panel | Arquitectura de pantallas |

## Pantallas candidatas futuras

Este inventario no implementa pantallas ni crea rutas. Cada pantalla necesita contrato, guardrails y aprobación humana antes de una implementación.

| Pantalla | Objetivo | Relación con UI actual | Reemplaza/absorbe/reorganiza | Datos permitidos | Acciones prohibidas | Blockers | Prioridad |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Panel Maestro Overview | Dar mapa general del sistema | Encabezado y resumen actuales | Reorganiza | Identidad, estado, límites | Operar o ejecutar | Arquitectura general | Alta |
| Domains Screen | Explicar dominios y contexto | Superficie `DOMAIN` | Absorbe selector/documentación | Dominios declarados | Crear/mutar sin contrato | Contrato de dominio | Media |
| Agents Screen | Explicar agentes, roles y relación | Tarjetas actuales | Reorganiza tarjetas | Agentes declarados | Ejecutar/editar/borrar | Modelo visual | Media |
| Final Screen Contracts Screen | Agrupar la baseline contractual | Cuatro secciones actuales | Absorbe índice contractual | FSC y evidencia segura | Conceder permiso | Preservar baseline | Alta |
| Validation & Readiness Screen | Hacer legible readiness | `FSC-VR-03` | Conserva/reorganiza | Validation declarada | Checks vivos | No runtime | Alta |
| Blocked Capabilities Screen | Hacer visibles límites | `FSC-BF-02` | Conserva/reorganiza | blocked/forbidden | Unlock/bypass | No CTA operativo | Alta |
| Request Contract Preview Screen | Representar preview diferido | `FSC-RCP-04` | Conserva/reorganiza | Draft y summary | Submit/dispatch | `DEFER_FINALIZATION` | Alta |
| Evidence & Details Screen | Ordenar evidencia y detalles | Disclosures actuales | Absorbe disclosures | Trazabilidad local | Live log/fetch | Fuente estable | Media |
| Configuration Read-only Screen | Mostrar configuración sin mutar | `CFG` bloqueado | Absorbe modal documental | Valores seguros | Save/apply | Read-only | Media |
| Roadmap / Future Work Screen | Documentar evolución futura | Notas y cursor | Absorbe roadmap | Decisiones y fases | Crear workflow activo | Gobernanza | Baja |
| Design System / Visual Tokens Screen | Documentar lenguaje visual | Tokens dispersos | Reorganiza referencias | Tokens y reglas | Cambiar UI en vivo | Aprobación visual | Baja |

## Tratamiento futuro de `+` y `DOMAIN`

- Hoy duplican intención visual/semántica.
- No habilitan creación operativa.
- No bloquean el avance.
- No se corrigen en este prompt.
- Se resolverán en el rediseño estructural.
- Opciones futuras: eliminar `+`.
- Opción futura: conservar `+` solo contextual.
- Opción futura: redefinir `+` como “agregar” dentro de una pantalla específica.
- Opción futura: separar `DOMAIN` como lectura/selector documental.
- Mover la creación real futura a un flujo de preview/materialización/backend validado.
- Mostrar creación directa como bloqueada si no hay contrato.
- No se decide implementación ahora.

## Fases futuras

- `1.120` — Auditoría de arquitectura actual de pantallas/zonas.
- `1.121` — Documento de arquitectura visual futura.
- `1.122` — Guardrails pre-implementación del rediseño estructural.
- `1.123` — Primer bloque de implementación visual si se aprueba.
- `1.124` — Hardening/checkpoint del primer bloque.
- Todo queda sujeto a aprobación humana antes de implementar.

## Risk register

| Riesgo | Mitigación |
| --- | --- |
| Rediseñar sin auditar arquitectura actual | Ejecutar 1.120 antes de dibujar solución final |
| Implementar antes de guardrails | No implementar antes de 1.122 |
| Tocar UI activa prematuramente | Mantener 1.119 solo documental |
| Reactivar controles inferiores | Mantener bloqueo publicado |
| Reabrir POST/PUT/DELETE desde UI | Guardas deny-by-default y revisión por contrato |
| Crear endpoints/fetches nuevos | Prohibición explícita en cada prompt |
| Introducir rutas/hash | Mantener navegación documental |
| Crear User Panel prematuro | Mantenerlo fuera del Panel Maestro |
| Confundir Panel Maestro con User Panel | Separar responsabilidades en arquitectura |
| Convertir lectura en acción | Etiquetar lectura y prohibiciones |
| Convertir futuro en activo | Usar estados futuros/bloqueados visibles |
| Ocultar bloqueos contractuales | Mantener `blocked` y `forbidden` siempre visibles |
| Eliminar trazabilidad | Enlazar decisiones, commits y documentos |
| Mezclar Final Screen Contracts con dominios/agentes | Preservar frontera de cuatro contratos |
| Resolver `+`/`DOMAIN` como parche aislado | Resolver en rediseño estructural |
| No preservar `DEFER_FINALIZATION` | Mantenerlo en toda pantalla futura relacionada |
| Reintroducir Lotería/SAAOP como identidad visible | Mantener IA_CORE como identidad activa |
| Crear fake success | Prohibir estados de éxito operativo |
| Crear ghost actions | Auditar markup, affordance y handlers |
| Exponer raw Package/payload crudo/secrets | Proyección segura y ausencia honesta |
| Limpiar deuda residual fuera de alcance | Dejarla fuera de 1.119 |
| Perder restore point `01d09ce` | Usarlo como baseline y rollback |

## Decisión final

`PANEL_MAESTRO_STRUCTURAL_REDESIGN_PLAN_READY_FOR_ARCHITECTURE_AUDIT`

## Justificación

El restore point `01d09ce` está publicado, la UI actual está bloqueada/read-only y la duplicidad `+`/`DOMAIN` no es operativa ni bloqueante. Antes de documentar una arquitectura visual futura conviene auditar la arquitectura actual de pantallas y zonas: qué se conserva, qué se absorbe, qué se separa y qué se elimina. Esto reduce supuestos, evita hardening prematuro y preserva los límites contract-aware.

## Próximo prompt exacto

`PROMPT UI/UX 1.120 - Auditar arquitectura actual de pantallas y zonas Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Límites preservados

Este documento establece no implementación, no UI activa, no rutas/hash, no User Panel, no backend, no pantalla, no quinta sección, no Final Screen Contracts, no elementos inferiores, no contrato funcional, no contrato final, no endpoints/fetches nuevos, no runtime, no endpoint, no CI, no deuda residual, no pyflakes y no push.

- No se implementó pantalla.
- No se agregó quinta sección.
- No se modificó UI activa.
- No se modificó Final Screen Contracts.
- No se modificaron elementos inferiores.
- No se cambió contrato funcional.
- No se creó contrato final.
- No se contradijo `DEFER_FINALIZATION`.
- No se creó User Panel.
- No se crearon rutas/hash.
- No se crearon endpoints/fetches nuevos.
- No se activó runtime/execution/dispatch.
- No se tocó backend/runtime/endpoints/CI/dependencias.
- No se limpió deuda residual general.
- No se corrigieron pyflakes.
- No se hizo push.
- No se avanzó a 1.120.
