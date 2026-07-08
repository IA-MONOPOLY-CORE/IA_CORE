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
- roles/arquetipos profesionales globales en `roles.json`.

Los roles globales describen funciones cognitivas u operativas reutilizables, como `Analista`, `Auditor`, `Optimizador` o `Gestor de riesgo`. No representan todavía los roles habilitados para un dominio específico y no reemplazan el selector actual de Crear Agente.

La conexión Dominio → Roles, las especializaciones, presets inteligentes de agentes, memoria `.md` inicial y papers automáticos se implementarán en prompts posteriores.

## Lotería

Lotería aparece como el nicho `Análisis de Lotería y Juegos de Azar` dentro de `Oficios y Otros`.

Lotería también aportó semilla conceptual para algunos arquetipos globales, como `Auditor`, `Detector de anomalías`, `Gestor de riesgo`, `Integrador central` y `Archivista`. Esa inspiración no convierte el catálogo global en un catálogo específico de Lotería.

Eso refleja la regla arquitectónica actual: Lotería es un dominio/nicho más del sistema, no el centro del Core ni una dependencia global.
