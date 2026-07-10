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

---

## ADR-014 — Normalización de metadata de agentes creados con presets

**Estado**: Aceptado

**Contexto**: Los agentes creados con el nuevo flujo (via `/api/agents/create` con presets) necesitan una estructura JSON consistente y trazable. Los agentes legacy existían sin campos de metadata, memory o información de preset aplicado, lo que dificultaba la auditoría y el mantenimiento de la configuración.

**Decisión**: Se introduce un schema técnico mínimo para agentes que incluye bloques `memory` y `metadata`. El helper `core.agent_config_schema.build_agent_config()` construye configuraciones normalizadas con estos bloques. `/api/agents/create` usa este helper para asegurar que todos los agentes nuevos tengan estructura consistente, independientemente de si usan preset o no. `PUT /api/agents/{agent_id}` preserva los campos nuevos y actualiza `updated_at` en metadata. `GET /api/agents/list` expone `memory` y `metadata` en la respuesta.

**Estructura del schema**:
- **Memory**: Bloque con `source_uploaded` (bool), `source_filename` (str|None), `indexed` (bool)
- **Metadata**: Bloque con `schema_version` (str), `created_at` (ISO timestamp), `updated_at` (ISO timestamp), `created_via` (str), `preset_source` (str|None)
- **Preset info**: Campos opcionales `profile_preset_id`, `profile_preset_name`, `preset_applied_at` cuando se aplica un preset

**Compatibilidad**: Agentes legacy sin estos bloques siguen funcionando. El endpoint de listado devuelve `null` para campos faltantes en agentes legacy. El helper `normalize_agent_config()` puede agregar bloques memory y metadata con defaults a agentes legacy si se necesita normalización explícita.

**Evidencia**:
- `core/agent_config_schema.py` — Helper con `build_agent_config()`, `normalize_agent_config()`, `validate_agent_config()`
- `api.py:1267-1289` — `/api/agents/create` usa `build_agent_config()` y agrega metadata
- `api.py:1303-1322` — Actualiza JSON del agente después de indexación de memoria
- `api.py:1490-1572` — `PUT /api/agents/{agent_id}` preserva campos nuevos y actualiza `updated_at`
- `api.py:1463-1464` — `GET /api/agents/list` incluye `memory` y `metadata` en respuesta

**Alcance**: Esta decisión normaliza la estructura técnica de agentes creados con el nuevo flujo, pero no modifica papers, memoria `.md`, runtime de agentes ni presets existentes. Los tests unitarios en `tests/test_agent_config_schema.py` validan el helper/schema.

---

## ADR-015 — Generar paper inicial desde preset al crear agente

**Estado**: Aceptado

**Contexto**: Después de normalizar la estructura de agentes con presets y metadata, el siguiente paso es usar el campo `paper_seed` del preset para generar un paper inicial automáticamente al crear un agente con preset. Los papers existentes deben seguir funcionando, y no se genera paper para agentes creados sin preset (pero se crea un paper básico para compatibilidad legacy).

**Decisión**: Se introduce `core.agent_paper_schema.py` con helpers para construir papers desde presets y escribirlos en la carpeta correcta del dominio (`domains/<domain_id>/agents/papers/`). `/api/agents/create` usa este helper:
1. Si `profile_preset_id` viene y existe, valida que el preset tenga `paper_seed`
2. Construye el paper inicial desde `paper_seed`, `agent_config` y `domain_metadata`
3. Guarda el paper en la carpeta del dominio (fallando si ya existe un paper para ese agent_id)
4. Agrega un bloque `paper` en la config del agente con `created`, `source`, `created_at`, `schema_version`
5. Si falla la creación del paper, no se crea el agente (rollback)

**Estructura del paper inicial**:
- **Nuevo schema**: `schema_version`, `agent_id`, `domain_id`, `source`, `profile_preset_id`, `profile_preset_name`, `identity`, `role`, `specialization_id`, `specialization_name`, `short_description`, `operating_style`, `learning_focus`, `decision_criteria`, `avoid`, `memory_policy`, `domain_context`, `system_prompt_snapshot`, `created_at`, `updated_at`, `history`
- **Campos legacy**: Se incluyen `agente_id`, `dominio_id`, `rol`, `identidad`, `instrucciones_dominio`, `reglas_clave`, `lecciones_aprendidas`, `errores_a_evitar`, `estilo_respuesta`, `fecha_creacion` para compatibilidad con `runtime_json_agent.py`

**Compatibilidad**:
- Agentes legacy sin bloque `paper` siguen funcionando
- Papers legacy existentes se siguen leyendo sin modificar
- `runtime_json_agent.py` no requiere cambios (usa campos legacy)
- Agentes creados sin preset reciben un paper básico para mantener compatibilidad con tests y scripts antiguos

**Evidencia**:
- `core/agent_paper_schema.py` — `build_initial_paper_from_preset()`, `get_domain_agent_paper_path()`, `write_initial_agent_paper()`
- `core/agent_config_schema.py` — Actualizado para agregar campo `paper` en `build_agent_config()` y `normalize_agent_config()`
- `api.py:1291-1320` — Integración en `/api/agents/create` para generar y guardar paper
- `tests/test_agent_config_schema.py` — Tests para el helper/schema de papers

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `core/agent_paper_schema.py`: **Core** — Funcionalidad genérica para crear papers desde presets, independiente de dominio
- Papers generados en `domains/<domain_id>/agents/papers/`: **Agente** — Identidad de un agente específico del dominio
- `paper_seed` en `domains/<domain_id>/agent_presets.json`: **Dominio** — Semilla de identidad específica del dominio

**Alcance diferido**: No se integra memoria `.md`, no se llama a LLM para generar papers, no se regeneran papers existentes, no se modifica `mejorar_papers.py`, no se modifica `runtime_json_agent.py` (excepto si fuera estrictamente necesario para compatibilidad, lo que no fue el caso).

---

## ADR-016 — Memoria `.md` opcional como enriquecimiento determinístico del paper inicial

**Estado**: Aceptado

**Contexto**: Después de generar papers iniciales desde presets, el siguiente paso es integrar la memoria `.md` opcional que el usuario puede subir al crear un agente. La memoria debe enriquecer el paper, pero no reemplazar el preset ni el paper_seed, y no debe llamar a un LLM para resumir ni generar contenido creativo.

**Decisión**:
1. Si el usuario sube una memoria `.md` al crear un agente con preset, se lee el contenido como texto plano (sin LLM)
2. Se agrega un bloque `memory_enrichment` al paper con:
   - `applied`: bool (true si hubo memoria)
   - `source`: "uploaded_md"
   - `source_filename`: nombre del archivo
   - `title`: título extraído del primer encabezado `#` (si existe)
   - `sections_detected`: lista de encabezados `#` y `##`
   - `content_excerpt`: extracto del contenido (truncado a 6000 caracteres)
   - `truncated`: bool (true si el contenido excedió 6000 caracteres)
   - `original_char_count`: int (longitud original del contenido)
   - `stored_char_count`: int (longitud del extracto guardado)
   - `applied_at`: ISO timestamp
3. Se agrega un evento `memory_enrichment_applied` al `history` del paper
4. El bloque `memory` del JSON del agente se actualiza con `paper_enriched` (bool), `paper_enrichment_applied_at` (ISO timestamp) y `paper_enrichment_reason` (str | None, para casos sin preset)
5. Si el usuario sube memoria pero no hay preset, `paper_enriched` es false y `paper_enrichment_reason` es "no_profile_preset"

**Reglas clave**:
- No se usa LLM ni se genera contenido creativo
- No se reemplaza el preset ni el paper_seed
- No se modifica `runtime_json_agent.py` ni `mejorar_papers.py`
- No se regeneran papers existentes
- No se guarda el contenido completo de la memoria en el JSON del agente ni en el paper (solo el extracto)

**Estructura**:
- `core/agent_paper_schema.py`: Actualizado con `_parse_markdown_memory()` y `build_initial_paper_from_preset()` acepta `memory_source` opcional
- `core/agent_config_schema.py`: Actualizado para agregar campos `paper_enriched`, `paper_enrichment_applied_at` y `paper_enrichment_reason` al bloque `memory`
- `api.py`: Actualizado para leer el contenido de la memoria antes de construir el paper, pasarla al helper y actualizar el JSON del agente

**Compatibilidad**:
- Papers sin `memory_enrichment` siguen funcionando
- Agentes legacy sin campos `paper_enriched` en el bloque `memory` siguen funcionando
- `normalize_agent_config()` agrega los campos faltantes con valores predeterminados

**Evidencia**:
- `core/agent_paper_schema.py:12-33` — `_parse_markdown_memory()` para extraer título y secciones
- `core/agent_paper_schema.py:36-131` — `build_initial_paper_from_preset()` actualizado para manejar `memory_source`
- `core/agent_config_schema.py:31-33` — `build_agent_config()` acepta campos de paper enrichment
- `core/agent_config_schema.py:136-163` — `normalize_agent_config()` agrega campos faltantes
- `api.py:1275-1290` — Lee contenido de memoria antes de construir paper
- `api.py:1321-1346` — Construye paper con memoria y actualiza config del agente
- `tests/test_agent_config_schema.py:172-362` — Tests para la nueva funcionalidad

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `core/agent_paper_schema.py` (actualizado): **Core** — Funcionalidad genérica para enriquecer papers con memoria, sin dependencia de dominio
- `core/agent_config_schema.py` (actualizado): **Core** — Schema normalizado para agentes, sin dependencia de dominio
- `memory_source` (contenido de memoria cargada por el usuario): **Agente** — Información específica de un agente
- Papers enriquecidos en `domains/<domain_id>/agents/papers/`: **Agente** — Identidad enriquecida de un agente específico

---

## ADR-017 — Recomendación inteligente de provider/model por perfil de agente

**Estado**: Aceptado

**Contexto**: Los agentes pueden elegir provider/model manualmente, pero IA_CORE no recomienda qué modelo conviene según el perfil del agente. El usuario tiene hardware local limitado (Ryzen 7 7730U, 16GB RAM, sin GPU), por lo que Ollama/local puede servir para agentes livianos pero no como default operativo para agentes pesados.

**Decisión**: Se introduce `core/model_recommendation.py` como módulo Core que provee recomendaciones de provider/model basadas en reglas determinísticas (sin LLM). Las recomendaciones consideran dominio, rol, especialización, carga cognitiva esperada, requerimientos de razonamiento y hardware local disponible. La recomendación es una sugerencia editable, NO una imposición.

**Reglas de clasificación**:
- **Workload heavy/critical** (auditor, simulador, integrador_central, gestor_riesgo): `cloud_preferred`, razonamiento alto
- **Workload medium** (analista, critico, investigador): `cloud_preferred` o cloud/local según disponibilidad
- **Workload light** (archivista, comunicador): `local` permitido si hay modelo chico disponible

**Perfil de hardware local**: Flexible y configurable. Prioridad: 1) `config/hardware_profile.json` si existe, 2) autodetección básica (CPU, RAM, GPU vía nvidia-smi en Windows), 3) fallback seguro. El perfil incluye `cpu`, `ram_gb`, `gpu`, `gpu_name`, `local_mode` ("limited", "capable", "high_end") y `source` ("manual_config", "autodetect", "fallback"). Si hardware es limitado y workload es heavy/critical, no se recomienda local como primera opción.

**Compatibilidad modelo/hardware**: Capa de protección que evalúa si un modelo específico es compatible con el hardware local. Valores: `compatible` (modelo funciona bien), `warning` (modelo puede funcionar pero con limitaciones), `blocked` (modelo no recomendado para este hardware), `cloud_available` (cloud no depende de hardware local), `unknown` (no se puede determinar). Cloud providers siempre son `cloud_available` porque la inferencia corre en cloud. Local providers se evalúan según tamaño del modelo (small/medium/large) y `local_mode` del hardware. Esta capa protege al usuario de elegir modelos no funcionales como opción normal.

**Selección de provider/model**:
1. Si workload heavy/critical: preferir provider cloud operativo (NVIDIA si disponible), fallback local con advertencia
2. Si workload medium: preferir cloud si disponible, si no local chico
3. Si workload light: local chico si disponible, cloud económico si no

No se usan providers demo/placeholders. No se eligen modelos inexistentes en la lista real del provider.

**Backend**: `POST /api/agents/model-recommendation` acepta `domain_id`, `role_id`, `specialization_id`, `profile_preset_id`, `current_provider`, `current_model` y devuelve recomendación con provider, modelo, workload, execution preference, reasoning_need, reason, compatibility, hardware_reason. El endpoint consulta providers disponibles desde supervisor y filtra placeholders/no saludables. `GET /api/system/hardware-profile` expone el perfil de hardware actual con todos sus campos y source. `POST /api/system/model-compatibility` acepta `provider` y `model` y devuelve compatibilidad del modelo seleccionado con el hardware local.

**HUD**: En Crear Agente, al seleccionar dominio, rol y especialización, se muestra un bloque de recomendación con modelo sugerido, workload, motivo, compatibilidad (con color según tipo) y hardware_reason. Botón "Aplicar recomendación" permite aplicar la sugerencia manualmente. Además, inmediatamente debajo del selector de modelo y antes de SYSTEM PROMPT, se muestra un bloque separado de "Compatibilidad del modelo seleccionado" que evalúa el provider/model actualmente elegido por el usuario, con estado (COMPATIBLE/ADVERTENCIA/NO RECOMENDADO/CLOUD/DESCONOCIDO), emoji, color y motivo del hardware. Este bloque es independiente de la recomendación del sistema y puede mostrarse aunque todavía no haya rol/especialización seleccionados. Al abrir Crear Agente, se inicializan los selectores de provider/model y se evalúa automáticamente la compatibilidad. Si no hay provider/model seleccionados, muestra un placeholder visible. En Editar Agente, al abrir un agente existente, se muestra recomendación si el provider/model actual parece subóptimo, sin cambiar automáticamente sin acción del usuario. La compatibilidad se recalcula cuando cambian: provider, modelo (obligatorios), y opcionalmente al cambiar dominio, rol o especialización.

**Regla de no pisado**: La UI mantiene flags de campos tocados. Si el usuario ya cambió provider/model manualmente, no se pisa su elección. La recomendación es solo una sugerencia.

**Evidencia**:
- `core/model_recommendation.py` — Helper con `classify_agent_model_need()`, `recommend_provider_model()`, `get_hardware_profile()`, `get_default_hardware_profile()`, `_load_hardware_profile_from_config()`, `_autodetect_hardware_profile()`, `_get_fallback_hardware_profile()`, `evaluate_model_compatibility()`, `_classify_model_size()`
- `config/hardware_profile.json` — Archivo de configuración editable para perfil de hardware
- `api.py:1517-1589` — Endpoint `POST /api/agents/model-recommendation` (ahora incluye compatibility y hardware_reason)
- `api.py:1592-1614` — Endpoint `GET /api/system/hardware-profile`
- `api.py:1619-1635` — Endpoint `POST /api/system/model-compatibility` (evalúa compatibilidad del modelo seleccionado)
- `ui/web/index.html:855-872` — Bloques UI de recomendación y compatibilidad en modal de agente (compatibilidad debajo del selector de modelo)
- `ui/web/index.html:1322-1364` — Funciones JS `consultarModelRecommendation()`, `displayModelRecommendation()` (muestra compatibilidad con color)
- `ui/web/index.html:1379-1453` — Funciones JS `clearModelCompatibility()`, `consultarModelCompatibility()`, `displayModelCompatibility()` (muestra compatibilidad del modelo seleccionado con emoji y texto)
- `ui/web/index.html:2373-2398` — Event listeners para recalcular compatibilidad al cambiar campos
- `tests/test_model_recommendation.py` — Tests para clasificación, hardware flexible, selección de provider/model, compatibilidad modelo/hardware

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `core/model_recommendation.py`: **Core** — Funcionalidad genérica de recomendación, independiente de dominio
- Reglas específicas de Lotería (auditor, simulador, etc.): **Dominio** — Lógica específica dentro del helper Core
- Perfil de hardware local: **Patrimonio compartido** — Configuración de hardware del usuario, reusable entre dominios
- Recomendaciones aplicadas a agentes: **Agente** — Elección específica de un agente

**Alcance diferido**: No se modifican masivamente agentes existentes, no se toca `agent_presets.json`, no se toca `profile_catalog.json`, no se modifica `runtime_json_agent.py`, no se modifica `mejorar_papers.py`, no se avanza a Prompt 13.

**Deuda UI pendiente**: Hacer visible de forma confiable en HUD la compatibilidad del modelo seleccionado. El backend y los endpoints existen (`POST /api/system/model-compatibility`), pero la representación visual queda diferida para una fase posterior de refinamiento UI. La capa backend de compatibilidad modelo/hardware queda implementada y testeada, pero la visualización HUD del semáforo de compatibilidad queda en stand by porque el bloque no muestra el estado real de forma confiable en la verificación manual.

**Deuda futura — Validación cross-platform real**: La arquitectura de hardware_profile y compatibilidad modelo/hardware debe mantenerse preparada para funcionar en distintos entornos: Windows local, Linux, macOS, Docker/contenedores, servidores, equipos con GPU dedicada, equipos sin GPU, equipos con RAM limitada, equipos con RAM alta. En esta fase NO se certifica multi-sistema. La validación real queda diferida para una fase futura.

---

## ADR-018 — Resolución de papers por dominio: `mejorar_papers.py` deja de pertenecer a Lotería

**Estado**: Aceptado

**Contexto**: `mejorar_papers.py` ya aceptaba `domain_id` como parámetro opcional, pero la función `regenerar_todos_los_papers()` tenía una lista hardcodeada de agentes de Lotería sin documentar explícitamente su naturaleza legacy. Tampoco existía cobertura de test que validara el comportamiento multi-dominio, la creación correcta de agentes en dominios temporales o la no contaminación entre dominios.

**Decisión**:

1. **`mejorar_papers.py` es Core**, no una utilidad del dominio Lotería. La resolución de rutas de papers por dominio pertenece a Core; el contenido semántico de cada paper pertenece al Agente; la carpeta que lo contiene pertenece al Dominio.

2. **Ruta canónica invariable**: `domains/<domain_id>/agents/papers/<agent_id>_paper.json`. `mejorar_paper()` siempre resuelve la ruta a través de `core/domain_registry.get_domain_agents_papers_dir(domain_id)` cuando se pasa `domain_id` explícito, y nunca usa `config.AGENTS_PAPERS_DIR` como destino universal.

3. **`regenerar_todos_los_papers()` es explícitamente legacy-Lotería**: La función lleva docstring que la identifica como compatibilidad con la lista histórica de agentes Lotería. El flujo genérico recomendado para nuevos dominios es llamar `mejorar_paper(agent_id, domain_id=<mi_dominio>, usar_llm=False)` directamente.

4. **Corrección de bug**: `mejorar_paper()` inicializaba `agente_id = "unknown"` cuando no había paper previo. La condición `final.get("agente_id") or agente_id` no sobreescribía `"unknown"` porque el string es truthy. Corregido a asignación directa `final["agente_id"] = agente_id`.

5. **No se crea `core/agent_paths.py`**: Los helpers de resolución de rutas ya existen en `core/domain_registry.py` (`get_domain_agents_papers_dir`, `get_domain_agents_config_dir`, `resolve_agent_json`). Un módulo separado sería redundancia sin valor.

6. **`api.py` no requiere cambios**: `/api/agents/create` usa `write_initial_agent_paper()` y un paper básico inline — ambos ya resuelven rutas por `domain_id` correctamente desde el Prompt 15.

**Evidencia**:
- `mejorar_papers.py` — Docstring de módulo expandido con ejemplos de uso y ruta canónica; `regenerar_todos_los_papers()` marcada como legacy-Lotería con instrucciones para el flujo genérico; `final["agente_id"] = agente_id` garantiza el ID correcto incluso al crear paper desde cero
- `tests/test_mejorar_papers_domain.py` — 11 tests en 4 clases: `TestRutaPorDominio` (5), `TestCompatibilidadLoteria` (2), `TestFallbackLegacy` (2), `TestNoHardcodeAGENTS_PAPERS_DIR` (2)
- `tests/test_no_hardcoded_agent_paths.py` — Ya cubría que `mejorar_papers.py` no use `config.AGENTS_PAPERS_DIR` directamente como destino de guardado

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `mejorar_papers.py` (lógica de resolución de rutas): **Core** — Funcionalidad genérica para mejorar papers en cualquier dominio
- `regenerar_todos_los_papers()` (lista hardcodeada): **Dominio Lotería** — Legacy; contenido acoplado a la lista histórica de Lotería, documentado como tal
- Papers mejorados en `domains/<domain_id>/agents/papers/`: **Agente** — Identidad actualizada de un agente específico del dominio
- `config.AGENTS_PAPERS_DIR`: Permanece como compatibilidad legacy, nunca como destino operativo del flujo genérico

**Alcance diferido**: No se crea endpoint de regeneración de papers. No se tocan papeles reales masivamente. No se modifica `runtime_json_agent.py`. No se avanza a Prompt 14.

**Alcance de la validación futura**: Una fase futura deberá comprobar:
- A. Perfil de hardware: carga desde config/hardware_profile.json, autodetección básica, fallback seguro, local_mode correcto, no exposición de datos sensibles.
- B. Endpoints: GET /api/system/hardware-profile, POST /api/system/model-compatibility, POST /api/agents/model-recommendation.
- C. Providers/modelos: Ollama/local en cada sistema donde aplique, cloud providers independientemente del hardware local, placeholders no operativos ignorados.
- D. Compatibilidad modelo/hardware: modelos locales chicos, modelos locales medianos/pesados, cloud_available, warning/blocked, unknown/fallback.
- E. Degradación segura: si no se puede detectar hardware, no romper; si no existe nvidia-smi, no romper; si no existe lspci, no romper; si corre en Docker con recursos limitados visibles, usar esos recursos o fallback.

**Regla de diseño cross-platform**: La detección de hardware debe ser best-effort. Nunca debe ser requisito para arrancar IA_CORE. Si la detección falla: usar config manual si existe; si no, fallback seguro; informar limitación; no bloquear el sistema salvo que no haya ningún provider/model operativo.

**No probar ahora**: No se ejecutan pruebas reales en Linux/macOS/Docker en esta fase. Esta tarea solo registra la deuda y deja preparada la arquitectura documentalmente.
