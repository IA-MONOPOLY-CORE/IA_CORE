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

Los presets inteligentes de agentes, memoria `.md` inicial y papers automáticos se implementarán en prompts posteriores.

## Catálogos globales vs catálogos de perfil por dominio

- `catalogs/roles.json`: biblioteca madre de roles profesionales reutilizables entre dominios.
- `catalogs/specializations.json`: biblioteca madre de especializaciones asociadas a esos roles.
- `domains/<domain_id>/profile_catalog.json`: selección y adaptación de roles/especializaciones para un dominio concreto.

El endpoint `GET /api/domains/{domain_id}/profile-catalog` expone el catálogo de perfiles de un dominio como read-only. Si un dominio no tiene `profile_catalog.json`, la API devuelve `404` claro en lugar de inventar un perfil por defecto.

Crear Agente todavía no consume `profile_catalog.json`: los selectores hardcodeados actuales del HUD y `specializationMap` se mantienen hasta el prompt que conecte formalmente este catálogo.

## Lotería

Lotería aparece como el nicho `Análisis de Lotería y Juegos de Azar` dentro de `Oficios y Otros`.

Lotería también aportó semilla conceptual para algunos arquetipos y especializaciones globales, como `Auditor`, `Detector de anomalías`, `Gestor de riesgo`, `Integrador central`, `Auditoría de consistencia`, `Detección de anomalías` y `Gestión de exposición`. Esa inspiración no convierte el catálogo global en un catálogo específico de Lotería.

El primer catálogo de perfil por dominio es `domains/loteria/profile_catalog.json`. Allí los perfiles históricos de Lotería/S.A.A.O.P. se profesionalizan y se mapean a roles/especializaciones globales, por ejemplo `Estadístico integral` → `analista` + `analisis_datos`, `Auditor hostil` → `auditor` + `auditoria_consistencia`, `Cazador de anomalías` → `detector_anomalias` + `deteccion_anomalias`, y `Gestor de bankroll` → `gestor_riesgo` + `gestion_exposicion`.

Eso refleja la regla arquitectónica actual: Lotería es un dominio/nicho más del sistema, no el centro del Core ni una dependencia global.
