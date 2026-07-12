# Matriz Perfil Profesional <-> Area/Nicho

<!-- GENERATED_BY: scripts/generate_professional_profile_matrix.py -->
<!-- MATRIX_SUMMARY profiles=106 areas=30 niches=200 covered_areas=30 uncovered_areas=0 covered_niches=166 uncovered_niches=34 -->

## Resumen Ejecutivo

Esta matriz es un artefacto derivado para consulta, auditoria y preparacion de fases futuras.

- Fuente de verdad: `catalogs/professional_profiles.json`.
- Catalogos de referencia: `catalogs/areas.json` y `catalogs/niches.json`.
- Total perfiles: 106.
- Total areas: 30.
- Total nichos: 200.
- Areas cubiertas: 30.
- Areas sin cobertura: 0.
- Nichos cubiertos: 166.
- Nichos sin cobertura: 34.

La matriz no reemplaza al catalogo global. Si cambia un perfil, se debe regenerar este archivo ejecutando `python scripts/generate_professional_profile_matrix.py`.

## Regla De Fuente De Verdad

- La fuente de verdad sigue siendo `catalogs/professional_profiles.json`.
- Este reporte se deriva desde `areas_compatibles` y `nichos_compatibles`.
- No editar esta matriz manualmente como si fuera catalogo.
- Los tests validan que la matriz generada coincide con los catalogos.

## Area -> Perfiles Compatibles

| area_id | area | perfiles | profile_ids |
| --- | --- | --- | --- |
| abastecimiento_logistica | Abastecimiento y Logística | 10 | analista_finanzas_pyme, auditor_operacion_diaria, controlador_gastos_pyme, coordinador_abastecimiento, coordinador_operaciones_portuarias, detector_fugas_rentabilidad, gestor_stock_inventario, optimizador_logistica_entregas, organizador_procesos_pyme, planificador_compras_proveedores |
| administracion_contabilidad_finanzas | Administración, Contabilidad y Finanzas | 35 | analista_contratos_operativos, analista_costos_local, analista_datos_negocio, analista_finanzas_pyme, analista_flujo_caja, analista_precios_margenes, analista_rentabilidad_margen, arquitecto_automatizaciones, asesor_emprendedor_generalista, auditor_facturacion_cobros, constructor_automatizaciones_no_code, consultor_modelo_negocio, consultor_operaciones_salud_farmacia, controlador_gastos_pyme, controlador_presupuesto, coordinador_abastecimiento, coordinador_proyectos_construccion, detector_fugas_rentabilidad, director_operativo_digital, disenador_workflows_automatizados, especialista_bi_dashboards, especialista_comercio_exterior_aduana, especialista_continuidad_operativa, especialista_promociones_locales, especialista_reporting_operativo, evaluador_herramientas_software, gestor_caja_diaria, gestor_compliance_pyme, gestor_documentacion_administrativa, modelador_metricas_kpis, organizador_procesos_pyme, planificador_compras_proveedores, planificador_financiero_operativo, priorizador_tareas_dueno_negocio, simulador_escenarios_negocio |
| aduana_comercio_exterior | Aduana y Comercio Exterior | 2 | coordinador_operaciones_portuarias, especialista_comercio_exterior_aduana |
| atencion_cliente_call_center_telemarketing | Atención al Cliente, Call Center y Telemarketing | 12 | analista_satisfaccion_cliente, auditor_calidad_atencion, auditor_facturacion_cobros, coordinador_soporte_multicanal, copywriter_conversion, disenador_base_respuestas_cliente, especialista_customer_success, especialista_ventas_consultivas, gestor_consultas_clientes, gestor_reclamos_postventa, operador_ventas_whatsapp, responsable_experiencia_cliente_local |
| automatizacion_integraciones | Automatización e Integraciones | 22 | administrador_sistemas_internos, analista_calidad_datos, analista_riesgo_tecnico_operativo, arquitecto_automatizaciones, arquitecto_crm_operativo, arquitecto_datos_negocio, auditor_automatizaciones, auditor_calidad_operativa, auditor_errores_sistemas, auditor_procesos_negocio, constructor_automatizaciones_no_code, coordinador_canal_whatsapp, coordinador_operaciones_digitales, coordinador_soporte_multicanal, director_operativo_digital, disenador_workflows_automatizados, documentador_flujos_sistemas, especialista_crm_whatsapp, especialista_integraciones_api, especialista_monitoreo_alertas, evaluador_herramientas_software, integrador_herramientas_digitales |
| comercial_ventas_negocios | Comercial, Ventas y Negocios | 36 | analista_costos_local, analista_datos_negocio, analista_finanzas_pyme, analista_oportunidades_locales, analista_precios_margenes, analista_rentabilidad_margen, analista_segmentacion_clientes, arquitecto_crm_operativo, asesor_emprendedor_generalista, constructor_automatizaciones_no_code, consultor_modelo_negocio, coordinador_canal_whatsapp, copywriter_conversion, creador_contenido_negocio_local, detector_fugas_rentabilidad, disenador_pipeline_comercial, especialista_crm_whatsapp, especialista_customer_success, especialista_performance_marketing, especialista_promociones_locales, especialista_ventas_consultivas, estratega_contenidos, estratega_growth, estratega_negocio_digital, estratega_propuesta_valor, fidelizador_clientes_recurrentes, gestor_caja_diaria, gestor_calendario_comercial, gestor_marketing_barrial, gestor_reclamos_postventa, gestor_stock_inventario, operador_ventas_whatsapp, optimizador_logistica_entregas, priorizador_tareas_dueno_negocio, responsable_experiencia_cliente_local, revenue_operations_manager |
| comunicacion_relaciones_institucionales_publicas | Comunicación, Relaciones Institucionales y Públicas | 14 | analista_roles_responsabilidades, creador_contenido_negocio_local, disenador_base_respuestas_cliente, disenador_onboarding_empleados, documentador_cultura_procesos, documentador_flujos_sistemas, especialista_base_conocimiento, estratega_contenidos, gestor_calendario_comercial, gestor_documentacion_administrativa, gestor_marketing_barrial, historiador_contexto_negocio, integrador_sintesis_decisiones, redactor_politicas_internas |
| customer_success_experiencia_cliente | Customer Success y Experiencia de Cliente | 29 | analista_satisfaccion_cliente, analista_segmentacion_clientes, arquitecto_crm_operativo, auditor_calidad_atencion, auditor_calidad_operativa, auditor_facturacion_cobros, auditor_operacion_diaria, consultor_operaciones_salud_farmacia, coordinador_canal_whatsapp, coordinador_operaciones_digitales, coordinador_soporte_multicanal, coordinador_soporte_tecnico, director_operativo_digital, disenador_base_respuestas_cliente, disenador_pipeline_comercial, especialista_base_conocimiento, especialista_bi_dashboards, especialista_crm_whatsapp, especialista_customer_success, estratega_growth, fidelizador_clientes_recurrentes, gestor_consultas_clientes, gestor_reclamos_postventa, integrador_herramientas_digitales, investigador_usuarios, optimizador_logistica_entregas, product_manager_digital, responsable_experiencia_cliente_local, revenue_operations_manager |
| datos_bi_analytics | Datos, BI y Analytics | 35 | analista_calidad_datos, analista_datos_negocio, analista_experimentos_ab_testing, analista_finanzas_pyme, analista_flujo_caja, analista_precios_margenes, analista_rentabilidad_margen, analista_satisfaccion_cliente, analista_segmentacion_clientes, analista_sesgos_decision, arquitecto_crm_operativo, arquitecto_datos_negocio, auditor_calidad_atencion, auditor_calidad_operativa, auditor_dashboards_metricas, auditor_privacidad_datos, controlador_presupuesto, detector_fugas_rentabilidad, disenador_pipeline_comercial, especialista_bi_dashboards, especialista_customer_success, especialista_integraciones_api, especialista_monitoreo_alertas, especialista_performance_marketing, especialista_reporting_operativo, estratega_growth, gestor_evaluacion_desempeno, integrador_herramientas_digitales, integrador_sintesis_decisiones, minimalista_senal_ruido, modelador_metricas_kpis, planificador_financiero_operativo, priorizador_roadmap, revenue_operations_manager, simulador_escenarios_negocio |
| departamento_tecnico | Departamento Técnico | 6 | auditor_errores_sistemas, coordinador_soporte_tecnico, documentador_procedimientos_operativos, especialista_base_conocimiento, especialista_entornos_despliegue, tester_funcional_negocio |
| diseno | Diseño | 4 | creador_contenido_negocio_local, estratega_contenidos, investigador_usuarios, product_manager_digital |
| educacion_docencia_investigacion | Educación, Docencia e Investigación | 6 | capacitador_operativo_interno, disenador_onboarding_empleados, documentador_cultura_procesos, documentador_flujos_sistemas, especialista_base_conocimiento, historiador_contexto_negocio |
| enfermeria | Enfermería | 1 | supervisor_turnos_y_tareas |
| gastronomia_turismo | Gastronomía y Turismo | 7 | analista_costos_local, auditor_operacion_diaria, coordinador_operacion_local, gestor_caja_diaria, gestor_stock_inventario, responsable_experiencia_cliente_local, supervisor_turnos_y_tareas |
| gerencia_direccion_general | Gerencia y Dirección General | 39 | administrador_sistemas_internos, analista_contratos_operativos, analista_flujo_caja, analista_operaciones_mineria_energia, analista_oportunidades_locales, analista_riesgo_legal_preventivo, analista_riesgo_tecnico_operativo, analista_roles_responsabilidades, analista_sesgos_decision, arquitecto_datos_negocio, asesor_emprendedor_generalista, auditor_automatizaciones, auditor_dashboards_metricas, auditor_procesos_negocio, consultor_modelo_negocio, controlador_gastos_pyme, controlador_presupuesto, coordinador_operacion_local, coordinador_operaciones_digitales, coordinador_proyectos_construccion, director_operativo_digital, disenador_workflows_automatizados, especialista_bi_dashboards, especialista_continuidad_operativa, especialista_reporting_operativo, estratega_negocio_digital, estratega_propuesta_valor, evaluador_herramientas_software, gestor_compliance_pyme, gestor_evaluacion_desempeno, historiador_contexto_negocio, integrador_sintesis_decisiones, minimalista_senal_ruido, modelador_metricas_kpis, organizador_procesos_pyme, planificador_financiero_operativo, priorizador_roadmap, priorizador_tareas_dueno_negocio, simulador_escenarios_negocio |
| ingenieria_civil_construccion | Ingeniería Civil y Construcción | 1 | coordinador_proyectos_construccion |
| ingenierias | Ingenierías | 1 | analista_ingenieria_operativa |
| legales | Legales | 8 | analista_contratos_operativos, analista_riesgo_legal_preventivo, auditor_privacidad_datos, controlador_cumplimiento_sops, especialista_comercio_exterior_aduana, gestor_compliance_pyme, gestor_documentacion_administrativa, redactor_politicas_internas |
| marketing_publicidad | Marketing y Publicidad | 25 | analista_datos_negocio, analista_experimentos_ab_testing, analista_oportunidades_locales, analista_rentabilidad_margen, analista_segmentacion_clientes, asesor_emprendedor_generalista, coordinador_canal_whatsapp, copywriter_conversion, creador_contenido_negocio_local, disenador_pipeline_comercial, especialista_crm_whatsapp, especialista_performance_marketing, especialista_promociones_locales, especialista_ventas_consultivas, estratega_contenidos, estratega_growth, estratega_negocio_digital, estratega_propuesta_valor, fidelizador_clientes_recurrentes, gestor_calendario_comercial, gestor_marketing_barrial, investigador_usuarios, minimalista_senal_ruido, operador_ventas_whatsapp, revenue_operations_manager |
| mineria_petroleo_gas | Minería, Petróleo y Gas | 1 | analista_operaciones_mineria_energia |
| naviero_maritimo_portuario | Naviero, Marítimo, Portuario | 1 | coordinador_operaciones_portuarias |
| oficios_otros | Oficios y Otros | 1 | coordinador_operacion_local |
| produccion_manufactura | Producción y Manufactura | 14 | analista_costos_local, analista_ingenieria_operativa, analista_operaciones_mineria_energia, arquitecto_automatizaciones, auditor_calidad_operativa, auditor_operacion_diaria, auditor_procesos_negocio, capacitador_operativo_interno, controlador_cumplimiento_sops, coordinador_abastecimiento, documentador_procedimientos_operativos, gestor_stock_inventario, organizador_procesos_pyme, planificador_compras_proveedores |
| producto_gestion_producto | Producto y Gestión de Producto | 11 | analista_experimentos_ab_testing, analista_sesgos_decision, consultor_modelo_negocio, copywriter_conversion, especialista_entornos_despliegue, estratega_negocio_digital, estratega_propuesta_valor, investigador_usuarios, priorizador_roadmap, product_manager_digital, tester_funcional_negocio |
| recursos_humanos_capacitacion | Recursos Humanos y Capacitación | 9 | analista_roles_responsabilidades, capacitador_operativo_interno, controlador_cumplimiento_sops, disenador_onboarding_empleados, documentador_cultura_procesos, documentador_procedimientos_operativos, gestor_evaluacion_desempeno, redactor_politicas_internas, supervisor_turnos_y_tareas |
| salud_medicina_farmacia | Salud, Medicina y Farmacia | 1 | consultor_operaciones_salud_farmacia |
| secretarias_recepcion | Secretarias y Recepción | 7 | coordinador_operacion_local, coordinador_operaciones_digitales, documentador_procedimientos_operativos, gestor_calendario_comercial, gestor_consultas_clientes, priorizador_tareas_dueno_negocio, supervisor_turnos_y_tareas |
| seguros | Seguros | 2 | analista_riesgo_legal_preventivo, especialista_continuidad_operativa |
| sociologia_trabajo_social | Sociología / Trabajo Social | 1 | analista_oportunidades_locales |
| tecnologia_sistemas_telecomunicaciones | Tecnología, Sistemas y Telecomunicaciones | 19 | administrador_sistemas_internos, analista_calidad_datos, analista_ingenieria_operativa, analista_riesgo_tecnico_operativo, arquitecto_automatizaciones, auditor_automatizaciones, auditor_dashboards_metricas, auditor_errores_sistemas, auditor_privacidad_datos, coordinador_soporte_tecnico, especialista_continuidad_operativa, especialista_entornos_despliegue, especialista_integraciones_api, especialista_monitoreo_alertas, evaluador_herramientas_software, integrador_herramientas_digitales, priorizador_roadmap, product_manager_digital, tester_funcional_negocio |

## Area -> Nichos Cubiertos

| area_id | area | nichos_cubiertos | nichos_totales | niche_ids_cubiertos |
| --- | --- | --- | --- | --- |
| abastecimiento_logistica | Abastecimiento y Logística | 5 | 5 | compras_proveedores, distribucion_transporte, gestion_inventarios, planificacion_compras, seguimiento_proveedores |
| administracion_contabilidad_finanzas | Administración, Contabilidad y Finanzas | 13 | 13 | contabilidad_general, control_deuda_pagos, control_gastos, control_gestion, flujo_caja_pyme, flujo_caja_semanal, impuestos_auditoria, planeamiento_financiero, presupuesto_por_area, punto_equilibrio, rentabilidad_producto, rentabilidad_unidad_negocio, tesoreria_cashflow |
| aduana_comercio_exterior | Aduana y Comercio Exterior | 5 | 5 | clasificacion_arancelaria, compliance_comercio_exterior, costos_importacion_exportacion, documentacion_import_export, seguimiento_embarques |
| atencion_cliente_call_center_telemarketing | Atención al Cliente, Call Center y Telemarketing | 6 | 6 | experiencia_cliente, mesa_ayuda, protocolos_respuesta_cliente, reclamos_postventa, soporte_cliente, ventas_telefonicas |
| automatizacion_integraciones | Automatización e Integraciones | 9 | 9 | aprobaciones_internas, arquitectura_sistemas_internos, automatizacion_procesos_internos, automatizacion_reportes_recurrentes, automatizacion_tareas_administrativas, automatizacion_whatsapp_crm, flujos_no_code_low_code, gestion_apis, integraciones_herramientas |
| comercial_ventas_negocios | Comercial, Ventas y Negocios | 12 | 12 | crm_comercial, diseno_pipeline_comercial, ecommerce_y_marketplaces, estrategia_comercial, gestion_cuentas_clave, procesos_venta_pymes, prospeccion_b2b, revenue_operations, scripts_objeciones_comerciales, seguimiento_oportunidades_comerciales, ventas_consultivas, ventas_retail |
| comunicacion_relaciones_institucionales_publicas | Comunicación, Relaciones Institucionales y Públicas | 2 | 5 | comunicacion_institucional, comunicacion_interna |
| customer_success_experiencia_cliente | Customer Success y Experiencia de Cliente | 9 | 9 | experiencia_cliente_omnicanal, experiencia_postventa, gestion_churn, medicion_satisfaccion_cliente, onboarding_clientes, programas_fidelizacion, recuperacion_clientes_inactivos, retencion_fidelizacion_clientes, voz_cliente_nps |
| datos_bi_analytics | Datos, BI y Analytics | 9 | 9 | analisis_clientes_recurrentes, analisis_cohortes, auditoria_datos, dashboards_operativos, indicadores_negocio, inteligencia_comercial, rentabilidad_por_canal, segmentacion_comercial_avanzada, tableros_margen_costos |
| departamento_tecnico | Departamento Técnico | 4 | 5 | base_conocimiento_tecnica, diagnostico_fallas, documentacion_tecnica, soporte_tecnico_producto |
| diseno | Diseño | 2 | 5 | investigacion_visual_usuarios, ux_ui |
| educacion_docencia_investigacion | Educación, Docencia e Investigación | 3 | 6 | capacitacion_corporativa, evaluacion_aprendizaje, investigacion_academica |
| enfermeria | Enfermería | 1 | 5 | coordinacion_turnos_enfermeria |
| gastronomia_turismo | Gastronomía y Turismo | 4 | 5 | cocina_costos_menu, gestion_restaurantes, hoteleria_experiencia_huesped, reservas_operaciones |
| gerencia_direccion_general | Gerencia y Dirección General | 9 | 9 | analisis_competidores, gestion_riesgos_proyecto, modelos_negocio, objetivos_metricas_okrs, planificacion_estrategica, planificacion_proyectos_internos, seguimiento_entregables, tablero_direccion, transformacion_organizacional |
| ingenieria_civil_construccion | Ingeniería Civil y Construcción | 5 | 5 | control_costos_obra, direccion_obra, presupuestos_computos, seguimiento_avance_obra, seguridad_higiene_obra |
| ingenierias | Ingenierías | 5 | 5 | gestion_cambios_ingenieria, gestion_proyectos_ingenieria, ingenieria_calidad, ingenieria_procesos, validacion_requerimientos_tecnicos |
| legales | Legales | 7 | 9 | analisis_contratos, checklist_documental_basico, compliance_normativo, contratos_simples_pymes, derecho_laboral, politicas_internas_basicas, proteccion_datos_basica |
| marketing_publicidad | Marketing y Publicidad | 13 | 13 | analisis_rendimiento_campanas, calendario_comercial, campanas_comercios_locales, contenidos_redes, crecimiento_instagram_tiktok, crecimiento_whatsapp, crm_fidelizacion, embudos_conversion, estrategia_contenidos, estrategia_marca, growth_marketing, investigacion_mercado, performance_ads |
| mineria_petroleo_gas | Minería, Petróleo y Gas | 5 | 5 | control_produccion_minera_energia, mantenimiento_equipos_pesados, operaciones_mineras, permisos_reportes_ambientales, seguridad_ambiental |
| naviero_maritimo_portuario | Naviero, Marítimo, Portuario | 5 | 5 | control_documental_portuario, coordinacion_operaciones_embarque, documentacion_maritima, logistica_naviera, operaciones_portuarias |
| oficios_otros | Oficios y Otros | 1 | 4 | gestion_servicios_oficios |
| produccion_manufactura | Producción y Manufactura | 4 | 5 | control_calidad, estandarizacion_procedimientos, mejora_continua_procesos, planificacion_produccion |
| producto_gestion_producto | Producto y Gestión de Producto | 5 | 5 | gestion_producto_digital, pricing_packaging, priorizacion_roadmap, research_usuarios, validacion_ideas_negocio |
| recursos_humanos_capacitacion | Recursos Humanos y Capacitación | 5 | 7 | capacitacion_desarrollo, clima_cultura, diseno_roles_internos, evaluacion_desempeno, onboarding_empleados |
| salud_medicina_farmacia | Salud, Medicina y Farmacia | 5 | 5 | agenda_consultorios_salud, auditoria_medica, farmacia_clinica, gestion_consultorios, seguimiento_pacientes_cronicos |
| secretarias_recepcion | Secretarias y Recepción | 5 | 5 | agenda_coordinacion, coordinacion_reuniones_eventos, gestion_documental, recepcion_atencion, seguimiento_tramites |
| seguros | Seguros | 1 | 5 | suscripcion_riesgos |
| sociologia_trabajo_social | Sociología / Trabajo Social | 1 | 5 | diagnostico_social |
| tecnologia_sistemas_telecomunicaciones | Tecnología, Sistemas y Telecomunicaciones | 6 | 9 | calidad_software_qa, desarrollo_software, devops_basico_pymes, seguridad_operativa_basica, soporte_it, soporte_tecnico_operativo |

## Nicho -> Perfiles Compatibles

| niche_id | nicho | area_id | perfiles | profile_ids |
| --- | --- | --- | --- | --- |
| agenda_consultorios_salud | Agenda de consultorios de salud | salud_medicina_farmacia | 1 | consultor_operaciones_salud_farmacia |
| agenda_coordinacion | Agenda y coordinación | secretarias_recepcion | 4 | coordinador_operacion_local, coordinador_operaciones_digitales, priorizador_tareas_dueno_negocio, supervisor_turnos_y_tareas |
| analisis_cartera_seguros | Análisis de cartera de seguros | seguros | 0 | - |
| analisis_clientes_recurrentes | Análisis de clientes recurrentes | datos_bi_analytics | 2 | analista_satisfaccion_cliente, analista_segmentacion_clientes |
| analisis_cohortes | Análisis de cohortes | datos_bi_analytics | 1 | analista_experimentos_ab_testing |
| analisis_competidores | Análisis de competidores | gerencia_direccion_general | 2 | analista_sesgos_decision, historiador_contexto_negocio |
| analisis_contratos | Análisis de contratos | legales | 1 | analista_contratos_operativos |
| analisis_loteria_juegos_azar | Análisis de Lotería y Juegos de Azar | oficios_otros | 0 | - |
| analisis_rendimiento_campanas | Análisis de rendimiento de campañas | marketing_publicidad | 7 | analista_datos_negocio, analista_experimentos_ab_testing, analista_rentabilidad_margen, detector_fugas_rentabilidad, especialista_performance_marketing, estratega_growth, minimalista_senal_ruido |
| aprobaciones_internas | Aprobaciones internas | automatizacion_integraciones | 2 | controlador_cumplimiento_sops, disenador_workflows_automatizados |
| arquitectura_sistemas_internos | Arquitectura de sistemas internos | automatizacion_integraciones | 8 | administrador_sistemas_internos, analista_riesgo_tecnico_operativo, arquitecto_automatizaciones, arquitecto_datos_negocio, auditor_privacidad_datos, documentador_flujos_sistemas, especialista_integraciones_api, evaluador_herramientas_software |
| asuntos_publicos | Asuntos públicos | comunicacion_relaciones_institucionales_publicas | 0 | - |
| atencion_productores | Atención a productores | seguros | 0 | - |
| auditoria_datos | Auditoría de datos | datos_bi_analytics | 9 | analista_calidad_datos, analista_datos_negocio, analista_sesgos_decision, arquitecto_datos_negocio, auditor_calidad_atencion, auditor_calidad_operativa, auditor_dashboards_metricas, auditor_privacidad_datos, especialista_integraciones_api |
| auditoria_medica | Auditoría médica | salud_medicina_farmacia | 1 | consultor_operaciones_salud_farmacia |
| automatizacion_procesos_internos | Automatización de procesos internos | automatizacion_integraciones | 6 | arquitecto_automatizaciones, auditor_automatizaciones, auditor_procesos_negocio, coordinador_operaciones_digitales, director_operativo_digital, disenador_workflows_automatizados |
| automatizacion_reportes_recurrentes | Automatización de reportes recurrentes | automatizacion_integraciones | 2 | especialista_monitoreo_alertas, especialista_reporting_operativo |
| automatizacion_tareas_administrativas | Automatización de tareas administrativas | automatizacion_integraciones | 2 | constructor_automatizaciones_no_code, disenador_workflows_automatizados |
| automatizacion_whatsapp_crm | Automatización de WhatsApp y CRM | automatizacion_integraciones | 6 | arquitecto_crm_operativo, constructor_automatizaciones_no_code, coordinador_canal_whatsapp, coordinador_soporte_multicanal, especialista_crm_whatsapp, integrador_herramientas_digitales |
| base_conocimiento_tecnica | Base de conocimiento técnica | departamento_tecnico | 3 | coordinador_soporte_tecnico, documentador_procedimientos_operativos, especialista_base_conocimiento |
| calendario_comercial | Calendario comercial | marketing_publicidad | 5 | asesor_emprendedor_generalista, especialista_promociones_locales, estratega_contenidos, gestor_calendario_comercial, gestor_marketing_barrial |
| calidad_software_qa | Calidad de software y QA | tecnologia_sistemas_telecomunicaciones | 5 | analista_calidad_datos, auditor_automatizaciones, auditor_errores_sistemas, especialista_entornos_despliegue, tester_funcional_negocio |
| campanas_comercios_locales | Campañas para comercios locales | marketing_publicidad | 5 | analista_oportunidades_locales, creador_contenido_negocio_local, especialista_promociones_locales, gestor_calendario_comercial, gestor_marketing_barrial |
| capacitacion_corporativa | Capacitación corporativa | educacion_docencia_investigacion | 5 | capacitador_operativo_interno, disenador_onboarding_empleados, documentador_cultura_procesos, documentador_flujos_sistemas, especialista_base_conocimiento |
| capacitacion_desarrollo | Capacitación y desarrollo | recursos_humanos_capacitacion | 4 | capacitador_operativo_interno, controlador_cumplimiento_sops, disenador_onboarding_empleados, redactor_politicas_internas |
| checklist_documental_basico | Checklist documental básico | legales | 5 | analista_contratos_operativos, auditor_privacidad_datos, gestor_compliance_pyme, gestor_documentacion_administrativa, redactor_politicas_internas |
| ciberseguridad | Ciberseguridad | tecnologia_sistemas_telecomunicaciones | 0 | - |
| clasificacion_arancelaria | Clasificación arancelaria | aduana_comercio_exterior | 1 | especialista_comercio_exterior_aduana |
| clima_cultura | Clima y cultura | recursos_humanos_capacitacion | 4 | analista_roles_responsabilidades, documentador_cultura_procesos, gestor_evaluacion_desempeno, redactor_politicas_internas |
| cocina_costos_menu | Cocina, costos y menú | gastronomia_turismo | 2 | analista_costos_local, gestor_stock_inventario |
| compliance_comercio_exterior | Compliance de comercio exterior | aduana_comercio_exterior | 1 | especialista_comercio_exterior_aduana |
| compliance_normativo | Compliance normativo | legales | 2 | analista_riesgo_legal_preventivo, gestor_compliance_pyme |
| compras_proveedores | Compras y proveedores | abastecimiento_logistica | 4 | analista_finanzas_pyme, controlador_gastos_pyme, coordinador_abastecimiento, planificador_compras_proveedores |
| comunicacion_institucional | Comunicación institucional | comunicacion_relaciones_institucionales_publicas | 1 | estratega_contenidos |
| comunicacion_interna | Comunicación interna | comunicacion_relaciones_institucionales_publicas | 10 | analista_roles_responsabilidades, disenador_base_respuestas_cliente, disenador_onboarding_empleados, documentador_cultura_procesos, documentador_flujos_sistemas, especialista_base_conocimiento, gestor_documentacion_administrativa, historiador_contexto_negocio, integrador_sintesis_decisiones, redactor_politicas_internas |
| contabilidad_general | Contabilidad general | administracion_contabilidad_finanzas | 2 | auditor_facturacion_cobros, gestor_documentacion_administrativa |
| contenidos_redes | Contenidos y redes sociales | marketing_publicidad | 4 | copywriter_conversion, creador_contenido_negocio_local, estratega_contenidos, gestor_calendario_comercial |
| contratos_simples_pymes | Contratos simples para pymes | legales | 1 | analista_contratos_operativos |
| control_calidad | Control de calidad | produccion_manufactura | 3 | auditor_calidad_operativa, auditor_operacion_diaria, controlador_cumplimiento_sops |
| control_costos_obra | Control de costos de obra | ingenieria_civil_construccion | 1 | coordinador_proyectos_construccion |
| control_deuda_pagos | Control de deuda y pagos | administracion_contabilidad_finanzas | 3 | analista_flujo_caja, auditor_facturacion_cobros, controlador_gastos_pyme |
| control_documental_portuario | Control documental portuario | naviero_maritimo_portuario | 1 | coordinador_operaciones_portuarias |
| control_gastos | Control de gastos | administracion_contabilidad_finanzas | 7 | analista_costos_local, constructor_automatizaciones_no_code, controlador_gastos_pyme, controlador_presupuesto, detector_fugas_rentabilidad, evaluador_herramientas_software, planificador_compras_proveedores |
| control_gestion | Control de gestión | administracion_contabilidad_finanzas | 13 | analista_calidad_datos, analista_datos_negocio, analista_finanzas_pyme, analista_rentabilidad_margen, auditor_procesos_negocio, controlador_gastos_pyme, controlador_presupuesto, especialista_bi_dashboards, especialista_reporting_operativo, integrador_sintesis_decisiones, modelador_metricas_kpis, organizador_procesos_pyme, priorizador_tareas_dueno_negocio |
| control_produccion_minera_energia | Control de producción minera y energética | mineria_petroleo_gas | 1 | analista_operaciones_mineria_energia |
| coordinacion_operaciones_embarque | Coordinación de operaciones de embarque | naviero_maritimo_portuario | 1 | coordinador_operaciones_portuarias |
| coordinacion_reuniones_eventos | Coordinación de reuniones y eventos | secretarias_recepcion | 2 | director_operativo_digital, gestor_calendario_comercial |
| coordinacion_turnos_enfermeria | Coordinación de turnos de enfermería | enfermeria | 1 | supervisor_turnos_y_tareas |
| costos_importacion_exportacion | Costos de importación y exportación | aduana_comercio_exterior | 1 | especialista_comercio_exterior_aduana |
| crecimiento_instagram_tiktok | Crecimiento en Instagram y TikTok | marketing_publicidad | 3 | creador_contenido_negocio_local, especialista_promociones_locales, gestor_marketing_barrial |
| crecimiento_whatsapp | Crecimiento por WhatsApp | marketing_publicidad | 3 | coordinador_canal_whatsapp, especialista_crm_whatsapp, operador_ventas_whatsapp |
| crm_comercial | CRM comercial | comercial_ventas_negocios | 6 | arquitecto_crm_operativo, constructor_automatizaciones_no_code, disenador_pipeline_comercial, especialista_crm_whatsapp, integrador_herramientas_digitales, revenue_operations_manager |
| crm_fidelizacion | CRM y fidelización | marketing_publicidad | 6 | analista_segmentacion_clientes, coordinador_canal_whatsapp, especialista_crm_whatsapp, estratega_growth, fidelizador_clientes_recurrentes, revenue_operations_manager |
| cuidados_clinicos | Cuidados clínicos | enfermeria | 0 | - |
| dashboards_operativos | Dashboards operativos | datos_bi_analytics | 8 | arquitecto_datos_negocio, auditor_dashboards_metricas, coordinador_operaciones_digitales, especialista_bi_dashboards, especialista_monitoreo_alertas, especialista_reporting_operativo, integrador_herramientas_digitales, minimalista_senal_ruido |
| datos_bi | Datos y BI | tecnologia_sistemas_telecomunicaciones | 0 | - |
| derecho_laboral | Derecho laboral | legales | 1 | analista_riesgo_legal_preventivo |
| desarrollo_software | Desarrollo de software | tecnologia_sistemas_telecomunicaciones | 2 | especialista_entornos_despliegue, especialista_integraciones_api |
| devops_basico_pymes | DevOps básico para pymes | tecnologia_sistemas_telecomunicaciones | 5 | analista_riesgo_tecnico_operativo, auditor_errores_sistemas, especialista_continuidad_operativa, especialista_entornos_despliegue, especialista_monitoreo_alertas |
| diagnostico_fallas | Diagnóstico de fallas | departamento_tecnico | 3 | auditor_errores_sistemas, coordinador_soporte_tecnico, tester_funcional_negocio |
| diagnostico_social | Diagnóstico social | sociologia_trabajo_social | 1 | analista_oportunidades_locales |
| direccion_obra | Dirección de obra | ingenieria_civil_construccion | 1 | coordinador_proyectos_construccion |
| diseno_curricular | Diseño curricular | educacion_docencia_investigacion | 0 | - |
| diseno_grafico_marca | Diseño gráfico y marca | diseno | 0 | - |
| diseno_pipeline_comercial | Diseño de pipeline comercial | comercial_ventas_negocios | 1 | disenador_pipeline_comercial |
| diseno_producto | Diseño de producto | diseno | 0 | - |
| diseno_roles_internos | Diseño de roles internos | recursos_humanos_capacitacion | 3 | analista_roles_responsabilidades, disenador_onboarding_empleados, supervisor_turnos_y_tareas |
| distribucion_transporte | Distribución y transporte | abastecimiento_logistica | 1 | optimizador_logistica_entregas |
| documentacion_import_export | Documentación import/export | aduana_comercio_exterior | 1 | especialista_comercio_exterior_aduana |
| documentacion_maritima | Documentación marítima | naviero_maritimo_portuario | 1 | coordinador_operaciones_portuarias |
| documentacion_tecnica | Documentación técnica | departamento_tecnico | 3 | documentador_flujos_sistemas, documentador_procedimientos_operativos, especialista_entornos_despliegue |
| ecommerce_y_marketplaces | E-commerce y marketplaces | comercial_ventas_negocios | 1 | especialista_performance_marketing |
| educacion_paciente | Educación del paciente | enfermeria | 0 | - |
| embudos_conversion | Embudos de conversión | marketing_publicidad | 4 | analista_experimentos_ab_testing, copywriter_conversion, especialista_performance_marketing, estratega_growth |
| estandarizacion_procedimientos | Estandarización de procedimientos | produccion_manufactura | 7 | auditor_calidad_operativa, auditor_operacion_diaria, auditor_procesos_negocio, capacitador_operativo_interno, controlador_cumplimiento_sops, documentador_procedimientos_operativos, organizador_procesos_pyme |
| estrategia_comercial | Estrategia comercial | comercial_ventas_negocios | 4 | consultor_modelo_negocio, especialista_ventas_consultivas, estratega_negocio_digital, estratega_propuesta_valor |
| estrategia_contenidos | Estrategia de contenidos | marketing_publicidad | 2 | creador_contenido_negocio_local, estratega_contenidos |
| estrategia_marca | Estrategia de marca | marketing_publicidad | 5 | copywriter_conversion, creador_contenido_negocio_local, estratega_contenidos, estratega_propuesta_valor, gestor_marketing_barrial |
| evaluacion_aprendizaje | Evaluación de aprendizaje | educacion_docencia_investigacion | 2 | capacitador_operativo_interno, gestor_evaluacion_desempeno |
| evaluacion_desempeno | Evaluación de desempeño | recursos_humanos_capacitacion | 2 | gestor_evaluacion_desempeno, supervisor_turnos_y_tareas |
| evaluacion_impacto_social | Evaluación de impacto social | sociologia_trabajo_social | 0 | - |
| experiencia_cliente | Experiencia del cliente | atencion_cliente_call_center_telemarketing | 4 | analista_satisfaccion_cliente, disenador_base_respuestas_cliente, gestor_consultas_clientes, responsable_experiencia_cliente_local |
| experiencia_cliente_omnicanal | Experiencia de cliente omnicanal | customer_success_experiencia_cliente | 4 | coordinador_soporte_multicanal, disenador_base_respuestas_cliente, investigador_usuarios, responsable_experiencia_cliente_local |
| experiencia_postventa | Experiencia postventa | customer_success_experiencia_cliente | 8 | auditor_calidad_operativa, auditor_facturacion_cobros, auditor_operacion_diaria, coordinador_soporte_multicanal, coordinador_soporte_tecnico, especialista_base_conocimiento, gestor_reclamos_postventa, optimizador_logistica_entregas |
| farmacia_clinica | Farmacia clínica | salud_medicina_farmacia | 1 | consultor_operaciones_salud_farmacia |
| flujo_caja_pyme | Flujo de caja para pymes | administracion_contabilidad_finanzas | 6 | analista_flujo_caja, asesor_emprendedor_generalista, especialista_continuidad_operativa, gestor_caja_diaria, planificador_financiero_operativo, simulador_escenarios_negocio |
| flujo_caja_semanal | Flujo de caja semanal | administracion_contabilidad_finanzas | 4 | analista_flujo_caja, especialista_reporting_operativo, gestor_caja_diaria, priorizador_tareas_dueno_negocio |
| flujos_no_code_low_code | Flujos no-code y low-code | automatizacion_integraciones | 1 | constructor_automatizaciones_no_code |
| gestion_apis | Gestión de APIs | automatizacion_integraciones | 4 | arquitecto_automatizaciones, especialista_integraciones_api, evaluador_herramientas_software, integrador_herramientas_digitales |
| gestion_beneficios_compensaciones | Gestión de beneficios y compensaciones | recursos_humanos_capacitacion | 0 | - |
| gestion_cambios_ingenieria | Gestión de cambios de ingeniería | ingenierias | 1 | analista_ingenieria_operativa |
| gestion_casos_sociales | Gestión de casos sociales | sociologia_trabajo_social | 0 | - |
| gestion_churn | Gestión de churn | customer_success_experiencia_cliente | 4 | especialista_customer_success, estratega_growth, gestor_reclamos_postventa, revenue_operations_manager |
| gestion_consultorios | Gestión de consultorios | salud_medicina_farmacia | 1 | consultor_operaciones_salud_farmacia |
| gestion_crisis_comunicacional | Gestión de crisis comunicacional | comunicacion_relaciones_institucionales_publicas | 0 | - |
| gestion_cuentas_clave | Gestión de cuentas clave | comercial_ventas_negocios | 2 | disenador_pipeline_comercial, especialista_ventas_consultivas |
| gestion_documental | Gestión documental | secretarias_recepcion | 1 | documentador_procedimientos_operativos |
| gestion_garantias_tecnicas | Gestión de garantías técnicas | departamento_tecnico | 0 | - |
| gestion_instituciones_educativas | Gestión de instituciones educativas | educacion_docencia_investigacion | 0 | - |
| gestion_inventarios | Gestión de inventarios | abastecimiento_logistica | 6 | auditor_operacion_diaria, coordinador_abastecimiento, detector_fugas_rentabilidad, gestor_stock_inventario, optimizador_logistica_entregas, planificador_compras_proveedores |
| gestion_producto_digital | Gestión de producto digital | producto_gestion_producto | 4 | especialista_entornos_despliegue, priorizador_roadmap, product_manager_digital, tester_funcional_negocio |
| gestion_proyectos_ingenieria | Gestión de proyectos de ingeniería | ingenierias | 1 | analista_ingenieria_operativa |
| gestion_restaurantes | Gestión de restaurantes | gastronomia_turismo | 3 | auditor_operacion_diaria, coordinador_operacion_local, gestor_caja_diaria |
| gestion_riesgos_proyecto | Gestión de riesgos de proyecto | gerencia_direccion_general | 7 | analista_riesgo_legal_preventivo, analista_riesgo_tecnico_operativo, auditor_automatizaciones, especialista_continuidad_operativa, especialista_monitoreo_alertas, gestor_compliance_pyme, simulador_escenarios_negocio |
| gestion_servicios_oficios | Gestión de servicios y oficios | oficios_otros | 1 | coordinador_operacion_local |
| gestion_siniestros | Gestión de siniestros | seguros | 0 | - |
| growth_marketing | Growth marketing | marketing_publicidad | 2 | analista_experimentos_ab_testing, estratega_growth |
| hoteleria_experiencia_huesped | Hotelería y experiencia del huésped | gastronomia_turismo | 1 | responsable_experiencia_cliente_local |
| impuestos_auditoria | Impuestos y auditoría | administracion_contabilidad_finanzas | 2 | gestor_compliance_pyme, gestor_documentacion_administrativa |
| indicadores_negocio | Indicadores de negocio | datos_bi_analytics | 13 | analista_calidad_datos, analista_datos_negocio, analista_flujo_caja, arquitecto_datos_negocio, auditor_dashboards_metricas, especialista_bi_dashboards, gestor_evaluacion_desempeno, minimalista_senal_ruido, modelador_metricas_kpis, planificador_financiero_operativo, priorizador_roadmap, revenue_operations_manager, simulador_escenarios_negocio |
| ingenieria_calidad | Ingeniería de calidad | ingenierias | 1 | analista_ingenieria_operativa |
| ingenieria_procesos | Ingeniería de procesos | ingenierias | 1 | analista_ingenieria_operativa |
| integraciones_herramientas | Integraciones entre herramientas | automatizacion_integraciones | 8 | administrador_sistemas_internos, arquitecto_automatizaciones, auditor_automatizaciones, auditor_errores_sistemas, documentador_flujos_sistemas, especialista_integraciones_api, evaluador_herramientas_software, integrador_herramientas_digitales |
| inteligencia_comercial | Inteligencia comercial | datos_bi_analytics | 4 | analista_datos_negocio, analista_segmentacion_clientes, especialista_performance_marketing, minimalista_senal_ruido |
| intervencion_comunitaria | Intervención comunitaria | sociologia_trabajo_social | 0 | - |
| investigacion_academica | Investigación académica | educacion_docencia_investigacion | 1 | historiador_contexto_negocio |
| investigacion_mercado | Investigación de mercado | marketing_publicidad | 3 | analista_oportunidades_locales, historiador_contexto_negocio, investigador_usuarios |
| investigacion_visual_usuarios | Investigación visual de usuarios | diseno | 1 | investigador_usuarios |
| litigios_contencioso | Litigios y contencioso | legales | 0 | - |
| logistica_naviera | Logística naviera | naviero_maritimo_portuario | 1 | coordinador_operaciones_portuarias |
| mantenimiento_edilicio | Mantenimiento edilicio | oficios_otros | 0 | - |
| mantenimiento_equipos_pesados | Mantenimiento de equipos pesados | mineria_petroleo_gas | 1 | analista_operaciones_mineria_energia |
| mantenimiento_industrial | Mantenimiento industrial | produccion_manufactura | 0 | - |
| medicion_satisfaccion_cliente | Medición de satisfacción del cliente | customer_success_experiencia_cliente | 5 | analista_satisfaccion_cliente, auditor_calidad_atencion, especialista_customer_success, fidelizador_clientes_recurrentes, responsable_experiencia_cliente_local |
| mejora_continua_procesos | Mejora continua de procesos | produccion_manufactura | 5 | arquitecto_automatizaciones, auditor_calidad_operativa, auditor_procesos_negocio, capacitador_operativo_interno, organizador_procesos_pyme |
| mesa_ayuda | Mesa de ayuda | atencion_cliente_call_center_telemarketing | 3 | auditor_facturacion_cobros, coordinador_soporte_multicanal, gestor_consultas_clientes |
| modelos_negocio | Modelos de negocio | gerencia_direccion_general | 6 | analista_oportunidades_locales, asesor_emprendedor_generalista, consultor_modelo_negocio, estratega_negocio_digital, estratega_propuesta_valor, simulador_escenarios_negocio |
| objetivos_metricas_okrs | Objetivos, métricas y OKRs | gerencia_direccion_general | 9 | analista_sesgos_decision, auditor_dashboards_metricas, estratega_negocio_digital, gestor_evaluacion_desempeno, integrador_sintesis_decisiones, modelador_metricas_kpis, planificador_financiero_operativo, priorizador_roadmap, priorizador_tareas_dueno_negocio |
| onboarding_clientes | Onboarding de clientes | customer_success_experiencia_cliente | 3 | coordinador_operaciones_digitales, director_operativo_digital, especialista_customer_success |
| onboarding_empleados | Onboarding de empleados | recursos_humanos_capacitacion | 3 | disenador_onboarding_empleados, documentador_cultura_procesos, documentador_procedimientos_operativos |
| operaciones_mineras | Operaciones mineras | mineria_petroleo_gas | 1 | analista_operaciones_mineria_energia |
| operaciones_portuarias | Operaciones portuarias | naviero_maritimo_portuario | 1 | coordinador_operaciones_portuarias |
| performance_ads | Performance y anuncios | marketing_publicidad | 1 | especialista_performance_marketing |
| permisos_reportes_ambientales | Permisos y reportes ambientales | mineria_petroleo_gas | 1 | analista_operaciones_mineria_energia |
| planeamiento_financiero | Planeamiento financiero | administracion_contabilidad_finanzas | 5 | analista_finanzas_pyme, analista_rentabilidad_margen, consultor_modelo_negocio, planificador_financiero_operativo, simulador_escenarios_negocio |
| planificacion_compras | Planificación de compras | abastecimiento_logistica | 4 | coordinador_abastecimiento, gestor_stock_inventario, organizador_procesos_pyme, planificador_compras_proveedores |
| planificacion_estrategica | Planificación estratégica | gerencia_direccion_general | 4 | estratega_negocio_digital, evaluador_herramientas_software, historiador_contexto_negocio, integrador_sintesis_decisiones |
| planificacion_produccion | Planificación de producción | produccion_manufactura | 2 | coordinador_abastecimiento, gestor_stock_inventario |
| planificacion_proyectos_internos | Planificación de proyectos internos | gerencia_direccion_general | 5 | administrador_sistemas_internos, analista_contratos_operativos, analista_roles_responsabilidades, disenador_workflows_automatizados, especialista_continuidad_operativa |
| planificacion_turistica | Planificación turística | gastronomia_turismo | 0 | - |
| politicas_internas_basicas | Políticas internas básicas | legales | 6 | analista_contratos_operativos, controlador_cumplimiento_sops, documentador_cultura_procesos, gestor_compliance_pyme, gestor_documentacion_administrativa, redactor_politicas_internas |
| prensa_medios | Prensa y medios | comunicacion_relaciones_institucionales_publicas | 0 | - |
| presupuesto_por_area | Presupuesto por área | administracion_contabilidad_finanzas | 3 | controlador_gastos_pyme, controlador_presupuesto, planificador_financiero_operativo |
| presupuestos_computos | Presupuestos y cómputos | ingenieria_civil_construccion | 1 | coordinador_proyectos_construccion |
| pricing_packaging | Pricing y packaging | producto_gestion_producto | 4 | analista_precios_margenes, analista_rentabilidad_margen, consultor_modelo_negocio, estratega_propuesta_valor |
| priorizacion_roadmap | Priorización de roadmap | producto_gestion_producto | 2 | priorizador_roadmap, product_manager_digital |
| procesos_venta_pymes | Procesos de venta para pymes | comercial_ventas_negocios | 1 | asesor_emprendedor_generalista |
| programas_fidelizacion | Programas de fidelización | customer_success_experiencia_cliente | 2 | especialista_customer_success, fidelizador_clientes_recurrentes |
| programas_sociales | Programas sociales | sociologia_trabajo_social | 0 | - |
| propiedad_intelectual | Propiedad intelectual | legales | 0 | - |
| prospeccion_b2b | Prospección B2B | comercial_ventas_negocios | 2 | disenador_pipeline_comercial, especialista_ventas_consultivas |
| proteccion_datos_basica | Protección básica de datos | legales | 2 | analista_riesgo_legal_preventivo, auditor_privacidad_datos |
| protocolos_respuesta_cliente | Protocolos de respuesta al cliente | atencion_cliente_call_center_telemarketing | 5 | auditor_calidad_atencion, coordinador_canal_whatsapp, disenador_base_respuestas_cliente, gestor_consultas_clientes, gestor_reclamos_postventa |
| punto_equilibrio | Análisis de punto de equilibrio | administracion_contabilidad_finanzas | 2 | analista_costos_local, analista_precios_margenes |
| recepcion_atencion | Recepción y atención presencial | secretarias_recepcion | 3 | coordinador_operacion_local, gestor_consultas_clientes, responsable_experiencia_cliente_local |
| reclamos_postventa | Reclamos y postventa | atencion_cliente_call_center_telemarketing | 5 | analista_satisfaccion_cliente, auditor_calidad_atencion, auditor_facturacion_cobros, gestor_reclamos_postventa, optimizador_logistica_entregas |
| recuperacion_clientes_inactivos | Recuperación de clientes inactivos | customer_success_experiencia_cliente | 1 | fidelizador_clientes_recurrentes |
| renovacion_polizas | Renovación de pólizas | seguros | 0 | - |
| rentabilidad_por_canal | Rentabilidad por canal | datos_bi_analytics | 4 | analista_finanzas_pyme, analista_precios_margenes, analista_rentabilidad_margen, detector_fugas_rentabilidad |
| rentabilidad_producto | Rentabilidad por producto | administracion_contabilidad_finanzas | 4 | analista_costos_local, analista_precios_margenes, detector_fugas_rentabilidad, especialista_promociones_locales |
| rentabilidad_unidad_negocio | Rentabilidad por unidad de negocio | administracion_contabilidad_finanzas | 1 | modelador_metricas_kpis |
| research_usuarios | Research de usuarios | producto_gestion_producto | 3 | analista_sesgos_decision, investigador_usuarios, product_manager_digital |
| reservas_operaciones | Reservas y operaciones | gastronomia_turismo | 2 | coordinador_operacion_local, supervisor_turnos_y_tareas |
| retencion_fidelizacion_clientes | Retención y fidelización de clientes | customer_success_experiencia_cliente | 4 | analista_segmentacion_clientes, arquitecto_crm_operativo, especialista_customer_success, fidelizador_clientes_recurrentes |
| revenue_operations | Revenue operations | comercial_ventas_negocios | 2 | arquitecto_crm_operativo, revenue_operations_manager |
| scripts_objeciones_comerciales | Scripts comerciales y objeciones | comercial_ventas_negocios | 3 | copywriter_conversion, especialista_ventas_consultivas, operador_ventas_whatsapp |
| segmentacion_comercial_avanzada | Segmentación comercial avanzada | datos_bi_analytics | 2 | analista_segmentacion_clientes, arquitecto_crm_operativo |
| seguimiento_avance_obra | Seguimiento de avance de obra | ingenieria_civil_construccion | 1 | coordinador_proyectos_construccion |
| seguimiento_embarques | Seguimiento de embarques | aduana_comercio_exterior | 1 | especialista_comercio_exterior_aduana |
| seguimiento_entregables | Seguimiento de entregables | gerencia_direccion_general | 5 | analista_riesgo_tecnico_operativo, analista_roles_responsabilidades, auditor_procesos_negocio, disenador_workflows_automatizados, especialista_reporting_operativo |
| seguimiento_indicaciones_cuidado | Seguimiento de indicaciones de cuidado | enfermeria | 0 | - |
| seguimiento_oportunidades_comerciales | Seguimiento de oportunidades comerciales | comercial_ventas_negocios | 7 | coordinador_canal_whatsapp, disenador_pipeline_comercial, especialista_crm_whatsapp, gestor_calendario_comercial, operador_ventas_whatsapp, optimizador_logistica_entregas, priorizador_tareas_dueno_negocio |
| seguimiento_pacientes_cronicos | Seguimiento de pacientes crónicos | salud_medicina_farmacia | 1 | consultor_operaciones_salud_farmacia |
| seguimiento_proveedores | Seguimiento de proveedores | abastecimiento_logistica | 2 | coordinador_abastecimiento, planificador_compras_proveedores |
| seguimiento_tramites | Seguimiento de trámites | secretarias_recepcion | 2 | coordinador_operaciones_digitales, organizador_procesos_pyme |
| seguridad_ambiental | Seguridad y ambiente | mineria_petroleo_gas | 1 | analista_operaciones_mineria_energia |
| seguridad_higiene_obra | Seguridad e higiene en obra | ingenieria_civil_construccion | 1 | coordinador_proyectos_construccion |
| seguridad_operativa_basica | Seguridad operativa básica | tecnologia_sistemas_telecomunicaciones | 4 | analista_calidad_datos, analista_riesgo_tecnico_operativo, auditor_automatizaciones, auditor_privacidad_datos |
| seleccion_talento | Selección de talento | recursos_humanos_capacitacion | 0 | - |
| servicios_tecnicos | Servicios técnicos | oficios_otros | 0 | - |
| sistemas_diseno_marca | Sistemas de diseño y marca | diseno | 0 | - |
| soporte_cliente | Soporte al cliente | atencion_cliente_call_center_telemarketing | 5 | auditor_calidad_atencion, coordinador_soporte_multicanal, disenador_base_respuestas_cliente, gestor_consultas_clientes, gestor_reclamos_postventa |
| soporte_it | Soporte IT | tecnologia_sistemas_telecomunicaciones | 2 | administrador_sistemas_internos, auditor_errores_sistemas |
| soporte_tecnico_operativo | Soporte técnico operativo | tecnologia_sistemas_telecomunicaciones | 3 | administrador_sistemas_internos, coordinador_soporte_tecnico, especialista_monitoreo_alertas |
| soporte_tecnico_producto | Soporte técnico de producto | departamento_tecnico | 3 | coordinador_soporte_tecnico, especialista_base_conocimiento, tester_funcional_negocio |
| suscripcion_riesgos | Suscripción de riesgos | seguros | 2 | analista_riesgo_legal_preventivo, especialista_continuidad_operativa |
| tablero_direccion | Tablero de dirección | gerencia_direccion_general | 8 | arquitecto_datos_negocio, auditor_dashboards_metricas, controlador_presupuesto, director_operativo_digital, especialista_bi_dashboards, integrador_sintesis_decisiones, minimalista_senal_ruido, modelador_metricas_kpis |
| tableros_margen_costos | Tableros de margen y costos | datos_bi_analytics | 2 | analista_precios_margenes, controlador_presupuesto |
| telecomunicaciones | Telecomunicaciones | tecnologia_sistemas_telecomunicaciones | 0 | - |
| tesoreria_cashflow | Tesorería y cashflow | administracion_contabilidad_finanzas | 3 | analista_finanzas_pyme, analista_flujo_caja, gestor_caja_diaria |
| transformacion_organizacional | Transformación organizacional | gerencia_direccion_general | 1 | director_operativo_digital |
| triage_admision | Triage y admisión | enfermeria | 0 | - |
| tutoria_academica | Tutoría académica | educacion_docencia_investigacion | 0 | - |
| ux_ui | UX/UI | diseno | 2 | product_manager_digital, tester_funcional_negocio |
| validacion_ideas_negocio | Validación de ideas de negocio | producto_gestion_producto | 7 | analista_experimentos_ab_testing, analista_sesgos_decision, asesor_emprendedor_generalista, consultor_modelo_negocio, estratega_negocio_digital, estratega_propuesta_valor, product_manager_digital |
| validacion_requerimientos_tecnicos | Validación de requerimientos técnicos | ingenierias | 2 | analista_ingenieria_operativa, priorizador_roadmap |
| ventas_consultivas | Ventas consultivas | comercial_ventas_negocios | 2 | copywriter_conversion, especialista_ventas_consultivas |
| ventas_retail | Ventas retail | comercial_ventas_negocios | 7 | analista_costos_local, analista_oportunidades_locales, especialista_promociones_locales, gestor_caja_diaria, gestor_marketing_barrial, gestor_stock_inventario, operador_ventas_whatsapp |
| ventas_telefonicas | Ventas telefónicas | atencion_cliente_call_center_telemarketing | 1 | operador_ventas_whatsapp |
| voz_cliente_nps | Voz del cliente y NPS | customer_success_experiencia_cliente | 3 | analista_satisfaccion_cliente, especialista_bi_dashboards, investigador_usuarios |

## Top Areas Con Mas Perfiles

| area_id | perfiles |
| --- | --- |
| gerencia_direccion_general | 39 |
| comercial_ventas_negocios | 36 |
| administracion_contabilidad_finanzas | 35 |
| datos_bi_analytics | 35 |
| customer_success_experiencia_cliente | 29 |
| marketing_publicidad | 25 |
| automatizacion_integraciones | 22 |
| tecnologia_sistemas_telecomunicaciones | 19 |
| comunicacion_relaciones_institucionales_publicas | 14 |
| produccion_manufactura | 14 |

## Top Areas Con Menos Perfiles

| area_id | perfiles |
| --- | --- |
| enfermeria | 1 |
| ingenieria_civil_construccion | 1 |
| ingenierias | 1 |
| mineria_petroleo_gas | 1 |
| naviero_maritimo_portuario | 1 |
| oficios_otros | 1 |
| salud_medicina_farmacia | 1 |
| sociologia_trabajo_social | 1 |
| aduana_comercio_exterior | 2 |
| seguros | 2 |

## Nichos Sin Cobertura

| niche_id | nicho | area_id |
| --- | --- | --- |
| analisis_cartera_seguros | Análisis de cartera de seguros | seguros |
| analisis_loteria_juegos_azar | Análisis de Lotería y Juegos de Azar | oficios_otros |
| asuntos_publicos | Asuntos públicos | comunicacion_relaciones_institucionales_publicas |
| atencion_productores | Atención a productores | seguros |
| ciberseguridad | Ciberseguridad | tecnologia_sistemas_telecomunicaciones |
| cuidados_clinicos | Cuidados clínicos | enfermeria |
| datos_bi | Datos y BI | tecnologia_sistemas_telecomunicaciones |
| diseno_curricular | Diseño curricular | educacion_docencia_investigacion |
| diseno_grafico_marca | Diseño gráfico y marca | diseno |
| diseno_producto | Diseño de producto | diseno |
| educacion_paciente | Educación del paciente | enfermeria |
| evaluacion_impacto_social | Evaluación de impacto social | sociologia_trabajo_social |
| gestion_beneficios_compensaciones | Gestión de beneficios y compensaciones | recursos_humanos_capacitacion |
| gestion_casos_sociales | Gestión de casos sociales | sociologia_trabajo_social |
| gestion_crisis_comunicacional | Gestión de crisis comunicacional | comunicacion_relaciones_institucionales_publicas |
| gestion_garantias_tecnicas | Gestión de garantías técnicas | departamento_tecnico |
| gestion_instituciones_educativas | Gestión de instituciones educativas | educacion_docencia_investigacion |
| gestion_siniestros | Gestión de siniestros | seguros |
| intervencion_comunitaria | Intervención comunitaria | sociologia_trabajo_social |
| litigios_contencioso | Litigios y contencioso | legales |
| mantenimiento_edilicio | Mantenimiento edilicio | oficios_otros |
| mantenimiento_industrial | Mantenimiento industrial | produccion_manufactura |
| planificacion_turistica | Planificación turística | gastronomia_turismo |
| prensa_medios | Prensa y medios | comunicacion_relaciones_institucionales_publicas |
| programas_sociales | Programas sociales | sociologia_trabajo_social |
| propiedad_intelectual | Propiedad intelectual | legales |
| renovacion_polizas | Renovación de pólizas | seguros |
| seguimiento_indicaciones_cuidado | Seguimiento de indicaciones de cuidado | enfermeria |
| seleccion_talento | Selección de talento | recursos_humanos_capacitacion |
| servicios_tecnicos | Servicios técnicos | oficios_otros |
| sistemas_diseno_marca | Sistemas de diseño y marca | diseno |
| telecomunicaciones | Telecomunicaciones | tecnologia_sistemas_telecomunicaciones |
| triage_admision | Triage y admisión | enfermeria |
| tutoria_academica | Tutoría académica | educacion_docencia_investigacion |

## Nichos Con Cobertura Debil

| niche_id | nicho | area_id | perfil |
| --- | --- | --- | --- |
| agenda_consultorios_salud | Agenda de consultorios de salud | salud_medicina_farmacia | consultor_operaciones_salud_farmacia |
| analisis_cohortes | Análisis de cohortes | datos_bi_analytics | analista_experimentos_ab_testing |
| analisis_contratos | Análisis de contratos | legales | analista_contratos_operativos |
| auditoria_medica | Auditoría médica | salud_medicina_farmacia | consultor_operaciones_salud_farmacia |
| clasificacion_arancelaria | Clasificación arancelaria | aduana_comercio_exterior | especialista_comercio_exterior_aduana |
| compliance_comercio_exterior | Compliance de comercio exterior | aduana_comercio_exterior | especialista_comercio_exterior_aduana |
| comunicacion_institucional | Comunicación institucional | comunicacion_relaciones_institucionales_publicas | estratega_contenidos |
| contratos_simples_pymes | Contratos simples para pymes | legales | analista_contratos_operativos |
| control_costos_obra | Control de costos de obra | ingenieria_civil_construccion | coordinador_proyectos_construccion |
| control_documental_portuario | Control documental portuario | naviero_maritimo_portuario | coordinador_operaciones_portuarias |
| control_produccion_minera_energia | Control de producción minera y energética | mineria_petroleo_gas | analista_operaciones_mineria_energia |
| coordinacion_operaciones_embarque | Coordinación de operaciones de embarque | naviero_maritimo_portuario | coordinador_operaciones_portuarias |
| coordinacion_turnos_enfermeria | Coordinación de turnos de enfermería | enfermeria | supervisor_turnos_y_tareas |
| costos_importacion_exportacion | Costos de importación y exportación | aduana_comercio_exterior | especialista_comercio_exterior_aduana |
| derecho_laboral | Derecho laboral | legales | analista_riesgo_legal_preventivo |
| diagnostico_social | Diagnóstico social | sociologia_trabajo_social | analista_oportunidades_locales |
| direccion_obra | Dirección de obra | ingenieria_civil_construccion | coordinador_proyectos_construccion |
| diseno_pipeline_comercial | Diseño de pipeline comercial | comercial_ventas_negocios | disenador_pipeline_comercial |
| distribucion_transporte | Distribución y transporte | abastecimiento_logistica | optimizador_logistica_entregas |
| documentacion_import_export | Documentación import/export | aduana_comercio_exterior | especialista_comercio_exterior_aduana |
| documentacion_maritima | Documentación marítima | naviero_maritimo_portuario | coordinador_operaciones_portuarias |
| ecommerce_y_marketplaces | E-commerce y marketplaces | comercial_ventas_negocios | especialista_performance_marketing |
| farmacia_clinica | Farmacia clínica | salud_medicina_farmacia | consultor_operaciones_salud_farmacia |
| flujos_no_code_low_code | Flujos no-code y low-code | automatizacion_integraciones | constructor_automatizaciones_no_code |
| gestion_cambios_ingenieria | Gestión de cambios de ingeniería | ingenierias | analista_ingenieria_operativa |
| gestion_consultorios | Gestión de consultorios | salud_medicina_farmacia | consultor_operaciones_salud_farmacia |
| gestion_documental | Gestión documental | secretarias_recepcion | documentador_procedimientos_operativos |
| gestion_proyectos_ingenieria | Gestión de proyectos de ingeniería | ingenierias | analista_ingenieria_operativa |
| gestion_servicios_oficios | Gestión de servicios y oficios | oficios_otros | coordinador_operacion_local |
| hoteleria_experiencia_huesped | Hotelería y experiencia del huésped | gastronomia_turismo | responsable_experiencia_cliente_local |
| ingenieria_calidad | Ingeniería de calidad | ingenierias | analista_ingenieria_operativa |
| ingenieria_procesos | Ingeniería de procesos | ingenierias | analista_ingenieria_operativa |
| investigacion_academica | Investigación académica | educacion_docencia_investigacion | historiador_contexto_negocio |
| investigacion_visual_usuarios | Investigación visual de usuarios | diseno | investigador_usuarios |
| logistica_naviera | Logística naviera | naviero_maritimo_portuario | coordinador_operaciones_portuarias |
| mantenimiento_equipos_pesados | Mantenimiento de equipos pesados | mineria_petroleo_gas | analista_operaciones_mineria_energia |
| operaciones_mineras | Operaciones mineras | mineria_petroleo_gas | analista_operaciones_mineria_energia |
| operaciones_portuarias | Operaciones portuarias | naviero_maritimo_portuario | coordinador_operaciones_portuarias |
| performance_ads | Performance y anuncios | marketing_publicidad | especialista_performance_marketing |
| permisos_reportes_ambientales | Permisos y reportes ambientales | mineria_petroleo_gas | analista_operaciones_mineria_energia |
| presupuestos_computos | Presupuestos y cómputos | ingenieria_civil_construccion | coordinador_proyectos_construccion |
| procesos_venta_pymes | Procesos de venta para pymes | comercial_ventas_negocios | asesor_emprendedor_generalista |
| recuperacion_clientes_inactivos | Recuperación de clientes inactivos | customer_success_experiencia_cliente | fidelizador_clientes_recurrentes |
| rentabilidad_unidad_negocio | Rentabilidad por unidad de negocio | administracion_contabilidad_finanzas | modelador_metricas_kpis |
| seguimiento_avance_obra | Seguimiento de avance de obra | ingenieria_civil_construccion | coordinador_proyectos_construccion |
| seguimiento_embarques | Seguimiento de embarques | aduana_comercio_exterior | especialista_comercio_exterior_aduana |
| seguimiento_pacientes_cronicos | Seguimiento de pacientes crónicos | salud_medicina_farmacia | consultor_operaciones_salud_farmacia |
| seguridad_ambiental | Seguridad y ambiente | mineria_petroleo_gas | analista_operaciones_mineria_energia |
| seguridad_higiene_obra | Seguridad e higiene en obra | ingenieria_civil_construccion | coordinador_proyectos_construccion |
| transformacion_organizacional | Transformación organizacional | gerencia_direccion_general | director_operativo_digital |
| ventas_telefonicas | Ventas telefónicas | atencion_cliente_call_center_telemarketing | operador_ventas_whatsapp |

## Perfiles Con Mas Nichos

| profile_id | nichos |
| --- | --- |
| administrador_sistemas_internos | 5 |
| analista_calidad_datos | 5 |
| analista_contratos_operativos | 5 |
| analista_costos_local | 5 |
| analista_datos_negocio | 5 |
| analista_experimentos_ab_testing | 5 |
| analista_finanzas_pyme | 5 |
| analista_flujo_caja | 5 |
| analista_ingenieria_operativa | 5 |
| analista_operaciones_mineria_energia | 5 |

## Perfiles Con Menos Nichos

| profile_id | nichos |
| --- | --- |
| administrador_sistemas_internos | 5 |
| analista_calidad_datos | 5 |
| analista_contratos_operativos | 5 |
| analista_costos_local | 5 |
| analista_datos_negocio | 5 |
| analista_experimentos_ab_testing | 5 |
| analista_finanzas_pyme | 5 |
| analista_flujo_caja | 5 |
| analista_ingenieria_operativa | 5 |
| analista_operaciones_mineria_energia | 5 |

## Dominantes Por Area

| area_id | familias_dominantes | model_policies_dominantes | business_scales_dominantes |
| --- | --- | --- | --- |
| abastecimiento_logistica | operaciones_procesos (4), finanzas_administracion (3), calidad_riesgo (2) | local_standard (3), privacy_sensitive (2), batch_analysis (2) | pyme (10), local_comercial (9), empresa_mediana (8) |
| administracion_contabilidad_finanzas | finanzas_administracion (12), operaciones_procesos (4), datos_analytics (4) | privacy_sensitive (7), batch_analysis (6), high_reliability (6) | pyme (35), empresa_mediana (26), local_comercial (22) |
| aduana_comercio_exterior | industria_oficios (2) | human_review_required (1), high_reliability (1) | pyme (2), empresa_mediana (2), enterprise (2) |
| atencion_cliente_call_center_telemarketing | soporte_customer_success (7), ventas_revenue (2), contenido_comunicacion (1) | cloud_low_latency (5), fast_iteration (2), human_review_required (1) | pyme (12), empresa_mediana (11), local_comercial (10) |
| automatizacion_integraciones | automatizacion_tecnologia (11), calidad_riesgo (5), operaciones_procesos (2) | high_reliability (8), hybrid (3), cloud_low_latency (3) | pyme (22), empresa_mediana (20), enterprise (16) |
| comercial_ventas_negocios | marketing_growth (5), ventas_revenue (5), finanzas_administracion (5) | batch_analysis (6), cloud_low_latency (6), fast_iteration (5) | pyme (36), local_comercial (27), emprendedor (26) |
| comunicacion_relaciones_institucionales_publicas | contenido_comunicacion (3), rrhh_capacitacion (3), marketing_growth (2) | long_context (6), cost_sensitive (2), fast_iteration (2) | pyme (14), local_comercial (11), empresa_mediana (10) |
| customer_success_experiencia_cliente | soporte_customer_success (10), operaciones_procesos (3), ventas_revenue (3) | cloud_low_latency (7), hybrid (6), privacy_sensitive (4) | pyme (29), empresa_mediana (27), local_comercial (18) |
| datos_bi_analytics | datos_analytics (8), finanzas_administracion (6), calidad_riesgo (5) | batch_analysis (8), high_reliability (8), privacy_sensitive (6) | pyme (35), empresa_mediana (34), enterprise (25) |
| departamento_tecnico | soporte_customer_success (2), calidad_riesgo (2), contenido_comunicacion (1) | high_reliability (3), cost_sensitive (1), long_context (1) | pyme (6), empresa_mediana (6), enterprise (5) |
| diseno | producto_ux (2), contenido_comunicacion (2) | hybrid (1), long_context (1), local_standard (1) | emprendedor (4), pyme (4), empresa_mediana (3) |
| educacion_docencia_investigacion | rrhh_capacitacion (3), automatizacion_tecnologia (1), soporte_customer_success (1) | long_context (5), local_standard (1) | pyme (6), empresa_mediana (6), local_comercial (5) |
| enfermeria | operaciones_procesos (1) | local_standard (1) | local_comercial (1), pyme (1), empresa_mediana (1) |
| gastronomia_turismo | operaciones_procesos (3), finanzas_administracion (2), soporte_customer_success (1) | local_standard (2), batch_analysis (2), privacy_sensitive (1) | local_comercial (7), pyme (7), empresa_mediana (4) |
| gerencia_direccion_general | calidad_riesgo (6), operaciones_procesos (5), estrategia_direccion (4) | high_reliability (8), human_review_required (7), cloud_reasoning (6) | pyme (38), empresa_mediana (35), enterprise (23) |
| ingenieria_civil_construccion | industria_oficios (1) | high_reliability (1) | pyme (1), empresa_mediana (1), enterprise (1) |
| ingenierias | industria_oficios (1) | high_reliability (1) | pyme (1), empresa_mediana (1), enterprise (1) |
| legales | legal_compliance (4), contenido_comunicacion (1), finanzas_administracion (1) | human_review_required (4), high_reliability (1), privacy_sensitive (1) | pyme (8), empresa_mediana (7), local_comercial (5) |
| marketing_publicidad | marketing_growth (5), ventas_revenue (4), contenido_comunicacion (3) | cloud_low_latency (5), fast_iteration (4), cloud_reasoning (3) | pyme (25), emprendedor (20), empresa_mediana (16) |
| mineria_petroleo_gas | industria_oficios (1) | human_review_required (1) | empresa_mediana (1), enterprise (1) |
| naviero_maritimo_portuario | industria_oficios (1) | high_reliability (1) | pyme (1), empresa_mediana (1), enterprise (1) |
| oficios_otros | operaciones_procesos (1) | local_standard (1) | emprendedor (1), local_comercial (1), pyme (1) |
| produccion_manufactura | calidad_riesgo (4), operaciones_procesos (3), finanzas_administracion (2) | high_reliability (5), local_standard (3), cost_sensitive (2) | pyme (13), empresa_mediana (12), local_comercial (9) |
| producto_gestion_producto | producto_ux (4), estrategia_direccion (2), calidad_riesgo (2) | cloud_reasoning (3), hybrid (2), high_reliability (2) | pyme (11), empresa_mediana (11), enterprise (8) |
| recursos_humanos_capacitacion | rrhh_capacitacion (5), contenido_comunicacion (2), operaciones_procesos (1) | long_context (3), local_standard (2), human_review_required (2) | pyme (9), empresa_mediana (9), local_comercial (7) |
| salud_medicina_farmacia | industria_oficios (1) | privacy_sensitive (1) | pyme (1), empresa_mediana (1), enterprise (1) |
| secretarias_recepcion | operaciones_procesos (4), marketing_growth (1), contenido_comunicacion (1) | cost_sensitive (3), local_standard (3), cloud_low_latency (1) | local_comercial (7), pyme (7), emprendedor (6) |
| seguros | legal_compliance (1), calidad_riesgo (1) | human_review_required (1), high_reliability (1) | pyme (2), empresa_mediana (2), enterprise (2) |
| sociologia_trabajo_social | investigacion_analisis (1) | cloud_reasoning (1) | emprendedor (1), local_comercial (1), pyme (1) |
| tecnologia_sistemas_telecomunicaciones | automatizacion_tecnologia (7), calidad_riesgo (6), producto_ux (2) | high_reliability (11), hybrid (3), human_review_required (2) | pyme (19), empresa_mediana (19), enterprise (18) |

## Recomendaciones Para Proximas Fases

- Usar esta matriz para generar vistas por dominio sin duplicar datos fuente.
- Priorizar Prompt 19.1 si se necesita export JSON/API de la matriz.
- Usar los 34 nichos sin cobertura como backlog de expansion futura, no como bloqueo.
- Usar los nichos con cobertura debil para decidir presets, papers o team templates.
- Mantener Prompt 20 como siguiente fase natural para recomendacion provider/model por perfil.
