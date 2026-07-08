# Architecture Decision Records (ADRs)

## ADR-001 — El Core jamás conoce un dominio

**Estado**: Aceptado

**Contexto**: El sistema debe permitir múltiples dominios sin que el Core tenga dependencias directas sobre ninguno de ellos. Esto facilita la escalabilidad y el mantenimiento.

**Decisión**: El Core inyecta funcionalidad específica de dominio (como scoring) mediante parámetros opcionales con import perezoso y fallback genérico, en lugar de importar directamente módulos de dominio.

**Evidencia**: `core/supervisor.py:126-134` — `_get_default_score_response_fn()` hace import perezoso de `domains.loteria.scoring.score_response` con fallback a `dummy_score()` si el dominio no existe:
```python
@staticmethod
def _get_default_score_response_fn() -> Callable:
    try:
        from domains.loteria.scoring import score_response
        return score_response
    except ImportError:
        def dummy_score(*args, **kwargs):
            from dataclasses import dataclass
```

**Evidencia adicional — separación de memoria (ADR-001)**:
- ¿Lo que quedó en `core/memoria_perpetua.py` después de este cambio es 100% Core? **Sí.** Sus APIs reciben diccionarios de metadata con claves arbitrarias y no contienen referencias a sorteos ni a Lotería.
- `domains/loteria/memoria_loteria.py` es el adaptador de **Dominio** que conserva las firmas con `sorteo` y traduce ese concepto a `{"sorteo": valor}` antes de llamar al Core.
- ¿Lo que se movió a `domains/loteria/database_loteria.py` es Dominio? **Sí.** Su esquema y sus operaciones modelan sorteos, debates por sorteo, intervenciones, U-Score, acuerdo y métricas V19, todos conceptos específicos de Lotería.
- En cumplimiento del ADR-001, `api.py` consume la base desde `domains.loteria.database_loteria` y `memory/database.py` dejó de existir en la carpeta genérica.

---

## ADR-002 — El agente es la principal unidad de ejecución inteligente del sistema

**Estado**: Aceptado

**Contexto**: El sistema necesita una unidad de ejecución inteligente bien definida que sea reutilizable entre dominios, pero sin ser la única unidad posible (deja espacio para schedulers, pipelines o automatizaciones sin agente en el futuro).

**Decisión**: Los agentes operan por ID independiente del dominio, con su configuración cargada dinámicamente desde JSON. El sistema no asume que toda ejecución inteligente debe pasar por un agente.

**Evidencia**: 
- `agents/runtime_json_agent.py:13-19` — `RuntimeJsonAgent` carga identidad desde JSON sin referencia a dominio específico
- `agents/manager.py:24-40` — `AgentManager` opera por `_config_dir` y IDs de agente, sin dependencia de lógica de dominio

---

## ADR-003 — Los papers (identidad de agentes) pertenecen al dominio hasta que exista una identidad completamente genérica reutilizable entre dominios

**Estado**: Aceptado — papers movidos a `domains/loteria/agents/papers/` en esta pasada

**Contexto**: Los papers de agentes contienen términos 100% específicos de Lotería/S.A.A.O.P. (U-Score, CAZADOR, ESPEJO, cobertura combinatoria, framework V19). Originalmente residían en `agents/papers/` (directorio genérico del sistema), lo que causaba contaminación de dominio.

**Decisión**: Los papers se mueven a `domains/loteria/agents/papers/` para reflejar su naturaleza específica del dominio Lotería. Si en el futuro se agregan más dominios, cada uno tendrá sus propios papers en `domains/{dominio}/agents/papers/`. Solo si se crea una identidad genérica reutilizable entre dominios, se podría considerar una capa compartida.

**Evidencia**: `domains/loteria/agents/papers/*.json` — 6 archivos de paper movidos desde `agents/papers/` (ej: `gpt_auditor_paper.json`, `estadistico_integral_paper.json`, `viejo_lobo_rey_paper.json`) ahora residen en el directorio específico del dominio Lotería

---

## ADR-004 — Toda nueva herramienta, agente o módulo de memoria debe clasificarse antes de implementarse: Core, Dominio, Agente o Patrimonio compartido

**Estado**: Aceptado, a partir de ahora

**Contexto**: El proyecto ha crecido orgánicamente sin una clasificación explícita de componentes. Esto ha llevado a ambigüedades sobre dónde debe residir cada nueva funcionalidad.

**Decisión**: Antes de implementar cualquier nuevo componente, debe clasificarse explícitamente en una de estas cuatro categorías:
- **Core**: Funcionalidad genérica independiente de dominio (ej: supervisor, debate, orquestación)
- **Dominio**: Funcionalidad específica de un dominio de negocio (ej: scoring de Lotería)
- **Agente**: Identidad y comportamiento de un agente específico (papers, configuración JSON)
- **Patrimonio compartido**: Utilidades reutilizables entre dominios pero no parte del Core (ej: herramientas genéricas, helpers)

**Evidencia**: Pendiente — esta decisión entra en vigencia a partir de la aprobación de este ADR. Futuros commits deben respetar esta clasificación.

---

**Respuesta a la pregunta de clasificación**: Lo que acabamos de mover (agents/papers/ → domains/loteria/agents/papers/) pasa a pertenecer al **Dominio** (específicamente al dominio Lotería), no al Core, ni a un Agente individual, ni es Patrimonio compartido. Esto confirma la actualización del ADR-003.

---

## ADR-005 — Lotería es un dominio declarado, no una dependencia global para rutas de agentes

**Estado**: Aceptado

**Contexto**: Los agentes JSON y sus papers ya viven bajo `domains/<dominio>/agents/`, pero algunos flujos genéricos seguían usando constantes legacy que apuntaban a Lotería (`config.AGENTS_CONFIG_DIR`, `config.AGENTS_PAPERS_DIR`) o trataban `config.DEFAULT_DOMAIN_ID == "loteria"` como caso especial.

**Decisión**: Los flujos genéricos de creación, edición, borrado y mejora de papers resuelven rutas por `domain_id` mediante `core.domain_registry`. Lotería sigue funcionando, pero como dominio con `domains/loteria/domain.json`, no como destino implícito del Core.

**Compatibilidad**: `config.DEFAULT_DOMAIN_ID`, `config.AGENTS_CONFIG_DIR` y `config.AGENTS_PAPERS_DIR` permanecen como compatibilidad legacy/default Lotería para scripts y pruebas antiguas. No son el patrón para nuevos flujos genéricos.

**Evidencia**:
- `core/domain_registry.py` centraliza `get_domain_dir()`, `get_domain_agents_config_dir()`, `get_domain_agents_papers_dir()`, `get_domain_memory_sources_dir()` y `resolve_agent_json()`.
- `api.py` crea papers básicos en `domains/<domain_id>/agents/papers/` para cualquier dominio y resuelve `PUT/DELETE /api/agents/{agent_id}` por `domain_id` opcional, fallando si el ID es ambiguo.
- `mejorar_papers.py` acepta `domain_id`, `config_path` o `paper_path` y ya no usa `config.AGENTS_PAPERS_DIR` como destino universal.

---

## ADR-006 — `catalogs/` es Patrimonio compartido para creación asistida de dominios

**Estado**: Aceptado

**Contexto**: El sistema necesita una fuente común para sugerir áreas profesionales y nichos al crear dominios, sin convertir ningún dominio existente en default global ni mezclar esta base con roles, especializaciones o presets de agentes.

**Decisión**: Se crea `catalogs/` como Patrimonio compartido. `catalogs/areas.json` define áreas profesionales y `catalogs/niches.json` define nichos iniciales con sugerencias de nombre, descripción e instrucciones para futuros dominios. Lotería se modela como el nicho `Análisis de Lotería y Juegos de Azar` dentro de `Oficios y Otros`.

**Backend**: `core/catalog_registry.py` carga y valida los catálogos, filtra activos por defecto y expone una estructura agrupada para creación de dominios. `GET /api/catalogs/domain-creation` publica esa estructura como endpoint read-only.

**HUD**: El modal Crear Dominio consume el endpoint read-only para ofrecer el flujo Área profesional → Nicho específico. Al elegir un nicho se autocompletan nombre, descripción e instrucciones heredadas, pero el usuario conserva edición manual antes de crear el dominio.

**Metadata de dominio**: Los dominios nuevos pueden persistir `area_profesional_id` y `nicho_id` en `domain.json`, manteniendo `nicho_sugerido` como compatibilidad.

**Alcance diferido**: Roles, especializaciones, presets inteligentes, memoria `.md` inicial y papers automáticos quedan para prompts posteriores.

---

## ADR-007 — Catálogo global de roles/arquetipos profesionales

**Estado**: Aceptado

**Contexto**: Luego de definir áreas profesionales y nichos, IA_CORE necesita una biblioteca madre de roles reutilizables que no dependa de Lotería ni de un dominio particular.

**Decisión**: Se crea `catalogs/roles.json` como Patrimonio compartido. Cada rol describe un arquetipo cognitivo u operativo global con nombre visible, descripción, función cognitiva, usos recomendados, usos a evitar, familia, estado y orden.

**Backend**: `core/catalog_registry.py` carga y valida los roles con `load_roles()` y expone `get_roles_catalog()`. `GET /api/catalogs/roles` publica los roles activos ordenados como endpoint read-only.

**Relación con Lotería**: Los perfiles de Lotería se usan solo como semilla conceptual para algunos arquetipos globales. El catálogo no incluye prompts ni lenguaje específico de Lotería como default global.

**Alcance diferido**: Crear Agente todavía no consume este catálogo. La habilitación Dominio → Roles, especializaciones y presets inteligentes quedan para prompts posteriores.

---

## ADR-008 — Catálogo global de especializaciones profesionales por rol

**Estado**: Aceptado

**Contexto**: Después de crear roles/arquetipos globales, IA_CORE necesita una biblioteca de especializaciones reutilizables que detalle ángulos profesionales asociados a cada rol sin depender de un dominio particular.

**Decisión**: Se crea `catalogs/specializations.json` como Patrimonio compartido. Cada especialización pertenece a un `role_id` existente de `catalogs/roles.json` y define nombre, descripción, enfoque, usos recomendados, usos a evitar, estado y orden.

**Backend**: `core/catalog_registry.py` carga, valida y agrupa especializaciones mediante `load_specializations()`, `get_specializations_by_role()` y `get_specializations_catalog()`. `GET /api/catalogs/specializations` expone el catálogo read-only y acepta `role_id` opcional para filtrar por rol.

**Relación con Lotería**: Los perfiles de Lotería aportan inspiración conceptual, pero el catálogo evita prompts o lenguaje específico de Lotería como default global.

**Alcance diferido**: Crear Agente todavía no consume este catálogo. La conexión Dominio → Roles → Especializaciones y los presets inteligentes quedan para prompts posteriores.

---

## ADR-009 — Catálogo de perfiles habilitados por dominio

**Estado**: Aceptado

**Contexto**: Los catálogos globales de roles y especializaciones son patrimonio compartido, pero cada dominio necesita declarar qué subconjunto usa y cómo se nombran/adaptan esos perfiles en su propio lenguaje operativo.

**Decisión**: Se introduce `domains/<domain_id>/profile_catalog.json` como catálogo específico de dominio. El archivo declara roles habilitados, especializaciones habilitadas por rol, etiquetas visibles, orden y notas de adaptación. Cada `role_id` debe existir en `catalogs/roles.json` y cada `specialization_id` debe existir en `catalogs/specializations.json` y pertenecer al rol global indicado.

**Backend**: `core/domain_registry.py` carga y valida estos catálogos mediante `load_domain_profile_catalog()`, `validate_domain_profile_catalog()` y `get_domain_profile_catalog()`. `GET /api/domains/{domain_id}/profile-catalog` expone el catálogo read-only; si el dominio no tiene `profile_catalog.json`, responde `404`.

**Relación con Lotería**: `domains/loteria/profile_catalog.json` es el primer dominio semilla. Los perfiles históricos de Lotería/S.A.A.O.P. se mapearon a roles/especializaciones globales con lenguaje profesional, sin copiar promesas irreales ni convertir Lotería en default global.

**Alcance diferido**: Crear Agente todavía no consume este catálogo. No se modifican roles hardcodeados del HUD, `specializationMap`, presets, memoria `.md`, papers ni `mejorar_papers.py`.

---

## ADR-010 — Crear Agente consume perfiles del dominio activo

**Estado**: Aceptado

**Contexto**: El modal Crear Agente todavía usaba roles y especializaciones hardcodeados en el HUD. Eso impedía que cada dominio controlara qué perfiles estaban disponibles y mezclaba el diseño histórico de Lotería con futuros dominios.

**Decisión**: Crear Agente carga `GET /api/domains/{domain_id}/profile-catalog` al abrir el modal y cada vez que cambia el dominio seleccionado. El selector de rol se puebla con `roles[].nombre_visible` y `roles[].role_id`; el selector de especialización se puebla con las `specializations` del rol elegido.

**Persistencia**: `/api/agents/create` acepta `specialization_id` opcional y lo guarda como metadata estructurada del agente junto con `role` y `domain_id`. Si el dominio tiene `profile_catalog.json`, el backend valida que el rol esté habilitado y que la especialización pertenezca a ese rol. Los agentes existentes sin `specialization_id` siguen siendo válidos.

**Fallback temporal**: Si un dominio todavía no tiene `profile_catalog.json`, el HUD muestra una advertencia y usa temporalmente los catálogos globales `GET /api/catalogs/roles` y `GET /api/catalogs/specializations`. Si esos catálogos no cargan, conserva `specializationMap` como fallback legacy aislado. Ese fallback no convierte a Lotería en default global.

**Alcance diferido**: Esta decisión no crea presets, no autocompleta system prompt, no genera memoria `.md` y no modifica papers ni `runtime_json_agent.py`. Los presets Rol + Especialización quedan para prompts posteriores.

---

## ADR-011 — Los dominios pueden declarar grupos visuales de roles

**Estado**: Aceptado

**Contexto**: Al conectar Crear Agente a `profile_catalog.json`, Lotería dejó de depender del selector hardcodeado antiguo, pero también perdió la jerarquía mental por capas que organizaba sus perfiles.

**Decisión**: `domains/<domain_id>/profile_catalog.json` puede declarar `role_groups` opcionales. Cada grupo define `id`, `nombre`, `descripcion` y `orden`; cada rol puede referenciarlo con `group_id`. El loader valida grupos, IDs únicos y referencias válidas, pero mantiene compatibilidad con dominios sin grupos.

**HUD**: Crear Agente renderiza `<optgroup>` cuando el catálogo del dominio trae `role_groups`. Si no existen, conserva el selector plano/fallback global. La UI no hardcodea capas de Lotería: lee la jerarquía desde el endpoint genérico `GET /api/domains/{domain_id}/profile-catalog`.

**Relación con Lotería**: `domains/loteria/profile_catalog.json` usa `role_groups` para representar sus capas operativas: Descubrimiento, Validación, Destrucción, Riesgo e Integración.

**Alcance diferido**: No se crean presets, no se autocompleta system prompt y no se modifican memoria `.md`, papers ni runtime.

---

## ADR-012 — Presets operativos de agentes por dominio

**Estado**: Aceptado

**Contexto**: Crear Agente ya conoce el dominio activo, los roles habilitados y las especializaciones disponibles por `profile_catalog.json`, pero todavía no existe una biblioteca operativa que proponga nombre, descripción, system prompt, criterios, sesgos a evitar, política de memoria y semilla de paper para combinaciones concretas.

**Decisión**: Se introduce `domains/<domain_id>/agent_presets.json` como archivo específico de dominio. Cada preset pertenece a una combinación exacta `role_id + specialization_id` declarada en `profile_catalog.json`; no vive en `catalogs/`, no es Core y no convierte a Lotería en default global.

**Backend**: `core/domain_registry.py` carga y valida estos presets mediante `load_domain_agent_presets()`, `validate_domain_agent_presets()`, `get_domain_agent_presets()` y `get_domain_agent_preset()`. El loader valida `schema_version`, `domain_id`, IDs únicos, campos obligatorios, orden, estado activo y que cada combinación exista bajo el rol correcto del `profile_catalog.json` del dominio. Por defecto devuelve solo presets activos y ordenados.

**API**: `GET /api/domains/{domain_id}/agent-presets` expone presets activos como read-only. `GET /api/domains/{domain_id}/agent-presets/match?role_id=...&specialization_id=...` devuelve un preset exacto o `404` claro si no existe. Los endpoints no escriben archivos y no dependen de `config.DEFAULT_DOMAIN_ID`.

**Relación con Lotería**: `domains/loteria/agent_presets.json` es la primera semilla, con presets responsables para descubrimiento, validación, destrucción crítica, riesgo e integración. Se evita lenguaje de promesa, método infalible o resultado asegurado como garantía operativa.

**Alcance diferido original**: En esta etapa inicial Crear Agente todavía no consumía estos presets, no autocompletaba nombre ni system prompt, no creaba agentes automáticamente, no generaba memoria `.md`, no generaba papers desde `paper_seed` y no modificaba `runtime_json_agent.py`, `mejorar_papers.py` ni la UI. El consumo editable desde Crear Agente queda definido en ADR-013.

---

## ADR-013 — Crear Agente aplica presets como sugerencias editables

**Estado**: Aceptado

**Contexto**: Los presets operativos por dominio ya existen y la API puede resolver un preset exacto por `domain_id + role_id + specialization_id`, pero el formulario Crear Agente todavía requería completar manualmente ID y system prompt aun cuando hubiera una combinación predefinida.

**Decisión**: Crear Agente consulta `GET /api/domains/{domain_id}/agent-presets/match` al seleccionar una especialización. Si existe preset activo, lo aplica como sugerencia editable: autocompleta campos no tocados, muestra un bloque informativo y conserva la posibilidad de edición manual. Si no hay preset o el dominio no tiene presets, informa el estado y no bloquea la creación.

**Regla de no pisado**: La UI mantiene flags de campos tocados para ID, system prompt, proveedor y modelo. Un preset solo completa un campo si está vacío o si el usuario todavía no lo editó. Cambiar rol, especialización o dominio limpia el preset actual sin destruir texto escrito.

**Persistencia**: `/api/agents/create` acepta `profile_preset_id` opcional. Si viene, el backend valida que exista en los presets activos del dominio y que corresponda al mismo `role + specialization_id`. El JSON del agente guarda `profile_preset_id`, `profile_preset_name` y `preset_applied_at`; el `system_prompt` guardado sigue siendo el texto final editado por el usuario.

**Alcance diferido**: No se genera paper desde `paper_seed`, no se integra memoria `.md`, no se modifica `runtime_json_agent.py`, no se toca `mejorar_papers.py` y no se crean agentes automáticamente.
