# Limpieza Legacy De Loteria

## Que se limpio

RESET 01 retiro del flujo operativo los agentes, papers, perfiles y presets legacy de Loteria. Los archivos operativos de `domains/loteria/agents/config` y `domains/loteria/agents/papers` fueron archivados en `docs/legacy/loteria` antes de retirarse.

`domains/loteria/profile_catalog.json` y `domains/loteria/agent_presets.json` quedaron como estructuras minimas validas, sin perfiles ni presets legacy activos.

## Que se preservo

- Snapshot de `profile_catalog.json`.
- Snapshot de `agent_presets.json`.
- Configs completas de 11 agentes.
- Papers completos de 11 agentes.
- Baseline de system prompts legacy en JSON y Markdown.
- Inventarios de agentes y papers.
- Manifest de limpieza.

## System prompts legacy preservados

Los baselines viven en `docs/legacy/loteria/legacy_system_prompts_baseline.json` y `docs/legacy/loteria/legacy_system_prompts_baseline.md`.

Incluyen Estadistico Integral, Gemini Cuantico, GPT Auditor, Nuevo DeepSeek, Viejo DeepSeek, Viejo Lobo y los agentes/presets restantes que tenian config con system prompt.

## Por que se limpio

Los agentes legacy nacieron antes de la Biblioteca Profesional Global. Servian como semilla conceptual, pero mantenian a Loteria como excepcion, mezclaban identidad historica con flujo nuevo y bloqueaban recrear agentes desde cero con el framework IA_CORE.

## Que queda de Loteria

Queda el dominio Loteria, sus archivos funcionales de dominio, su database/backtesting/scoring historico y catalogos minimos no operativos para mantener compatibilidad de carga.

No quedan agentes reales legacy en `domains/loteria/agents/config`. No quedan papers legacy en `domains/loteria/agents/papers`.

## Como se recrearan agentes luego

Los agentes deberan recrearse con una fase de materializacion controlada, tomando:

- perfil profesional global;
- arquetipo reutilizable;
- dominio, area, nicho, escala y objetivo;
- system prompt template nuevo;
- paper seed template;
- revision humana.

## Loteria no es excepcion

Loteria deja de conservar perfiles psicologicos activos propios. Los enfoques historicos pasan a la biblioteca global de arquetipos reutilizables.

## SAAOP como referencia historica

SAAOP/SAAOPS/S.A.A.O.P. queda preservado solo en backups, docs legacy o referencias historicas/deuda. No debe usarse como identidad activa en templates nuevos.

## Riesgos

- Algunos tests y flujos antiguos pueden asumir que existen 11 agentes activos.
- Algunos modulos legacy de Loteria todavia contienen nombres historicos y deben revisarse en una fase separada.
- HUD contiene referencias visibles antiguas, reportadas como deuda porque RESET 01 no toca HUD.

## Rollback y documentacion

Los snapshots completos en `docs/legacy/loteria` permiten reconstruir el estado anterior si hiciera falta. Cualquier rollback debe ser explicito y no debe reactivar identidad vieja como default del framework.
