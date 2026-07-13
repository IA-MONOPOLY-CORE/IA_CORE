# Inventario de dominios Loteria limpiados

Fecha: 2026-07-13

## Dominios encontrados

| ID | Nombre visible | Ruta | Origen estimado | Profile catalog | Agent presets | Agents | Papers | Activo/visible antes | Legacy | Duplicado/equivalente | Mecanismo UI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `loteria` | Loteria / IA_CORE | `domains/loteria` | historico / primer dominio creado | si, minimo no operativo | si, minimo no operativo | carpetas vacias tras RESET 01 | carpetas vacias tras RESET 01 | si | si | si | `GET /api/domains/list` escaneaba `domains/*/domain.json` |
| `loteria_analisis_de_juegos_de_azar` | Loteria - Analisis de Juegos de Azar | `domains/loteria_analisis_de_juegos_de_azar` | creado desde boton Dominio en UI | no | no | carpetas vacias | carpetas vacias | si, al tener `domain.json` | no trackeado/parcial | si | `GET /api/domains/list` escaneaba `domains/*/domain.json` |
| `demo_generico` | Demo generico | `domains/demo_generico` | demo interno | no | no | configs baseline demo | no | no, `visible_en_hud=false` y `es_demo=true` | no | no | oculto por `_is_internal_domain` |
| `codex_qa_prompt_2_20260707` | sin manifest | `domains/codex_qa_prompt_2_20260707` | sandbox/parcial | no | no | carpetas vacias | carpetas vacias | no, no tiene `domain.json` | no | no | no aparece; `list_domains()` requiere manifest |

## Dominio viejo detectado

- ID: `loteria`
- Nombre visible: Loteria / IA_CORE
- Ruta: `domains/loteria`
- Origen: historico / primer dominio creado.
- Estado antes de limpiar: legacy con archivos minimos no operativos, pero visible en el selector por no tener `visible_en_hud=false`.
- Contenido antes: `domain.json`, `profile_catalog.json`, `agent_presets.json`, modulos especificos de Loteria y carpetas `agents/config` y `agents/papers` vacias.

## Dominio nuevo creado desde UI

- ID: `loteria_analisis_de_juegos_de_azar`
- Nombre visible: Loteria - Analisis de Juegos de Azar
- Ruta: `domains/loteria_analisis_de_juegos_de_azar`
- Origen: creado desde el boton Dominio de la UI.
- Estado antes de limpiar: no trackeado, parcial, con `domain.json` y estructura de carpetas `agents/*` vacia.
- Profile catalog: no.
- Agent presets: no.
- Configs: no.
- Papers: no.

## Resultado

Ambos dominios representan el mismo concepto funcional: Loteria / analisis de juegos de azar. El dominio viejo queda preservado como referencia historica no visible; el dominio nuevo creado desde UI se remueve del flujo operativo luego de preservar snapshot documental.
