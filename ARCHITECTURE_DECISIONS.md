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
