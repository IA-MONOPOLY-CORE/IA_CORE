# Manifest De Limpieza Legacy Loteria

Commit inicial: `a61e5b6`.

Advertencia: legacy preservado solo como fuente historica, no operativo.

## Que existia

- `domains/loteria/profile_catalog.json` con perfiles psicologicos legacy activos e inactivos.
- `domains/loteria/agent_presets.json` con presets operativos legacy.
- 11 configs de agentes en `domains/loteria/agents/config`.
- 11 papers en `domains/loteria/agents/papers`.

## Que se preservo

- Snapshot de profile catalog: `legacy_profile_catalog_snapshot.json`.
- Snapshot de agent presets: `legacy_agent_presets_snapshot.json`.
- Configs completas: `agents_config_snapshot/`.
- Papers completos: `legacy_papers_snapshot/`.
- Baselines de system prompts: `legacy_system_prompts_baseline.json` y `.md`.

## Que se elimino del flujo operativo

- Configs de agentes legacy bajo `domains/loteria/agents/config`.
- Papers legacy bajo `domains/loteria/agents/papers`.
- Perfiles y presets activos de Loteria.

## Que se transformo

- Los perfiles psicologicos historicos pasan a `catalogs/agent_archetypes.json` como arquetipos globales reutilizables.

## Que quedo pendiente

- Recrear agentes reales desde cero con materializacion controlada.
- Decidir que arquetipos se activan por dominio/nicho.
- Generar papers nuevos desde templates, no desde prompts legacy.

## Motivo

Loteria no debe quedar como excepcion del framework ni conservar agentes/perfiles psicologicos legacy activos.
