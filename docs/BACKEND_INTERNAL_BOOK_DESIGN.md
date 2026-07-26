# IA_CORE - Libro Backend Interno - Diseno

## 1. Proposito del libro

Este libro define el backend interno que debe convertir propuestas derivadas en artefactos operativos reales de forma controlada, testeable y reversible.

El libro no materializa nada por si mismo. Fija reglas, estados, contratos y criterios para una fase posterior donde IA_CORE pueda crear un dominio sandbox real, `profile_catalog`, `agent_presets`, papers, agentes, equipos, rollback, regeneracion segura y contrato backend estable para UI.

La UI no debe resolver logica de negocio, materializacion, validacion, rollback ni estados. La UI consume un backend interno estable.

## 2. Estado base posterior a CORE 01

La base auditada queda asi:

- La Biblioteca Profesional Global esta cerrada y documentada.
- `catalogs/professional_profiles.json` es fuente de verdad para perfiles profesionales globales.
- Matriz, recomendaciones, `profile_catalog`, `agent_presets`, team templates y validacion end-to-end son artefactos derivados y no operativos.
- RESET 01 archivo la identidad legacy de Loteria y movio arquetipos reutilizables a `catalogs/agent_archetypes.json`.
- CORE 01 agrego unicidad de dominios y bloqueo de dominios duplicados/equivalentes.
- `domains/loteria/domain.json` esta marcado como `status=legacy`, `legacy=true` y `visible_en_hud=false`.
- `domains/loteria/profile_catalog.json` y `domains/loteria/agent_presets.json` son estructuras minimas no operativas.
- Los snapshots legacy de dominios y Loteria viven en `docs/legacy/`.
- No hay dominio sandbox real materializado para este libro.

## 3. Principio PASSED aplicado al backend interno

Nada operativo puede quedar como fantasma.

Un artefacto operativo PASSED debe ser:

- validado;
- coherente;
- trazable;
- no duplicado;
- no legacy activo por accidente;
- no decorativo;
- ejecutable o consumible por el backend segun corresponda;
- cubierto por tests o validaciones;
- reversible cuando aplica;
- con errores legibles si falla.

`activo=true` o `status=active` no son decoracion: significan que el artefacto puede entrar en flujo operativo real.

## 4. Artefacto derivado vs artefacto operativo real

Artefacto derivado, preview o propuesta:

- Puede existir como simulacion, recomendacion, salida previa o fixture documental.
- No es operativo.
- No debe ser tratado como materializado.
- Puede contener gaps, warnings y riesgos.
- Puede vivir en `docs/`, `docs/generated/` o una salida temporal segura.
- No crea dominios, agentes, papers, presets ni equipos.

Artefacto operativo real:

- Existe en filesystem o registry operativo.
- Tiene estado.
- Tiene trazabilidad.
- Tiene validacion previa y posterior.
- Tiene rollback cuando aplica.
- Puede ser consumido por servicios internos o UI mediante contrato backend.
- Debe poder explicar su origen, version, dependencias y errores.

## 4.1 Contrato derivado vs operativo real

El contrato tecnico vive en `core/artifact_state.py`. Su objetivo es impedir que una salida calculada, sugerida o previsualizada sea confundida con un artefacto real de IA_CORE.

Estados definidos:

- `derived_preview`: salida generada para revision. No escribe artefacto operativo. No puede ser consumida como materializada.
- `ready_to_materialize`: salida derivada validada y lista para materializacion posterior. Todavia no es operativa.
- `materialized`: artefacto escrito en filesystem o registry sandbox con manifest o trazabilidad minima. No necesariamente activo.
- `active`: artefacto operativo PASSED, usable por backend o flujo correspondiente.
- `archived`: artefacto retirado del flujo activo, conservado por trazabilidad.
- `legacy`: artefacto historico conservado, no parte del flujo nuevo salvo recuperacion formal.
- `broken`: artefacto inconsistente, incompleto o fallido. No puede usarse.

Transiciones validas:

- `derived_preview -> ready_to_materialize`
- `ready_to_materialize -> materialized`
- `materialized -> active`
- `active -> archived`
- `materialized -> archived`
- `legacy -> ready_to_materialize` solo mediante recuperacion formal
- cualquier estado relevante puede pasar a `broken` si falla validacion critica
- `broken -> derived_preview` o `broken -> ready_to_materialize` solo mediante regeneracion validada

Transiciones invalidas:

- `derived_preview -> active`
- `ready_to_materialize -> active` sin materializacion
- `legacy -> active` sin recuperacion formal
- `broken -> active` sin reparacion
- `archived -> active` sin restore y validacion

Relacion con PASSED:

Solo `active` con trazabilidad completa equivale a PASSED operativo y puede aparecer como usable. `derived_preview`, `ready_to_materialize`, `materialized`, `archived`, `legacy` y `broken` no son opciones usables por defecto. Estados desconocidos, incluidos valores transicionales historicos como `proposed` o `draft`, no pasan como operativos.

Impacto sobre UI:

La UI puede mostrar previews, warnings y proximas acciones, pero no debe inferir que una propuesta existe operativamente. La UI debe consumir estado y permisos desde backend. Si un helper genera un `profile_catalog`, ese resultado es `derived_preview` o `ready_to_materialize`; no se vuelve real hasta escribirse bajo un sandbox con manifest y validacion.

Ejemplos:

- `profile_catalog` generado por helper: `derived_preview` / `ready_to_materialize`, no operativo.
- `profile_catalog` escrito dentro de `domains/sandbox_x/profile_catalog.json` con manifest: `materialized`.
- `profile_catalog` validado, consistente y usable: `active` / PASSED.
- `paper_seed_expected`: derivado, no paper real.
- paper real escrito y validado: `materialized` o `active` segun estado.

## 4.2 Inventario de artefactos actuales y previstos

Artefactos derivados detectados hoy:

- `derived_profile_catalog`: generado por `core/professional_profile_catalog_generator.py`; existe como salida derivada, no como catalogo operativo.
- `derived_agent_presets`: generado por `core/professional_agent_preset_generator.py`; existe como salida derivada, no como presets reales.
- `derived_team_template`: generado por `core/professional_team_template_generator.py`; existe como plantilla derivada, no como equipo real.
- `derived_model_recommendation`: generado por `core/professional_model_recommendation.py` y usado en generadores; recomendacion, no seleccion operativa obligatoria.
- `derived_paper_seed`: presente como `paper_seed_expected` y `paper_seed` en presets derivados; no es paper real.
- `derived_end_to_end_output`: generado por `core/professional_domain_end_to_end.py`; valida cadena completa sin modificar dominios.

Artefactos operativos reales detectados o previstos:

- `domain_registry_entry`: `domains/*/domain.json`, cargado por `core/domain_registry.py`; puede ser visible o interno segun estado/metadata.
- `materialized_domain`: implementado para sandbox controlado, no dominio operativo.
- `materialized_profile_catalog`: implementado bajo sandbox en `profile_catalog/profile_catalog.json`, registrado en `artifact_manifest.json`.
- `materialized_agent_presets`: implementado bajo sandbox en `agent_presets/agent_presets.json`, dependiente de `profile_catalog_main`.
- `materialized_paper_seed`: implementado bajo sandbox en `paper_seed/paper_seed.json`, dependiente de `profile_catalog_main` y `agent_presets_main`.
- `materialized_paper`: previsto para Fase 3 bajo `domains/<sandbox>/agents/papers/`; no se crea en Fase 0.
- `materialized_agent`: previsto para Fase 4 bajo `domains/<sandbox>/agents/config/`; no se crea en Fase 0.
- `materialized_team`: previsto para Fase 5 mediante manifest de equipo; no existe todavia.

Artefactos historicos o no operativos:

- `legacy_artifact`: Loteria historica y arquetipos recuperados en `docs/legacy/loteria/` y `catalogs/agent_archetypes.json`.
- `archived_artifact`: snapshots de dominios y legacy en `docs/legacy/`.
- `broken_artifact`: categoria reservada para artefactos incompletos, invalidos o fallidos; no debe aparecer como usable.

## 4.3 Administracion interna de dominios

El contrato tecnico de estados de dominio vive en `core/domain_state.py`. No reemplaza a `core/domain_identity.py`: identidad y duplicados siguen en `domain_identity`, mientras que estado, acciones internas y protecciones viven en `domain_state`.

Estados formales de dominio:

- `empty`: dominio sin contenido operativo todavia.
- `draft`: definicion inicial no lista para uso.
- `preview`: vista previa derivada antes de materializacion.
- `materialized`: dominio escrito y trazado por backend interno.
- `active`: dominio operativo PASSED.
- `archived`: dominio retirado del flujo activo pero conservado.
- `legacy`: dominio historico fuera del flujo nuevo.
- `broken`: dominio inconsistente o invalido.

Acciones internas:

- Archivar: retira un dominio de operacion, marca `status=archived`, apaga `visible_en_hud` y conserva el manifest, archivos y trazabilidad. No borra informacion.
- Restaurar: recupera un dominio archivado hacia `materialized` u otro estado no activo permitido. No activa directamente; `active` requiere validacion PASSED separada.
- Resetear: devuelve el dominio a `empty`, conserva manifest y trazabilidad, y no destruye patrimonio sin backup.
- Eliminar: accion destructiva controlada y ultimo recurso. `delete_domain_safely()` exige `confirm=True`, estado `archived`, trazabilidad previa y rechaza dominios `legacy`.

Protecciones:

- `legacy` no puede pasar directo a `active`.
- `archived`, `legacy`, `broken`, `empty`, `draft`, `preview` y `materialized` no aparecen en el registry activo por defecto.
- `broken` debe declarar `broken_reason`.
- `active` requiere trazabilidad minima.
- La UI futura debe consumir estas acciones desde backend; no debe inferir por su cuenta si puede archivar, resetear, restaurar o eliminar.

## 4.4 Contrato de preview de materializacion

El preview de materializacion vive en `core/domain_materialization_preview.py`. Es una capa obligatoria antes de crear cualquier dominio sandbox real.

Un preview responde:

- que dominio se quiere crear;
- desde que fuente de verdad sale;
- que perfiles profesionales recomienda;
- que presets derivados se generarian;
- que team template derivado compone;
- que recomendaciones de modelo aparecen;
- que paper seeds serian necesarios;
- que warnings, gaps y riesgos hay;
- que acciones faltan antes de materializar.

El preview no puede:

- crear carpetas en `domains/`;
- crear `profile_catalog.json` operativo;
- crear `agent_presets.json` operativo;
- crear papers;
- crear agentes;
- crear equipos;
- marcar nada como `active`;
- activar dominios.

Estados permitidos:

- `derived_preview`: preview generado para revision.
- `ready_to_materialize`: preview revisado y apto para alimentar una fase futura.
- `broken`: preview invalido o incompleto.

Relacion con PASSED:

Un preview, incluso si esta `ready_to_materialize`, no es PASSED operativo. PASSED aparece recien cuando una fase posterior materializa, valida, traza y marca el artefacto real como `active`.

Relacion con rollback futuro:

El preview define lo que se intentaria crear y sus dependencias. Esa informacion sera la base para manifest de materializacion y rollback, pero no ejecuta rollback ni escribe recursos por si misma.

## 4.5 Auditoria de rutas de creacion de dominio

Antes de disenar el schema sandbox real se auditaron las rutas que pueden crear, registrar, listar o mostrar dominios. El detalle vive en `docs/DOMAIN_CREATION_ROUTES_AUDIT.md`.

Motivo:

- evitar que un endpoint viejo, script suelto, helper directo, UI bypass o test mal armado cree dominios por fuera del backend interno;
- asegurar que unicidad, equivalencias, estados, reglas PASSED y preview previo a materializacion se apliquen desde servicios centrales;
- confirmar que `preview != dominio materializado` y que `materialized != active`.

Ruta oficial futura:

1. generar preview no operativo con `core/domain_materialization_preview.py`;
2. revisar gaps, riesgos y acciones requeridas;
3. materializar en una fase posterior con backend interno validado;
4. persistir manifest, trazabilidad y estado;
5. activar solo luego de PASSED explicito.

Rutas prohibidas:

- escritura publica directa en `domains/`;
- endpoint legacy que cree `domain.json` operativo sin preview;
- UI que materialice por su cuenta;
- scripts que escriban `profile_catalog.json` o `agent_presets.json` dentro de `domains/`;
- restores que vuelvan directo a `active`;
- listados que traten `legacy`, `archived`, `broken`, `preview`, `materialized` o estados desconocidos como activos.

Correccion aplicada:

- `/api/domains/create` queda bloqueado para el root operativo `domains/`.
- `list_domains()` usa el contrato de `core/domain_state.py` para decidir visibilidad activa.
- Los fixtures de tests solo pueden crear dominios en rutas temporales aisladas.

Relacion con `artifact_state` y `domain_state`:

- `artifact_state` gobierna outputs derivados y previews.
- `domain_state` gobierna manifests de dominio y acciones internas.
- Ninguna UI o integracion externa debe inferir materializacion, activacion, rollback ni reparacion sin consultar estos contratos.

## 4.6 Schema de dominio sandbox real

El schema de dominio sandbox real vive en `core/sandbox_domain_schema.py` y se documenta en `docs/SANDBOX_DOMAIN_SCHEMA.md`.

El schema viene antes de materializar porque la futura Fase 1 no puede crear carpetas o archivos sueltos en `domains/` sin contrato. Un sandbox materializado debe tener identidad, origen, estado, trazabilidad, validacion, revision humana y rollback desde su primer `domain.json`.

Garantiza:

- `domain_id` estable y normalizado;
- `domain_type=sandbox`;
- `status` controlado por `core/domain_state.py`;
- `artifact_state` controlado por `core/artifact_state.py`;
- `source_request` no vacio;
- `created_from` trazable;
- `materialization_id` no vacio;
- `rollback_manifest` presente;
- `human_review_required=true` en esta fase;
- payload serializable como JSON;
- bloqueo de `active` sin PASSED.

Evita dominios fantasma porque un `domain.json` incompleto, sin origen, sin rollback, con estado desconocido o con `active` prematuro falla validacion. Tambien bloquea fixtures que apunten rollback a `domains/` operativo real.

Conexion con preview:

- `source_request` puede venir de `core/domain_materialization_preview.py`.
- `created_from` puede referenciar `preview_id`.
- Un preview `ready_to_materialize` todavia no es dominio operativo; solo puede alimentar una futura materializacion controlada.

Conexion con rollback:

- `rollback_manifest.created_paths` listara paths creados por materializacion futura.
- `rollback_manifest.modified_paths` listara paths modificados.
- `rollback_manifest.backup_paths` listara backups necesarios.
- En PROMPT 1.0 no se ejecuta rollback real ni se materializa dominio persistente.

Conexion con UI futura:

- La UI no debe inferir si un sandbox existe, esta activo o puede operar.
- La UI futura debera consumir manifests validados por backend y mostrar errores accionables.
- `materialized` no es igual a `active`: `materialized` es existencia trazada; `active` exige PASSED posterior.

## 4.7 Materializacion sandbox controlada

La primera capa de materializacion sandbox vive en `core/domain_materializer.py` y se documenta en `docs/SANDBOX_MATERIALIZATION_FLOW.md`.

Flujo:

1. recibir un `domain_schema` validado por `core/sandbox_domain_schema.py`;
2. validar unicidad/equivalencias contra dominios reales e internos;
3. validar que el destino no sea `domains/` operativo;
4. generar `materialization_id`;
5. crear `<sandbox_root>/<domain_id>/domain.json`;
6. crear `<sandbox_root>/<domain_id>/materialization_manifest.json`;
7. registrar `rollback_manifest.created_paths`;
8. ejecutar validacion post materializacion.

Entradas:

- schema sandbox valido;
- raiz sandbox temporal o controlada;
- metadata opcional de ejecucion.

Salidas:

- `domain.json` sandbox materializado;
- `materialization_manifest.json`;
- resultado de validacion post-creacion.

Limites:

- no escribe en `C:\IA_CORE\domains`;
- no activa dominios;
- no registra dominios operativos;
- no crea `profile_catalog.json`;
- no crea `agent_presets.json`;
- no crea agentes, papers ni equipos.

Seguridad:

- toda escritura pasa por el materializador;
- se bloquea sobrescritura accidental;
- se bloquean duplicados y equivalentes legacy;
- `materialized` sigue sin ser `active`;
- rollback real queda preparado por manifest, pero no se ejecuta todavia.

## 4.8 Rollback y limpieza segura de sandbox

El rollback de materializacion sandbox vive en `core/domain_materialization_rollback.py`.

Criterio de cierre:

Una materializacion sandbox no esta completa si no puede revertirse de forma segura.

El rollback:

- lee `materialization_manifest.json`;
- valida que sea manifest sandbox;
- valida que todos los paths esten dentro de la raiz sandbox permitida;
- bloquea cualquier path hacia `C:\IA_CORE\domains`;
- elimina solo lo declarado en `created_paths`;
- conserva trazabilidad en `<sandbox_root>/_rollback_records/`;
- tolera ejecucion repetida sin romper;
- no activa, registra ni toca dominios legacy.

La limpieza segura deja el sandbox sin estructura fantasma y mantiene evidencia suficiente para auditoria. Backups y rollback de modificaciones quedan para fases posteriores si la materializacion llega a modificar artefactos existentes.

## 4.9 Ciclo de vida sandbox completo

El ciclo completo vive en `core/sandbox_lifecycle_validation.py` y se documenta en `docs/SANDBOX_LIFECYCLE.md`.

Secuencia validada:

1. preview valido;
2. schema sandbox valido;
3. materializacion controlada;
4. validacion post materializacion;
5. regeneracion segura;
6. rollback;
7. estado limpio.

Reglas:

- el `source_request` del schema debe ser trazable al preview;
- cada materializacion genera `materialization_id`;
- cada regeneracion incrementa `generation_number`;
- cada regeneracion conserva `previous_materialization_id`;
- `lifecycle_history` conserva materializaciones y rollbacks;
- no se sobrescribe silenciosamente;
- no se crea estado `active`;
- no se toca `domains/` operativo;
- no se toca legacy.

El ciclo permite repetir operaciones sin dominios fantasma: si existe una materializacion previa, la regeneracion ejecuta rollback controlado antes de recrear el sandbox desde origen valido.

## 4.10 Contrato de artefactos internos sandbox

El contrato de artefactos internos vive en `core/artifact_manifest_schema.py` y se documenta en `docs/ARTIFACT_MANIFEST_DESIGN.md`.

Objetivo:

- inventariar artefactos internos del sandbox;
- registrar lineage;
- representar dependencias;
- preparar rollback por artefacto;
- mantener estados con `core/artifact_state.py`.

Manifest minimo:

```txt
artifact_manifest.json
  artifact_manifest_version
  domain_id
  artifacts[]
```

Tipos preparados:

- `profile_catalog`
- `agent_preset`
- `paper_seed`
- `agent`
- `team`
- `memory`
- `model_recommendation`

Cada artefacto debe declarar:

- `artifact_id`;
- `artifact_type`;
- `version`;
- `status`;
- `created_from`;
- `created_by`;
- `dependencies`;
- `rollback_info`.

Regla:

Fase 2 no debe escribir `profile_catalog` ni `agent_presets` como archivos sueltos. Debe registrarlos en `artifact_manifest.json` y validar dependencias antes de considerarlos materializados.

## 4.11 Materializacion de profile_catalog sandbox

El primer artefacto interno materializable es `profile_catalog`.

Contrato implementado:

- servicio: `core/profile_catalog_materializer.py`;
- generador fuente: `core.professional_profile_catalog_generator.generate_profile_catalog_for_domain`;
- archivo de artefacto: `<sandbox>/<domain_id>/profile_catalog/profile_catalog.json`;
- manifest de artefactos: `<sandbox>/<domain_id>/manifests/artifact_manifest.json`;
- `artifact_id`: `profile_catalog_main`;
- `artifact_type`: `profile_catalog`;
- estado inicial: `materialized`;
- estado operativo: no activo, no PASSED.

Reglas:

- requiere dominio sandbox ya materializado;
- requiere `materialization_manifest.json`;
- bloquea duplicados salvo `regenerate=True`;
- la regeneracion incrementa version y conserva historial;
- registra paths en `artifact_manifest.json` y en `materialization_manifest.json`;
- no escribe en `domains/` operativo;
- no modifica catalogos globales;
- no crea `agent_presets`, papers, agentes ni equipos.

El detalle operativo queda documentado en `docs/PROFILE_CATALOG_SANDBOX_MATERIALIZATION.md`.

## 4.12 Materializacion de agent_presets sandbox

El segundo artefacto interno materializable es `agent_presets`.

Contrato implementado:

- servicio: `core/agent_preset_materializer.py`;
- generador fuente: `core.professional_agent_preset_generator.generate_agent_presets_for_profile_catalog`;
- archivo de artefacto: `<sandbox>/<domain_id>/agent_presets/agent_presets.json`;
- manifest de artefactos: `<sandbox>/<domain_id>/manifests/artifact_manifest.json`;
- `artifact_id`: `agent_presets_main`;
- `artifact_type`: `agent_preset`;
- dependencia: `profile_catalog_main`;
- estado inicial: `materialized`;
- estado operativo: no activo, no PASSED.

Reglas:

- requiere `profile_catalog` ya materializado;
- bloquea duplicados salvo `regenerate=True`;
- la regeneracion incrementa version y conserva historial;
- cada preset conserva referencia a perfil, rol, especializacion y policy de modelo;
- el rollback parcial elimina `agent_presets` sin eliminar `profile_catalog`;
- no crea agentes, papers ni equipos;
- no escribe en `domains/` operativo;
- no modifica catalogos globales.

El detalle operativo queda documentado en `docs/AGENT_PRESET_SANDBOX_MATERIALIZATION.md`.

## 4.13 Materializacion de paper_seed sandbox

El tercer artefacto interno materializable es `paper_seed`.

Contrato implementado:

- servicio: `core/paper_seed_materializer.py`;
- fuente: `paper_seed` embebido en cada preset materializado;
- archivo de artefacto: `<sandbox>/<domain_id>/paper_seed/paper_seed.json`;
- manifest de artefactos: `<sandbox>/<domain_id>/manifests/artifact_manifest.json`;
- `artifact_id`: `paper_seed_main`;
- `artifact_type`: `paper_seed`;
- dependencias: `profile_catalog_main`, `agent_presets_main`;
- estado inicial: `materialized`;
- estado operativo: no activo, no PASSED.

Reglas:

- requiere `profile_catalog` y `agent_presets` ya materializados;
- bloquea duplicados salvo `regenerate=True`;
- la regeneracion incrementa version y conserva historial;
- cada seed conserva referencia a perfil y preset;
- el rollback parcial elimina `paper_seed` sin eliminar `profile_catalog` ni `agent_presets`;
- no crea papers operativos, agentes ni equipos;
- no escribe en `domains/` operativo;
- no modifica papers globales.

El detalle operativo queda documentado en `docs/PAPER_SEED_SANDBOX_MATERIALIZATION.md`.

## 4.14 Contrato de agente sandbox

Antes de materializar agentes reales, el sistema define un contrato validable de agente sandbox.

Contrato implementado:

- schema: `core/sandbox_agent_schema.py`;
- documentacion: `docs/SANDBOX_AGENT_CONTRACT.md`;
- `artifact_type` futuro: `agent`;
- dependencias: `profile_catalog_main`, `agent_presets_main`, `paper_seed_main`;
- estado permitido: `ready_to_materialize`, `materialized`, `archived` o `broken`;
- estado bloqueado: `active`.

Reglas:

- el contrato no crea agentes;
- no escribe configs en `agents/`;
- no toca dominios operativos;
- valida referencias a perfil, preset y paper seed;
- valida rollback futuro;
- representa compatibilidad con `artifact_manifest.json`;
- deja memoria, herramientas, runtime y equipos para fases posteriores.

El agente sandbox se entiende como activo trazable compuesto por identidad, rol, especializacion, modelo recomendado, conocimiento asociado y ciclo de vida.

## 4.15 Lineage de agentes sandbox

Antes de crear agentes sandbox reales, el sistema define lineage evolutivo de agente.

Contrato implementado:

- schema: `core/agent_lineage_schema.py`;
- documentacion: `docs/AGENT_LINEAGE_DESIGN.md`;
- entidad: `agent_lineage`;
- cadena: `profile_catalog_main -> agent_presets_main -> paper_seed_main -> agent_identity -> agent`;
- estrategia de identidad: `agent_id` estable para regeneraciones y actualizaciones; reemplazos trazados con `replaced_by`;
- historial: eventos versionados en `history`;
- compatibilidad: metadata embebible en `artifact_manifest.created_from.lineage`.

Reglas:

- lineage no crea agentes;
- no escribe configs en `agents/`;
- no crea memoria operativa;
- no duplica dependencias del `artifact_manifest`;
- conserva origen, version actual, artefactos relacionados, reemplazos e historial.

La memoria futura debe ser artefacto separado si se vuelve persistente, compartida, vectorial o asociada a herramientas con estado.

## 4.16 Materializacion de agentes sandbox

El sistema ya puede materializar una configuracion de agente dentro del sandbox sin activar ejecucion.

Contrato implementado:

- servicio: `core/sandbox_agent_materializer.py`;
- documentacion: `docs/SANDBOX_AGENT_MATERIALIZATION.md`;
- carpeta: `<sandbox>/<domain_id>/sandbox_agents/<agent_id>.json`;
- `artifact_type`: `agent`;
- dependencias: `profile_catalog_main`, `agent_presets_main`, `paper_seed_main`;
- estado inicial: `materialized`;
- runtime: deshabilitado.

Reglas:

- requiere `profile_catalog`, `agent_presets` y `paper_seed` materializados;
- registra lineage;
- registra agente en `artifact_manifest.json`;
- bloquea duplicados salvo `regenerate=True`;
- la regeneracion conserva `agent_id` e incrementa version;
- rollback elimina solo el agente sandbox;
- no escribe en `agents/` runtime;
- no crea memoria operativa;
- no activa agentes.

Esta capa crea identidad y configuracion sandbox, no operacion real.

## 4.17 Checkpoint extremo de confiabilidad y usabilidad sandbox

PROMPT 2.4.1 valida la cadena sandbox desde minimo controlado hasta stress maximo actual controlado.

Entregables:

- tests: `tests/test_sandbox_chain_checkpoint.py`;
- tests: `tests/test_sandbox_chain_maximum_checkpoint.py`;
- reporte: `docs/SANDBOX_CHAIN_RELIABILITY_CHECKPOINT.md`.

Resultado:

- minimo controlado: `PASSED`;
- biblioteca detectada: 30 areas, 200 nichos, 106 perfiles, 20 roles, 80 especializaciones;
- stress ejecutado: 12 dominios reales, 295 perfiles, 295 presets, 295 paper_seed, 295 agentes sandbox;
- rollback selectivo: `PASSED`;
- rollback total: `PASSED`;
- runtime boundary: `PASSED`;
- legacy isolation: `PASSED`;
- maximo completo 200/200: `PARTIAL`.

Estado antes de PROMPT 2.5:

```txt
subprompt de refuerzo antes de 2.5
```

Refuerzo recomendado: benchmark largo y metricas persistentes de escala sandbox 200/200 antes de avanzar a memoria, herramientas, equipos, activacion o runtime.

## 5. Alcance del libro

Este libro cubre solo backend interno:

- estados internos de artefactos;
- preview y validacion;
- aprobacion interna o humana cuando corresponda;
- materializacion sandbox;
- manifest de materializacion;
- trazabilidad;
- rollback;
- regeneracion segura;
- errores accionables;
- contrato backend estable para UI;
- fixtures y tests de contrato.

## 6. Fuera de alcance explicito

Quedan fuera de este libro o de este prompt:

- UI/UX final;
- HUD final;
- n8n;
- Hermes Agent;
- Home Assistant;
- WhatsApp;
- Gmail;
- Sheets;
- Calendar;
- Drive;
- CRM;
- APIs externas;
- dominios productivos reales sin sandbox previo;
- ejecucion externa sin aprobacion;
- recuperacion completa del legacy historico de Loteria;
- orquestador principal futuro;
- automatizaciones externas;
- integraciones con providers en vivo salvo validaciones posteriores explicitamente aprobadas.

Las integraciones futuras pueden quedar como direccion conceptual, no como implementacion.

## 7. Fases del libro

### Fase 0 - Reglas internas, estados y contrato de materializacion

- Objetivo: definir estados, tipos de artefacto, invariantes, permisos y contrato conceptual.
- Entregable esperado: documento tecnico y tests unitarios de estados/contrato si se implementa codigo.
- Puede tocar: docs, constantes/modelos internos si un prompt posterior lo autoriza.
- No debe tocar: dominios reales, UI final, integraciones externas.
- Criterio de cerrado: estados y transiciones quedan definidos, testeados si hay codigo, y sin ambiguedad entre derivado y operativo.
- Tests esperables: validacion de estados, transiciones invalidas, errores legibles.
- Riesgos: sobredisenar antes de materializar; mezclar preview con operacion.
- Posibles subprompts: `PROMPT 0.1 - Estados internos y contrato de materializacion`.

### Fase 1 - Dominio sandbox real

- Objetivo: crear un dominio sandbox controlado para probar materializacion sin afectar dominios historicos.
- Entregable esperado: dominio sandbox con manifest, estado, trazabilidad y no equivalencia con dominios existentes.
- Puede tocar: carpeta sandbox bajo `domains/` solo cuando el prompt lo autorice.
- No debe tocar: Loteria legacy, dominios productivos, snapshots legacy.
- Criterio de cerrado: dominio visible solo segun estado definido, no duplicado, con rollback o limpieza documentada.
- Tests esperables: unicidad, visibilidad, estado, schema de `domain.json`.
- Riesgos: crear otro dominio vacio que parezca operativo.
- Posibles subprompts: `PROMPT 1.0 - Crear dominio sandbox real`.

### Fase 2 - Materializacion de profile_catalog y presets

- Objetivo: convertir derivados aprobados en `profile_catalog.json` y `agent_presets.json` sandbox reales.
- Entregable esperado: artefactos sandbox registrados en `artifact_manifest.json` y validados contra catalogos globales.
- Puede tocar: carpeta del sandbox materializado y sus subcarpetas de artefactos.
- No debe tocar: catalogos globales salvo bug bloqueante reportado, dominios productivos.
- Criterio de cerrado: cada artefacto materializado tiene manifest, version, dependencias internas, trazabilidad a perfil global y estado no activo hasta una aprobacion posterior.
- Tests esperables: consistencia profile/preset, schemas, active_only, gaps rechazados.
- Riesgos: copiar outputs derivados sin aprobacion; perder source ids.
- Posibles subprompts: `PROMPT 2.0 - Materializar profile_catalog sandbox`.

### Fase 3 - Papers reales y memoria documental

- Objetivo: materializar papers minimos reales para agentes sandbox aprobados.
- Entregable esperado: papers versionados, trazables a preset/profile y validables.
- Puede tocar: `domains/<sandbox>/agents/papers/` y manifest documental del sandbox.
- No debe tocar: papers legacy, memoria externa, integraciones.
- Criterio de cerrado: cada paper requerido existe, tiene origen, alcance, limites, criterios y estado.
- Tests esperables: existencia, schema, referencias a preset/agente, no placeholders.
- Riesgos: generar papers decorativos o demasiado generales.
- Posibles subprompts: `PROMPT 3.0 - Materializar papers sandbox`.

### Fase 4 - Agentes reales sandbox

- Objetivo: crear agentes ejecutables dentro del sandbox desde presets y papers PASSED.
- Entregable esperado: configs de agentes sandbox con metadata, modelo, paper y policy coherentes.
- Puede tocar: `domains/<sandbox>/agents/config/`.
- No debe tocar: agentes legacy, UI final, providers externos.
- Criterio de cerrado: agentes cargan, validan y no dependen de defaults criticos ocultos.
- Tests esperables: schema de agente, carga runtime, referencias paper/preset, errores.
- Riesgos: crear agentes con prompts genericos o sin paper real.
- Posibles subprompts: `PROMPT 4.0 - Materializar agentes sandbox`.

### Fase 5 - Equipos reales sandbox

- Objetivo: componer agentes sandbox en equipos operativos minimos.
- Entregable esperado: team manifest con roles, dependencias, objetivo y criterios.
- Puede tocar: manifest de equipos sandbox si se define ubicacion.
- No debe tocar: orquestador futuro principal ni automatizaciones externas.
- Criterio de cerrado: cada equipo referencia agentes reales, tiene objetivo, limites, outputs y estado.
- Tests esperables: referencias cruzadas, roles obligatorios, ausencia de agentes inexistentes.
- Riesgos: llamar equipo a una lista decorativa de agentes.
- Posibles subprompts: `PROMPT 5.0 - Materializar equipos sandbox`.

### Fase 6 - End-to-end operativo, rollback y regeneracion

- Objetivo: probar el ciclo completo desde intencion hasta artefactos reales con rollback y regeneracion segura.
- Entregable esperado: flujo backend interno reproducible, manifest y reporte de validacion.
- Puede tocar: servicios backend internos y sandbox.
- No debe tocar: UI final ni integraciones externas.
- Criterio de cerrado: puede materializar, validar, revertir y regenerar sin duplicar ni pisar cambios manuales.
- Tests esperables: e2e sandbox, rollback parcial/total, idempotencia, conflictos.
- Riesgos: rollback incompleto; regeneracion destructiva.
- Posibles subprompts: `PROMPT 6.0 - End-to-end sandbox con rollback`.

### Fase 7 - Contrato backend para UI

- Objetivo: exponer endpoints o funciones internas estables para que la UI consuma previews, estados y acciones.
- Entregable esperado: contrato versionado para preview, validation, materialization, status, rollback y next_actions.
- Puede tocar: backend/API interno y documentacion de contrato.
- No debe tocar: UI final salvo fixtures o smoke minimo autorizado.
- Criterio de cerrado: la UI no necesita inferir estados ni reglas de negocio.
- Tests esperables: contrato de respuestas, codigos de error, payloads estables.
- Riesgos: filtrar decisiones de negocio hacia frontend.
- Posibles subprompts: `PROMPT 7.0 - Contrato backend/UI`.

### Fase 8 - Tests de contrato, errores y fixtures

- Objetivo: fijar fixtures y pruebas de errores legibles para UI.
- Entregable esperado: suite de contrato con casos PASSED, warnings, conflicts y failures.
- Puede tocar: tests, fixtures y helpers internos.
- No debe tocar: dominios productivos ni integraciones.
- Criterio de cerrado: los errores son accionables y los fixtures representan estados reales.
- Tests esperables: snapshots/payloads, errores por duplicado, falta de aprobacion, rollback no disponible.
- Riesgos: tests que solo congelan forma sin validar significado.
- Posibles subprompts: `PROMPT 8.0 - Fixtures y errores de contrato`.

### Fase 9 - Cierre del backend interno

- Objetivo: consolidar evidencia, deuda futura y criterio de salida hacia UI/productivo.
- Entregable esperado: reporte de cierre, tests verdes, commit limpio.
- Puede tocar: documentacion de cierre y decisiones arquitectonicas reales.
- No debe tocar: nuevas features laterales.
- Criterio de cerrado: sandbox demuestra operacion controlada y la UI tiene contrato estable.
- Tests esperables: suite completa relevante, contrato, e2e sandbox.
- Riesgos: cerrar por relato sin evidencia.
- Posibles subprompts: `PROMPT 9.0 - Cierre Backend Interno`.

## 8. Criterios de cierre por fase

Cada fase cierra solo si:

- sus entregables existen;
- no materializa piezas fuera de su alcance;
- conserva trazabilidad;
- tiene tests reales o validaciones ejecutables acordes al riesgo;
- reporta gaps, warnings y riesgos;
- deja `git status --short` limpio despues del commit;
- no introduce dominios duplicados o legacy activo por accidente.

## 9. Criterios de cierre para dominio sandbox

Un dominio sandbox cierra PASSED si:

- no es equivalente a dominios activos, legacy o archivados;
- tiene `domain.json` valido;
- declara estado explicito;
- su visibilidad no confunde sandbox con productivo;
- tiene manifest de origen;
- no depende de Loteria ni de defaults legacy;
- puede eliminarse o revertirse segun politica del libro.

## 10. Criterios de cierre para profile_catalog sandbox

`profile_catalog` sandbox cierra PASSED si:

- deriva de `catalogs/professional_profiles.json` o de una fuente aprobada;
- conserva `source_profile_id`;
- valida `role_id` y `specialization_id`;
- no expone perfiles sin preset esperable;
- separa activos de inactivos;
- no contiene proposed/draft usables;
- tiene errores legibles ante referencias invalidas.

## 11. Criterios de cierre para agent_presets sandbox

`agent_presets` sandbox cierra PASSED si:

- cada preset corresponde a un perfil activo del sandbox;
- conserva trazabilidad a perfil global y profile_catalog;
- incluye system prompt revisado, decision criteria, avoid, memory policy y paper seed;
- incluye policy o recomendacion de modelo;
- no promete resultados garantizados;
- no queda como semilla decorativa tratada como agente real.

## 12. Criterios de cierre para papers

Un paper real cierra PASSED si:

- existe como archivo operativo en el sandbox;
- referencia agente, preset, perfil y dominio;
- contiene identidad, alcance, metodologia, limites, riesgos y criterios de actualizacion;
- no copia legacy como identidad activa;
- no es un placeholder;
- puede validarse por schema o reglas internas.

## 13. Criterios de cierre para agentes reales sandbox

Un agente sandbox cierra PASSED si:

- tiene config ejecutable;
- referencia paper existente;
- referencia preset/profile validos;
- declara provider/model o policy resuelta;
- conserva metadata de origen;
- carga desde backend sin ambiguedad;
- falla con error legible si falta una dependencia.

## 14. Criterios de cierre para equipos reales sandbox

Un equipo sandbox cierra PASSED si:

- referencia agentes reales existentes;
- declara objetivo, roles, interaccion, outputs, limites y riesgos;
- no depende de agentes decorativos;
- puede validarse sin ejecutar integraciones externas;
- tiene manifest y estado.

## 15. Criterios de cierre para end-to-end operativo sandbox

El e2e sandbox cierra PASSED si demuestra:

- input/intencion;
- preview;
- validacion;
- aprobacion cuando corresponda;
- materializacion;
- manifest;
- validacion post-materializacion;
- exposicion por contrato backend;
- rollback disponible;
- regeneracion segura;
- errores legibles para casos negativos.

## 16. Criterios de cierre para rollback

Rollback cierra PASSED si:

- conoce exactamente que archivos y registros creo o modifico;
- puede revertir por manifest;
- distingue rollback total y parcial si aplica;
- no borra artefactos preexistentes no creados por la operacion;
- reporta estado final y fallas;
- tiene tests de conflicto e idempotencia.

## 17. Criterios de cierre para regeneracion segura

Regeneracion segura cierra PASSED si:

- compara origen, version y manifest previo;
- detecta cambios manuales;
- no sobrescribe sin aprobacion;
- conserva historial o snapshot cuando aplica;
- no duplica dominios ni artefactos;
- deja evidencia auditable.

## 18. Criterios de cierre para contrato backend/UI

El contrato backend/UI cierra PASSED si:

- versiona endpoints o funciones internas;
- entrega `status`, `artifact_type`, `operational`, `traceability`, `warnings`, `errors` y `next_actions` cuando aplique;
- separa preview, validation, materialization, status, rollback y regeneration;
- no exige que la UI infiera reglas de negocio;
- cubre errores esperables con payload estable;
- tiene tests de contrato.

## 19. Criterios de errores legibles para UI

Un error legible para UI debe incluir:

- codigo estable;
- mensaje humano claro;
- severidad;
- artefacto afectado;
- estado actual;
- causa probable;
- accion recomendada;
- si la accion es reintentable;
- si requiere aprobacion humana;
- referencias de trazabilidad disponibles.

La UI puede mostrar el error, pero no resolver la regla que lo produjo.

## 20. Contrato conceptual de materializacion controlada

Flujo esperado:

```text
input/intencion
-> preview
-> validacion
-> aprobacion interna/humana cuando corresponda
-> materializacion sandbox
-> manifest
-> validacion post-materializacion
-> rollback disponible
-> regeneracion segura
-> exposicion por contrato backend
```

Este flujo queda disenado, no implementado en este prompt.

## 21. Limites UI/backend

La UI puede:

- pedir previews;
- mostrar estados;
- mostrar errores;
- pedir validaciones;
- pedir materializacion cuando el backend lo permita;
- mostrar `next_actions`.

La UI no debe:

- decidir reglas de negocio;
- crear archivos por su cuenta;
- inferir estados;
- reparar inconsistencias;
- materializar sin backend;
- saltear validaciones;
- inventar defaults criticos;
- resolver rollback.

## 22. Riesgos principales

- Confundir artefactos derivados con operativos.
- Crear un sandbox vacio visible como producto real.
- Activar legacy por accidente.
- Copiar seeds como prompts finales.
- Materializar sin rollback.
- Sobrescribir trabajo manual durante regeneracion.
- Dejar a la UI interpretando reglas internas.
- Agregar integraciones externas antes de cerrar el core interno.

## 23. Subprocesos esperables

- Definir modelo de estados internos.
- Definir manifest de materializacion.
- Definir formato de preview.
- Definir politica de aprobacion humana.
- Crear dominio sandbox real.
- Materializar `profile_catalog` sandbox.
- Materializar `agent_presets` sandbox.
- Materializar papers reales.
- Crear agentes reales sandbox.
- Crear equipos sandbox.
- Implementar rollback y regeneracion segura.
- Versionar contrato backend/UI.
- Crear fixtures de contrato y errores.

## 24. Deudas futuras documentadas

- Panel admin de dominios con archivar, restaurar, resetear, eliminar y ver dependencias.
- Recuperacion legacy de Loteria solo como libro o subprompt separado.
- Validacion de providers/modelos en vivo.
- Integracion n8n y automatizaciones externas.
- Orquestador principal futuro.
- UI/UX final sobre contrato backend estable.
- Politicas de permisos por usuario o rol.
- Versionado formal de manifests y migraciones.

## 25. Inconsistencias detectadas durante el diseno

No se detecto una inconsistencia bloqueante para crear este documento.

Condicionantes no bloqueantes:

- El documento externo de Direccion de Producto no aparece como archivo versionado dentro del repo; el diseno usa el prompt adjunto como fuente vigente de direccion.
- Existen archivos legacy de Loteria en `domains/loteria/`, pero el dominio esta oculto y marcado como legacy, coherente con CORE 01.
- El README del repo se considera documento tecnico viejo, no brujula estrategica.

No corresponde abrir `PROMPT 0.0.1` antes de cerrar este prompt.

## 26. PROMPT 2.4.2 - Benchmark largo sandbox 200/200 y metricas persistentes

Estado: `PASSED_FULL_200`.

Evidencia:

- runner: `scripts/run_sandbox_full_benchmark.py`;
- test: `tests/test_sandbox_chain_full_benchmark.py`;
- metricas: `docs/benchmarks/sandbox_full_200_benchmark.json`;
- reporte: `docs/SANDBOX_FULL_200_BENCHMARK_REPORT.md`.

Resultado medido:

- areas detectadas: 30;
- nichos detectados: 200;
- combinaciones detectadas: 200;
- dominios intentados/materializados: 200/200;
- profile_catalogs: 200;
- perfiles/presets/paper_seed/agentes sandbox: 3175/3175/3175/3175;
- fallos de artifact_manifest, lineage, runtime boundary y legacy isolation: 0;
- rollback selectivo: 65/65;
- rollback total: 200/200;
- regeneracion representativa: 4/4;
- duracion total: 648.316 s.

Decision:

IA_CORE soporta la escala full actual de la biblioteca profesional en sandbox temporal para la cadena `domain -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agent`, sin activar runtime ni tocar flujos operativos. Queda listo para avanzar a PROMPT 2.5.

## 27. PROMPT 2.5 - Contrato de memoria y herramientas para agentes sandbox

Estado: `PASSED`.

Evidencia:

- memoria declarativa: `core/sandbox_agent_memory_contract.py`;
- herramientas declarativas: `core/sandbox_agent_tool_contract.py`;
- integracion opcional: `core/sandbox_agent_schema.py`;
- tests: `tests/test_sandbox_agent_memory_tool_contract.py`;
- documentacion: `docs/SANDBOX_AGENT_MEMORY_TOOL_CONTRACT.md`.

Decision:

Los agentes sandbox pueden declarar capacidades futuras en `capabilities.memory` y `capabilities.tools`, pero no pueden activarlas ni ejecutarlas. La fase solo permite `declared_only=true`; memoria exige `runtime_enabled=false`; herramientas exigen `runtime_enabled=false`, `execution_allowed=false` y `external_access=false`.

Relaciones futuras:

- memoria persistente o compartida deberia ser artefacto futuro separado si contiene estado propio, indices, aprendizaje o rollback independiente;
- herramientas quedan como capability declarativa por ahora y deberian pasar a artefacto/policy futuro si requieren permisos, estado, auditoria o ejecucion;
- se recomienda una `capability_policy` antes de activar memoria o herramientas reales.

Limites:

- no se implemento memoria real;
- no se implementaron herramientas reales;
- no se activo runtime;
- no se tocaron UI, integraciones, `agents/` legacy, `domains/` operativo, catalogos globales ni papers globales.

## 28. PROMPT 2.6 - Contrato de equipo sandbox antes de materializacion

Estado: `PASSED`.

Evidencia:

- schema: `core/sandbox_team_schema.py`;
- tests: `tests/test_sandbox_team_schema.py`;
- documentacion: `docs/SANDBOX_TEAM_CONTRACT.md`.

Decision:

El equipo sandbox queda definido como contrato de coordinacion, no como ejecucion. Puede declarar miembros, objetivo, dependencias sobre agentes sandbox, coordinacion declarativa y capacidades futuras, pero no crea equipos reales, no ejecuta agentes, no activa runtime y no materializa artefactos.

Reglas:

- estado permitido en esta fase: `materialized` como contrato validado, no operativo;
- `active`, `runtime_enabled=true` y `execution_enabled=true` quedan bloqueados;
- miembros duplicados o sin responsabilidad fallan;
- `coordination_model` declara estructura, no debate/pipeline/orquestacion real;
- capabilities de equipo (`memory`, `tools`, `policies`) son declarativas y no ejecutables;
- futura materializacion debera registrarse como `artifact_type: team`.

Relacion arquitectonica:

El equipo depende de agentes sandbox (`agent_<agent_id>`), no de presets directamente. Los presets quedan como dependencia indirecta de cada agente. Antes de runtime real se recomienda cerrar una `capability_policy` comun para agentes y equipos.

## 29. PROMPT 2.7 - Materializacion de equipos sandbox

Estado: `PASSED`.

Evidencia:

- materializador: `core/sandbox_team_materializer.py`;
- tests: `tests/test_sandbox_team_materialization.py`;
- documentacion: `docs/SANDBOX_TEAM_MATERIALIZATION.md`.

Decision:

Los equipos sandbox quedan materializados como artefactos trazables dentro del sandbox, no como runtime. El equipo agrupa agentes sandbox existentes, registra `artifact_type: team` en `artifact_manifest`, conserva dependencias base y dependencias `agent_<agent_id>`, y mantiene bloqueados runtime, ejecucion, debate real, pipelines reales, memoria real y herramientas reales.

Flujo:

```txt
domain sandbox
-> profile_catalog
-> agent_presets
-> paper_seed
-> sandbox_agents
-> sandbox_team
```

Controles:

- miembros requeridos y existentes;
- duplicados bloqueados;
- coordinacion declarativa validada;
- capabilities declarativas validadas;
- rollback elimina solo el equipo y conserva agentes/dependencias;
- regeneracion incrementa version y conserva identidad/dependencias;
- sin escritura en `agents/`, `domains/` operativo, catalogos globales ni papers globales.

Riesgo futuro:

Antes de ejecutar equipos reales sigue siendo necesaria una `capability_policy` comun para agentes/equipos.

## 30. PROMPT 2.7.1 - Checkpoint end-to-end con equipos sandbox antes de capability_policy

Estado: `PASSED_TEAM_CHAIN`.

Evidencia:

- test: `tests/test_sandbox_chain_with_team_checkpoint.py`;
- reporte: `docs/SANDBOX_TEAM_CHAIN_CHECKPOINT.md`.

Decision:

La cadena completa `domain -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agents -> sandbox_team` queda validada en sandbox temporal. El checkpoint confirma manifest consistente, lineage de agentes conservado, dependencias de team correctas, runtime boundary, legacy isolation, rollback selectivo, rollback total y regeneracion de equipo.

Resultado:

- `sandbox_team` registrado como `artifact_type: team`;
- dependencias del team en manifest: `profile_catalog_main`, `agent_presets_main`, `paper_seed_main`, `agent_<agent_id>`;
- equipo depende contractualmente de agentes sandbox;
- rollback de equipo conserva agentes y dependencias base;
- regeneracion conserva `team_id`, miembros y dependencias;
- no se ejecutan agentes/equipos;
- no se implementa `capability_policy`.

Recomendacion:

Listo para `capability_policy`.

## 31. PROMPT 2.8 - Capability policy comun para agentes y equipos sandbox

Estado: `PASSED_DECLARATIVE_POLICY`.

Evidencia:

- schema: `core/capability_policy_schema.py`;
- tests: `tests/test_capability_policy_schema.py`;
- contrato: `docs/CAPABILITY_POLICY_CONTRACT.md`.

Decision:

`capability_policy` queda definida como contrato declarativo comun para agentes y equipos sandbox. La policy valida sujetos (`agent`, `team`), tipos (`memory`, `tool`, `policy`), estados (`declared`, `allowed_declared`, `blocked`, `forbidden`, `future_requires_approval`) y frontera runtime sin activar permisos reales.

Regla central:

```txt
declared + policy validated
!= enabled
!= runtime
!= execution
```

Controles:

- `runtime_enabled=false`;
- `execution_allowed=false`;
- `external_access=false`;
- `declared_only=true`;
- self-approval bloqueado;
- auto-escalation bloqueado;
- runtime mutation bloqueado;
- capabilities de equipo no habilitan automaticamente agentes miembros;
- agentes/equipos sin capabilities siguen validos;
- policies faltantes pueden evaluarse como `missing/not_evaluated` sin romper compatibilidad.

Relacion con manifest:

No se agrega `artifact_type: capability_policy` en esta fase. Queda documentado como posible artefacto futuro si se implementan approval real, auditoria persistente, versionado o rollback independiente.

Recomendacion:

Listo para avanzar a contrato de activacion futura, manteniendo approval workflow y audit log real fuera de esta fase.

## 32. PROMPT 2.8.1 - Auditoria de estados y transiciones antes de promotion gate

Estado: `PASSED_STATE_TRANSITION_AUDIT`.

Evidencia:

- auditoria: `docs/STATE_TRANSITION_AUDIT_BEFORE_PROMOTION_GATE.md`;
- tests: `tests/test_state_transition_consistency.py`.

Decision:

Los estados actuales quedan suficientemente alineados para definir una promotion gate segura en el siguiente prompt. `active` existe como estado global en `domain_state` y `artifact_state`, pero los contratos sandbox de dominio, agente, equipo y capability policy lo bloquean como estado operativo prematuro.

Mapa confirmado:

- dominio general: `empty`, `draft`, `preview`, `materialized`, `active`, `archived`, `legacy`, `broken`;
- artefacto general: `derived_preview`, `ready_to_materialize`, `materialized`, `active`, `archived`, `legacy`, `broken`;
- capability policy: `declared`, `allowed_declared`, `blocked`, `forbidden`, `future_requires_approval`;
- futuro no implementado: `validated`, `candidate_for_activation`.

Reglas antes de promotion gate:

- `materialized` no equivale a usable operativo;
- `active` requiere puerta futura con evidencia, approval y auditoria;
- sandbox domain/agent/team no aceptan `active`;
- runtime, execution y external access siguen bloqueados;
- legacy no transiciona directo a `active`;
- broken/archived no son ejecutables;
- capabilities de equipo no habilitan automaticamente agentes miembros.

Recomendacion:

Listo para `PROMPT 2.9 - promotion gate`. No hace falta subprompt previo, pero la gate no debe usar `can_activate()` como autorizacion suficiente sin evidencia adicional.

## 33. PROMPT 2.9 - Contrato de promotion gate sandbox

Estado: `PASSED_PROMOTION_GATE_CONTRACT`.

Evidencia:

- schema: `core/promotion_gate_schema.py`;
- evaluador: `core/promotion_gate.py`;
- tests: `tests/test_promotion_gate.py`;
- contrato: `docs/PROMOTION_GATE_CONTRACT.md`.

Decision:

La promotion gate queda definida como evaluador no mutante. Puede devolver `validated` o `candidate_for_activation` como resultado de evaluacion, pero no cambia estado operativo, no activa targets y no ejecuta runtime.

Regla central:

```txt
materialized
!= validated
!= candidate_for_activation
!= active
```

Targets soportados:

- `domain`;
- `artifact`;
- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- `agent`;
- `team`;
- `capability_policy`.

Bloqueos:

- `requested_status=active`;
- target `active`, `broken`, `archived` o `legacy`;
- manifest inconsistente;
- dependencias rotas;
- runtime/execution/external access;
- capability policy invalida;
- agente sin lineage;
- equipo con coordinacion ejecutable.

Recomendacion:

Listo para una fase futura de approval workflow y audit log. La promocion real todavia no existe y debe consumir evidencia de gate antes de mutar estados.

## 34. PROMPT 2.9.1 - Checkpoint end-to-end de promotion gate sobre cadena sandbox completa

Estado: `PASSED_PROMOTION_GATE_E2E`.

Evidencia:

- test: `tests/test_promotion_gate_end_to_end.py`;
- reporte: `docs/PROMOTION_GATE_E2E_CHECKPOINT.md`.

Decision:

La promotion gate evalua una cadena sandbox completa real en `tmp_path`, desde dominio hasta equipo y capability_policy, sin mutar targets y sin activar nada. El checkpoint confirma evaluaciones para `validated` y `candidate_for_activation`, bloqueo de `active`, runtime boundary, execution boundary, external access boundary, manifest dependencies, lineage de agente y policy declarativa.

Resultado:

- targets evaluados: `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `agent`, `team`, `capability_policy`;
- `requested_status=active` queda bloqueado;
- manifest inconsistente bloquea;
- agente sin lineage bloquea;
- capability policy invalida bloquea;
- snapshots de sandbox, manifest, dependencies, lineage y capabilities no cambian durante evaluaciones validas;
- no se toca `agents/`, `domains/`, catalogos globales ni papers globales.

Recomendacion:

Listo para `PROMPT 2.10 - approval workflow y audit log`.

## 35. PROMPT 2.10 - Contrato de approval workflow y audit log para promotion gate

Estado: `PASSED_APPROVAL_AUDIT_CONTRACT`.

Evidencia:

- approval schema: `core/approval_workflow_schema.py`;
- audit schema: `core/audit_log_schema.py`;
- helpers: `core/approval_workflow.py`;
- tests: `tests/test_approval_workflow_audit_log.py`;
- contrato: `docs/APPROVAL_WORKFLOW_AUDIT_LOG_CONTRACT.md`.

Decision:

Approval workflow y audit log quedan definidos como contratos no mutantes para decisiones futuras sobre resultados de promotion gate. La regla central queda:

```txt
promotion_gate passed
!= approved
!= promoted
!= active
```

Controles:

- approval request requiere `promotion_gate_result=passed`;
- approval request bloquea `active`;
- approval request requiere actor y evidencia;
- approval decision registra decision pero no promueve;
- self-approval queda bloqueado para decisiones aprobatorias;
- audit event requiere actor, target, evidencia e `immutable=true`;
- audit event bloquea `runtime_related=true` y `external_access_related=true`;
- no se toca `domains/` operativo ni `agents/` legacy.

Recomendacion:

Listo para una futura fase de promotion executor controlado. La persistencia avanzada de audit log y auth real quedan como fases futuras, no implementadas aqui.

## 36. PROMPT 2.11 - Promotion executor controlado para estados intermedios

Estado: `PASSED_PROMOTION_EXECUTOR_INTERMEDIATE`.

Evidencia:

- schema: `core/promotion_executor_schema.py`;
- executor: `core/promotion_executor.py`;
- tests: `tests/test_promotion_executor.py`;
- contrato: `docs/PROMOTION_EXECUTOR_CONTRACT.md`.

Decision:

El promotion executor puede aplicar mutacion controlada solo hacia estados intermedios:

```txt
materialized -> validated
materialized -> candidate_for_activation
validated -> candidate_for_activation
```

Bloqueos:

- `active`;
- runtime/execution/external access;
- legacy/broken/archived;
- approval faltante o incorrecta;
- promotion gate no passed;
- approval para otro target o estado.

Controles:

- dry-run no mutante;
- execute con gate passed y approval valido;
- audit event `promotion_executed`;
- rollback de estado, no de materializacion;
- no se tocan `domains/` operativo ni `agents/` legacy.

Recomendacion:

Hace falta un checkpoint E2E posterior del executor antes de considerar cualquier fase de active promotion.

## 37. PROMPT 2.11.1 - Checkpoint end-to-end de promotion executor sobre cadena sandbox completa

Estado: `PASSED_PROMOTION_EXECUTOR_E2E`.

Evidencia:

- test: `tests/test_promotion_executor_end_to_end.py`;
- reporte: `docs/PROMOTION_EXECUTOR_E2E_CHECKPOINT.md`;
- executor: `core/promotion_executor.py`;
- schema: `core/promotion_executor_schema.py`.

Decision:

El promotion executor fue validado end-to-end sobre una cadena sandbox completa materializada en `tmp_path`:

```txt
domain -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agents -> sandbox_team -> capability_policy
```

El flujo probado fue:

```txt
promotion_gate -> approval_request -> approval_decision -> audit_event -> dry_run -> execute -> rollback
```

Resultado:

- targets probados: `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `agent`, `team`, `capability_policy`;
- `validated` probado para todos los targets;
- `candidate_for_activation` probado para targets representativos: `domain`, `agent`, `team`, `capability_policy`;
- dry-run no muta estado, manifest, dependencies, lineage ni capabilities;
- execute muta solo estado permitido y registra audit event `promotion_executed`;
- rollback restaura el estado previo y no borra artefactos;
- `active` queda bloqueado;
- approvals invalidos quedan bloqueados;
- gates fallidos/bloqueados e inconsistencias de manifest quedan bloqueados;
- runtime/execution/external access quedan bloqueados;
- legacy/broken/archived quedan bloqueados;
- no se tocan `domains/` operativo, `agents/` legacy, catalogos globales ni papers globales.

Recomendacion:

Listo para revisar frontera de `active` en una fase posterior separada. Esa fase no debe reutilizar este checkpoint como activacion implicita.

## 38. PROMPT 2.12 - Auditoria de frontera active antes de activacion real

Estado: `ACTIVE_BOUNDARY_READY_BUT_RUNTIME_MISSING`.

Evidencia:

- auditoria: `docs/ACTIVE_BOUNDARY_AUDIT.md`;
- tests: `tests/test_active_boundary_audit.py`;
- contratos revisados: `artifact_state`, `domain_state`, `promotion_gate`, `approval_workflow`, `promotion_executor`, `capability_policy`, `sandbox_agent`, `sandbox_team`.

Decision:

`active` queda auditado como frontera conceptual, tecnica y de seguridad, no implementado como activacion real.

Regla central:

```txt
candidate_for_activation != active
validated != active
```

Resultado:

- `active` existe en enums globales de dominio/artefacto, pero no como destino permitido por promotion executor;
- promotion gate bloquea `requested_status=active`;
- approval workflow no crea approval request para `active`;
- capability_policy sigue declarativa y bloquea runtime/execution/external access;
- sandbox domain/agent/team bloquean `active`;
- legacy, broken y archived no pueden cruzar a active;
- `active` no implica runtime automatico en esta etapa ni deberia implicarlo automaticamente en la siguiente.

Bloqueadores antes de active real:

- active promotion contract;
- permission enforcement;
- audit log persistente;
- approval persistence;
- auth/actor real;
- rollback desde active;
- runtime/execution contract;
- observability;
- UI visibility contract.

Recomendacion:

El proximo paso seguro es disenar `active contract`. Runtime contract y observability/audit persistence deben venir despues o como subfases explicitas, sin activar agentes/equipos.

## 39. PROMPT 2.13 - Contrato de active sin runtime

Estado: `ACTIVE_CONTRACT_NO_RUNTIME_DEFINED`.

Evidencia:

- schema: `core/active_contract_schema.py`;
- evaluador: `core/active_contract.py`;
- tests: `tests/test_active_contract.py`;
- documento: `docs/ACTIVE_CONTRACT_NO_RUNTIME.md`.

Decision:

`active` queda definido como contrato interno, sin implementacion de promocion real y sin runtime.

Separaciones obligatorias:

```txt
active interno != runtime enabled
active interno != execution enabled
active interno != external access enabled
active interno != visible en UI
active interno != herramientas reales
active interno != memoria real
```

Targets soportados por contrato:

- `domain`;
- `profile_catalog`;
- `agent_preset`;
- `paper_seed`;
- `agent`;
- `team`;
- `capability_policy`.

Resultado:

- solo `internal_active` queda evaluable contractualmente;
- `runtime_active_future` y `external_active_future` quedan bloqueados;
- el target debe estar en `candidate_for_activation`;
- approval y audit son requeridos;
- runtime/execution/external access deben permanecer false;
- legacy/broken/archived quedan bloqueados;
- manifest inconsistente, dependencies rotas, lineage invalido y capability_policy invalida bloquean;
- `evaluate_active_contract()` evalua y no muta;
- `promotion_executor` sigue bloqueando `active`.

Recomendacion:

Antes de implementar un active executor, ejecutar un checkpoint end-to-end del active contract sobre la cadena sandbox completa. Runtime, UI e integraciones siguen fuera de alcance.

## 40. PROMPT 2.13.1 - Checkpoint end-to-end del active contract sin runtime

Estado: `PASSED_ACTIVE_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_active_contract_end_to_end.py`;
- reporte: `docs/ACTIVE_CONTRACT_E2E_CHECKPOINT.md`;
- contrato: `core/active_contract.py`;
- schema: `core/active_contract_schema.py`.

Decision:

El active contract fue validado end-to-end sobre una cadena sandbox completa, con todos los targets evaluados como `candidate_for_activation` antes de `internal_active`.

Flujo probado:

```txt
promotion_gate -> approval_request -> approval_decision -> audit_event -> promotion_executor -> candidate_for_activation -> evaluate_active_contract
```

Resultado:

- targets candidatos: `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `agent`, `team`, `capability_policy`;
- `internal_active` evalua `passed` cuando hay candidate, approval, audit, manifest/dependencies, lineage y policy validos;
- `runtime_active_future` y `external_active_future` bloquean;
- targets no candidate bloquean;
- approval/audit faltantes bloquean;
- manifest inconsistente y dependencies rotas bloquean;
- lineage invalido y capability_policy invalida bloquean;
- `promotion_executor` sigue bloqueando `requested_status=active`;
- `evaluate_active_contract()` no muta estado ni manifest;
- runtime/execution/external access permanecen false;
- no se tocan `domains/`, `agents/`, catalogos globales ni papers globales.

Recomendacion:

Listo para disenar un active executor interno sin runtime. Ese diseno debe seguir bloqueando runtime, UI, integraciones y ejecucion real.

## 41. PROMPT 2.14 - Active executor interno sin runtime

Estado: `ACTIVE_EXECUTOR_NO_RUNTIME_IMPLEMENTED`.

Evidencia:

- schema: `core/active_executor_schema.py`;
- executor: `core/active_executor.py`;
- audit events: `active_executed`, `active_rollback_recorded`;
- tests: `tests/test_active_executor.py`;
- documento: `docs/ACTIVE_EXECUTOR_NO_RUNTIME.md`.

Decision:

`active_executor` queda implementado como unico modulo para aplicar:

```txt
candidate_for_activation -> active
```

La transicion es interna, auditable, reversible y sin runtime.

Resultado:

- `dry_run_active_execution()` evalua sin mutar;
- `execute_active()` muta solo status a `active`;
- `rollback_active_execution()` revierte solo status al estado anterior;
- se exige active contract `passed`;
- se exige approval `approved_for_activation_candidate`;
- se exige audit evidence;
- se bloquean runtime/execution/external access;
- se bloquean legacy/broken/archived;
- se bloquean manifest inconsistente, dependencies rotas, lineage invalido y capability_policy invalida;
- `promotion_executor` sigue bloqueando `active`;
- no se toca UI, integraciones, memoria real ni herramientas reales.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end del active executor sobre la cadena sandbox completa. Runtime, execution, UI e integraciones siguen fuera de alcance.

## 42. PROMPT 2.14.1 - Checkpoint end-to-end del active executor interno sin runtime

Estado: `PASSED_ACTIVE_EXECUTOR_E2E`.

Evidencia:

- test: `tests/test_active_executor_end_to_end.py`;
- reporte: `docs/ACTIVE_EXECUTOR_E2E_CHECKPOINT.md`;
- executor: `core/active_executor.py`;
- schema: `core/active_executor_schema.py`.

Decision:

El active executor fue validado end-to-end sobre una cadena sandbox completa. Puede aplicar y revertir `active` interno sin runtime.

Flujo probado:

```txt
promotion_gate -> approval_request -> approval_decision -> audit_event -> promotion_executor -> candidate_for_activation -> active_contract -> dry_run_active_execution -> execute_active -> rollback_active_execution
```

Resultado:

- targets probados: `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `agent`, `team`, `capability_policy`;
- todos llegan primero a `candidate_for_activation`;
- active contract pasa antes de active;
- dry run pasa sin mutar;
- execute aplica `active` interno y registra `active_executed`;
- rollback vuelve a `candidate_for_activation` y registra `active_rollback_recorded`;
- solo se muta status/artifact_state/status de manifest segun target;
- approval invalido y decision incorrecta bloquean;
- audit faltante o de otro target bloquea;
- active_contract failed, `runtime_active_future` y `external_active_future` bloquean;
- runtime/execution/external access permanecen bloqueados;
- no se tocan `domains/`, `agents/`, catalogos globales ni papers globales.

Recomendacion:

Listo para auditar frontera runtime. Todavia no implementar runtime ni ejecucion real.

## 43. PROMPT 2.15 - Auditoria de frontera runtime antes de ejecucion real

Estado: `RUNTIME_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/RUNTIME_BOUNDARY_AUDIT.md`;
- tests: `tests/test_runtime_boundary_audit.py`;
- frontera active: `core/active_contract.py`;
- executor active: `core/active_executor.py`;
- policies/tools/memory declarativas: `core/capability_policy_schema.py`, `core/sandbox_agent_tool_contract.py`, `core/sandbox_agent_memory_contract.py`.

Decision:

La frontera runtime queda auditada y explicitamente bloqueada. `active` sigue siendo un estado interno, aprobado, auditable y reversible, sin ejecucion real.

Resultado:

- runtime se define como capa futura de preparacion o ejecucion operativa real;
- `agent` y `team` son los targets con runtime directo futuro;
- `domain`, `capability_policy`, `memory_contract` y `tool_contract` solo participan como contexto o guardrails;
- `profile_catalog`, `agent_preset` y `paper_seed` no tienen runtime directo;
- `runtime_enabled=true`, `execution_enabled=true`, `execution_allowed=true` y `external_access=true` permanecen bloqueados;
- `runtime_active_future` y `external_active_future` siguen bloqueados;
- `promotion_executor` sigue bloqueando `requested_status=active`;
- memoria y herramientas siguen siendo declarativas;
- no se implementa runtime executor, no se ejecutan agentes/equipos, no se crean adapters, no se habilita UI ni integraciones.

Recomendacion:

El proximo paso seguro es disenar un contrato runtime futuro. Ese contrato debe existir antes de cualquier runtime executor, execution executor, tool adapter, memoria persistente o acceso externo.

## 44. PROMPT 2.16 - Contrato runtime sin ejecucion real

Estado: `RUNTIME_CONTRACT_NO_EXECUTION_DEFINED`.

Evidencia:

- schema: `core/runtime_contract_schema.py`;
- evaluador: `core/runtime_contract.py`;
- tests: `tests/test_runtime_contract.py`;
- documento: `docs/RUNTIME_CONTRACT_NO_EXECUTION.md`.

Decision:

Runtime queda definido como contrato declarativo para `agent` y `team`, sin runtime real y sin ejecucion.

Resultado:

- `runtime_contract` evalua readiness declarativa, no habilita runtime;
- solo `agent` y `team` son targets directos;
- `domain`, `profile_catalog`, `agent_preset`, `paper_seed`, `capability_policy`, `tool_contract` y `memory_contract` quedan bloqueados como runtime directo;
- unico runtime mode permitido: `declarative_runtime_contract`;
- `runtime_ready_future`, `execution_ready_future` y `external_access_future` quedan bloqueados;
- se exige target `active` y evidencia de `active_executor`;
- se exigen capability policies, memory/tool contracts declarativos cuando existan, lineage/dependencies y audit evidence;
- `runtime_allowed`, `runtime_enabled`, `execution_allowed`, `execution_enabled`, `external_access_allowed`, `external_access_enabled`, `tool_execution_allowed`, `tool_execution_enabled`, `memory_persistence_allowed` y `memory_persistence_enabled` permanecen bloqueados;
- no se modifica `active_executor`;
- no se crea runtime executor;
- no se toca UI, integraciones, tools reales ni memoria persistente.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end del runtime contract sobre la cadena sandbox activa antes de disenar cualquier runtime executor.

## 45. PROMPT 2.16.1 - Checkpoint end-to-end del runtime contract sobre cadena sandbox activa

Estado: `PASSED_RUNTIME_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_runtime_contract_end_to_end.py`;
- reporte: `docs/RUNTIME_CONTRACT_E2E_CHECKPOINT.md`;
- evaluador: `core/runtime_contract.py`;
- schema: `core/runtime_contract_schema.py`.

Decision:

El runtime contract fue validado end-to-end sobre una cadena sandbox completa con `agent` y `team` en `active` interno.

Flujo probado:

```txt
domain -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agents -> sandbox_team -> capability_policy
promotion_gate -> approval_request -> approval_decision -> promotion_executor -> candidate_for_activation -> active_contract -> active_executor -> runtime_contract
```

Resultado:

- `agent` llega a `active` interno;
- `team` llega a `active` interno;
- `runtime_contract` pasa para `agent` y `team` con `declarative_runtime_contract`;
- targets no active bloquean;
- runtime modes futuros bloquean;
- runtime/execution/external/tools/memory flags true bloquean;
- evidencia faltante, capability policy faltante/invalida, memory/tool invalidos, lineage invalido y dependencies rotas bloquean;
- targets sin runtime directo bloquean;
- runtime contract no muta estado, manifest, lineage, dependencies ni capabilities;
- no se habilita runtime, execution, external access, tool execution ni memory persistence;
- no se toca UI, integraciones, `domains/`, `agents/`, catalogos globales ni papers globales.

Recomendacion:

Listo para decidir el proximo bloque interno: runtime executor futuro, observability/audit persistence o execution contract. No implementar runtime executor sin una decision explicita de fase.

## 46. PROMPT 2.17 - Contrato de observability y audit persistence antes de runtime executor

Estado: `OBSERVABILITY_AUDIT_PERSISTENCE_CONTRACT_DEFINED`.

Evidencia:

- schema observability: `core/observability_schema.py`;
- schema audit persistence: `core/audit_persistence_schema.py`;
- helpers: `core/observability.py`;
- tests: `tests/test_observability_audit_persistence.py`;
- documento: `docs/OBSERVABILITY_AUDIT_PERSISTENCE_CONTRACT.md`.

Decision:

Observability y audit persistence quedan definidos como contrato previo a runtime executor, sin runtime, sin ejecucion, sin tools reales, sin memoria real y sin UI.

Resultado:

- se definen eventos minimos de gate, approval, promotion, active, runtime_contract, boundary violation, snapshots y rollback;
- cada evento exige correlation, target/domain/operation, evidence refs, mutation scope, flags runtime/execution/external/tools-memory e immutability;
- se define correlation policy para evitar evidencia cruzada entre target, dominio, operacion, status o contrato;
- se define snapshot policy con before/after/diff/rollback/checksum;
- se define audit store contract con `write_mode=append_only`, `append_only=true` e `immutable_records=true`;
- se definen metricas minimas de eventos, bloqueos, exitos, rollbacks, boundary violations, mutation violations y evidencia faltante;
- helpers validan eventos, correlacion, refs y resumen de metricas sin mutar targets;
- no se implementa runtime executor ni persistent event log real.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end de observability/audit persistence sobre la cadena sandbox activa antes de cualquier runtime executor.

## 47. PROMPT 2.17.1 - Checkpoint end-to-end de observability/audit persistence sobre cadena sandbox activa

Estado: `PASSED_OBSERVABILITY_AUDIT_E2E`.

Evidencia:

- test: `tests/test_observability_audit_persistence_end_to_end.py`;
- reporte: `docs/OBSERVABILITY_AUDIT_E2E_CHECKPOINT.md`;
- helpers: `core/observability.py`;
- schemas: `core/observability_schema.py`, `core/audit_persistence_schema.py`.

Decision:

Observability/audit persistence fue validado end-to-end sobre una cadena sandbox activa completa. Queda como contrato validado, no como writer append-only real.

Resultado:

- cadena probada: domain -> profile_catalog -> presets -> paper_seed -> agents -> team -> capability_policy -> active -> runtime_contract;
- eventos minimos validados para gate, approval, promotion, active, runtime_contract, rollback, snapshots, mutation scope y boundary checks;
- correlation policy detecta evidencia cruzada por target, domain, operation, requested_status/runtime_mode, contract_ref, approval_ref y audit_ref;
- snapshot policy valida before/after/diff/rollback/checksum;
- mutation scope policy valida `none` y `status_only`, y bloquea scopes excesivos;
- audit store contract valida append-only, immutability, checksum y event_count;
- metricas minimas se generan con exitos, bloqueos, rollbacks, boundary violation, invalid correlation y missing evidence;
- runtime, execution, external access, tool execution y memory persistence siguen bloqueados;
- no se toca UI, integraciones, `domains/`, `agents/`, catalogos globales ni papers globales.

Recomendacion:

Listo para integrar observability progresivamente en executors existentes. Runtime executor debe esperar una decision explicita o un checkpoint que conecte observability real a outputs de executor.

## 48. PROMPT 2.18 - Integracion progresiva de observability en executors existentes

Estado: `OBSERVABILITY_EXECUTOR_INTEGRATION_DEFINED`.

Evidencia:

- helpers/context: `core/observability.py`;
- promotion executor: `core/promotion_executor.py`;
- active executor: `core/active_executor.py`;
- runtime contract: `core/runtime_contract.py`;
- tests: `tests/test_observability_executor_integration.py`;
- documento: `docs/OBSERVABILITY_EXECUTOR_INTEGRATION.md`.

Decision:

Observability queda integrada progresivamente en executors existentes mediante `observability_context` opcional. No cambia logica de negocio, no habilita runtime, no habilita execution y no toca UI.

Resultado:

- `promotion_executor` puede emitir `promotion_executed`, `promotion_rollback_recorded` y `mutation_scope_verified`;
- `active_executor` puede emitir `active_executed`, `active_rollback_recorded`, `mutation_scope_verified` y `runtime_boundary_violation`;
- `runtime_contract` puede emitir `runtime_contract_evaluated`, `runtime_contract_blocked` y `runtime_boundary_violation`;
- los eventos incluyen correlation, target/domain/operation, evidence refs, approval/contract/audit refs, mutation scope y snapshots livianos;
- sin observability context, los modulos siguen funcionando como antes;
- no se implementa writer append-only real ni runtime executor;
- runtime/execution/external/tools/memory siguen bloqueados.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end de observability integrada en executors o la integracion progresiva con un audit store append-only real.

## 49. PROMPT 2.18.1 - Checkpoint end-to-end de observability integrada en executors

Estado: `PASSED_OBSERVABILITY_EXECUTOR_INTEGRATION_E2E`.

Evidencia:

- test: `tests/test_observability_executor_integration_end_to_end.py`;
- reporte: `docs/OBSERVABILITY_EXECUTOR_INTEGRATION_E2E_CHECKPOINT.md`;
- integration test base: `tests/test_observability_executor_integration.py`;
- modulos: `core/promotion_executor.py`, `core/active_executor.py`, `core/runtime_contract.py`.

Decision:

La observability integrada en executors fue validada end-to-end sobre una cadena sandbox completa. La integracion sigue siendo opcional y compatible.

Resultado:

- `promotion_executor` emite eventos observability validos con context;
- `active_executor` emite eventos observability validos con context;
- `runtime_contract` emite eventos observability validos con context;
- eventos contienen correlation, target/domain/operation, requested_status/runtime_mode, refs y snapshots;
- evidence crossing bloquea por correlation, target, domain, operation, requested_status, contract_ref, approval_ref y audit_ref;
- snapshots/checksums y mutation scope quedan validados;
- sin observability context, promotion, active y runtime mantienen resultados funcionales;
- runtime, execution, external access, tools y memory persistence siguen bloqueados;
- no se toca UI, integraciones, `domains/`, `agents/`, catalogos globales ni papers globales.

Recomendacion:

Listo para implementar audit store append-only real. Runtime executor debe esperar una decision explicita posterior.

## 50. PROMPT 2.19 - Audit store append-only real

Estado: `AUDIT_STORE_APPEND_ONLY_IMPLEMENTED`.

Evidencia:

- modulo: `core/audit_store.py`;
- tests: `tests/test_audit_store_append_only.py`, `tests/test_audit_store_observability_integration.py`;
- documento: `docs/AUDIT_STORE_APPEND_ONLY.md`.

Decision:

IA_CORE cuenta con un audit store local append-only logico/verificable para eventos observability. El store persiste eventos en filesystem local con manifest, secuencia, checksum por evento y chain por `previous_event_checksum`.

Resultado:

- `create_audit_store` crea/valida manifest y carpeta `events`;
- `append_audit_event` valida observability antes de escribir, crea archivos nuevos con modo exclusivo y no sobrescribe eventos;
- `read_audit_events` devuelve eventos ordenados por secuencia;
- `verify_audit_store` detecta deletes, reorder, mutacion de evento y manifest inconsistente;
- `summarize_audit_store` reutiliza metricas observability y adjunta verificacion del store;
- la integracion E2E persiste eventos reales de promotion, active y runtime contract sin ejecutar runtime;
- no se habilita runtime, execution, tools, memoria real, UI ni integraciones.

Recomendacion:

El proximo checkpoint seguro es integrar, si se decide, escritura opcional hacia audit store desde flujos internos controlados, manteniendo el store desactivado por defecto para runtime.

## 51. PROMPT 2.19.1 - Checkpoint de escritura opcional controlada desde flujos internos hacia audit store

Estado: `PASSED_AUDIT_STORE_INTERNAL_FLOWS_E2E`.

Evidencia:

- helper/context: `core/observability.py`;
- executors integrados: `core/promotion_executor.py`, `core/active_executor.py`, `core/runtime_contract.py`;
- test: `tests/test_audit_store_internal_flows_end_to_end.py`;
- reporte: `docs/AUDIT_STORE_INTERNAL_FLOWS_E2E_CHECKPOINT.md`;
- store base: `core/audit_store.py`.

Decision:

La escritura hacia audit store queda como salida opcional controlada por `observability_context`, no como dependencia obligatoria. Los flujos internos pueden persistir eventos observability append-only con checksum chain cuando reciben `audit_store_path` y `persist_events=true`.

Resultado:

- promotion, active y runtime contract escriben eventos en audit store cuando el context lo solicita;
- sin context siguen funcionando y no emiten eventos;
- con context sin store siguen funcionando y reportan `audit_store_path_missing`;
- eventos invalidos no escriben parcial porque se validan antes de persistir;
- store inexistente o tampered reporta error controlado en `audit_store_result`;
- read, verify y summarize validan secuencia, checksum chain, correlation y metricas;
- runtime, execution, external access, tools y memory persistence siguen bloqueados;
- no se toca UI, integraciones, `domains/`, `agents/`, catalogos ni papers globales.

Recomendacion:

Listo para disenar execution contract antes de runtime executor.

## 52. PROMPT 2.20 - Contrato de execution antes de runtime executor

Estado: `EXECUTION_CONTRACT_DEFINED_NO_EXECUTION`.

Evidencia:

- schema: `core/execution_contract_schema.py`;
- evaluador: `core/execution_contract.py`;
- tests: `tests/test_execution_contract.py`;
- documento: `docs/EXECUTION_CONTRACT_NO_EXECUTION.md`.

Decision:

Execution queda definido como contrato declarativo de readiness para una corrida futura de `agent` o `team`. No ejecuta agentes, no ejecuta equipos, no invoca modelos, no ejecuta tools, no persiste memoria y no toca UI.

Resultado:

- targets directos permitidos: `agent`, `team`;
- targets operativos no ejecutables directamente quedan bloqueados;
- modo permitido: `declarative_execution_contract`;
- modos futuros bloqueados: `execution_ready_future`, `model_invocation_future`, `tool_execution_future`, `external_execution_future`;
- exige `runtime_contract` passed y `active_execution` passed del mismo target/domain;
- exige input/output contract, prompt contract, model invocation contract declarativo, timeout/retry/cancellation/failure policies;
- exige `observability_required=true`, `audit_store_required=true`, correlation id y audit store verificable;
- bloquea execution/external/tools/memory flags;
- no muta targets ni habilita runtime/execution.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end de execution contract sobre cadena sandbox activa antes de disenar runtime executor.

## 53. PROMPT 2.20.1 - Checkpoint end-to-end de execution contract sobre cadena sandbox activa

Estado: `PASSED_EXECUTION_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_execution_contract_end_to_end.py`;
- evaluador: `core/execution_contract.py`;
- schema: `core/execution_contract_schema.py`;
- reporte: `docs/EXECUTION_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

Execution contract fue validado end-to-end sobre cadena sandbox activa completa para `agent` y `team`. La validacion confirma readiness declarativa sin runtime executor, sin execution runner, sin modelos, sin tools reales, sin memoria real, sin UI y sin integraciones.

Resultado:

- cadena temporal completa materializada hasta agent/team active;
- runtime_contract passed para agent y team;
- audit_store append-only creado, poblado con eventos correlacionados y verificado;
- execution_contract passed para `declarative_execution_contract`;
- bloquea target no active, runtime_contract invalido, audit_store invalido, observability/correlation invalida, contracts faltantes, policies faltantes, flags prohibidos, modes futuros y target types incorrectos;
- no muta estado, manifest, dependencies, lineage ni capabilities durante la evaluacion;
- runtime/execution/model/tools/memory/external access siguen bloqueados;
- no toca `domains/`, `agents/`, catalogos ni papers globales.

Recomendacion:

Listo para auditar frontera runtime executor antes de disenar runtime executor.

## 54. PROMPT 2.21 - Auditoria de frontera runtime executor antes de implementacion

Estado: `RUNTIME_EXECUTOR_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/RUNTIME_EXECUTOR_BOUNDARY_AUDIT.md`;
- tests: `tests/test_runtime_executor_boundary_audit.py`;
- contratos auditados: `core/runtime_contract.py`, `core/execution_contract.py`, `core/audit_store.py`, `core/observability.py`.

Decision:

La frontera runtime executor queda auditada y documentada. No se implementa runtime executor, execution runner, model invocation, tool execution, memory persistence, external access, UI ni integraciones.

Resultado:

- `runtime_executor` se define como modulo futuro de prepare/coordination, separado de execution runner real;
- modos futuros definidos: `prepare_only`, `dry_run_only`, `plan_only`, `execute_future`;
- modo recomendado para primer contrato futuro: `prepare_only`;
- targets futuros candidatos: `agent`, `team`;
- targets bloqueados: domain, profile_catalog, agent_preset, paper_seed, capability_policy, tool_contract, memory_contract, runtime_contract;
- se clasifican bloqueadores previos a runtime executor, execution runner, model invocation, tool execution, memory persistence, external access, UI e integraciones;
- tests confirman que active/runtime/execution/audit passed no implican ejecucion real ni habilitan flags;
- runtime, execution, model/tool/memory/external access siguen bloqueados.

Recomendacion:

El proximo paso seguro es disenar contrato/schema de runtime executor prepare-only, todavia sin implementar runner ni ejecucion real.

## 55. PROMPT 2.22 - Contrato de runtime executor prepare-only

Estado: `RUNTIME_EXECUTOR_CONTRACT_PREPARE_ONLY_DEFINED`.

Evidencia:

- schema: `core/runtime_executor_schema.py`;
- evaluador: `core/runtime_executor_contract.py`;
- tests: `tests/test_runtime_executor_contract.py`;
- documento: `docs/RUNTIME_EXECUTOR_CONTRACT_PREPARE_ONLY.md`.

Decision:

Runtime executor contract queda definido en modo `prepare_only`, sin runtime real, sin execution runner, sin ejecucion, sin modelos, sin tools reales, sin memoria real, sin UI y sin integraciones.

Resultado:

- targets soportados: `agent`, `team`;
- targets bloqueados: domain, profile_catalog, agent_preset, paper_seed, capability_policy, tool_contract, memory_contract, runtime_contract, execution_contract;
- modo permitido: `prepare_only`;
- modos bloqueados: `dry_run_only`, `plan_only`, `execute_future`;
- exige runtime_contract passed, execution_contract passed, observability context, audit_store verified, correlation_id, preparation_plan, abort_plan, rollback_plan, idempotency_key, lock_policy, concurrency_policy, mutation_policy y boundary_policy;
- boundary_policy mantiene bloqueados runtime, execution, model invocation, tool execution, memory persistence, external access, UI trigger e integration runner;
- el evaluador devuelve contrato prepare-only sin mutar targets ni habilitar flags.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end de runtime executor contract prepare-only sobre cadena sandbox activa.

## 56. PROMPT 2.22.1 - Checkpoint end-to-end del runtime executor contract prepare-only sobre cadena sandbox activa

Estado: `PASSED_RUNTIME_EXECUTOR_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_runtime_executor_contract_end_to_end.py`;
- evaluador reforzado: `core/runtime_executor_contract.py`;
- eventos declarativos reconocidos: `core/observability_schema.py`;
- documento: `docs/RUNTIME_EXECUTOR_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

Runtime executor contract prepare-only queda validado end-to-end sobre cadena sandbox activa completa para `agent` y `team`. La validacion confirma que puede evaluar targets activos con runtime_contract passed, execution_contract passed, observability valida y audit_store append-only verificado sin mutar ni habilitar runtime real.

Resultado:

- cadena temporal completa materializada desde domain hasta capability_policy, promotion, active, runtime_contract, execution_contract y audit_store;
- `agent` y `team` llegaron a active interno;
- runtime_contract y execution_contract pasaron para ambos targets;
- audit_store exige eventos prepare-only seguros y correlacionados;
- preparation_plan, abort_plan, rollback_plan, idempotency, lock y concurrency validan;
- bloquea target no active, runtime_contract invalido, execution_contract invalido, audit_store invalido, observability/correlation invalida, plans/policies faltantes, flags prohibidos, modes futuros y target types incorrectos;
- no muta status, manifest, dependencies, lineage, capabilities ni artefactos sandbox durante evaluacion;
- runtime real, execution runner, model invocation, tool execution, memory persistence, external access, UI e integraciones siguen bloqueados;
- no toca `domains/`, `agents/`, catalogos ni papers globales.

Recomendacion:

Listo para implementar runtime executor prepare-only.

## 57. PROMPT 2.23 - Implementar runtime executor prepare-only

Estado: `RUNTIME_EXECUTOR_PREPARE_ONLY_IMPLEMENTED`.

Evidencia:

- modulo: `core/runtime_executor.py`;
- eventos permitidos: `core/observability_schema.py`;
- tests: `tests/test_runtime_executor_prepare_only.py`;
- documento: `docs/RUNTIME_EXECUTOR_PREPARE_ONLY.md`.

Decision:

Runtime executor prepare-only queda implementado como capa operativa declarativa. Puede generar preparation record, registrar observability events, persistir audit_store events append-only, respetar idempotency y aplicar lock/concurrency minima dentro del proceso.

Resultado:

- funciones expuestas: `prepare_runtime`, `abort_runtime_preparation`, `rollback_runtime_preparation`;
- status soportados: `prepared`, `blocked`, `aborted`, `rolled_back`, `noop_idempotent`;
- `prepare_runtime` exige runtime_executor_contract passed, runtime_contract passed, execution_contract passed, observability context, audit_store verified, correlation_id e idempotency_key;
- registra eventos seguros `runtime_prepare_started`, `runtime_prepare_validated`, `runtime_prepare_completed`, `runtime_prepare_idempotent_replay`, `runtime_prepare_blocked`, `runtime_prepare_aborted`, `runtime_prepare_rolled_back` y `mutation_scope_verified`;
- idempotency evita duplicar `runtime_prepare_completed` ante mismo target/correlation/idempotency_key;
- lock in-memory bloquea doble preparacion simultanea del mismo target con `runtime_preparation_lock_conflict`;
- abort y rollback son declarativos y solo registran metadata/audit/observability;
- no implementa execution runner, no ejecuta agentes/equipos, no invoca modelos, no ejecuta tools, no persiste memoria real, no toca UI ni integraciones;
- no toca `domains/`, `agents/`, catalogos ni papers globales.

Recomendacion:

El proximo paso seguro es checkpoint end-to-end de runtime executor prepare-only sobre cadena sandbox activa.

## 58. PROMPT 2.23.1 - Checkpoint end-to-end de runtime executor prepare-only sobre cadena sandbox activa

Estado: `PASSED_RUNTIME_EXECUTOR_PREPARE_ONLY_E2E`.

Evidencia:

- test: `tests/test_runtime_executor_prepare_only_end_to_end.py`;
- modulo validado: `core/runtime_executor.py`;
- documento: `docs/RUNTIME_EXECUTOR_PREPARE_ONLY_E2E_CHECKPOINT.md`.

Decision:

Runtime executor prepare-only queda validado end-to-end sobre cadena sandbox activa completa. `prepare_runtime` prepara `agent` y `team` activos con runtime_contract, execution_contract y runtime_executor_contract passed, audit_store verificado, observability valida, idempotency, lock/concurrency y abort/rollback declarativos.

Resultado:

- cadena temporal completa materializada desde domain hasta runtime_executor_contract y audit_store;
- `agent` y `team` llegaron a active interno;
- runtime_contract, execution_contract y runtime_executor_contract pasaron para ambos targets;
- `prepare_runtime` devolvio `prepared` para `agent` y `team`;
- preparation record, preparation_id, refs de contratos y refs audit/observability validados;
- idempotency devuelve `noop_idempotent` sin duplicar `runtime_prepare_completed`;
- lock/concurrency bloquea doble preparacion con `runtime_preparation_lock_conflict`;
- abort y rollback registran eventos declarativos y no mutan targets;
- contratos invalidos/cruzados, audit/observability invalidos, targets invalidos, flags prohibidos y modos prohibidos bloquean;
- runtime real, execution runner, modelos, tools, memoria real, external access, UI e integraciones siguen bloqueados;
- no toca `domains/`, `agents/`, catalogos ni papers globales.

Recomendacion:

Listo para auditar frontera execution runner.

## 59. PROMPT 2.24 - Auditoria de frontera execution runner

Estado: `EXECUTION_RUNNER_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/EXECUTION_RUNNER_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_runner_boundary_audit.py`;
- piezas auditadas: `core/runtime_executor.py`, `core/execution_contract.py`, `core/runtime_contract.py`, `core/audit_store.py`, `core/observability.py`.

Decision:

Execution runner queda auditado como frontera conceptual, tecnica y de seguridad. No se implementa `execution_runner`, no se habilita execution, no se invocan modelos, no se ejecutan tools reales, no se persiste memoria real, no se toca UI ni integraciones.

Resultado:

- `execution_runner` se define como modulo futuro para coordinar una corrida controlada, inicialmente `contract_only`;
- no significa model invocation real, tool execution real, memory persistence real, external access, UI trigger, integration runner, scheduler ni worker queue;
- debe requerir active_executor passed, runtime_contract passed, execution_contract passed, runtime_executor_contract passed, runtime prepare-only `prepared`, observability context, audit_store verified, policies declarativas, idempotency/lock/concurrency y abort/rollback plan;
- targets futuros candidatos: `agent`, `team`;
- targets directos bloqueados: domain, profile_catalog, agent_preset, paper_seed, capability_policy, tool_contract, memory_contract, runtime_contract, execution_contract y runtime_executor_contract;
- modos futuros definidos: `contract_only`, `dry_run_only`, `simulation_only`, `no_model_execution_plan`, `model_invocation_future`, `tool_execution_future`, `memory_persistence_future`, `full_execution_future`;
- modo recomendado: `contract_only`;
- execution, execution runner, modelos, tools, memoria real, external access, UI e integraciones permanecen bloqueados.

Recomendacion:

El proximo paso seguro es disenar `execution_runner_contract` en modo `contract_only`, sin ejecucion real.

## 60. PROMPT 2.25 - Disenar execution_runner_contract sin ejecucion real

Estado: `EXECUTION_RUNNER_CONTRACT_PASSED`.

Evidencia:

- schema: `core/execution_runner_schema.py`;
- validador: `core/execution_runner_contract.py`;
- tests: `tests/test_execution_runner_contract.py`;
- documento: `docs/EXECUTION_RUNNER_CONTRACT_NO_EXECUTION.md`.

Decision:

`execution_runner_contract` queda creado como contrato declarativo previo al futuro runner. El unico modo operativo aceptado es `contract_only`; los modos futuros quedan reconocidos por schema pero bloqueados por contrato.

Resultado:

- valida `agent` y `team` activos con runtime_contract passed, execution_contract passed, runtime_executor_contract passed y runtime_prepare_result prepared;
- exige preparation_id, audit_store verified, observability_context valido, capability_policy declarativa, idempotency_key, lock/concurrency, abort/rollback, input_contract y boundary_contract;
- bloquea targets no directos, targets legacy/archived/broken/no active, refs cruzadas, contratos faltantes o no passed, audit/observability invalidos, input payload real y flags prohibidos;
- no crea `core/execution_runner.py`;
- no crea execution attempt;
- no ejecuta agentes ni equipos;
- no invoca modelos;
- no ejecuta tools;
- no persiste memoria real;
- no habilita external access;
- no toca UI, integraciones, scheduler ni worker queue;
- no escribe eventos audit nuevos; solo verifica el audit_store recibido.

Recomendacion:

El proximo paso seguro es `PROMPT 2.25.1 - Checkpoint end-to-end execution_runner_contract sobre cadena sandbox activa`.

## 61. PROMPT 2.25.1 - Checkpoint end-to-end execution_runner_contract sobre cadena sandbox activa

Estado: `PASSED_EXECUTION_RUNNER_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_execution_runner_contract_end_to_end.py`;
- contrato validado: `core/execution_runner_contract.py`;
- documento: `docs/EXECUTION_RUNNER_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

`execution_runner_contract` queda validado end-to-end sobre cadena sandbox activa completa para `agent` y `team`. La validacion confirma que puede pasar en modo `contract_only` cuando existen runtime_contract passed, execution_contract passed, runtime_executor_contract passed, runtime_prepare_result prepared, audit_store verified y observability valida.

Resultado:

- cadena temporal completa materializada desde sandbox hasta execution_runner_contract;
- `agent` y `team` llegaron a active interno;
- runtime_contract, execution_contract y runtime_executor_contract pasaron para ambos targets;
- runtime_executor prepare-only devolvio `prepared`;
- execution_runner_contract devolvio `passed` para `agent` y `team`;
- contratos faltantes/invalidos, audit/observability invalidos, targets invalidos, refs cruzadas, inputs prohibidos, flags prohibidos y modos futuros bloquean;
- idempotency/replay declarativo devuelve contrato equivalente sin escribir eventos nuevos;
- no crea `core/execution_runner.py`;
- no crea execution attempt;
- no ejecuta agentes ni equipos;
- no invoca modelos;
- no ejecuta tools reales;
- no persiste memoria real;
- no habilita external access;
- no toca UI, integraciones, scheduler ni worker queue;
- no contamina legacy/global artifacts.

Recomendacion:

Listo para auditar frontera execution_runner dry-run.

## 62. PROMPT 2.26 - Auditoria de frontera execution_runner dry-run

Estado: `DRY_RUN_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/EXECUTION_RUNNER_DRY_RUN_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_runner_dry_run_boundary_audit.py`;
- base validada: `docs/EXECUTION_RUNNER_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

`execution_runner dry-run` queda auditado como frontera conceptual, tecnica y de seguridad. Dry-run se define como simulacion declarativa futura de una corrida, no como ejecucion real.

Resultado:

- dry-run no esta implementado;
- `core/execution_runner.py` no existe;
- no existe execution attempt real ni execution attempt store;
- `execution_runner_contract passed` no implica dry-run habilitado;
- `runtime_prepare_result prepared` no implica dry-run habilitado;
- `dry_run_only` sigue bloqueado como modo operativo;
- dry-run futuro debe requerir execution_runner_contract passed, runtime_prepare_result prepared, audit_store verified y observability valida;
- dry-run futuro debe producir simulated_plan, simulated_steps, expected inputs/outputs, risk summary, boundary/readiness summaries y event plans;
- agent/team son targets futuros candidatos;
- domains, catalogs, presets, papers, contracts, policies, UI, integrations, scheduler y worker_queue quedan bloqueados;
- no se ejecutan agentes/equipos;
- no se invocan modelos;
- no se ejecutan tools reales;
- no se persiste memoria real;
- no se habilita external access;
- no se toca UI, integraciones, scheduler ni worker queue.

Recomendacion:

El proximo paso seguro es disenar `execution_runner_dry_run_contract` sin implementacion.

## 63. PROMPT 2.27 - Disenar execution_runner_dry_run_contract sin implementacion

Estado: `EXECUTION_RUNNER_DRY_RUN_CONTRACT_PASSED`.

Evidencia:

- schema: `core/execution_runner_dry_run_schema.py`;
- validador: `core/execution_runner_dry_run_contract.py`;
- tests: `tests/test_execution_runner_dry_run_contract.py`;
- documento: `docs/EXECUTION_RUNNER_DRY_RUN_CONTRACT_NO_IMPLEMENTATION.md`.

Decision:

`execution_runner_dry_run_contract` queda creado como contrato declarativo previo al futuro dry-run. El modo canonico permitido es `dry_run_contract_only`; `dry_run_only` y los modos futuros quedan reconocidos pero bloqueados.

Resultado:

- valida `agent` y `team` activos con runtime_contract passed, execution_contract passed, runtime_executor_contract passed, runtime_prepare_result prepared y execution_runner_contract passed;
- exige audit_store verified, observability context valido, capability_policy declarativa, simulated plan, simulated steps, input/output expectations, boundary, side effects, risk, idempotency, lock, abort y rollback;
- bloquea contratos faltantes/no passed, target no active, refs cruzadas, audit/observability invalidos, plan/steps invalidos, input/output reales, flags prohibidos, side effects, risk critical sin human review y modos futuros;
- no implementa dry-run;
- no crea `core/execution_runner.py`;
- no crea execution attempt ni execution attempt store;
- no ejecuta agentes/equipos;
- no invoca modelos;
- no ejecuta tools reales;
- no persiste memoria real;
- no habilita external access;
- no toca UI, integraciones, scheduler ni worker queue.

Recomendacion:

El proximo paso seguro es `PROMPT 2.27.1 - Checkpoint end-to-end execution_runner_dry_run_contract sobre cadena sandbox activa`.

## 64. PROMPT 2.27.1 - Checkpoint end-to-end execution_runner_dry_run_contract sobre cadena sandbox activa

Estado: `PASSED_EXECUTION_RUNNER_DRY_RUN_CONTRACT_E2E`.

Evidencia:

- test: `tests/test_execution_runner_dry_run_contract_end_to_end.py`;
- contrato validado: `core/execution_runner_dry_run_contract.py`;
- documento: `docs/EXECUTION_RUNNER_DRY_RUN_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

`execution_runner_dry_run_contract` queda validado end-to-end sobre cadena sandbox activa completa para `agent` y `team`. La validacion confirma que puede pasar en modo `dry_run_contract_only` con plan simulado declarativo, steps declarativos, input/output expectations y risk summary, sin dry-run real ni ejecucion.

Resultado:

- cadena temporal completa materializada desde sandbox hasta dry-run contract;
- `agent` y `team` llegaron a active interno;
- runtime_contract, execution_contract, runtime_executor_contract y execution_runner_contract pasaron para ambos targets;
- runtime_executor prepare-only devolvio `prepared`;
- dry-run contract devolvio `passed` para `agent` y `team`;
- contratos faltantes/invalidos, audit/observability invalidos, targets invalidos, refs cruzadas, plan simulado invalido, input/output prohibido, flags prohibidos, modos prohibidos y riesgos prohibidos bloquean;
- idempotency/replay declarativo devuelve contrato equivalente sin escribir eventos nuevos;
- no se crea dry-run implementation;
- no se crea `core/execution_runner.py`;
- no se crea execution attempt ni execution attempt store;
- no se ejecutan agentes/equipos;
- no se invocan modelos;
- no se ejecutan tools reales;
- no se persiste memoria real;
- no se habilita external access;
- no se toca UI, integraciones, scheduler ni worker queue;
- no hay contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de implementacion execution_runner dry-run sin ejecucion real.

## 65. PROMPT 2.28 - Auditoria de frontera de implementacion execution_runner dry-run sin ejecucion real

Estado: `DRY_RUN_READY_FOR_RESULT_ONLY_IMPLEMENTATION`.

Evidencia:

- auditoria: `docs/EXECUTION_RUNNER_DRY_RUN_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_runner_dry_run_implementation_boundary_audit.py`;
- base validada: `docs/EXECUTION_RUNNER_DRY_RUN_CONTRACT_E2E_CHECKPOINT.md`.

Decision:

La implementacion futura de `execution_runner dry-run` queda auditada como frontera result-only. Podra existir `core/execution_runner.py` recien en el siguiente prompt, con funciones de dry-run declarativo y sin ejecucion real.

Resultado:

- dry-run implementation no esta creada;
- `core/execution_runner.py` no existe;
- no existen `prepare_dry_run`, `run_dry_run`, `abort_dry_run` ni `rollback_dry_run`;
- no existe execution attempt real;
- no existe execution attempt store;
- no existe dry_run_store operativo;
- `execution_runner_dry_run_contract passed` no implica implementacion;
- `dry_run_contract_only passed` no implica `dry_run_only`;
- `dry_run_only` sigue bloqueado como modo operativo;
- futura implementacion debe requerir dry_run_contract passed, execution_runner_contract passed, runtime_prepare_result prepared, audit_store verified y observability valida;
- primera implementacion recomendada: `FIRST_DRY_RUN_RESULT_ONLY`;
- no se ejecutan agentes/equipos;
- no se invocan modelos;
- no se ejecutan tools reales;
- no se persiste memoria real;
- no se habilita external access;
- no se toca UI, integraciones, scheduler ni worker queue;
- no se mutan targets ni artefactos legacy/global.

Recomendacion:

El proximo paso seguro es implementar primer `execution_runner` dry-run result-only sin ejecucion real.

## 66. PROMPT 2.29 - Implementar execution_runner dry-run result-only sin ejecucion real

Estado: `PASSED_DRY_RUN_RESULT_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/execution_runner.py`;
- tests unitarios: `tests/test_execution_runner_dry_run_result_only.py`;
- tests E2E: `tests/test_execution_runner_dry_run_result_only_end_to_end.py`;
- documento: `docs/EXECUTION_RUNNER_DRY_RUN_RESULT_ONLY.md`.

Decision:

Se crea el primer `execution_runner` dry-run result-only. El runner acepta contratos `execution_runner_dry_run_contract` en modo `dry_run_contract_only` o `contract_only`, valida que esten `passed`, verifica runtime preparation, audit store y observability, y devuelve un `DryRunResult` estructurado sin ejecutar agentes/equipos.

Resultado:

- `core/execution_runner.py` creado;
- funciones `prepare_dry_run`, `run_dry_run`, `abort_dry_run` y `rollback_dry_run` implementadas;
- `DryRunResult` result-only devuelve plan, steps, expectations, risk, boundaries, readiness, eventos declarativos y evidence;
- idempotency result-only soportada con registry in-memory, sin store persistente;
- sin execution attempt;
- sin execution attempt store;
- sin dry_run_store persistente;
- sin ejecucion real de agent/team;
- sin model invocation;
- sin tool execution;
- sin memory persistence;
- sin external access;
- sin UI ni integraciones;
- sin scheduler ni worker queue;
- sin mutacion de targets ni contaminacion legacy/global.

Recomendacion:

El proximo paso seguro es `PROMPT 2.29.1 - Checkpoint end-to-end execution_runner dry-run result-only`.

## 67. PROMPT 2.29.1 - Checkpoint end-to-end execution_runner dry-run result-only

Estado: `PASSED_DRY_RUN_RESULT_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_RUNNER_DRY_RUN_RESULT_ONLY_E2E_CHECKPOINT.md`;
- test E2E reforzado: `tests/test_execution_runner_dry_run_result_only_end_to_end.py`;
- implementacion validada: `core/execution_runner.py`.

Decision:

`execution_runner dry-run result-only` queda validado E2E para `agent` y `team` sobre cadena completa: sandbox, promotion gate, approval workflow, promotion executor, active interno, runtime contract, execution contract, runtime executor contract, runtime prepare, execution runner contract, dry-run contract, prepare, run, abort y rollback.

Resultado:

- dry-run result-only validado E2E;
- `prepare_dry_run` devuelve `prepared`;
- `run_dry_run` devuelve `simulated`;
- `abort_dry_run` devuelve `aborted`;
- `rollback_dry_run` devuelve `rolled_back`;
- idempotency/replay result-only validado con registry in-memory;
- sin execution attempt;
- sin execution attempt store;
- sin `dry_run_store` persistente;
- sin ejecucion real;
- sin modelo/tool/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion;
- sin contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de `dry_run_store` o `execution attempt store`. No habilitar store/attempt directo sin auditoria previa.

## 68. PROMPT 2.30 - Auditoria de frontera dry_run_store vs execution_attempt_store

Estado: `DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/DRY_RUN_STORE_VS_EXECUTION_ATTEMPT_STORE_BOUNDARY_AUDIT.md`;
- tests: `tests/test_dry_run_store_vs_execution_attempt_store_boundary_audit.py`.

Decision:

`dry_run_store` y `execution_attempt_store` quedan separados. `dry_run_store` guarda simulaciones declarativas `dry_run_result_only`; `execution_attempt_store` guardaria intentos de ejecucion real o pre-ejecucion operativa y no esta listo.

Resultado:

- politica recomendada: `DRY_RUN_STORE_FIRST`;
- persistencia recomendada futura: `APPEND_ONLY_JSONL`;
- readiness principal: `DRY_RUN_STORE_READY_FOR_CONTRACT_ONLY`;
- `EXECUTION_ATTEMPT_STORE_NOT_READY`;
- no se crea `core/dry_run_store.py`;
- no se crea `core/execution_attempt_store.py`;
- no se crea storage real;
- no hay persistencia nueva;
- no se crea execution attempt;
- no se habilita ejecucion real;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target.

Recomendacion:

El proximo paso seguro es `PROMPT 2.31 - Disenar dry_run_store_contract append-only sin implementation`.

## 69. PROMPT 2.31 - Disenar dry_run_store_contract append-only sin implementation

Estado: `DRY_RUN_STORE_CONTRACT_PASSED`.

Evidencia:

- schema: `core/dry_run_store_schema.py`;
- validador: `core/dry_run_store_contract.py`;
- tests: `tests/test_dry_run_store_contract.py`;
- documento: `docs/DRY_RUN_STORE_CONTRACT_APPEND_ONLY.md`.

Decision:

Se define el contrato declarativo `dry_run_store_contract` en modo `dry_run_store_contract_only`. El contrato valida `DryRunResult` result-only para `agent` y `team`, exige refs de cadena, audit store verificado, observability valida, capability policy, idempotencia, checksum `sha256`, retention y politica append-only.

Resultado:

- storage futuro permitido: `append_only_jsonl`;
- formatos futuros bloqueados: `append_only_json`, `database_future`, `in_memory_only`, `audit_store_only`, `execution_attempt_store_future`;
- targets directos permitidos: `agent` y `team`;
- targets internos/no operativos bloqueados;
- payloads reales bloqueados;
- `execution_attempt_id` bloqueado;
- no se crea `core/dry_run_store.py`;
- no se crea `core/execution_attempt_store.py`;
- no se escribe JSONL;
- no se crea store real;
- no se ejecutan agentes/equipos;
- sin modelo/tool/memoria/external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion de targets ni artefactos.

Recomendacion:

El proximo paso seguro es un checkpoint end-to-end de `dry_run_store_contract` antes de cualquier implementacion append-only real.

## 70. PROMPT 2.31.1 - Checkpoint end-to-end dry_run_store_contract sobre dry-run result-only

Estado: `PASSED_DRY_RUN_STORE_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/DRY_RUN_STORE_CONTRACT_E2E_CHECKPOINT.md`;
- test E2E: `tests/test_dry_run_store_contract_end_to_end.py`;
- contrato validado: `core/dry_run_store_contract.py`.

Decision:

Se valida E2E que `dry_run_store_contract` puede pasar en modo `dry_run_store_contract_only` para `agent` y `team` usando `DryRunResult` real result-only producido por `execution_runner`.

Resultado:

- cadena completa validada desde sandbox hasta `dry_run_store_contract`;
- `agent` y `team` activos;
- runtime/execution/runtime_executor/execution_runner/dry-run contracts passed;
- `prepare_dry_run` prepared;
- `run_dry_run` simulated;
- storage declarado: `append_only_jsonl`;
- entry, append-only, idempotency, checksum, refs, payload boundary, retention, audit y observability contracts validados;
- sin `core/dry_run_store.py`;
- sin JSONL real;
- sin storage real;
- sin `core/execution_attempt_store.py`;
- sin `execution_attempt_id`;
- sin execution attempt;
- sin ejecucion real;
- sin modelo/tool/memoria/external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de implementacion `dry_run_store` append-only.

## 71. PROMPT 2.32 - Auditoria de frontera de implementacion dry_run_store append-only

Estado: `DRY_RUN_STORE_READY_FOR_APPEND_ONLY_IMPLEMENTATION`.

Estado complementario: `EXECUTION_ATTEMPT_STORE_NOT_READY`.

Evidencia:

- auditoria: `docs/DRY_RUN_STORE_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- tests: `tests/test_dry_run_store_implementation_boundary_audit.py`.

Decision:

Se audita la frontera de implementacion futura de `dry_run_store` append-only. La implementacion no se crea en este prompt.

Resultado:

- archivo futuro permitido: `core/dry_run_store.py`;
- funciones futuras permitidas: append, read by id, list read-only, verify e idempotency replay;
- ubicacion futura recomendada: `runtime/dry_runs/dry_run_store.jsonl`;
- formato futuro: JSONL append-only con serializacion canonica y checksum `sha256`;
- idempotency scope: target, correlation, idempotency key, dry-run id y dry-run contract ref;
- relacion con `audit_store`: complementaria, compartiendo `correlation_id`;
- relacion con `execution_attempt_store`: separada, no lista;
- no se crea `core/dry_run_store.py`;
- no se crea JSONL real;
- no se crea storage real;
- no se crea `core/execution_attempt_store.py`;
- no se crea `execution_attempt_id`;
- no se crea execution attempt;
- no se habilita ejecucion real;
- sin modelo/tool/memoria/external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni artefactos globales.

Recomendacion:

El proximo paso seguro es implementar `core/dry_run_store.py` append-only en un prompt dedicado, manteniendo esta frontera.

## 72. PROMPT 2.33 - Implementar dry_run_store append-only sin execution attempts

Estado: `PASSED_DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/dry_run_store.py`;
- tests unitarios: `tests/test_dry_run_store_append_only.py`;
- tests E2E: `tests/test_dry_run_store_append_only_end_to_end.py`;
- documento: `docs/DRY_RUN_STORE_APPEND_ONLY_IMPLEMENTATION.md`.

Decision:

Se implementa `dry_run_store` append-only JSONL para persistir `DryRunResult` result-only solo cuando `dry_run_store_contract` esta `passed`.

Resultado:

- `core/dry_run_store.py` creado;
- append-only JSONL implementado;
- serializacion canonica implementada;
- checksum `sha256` implementado;
- `previous_entry_checksum` implementado;
- idempotency real implementada;
- lectura por `dry_run_id` implementada;
- listado read-only implementado;
- verify/tamper evidence implementado;
- payload boundary profundo implementado;
- storage path configurable;
- tests escriben solo en `tmp_path`;
- sin `core/execution_attempt_store.py`;
- sin `execution_attempt_id`;
- sin execution attempt;
- sin execution lifecycle;
- sin ejecucion real;
- sin modelo/tool/memoria/external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni artefactos globales.

Recomendacion:

El proximo paso seguro es `PROMPT 2.33.1 - Checkpoint end-to-end dry_run_store append-only`.

## 73. PROMPT 2.33.1 - Checkpoint end-to-end dry_run_store append-only

Estado: `PASSED_DRY_RUN_STORE_APPEND_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/DRY_RUN_STORE_APPEND_ONLY_E2E_CHECKPOINT.md`;
- test E2E reforzado: `tests/test_dry_run_store_append_only_end_to_end.py`.

Decision:

Se valida E2E `dry_run_store` append-only sobre cadena sandbox completa para `agent` y `team`, usando JSONL controlado en `tmp_path`.

Resultado:

- `dry_run_store` append-only validado E2E;
- JSONL en `tmp_path`;
- append/get/list/verify/idempotency validados;
- checksum `sha256` validado;
- `previous_entry_checksum` validado;
- canonical serialization validada;
- tamper evidence validado;
- payload boundary profundo validado;
- sin `core/execution_attempt_store.py`;
- sin `execution_attempt_id`;
- sin execution attempt;
- sin execution lifecycle;
- sin ejecucion real;
- sin payloads reales;
- sin modelo/tool/memoria/external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de `execution_attempt_store` contract.

## 74. PROMPT 2.34 - Auditoria de frontera execution_attempt_store contract

Estado: `ATTEMPT_STORE_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/EXECUTION_ATTEMPT_STORE_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_attempt_store_boundary_audit.py`.

Decision:

Se audita la frontera conceptual y tecnica de `execution_attempt_store` antes de disenar su contrato. IA_CORE esta listo para un contrato futuro preflight-only y contract-only, no para implementacion ni ejecucion.

Resultado:

- `execution_attempt_store` auditado;
- `execution_attempt_store` no implementado;
- no se crea `core/execution_attempt_store.py`;
- no se crea `execution_attempt_id`;
- no se crea execution attempt;
- no se crea execution lifecycle;
- no se crea execution_history_store;
- no se habilita ejecucion real;
- `dry_run_store` queda separado y validado como simulacion append-only;
- datos futuros permitidos: refs, summaries, blockers, audit/observability refs, checksum e idempotencia;
- datos prohibidos: payloads reales, agent/team outputs, model prompt/response, tool call/result, memoria, external, scheduler, worker, mutaciones, secretos y credenciales;
- estados preflight-only futuros permitidos: `created`, `preflight_passed`, `preflight_blocked`, `blocked`, `failed`, `not_applicable`;
- estados bloqueados: `queued_future`, `running_future`, `completed_future`, `model_invoked`, `tool_executed`, `memory_persisted`, `external_accessed`;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

El proximo paso seguro es `PROMPT 2.35 - Disenar execution_attempt_store_contract preflight-only sin implementation`.

## 75. PROMPT 2.35 - Disenar execution_attempt_store_contract preflight-only sin implementation

Estado: `EXECUTION_ATTEMPT_STORE_CONTRACT_PASSED`.

Evidencia:

- schema: `core/execution_attempt_store_schema.py`;
- contrato: `core/execution_attempt_store_contract.py`;
- tests: `tests/test_execution_attempt_store_contract.py`;
- documento: `docs/EXECUTION_ATTEMPT_STORE_CONTRACT_PREFLIGHT_ONLY.md`.

Decision:

Se crea `execution_attempt_store_contract` en modo `execution_attempt_store_contract_only` y `preflight_only`. El contrato valida que un futuro attempt store solo podria registrar intencion/preflight por referencia a dry-run verificado, contratos runtime/execution, audit/observability, `correlation_id` e `idempotency_key`.

Resultado:

- `execution_attempt_store_contract` creado;
- preflight-only;
- contract-only;
- `store_type=execution_attempt_store`;
- `storage_format=append_only_jsonl_future`;
- dry-run dependency obligatoria: `dry_run_ref`, `dry_run_store_ref`, `dry_run_store_verified`, `dry_run_store_checksum_ref`, `dry_run_store_contract_ref`;
- attempt id policy: generation/persistence/materialization disabled;
- lifecycle real bloqueado;
- estados preflight-only permitidos: `created`, `preflight_passed`, `preflight_blocked`, `blocked`, `failed`, `not_applicable`;
- estados operativos bloqueados: `queued`, `running`, `completed`, `cancelled`, `model_invoked`, `tool_executed`, `memory_persisted`, `external_accessed`, `scheduler_started`, `worker_started`;
- payloads reales bloqueados profundamente;
- append-only/checksum future policy declarada sin implementacion;
- audit/observability refs obligatorios;
- eventos contract-only permitidos y eventos de ejecucion prohibidos;
- sin `core/execution_attempt_store.py`;
- sin `execution_attempt_id` operativo;
- sin execution attempt real;
- sin execution lifecycle real;
- sin ejecucion real;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target.

Recomendacion:

El proximo paso seguro es `PROMPT 2.35.1 - Checkpoint end-to-end execution_attempt_store_contract preflight-only`.

## 76. PROMPT 2.35.1 - Checkpoint end-to-end execution_attempt_store_contract preflight-only

Estado: `PASSED_EXECUTION_ATTEMPT_STORE_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_ATTEMPT_STORE_CONTRACT_E2E_CHECKPOINT.md`;
- test E2E: `tests/test_execution_attempt_store_contract_end_to_end.py`.

Decision:

Se valida end-to-end `execution_attempt_store_contract` para `agent` y `team`, usando cadena completa hasta `dry_run_store` real verificado en `tmp_path`.

Resultado:

- `execution_attempt_store_contract` validado E2E;
- `agent` y `team` activos;
- runtime/execution/runtime executor/execution runner/dry-run contracts passed;
- runtime prepare `prepared`;
- `prepare_dry_run` `prepared`;
- `run_dry_run` `simulated`;
- `dry_run_store_contract` `passed`;
- append de `dry_run_store` real solo en `tmp_path`;
- `verify_dry_run_store` `verified`;
- `execution_attempt_store_contract` `passed`;
- preflight-only;
- contract-only;
- sin `core/execution_attempt_store.py`;
- sin `execution_attempt_id` operativo;
- sin execution attempt real;
- sin lifecycle real;
- sin JSONL attempts real;
- sin ejecucion real;
- sin payloads reales;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de implementacion `execution_attempt_store` preflight-only.

## 77. PROMPT 2.36 - Auditoria de frontera de implementacion execution_attempt_store preflight-only

Estado: `EXECUTION_ATTEMPT_STORE_READY_FOR_PREFLIGHT_ONLY_IMPLEMENTATION`.

Evidencia:

- auditoria: `docs/EXECUTION_ATTEMPT_STORE_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_attempt_store_implementation_boundary_audit.py`.

Decision:

Se audita la frontera de implementacion futura de `execution_attempt_store` preflight-only. La implementacion no se crea en este prompt.

Resultado:

- `execution_attempt_store` implementation auditada;
- implementation no creada;
- `core/execution_attempt_store.py` no creado;
- archivo futuro permitido: `core/execution_attempt_store.py`;
- funciones futuras permitidas: build/append/get/list/verify/replay/checksum/canonical/validate de preflight;
- funciones de ejecucion prohibidas;
- storage recomendado futuro: `runtime/execution_attempts/execution_attempt_store.jsonl`;
- storage debe ser configurable/testable y tests futuros deben usar `tmp_path`;
- attempt_ref policy definida;
- `execution_attempt_id` operativo no creado;
- attempt id generation/persistence/materialization disabled;
- execution lifecycle real no creado;
- attempts JSONL no escrito;
- ejecucion real no habilitada;
- payloads reales prohibidos;
- dependencia obligatoria de `dry_run_store` verified;
- idempotency scope definido;
- canonical serialization/checksum sha256 definidos;
- relacion con audit_store/observability definida por `correlation_id`;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

El proximo paso seguro es implementar `execution_attempt_store` preflight-only en prompt dedicado, manteniendo bloqueados lifecycle real, ejecucion real, modelos/tools/memoria, external access, scheduler y worker queue.

## 78. PROMPT 2.37 - Implementar execution_attempt_store preflight-only sin execution_attempt_id operativo

Estado: `PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/execution_attempt_store.py`;
- documentacion: `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION.md`;
- tests unitarios: `tests/test_execution_attempt_store_preflight_only.py`;
- tests E2E: `tests/test_execution_attempt_store_preflight_only_end_to_end.py`.

Decision:

Se implementa `execution_attempt_store` preflight-only como JSONL append-only de intencion/preflight, validado por `execution_attempt_store_contract` passed y `dry_run_store` verified.

Resultado:

- `core/execution_attempt_store.py` creado;
- preflight-only JSONL append-only implementado;
- `ExecutionAttemptPreflightStoreEntry` implementado;
- `ExecutionAttemptStoreOperationResult` implementado;
- `attempt_ref` declarativo implementado;
- checksum sha256 implementado;
- serialization canonica implementada;
- `previous_entry_checksum` implementado;
- idempotency real implementada;
- append/read/list/verify implementados;
- payload boundary profundo implementado;
- storage path configurable y testeado con `tmp_path`;
- sin `execution_attempt_id` operativo;
- sin execution attempt real;
- sin execution lifecycle real;
- sin `execution_history_store`;
- sin ejecucion real;
- sin modelos/tools/memoria;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

Ejecutar `PROMPT 2.37.1 - Checkpoint end-to-end execution_attempt_store preflight-only`.

## 79. PROMPT 2.37.1 - Checkpoint end-to-end execution_attempt_store preflight-only

Estado: `PASSED_EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_E2E_CHECKPOINT.md`;
- implementacion actualizada: `docs/EXECUTION_ATTEMPT_STORE_PREFLIGHT_ONLY_IMPLEMENTATION.md`;
- tests E2E reforzados: `tests/test_execution_attempt_store_preflight_only_end_to_end.py`;
- tests unitarios/base: `tests/test_execution_attempt_store_preflight_only.py`.

Decision:

Se valida `execution_attempt_store` preflight-only end-to-end para `agent` y `team`, usando JSONL controlado en `tmp_path` y manteniendo cerradas las fronteras de attempt ID operativo, lifecycle real, ejecucion, payloads reales y mutacion.

Resultado:

- execution_attempt_store preflight-only validado E2E;
- JSONL en `tmp_path`;
- `attempt_ref` declarativo validado;
- append/get/list/verify/idempotency validados;
- checksum sha256 validado;
- `previous_entry_checksum` validado;
- payload boundary profundo validado;
- blockers negativos validados;
- sin `execution_attempt_id` operativo;
- sin lifecycle real;
- sin ejecucion real;
- sin payloads reales;
- sin external/UI/integraciones;
- sin scheduler/worker queue;
- sin mutacion target ni contaminacion legacy/global.

Recomendacion:

Listo para auditar frontera de execution lifecycle contract.

## 80. PROMPT 2.38 - Auditoria de frontera execution lifecycle contract

Estado: `LIFECYCLE_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/EXECUTION_LIFECYCLE_CONTRACT_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_lifecycle_contract_boundary_audit.py`.

Decision:

Se audita la frontera previa al diseno de `execution_lifecycle_contract`, partiendo de `execution_attempt_store` preflight-only E2E y manteniendo lifecycle real, execution attempt real, scheduler/worker, modelos/tools/memoria/external access y mutaciones fuera de alcance.

Resultado:

- execution lifecycle contract auditado;
- readiness: `LIFECYCLE_READY_FOR_CONTRACT_ONLY`;
- `core/execution_lifecycle.py` no creado;
- `core/execution_lifecycle_contract.py` no creado;
- `core/execution_lifecycle_schema.py` no creado;
- `core/execution_attempt_lifecycle.py` no creado;
- `core/execution_attempt_id.py` no creado;
- `core/execution_history_store.py` no creado;
- scheduler/worker no creado;
- ejecucion real no habilitada;
- agent/team execution no habilitada;
- model invocation no habilitada;
- tool execution no habilitada;
- memory persistence no habilitada;
- external access no habilitada;
- UI/integraciones no tocadas;
- targets no mutados.

Recomendacion:

`PROMPT 2.39 - Disenar execution_lifecycle_contract preflight-transitions-only sin implementation`.

## 81. PROMPT 2.39 - Disenar execution_lifecycle_contract preflight-transitions-only sin implementation

Estado: `EXECUTION_LIFECYCLE_CONTRACT_PASSED`.

Evidencia:

- schema: `core/execution_lifecycle_schema.py`;
- contrato: `core/execution_lifecycle_contract.py`;
- documentacion: `docs/EXECUTION_LIFECYCLE_CONTRACT_PREFLIGHT_TRANSITIONS_ONLY.md`;
- tests: `tests/test_execution_lifecycle_contract.py`.

Decision:

Se disena `execution_lifecycle_contract` como contrato declarativo preflight-transitions-only sobre `attempt_ref` declarativo y evidencia referencial verified de `execution_attempt_store` y `dry_run_store`.

Resultado:

- execution_lifecycle_contract creado;
- preflight-transitions-only;
- contract-only;
- estados preflight permitidos definidos;
- transiciones preflight permitidas definidas;
- estados operativos bloqueados;
- transiciones operativas bloqueadas;
- attempt_ref declarativo requerido;
- `execution_attempt_id` operativo bloqueado;
- dependencies y refs cruzadas validadas;
- boundary de ejecucion validado;
- payload boundary profundo validado;
- audit/observability policy validada;
- sin `core/execution_lifecycle.py`;
- sin `core/execution_attempt_lifecycle.py`;
- sin execution lifecycle real;
- sin execution attempt real;
- sin scheduler/worker queue;
- sin ejecucion real;
- sin payloads reales;
- sin mutacion target.

Recomendacion:

`PROMPT 2.39.1 - Checkpoint end-to-end execution_lifecycle_contract preflight-transitions-only`.

## 82. PROMPT 2.39.1 - Checkpoint end-to-end execution_lifecycle_contract preflight-transitions-only

Estado: `PASSED_EXECUTION_LIFECYCLE_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_LIFECYCLE_CONTRACT_E2E_CHECKPOINT.md`;
- tests E2E: `tests/test_execution_lifecycle_contract_end_to_end.py`;
- documentacion actualizada: `docs/EXECUTION_LIFECYCLE_CONTRACT_PREFLIGHT_TRANSITIONS_ONLY.md`.

Decision:

Se valida `execution_lifecycle_contract` end-to-end para `agent` y `team`, sobre cadena completa y stores verified reales en `tmp_path`.

Resultado:

- execution_lifecycle_contract validado E2E;
- sobre `execution_attempt_store` verified real en `tmp_path`;
- sobre `dry_run_store` verified real en `tmp_path`;
- preflight-transitions-only;
- contract-only;
- estados permitidos validados;
- transiciones permitidas validadas;
- state leaks bloqueados;
- transition leaks bloqueados;
- attempt ID leaks bloqueados;
- execution leaks bloqueados;
- payload leaks bloqueados;
- eventos prohibidos bloqueados;
- sin `core/execution_lifecycle.py`;
- sin `core/execution_attempt_lifecycle.py`;
- sin `execution_attempt_id` operativo;
- sin lifecycle real;
- sin scheduler/worker;
- sin ejecucion real;
- sin payloads reales;
- sin mutacion.

Recomendacion:

Listo para auditar frontera de implementacion execution_lifecycle preflight-transitions-only.

## 83. PROMPT 2.40 - Auditoria de frontera de implementacion execution_lifecycle preflight-transitions-only

Estado: `EXECUTION_LIFECYCLE_READY_FOR_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION`.

Evidencia:

- auditoria: `docs/EXECUTION_LIFECYCLE_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_lifecycle_implementation_boundary_audit.py`.

Decision:

Se audita la frontera antes de implementar `execution_lifecycle.py`. La evidencia de `execution_lifecycle_contract` E2E, `execution_attempt_store` verified y `dry_run_store` verified permite una implementacion futura limitada a append-only preflight transitions.

Resultado:

- implementation boundary audit creada;
- `core/execution_lifecycle.py` no creado;
- execution_lifecycle implementation no creada;
- `execution_attempt_id` operativo no creado;
- execution attempt real no creado;
- `execution_history_store` no creado;
- scheduler/worker no creado;
- ejecucion real no habilitada;
- estados `queued/running/completed/cancelled/rolled_back` siguen bloqueados;
- store futuro permitido solo append-only JSONL con path configurable y tests en `tmp_path`;
- readiness real: `EXECUTION_LIFECYCLE_READY_FOR_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION`.

Recomendacion:

`PROMPT 2.41 - Implementar execution_lifecycle preflight-transitions-only append-only`.

## 84. PROMPT 2.41 - Implementar execution_lifecycle preflight-transitions-only append-only

Estado: `PASSED_EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/execution_lifecycle.py`;
- documentacion: `docs/EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_IMPLEMENTATION.md`;
- tests unitarios: `tests/test_execution_lifecycle_preflight_transitions_only.py`;
- tests E2E: `tests/test_execution_lifecycle_preflight_transitions_only_end_to_end.py`;
- frontera contractual actualizada: `core/execution_lifecycle_contract.py`;
- checkpoint contractual actualizado: `tests/test_execution_lifecycle_contract_end_to_end.py`.

Decision:

Se implementa `execution_lifecycle` solo como store append-only de transiciones preflight, consumiendo `execution_lifecycle_contract passed` y dependencias verified de `execution_attempt_store` y `dry_run_store`.

Resultado:

- `core/execution_lifecycle.py` creado;
- JSONL append-only con path configurable;
- tests escriben solo en `tmp_path`;
- checksum `sha256` por entrada;
- `previous_entry_checksum`;
- `sequence_number` monotono;
- canonical serialization;
- get/list/verify read-only;
- idempotency noop/conflict;
- estados preflight permitidos;
- transiciones preflight permitidas;
- estados/transiciones operativas bloqueadas;
- `execution_attempt_id` operativo bloqueado;
- scheduler/worker bloqueado;
- modelos/tools/memoria/external access bloqueados;
- payloads reales bloqueados;
- sin mutacion target;
- sin `core/execution_attempt_lifecycle.py`;
- sin `core/execution_attempt_id.py`;
- sin `core/execution_history_store.py`;
- sin scheduler/worker queue.

Recomendacion:

`PROMPT 2.41.1 - Checkpoint E2E execution_lifecycle preflight-transitions-only append-only`.

## 85. PROMPT 2.41.1 - Checkpoint E2E execution_lifecycle preflight-transitions-only append-only

Estado: `PASSED_EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_LIFECYCLE_PREFLIGHT_TRANSITIONS_ONLY_E2E_CHECKPOINT.md`;
- E2E reforzado: `tests/test_execution_lifecycle_preflight_transitions_only_end_to_end.py`;
- implementacion validada: `core/execution_lifecycle.py`.

Decision:

Se valida end-to-end `execution_lifecycle` append-only para `agent` y `team`, sobre cadena completa y stores reales aislados en `tmp_path`.

Resultado:

- `execution_lifecycle` append-only validado E2E;
- `agent` y `team`;
- `dry_run_store` real en `tmp_path` append/verify;
- `execution_attempt_store` real en `tmp_path` append/verify;
- `execution_lifecycle_store` real en `tmp_path` append/get/list/verify;
- idempotency replay;
- idempotency conflict bloqueado;
- checksum chain;
- `previous_entry_checksum`;
- `sequence_number` monotonico;
- sin `execution_attempt_id` operativo;
- sin execution attempt real;
- sin `execution_history_store`;
- sin scheduler/worker queue;
- sin `queued/running/completed` reales;
- sin ejecucion real;
- sin modelos/tools/memoria;
- sin external access;
- sin payloads reales;
- sin mutacion target;
- sin JSONL runtime real fuera de `tmp_path`.

Recomendacion:

Listo para auditar frontera de execution history / attempt history contract.

## 86. PROMPT 2.42 - Auditoria de frontera execution history / attempt history contract

Estado: `HISTORY_READY_FOR_DERIVED_VIEW_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/EXECUTION_HISTORY_ATTEMPT_HISTORY_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_history_attempt_history_boundary_audit.py`;
- stores primarios existentes: `dry_run_store`, `execution_attempt_store`, `execution_lifecycle`.

Decision:

Se audita la frontera entre lifecycle store, attempt history, execution history, result history y execution attempt real. La decision segura es no crear store nuevo: primero disenar `execution_history_view_contract` como vista derivada, preflight-only, contract-only y sin JSONL propio.

Resultado:

- history boundary audit creada;
- `execution_history_store` no creado;
- `attempt_history` no creado;
- `execution_result_store` no creado;
- `execution_attempt_id` operativo no creado;
- history view derived-only recomendada;
- stores primarios existentes deben seguir siendo la fuente de verdad;
- sin execution attempt real;
- sin result history real;
- sin scheduler/worker queue;
- sin `queued/running/completed` reales;
- sin ejecucion real;
- sin payloads reales;
- readiness real: `HISTORY_READY_FOR_DERIVED_VIEW_CONTRACT_ONLY`.

Recomendacion:

`PROMPT 2.43 - Disenar execution_history_view_contract derived-only preflight-only sin store`.

## 87. PROMPT 2.43 - Disenar execution_history_view_contract derived-only preflight-only sin store

Estado: `EXECUTION_HISTORY_VIEW_CONTRACT_PASSED`.

Evidencia:

- schema: `core/execution_history_view_schema.py`;
- contrato: `core/execution_history_view_contract.py`;
- tests: `tests/test_execution_history_view_contract.py`;
- documentacion: `docs/EXECUTION_HISTORY_VIEW_CONTRACT_DERIVED_ONLY.md`.

Decision:

Se crea `execution_history_view_contract` como contrato declarativo derived-only, preflight-only y contract-only. La vista se deriva de `dry_run_store`, `execution_attempt_store` y `execution_lifecycle_store` verified, sin store propio.

Resultado:

- `execution_history_view_contract` creado;
- derived-only;
- preflight-only;
- contract-only;
- sin `execution_history_store`;
- sin attempt_history store;
- sin `execution_result_store`;
- sin `execution_attempt_id` operativo;
- sin JSONL history;
- sin ejecucion real;
- sin payloads reales;
- sin mutacion target;
- timeline permitido definido;
- estados permitidos/bloqueados definidos;
- dependency policy validada;
- store prohibition policy validada;
- attempt ID policy validada;
- execution boundary policy validada;
- payload boundary profundo validado.

Recomendacion:

`PROMPT 2.43.1 - Checkpoint E2E execution_history_view_contract derived-only preflight-only`.

## 88. PROMPT 2.43.1 - Checkpoint E2E execution_history_view_contract derived-only preflight-only

Estado: `PASSED_EXECUTION_HISTORY_VIEW_CONTRACT_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_HISTORY_VIEW_CONTRACT_E2E_CHECKPOINT.md`;
- test E2E: `tests/test_execution_history_view_contract_end_to_end.py`;
- contrato base: `core/execution_history_view_contract.py`.

Decision:

Se valida end-to-end el contrato de vista historica derivada sobre la cadena completa y stores primarios reales aislados en `tmp_path`, para `agent` y `team`.

Resultado:

- `agent` y `team` validados;
- `dry_run_store` append/verify real en `tmp_path`;
- `execution_attempt_store` append/verify real en `tmp_path`;
- `execution_lifecycle_store` append/verify real en `tmp_path`;
- `execution_history_view_contract` passed;
- `summary`, `timeline`, `preflight_status`, `transition_history`, `store_verification_summary`, `boundary_summary`, `risk_summary` y `evidence` validados como vista derivada;
- `audit_refs`, `observability_refs`, `capability_policy_ref`, `correlation_id`, `idempotency_key`, `target_ref` y `attempt_ref` declarativo validados;
- leaks de store/history/result bloqueados;
- leaks de `execution_attempt_id` operativo bloqueados;
- estados y eventos operativos bloqueados;
- ejecucion/modelos/tools/memoria/external access/scheduler/worker bloqueados;
- payloads reales bloqueados;
- mismatches de refs bloqueados;
- sin `execution_history_store`;
- sin `attempt_history store`;
- sin `execution_result_store`;
- sin `execution_attempt_id` operativo;
- sin JSONL history propio;
- sin ejecucion real;
- sin mutacion target;
- sin JSONL runtime real fuera de `tmp_path`.

Recomendacion:

Listo para auditar frontera de derived history view implementation sin store.

## 89. PROMPT 2.44 - Auditoria de frontera de implementacion derived history view sin store

Estado: `HISTORY_VIEW_READY_FOR_DERIVED_ONLY_IMPLEMENTATION`.

Evidencia:

- auditoria: `docs/EXECUTION_HISTORY_VIEW_IMPLEMENTATION_BOUNDARY_AUDIT.md`;
- tests: `tests/test_execution_history_view_implementation_boundary_audit.py`;
- contrato E2E previo: `docs/EXECUTION_HISTORY_VIEW_CONTRACT_E2E_CHECKPOINT.md`;
- contrato base: `core/execution_history_view_contract.py`.

Decision:

Se audita la frontera antes de implementar `core/execution_history_view.py`. La implementacion futura queda permitida solo como vista derivada in-memory, `preflight-only`, sin store propio y sin JSONL propio.

Resultado:

- implementation boundary audit creada;
- `core/execution_history_view.py` no creado;
- `execution_history_store` no creado;
- `attempt_history store` no creado;
- `execution_result_store` no creado;
- `execution_attempt_id` operativo no creado;
- JSONL history no creado;
- JSONL result no creado;
- archivo futuro permitido: `core/execution_history_view.py`;
- archivos bloqueados: `core/execution_history_store.py`, `core/attempt_history.py`, `core/execution_attempt_history.py`, `core/execution_result_store.py`, `core/execution_attempt_id.py`, `core/scheduler_queue.py`, `core/worker_queue.py`;
- funciones futuras permitidas: `build_execution_history_view`, `derive_execution_history_timeline`, `derive_preflight_status`, `derive_transition_history`, `derive_store_verification_summary`, `derive_boundary_summary`, `derive_risk_summary`, `validate_execution_history_view`;
- funciones de append/write/persist/store/result/attempt_id/execution/model/tool/memory/external/scheduler/worker bloqueadas;
- inputs futuros obligatorios: stores primarios entries + verified, `execution_history_view_contract passed`, `attempt_ref` declarativo, `target_ref`, `correlation_id`, `idempotency_key`, audit/observability/capability refs y contratos previos;
- outputs permitidos: `summary`, `timeline`, `preflight_status`, `transition_history`, `store_verification_summary`, `boundary_summary`, `risk_summary`, `evidence`, `warnings`, `blockers`;
- outputs prohibidos: `execution_result`, `execution_output`, `execution_history_payload`, `execution_result_history`, outputs de agent/team/model/tool/memory/external, secretos, credenciales y side effects;
- store/jsonl policy: sin store propio, sin JSONL propio, sin history path, sin result path, sin append, sin persistencia, sin escritura runtime;
- dependency policy: stores verified, contract passed y refs coincidentes;
- boundary policy: execution/model/tool/memory/external/scheduler/worker/history/result/attempt_id flags siguen en false;
- sin execution attempt real;
- sin `queued/running/completed` reales;
- sin ejecucion real;
- sin UI/integraciones;
- sin mutacion target.

Riesgo principal:

Convertir la vista en store, duplicar stores primarios o guardar payloads/resultados reales camuflados como resumen.

Recomendacion:

`PROMPT 2.45 - Implementar execution_history_view derived-only preflight-only sin store`.

## 90. PROMPT 2.45 - Implementar execution_history_view derived-only preflight-only sin store

Estado: `PASSED_EXECUTION_HISTORY_VIEW_DERIVED_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/execution_history_view.py`;
- documentacion: `docs/EXECUTION_HISTORY_VIEW_DERIVED_ONLY_IMPLEMENTATION.md`;
- tests unitarios: `tests/test_execution_history_view_derived_only.py`;
- E2E minimo: `tests/test_execution_history_view_derived_only_end_to_end.py`.

Decision:

Se implementa `execution_history_view` como vista historica derivada, in-memory, `derived-only` y `preflight-only`, construida desde stores primarios verificados y con `execution_history_view_contract` passed.

Resultado:

- `core/execution_history_view.py` creado;
- derived-only;
- preflight-only;
- in-memory;
- read/build only;
- `ExecutionHistoryView` creado;
- `ExecutionHistoryViewOperationResult` creado;
- `build_execution_history_view` creado;
- `derive_execution_history_timeline` creado;
- `derive_preflight_status` creado;
- `derive_transition_history` creado;
- `derive_store_verification_summary` creado;
- `derive_boundary_summary` creado;
- `derive_risk_summary` creado;
- `validate_execution_history_view` creado;
- sin store propio;
- sin JSONL propio;
- sin `execution_history_store`;
- sin `attempt_history store`;
- sin `execution_result_store`;
- sin `execution_attempt_id` operativo;
- sin ejecucion real;
- sin payloads reales;
- sin scheduler/worker;
- sin UI/integraciones;
- sin mutacion target.

Recomendacion:

`PROMPT 2.45.1 - Checkpoint E2E execution_history_view derived-only preflight-only`.

## 91. PROMPT 2.45.1 - Checkpoint E2E execution_history_view derived-only preflight-only

Estado: `PASSED_EXECUTION_HISTORY_VIEW_DERIVED_ONLY_E2E`.

Evidencia:

- checkpoint: `docs/EXECUTION_HISTORY_VIEW_DERIVED_ONLY_E2E_CHECKPOINT.md`;
- test: `tests/test_execution_history_view_derived_only_checkpoint_end_to_end.py`;
- implementacion validada: `core/execution_history_view.py`.

Decision:

Se crea checkpoint E2E fuerte para validar `execution_history_view` real de punta a punta, cubriendo `agent` y `team`, con stores primarios reales en `tmp_path` y `execution_history_view_contract` como dependencia obligatoria.

Resultado:

- checkpoint E2E creado;
- `agent` y `team` validados;
- cadena completa validada desde sandbox/promotion/active hasta `execution_history_view build/validate`;
- history view build/validate integrado;
- outputs derivados validados: `summary`, `timeline`, `preflight_status`, `transition_history`, `store_verification_summary`, `boundary_summary`, `risk_summary`, `evidence`, `warnings`, `blockers`;
- negativos cubiertos: contract no passed, store no verified, attempt mismatch, target mismatch, timeline completed, `execution_result`, history store enabled, `execution_attempt_id`, scheduler y external access;
- sin `execution_history_store`;
- sin `attempt_history store`;
- sin `execution_result_store`;
- sin `execution_attempt_id` operativo;
- sin JSONL history/result;
- sin ejecucion real;
- sin scheduler/worker;
- sin modelos/tools/memoria;
- sin external access;
- sin mutacion target;
- sin payloads reales.

Recomendacion:

`PROMPT 2.46 - Auditoria de frontera de read model interno`.

## 92. PROMPT 2.46 - Auditoria de frontera de read model interno

Estado: `READ_MODEL_READY_FOR_CONTRACT_ONLY`.

Evidencia:

- auditoria: `docs/INTERNAL_BACKEND_READ_MODEL_BOUNDARY_AUDIT.md`;
- test: `tests/test_internal_backend_read_model_boundary_audit.py`;
- cadena previa validada hasta `execution_history_view`.

Decision:

Se audita la frontera para una futura capa `internal_backend_read_model`. La decision segura es disenar primero un contrato read-only, sin crear implementacion, store, API ni dashboard adapter.

Fuentes permitidas futuras:

- domain/artifact state;
- sandbox materialization preview/result;
- promotion gate/executor result;
- active contract/executor result;
- runtime/execution contracts;
- runtime preparation;
- execution runner contract;
- dry-run contract/result-only;
- `dry_run_store`, `execution_attempt_store`, `execution_lifecycle` verified entries;
- `execution_history_view` derived view;
- audit/observability/capability refs.

Archivos futuros permitidos:

- `core/internal_backend_read_model_schema.py`;
- `core/internal_backend_read_model_contract.py`;
- `tests/test_internal_backend_read_model_contract.py`;
- `tests/test_internal_backend_read_model_contract_end_to_end.py`;
- `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md`.

Archivos todavia bloqueados:

- `core/internal_backend_read_model.py`;
- `core/backend_read_model_store.py`;
- `core/backend_status_api.py`;
- `core/backend_dashboard_adapter.py`.

Riesgos:

- convertir read model en API prematura;
- mezclar read-only con mutacion;
- duplicar stores;
- exponer payloads reales;
- crear snapshots persistidos antes de tiempo;
- acoplar UI a estructuras internas inestables.

Recomendacion:

`PROMPT 2.47 - Disenar internal_backend_read_model_contract read-only`.

## 93. PROMPT 2.47 - Disenar internal_backend_read_model_contract read-only

Estado: `INTERNAL_BACKEND_READ_MODEL_CONTRACT_PASSED`.

Evidencia:

- schema: `core/internal_backend_read_model_schema.py`;
- contract: `core/internal_backend_read_model_contract.py`;
- unit tests: `tests/test_internal_backend_read_model_contract.py`;
- E2E contractual: `tests/test_internal_backend_read_model_contract_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT.md`.

Decision:

Se disena el contrato read-only de `internal_backend_read_model`, sin implementar todavia el read model operativo, sin store, sin API y sin dashboard adapter.

Resultado:

- schema creado;
- contract creado;
- funciones publicas creadas: `validate_internal_backend_read_model_contract`, `build_internal_backend_read_model_contract_shape`, `validate_internal_backend_read_model_sources`, `validate_internal_backend_read_model_boundaries`, `validate_internal_backend_read_model_outputs`;
- modos permitidos: `internal_backend_read_model_contract_only`, `internal_backend_read_model_read_only`, `internal_backend_snapshot`;
- fuentes requeridas definidas;
- outputs permitidos definidos;
- outputs bloqueados definidos;
- boundary flags read-only/contract-only definidos;
- readiness contractual `ready_for_read_model_implementation` validada;
- E2E contractual `agent` y `team`;
- sin `core/internal_backend_read_model.py`;
- sin `core/backend_read_model_store.py`;
- sin `core/backend_status_api.py`;
- sin `core/backend_dashboard_adapter.py`.

Recomendacion:

`PROMPT 2.47.1 - Checkpoint E2E internal_backend_read_model_contract`.

## 94. PROMPT 2.47.1 - Checkpoint E2E internal_backend_read_model_contract

Estado: `PASSED_INTERNAL_BACKEND_READ_MODEL_CONTRACT_E2E`.

Evidencia:

- checkpoint: `tests/test_internal_backend_read_model_contract_checkpoint_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_CONTRACT_E2E_CHECKPOINT.md`;
- contrato base: `core/internal_backend_read_model_contract.py`;
- schema base: `core/internal_backend_read_model_schema.py`.

Decision:

Se valida end-to-end el contrato `internal_backend_read_model_contract` como snapshot contractual read-only, usando la cadena backend interna ya validada hasta `execution_history_view`, para `agent` y `team`.

Resultado:

- checkpoint E2E creado;
- `agent` y `team` validados;
- cadena contractual validada desde sandbox/promotion/active hasta `execution_history_view`;
- snapshot fields validados: `snapshot_id`, `schema_version`, `read_model_mode`, `generated_at`, `target_type`, `target_id`, `target_ref`, `domain_ref`, `source_refs`, summaries, readiness, blockers, warnings, evidence y boundary_summary;
- outputs permitidos validados: `summaries`, `derived_status`, `readiness`, `blockers`, `warnings`, `evidence`, `refs`, `counts`, `timestamps`, `contract_verdicts`, `boundary_summaries`;
- negativos cubiertos: source faltante, source no verified, history view no validated, `model_response`, `tool_result`, implementation/API/mutation/execution/external access enabled;
- sin `core/internal_backend_read_model.py`;
- sin `core/backend_read_model_store.py`;
- sin `core/backend_status_api.py`;
- sin `core/backend_dashboard_adapter.py`.

Recomendacion:

`PROMPT 2.48 - Implementar internal_backend_read_model read-only`.

## 95. PROMPT 2.48 - Implementar internal_backend_read_model read-only

Estado: `PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_IMPLEMENTATION`.

Evidencia:

- implementacion: `core/internal_backend_read_model.py`;
- unit tests: `tests/test_internal_backend_read_model_read_only.py`;
- E2E read-only: `tests/test_internal_backend_read_model_read_only_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_READ_ONLY_IMPLEMENTATION.md`;
- contrato base actualizado: `core/internal_backend_read_model_contract.py`.

Decision:

Se implementa `internal_backend_read_model` como builder/validator read-only e in-memory sobre sources contractuales verificadas. La implementacion no persiste snapshots, no crea store, no crea API, no crea dashboard adapter y no habilita ejecucion real.

Resultado:

- implementacion creada;
- tests creados;
- E2E creado;
- snapshot read-only con summaries, refs, readiness, blockers, warnings, evidence y boundary_summary;
- sources requeridas y flags verified validadas;
- outputs permitidos validados;
- outputs prohibidos bloqueados;
- boundaries read-only implementadas;
- `implementation_enabled=true`;
- `store_enabled=false`;
- `api_enabled=false`;
- `dashboard_adapter_enabled=false`;
- `mutation_enabled=false`;
- `execution_enabled=false`;
- `external_access_enabled=false`.

Recomendacion:

`PROMPT 2.48.1 - Checkpoint E2E internal_backend_read_model read-only`.

## 96. PROMPT 2.48.1 - Checkpoint E2E internal_backend_read_model read-only

Estado: `PASSED_INTERNAL_BACKEND_READ_MODEL_READ_ONLY_E2E`.

Evidencia:

- checkpoint: `tests/test_internal_backend_read_model_read_only_checkpoint_end_to_end.py`;
- documentacion: `docs/INTERNAL_BACKEND_READ_MODEL_READ_ONLY_E2E_CHECKPOINT.md`;
- implementacion validada: `core/internal_backend_read_model.py`.

Decision:

Se valida end-to-end la implementacion read-only del read model interno para `agent` y `team`, desde sources contractuales verificadas hasta build y validate del snapshot.

Resultado:

- checkpoint creado;
- `agent` y `team` validados;
- cadena E2E validada con contrato, build y validate;
- snapshot fields validados;
- outputs permitidos y bloqueados validados;
- boundaries read-only validadas;
- negativos cubiertos: source faltante, source no verified, history view no validated, outputs prohibidos, boundary leaks y modo invalido;
- sin `core/backend_read_model_store.py`;
- sin `core/backend_status_api.py`;
- sin `core/backend_dashboard_adapter.py`.

Recomendacion:

`PROMPT 2.49 - Auditoria final de backend interno pre-operacional`.

## 97. PROMPT 2.49 - Auditoria final de backend interno pre-operacional

Estado: `BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT`.

Evidencia:

- documento creado: `docs/BACKEND_INTERNAL_PRE_OPERATIONAL_FINAL_AUDIT.md`;
- test creado: `tests/test_backend_internal_pre_operational_final_audit.py`.

Decision:

Se audita el bloque backend interno 2.x completo antes del checkpoint integral 2.50. La cadena esta coherente, trazable y lista para validacion integral pre-operacional.

Resultado:

- documento creado;
- test creado;
- veredicto final: `BACKEND_INTERNAL_READY_FOR_INTEGRAL_CHECKPOINT`;
- gaps encontrados: sin critical ni major; minor/deferred no bloqueantes;
- riesgos antes de 2.50: suite pesada, tests lentos acumulados, drift documental, contratos verbosos, nombres largos, dependencia de fixtures y confusion pre-operacional/operacional;
- no se implementan features nuevas;
- no se crean stores, API, UI, scheduler, worker, ejecucion real, modelos/tools/memoria ni external access.

Recomendacion:

`PROMPT 2.50 - Checkpoint integral backend interno pre-operacional`.

## 98. PROMPT 2.50 - Checkpoint integral backend interno pre-operacional

Estado: `BACKEND_INTERNAL_PRE_OPERATIONAL_CHECKPOINT_PASSED`.

Readiness:

- `backend_internal_pre_operational_ready`;
- `ready_for_next_backend_phase_planning`.

Evidencia:

- checkpoint integral creado: `tests/test_backend_internal_pre_operational_integral_checkpoint.py`;
- documento creado: `docs/BACKEND_INTERNAL_PRE_OPERATIONAL_INTEGRAL_CHECKPOINT.md`.

Decision:

Se cierra el checkpoint integral del backend interno 2.x como bloque pre-operacional. No se implementan features nuevas.

Resultado:

- escenarios `agent` y `team`;
- cadena integral validada desde sandbox hasta read model build/validate;
- snapshot final read-only validado;
- veredictos esperados validados;
- gaps finales: critical none, major none, minor/deferred no bloqueantes;
- boundaries globales preservadas;
- features postergadas: execution real, execution_attempt_id operativo, result/history stores, scheduler/worker/queue, model invocation, tool execution, memory persistence, external access, API, dashboard adapter y UI/UX.

Recomendacion:

`PROMPT 2.51 - Plan de transicion hacia Backend Interno Fase 3.x`.

## 100. PROMPT 2.51 - Plan de transicion hacia Backend Interno Fase 3.x

Estado: `PHASE_3_TRANSITION_PLAN_READY`.

Funcion:

Cerrar formalmente 2.x y preparar 3.x sin activar runtime operativo.

Evidencia:

- plan: `docs/BACKEND_INTERNAL_PHASE_3_TRANSITION_PLAN.md`;
- test: `tests/test_backend_internal_phase_3_transition_plan.py`.

Resultado:

- 2.x queda cerrado como backend interno pre-operacional;
- proximo paso definido: `PROMPT 3.0 — Auditoría de frontera operacional`;
- Market Catalog queda como planned database no activa;
- Business Composition Layer queda futura/no operativa;
- siguen bloqueados runtime operativo, ejecucion real, scheduler, worker, queue, modelos/tools/memoria, external access, API y UI.

Recomendacion:

`PROMPT 3.0 — Auditoría de frontera operacional`.

## 101. PROMPT 3.0 - Auditoria de frontera operacional

Estado: `OPERATIONAL_BOUNDARY_AUDIT_COMPLETED`.

Veredicto: `OPERATIONAL_BOUNDARY_READY_FOR_CONTRACT_DESIGN`.

Readiness: `ready_for_execution_intent_contract`.

Evidencia:

- auditoria: `docs/BACKEND_INTERNAL_OPERATIONAL_BOUNDARY_AUDIT.md`;
- test: `tests/test_backend_internal_operational_boundary_audit.py`.

Decision:

Se audita la frontera operacional entre preflight/dry-run/read-only/derived history y futura ejecucion operativa real. No se activa runtime operativo ni ejecucion real.

Resultado:

- no hay gaps criticos;
- no hay gaps mayores bloqueantes;
- Market Catalog queda `planned_not_active`;
- Business Composition Layer queda futura/no operativa;
- runtime operativo, scheduler, worker, queue, modelos/tools/memoria, external access, API y UI siguen bloqueados.

Proximo paso:

`PROMPT 3.1 — Contrato de execution intent operativo`.

## 102. PROMPT 3.1 - Contrato de execution intent operativo

Estado: `EXECUTION_INTENT_CONTRACT_READY`.

Readiness: `ready_for_execution_attempt_id_audit`.

Evidencia:

- contrato: `core/execution_intent.py`;
- documentacion: `docs/EXECUTION_INTENT_CONTRACT.md`;
- tests: `tests/test_execution_intent_contract.py`.

Decision:

Se define `ExecutionIntent` como contrato operativo previo a attempt real. El contrato es contract-only y no ejecuta nada.

Resultado:

- schema de intent creado;
- valores permitidos definidos;
- constraints operativas obligatorias en false;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa;
- no attempts;
- no stores operativos;
- no scheduler/worker/queue;
- no modelos/tools/memoria;
- no external access;
- no API/UI.

Proximo paso:

`PROMPT 3.2 — Auditoría de execution_attempt_id operativo`.

## 99. PROMPT 2.50.1 - Market Catalog / Catalogo de Mercados

Estado: `MARKET_CATALOG_REGISTERED_AS_PLANNED_DATABASE`.

Evidencia:

- modulo: `core/market_catalog/`;
- database: `data/market_catalog/market_catalog.generated.json`;
- decision de producto: `docs/MARKET_CATALOG_PRODUCT_DECISION.md`;
- plan de activacion: `docs/MARKET_CATALOG_ACTIVATION_PLAN.md`;
- tests: `tests/test_market_catalog_planned_database.py`.

Decision:

El Market Catalog queda registrado desde PROMPT 2.50.1 como database externa no activa. Su funcion futura sera alimentar la Business Composition Layer para conectar areas, nichos internos, rubros de mercado, perfiles y unidades de negocio digital. No forma parte del runtime pre-operacional ni de la ejecucion actual.

Formula futura:

```txt
Area interna IA_CORE
+
Nicho interno IA_CORE
+
Rubro externo de mercado
+
Perfiles compatibles
=
Equipo operativo / unidad de negocio digital
```

Boundaries:

- `planned_not_active`;
- runtime deshabilitado;
- UI deshabilitada;
- business composition deshabilitada;
- no modifica catalogos internos activos;
- no habilita API, scheduler, worker, ejecucion real, modelos/tools/memoria ni external access.

Recomendacion:

`PROMPT 2.51 - Plan de transicion hacia Backend Interno Fase 3.x`.
## 103. PROMPT 3.2 - Auditoria de execution_attempt_id operativo

Estado esperado:

`EXECUTION_ATTEMPT_ID_AUDIT_COMPLETED`

Veredicto esperado:

`EXECUTION_ATTEMPT_ID_READY_FOR_SCHEMA_DESIGN`

Readiness esperada:

`ready_for_execution_attempt_schema`

Evidencia:

- auditoria: `docs/EXECUTION_ATTEMPT_ID_OPERATIONAL_AUDIT.md`;
- test: `tests/test_execution_attempt_id_operational_audit.py`.

Decision:

Se audita el `execution_attempt_id` operativo como identificador futuro de un ExecutionAttempt derivado de un ExecutionIntent validado. La auditoria no crea attempts reales, no crea generador operativo, no crea result store y no activa runtime.

Resultado:

- formato recomendado: `attempt_<intent_id>_<sequence>_<short_hash>`;
- ownership futuro: attempt factory / attempt builder controlado;
- `attempt_ref` preflight existente sigue separado del futuro `execution_attempt_id`;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa;
- sin scheduler/worker/queue;
- sin modelos/tools/memoria;
- sin external access;
- sin API/UI.

Proximo paso:

`PROMPT 3.3 — Schema de execution attempt operativo`

## 104. PROMPT 3.2.1 - Checkpoint E2E de execution_attempt_id operativo

Estado esperado:

`EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_PASSED`

Funcion:

Validar la cadena 3.0 -> 3.1 -> 3.2 antes del schema de ExecutionAttempt.

Evidencia:

- checkpoint: `docs/EXECUTION_ATTEMPT_ID_OPERATIONAL_E2E_CHECKPOINT.md`;
- test: `tests/test_execution_attempt_id_operational_e2e_checkpoint.py`.

Proximo paso:

`PROMPT 3.3 — Schema de execution attempt operativo`

## 105. PROMPT 3.3 - Schema de execution attempt operativo

Estado:

`EXECUTION_ATTEMPT_SCHEMA_READY`

Readiness:

`ready_for_operational_state_machine_contract`

Evidencia:

- schema: `core/execution_attempt.py`;
- documentacion: `docs/EXECUTION_ATTEMPT_SCHEMA.md`;
- checkpoint E2E: `docs/EXECUTION_ATTEMPT_SCHEMA_E2E_CHECKPOINT.md`;
- tests: `tests/test_execution_attempt_schema.py`, `tests/test_execution_attempt_schema_e2e_checkpoint.py`.

Decision:

Se define el molde oficial y validable de `ExecutionAttempt` como schema-only. El schema puede derivarse desde un `ExecutionIntent` validado, pero no crea attempts operativos reales ni genera IDs automaticamente.

Resultado:

- `attempt_id` recomendado: `attempt_<intent_id>_<sequence>_<short_hash>`;
- status permitidos: `draft`, `schema_validated`, `rejected`, `blocked`;
- lifecycle inicial permitido: `not_started`, `preflight_only`, `blocked`;
- constraints operativas obligatorias en false;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa;
- sin factory activa;
- sin store writes;
- sin result store;
- sin runtime execution.

Proximo paso:

`PROMPT 3.4 — State machine operacional contract-only`

## 106. PROMPT 3.4 - State machine operacional contract-only

Estado:

`EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT_READY`

Readiness:

`ready_for_result_store_boundary_audit`

Evidencia:

- contrato: `core/execution_attempt_state_machine.py`;
- documentacion: `docs/EXECUTION_ATTEMPT_STATE_MACHINE_CONTRACT.md`;
- checkpoint E2E: `docs/EXECUTION_ATTEMPT_STATE_MACHINE_E2E_CHECKPOINT.md`;
- tests: `tests/test_execution_attempt_state_machine_contract.py`, `tests/test_execution_attempt_state_machine_e2e_checkpoint.py`.

Decision:

Se define la maquina de estados contractual de `ExecutionAttempt` como contract-only/read-only. Valida estados y transiciones sobre el schema sin mutar attempts, sin escribir stores y sin crear eventos de lifecycle.

Resultado:

- estados contract-only: `draft`, `schema_validated`, `preflight_ready`, `blocked`, `cancelled`;
- estados futuros/no activos: `queued`, `running`, `succeeded`, `failed`, `partially_succeeded`, `retrying`, `expired`;
- terminales contract-only: `blocked`, `cancelled`;
- transiciones permitidas hasta `preflight_ready`, `blocked` y `cancelled`;
- transiciones runtime futuras bloqueadas;
- sin lifecycle writes;
- sin result store;
- sin runtime execution.

Proximo paso:

`PROMPT 3.5 — Auditoría de result store boundary`

## 107. PROMPT 3.5 - Auditoria de result store boundary

Estado:

`RESULT_STORE_BOUNDARY_AUDIT_COMPLETED`

Veredicto:

`RESULT_STORE_BOUNDARY_READY_FOR_CONTRACT_DESIGN`

Readiness:

`ready_for_result_store_contract`

Evidencia:

- auditoria: `docs/RESULT_STORE_BOUNDARY_AUDIT.md`;
- checkpoint E2E: `docs/RESULT_STORE_BOUNDARY_AUDIT_E2E_CHECKPOINT.md`;
- tests: `tests/test_result_store_boundary_audit.py`, `tests/test_result_store_boundary_audit_e2e_checkpoint.py`.

Decision:

Se audita la frontera del futuro `ExecutionResult` / result store. No se crea result store operativo, no se escribe ningun resultado y no se activa runtime.

Resultado:

- definicion de resultado y no-resultado;
- diferencia Attempt vs Result documentada;
- diferencia lifecycle event vs result documentada;
- diferencia dry_run output vs result documentada;
- campos candidatos propuestos;
- riesgos principales documentados;
- Market Catalog permanece `planned_not_active`;
- Business Composition Layer permanece futura/no operativa;
- sin store writes;
- sin lifecycle writes;
- sin runtime execution.

Proximo paso:

`PROMPT 3.6 — Contrato de result store operativo read-only`
