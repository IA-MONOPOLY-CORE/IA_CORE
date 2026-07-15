# Materializacion de profile_catalog en sandbox

## Proposito

`core/profile_catalog_materializer.py` materializa el primer artefacto interno real de un dominio sandbox: `profile_catalog`.

La materializacion no activa el dominio, no crea presets, no crea papers, no crea agentes y no escribe en `domains/` operativo. El resultado queda como patrimonio interno del sandbox, trazado por `artifact_manifest.json`.

## Entradas

- Un dominio sandbox ya materializado con `domain.json`.
- Un `materialization_manifest.json` valido.
- Un `source_request` trazable, con `area_id` y nichos derivados del preview.

El generador usado es:

```txt
core.professional_profile_catalog_generator.generate_profile_catalog_for_domain
```

## Salidas

Dentro del sandbox:

```txt
<sandbox>/<domain_id>/
  profile_catalog/profile_catalog.json
  manifests/artifact_manifest.json
```

`profile_catalog/profile_catalog.json` contiene el catalogo derivado y agrega metadata `sandbox_artifact` con:

- `artifact_id`;
- `artifact_type`;
- `version`;
- `status`;
- `domain_id`;
- `materialization_id`;
- marca no operativa.

## Artifact Manifest

El artefacto se registra como:

```txt
artifact_id: profile_catalog_main
artifact_type: profile_catalog
status: materialized
dependencies: []
rollback_info.safe_remove: true
```

`created_from` registra:

- dominio sandbox;
- `materialization_id`;
- `source_request`;
- generador;
- catalogos globales leidos.

## Regeneracion

La escritura duplicada esta bloqueada por defecto. Para regenerar se requiere `regenerate=True`.

La regeneracion:

- incrementa version patch (`1.0.0` a `1.0.1`);
- archiva el catalogo anterior en `profile_catalog/history/`;
- conserva historial en el artefacto;
- no crea un segundo `profile_catalog` en el manifest.

## Rollback

No hay rollback parcial por artefacto en esta fase.

El materializador registra los paths creados tanto en `artifact_manifest.json` como en `materialization_manifest.json`. El rollback completo del sandbox elimina el dominio y sus artefactos derivados.

## Limites

Esta fase no:

- activa el dominio;
- marca PASSED;
- crea `agent_presets`;
- crea papers;
- crea agentes;
- crea equipos;
- toca catalogos globales;
- toca dominios operativos;
- integra UI o proveedores externos.

## Auditoria de cierre

- `profile_catalog` queda tratado como artefacto/patrimonio del sandbox.
- `domain.json` conserva identidad y estado del dominio.
- `materialization_manifest.json` conserva materializacion y rollback completo.
- `artifact_manifest.json` conserva inventario, lineage, version y rollback por artefacto.
- La separacion Core / Domain / Artifact queda suficiente para avanzar hacia presets sin activar nada.
- La linea futura pendiente es definir rollback parcial real por artefacto cuando existan dependencias entre `profile_catalog`, presets, papers, agentes y teams.
