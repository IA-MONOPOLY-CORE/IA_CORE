# Auditoria Role/Specialization De Perfiles Profesionales

Prompt 18.8 normaliza la relacion entre perfiles profesionales globales, roles globales y especializaciones globales.

## Resumen Ejecutivo

La auditoria encontro una base estructuralmente sana:

- Perfiles globales: 106.
- Roles globales: 20.
- Especializaciones globales: 80.
- `expected_role_id` validos: 106 de 106.
- `expected_specialization_id` validos: 106 de 106.
- Valores `pending`/`required`: 0.
- Desajustes entre rol esperado y rol de la especializacion: 0.
- Roles usados por perfiles: 20 de 20.
- Especializaciones usadas por perfiles: 49 de 80.

No se agregaron roles ni especializaciones. Los gaps documentados en prompts anteriores eran semanticos, no roturas de catalogo. La decision de normalizacion fue reutilizar los roles y especializaciones existentes, reforzar el test de integridad y documentar que los gaps restantes deben resolverse en presets/papers o en una expansion futura basada en uso real.

## Totales

| Dimension | Antes | Despues |
| --- | ---: | ---: |
| Perfiles globales | 106 | 106 |
| Roles globales | 20 | 20 |
| Especializaciones globales | 80 | 80 |
| `expected_role_id` validos | 106 | 106 |
| `expected_specialization_id` validos | 106 | 106 |
| `expected_role_id` pending/required/invalid | 0 | 0 |
| `expected_specialization_id` pending/required/invalid | 0 | 0 |

## Roles Mas Usados

- `coordinador`: 14 perfiles.
- `auditor`: 11 perfiles.
- `especialista_comunicacion`: 10 perfiles.
- `analista`: 10 perfiles.
- `planificador`: 9 perfiles.
- `estratega`: 7 perfiles.
- `arquitecto_sistemas`: 7 perfiles.
- `archivista`: 6 perfiles.
- `gestor_riesgo`: 5 perfiles.
- `optimizador`: 4 perfiles.
- `validador`: 4 perfiles.

Todos los roles activos tienen al menos un perfil global que los usa.

## Especializaciones Mas Usadas

- `coordinacion_flujos`: 8 perfiles.
- `comunicacion_persuasiva`: 5 perfiles.
- `analisis_datos`: 5 perfiles.
- `comunicacion_clara`: 5 perfiles.
- `planificacion_operativa`: 4 perfiles.
- `estrategia_crecimiento`: 3 perfiles.
- `coordinacion_interareas`: 3 perfiles.
- `planificacion_hitos`: 3 perfiles.
- `arquitectura_procesos`: 3 perfiles.
- `auditoria_calidad`: 3 perfiles.
- `optimizacion_procesos`: 3 perfiles.
- `archivo_documental`: 3 perfiles.
- `auditoria_riesgo`: 3 perfiles.
- `auditoria_consistencia`: 3 perfiles.

Hay 31 especializaciones activas sin uso por perfiles globales en esta etapa. No son errores: forman parte del catalogo global base y quedan disponibles para presets, papers, equipos o perfiles futuros.

## Gaps Agrupados Por Familia Profesional

| Familia | Lectura de gaps | Decision 18.8 |
| --- | --- | --- |
| `automatizacion_tecnologia` | CRM operativo, no-code/low-code, APIs, webhooks, monitoreo, SaaS tooling y documentacion tecnica. | Reutilizar `arquitecto_sistemas`, `coordinador`, `optimizador`, `detector_anomalias`, `archivista` y `planificador`; no crear rol tecnico nuevo. |
| `datos_analytics` | BI avanzado, data quality, dashboards, reporting y segmentacion. | Reutilizar `analista`, `sintetizador`, `validador`, `arquitecto_sistemas` y `simulador`; no crear especializacion BI todavia. |
| `ventas_revenue` | WhatsApp/CRM, pipeline, revenue systems y ventas consultivas. | Reutilizar `arquitecto_sistemas`, `especialista_comunicacion` e `integrador_central`; resolver operatividad en presets. |
| `marketing_growth` | Marketing local, promociones, calendario comercial y performance. | Reutilizar estrategia, planificacion, comunicacion y optimizacion existentes. |
| `finanzas_administracion` | Caja diaria, flujo de caja, presupuesto, cobros, precios y margenes. | Reutilizar analisis, auditoria, planificacion y gestion de recursos; no crear rol financiero. |
| `legal_compliance` | Contratos, compliance pyme, privacidad y riesgo legal. | Reutilizar `auditor` y `gestor_riesgo`; mantener revision humana en prompts futuros. |
| `rrhh_capacitacion` | Onboarding, capacitacion, desempeno, roles y cultura. | Reutilizar planificacion, comunicacion, coordinacion, validacion y memoria. |
| `soporte_customer_success` | Soporte multicanal, postventa, satisfaccion, NPS y base de respuestas. | Reutilizar observacion conductual, coordinacion, comunicacion, archivo y analisis. |
| `calidad_riesgo` | SOPs, QA, continuidad, riesgo operativo y sesgos. | Reutilizar auditoria, deteccion, supervision, validacion, riesgo, planificacion y critica. |
| `industria_oficios` | Comercio exterior, construccion, ingenieria, mineria/energia, portuario y salud/farmacia. | Reutilizar coordinacion, planificacion, validacion y riesgo; no crear roles sectoriales por ahora. |

## Gaps Agrupados Por Area/Nicho

- Comercial / WhatsApp / CRM: cubierto con `especialista_crm_whatsapp`, `operador_ventas_whatsapp`, `coordinador_canal_whatsapp`, `arquitecto_crm_operativo`, `revenue_operations_manager` y `coordinador_soporte_multicanal`.
- Pyme / local: cubierto con perfiles de caja, costos, gastos, compras, stock, turnos, tareas, operacion diaria, marketing barrial y promocion local.
- Datos / BI / tecnica: cubierto con perfiles de datos, BI, reporting, calidad de datos, integraciones, APIs, QA, monitoreo y documentacion tecnica.
- Legal / finanzas / RRHH / compliance: cubierto con perfiles de contratos, compliance, privacidad, politicas, caja, cobros, precios, onboarding, capacitacion, desempeno y continuidad.
- Sectoriales: cubierto tras 18.7.A con perfiles de aduana/comercio exterior, construccion, ingenieria, mineria/energia, portuario y salud/farmacia.

## Gaps Repetidos

- Necesidad de especializaciones mas nominales por vertical operativo: CRM, BI, finanzas pyme, legal pyme, soporte y no-code.
- Necesidad de presets que bajen roles genericos a instrucciones operables por escala.
- Necesidad de papers que expliquen limites, inputs, outputs y revision humana en areas sensibles.

## Gaps Unicos

- Algunas areas sectoriales tienen cobertura minima, pero aun no profundidad: comercio exterior, portuario, mineria/energia, salud/farmacia, construccion e ingenierias.
- Algunas especializaciones activas aun no fueron usadas por perfiles globales. No bloquean la normalizacion porque el objetivo era conectar perfiles existentes, no forzar consumo de todo el catalogo.

## Reutilizacion De Roles Existentes

La auditoria confirma que los 20 roles actuales alcanzan para los 106 perfiles. Los gaps conocidos no justifican roles nuevos porque:

- no representan una funcion profesional transversal nueva;
- son variantes operativas dentro de roles existentes;
- pueden tener instrucciones especificas en presets;
- no conviene crear roles sectoriales antes de ver uso real.

## Reutilizacion De Especializaciones Existentes

Las especializaciones actuales alcanzan para normalizar todos los perfiles. Las aproximaciones usadas son funcionales:

- BI/reporting: `analisis_datos`, `sintesis_ejecutiva`, `validacion_datos`, `auditoria_consistencia`.
- CRM/WhatsApp: `coordinacion_flujos`, `arquitectura_procesos`, `comunicacion_persuasiva`.
- Finanzas pyme: `administracion_recursos`, `analisis_temporal`, `analisis_datos`, `auditoria_calidad`, `planificacion_operativa`.
- Legal/compliance: `auditoria_cumplimiento`, `auditoria_riesgo`, `priorizacion_riesgos`.
- RRHH: `planificacion_hitos`, `comunicacion_clara`, `coordinacion_equipos`, `validacion_criterios`, `memoria_operativa`.
- Sectoriales: `coordinacion_flujos`, `planificacion_hitos`, `validacion_criterios`, `mitigacion_operativa`, `coordinacion_interareas`.

## Nuevas Especializaciones Recomendadas

Ninguna para agregar en 18.8.

Backlog posible para despues de presets/papers, solo si aparece repeticion real:

- CRM y revenue operations.
- BI/dashboarding operativo.
- Finanzas pyme/cashflow.
- Compliance pyme y privacidad operativa.
- No-code/low-code.
- Soporte multicanal.
- Operaciones sectoriales reguladas.

## Nuevos Roles Recomendados

Ninguno.

Crear roles nuevos ahora seria prematuro: los huecos son variantes concretas, no funciones cognitivas amplias con varias especializaciones futuras ya demostradas.

## Cambios Realizados

- Se creo `tests/test_professional_profile_role_specialization.py`.
- Se creo este reporte de auditoria.
- Se actualizo `docs/PROFESSIONAL_LIBRARY_DESIGN.md`.
- Se actualizo `docs/PROFESSIONAL_PROFILE_COVERAGE_AUDIT.md`.

## Cambios No Realizados Y Motivo

- No se modifico `catalogs/professional_profiles.json`: todos los perfiles ya tenian rol y especializacion validos.
- No se modifico `catalogs/roles.json`: no hay hueco real que justifique rol nuevo.
- No se modifico `catalogs/specializations.json`: no hay pending ni invalidos que exijan especializacion nueva.
- No se agregaron perfiles: 18.8 era normalizacion, no expansion.
- No se tocaron dominios especificos, presets, papers, agentes, HUD, n8n ni orquestadores.

## Riesgos

- Los perfiles con especializaciones genericas podrian necesitar instrucciones mas concretas al generar presets.
- Las areas sectoriales recien cerradas tienen cobertura minima, no profundidad.
- Si Prompt 18.9 intenta generar presets demasiado especificos, podria aparecer la necesidad real de nuevas especializaciones.

## Recomendacion Para Prompt 18.9

Avanzar a cierre del inventario inicial con la biblioteca de 106 perfiles. Prompt 18.9 deberia mantener la regla de no agregar perfiles por cantidad, usar este test como compuerta y preparar la transicion hacia presets/papers sin crear catalogos fantasma.

## Nota 18.9 - Certificacion de cierre

18.9 certifica que la relacion perfil -> rol/especializacion queda validada para la fase inicial.

La biblioteca cierra con 106 perfiles, 106 role_id validos, 106 specialization_id validos, 0 pending y 0 desajustes entre rol esperado y rol de la especializacion. No se agregan roles ni especializaciones en este cierre.
