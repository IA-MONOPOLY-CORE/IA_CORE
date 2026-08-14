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

**Alcance diferido**: Se crea endpoint de regeneración de papers en Prompt 14. No se tocan papeles reales masivamente. No se modifica `runtime_json_agent.py`.

---

## ADR-019 — Endpoint de regeneración de paper por agente

**Estado**: Aceptado

**Contexto**: El sistema necesita un endpoint administrativo backend para regenerar el paper de un agente puntual, usando la lógica ya generalizada de `mejorar_papers.py` por dominio. Este prompt agrega backend/API, no UI.

**Decisión**: Crear endpoint `POST /api/agents/{agent_id}/regenerate-paper` que acepta `domain_id` y `usar_llm` en el body JSON, valida que el dominio y agente existen, llama a `mejorar_paper()` con los parámetros correspondientes, y devuelve el paper regenerado con ruta relativa. El endpoint es genérico por dominio y no pertenece a Lotería.

**Backend**: `POST /api/agents/{agent_id}/regenerate-paper` acepta `{"domain_id": "loteria", "usar_llm": false}` y devuelve `{"success": true, "agent_id": "auditor_hostil", "domain_id": "loteria", "paper_path": "domains/loteria/agents/papers/auditor_hostil_paper.json", "changed": true, "message": "Paper regenerado correctamente.", "paper": {...}}`. El endpoint valida domain_id requerido, dominio existente, agente existente, y usar_llm booleano. No expone rutas absolutas del sistema en la respuesta.

**Validaciones**: El endpoint valida que domain_id sea requerido, que el dominio exista, que el agente exista (config JSON), y que usar_llm sea booleano. Si alguna validación falla, devuelve error claro con código HTTP apropiado. No llama LLM salvo que el body lo pida explícitamente (usar_llm=true).

**Integración**: El endpoint llama a `mejorar_paper(agent_id, usar_llm=usar_llm, domain_id=domain_id)` desde `mejorar_papers.py`, que ya está generalizado por dominio. No duplica lógica de regeneración dentro de `api.py`.

**Manejo de errores**: Responde con errores claros para: dominio inexistente, agente inexistente, error al regenerar paper, paper resultante inválido, usar_llm inválido, domain_id faltante. No expone tracebacks crudos al cliente.

**UI**: La UI queda fuera de este prompt. Este prompt solo agrega el endpoint backend.

**Evidencia**:
- `api.py:1827-1908` — Endpoint `POST /api/agents/{agent_id}/regenerate-paper` con validaciones, integración con `mejorar_papers.py`, y manejo de errores
- `tests/test_api_regenerate_paper.py` — 7 tests en 1 clase: `TestEndpointRegeneratePaper` (endpoint exitoso, agente inexistente, dominio inexistente, domain_id faltante, usar_llm default false, no toca papers reales, respuesta no expone path absoluto)

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `api.py` (endpoint): **Core** — Orquestador genérico que llama a `mejorar_papers.py`
- `mejorar_papers.py` (lógica): **Core** — Funcionalidad genérica para mejorar papers en cualquier dominio
- Papers regenerados en `domains/<domain_id>/agents/papers/`: **Agente** — Identidad actualizada de un agente específico del dominio

---

## Cierre del bloque de profesionalización de creación de agentes / presets / papers

**Estado**: Cerrado (Prompt 15)

**Últimos commits relevantes**:
- `01b11b1` — Generalizar mejorar_papers.py por dominio (Prompt 13)
- `59cdff0` — Limpieza final y cierre real de Prompt 13
- `a2faa08` — Agregar endpoint para regenerar paper de agente (Prompt 14)

**Estado de endpoints nuevos**:
- `POST /api/agents/{agent_id}/regenerate-paper` — Backend listo para regeneración de paper por agente y dominio
- `POST /api/agents/create` — Soporta presets, papers iniciales y enriquecimiento con memoria .md
- `GET /api/system/hardware-profile` — Perfil de hardware configurable/detectable
- `POST /api/system/model-compatibility` — Compatibilidad modelo/hardware backend
- `POST /api/agents/model-recommendation` — Recomendación provider/model por perfil

**Tests finales**:
- Suite completa: 219 passed, 4 deselected, 5 warnings
- Tests focalizados: test_agent_config_schema (19), test_model_recommendation (40), test_mejorar_papers_domain (11), test_api_regenerate_paper (7)

**Deudas no bloqueantes**:
- Semáforo/compatibilidad visual HUD en stand by (registrado en ADR-017)
- Validación cross-platform futura (registrada en ADR-017)
- UI de regeneración de paper queda fuera de este bloque (para prompt posterior)

**Confirmaciones arquitectónicas**:
- Lotería quedó como dominio y no como Core (ADR-001, ADR-003)
- Papers se resuelven por dominio mediante `core/domain_registry.py` (ADR-018)
- Regeneración de paper ya tiene endpoint backend (ADR-019)
- `mejorar_papers.py` es Core genérico multi-dominio (ADR-018)
- `regenerar_todos_los_papers()` es explícitamente legacy-Lotería (ADR-018)
- No hay hardcodes nuevos de Lotería en Core (solo imports perezosos con fallback)
- Tests no modifican papers reales (usan tmp_path/monkeypatch)

**Alcance de la validación futura**: Una fase futura deberá comprobar:
- A. Perfil de hardware: carga desde config/hardware_profile.json, autodetección básica, fallback seguro, local_mode correcto, no exposición de datos sensibles.
- B. Endpoints: GET /api/system/hardware-profile, POST /api/system/model-compatibility, POST /api/agents/model-recommendation.
- C. Providers/modelos: Ollama/local en cada sistema donde aplique, cloud providers independientemente del hardware local, placeholders no operativos ignorados.
- D. Compatibilidad modelo/hardware: modelos locales chicos, modelos locales medianos/pesados, cloud_available, warning/blocked, unknown/fallback.
- E. Degradación segura: si no se puede detectar hardware, no romper; si no existe nvidia-smi, no romper; si no existe lspci, no romper; si corre en Docker con recursos limitados visibles, usar esos recursos o fallback.

**Regla de diseño cross-platform**: La detección de hardware debe ser best-effort. Nunca debe ser requisito para arrancar IA_CORE. Si la detección falla: usar config manual si existe; si no, fallback seguro; informar limitación; no bloquear el sistema salvo que no haya ningún provider/model operativo.

**No probar ahora**: No se ejecutan pruebas reales en Linux/macOS/Docker en esta fase. Esta tarea solo registra la deuda y deja preparada la arquitectura documentalmente.

---

## ADR-020 — La Biblioteca Profesional es patrimonio compartido global y los dominios heredan perfiles compatibles

**Estado**: Propuesto
**Fecha**: 2026-07-10
**Prompt**: 16

**Contexto**:
IA_CORE evolucionó desde un dominio específico (Lotería) a un framework multi-dominio. Los perfiles profesionales actuales están fuertemente influenciados por Lotería y no hay una estructura global reutilizable. El sistema actual obliga a duplicar presets por dominio de forma innecesaria.

**Decisión**:
- Los perfiles profesionales no nacen dentro de un dominio puntual.
- Se definen globalmente en `catalogs/professional_profiles.json`.
- Los dominios seleccionan o heredan perfiles compatibles vía `profile_catalog.json`.
- Todo perfil usable debe tener preset_seed y paper_seed.
- Toda recomendación de modelo debe considerar carga cognitiva, tipo de tarea y hardware.
- Los dominios pueden tener overrides, pero no deben duplicar la definición global sin necesidad.

**Consecuencias**:
- Permite escalar a múltiples dominios sin duplicar definiciones.
- Facilita la creación de nuevos dominios reusando perfiles existentes.
- Mantiene consistencia en la definición de roles y especializaciones.
- Permite evolucionar la biblioteca global sin impactar dominios existentes.

**Clasificación Patrimonio/Core/Dominio/Agente**:
- `catalogs/professional_profiles.json`: **Patrimonio compartido** — Definiciones globales reusables
- `catalogs/professional_archetypes.json`: **Patrimonio compartido** — Modelos psicológicos/cognitivos
- `catalogs/team_templates.json`: **Patrimonio compartido** — Configuraciones de equipos
- `catalogs/profile_model_policies.json`: **Patrimonio compartido** — Políticas de ejecución
- `domains/*/profile_catalog.json`: **Dominio** — Hereda y adapta perfiles globales
- `domains/*/agent_presets.json`: **Dominio** — Hereda y adapta presets globales
- Papers generados: **Agente** — Identidad específica de cada agente operativo

## ADR-021 — Catálogos de áreas/nichos soportan metadatos operativos sin romper compatibilidad

**Estado**: Aceptado
**Fecha**: 2026-07-10
**Prompt**: 17.1

**Contexto**:
El reporte del Prompt 17 detectó que el catálogo actual (areas.json, niches.json) no soporta metadatos operativos necesarios para la Biblioteca Profesional Global a escala. Para cargar 106 nichos nuevos con trazabilidad operativa, el loader necesita soportar campos como status, complexity, operational_priority, model_policy_need, expected_profile_types y operationalization_contract.

**Decisión**:
- Los catálogos globales de áreas y nichos pueden contener metadatos operativos opcionales.
- Los campos nuevos son opcionales y no se requieren para los JSON existentes.
- El loader `core/catalog_registry.py` valida los campos si están presentes pero no los exige.
- Los catálogos actuales no requieren migración y siguen funcionando sin cambios.
- Los valores válidos para cada campo están definidos como constantes en el loader.
- El status `active` no debe usarse como decoración; requiere trazabilidad operativa completa.

**Consecuencias**:
- Permite cargar expansión de nichos con metadatos operativos sin romper compatibilidad.
- Facilita trazabilidad hacia perfiles profesionales, presets, papers y políticas de modelo.
- Mantiene compatibilidad hacia atrás con los 94 nichos existentes.
- Prepara el terreno para Prompt 17.2 (carga de expansión real).

**Campos Soportados**:
- `status`: proposed / draft / active / deprecated
- `complexity`: low / medium / high / critical
- `operational_priority`: low / medium / high / critical
- `model_policy_need`: local_ok / auto / cloud_preferred / cloud_required / critical_reasoning_required
- `compatible_business_scales`: micro / local_business / freelancer / pyme / company / enterprise / department / research_team / experimental_domain
- `tags`, `typical_needs`, `expected_profile_types`, `likely_professional_profiles`, `required_capabilities`, `possible_team_templates`, `activation_requirements`: list[str]
- `operationalization_contract`: object con estructura específica

---

## ADR-022 — Ningún perfil o preset usable puede quedar sin trazabilidad operativa completa

**Estado**: Aceptado

**Prompt**: 17.1.1

**Contexto**:
La auditoría de Prompt 17.1.1 detectó que 19 combinaciones role+specialization en `profile_catalog.json` no tenían preset operativo correspondiente. Esto violaba la regla de que todo elemento seleccionable para crear agentes debe tener trazabilidad completa. Sin corrección, estos profiles aparecerían como opciones usables pero no podrían crear agentes operativos.

**Decisión**:
- Todo elemento seleccionable (activo: true) debe tener trazabilidad operativa completa.
- La cadena de trazabilidad obligatoria es: profile_catalog (activo: true) → role_id válido → specialization_id válida → preset correspondiente → paper_seed → default_model_policy o recomendación dinámica → agent config ejecutable.
- Si falta una pieza obligatoria, el elemento debe marcarse como `activo: false` o `draft` y no aparecer como opción usable.
- Los presets sin `recommended_provider`/`recommended_model` no es inconsistencia: el diseño delega recomendación a `core/model_recommendation.py`.
- Los agentes legacy sin combinación formal role+specialization se documentan pero no se eliminan por compatibilidad.

**Consecuencias**:
- 19 especializaciones en `profile_catalog.json` fueron marcadas como `activo: false` con nota explicativa.
- Se agregó campo `notas` para documentar por qué una especialización no es seleccionable.
- Se creó `tests/test_profile_preset_consistency.py` con 10 tests para validar consistencia.
- Los 11 agentes, 11 papers y 11 presets de Lotería siguen operativos e intactos.
- Los 5 agentes legacy (gemini_cuantico, gpt_auditor, nuevo_deepseek_saaop, viejo_deepseek, viejo_lobo_rey) se documentan como legacy pero no se rompen.
- Prompt 17.2 puede avanzar sobre una base saneada con trazabilidad operativa garantizada.

**Regla No Negociable**:
No puede existir un perfil usable sin preset operativo. No puede existir un preset usable sin profile asociado. No puede existir un agente operativo sin trazabilidad a profile/preset/paper/model policy, salvo que se documente explícitamente como legacy y no sea parte del flujo nuevo.

---

## ADR-023 — Catálogos operativos no deben contener elementos fantasma

**Estado**: Aceptado

**Prompt**: 17.1.2

**Contexto**:
En Prompt 17.1 se preparó soporte técnico para status como proposed/draft/active/deprecated. Sin embargo, la decisión de producto es más estricta: IA_CORE no debe tener elementos "propuestos" o "borradores" dentro de los catálogos operativos si después no se pueden usar. No queremos catálogos llenos de candidatos que nunca pasan a uso real, ni opciones visibles que no pueden terminar en agente/equipo operativo.

**Decisión**:
- IA_CORE distingue entre universo exploratorio/backlog documental y catálogo operativo.
- El universo exploratorio (ideas, propuestas, borradores, perfiles históricos, nichos candidatos) vive en docs/, reportes, backlog futuro o documentos de diseño.
- El catálogo operativo expone solo elementos PASSED/active con camino real hacia uso.
- `activo: true` = PASSED operativo.
- `activo: false` = baja/desactivado temporal.
- `status: active` (si se usa en futuro) = PASSED operativo.
- `status: proposed/draft` = estados de transición para clasificar y decidir, no usables.
- Los loaders operativos (`active_only=True`) excluyen `proposed`, `draft` y `deprecated` aunque `activo` sea `true`.
- Elementos incompletos deben clasificarse como recuperar_para_operar, legacy, baja/desactivado o backlog_documental.
- Ningún elemento puede aparecer como opción usable sin cumplir reglas de consistencia.

**Consecuencias**:
- El soporte técnico para proposed/draft NO existe para acumular ideas dormidas o catálogos fantasma.
- Existe para convertir lo que ya está creado en algo operativo, o para decidir formalmente que debe darse de baja, quedar legacy o pasar a recuperación posterior.
- Todo elemento existente queda clasificado en una tabla de decisión: PASSED / recuperar_para_operar / legacy / baja/desactivado / backlog_documental.
- Prompt 17.2 debe cargar solo elementos PASSED o preparar bloques con trazabilidad suficiente.
- Lo no validado queda en reporte/backlog, no en JSON operativo.

**Regla No Negociable**:
Ningún perfil/nicho/preset puede estar visible como usable sin cumplir reglas de consistencia. Todo elemento propuesto debe tender a operación real o darse de baja.

---

## ADR-024 — Perfil Profesional Global como entidad reutilizable previa al agente

**Estado**: Aceptado

**Prompt**: 18.0

**Contexto**:
IA_CORE necesita iniciar el inventario de perfiles profesionales globales sobre una base de 30 áreas y 200 nichos PASSED. Sin una entidad previa al agente, los perfiles pueden volverse otra lista decorativa o mezclarse con presets, papers, perfiles específicos de dominio y agentes legacy.

**Decisión**:
- IA_CORE define el Perfil Profesional Global como entidad reutilizable anterior a `domains/*/profile_catalog.json`, presets, papers y agentes.
- Un perfil global no es un agente ejecutable por sí mismo.
- Cada perfil global debe mapear áreas y nichos compatibles.
- Cada perfil global debe preparar trazabilidad hacia `role_id`, `specialization_id`, `preset_seed`, `paper_seed` y `default_model_policy`.
- `catalogs/professional_profiles.json` será la ubicación recomendada para el catálogo global PASSED cuando Prompt 18 cargue perfiles reales.
- La masa crítica inicial de 80-100 perfiles no es un techo; la auditoría de cobertura decide si conviene ampliar, dividir o fusionar perfiles.
- Ningún perfil debe entrar como PASSED si no puede avanzar hacia operación real y generación de valor.

**Consecuencias**:
- Los dominios específicos dejan de ser el centro simbólico del sistema y pasan a consumir o adaptar patrimonio global.
- Los perfiles históricos de dominios específicos se recuperarán solo mediante conversión controlada a perfiles PASSED, legacy o específicos de dominio.
- El inventario futuro de perfiles podrá validar cobertura contra áreas, nichos, escalas de negocio, tipos de equipo, model policies y valor económico.
- Prompt 18.0 no crea perfiles, presets, papers ni agentes; solo fija el contrato para cargarlos ordenadamente después.

## ADR-025 - Matriz perfil-area-nicho como artefacto derivado

**Estado**: Aceptado

**Prompt**: 19.0

**Contexto**:
Los perfiles profesionales globales ya declaran `areas_compatibles` y `nichos_compatibles` en `catalogs/professional_profiles.json`. El sistema necesita una matriz consultable para auditoria, cobertura y preparacion de generadores futuros, pero duplicar manualmente esa relacion crearia una segunda fuente de verdad.

**Decision**:
- La matriz Perfil Profesional <-> Area/Nicho es un artefacto derivado.
- La fuente de verdad sigue siendo `catalogs/professional_profiles.json`.
- La matriz se genera con `scripts/generate_professional_profile_matrix.py`.
- El reporte derivado vive en `docs/PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md`.
- Si cambia un perfil, la matriz debe regenerarse.
- La matriz no debe editarse manualmente como catalogo operativo.

**Consecuencias**:
- Permite consultar cobertura por area y nicho sin duplicar logica manual.
- Facilita detectar huecos, cobertura debil y sobrecobertura.
- Prepara generacion futura de dominios, presets, papers y team templates.
- Los tests validan que la matriz generada coincida con los catalogos fuente.

---

## ADR-026 - Model policy como puente entre perfil profesional y provider/model

**Estado**: Aceptado

**Prompt**: 20

**Contexto**:
Los perfiles profesionales globales declaran `default_model_policy`, pero esa policy necesitaba conectarse con recomendaciones operativas de provider/model, hardware local, privacidad, costo, latencia, contexto y revision humana.

**Decision**:
- IA_CORE usa `default_model_policy` como puente entre perfil profesional y provider/model.
- Las policies viven en `catalogs/profile_model_policies.json`.
- La recomendacion profesional vive en `core/professional_model_recommendation.py`.
- La recomendacion reutiliza `core.model_recommendation.HardwareProfile` y `evaluate_model_compatibility`.
- Cada recomendacion debe incluir provider/model primario, fallback, ejecucion recomendada, razon, privacidad, revision humana y nota hardware.

**Consecuencias**:
- Los perfiles quedan preparados para presets/papers/agentes futuros sin crear agentes ahora.
- La seleccion de modelo queda testeable y extensible.
- Hardware limitado puede forzar cloud o fallback local liviano.
- `human_review_required` y privacidad no quedan como texto decorativo: afectan la recomendacion.

---

## ADR-027 - profile_catalog por dominio como seleccion derivada

**Estado**: Aceptado

**Prompt**: 21

**Contexto**:
IA_CORE ya tiene perfiles profesionales globales, matriz area/nicho y recomendacion provider/model por perfil. El siguiente paso necesita llevar esa biblioteca a dominios concretos, pero escribir directamente `domains/*/profile_catalog.json` desde la biblioteca global crearia riesgo de duplicar verdad o modificar dominios reales prematuramente.

**Decision**:
- IA_CORE genera `profile_catalog` por dominio como una seleccion derivada de `catalogs/professional_profiles.json`.
- La Biblioteca Profesional Global sigue siendo fuente de verdad.
- El generador vive en `core/professional_profile_catalog_generator.py`.
- El CLI seguro vive en `scripts/generate_domain_profile_catalog.py`.
- Cada entrada derivada conserva `source_profile_id`, `role_id`, `specialization_id`, `default_model_policy`, `preset_seed_expected`, `paper_seed_expected`, scoring y `model_recommendation`.
- El CLI no escribe dentro de `domains/` ni sobrescribe archivos existentes.

**Consecuencias**:
- Los dominios futuros pueden recibir candidatos testeables sin crear agentes, presets ni papers.
- Los gaps de cobertura se reportan como warnings en lugar de inventar perfiles.
- Prompt 22 puede consumir esta seleccion para generar presets candidatos sin cambiar la fuente de verdad.

---

## ADR-028 - agent_presets por dominio como artefacto derivado

**Estado**: Aceptado

**Prompt**: 22

**Contexto**:
IA_CORE ya puede generar `profile_catalog` derivados desde la Biblioteca Profesional Global. El paso siguiente necesita convertir esos perfiles seleccionados en presets candidatos, pero escribir `domains/*/agent_presets.json` o crear agentes automaticamente adelantaria operacion sin revision.

**Decision**:
- IA_CORE genera `agent_presets` por dominio como artefactos derivados desde un `profile_catalog` derivado.
- La fuente de verdad sigue siendo `catalogs/professional_profiles.json`.
- El generador vive en `core/professional_agent_preset_generator.py`.
- El CLI seguro vive en `scripts/generate_domain_agent_presets.py`.
- Cada preset derivado conserva `source_profile_id`, `source_domain_profile_id`, `role_id`, `specialization_id`, `model_recommendation`, `fallback_recommendation`, `preset_seed_expected` y `paper_seed_expected`.
- `instructions_seed` es semilla inicial, no prompt final.
- El CLI no escribe dentro de `domains/` ni sobrescribe archivos existentes.

**Consecuencias**:
- Los dominios futuros pueden evaluar presets candidatos sin crear agentes ni papers.
- La recomendacion provider/model no se pierde al pasar de perfil a preset.
- Prompt 23 puede preparar papers candidatos o validacion de escritura real sin duplicar verdad.

---

## ADR-029 - team templates como composicion derivada de perfiles y presets

**Estado**: Aceptado

**Prompt**: 23

**Contexto**:
IA_CORE ya puede derivar profile_catalogs y agent_presets desde la Biblioteca Profesional Global. Un dominio real rara vez necesita un agente aislado; necesita composiciones de capacidades, roles, control, operacion y valor economico. Crear equipos operativos automaticamente seria prematuro.

**Decision**:
- IA_CORE genera plantillas de equipos profesionales como artefactos derivados.
- La fuente de verdad sigue siendo `catalogs/professional_profiles.json`.
- La composicion usa profile_catalog derivado, agent_presets derivados, `team_roles`, business scales, value paths y model recommendations.
- El generador vive en `core/professional_team_template_generator.py`.
- El CLI seguro vive en `scripts/generate_professional_team_template.py`.
- Las plantillas no crean agentes reales, papers ni escrituras en dominios.

**Consecuencias**:
- Los dominios futuros pueden evaluar equipos candidatos antes de operar.
- `model_policy_mix`, gaps, riesgos y criterios de activacion quedan visibles.
- Prompt 24 puede validar composicion end-to-end o preparar escritura controlada sin duplicar verdad.

---

## ADR-030 - validacion end-to-end profesional como artefacto no operativo

**Estado**: Aceptado

**Prompt**: 24

**Contexto**:
IA_CORE puede derivar perfiles, presets, recomendaciones de modelo y equipos. Antes de materializar recursos reales necesita demostrar que la cadena completa conserva consistencia y trazabilidad sin contaminar dominios existentes.

**Decision**:
- La validacion end-to-end vive en `core/professional_domain_end_to_end.py`.
- Su salida es un artefacto derivado, seguro y explicitamente no operativo.
- Compone los generadores existentes y agrega paper seeds esperados, gaps, warnings, riesgos, outputs y plan de activacion.
- El CLI rechaza escrituras dentro de `domains/` y no sobrescribe salidas.
- La validacion no crea dominios, presets operativos, papers ni agentes.

**Consecuencias**:
- La cadena profesional completa puede auditarse antes de autorizar materializacion.
- Cada pieza conserva su origen en `catalogs/professional_profiles.json`.
- Los faltantes se informan y no se sustituyen por catalogos inventados.

---

## Nota de cierre - Libro Biblioteca Profesional Global

Prompt 25 no agrega una decision arquitectonica nueva. Cierra y consolida las decisiones ADR-024 a ADR-030 como el bloque arquitectonico de la Biblioteca Profesional Global.

La decision consolidada es mantener `catalogs/professional_profiles.json` como fuente de verdad, y tratar matriz, recomendaciones, `profile_catalog`, `agent_presets`, team templates y validacion end-to-end como artefactos derivados, trazables y no operativos hasta que una fase posterior autorice materializacion controlada en dominios reales.

---

## ADR-031 - Arquetipos psicologicos globales reutilizables, baseline legacy y limpieza de identidad activa

**Estado**: Aceptado

**Prompt**: RESET 01

**Contexto**:
Los perfiles/agentes psicologicos historicos de Loteria sirvieron como semilla conceptual de IA_CORE, pero quedaron mezclados con agentes reales, papers, presets y system prompts manuales creados antes de la Biblioteca Profesional Global. Esa mezcla mantenia a Loteria como excepcion y preservaba una identidad vieja como si fuera activa.

**Decision**:
- Los perfiles psicologicos historicos pasan a `catalogs/agent_archetypes.json` como arquetipos globales reutilizables.
- Los system prompts legacy se archivan en `docs/legacy/loteria/legacy_system_prompts_baseline.json` y `.md`.
- Los snapshots completos de profile catalog, agent presets, configs y papers legacy de Loteria se preservan en `docs/legacy/loteria/`.
- `domains/loteria/profile_catalog.json` y `domains/loteria/agent_presets.json` quedan como estructuras minimas no operativas, sin perfiles ni presets legacy activos.
- Los configs y papers legacy salen de `domains/loteria/agents/` para no quedar como agentes/papers operativos.
- IA_CORE deja de usar SAAOP/SAAOPS/S.A.A.O.P. como identidad activa en templates nuevos.

**Consecuencias**:
- Loteria deja de ser excepcion del framework.
- Los arquetipos pueden combinarse con cualquier dominio, area, nicho, escala y objetivo.
- La historia queda preservada para comparacion, pero no ejecuta ni define identidad activa.
- La recreacion futura de agentes debe pasar por materializacion controlada y revision humana.

---

## ADR-032 - Unicidad de dominios y limpieza de dominios legacy duplicados

**Estado**: Aceptado

**Prompt**: CORE 01

**Contexto**:
IA_CORE podia mostrar dominios duplicados o funcionalmente equivalentes. El dominio historico `loteria` seguia visible como "Loteria / IA_CORE" y coexistia con `loteria_analisis_de_juegos_de_azar`, creado desde la UI como "Loteria - Analisis de Juegos de Azar". El primero era legacy y el segundo estaba parcial, pero ambos aparecian como candidatos operativos.

**Decision**:
- IA_CORE no permite dominios duplicados o equivalentes.
- La equivalencia de dominios se normaliza en `core/domain_identity.py`.
- `core/domain_registry.create_domain()` valida unicidad contra dominios activos, dominios internos/legacy y snapshots archivados en `docs/legacy/domains/`.
- `domains/loteria/domain.json` queda marcado como `visible_en_hud=false`, `status=legacy` y `legacy=true`.
- El dominio UI `domains/loteria_analisis_de_juegos_de_azar` se preserva como snapshot documental y sale del flujo operativo.

**Consecuencias**:
- El selector de dominios ya no expone Loteria como dominio activo hasta que sea recreada con el framework nuevo.
- Un dominio archivado o legacy sigue bloqueando recreaciones duplicadas sin accion admin explicita.
- Los dominios vacios, historicos o equivalentes no pueden presentarse como operativos por accidente.

---

## ADR-033 - Backend interno como fuente de verdad para materializacion controlada

**Estado**: Aceptado

**Prompt**: 0.0 - Libro Backend Interno

**Contexto**:
La Biblioteca Profesional Global dejo artefactos derivados y no operativos preparados para una futura materializacion. Para pasar de propuesta a operacion real sin contaminar dominios, IA_CORE necesita una capa interna que gobierne preview, validacion, estados, escritura, trazabilidad, rollback, regeneracion y contrato para UI.

**Decision**:
- IA_CORE separa artefactos derivados/no operativos de artefactos operativos reales.
- La UI no materializa ni valida reglas de negocio por su cuenta.
- El backend interno administra preview, validacion, materializacion, estados, rollback, regeneracion y contrato estable para UI.
- Todo artefacto operativo debe tener trazabilidad, validacion y criterio PASSED.
- Las integraciones externas quedan fuera del core y se tratan como extensiones futuras.

**Consecuencias**:
- El proximo libro debe comenzar por reglas internas, estados y contrato antes de crear sandbox real.
- Los derivados existentes no se consideran operativos hasta pasar por materializacion controlada.
- La UI puede mostrar estados, errores y acciones, pero no inferir ni reparar reglas internas.

---

## ADR-034 - Separacion obligatoria entre artefactos derivados y operativos

**Estado**: Aceptado

**Prompt**: 0.1 - Contrato derivado vs operativo real

**Contexto**:
IA_CORE ya puede generar `profile_catalog`, `agent_presets`, recomendaciones, team templates, paper seeds y validaciones end-to-end como salidas derivadas. Sin un contrato tecnico, esas salidas podrian confundirse con artefactos reales disponibles para backend o UI.

**Decision**:
- IA_CORE distingue formalmente artefactos derivados/no operativos de artefactos operativos reales mediante `core/artifact_state.py`.
- Las salidas derivadas pueden estar listas para revision o materializacion, pero no son usables ni visibles como operativas hasta estar materializadas, validadas, trazadas y marcadas como `active`/PASSED.
- `derived_preview` y `ready_to_materialize` nunca son operativos.
- `materialized` existe en filesystem o registry sandbox, pero no equivale automaticamente a `active`.
- Estados historicos o fallidos (`legacy`, `archived`, `broken`) no entran al flujo nuevo salvo recuperacion, restore o regeneracion formal.

**Consecuencias**:
- La UI y los servicios internos no pueden tratar previews, seeds, templates o outputs derivados como artefactos reales.
- Todo paso hacia operacion debe pasar por materializacion controlada, validacion y trazabilidad.
- Estados desconocidos o transicionales como `proposed`/`draft` no pasan como operativos por defecto.

---

## ADR-035 - Estados y administracion interna segura de dominios

**Estado**: Aceptado

**Prompt**: 0.2 - Estados y administracion interna de dominios

**Contexto**:
IA_CORE necesita administrar dominios desde backend interno sin que la UI infiera si un dominio puede aparecer activo, archivarse, restaurarse, resetearse o eliminarse. CORE 01 resolvio identidad/unicidad; faltaba un contrato de estado y acciones seguras.

**Decision**:
- Se crea `core/domain_state.py` para estados y acciones internas de dominios.
- Los estados formales son `empty`, `draft`, `preview`, `materialized`, `active`, `archived`, `legacy` y `broken`.
- `core/domain_registry.list_domains()` oculta por defecto dominios con estados no activos.
- `archive_domain()`, `restore_domain()`, `reset_domain()` y `delete_domain_safely()` actualizan manifest con trazabilidad y protecciones explicitas.
- `legacy` no puede pasar a `active` directamente y `delete_domain_safely()` nunca borra legacy automaticamente.

**Consecuencias**:
- La UI futura puede consumir permisos/estado desde backend en vez de deducir reglas.
- Archivar, restaurar, resetear y eliminar quedan diferenciados.
- Dominios vacios, historicos, rotos o materializados pero no PASSED no aparecen como activos por accidente.

---

## ADR-036 - Preview obligatorio antes de materializacion de dominios

**Estado**: Aceptado

**Prompt**: 0.3 - Contrato de preview antes de materializacion

**Contexto**:
IA_CORE ya puede derivar `profile_catalog`, `agent_presets`, team templates, recomendaciones de modelo y paper seeds. Antes de crear un dominio sandbox real, el backend necesita exponer una vista previa completa y no operativa que permita revisar riesgos, gaps y acciones pendientes.

**Decision**:
- Se crea `core/domain_materialization_preview.py` como capa de preview previa a cualquier materializacion.
- El preview compone generadores existentes y devuelve un payload serializable con `domain_request`, `source`, `derived_outputs`, `warnings`, `gaps`, `risks`, `required_actions` y `validation_status`.
- Los estados permitidos del preview son `derived_preview`, `ready_to_materialize` y `broken`.
- El preview nunca escribe en `domains/`, nunca crea agentes, papers, presets operativos ni equipos, y nunca marca artefactos como operativos.

**Consecuencias**:
- La materializacion futura parte de un contrato revisable, trazable y testeado.
- La UI futura podra mostrar preview y acciones pendientes sin inferir reglas de negocio.
- `ready_to_materialize` no equivale a PASSED; solo habilita una fase posterior controlada.

---

## ADR-037 - Creacion de dominio solo por backend interno validado

**Estado**: Aceptado

**Prompt**: 0.4 - Auditoria de rutas de creacion de dominio y bloqueo de bypasses

**Contexto**:
Despues de definir unicidad, estados y preview obligatorio, quedaba una ruta publica legacy (`/api/domains/create`) capaz de escribir dominios reales antes de pasar por materializacion controlada. Esa ruta podia funcionar como bypass de preview, trazabilidad y reglas PASSED.

**Decision**:
- IA_CORE no permite rutas paralelas de creacion, registro o exposicion de dominios que salteen unicidad, equivalencias, estados, preview, materializacion controlada o reglas PASSED.
- `/api/domains/create` queda bloqueado para el root operativo `domains/`.
- `core/domain_registry.create_domain()` queda como primitiva central para fixtures aislados y futura materializacion interna, no como ruta publica directa de UI.
- `core/domain_registry.list_domains()` decide visibilidad activa usando `core/domain_state.py`, incluyendo rechazo de estados desconocidos.
- Scripts, tests, endpoints y UI deben usar servicios centrales o fixtures temporales aislados.

**Consecuencias**:
- Ningun dominio puede aparecer como activo/usable por escritura directa o bypass de registry.
- La UI futura debe reemplazar la creacion directa por preview y materializacion controlada.
- Los tests pueden crear fixtures temporales, pero no deben modificar `domains/` operativo.

---

## ADR-038 - Domain.json validado para todo sandbox materializado

**Estado**: Aceptado

**Prompt**: 1.0 - Schema de dominio sandbox real

**Contexto**:
La Fase 1 introduce dominio sandbox real, pero antes de materializar cualquier carpeta en `domains/` IA_CORE necesita un contrato minimo que impida dominios fantasma, dominios sin origen, dominios sin rollback o dominios marcados como activos sin PASSED.

**Decision**:
- Todo dominio sandbox materializado debe tener un `domain.json` validado por `core/sandbox_domain_schema.py`.
- El manifest debe declarar identidad, `status`, `domain_type=sandbox`, `source_request`, `created_from`, `materialization_id`, `materialization_status`, `artifact_state`, fechas, `human_review_required`, `rollback_manifest`, `validation`, `warnings` y `metadata`.
- `materialized` no equivale automaticamente a `active`.
- `active` queda bloqueado hasta que exista trazabilidad PASSED completa y una fase posterior defina la activacion.
- El schema no crea ni registra dominios; solo valida contrato.

**Consecuencias**:
- La futura materializacion no puede escribir carpetas o archivos sueltos sin manifest validable.
- La UI y servicios internos deberan consumir dominios sandbox mediante estructuras validadas.
- Rollback, preview y revision humana quedan presentes desde el primer contrato de sandbox, aunque su ejecucion real llegue en prompts posteriores.

---

## ADR-039 - Materializacion sandbox solo mediante servicio controlado

**Estado**: Aceptado

**Prompt**: 1.1 - Materializacion controlada de dominio sandbox

**Contexto**:
Una vez definido el schema de dominio sandbox, IA_CORE necesita una forma unica y testeable de transformar ese contrato en archivos reales de sandbox. Es necesario evitar escrituras directas, sobrescrituras, duplicados, dominios legacy reactivados y estados activos prematuros.

**Decision**:
- La materializacion sandbox debe pasar por `core/domain_materializer.py`.
- El materializador valida schema antes de escribir, genera `materialization_id`, crea `domain.json` y `materialization_manifest.json`, registra paths creados y ejecuta validacion post materializacion.
- El destino no puede ser `domains/` operativo.
- La materializacion queda en `materialized`; no activa dominios ni registra dominios operativos.
- Rollback real queda diferido, pero su manifest debe existir desde la materializacion.

**Consecuencias**:
- Ningun flujo futuro deberia crear sandboxes escribiendo archivos sueltos.
- Tests y servicios deben usar raices temporales o controladas.
- La activacion PASSED queda reservada para fases posteriores.

---

## ADR-040 - Toda materializacion sandbox debe ser reversible mediante manifest

**Estado**: Aceptado

**Prompt**: 1.2 - Rollback y limpieza segura de dominio sandbox

**Contexto**:
La materializacion sandbox ya crea `domain.json` y `materialization_manifest.json` en una raiz controlada. Para evitar residuos, estructuras fantasma o borrados a ciegas, cada materializacion debe poder revertirse usando evidencia declarada.

**Decision**:
- Toda materializacion sandbox debe registrar `created_paths` en `materialization_manifest.json`.
- El rollback debe pasar por `core/domain_materialization_rollback.py`.
- El rollback solo puede eliminar paths declarados por el manifest y contenidos dentro de la raiz sandbox permitida.
- Cualquier path hacia `domains/` operativo queda bloqueado.
- El rollback debe conservar trazabilidad en `_rollback_records` y ser idempotente.

**Consecuencias**:
- Una materializacion sandbox no se considera completa si no puede revertirse de forma segura.
- Los tests ida/vuelta deben probar materializacion, rollback, limpieza e idempotencia.
- Rollback de modificaciones o backups reales queda diferido hasta que una fase futura cree artefactos modificables.

---

## ADR-041 - Todo sandbox debe tener ciclo reversible y regenerable

**Estado**: Aceptado

**Prompt**: 1.3 - Validacion completa del ciclo sandbox y regeneracion segura

**Contexto**:
IA_CORE ya cuenta con preview, schema, materializacion y rollback sandbox. Faltaba validar que esas piezas funcionen como ciclo repetible: materializar, validar, regenerar y revertir sin residuos ni duplicados.

**Decision**:
- Todo ciclo sandbox debe poder validarse end-to-end mediante `core/sandbox_lifecycle_validation.py`.
- La regeneracion debe ejecutar rollback controlado antes de recrear.
- Cada regeneracion debe generar un nuevo `materialization_id`, incrementar `generation_number` y conservar `previous_materialization_id`.
- El historial debe conservar eventos de materializacion y rollback.
- El ciclo no puede activar dominios ni tocar `domains/` operativo.

**Consecuencias**:
- Un sandbox no se considera sano si no puede repetirse y limpiarse.
- Los prompts posteriores deben apoyarse en este ciclo antes de crear artefactos reales como catalogos, presets, papers o agentes.
- La trazabilidad del ciclo queda como base para auditoria y UI futura.

---

## ADR-042 - Todo artefacto interno sandbox debe tener manifest y trazabilidad

**Estado**: Aceptado

**Prompt**: 1.4.1 - Contrato de artifact_manifest para sandbox

**Contexto**:
La auditoria de preparacion sandbox detecto que el dominio y su ciclo estan listos, pero los artefactos internos futuros necesitan lineage propio para no convertirse en archivos sueltos sin dependencias ni rollback.

**Decision**:
- Todo artefacto interno sandbox debe registrarse en `artifact_manifest.json`.
- El contrato se valida mediante `core/artifact_manifest_schema.py`.
- Cada artefacto debe declarar `artifact_id`, `artifact_type`, `version`, `status`, `created_from`, `created_by`, `dependencies` y `rollback_info`.
- Los estados de artefacto reutilizan `core/artifact_state.py`.
- Las dependencias deben apuntar a otros `artifact_id` existentes dentro del mismo manifest.

**Consecuencias**:
- Fase 2 no debe materializar `profile_catalog` ni `agent_presets` como archivos sueltos.
- Rollback parcial queda preparado por contrato, aunque no se implemente todavia.
- Papers, agentes, equipos y memoria deberan entrar al sandbox con la misma disciplina de manifest.

---

## ADR-043 - Los equipos sandbox son estructuras declarativas no ejecutables

**Estado**: Aceptado

**Prompt**: 5.0 - Schema de equipo real sandbox

**Contexto**:
Fase 5 inicia la representacion de equipos reales sandbox. IA_CORE ya tenia piezas historicas de `sandbox_team` y generadores de `team_template`, pero faltaba separar formalmente una plantilla derivada de un equipo sandbox real asociado a dominio, miembros, lineage, permisos y politica de no ejecucion.

**Decision**:
- IA_CORE representa equipos reales sandbox como artefactos declarativos trazables, asociados a un dominio sandbox.
- Un equipo sandbox puede derivar de `team_template`, pero `team_template` no es equipo real sandbox.
- `core/sandbox_team_schema.py` es el contrato canonico para validar identidad, `artifact_id`, `materialization_id`, `source_team_template`, `created_from`, miembros, `execution_policy`, `permissions`, estados y compatibilidad futura con manifest.
- El `artifact_manifest` vigente conserva `artifact_type: team` por compatibilidad, mientras el contrato declara `sandbox_team` como tipo conceptual.
- Un equipo sandbox no habilita ejecucion multiagente real, invocacion de modelos, tools, runtime, outputs operativos ni integraciones.

**Consecuencias**:
- La futura materializacion de equipos podra validar identidad, miembros, roles, permisos, dependencies y lineage antes de cualquier ejecucion.
- Runtime y ejecucion real siguen bloqueados hasta una fase posterior explicita.
- La UI futura no debe tratar `team_template` ni equipo sandbox `materialized` como equipo operativo activo.

---

## ADR-044 - La materializacion de equipos sandbox desde team_template es declarativa

**Estado**: Aceptado

**Prompt**: 5.1 - Materializar equipo real sandbox desde team_template

**Contexto**:
Fase 5 ya definio el schema de equipo sandbox real. El siguiente paso necesitaba convertir un `team_template` derivado en artefactos sandbox trazables sin confundir plantilla derivada, equipo sandbox materializado y equipo operativo ejecutable.

**Decision**:
- La materializacion desde `team_template` usa `core/sandbox_team_materializer.py`; no se crea un materializador paralelo.
- El flujo crea `sandbox_teams/<team_id>.json`, `sandbox_teams/<team_id>.manifest.json`, registro en `manifests/artifact_manifest.json` y extension de `materialization_manifest.json`.
- El `artifact_manifest` mantiene `artifact_type: team` por compatibilidad con `core/artifact_manifest_schema.py`.
- La semantica especifica se declara con `artifact_kind: sandbox_team`, `source_team_template`, `created_from`, `materialization_id` y flags no operativos.
- Los miembros pueden quedar como referencias declarativas con `agent_reference=null`; esto no crea agentes ni habilita ejecucion.
- La validacion rechaza paths operativos, flags de runtime/execution/tools/modelos/integraciones y permisos sensibles en `true`.

**Consecuencias**:
- PROMPT 5.1 permite auditar equipos sandbox materializados sin activar runtime multiagente.
- La futura auditoria 5.2 debe revisar team, manifest, artifact manifest, lineage y frontera no-operativa.
- Cualquier cambio futuro para aceptar `artifact_type: sandbox_team` en el manifest global requiere subprompt explicito de compatibilidad.

---

## ADR-045 - Los equipos sandbox se exponen internamente mediante read model no operativo

**Estado**: Aceptado

**Prompt**: 5.3 - Biblioteca interna/listado de equipos sandbox para futura UI

**Contexto**:
Fase 5 ya cuenta con schema, materializacion declarativa y auditoria de equipos sandbox. Antes de cualquier UI futura, IA_CORE necesita una forma interna, segura y legible de listar equipos materializados sin abrir operacion real.

**Decision**:
- IA_CORE expone equipos sandbox materializados solo mediante `core/sandbox_team_read_model.py` como read model interno, read-only y JSON-safe.
- El read model resume identidad, dominio, origen `team_template`, `artifact_id`, `materialization_id`, members declarativos, permissions, execution policy, warnings, validation y readiness.
- El read model conserva `artifact_type: team` y `artifact_kind: sandbox_team` sin ambiguedad.
- El read model no crea UI, endpoints publicos, equipos, agentes, runtime, tools, modelos, outputs, stores ni integraciones.
- Payloads con permisos sensibles, execution/runtime/tools/modelos/integraciones en `true`, secrets/env/runtime handles o configs sensibles deben fallar con error controlado.

**Consecuencias**:
- La UI futura puede listar e inspeccionar equipos sandbox sin inferir reglas criticas ni activar operacion real.
- Toda mutacion, materializacion, correccion, activacion o ejecucion seguira perteneciendo a backend interno y fases posteriores explicitas.
- Fase 5 minima puede cerrarse con readiness hacia planificacion del siguiente bloque arquitectonico.

---

## ADR-046 - Fase 6 debe reutilizar la cadena sandbox existente antes de crear nuevos flujos E2E

**Estado**: Aceptado

**Prompt**: 5.4 - Planificacion del siguiente bloque arquitectonico despues de Fase 5

**Contexto**:
Fase 5 minima quedo cerrada con schema, materializacion, auditoria y read model de equipos sandbox. El libro Backend Interno define la fase siguiente como end-to-end sandbox, rollback y regeneracion. El repo ya contiene piezas vigentes e historicas de lifecycle, rollback y sandbox chain, incluyendo `tests/test_sandbox_chain_with_team_checkpoint.py`.

**Decision**:
- El siguiente bloque arquitectonico es `Fase 6 - End-to-end operativo sandbox, rollback y regeneracion`.
- El proximo prompt exacto es `PROMPT 6.0 - Validacion end-to-end sandbox completa`.
- Fase 6 debe reutilizar o extender las piezas existentes antes de crear cualquier flujo E2E nuevo.
- Fase 6 permanece sandbox/no-operativa: runtime, execution, dry-run real, tools, modelos, UI, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS siguen bloqueados.

**Consecuencias**:
- Se reduce riesgo de duplicar `sandbox_chain`.
- `PROMPT 6.0` debe empezar por validacion/reconciliacion, no por runtime ni UI.
- La futura Fase 7 de contrato backend/UI recibira evidencia de Fase 6, no logica inferida desde frontend.

---

## ADR-047 - Rollback integral sandbox basado en manifests y paths declarados

**Estado**: Aceptado

**Prompt**: 6.1 - Rollback integral de dominio sandbox completo

**Contexto**:
Fase 6 ya valido la cadena sandbox completa con dominio, artifact manifest, profile catalog, agent presets, paper seed, agentes sandbox, equipo sandbox y read model. El rollback base de Fase 1 era seguro para la materializacion del dominio, pero la cadena completa necesita una regla integral que combine `materialization_manifest.json`, `artifact_manifest.json` y `created_paths` declarados para evitar borrados amplios o ambiguos.

**Decision**:
- IA_CORE permite rollback integral de dominios sandbox unicamente sobre paths declarados por manifests y contenidos bajo `sandbox_root` validado.
- El contrato integral vive en `core/domain_materialization_rollback.py`; no se crea un modulo paralelo.
- El rollback plan debe derivarse de `artifact_manifest`, `rollback_info.created_paths` y `materialization_manifest.created_paths`.
- Cualquier path fuera del sandbox, hacia `domains/` operativo, repo root, `.git/`, `core/`, `docs/`, `tests/`, `agents/`, path traversal, glob destructivo o symlink escape queda bloqueado.
- El rollback integral debe ser idempotente y conservar trazabilidad en `_rollback_records`.
- Runtime, execution, tools, modelos, UI e integraciones permanecen bloqueados.

**Consecuencias**:
- La cadena sandbox completa puede revertirse sin riesgo de borrar activos operativos o codigo del repo.
- La regeneracion segura futura debe partir de esta garantia de rollback integral.
- Cualquier ampliacion futura de artefactos sandbox debe declarar `created_paths` coherentes si espera participar del rollback integral.

---

## ADR-048 - Regeneracion sandbox segura posterior a rollback integral

**Estado**: Aceptado

**Prompt**: 6.2 - Regeneracion segura sandbox completa

**Contexto**:
Despues de validar la cadena sandbox completa y el rollback integral basado en manifests, IA_CORE necesita reconstruir esa cadena sin asumir continuidad operativa ni reutilizar residuos. La regeneracion debe validar equivalencia estructural, no igualdad bit a bit, porque `materialization_id`, timestamps y registros de rollback pueden cambiar por diseno.

**Decision**:
- IA_CORE permite regenerar cadenas sandbox completas unicamente despues de rollback integral validado.
- La regeneracion usa `sandbox_root` controlado, `materialization_manifest`, `artifact_manifest`, `created_paths` y comparacion estructural no-operativa.
- La regeneracion preserva identidad logica del dominio y lineage mediante `previous_materialization_id`.
- La regeneracion debe crear un nuevo `materialization_id` cuando corresponde.
- Cualquier residuo no declarado dentro del dominio sandbox previo bloquea la regeneracion con error controlado.
- La comparacion estructural valida familia de artefactos, tipos, `artifact_kind`, dependencies, read model shape, flags no-operativas y ausencia de duplicados.
- Regenerar no implica continuidad de ejecucion, activacion runtime, invocacion de modelos, tools, UI ni integraciones.

**Consecuencias**:
- El sistema puede reconstruir cadenas sandbox de forma trazable y repetible sin residuos ni duplicados.
- Fase 6.3 puede construir audit pack sobre evidencia de materializacion, rollback y regeneracion.
- La futura activacion operacional no puede inferirse de una regeneracion sandbox exitosa.

---

## ADR-049 - Audit pack sandbox como evidencia interna no operativa

**Estado**: Aceptado

**Prompt**: 6.3 - Audit pack y trazabilidad de materializacion sandbox

**Contexto**:
Fase 6 ya valido la cadena sandbox completa, rollback integral, regeneracion segura y comparacion estructural. Faltaba empaquetar esa evidencia de forma consumible por backend interno, auditoria futura y futura UI sin convertirla en ejecucion ni exponer datos sensibles.

**Decision**:
- IA_CORE empaqueta la evidencia de materializacion, rollback y regeneracion sandbox en un audit pack interno JSON-safe, no operativo y sin side effects.
- El contrato vive en `core/sandbox_materialization_audit_pack.py`.
- El audit pack resume manifests, lineage, dependencies, `created_paths`, reports, comparacion estructural, bloqueos y readiness.
- El audit pack excluye secrets/env, runtime handles, API keys, access tokens, model/tool configs operativos, network/output delivery handles, data productiva, raw prompts, dumps excesivos y rutas absolutas completas.
- El audit pack declara `operational=false`, `passed=false`, `runtime_enabled=false`, `execution_enabled=false`, `tool_execution_enabled=false`, `model_invocation_enabled=false` y `external_integrations_enabled=false`.

**Consecuencias**:
- Backend interno y futura UI podran inspeccionar evidencia probatoria sin activar runtime ni inferir reglas criticas.
- La auditoria de Fase 6 queda desacoplada de cualquier ejecucion real.
- El checkpoint integral 6.4 puede consumir evidencia resumida y trazable sin abrir runtime, execution, tools, modelos, UI ni integraciones.

---

## ADR-050 - Fase 6 cierra el ciclo sandbox E2E rollback regeneracion auditoria sin operacion real

**Estado**: Aceptado

**Prompt**: 6.4 - Checkpoint integral Fase 6

**Contexto**:
Fase 6 ya valido E2E sandbox completo, rollback integral, regeneracion segura y audit pack interno. El libro Backend Interno necesita un cierre integral antes de avanzar al contrato backend interno para futura UI.

**Decision**:
- IA_CORE considera cerrada Fase 6 cuando la cadena sandbox completa fue validada E2E, revertida mediante rollback integral, regenerada de forma segura y empaquetada en un audit pack JSON-safe.
- El cierre integral se documenta en `docs/BACKEND_INTERNAL_PHASE_6_INTEGRAL_CHECKPOINT.md`.
- El siguiente bloque seleccionado es `Fase 7 - Contrato backend interno para UI`.
- Fase 7 no queda implementada por el checkpoint 6.4.
- Runtime, execution, dry-run real, modelos, tools, UI visual real, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS permanecen bloqueados.

**Consecuencias**:
- El sistema puede avanzar al contrato backend interno para futura UI con evidencia suficiente de que la cadena sandbox es trazable, reversible, regenerable y auditable sin ser operativa.
- La futura UI debe consumir contrato backend interno y no inferir reglas criticas desde manifests, audit pack o archivos crudos.
- Cualquier apertura operativa futura requiere prompts posteriores explicitos.

---

## ADR-051 - Contrato backend interno como frontera segura para futura UI

**Estado**: Aceptado

**Prompt**: 7.0 - Contrato backend interno para UI

**Contexto**:
Fase 6 cerro la cadena sandbox completa con E2E, rollback integral, regeneracion segura y audit pack JSON-safe. El siguiente bloque necesita preparar una futura UI sin permitir que la UI invente estados, readiness, permisos o acciones criticas desde manifests crudos.

**Decision**:
- IA_CORE define `core/backend_internal_ui_contract.py` como frontera backend interna para futura UI.
- La UI futura debe consumir payloads JSON-safe, estados, readiness, errores y limites definidos por backend.
- En 7.0 solo quedan disponibles servicios de contrato puro: `get_backend_internal_ui_contract` y `validate_backend_internal_ui_contract`.
- Servicios como `list_domains_status`, `preview_materialization`, `materialize_sandbox`, `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain` quedan planeados, no disponibles al cierre de 7.0.
- Runtime, execution, dry-run real, agentes, modelos, tools, integraciones, UI visual, endpoints publicos, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS permanecen bloqueados.

**Consecuencias**:
- El sistema podra construir UI futura sobre una base estable y segura.
- La UI no sera fuente de verdad arquitectonica ni podra convertir artefactos sandbox en operacion real por si misma.
- Cualquier servicio con write controlado o accion destructiva requiere fase posterior explicita y confirmacion humana cuando corresponda.

---

## ADR-052 - list_domains/status como primer servicio interno read-only para futura UI

**Estado**: Aceptado

**Prompt**: 7.1 - Servicio interno list_domains/status

**Contexto**:
Despues del contrato backend interno para UI, IA_CORE necesita un primer servicio real de lectura para que una futura UI pueda listar dominios sandbox sin tocar el sistema operativo del repo ni convertir el contrato en endpoint publico.

**Decision**:
- IA_CORE expone el estado de dominios sandbox a futura UI mediante el servicio interno read-only `list_domains/status`.
- El servicio vive en `core/backend_internal_domain_status_service.py`.
- El servicio requiere `sandbox_root` explicito/controlado y no lee `domains/` operativo por defecto.
- El payload es JSON-safe e incluye estado, readiness, artefactos, audit pack, equipo sandbox/read model, rollback/regeneration, allowed_actions, forbidden_actions, next_actions, warnings y errores.
- `list_domains_status` queda `available_now=true` en el contrato backend interno.
- Los servicios 7.2+ siguen planned/available_now=false.
- Runtime, execution, dry-run real, modelos, tools, UI visual, endpoints publicos, integraciones, Market Catalog runtime, Business Composition Layer runtime y OBLITERATUS permanecen bloqueados.

**Consecuencias**:
- La UI futura podra listar estados de dominios sin inferir logica critica ni activar operacion real.
- Los servicios con mutacion o acciones destructivas quedan en prompts posteriores con confirmacion y contratos especificos.
- La frontera de lectura queda separada de preview, materializacion, rollback, regeneracion y UI visual.

---

## ADR-053 - preview_materialization como simulacion no-write previa a materializacion

**Estado**: Aceptado

**Prompt**: 7.2 - Servicio interno preview_materialization

**Contexto**:
IA_CORE ya cuenta con `core/domain_materialization_preview.py` como preview no operativo previo a materializacion de dominios. Fase 7 necesita exponer esa capacidad como servicio interno para futura UI sin permitir que preview cree archivos, manifests, dominios o runtime.

**Decision**:
- IA_CORE expone `preview_materialization` como servicio interno no-write para calcular artefactos, paths, manifests, lineage, warnings y readiness antes de cualquier materializacion real.
- El servicio vive en `core/backend_internal_preview_materialization_service.py`.
- El servicio exige `domain_request` y `sandbox_root` explicito/controlado.
- Planned paths se devuelven como rutas relativas con `operation=would_create`.
- `preview_materialization` queda `available_now=true` en el contrato backend interno para UI.
- `list_domains_status` sigue disponible y los servicios 7.3+ siguen planned/available_now=false.
- El preview no crea archivos, no muta manifests, no toca domains operativo, no activa runtime y no habilita ejecucion.

**Consecuencias**:
- La futura UI y el backend interno podran mostrar una vista previa segura antes de pedir materializacion controlada.
- La escritura real queda separada en `PROMPT 7.3 - Servicio interno materialize_sandbox` con contrato propio.
- La frontera preview evita confundir simulacion declarativa con materializacion real.

---

## ADR-054 - materialize_sandbox como escritura controlada posterior a preview

**Estado**: Aceptado

**Prompt**: 7.3 - Servicio interno materialize_sandbox

**Contexto**:
Despues de `preview_materialization`, IA_CORE necesita permitir una escritura sandbox real para que la futura UI pueda solicitar materializacion sin tocar `domains/` operativo ni abrir runtime. La decision debia separar escritura sandbox controlada de ejecucion operativa.

**Decision**:
- IA_CORE permite materializacion sandbox desde el contrato backend interno solo mediante `materialize_sandbox`.
- `materialize_sandbox` es `controlled-write`, exige preview valido, `sandbox_root` seguro, confirmacion explicita, paths seguros, `allow_overwrite=false` y rollback preparado.
- La cadena materializada reutiliza Fase 6: `domain sandbox -> artifact_manifest -> profile_catalog -> agent_presets -> paper_seed -> sandbox agents -> sandbox team -> team read model`.
- El servicio vive en `core/backend_internal_materialize_sandbox_service.py` y queda `available_now=true` en `core/backend_internal_ui_contract.py`.
- La materializacion escribe unicamente en sandbox controlado y mantiene runtime, execution, dry-run real, modelos, tools, UI visual, endpoints publicos e integraciones bloqueados.

**Consecuencias**:
- La futura UI podra pedir materializacion sandbox de manera segura sin inferir reglas criticas.
- Toda escritura queda trazada, validada y reversible mediante rollback plan integral.
- `domains/` operativo, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel siguen fuera de alcance.

---

## ADR-055 - validate_domain como validacion interna read-only para futura UI

**Estado**: Aceptado

**Prompt**: 7.4 - Servicio interno validate_domain

**Contexto**:
Despues de `materialize_sandbox`, IA_CORE necesita validar dominios sandbox materializados antes de exponer readiness a servicios correctivos futuros. La futura UI debe recibir diagnosticos confiables sin reparar, escribir ni inferir logica critica.

**Decision**:
- IA_CORE expone `validate_domain` como servicio interno read-only-validation.
- El servicio vive en `core/backend_internal_validate_domain_service.py`.
- El servicio requiere `sandbox_root` explicito/controlado y `domain_id`.
- Valida dominio, materialization manifest, artifact_manifest, created_paths, lineage/dependencies, artefactos esperados, read models y rollback readiness.
- `validate_domain` queda `available_now=true` en `core/backend_internal_ui_contract.py`.
- El servicio no escribe, no materializa, no repara, no regenera, no ejecuta rollback, no activa runtime, no ejecuta agentes, no invoca modelos/tools y no toca integraciones.

**Consecuencias**:
- La futura UI podra mostrar diagnosticos y readiness sin modificar estado.
- Rollback/archive/delete/reset quedan separados en `PROMPT 7.5 - Servicio interno rollback/archive/delete/reset`.
- Runtime, execution, dry-run real, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel siguen bloqueados.

---

## ADR-056 - Acciones lifecycle sandbox controladas por validacion, confirmacion y manifest

**Estado**: Aceptado

**Prompt**: 7.5 - Servicio interno rollback/archive/delete/reset

**Contexto**:
Despues de `validate_domain`, IA_CORE necesita exponer acciones lifecycle internas para futura UI sin convertir rollback/archive/delete/reset en una operacion ambigua o peligrosa. La accion debe quedar limitada al sandbox controlado, con evidencia previa y confirmacion humana explicita.

**Decision**:
- IA_CORE expone `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain` mediante `core/backend_internal_domain_lifecycle_service.py`.
- Cada accion exige `sandbox_root` seguro, `validation_payload` de `validate_domain`, confirmacion humana explicita y paths declarados por manifest/created_paths.
- `rollback_sandbox` reutiliza rollback integral 6.1.
- `archive_sandbox_domain` mueve a `_archives` dentro del sandbox y no borra definitivamente.
- `delete_sandbox_domain` requiere `allow_delete=true`.
- `reset_sandbox_domain` requiere `allow_reset=true` y no regenera automaticamente.
- `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain` y `reset_sandbox_domain` quedan `available_now=true` en el contrato backend interno.
- Runtime, execution, dry-run real, agentes, modelos, tools, integraciones, UI visual, endpoints publicos, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

**Consecuencias**:
- La futura UI podra solicitar acciones lifecycle sin inferir logica critica ni saltarse confirmaciones.
- Las operaciones quedan trazadas, JSON-safe e idempotentes cuando corresponde.
- `domains/` operativo, repo root, `.git/`, `core/`, `docs/` y `tests/` quedan fuera del alcance de las acciones lifecycle.
- `PROMPT 7.6 - Payloads estables para futura UI` puede enfocarse en estabilizar forma de payload sin implementar UI visual ni runtime.

---

## ADR-057 - Payload envelope estable para futura UI backend interna

**Estado**: Aceptado

**Prompt**: 7.6 - Payloads estables para futura UI

**Contexto**:
Los servicios 7.1-7.5 ya devuelven payloads JSON-safe, pero cada uno usa estructura propia. Una futura UI necesita consumirlos sin inferir logica critica desde texto libre, sin interpretar flags de forma invertida y sin recibir rutas absolutas sensibles.

**Decision**:
- IA_CORE normaliza los resultados de servicios backend internos mediante `backend_internal_ui_payload.v1`.
- El envelope vive en `core/backend_internal_ui_payloads.py`.
- El envelope unifica service metadata, service_kind, status, readiness, domain/materialization, summary, data, warnings, errors, actions, blocked capabilities, meta y flags no-operativas.
- `blocked_capabilities` usa semantica `true = blocked`.
- Los payloads originales de 7.1-7.5 se preservan como `data.raw_payload` sanitizado.
- `stable_ui_payloads` queda `available_now=true` como `contract/payload-normalization`.
- Runtime, execution, dry-run real, agentes, modelos, tools, integraciones, UI visual, endpoints publicos, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

**Consecuencias**:
- La UI futura puede renderizar estados, errores y acciones disponibles de forma consistente.
- El backend conserva autoridad sobre permisos, seguridad, readiness y no-operatividad.
- 7.7 puede cerrar Fase 7 con checkpoint integral sin crear UI visual ni endpoints publicos.

---

## ADR-058 - Cierre de Fase 7 como contrato backend interno estable para futura UI

**Estado**: Aceptado

**Prompt**: 7.7 - Checkpoint integral contrato backend interno para UI

**Contexto**:
Fase 7 ya cuenta con contrato 7.0, servicios internos 7.1-7.5 y payload estable 7.6. Antes de avanzar a cualquier puente o exposicion interna para futura UI, IA_CORE necesita declarar que la frontera backend esta cerrada y que no se habilitaron runtime, execution, UI visual ni endpoints publicos.

**Decision**:
- IA_CORE considera Fase 7 cerrada cuando el contrato backend interno confirma servicios para status, preview, materializacion sandbox controlada, validacion, lifecycle y payloads estables.
- El cierre queda registrado por `BACKEND_INTERNAL_UI_CONTRACT_PHASE_7_CHECKPOINT_PASSED`.
- Los servicios confirmados son `list_domains_status`, `preview_materialization`, `materialize_sandbox`, `validate_domain`, `rollback_sandbox`, `archive_sandbox_domain`, `delete_sandbox_domain`, `reset_sandbox_domain` y `stable_ui_payloads`.
- El envelope estable sigue siendo `backend_internal_ui_payload.v1`, con `blocked_capabilities` usando semantica `true = blocked`.
- El backend conserva autoridad sobre permisos, readiness, acciones disponibles, acciones prohibidas, error contract, confirmaciones humanas y path safety.
- Fase 8 queda seleccionada como `Fase 8 - Exposicion interna controlada para futura UI`.
- El proximo prompt exacto es `PROMPT 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI`.
- Fase 7 no crea UI visual, no crea endpoints publicos, no activa runtime, no ejecuta agentes, no invoca modelos/tools, no toca integraciones y no toca `domains/` operativo.

**Consecuencias**:
- IA_CORE puede planificar una exposicion interna controlada para futura UI sin mover logica critica al frontend.
- Runtime, execution, dry-run real, tools, modelos, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.
- Fase 8 debera empezar como planificacion/control boundary, no como implementacion de UI visual ni endpoints publicos.

---

## ADR-059 - Fase 8 como exposicion interna controlada previa a UI visual

**Estado**: Aceptado

**Prompt**: 8.0 - Planificacion del bloque de exposicion interna controlada para futura UI

**Contexto**:
Fase 7 cerro el contrato backend interno para futura UI con servicios 7.1-7.6 y response envelope estable `backend_internal_ui_payload.v1`. Antes de construir UI visual o endpoints publicos, IA_CORE necesita planificar una capa intermedia que permita exponer internamente esos servicios sin convertirlos en runtime, API publica o logica frontend.

**Decision**:
- IA_CORE inicia Fase 8 como `Fase 8 - Exposicion interna controlada para futura UI`.
- Exposicion interna controlada significa capa backend interna para consultar o solicitar servicios internos contratados mediante payloads estables.
- Fase 8 no es UI visual, no es endpoint publico, no es router HTTP, no es runtime, no ejecuta agentes, no invoca modelos/tools, no toca integraciones y no toca `domains/` operativo.
- El backend conserva autoridad sobre permisos, readiness, confirmaciones, seguridad de paths, actions, errors y blocked capabilities.
- La futura UI solo podra consumir summaries, status, warnings/errors, readiness y actions declaradas por backend; no inferira permisos ni disponibilidad.
- El request envelope futuro queda planificado como `backend_internal_ui_request.v1`.
- La response envelope heredada sigue siendo `backend_internal_ui_payload.v1`.
- El proximo prompt exacto es `PROMPT 8.1 - Internal exposure registry / service map`.

**Consecuencias**:
- La futura UI podra apoyarse en una frontera interna estable sin recibir autoridad critica.
- La implementacion se realizara por etapas: registry, request validation, routing contractual, confirmation gate, response adapter y checkpoint.
- Runtime, execution, dry-run real, tools, modelos, integraciones, endpoints publicos, UI visual, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

---

## ADR-060 - Internal exposure registry como service map no-operativo

**Estado**: Aceptado

**Prompt**: 8.1 - Internal exposure registry / service map

**Contexto**:
Fase 8 fue planificada como exposicion interna controlada para futura UI, despues del cierre de Fase 7 y antes de cualquier request envelope, dispatcher, API o UI visual. IA_CORE necesita declarar que servicios backend internos pueden exponerse contractualmente sin habilitar ejecucion ni mover permisos al frontend.

**Decision**:
- IA_CORE crea `core/backend_internal_exposure_registry.py` como `internal_exposure_registry`.
- El registry es un service map read-only/contractual con schema `backend_internal_exposure_registry.v1`.
- El registry declara servicios exponibles, service kinds, input minimo, response schema `backend_internal_ui_payload.v1`, confirmaciones, side effects, destructive flags, blocked capabilities, forbidden actions, docs y tests fuente.
- `internal_exposure_registry` queda `available_now=true` en el contrato backend interno como `contract/internal-exposure-registry`.
- Backend conserva autoridad sobre permisos, readiness, confirmaciones, path safety, errores, allowed_actions, forbidden_actions y blocked capabilities.
- La futura UI no infiere permisos y no muta el registry.
- 8.1 confirma no dispatcher, no request handling, no UI visual, no endpoints publicos y no toca `domains/` operativo.

**Consecuencias**:
- Fase 8 puede avanzar a `PROMPT 8.2 - Internal request envelope y request validation` con un mapa estable de servicios.
- El registry no ejecuta servicios 7.x, no importa modulos operativos, no crea API real, no crea router HTTP, no activa runtime, no abre execution, no ejecuta dry-run real, no invoca modelos/tools y no toca integraciones.
- Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

---

## ADR-061 - Internal request envelope previo a dispatcher

**Estado**: Aceptado

**Prompt**: 8.2 - Internal request envelope y request validation

**Contexto**:
Despues del registry 8.1, IA_CORE necesita una forma estable de recibir solicitudes futuras desde UI/capa interna antes de cualquier dispatcher. La entrada debe validar service_id, caller, payload, confirmation y safety sin ejecutar servicios ni convertir la frontera en API publica.

**Decision**:
- IA_CORE introduce `backend_internal_ui_request.v1` como internal request envelope.
- El modulo vive en `core/backend_internal_request_envelope.py`.
- `internal_request_envelope` e `internal_request_validation` quedan disponibles ahora como contratos 8.2.
- El validador compara el request contra `internal_exposure_registry`, exige caller_kind permitido, payload JSON-safe, safety deny-by-default y requisitos de confirmation, validation_payload, preview_payload, allow_delete y allow_reset cuando correspondan.
- El resultado de validacion usa `backend_internal_ui_request_validation.v1` y mantiene `dispatcher_created=false`, `request_handling_enabled=false`, `operational=false`, `runtime_enabled=false` y `execution_enabled=false`.
- 8.2 confirma no dispatcher, no request handling, no routing, no ejecucion de servicios, no UI visual, no endpoints publicos y no toca `domains/` operativo.

**Consecuencias**:
- La futura capa 8.3 podra recibir requests ya validados por contrato.
- Backend conserva autoridad sobre permisos, confirmaciones, blocked capabilities y service exposure.
- Runtime, execution, dry-run real, tools, modelos, integraciones, Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

---

## ADR-062 - Internal dispatcher no-runtime y no-side-effect por defecto

**Estado**: Aceptado

**Prompt**: 8.3 - Internal dispatcher no-runtime/no-side-effect por defecto

**Contexto**:
Despues del request envelope 8.2, IA_CORE necesita decidir si un request validado puede despacharse internamente sin convertir el sistema en runtime executor ni abrir endpoints publicos. La decision debe conservar la autoridad backend y bloquear side effects prematuros.

**Decision**:
- IA_CORE introduce `core/backend_internal_dispatcher.py` como dispatcher interno contractual.
- El dispatcher valida request envelope 8.2, consulta registry 8.1 y aplica dispatch policy no-runtime/no-side-effect.
- Solo despacha servicios contractuales seguros: `stable_ui_payloads`, `internal_exposure_registry` e `internal_request_validation`.
- `materialize_sandbox` y lifecycle quedan bloqueados por `CONFIRMATION_GATE_REQUIRED` hasta 8.4.
- `internal_dispatcher_no_runtime` e `internal_dispatch_policy` quedan disponibles ahora en el contrato backend interno.
- No endpoints publicos, no API/router HTTP, no UI visual, no runtime, no execution, no agentes, no modelos/tools, no integraciones y no `domains/` operativo.

**Consecuencias**:
- Fase 8 puede avanzar a confirmation gate con una frontera de dispatch ya controlada.
- La exposicion interna puede decidir requests sin ejecutar side effects ni habilitar runtime.
- Market Catalog runtime, Business Composition Layer runtime, OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

---

## ADR-063 - Confirmation gate contractual para controlled-write/lifecycle

**Estado**: Aceptado

**Prompt**: 8.4 - Confirmation gate para controlled-write/lifecycle

**Contexto**:
Despues del dispatcher 8.3, los servicios `controlled_write` y
`controlled_lifecycle` necesitan una puerta de confirmacion humana antes de
cualquier adaptador futuro. Esta puerta debe validar intencion, scope y payload
sin ejecutar servicios ni abrir runtime.

**Decision**:
- IA_CORE introduce `core/backend_internal_confirmation_gate.py`.
- El gate devuelve `backend_internal_confirmation_gate_result.v1`.
- Valida `confirmed=true`, `human_confirmation_required=true`,
  `confirmation_scope`, `confirmed_by`, `confirmation_id`, sandbox root seguro,
  `preview_payload`, `validation_payload`, `allow_delete`, `allow_reset` y
  `gate_options` controladas.
- El dispatcher 8.3 integra el gate y puede devolver
  `confirmation_gate_passed=true` con `dispatch_allowed=true`, pero conserva
  `dispatch_executed=false`.
- `internal_confirmation_gate` y `confirmation_gate_validation` quedan
  disponibles como contratos 8.4.
- En el cierre de 8.4, `internal_response_adapter` quedaba como siguiente
  bloque para 8.5; ADR-064 registra su implementacion.

**Consecuencias**:
- Fase 8 avanza a `PROMPT 8.5 - Internal response adapter usando stable_ui_payloads`.
- La confirmacion humana queda validada antes de cualquier controlled execution adapter futuro.
- Runtime, execution, dry-run real, tools, modelos, integraciones, endpoints,
  UI runtime, Market Catalog runtime, Business Composition Layer runtime,
  OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.

---

## ADR-064 - Internal response adapter basado en stable_ui_payloads

**Estado**: Aceptado

**Prompt**: 8.5 - Internal response adapter usando stable_ui_payloads

**Contexto**:
Despues del registry 8.1, request envelope 8.2, dispatcher 8.3 y confirmation
gate 8.4, IA_CORE necesita una salida comun para futura UI sin obligar a la UI
a interpretar schemas internos distintos ni inferir permisos.

**Decision**:
- IA_CORE introduce `core/backend_internal_response_adapter.py`.
- El adapter normaliza resultados del exposure registry, request validation,
  dispatcher, dispatch policy y confirmation gate al envelope
  `backend_internal_ui_payload.v1`.
- `internal_response_adapter` y `stable_response_adapter` quedan disponibles
  ahora como `contract/response-adapter`.
- El adapter bloquea schemas desconocidos, payloads no JSON-safe, secrets,
  tracebacks crudos y paths absolutos sensibles.
- El adapter no ejecuta servicios, no despacha requests, no invoca confirmation
  gate como ejecucion, no abre endpoints, no crea UI, no activa runtime y no
  toca `domains/` operativo.

**Consecuencias**:
- La futura UI podra consumir respuestas internas homogeneas sin mover logica
  critica al frontend.
- Fase 8 avanza a `PROMPT 8.6 - Exposure audit checkpoint`.
- Runtime, execution, dry-run real, tools, modelos, integraciones, endpoints,
  UI runtime, Market Catalog runtime, Business Composition Layer runtime,
  OBLITERATUS y raw Package directo al User Panel permanecen bloqueados.
