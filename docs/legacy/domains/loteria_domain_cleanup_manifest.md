# Limpieza de dominios Loteria duplicados

Fecha: 2026-07-13

Advertencia: preservado como referencia historica, no dominio operativo activo.

## Motivo

IA_CORE podia mostrar dominios duplicados o funcionalmente equivalentes en el selector de dominios. En particular coexistian:

- `loteria`: dominio historico visible como "Loteria / IA_CORE".
- `loteria_analisis_de_juegos_de_azar`: dominio no trackeado creado desde UI como "Loteria - Analisis de Juegos de Azar".

Ambos representaban el mismo concepto de trabajo: analisis de Loteria y juegos de azar. Ninguno debia quedar activo hasta ser recreado correctamente con el framework nuevo.

## Preservado

- Snapshot del dominio historico: `docs/legacy/domains/loteria_legacy_domain_snapshot.json`.
- Snapshot del dominio creado desde UI: `docs/legacy/domains/loteria_ui_created_domain_snapshot.json`.
- Inventario: `docs/legacy/domains/loteria_domain_inventory.md`.
- Legacy operativo anterior de agentes/papers/configs: `docs/legacy/loteria/`.

## Eliminado o desactivado

- `domains/loteria` queda con `visible_en_hud=false`, `status=legacy` y `legacy=true`.
- `domains/loteria_analisis_de_juegos_de_azar` se elimina del working tree operativo despues del snapshot.
- No se crean agentes, papers, presets reales ni dominios materializados.

## Contenido detectado en el dominio UI

- `domain.json`: si.
- `profile_catalog.json`: no.
- `agent_presets.json`: no.
- `agents/config/*.json`: no.
- `agents/papers/*.json`: no.
- `agents/memory_sources`: carpeta vacia.

Estado: no trackeado / no operativo / parcial.

## Regla nueva

La creacion de dominios llama a `core.domain_identity.validate_unique_domain()` desde `core.domain_registry.create_domain()`. La validacion compara nombres, ids/slugs, aliases, area/nicho y equivalencias conceptuales contra dominios activos, internos/legacy y snapshots archivados.

Mensaje esperado ante duplicados:

> Ya existe un dominio equivalente. No se pueden crear dominios duplicados. Revisa el dominio existente o usa otro nombre/nicho.

## Recreacion futura

Para recrear Loteria como dominio operativo se debe usar un flujo admin explicito: revisar el legacy, resetear/restaurar o crear una version realmente distinta con nuevo alcance, perfiles derivados desde la Biblioteca Profesional Global y estado claro. No debe reaparecer por simple creacion manual de un dominio equivalente.
