# Catálogos compartidos de IA_CORE

`catalogs/` es Patrimonio compartido del sistema: no pertenece al Core de ejecución ni a un dominio particular como Lotería.

Contiene fuentes comunes para ayudar a crear dominios nuevos de forma consistente.

## Área profesional vs nicho

- Un **área profesional** agrupa una familia amplia de trabajo, por ejemplo `Legales` o `Tecnología, Sistemas y Telecomunicaciones`.
- Un **nicho** es un caso de uso más concreto dentro de un área, por ejemplo `Análisis de contratos` o `Soporte IT`.

Los nichos incluyen sugerencias para crear dominios:

- nombre sugerido del dominio;
- descripción sugerida;
- instrucciones sugeridas que luego podrán heredar los agentes del dominio.

El modal **Crear Dominio** consume estos catálogos desde `GET /api/catalogs/domain-creation`.
El usuario elige primero un área profesional y luego un nicho específico; con esa selección se autocompletan nombre, descripción e instrucciones, pero los campos siguen siendo editables antes de guardar.

## Alcance actual

El catálogo cubre:

- áreas profesionales y nichos iniciales;
- roles/arquetipos profesionales globales en `roles.json`;
- especializaciones profesionales globales por rol en `specializations.json`.

Los roles globales describen funciones cognitivas u operativas reutilizables, como `Analista`, `Auditor`, `Optimizador` o `Gestor de riesgo`. No representan todavía los roles habilitados para un dominio específico y no reemplazan el selector actual de Crear Agente.

Las especializaciones son ángulos profesionales asociados a roles globales. Por ejemplo, `auditor` puede tener `Auditoría de calidad`, `Auditoría de consistencia` o `Auditoría de sesgos`. No representan todavía especializaciones habilitadas por dominio y no reemplazan `specializationMap`.

La habilitación Dominio → Roles → Especializaciones empieza a vivir en `domains/<domain_id>/profile_catalog.json`. Ese archivo no pertenece a `catalogs/`: es específico de cada dominio y declara qué roles globales y especializaciones globales están disponibles allí, con etiquetas visibles y notas de adaptación propias del dominio.

Los presets inteligentes de agentes viven en `domains/<domain_id>/agent_presets.json` cuando un dominio los declara. Ese archivo tampoco pertenece a `catalogs/`: define presets operativos por combinación `role_id + specialization_id`, con nombre/id sugeridos, descripción, system prompt, criterios de decisión, sesgos a evitar, sugerencias de proveedor/modelo/temperatura, política de memoria y `paper_seed`.

Crear Agente consume `agent_presets.json` como sugerencia editable cuando el usuario selecciona una combinación Dominio + Rol + Especialización con preset activo. El preset puede autocompletar ID, system prompt y temperatura recomendada, y muestra un resumen operativo compacto. Si el usuario ya editó un campo, la UI no lo pisa silenciosamente.

La memoria `.md` inicial y la generación automática de papers desde presets siguen diferidas.

## Catálogos globales vs catálogos de perfil por dominio

- `catalogs/roles.json`: biblioteca madre de roles profesionales reutilizables entre dominios.
- `catalogs/specializations.json`: biblioteca madre de especializaciones asociadas a esos roles.
- `domains/<domain_id>/profile_catalog.json`: selección y adaptación de roles/especializaciones para un dominio concreto.
- `domains/<domain_id>/agent_presets.json`: biblioteca operativa de presets de agentes para combinaciones habilitadas por el perfil del dominio.

El endpoint `GET /api/domains/{domain_id}/profile-catalog` expone el catálogo de perfiles de un dominio como read-only. Si un dominio no tiene `profile_catalog.json`, la API devuelve `404` claro en lugar de inventar un perfil por defecto.

El endpoint `GET /api/domains/{domain_id}/agent-presets` expone presets activos de un dominio como read-only. `GET /api/domains/{domain_id}/agent-presets/match?role_id=...&specialization_id=...` devuelve un preset exacto si existe. Crear Agente usa el endpoint `match` para sugerir valores editables. Ambos endpoints validan que los IDs referencien combinaciones reales de `profile_catalog.json` y no dependen de `config.DEFAULT_DOMAIN_ID`.

Un `profile_catalog.json` también puede declarar `role_groups`: grupos visuales/mentales propios del dominio para ordenar los roles. Lotería usa esta metadata para recuperar sus capas operativas (`Capa 1: Descubrimiento`, `Capa 2: Validación`, etc.) sin hardcodearlas en el HUD.

Crear Agente ya consume `profile_catalog.json` cuando el dominio seleccionado lo declara. En ese caso, los roles/especializaciones globales no se muestran directamente como UI final: el catálogo de dominio decide la disponibilidad y las etiquetas visibles.

Cuando un preset activo existe para la combinación seleccionada, Crear Agente guarda `profile_preset_id` y `profile_preset_name` como metadata del agente. El system prompt persistido sigue siendo el texto final editado por el usuario.

Para dominios sin `profile_catalog.json`, el HUD usa un fallback temporal con `GET /api/catalogs/roles` y `GET /api/catalogs/specializations`, mostrando una advertencia suave. Si esos catálogos tampoco están disponibles, `specializationMap` queda como fallback legacy aislado hasta que todos los dominios relevantes tengan catálogo propio.

## Lotería

Lotería aparece como el nicho `Análisis de Lotería y Juegos de Azar` dentro de `Oficios y Otros`.

Lotería también aportó semilla conceptual para algunos arquetipos y especializaciones globales, como `Auditor`, `Detector de anomalías`, `Gestor de riesgo`, `Integrador central`, `Auditoría de consistencia`, `Detección de anomalías` y `Gestión de exposición`. Esa inspiración no convierte el catálogo global en un catálogo específico de Lotería.

El primer catálogo de perfil por dominio es `domains/loteria/profile_catalog.json`. Allí los perfiles históricos de Lotería/S.A.A.O.P. se profesionalizan y se mapean a roles/especializaciones globales, por ejemplo `Estadístico integral` → `analista` + `analisis_datos`, `Auditor hostil` → `auditor` + `auditoria_consistencia`, `Cazador de anomalías` → `detector_anomalias` + `deteccion_anomalias`, y `Gestor de bankroll` → `gestor_riesgo` + `gestion_exposicion`.

El primer archivo de presets por dominio es `domains/loteria/agent_presets.json`. Lotería queda como dominio semilla con presets iniciales responsables para descubrimiento, validación, destrucción crítica, riesgo e integración. No hay preset de geometría/estructura espacial dedicado porque esa combinación todavía no existe en `profile_catalog.json`; la cobertura inicial usa `analista + analisis_comparativo` como aproximación documentada.

Eso refleja la regla arquitectónica actual: Lotería es un dominio/nicho más del sistema, no el centro del Core ni una dependencia global.
