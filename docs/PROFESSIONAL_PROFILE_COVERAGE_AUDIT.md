# Auditoría de cobertura de perfiles profesionales

Prompt 18.7 audita la cobertura real de `catalogs/professional_profiles.json` contra 30 áreas y 200 nichos. No agrega perfiles, no modifica dominios específicos y no resuelve huecos todavía: los documenta para decidir el siguiente movimiento con evidencia.

## Resumen Ejecutivo

- Perfiles globales PASSED: 100.
- Áreas totales: 30.
- Áreas con al menos 1 perfil compatible: 24.
- Áreas sin cobertura: 6.
- Nichos totales: 200.
- Nichos con al menos 1 perfil compatible: 137.
- Nichos sin cobertura: 63.
- Nichos con 2+ perfiles: 114.
- Nichos con 3+ perfiles: 82.
- Familias profesionales usadas: 14 de 16.
- Model policies usadas: 13 de 15.
- Escalas de negocio usadas: 6 de 7.

Recomendación final: **requiere expansión controlada**, no por cantidad, sino por huecos sectoriales claros. La masa crítica de 100 perfiles es suficiente para avanzar en normalización y diseño de presets generales, pero no alcanza para declarar cobertura sana de las 30 áreas porque 6 áreas están sin perfiles y el test mínimo de 25 áreas cubiertas falla con 24.

## Métricas De Cobertura

| Métrica | Valor |
|---|---:|
| Áreas con al menos 1 perfil | 24 |
| Áreas con al menos 3 perfiles | 20 |
| Áreas con al menos 5 perfiles | 19 |
| Áreas con cobertura débil, 1-2 perfiles | 4 |
| Áreas sin cobertura | 6 |
| Nichos con al menos 1 perfil | 137 |
| Nichos con al menos 2 perfiles | 114 |
| Nichos con al menos 3 perfiles | 82 |
| Nichos con cobertura débil, 1 perfil | 23 |
| Nichos sin cobertura | 63 |
| Promedio de perfiles por área | 11.40 |
| Mediana de perfiles por área | 7 |
| Promedio de perfiles por nicho | 2.50 |
| Mediana de perfiles por nicho | 2 |

## Criterios De Salud

- Área saludable: al menos 3 perfiles compatibles; idealmente 5+ si tiene muchos nichos.
- Nicho saludable: al menos 1 perfil compatible; idealmente 2+ si es operativo importante; 3+ si impacta ingresos, riesgo o automatización.
- Perfil demasiado amplio: muchas áreas/nichos sin justificación clara. En esta etapa no hay extremos: el patrón dominante es 3-4 áreas y 5 nichos.
- Perfil demasiado estrecho: muy pocos nichos sin necesidad clara. En esta etapa no se detectan perfiles de 1 nicho.
- Solapamiento: coincidencia alta de áreas, nichos, familia y función. Hay solapamientos aceptables y algunos pares para revisar.
- Hueco crítico: área sin cobertura, nicho sin cobertura en área sectorial o valor económico importante subcubierto.

## Cobertura Por Área

| area_id | nichos | perfiles | clasificación | recomendación |
|---|---:|---:|---|---|
| `gerencia_direccion_general` | 9 | 37 | cobertura_fuerte | Mantener; evitar sobrecargar con perfiles directivos genéricos. |
| `comercial_ventas_negocios` | 12 | 36 | cobertura_fuerte | Suficiente para presets iniciales. |
| `datos_bi_analytics` | 9 | 35 | cobertura_fuerte | Suficiente; revisar especializaciones BI en Prompt 18.8. |
| `administracion_contabilidad_finanzas` | 13 | 32 | cobertura_fuerte | Suficiente; buen eje pyme/operativo. |
| `customer_success_experiencia_cliente` | 9 | 28 | cobertura_fuerte | Suficiente para soporte/retención. |
| `marketing_publicidad` | 13 | 25 | cobertura_fuerte | Suficiente; posibles presets por canal después. |
| `automatizacion_integraciones` | 9 | 22 | cobertura_fuerte | Suficiente; requiere normalizar API/no-code en roles. |
| `tecnologia_sistemas_telecomunicaciones` | 9 | 18 | cobertura_fuerte | Buena base; ciberseguridad y telecom quedan sin nicho cubierto. |
| `comunicacion_relaciones_institucionales_publicas` | 5 | 14 | cobertura_fuerte | Buena base; prensa/asuntos públicos quedan débiles. |
| `produccion_manufactura` | 5 | 12 | cobertura_fuerte | Base transversal, no sectorial profunda. |
| `atencion_cliente_call_center_telemarketing` | 6 | 12 | cobertura_fuerte | Suficiente para atención inicial. |
| `producto_gestion_producto` | 5 | 11 | cobertura_fuerte | Suficiente. |
| `abastecimiento_logistica` | 5 | 9 | cobertura_fuerte | Suficiente para pyme/logística básica. |
| `recursos_humanos_capacitacion` | 7 | 9 | cobertura_fuerte | Suficiente, salvo selección/beneficios sin cobertura. |
| `gastronomia_turismo` | 5 | 7 | cobertura_fuerte | Base local/operativa; turismo específico débil. |
| `legales` | 9 | 7 | cobertura_fuerte | Base preventiva; litigios y PI sin cobertura. |
| `secretarias_recepcion` | 5 | 7 | cobertura_fuerte | Suficiente para gestión administrativa. |
| `departamento_tecnico` | 5 | 6 | cobertura_fuerte | Suficiente inicial; garantías técnicas sin cobertura. |
| `educacion_docencia_investigacion` | 6 | 6 | cobertura_fuerte | Suficiente general; diseño curricular y tutoría sin cobertura. |
| `diseno` | 5 | 4 | cobertura_media | Requiere expansión futura si diseño se vuelve prioridad. |
| `seguros` | 5 | 2 | cobertura_debil | Requiere expansión sectorial controlada. |
| `sociologia_trabajo_social` | 5 | 1 | cobertura_debil | Requiere expansión sectorial si se priorizan programas sociales. |
| `enfermeria` | 5 | 1 | cobertura_debil | Requiere perfiles de salud/enfermería, con cuidado regulatorio. |
| `oficios_otros` | 4 | 1 | cobertura_debil | Requiere cobertura de oficios sin contaminar dominios específicos. |
| `salud_medicina_farmacia` | 5 | 0 | sin_cobertura | Hueco crítico sectorial. |
| `ingenierias` | 5 | 0 | sin_cobertura | Hueco sectorial técnico. |
| `ingenieria_civil_construccion` | 5 | 0 | sin_cobertura | Hueco sectorial técnico. |
| `mineria_petroleo_gas` | 5 | 0 | sin_cobertura | Hueco sectorial regulado. |
| `aduana_comercio_exterior` | 5 | 0 | sin_cobertura | Hueco sectorial regulado. |
| `naviero_maritimo_portuario` | 5 | 0 | sin_cobertura | Hueco sectorial operativo/regulado. |

## Nichos

### Nichos Con Cobertura Fuerte

Los nichos más cubiertos son `control_gestion` e `indicadores_negocio` con 13 perfiles cada uno, seguidos por `comunicacion_interna` con 10, `auditoria_datos` y `objetivos_metricas_okrs` con 9, y `arquitectura_sistemas_internos`, `integraciones_herramientas`, `tablero_direccion`, `dashboards_operativos` y `experiencia_postventa` con 8.

### Nichos Con Cobertura Débil

Hay 23 nichos con un solo perfil. Entre los más relevantes: `analisis_cohortes`, `analisis_contratos`, `contratos_simples_pymes`, `derecho_laboral`, `diseno_pipeline_comercial`, `ecommerce_y_marketplaces`, `flujos_no_code_low_code`, `gestion_servicios_oficios`, `investigacion_academica`, `performance_ads`, `recuperacion_clientes_inactivos`, `transformacion_organizacional`, `validacion_requerimientos_tecnicos` y `ventas_telefonicas`.

### Nichos Sin Cobertura

Hay 63 nichos sin cobertura. Se concentran en salud, enfermería, ingeniería civil, ingenierías, minería/energía, aduana/comercio exterior, naviero/portuario, seguros, comunicación institucional avanzada, diseño visual/producto, educación específica y algunos nichos técnicos como `ciberseguridad`, `telecomunicaciones` y `datos_bi`.

Nichos sin cobertura más críticos para expansión futura:

- `gestion_consultorios`, `auditoria_medica`, `farmacia_clinica`, `seguimiento_pacientes_cronicos`.
- `cuidados_clinicos`, `triage_admision`, `educacion_paciente`.
- `gestion_proyectos_ingenieria`, `ingenieria_procesos`, `ingenieria_calidad`.
- `direccion_obra`, `presupuestos_computos`, `seguridad_higiene_obra`.
- `operaciones_mineras`, `seguridad_ambiental`, `control_produccion_minera_energia`.
- `clasificacion_arancelaria`, `documentacion_import_export`, `compliance_comercio_exterior`.
- `operaciones_portuarias`, `logistica_naviera`, `documentacion_maritima`.
- `gestion_siniestros`, `renovacion_polizas`, `analisis_cartera_seguros`.
- `ciberseguridad`, `telecomunicaciones`.

## Familias Profesionales

Más presentes:

- `calidad_riesgo`: 13
- `automatizacion_tecnologia`: 12
- `finanzas_administracion`: 12
- `soporte_customer_success`: 10
- `operaciones_procesos`: 9
- `datos_analytics`: 8

Menos presentes:

- `legal_compliance`: 4
- `estrategia_direccion`: 4
- `producto_ux`: 4
- `investigacion_analisis`: 4
- `industria_oficios`: 0
- `dominio_especializado`: 0

La ausencia de `industria_oficios` y `dominio_especializado` es coherente con la decisión de no crear perfiles específicos de dominio todavía, pero explica parte de la baja cobertura sectorial.

## Tipos, Seniority, Carga Cognitiva Y Estilo

Tipos más presentes: `analitico` 15, `operativo` 11, `tecnico` 9, `coordinacion` 8, `auditoria` 7.  
Seniority: `senior` 56, `semi_senior` 30, `lead` 12, `executive` 2.  
Cognitive load: `media` 45, `alta` 45, `muy_alta` 9, `baja` 1.  
Reasoning style: `operativo` 19, `critico` 19, `analitico` 16, `coordinador` 11, `tecnico` 9.

## Escalas De Negocio

- `pyme`: 100
- `empresa_mediana`: 83
- `local_comercial`: 59
- `enterprise`: 48
- `emprendedor`: 47
- `investigacion`: 4
- `dominio_especializado`: 0

Pyme está deliberadamente cubierta por todos los perfiles. Emprendedor/local quedaron bien cubiertos. Enterprise tiene cobertura suficiente, no dominante. `dominio_especializado` está aislado, correcto para esta etapa.

## Valor Económico

Mejor cubiertos:

- reducir costos: 19
- ordenar operación: 17
- proteger valor: 17
- mejorar decisión: 17
- aumentar ventas: 15
- mejorar conversión: 14
- generar ingresos: 14
- mejorar retención: 13
- mejorar margen: 12
- profesionalizar negocio: 12

Débiles o subrepresentados:

- escalar equipo.
- cobertura regulatoria sectorial.
- seguridad/ciberseguridad.
- continuidad sanitaria/asistencial.
- comercio exterior y logística portuaria.
- ingeniería/obra/minería.
- propiedad intelectual y litigios.

## Model Policies

Usadas:

- `high_reliability`: 17
- `batch_analysis`: 10
- `hybrid`: 10
- `privacy_sensitive`: 9
- `local_standard`: 9
- `cloud_low_latency`: 9
- `human_review_required`: 8
- `long_context`: 7
- `cloud_reasoning`: 6
- `cost_sensitive`: 6
- `fast_iteration`: 6
- `local_heavy`: 2
- `local_light`: 1

No usadas:

- `multimodal`
- `offline_capable`

Subrepresentadas: `local_heavy`, `local_light`, `offline_capable`, `multimodal`. Esto no bloquea la etapa, pero debe revisarse antes de perfiles sectoriales con documentos, imágenes, campo u operación offline.

No se detecta exceso problemático de `cloud_reasoning`. La presencia de `human_review_required` y `privacy_sensitive` es razonable para legal, RRHH, riesgo, privacidad y finanzas.

## Perfiles Amplios, Estrechos Y Solapamientos

No hay perfiles extremadamente amplios: el máximo observado es 4 áreas y 5 nichos. Esto sugiere buena calibración general, aunque varios perfiles son transversales.

Perfiles amplios aceptables:

- `analista_costos_local`
- `supervisor_turnos_y_tareas`
- `gestor_stock_inventario`
- `responsable_experiencia_cliente_local`
- `arquitecto_crm_operativo`
- `especialista_continuidad_operativa`
- `evaluador_herramientas_software`
- `asesor_emprendedor_generalista`

Perfiles estrechos: no se detectan perfiles de 1 nicho o 1 área. La estrechez real está en áreas sectoriales sin perfiles, no en perfiles existentes demasiado micro.

Solapamientos a revisar en futuro:

- `especialista_promociones_locales` y `gestor_marketing_barrial`: posible fusión o separación por canal/campaña.
- `especialista_crm_whatsapp` y `coordinador_canal_whatsapp`: solapamiento alto pero aceptable si uno queda como CRM y otro como canal.
- `controlador_gastos_pyme` y `controlador_presupuesto`: revisar límites.
- `especialista_bi_dashboards`, `arquitecto_datos_negocio` y `modelador_metricas_kpis`: solapamiento técnico aceptable, requiere normalización de roles/especializaciones.
- `disenador_onboarding_empleados` y `documentador_cultura_procesos`: revisar si el segundo debe ser memoria/cultura y no onboarding.
- `auditor_calidad_operativa` y `auditor_operacion_diaria`: revisar alcance de auditoría.

## Huecos Y Recomendaciones

### Huecos Que Justifican Expansión Futura

- Salud, medicina y farmacia.
- Enfermería.
- Ingenierías.
- Ingeniería civil y construcción.
- Minería, petróleo y gas.
- Aduana y comercio exterior.
- Naviero, marítimo y portuario.
- Seguros.
- Oficios y servicios técnicos.
- Sociología/trabajo social.
- Diseño visual/producto cuando sea prioridad.
- Ciberseguridad y telecomunicaciones.

### Huecos Para Resolver Con Normalización De Roles/Especializaciones

- BI avanzado y data quality.
- CRM operativo y revenue systems.
- No-code/low-code.
- QA funcional y observabilidad.
- Compliance pyme, privacidad y contratos.
- SOPs, continuidad y auditoría de procesos.
- Sesgos, síntesis multicriterio y simulación.

### Huecos Para Resolver Con Presets/Papers Después

- Perfiles ya fuertes pero todavía no operables como agentes: datos/BI, automatización, finanzas pyme, soporte multicanal, CRM, auditoría y RRHH.
- Perfiles que necesitan instrucciones de uso por escala: emprendedor, local comercial, pyme y empresa mediana.
- Perfiles de alto riesgo que necesitarán human review explícito en presets: legal, RRHH, privacidad, finanzas y continuidad.

## Decisión

La masa crítica de 100 perfiles es **útil y suficiente para avanzar a Prompt 18.8**, pero no es suficiente para declarar cobertura completa. La siguiente etapa debe normalizar roles/especializaciones y, después, planificar una expansión sectorial controlada para áreas hoy sin cobertura.

No se agregaron perfiles en Prompt 18.7.

## 18.7.A — Expansión sectorial mínima para cerrar cobertura

La auditoría 18.7 detectó 6 áreas sin cobertura:

- `aduana_comercio_exterior`
- `ingenieria_civil_construccion`
- `ingenierias`
- `mineria_petroleo_gas`
- `naviero_maritimo_portuario`
- `salud_medicina_farmacia`

El subprompt 18.7.A no relajó el test de cobertura. Agregó una expansión sectorial mínima de 6 perfiles PASSED, uno por área descubierta, para resolver el hueco real sin convertir la corrección en expansión masiva.

Perfiles agregados:

- `especialista_comercio_exterior_aduana` cubre `aduana_comercio_exterior`.
- `coordinador_proyectos_construccion` cubre `ingenieria_civil_construccion`.
- `analista_ingenieria_operativa` cubre `ingenierias`.
- `analista_operaciones_mineria_energia` cubre `mineria_petroleo_gas`.
- `coordinador_operaciones_portuarias` cubre `naviero_maritimo_portuario`.
- `consultor_operaciones_salud_farmacia` cubre `salud_medicina_farmacia`.

Cobertura resultante:

- Perfiles globales: 106.
- Áreas con cobertura: 30 de 30.
- Áreas sin cobertura: 0.
- Nichos con cobertura: 166 de 200.
- Nichos sin cobertura: 34.

Nichos reforzados:

- Documentación import/export, clasificación arancelaria, compliance de comercio exterior, seguimiento de embarques y costos de import/export.
- Dirección de obra, presupuestos/cómputos, seguridad e higiene, seguimiento de avance y control de costos de obra.
- Ingeniería de procesos, ingeniería de calidad, proyectos de ingeniería, requerimientos técnicos y cambios de ingeniería.
- Operaciones mineras, seguridad/ambiente, mantenimiento de equipos pesados, producción minera/energética y reportes ambientales.
- Operaciones portuarias, documentación marítima, logística naviera, coordinación de embarque y control documental portuario.
- Gestión de consultorios, farmacia clínica, auditoría médica, agenda de salud y seguimiento de pacientes crónicos.

Esta corrección no crea perfiles de dominio específico. Son perfiles globales sectoriales para áreas profesionales reguladas o técnicas que antes estaban completamente descubiertas.

## Nota 18.8 - Normalizacion role_id / specialization_id

Prompt 18.8 normalizo la relacion entre perfiles globales y roles/especializaciones.

Resultado:

- 106 de 106 perfiles tienen `expected_role_id` valido.
- 106 de 106 perfiles tienen `expected_specialization_id` valido.
- 0 perfiles mantienen valores `pending`, `required` o invalidos.
- 20 de 20 roles globales estan usados por perfiles.
- 49 de 80 especializaciones globales estan usadas por perfiles.
- No se agregaron roles, especializaciones ni perfiles.

La normalizacion queda documentada en `docs/PROFESSIONAL_PROFILE_ROLE_SPECIALIZATION_AUDIT.md` y validada por `tests/test_professional_profile_role_specialization.py`.
