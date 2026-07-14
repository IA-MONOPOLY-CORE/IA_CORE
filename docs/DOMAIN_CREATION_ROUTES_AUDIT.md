# Auditoria de rutas de creacion de dominio

## 1. Proposito

Esta auditoria cierra PROMPT 0.4 antes de disenar el schema de dominio sandbox real. El objetivo es confirmar que ninguna ruta cree, registre, liste o exponga dominios por fuera de unicidad, equivalencias, estados internos, reglas PASSED, contrato derivado/operativo y preview previo a materializacion.

## 2. Estado inicial

- `git status --short`: sin salida.
- HEAD inicial: `395cef3`.
- Working tree inicial limpio: si.

## 3. Rutas auditadas

Se buscaron referencias a `create_domain`, `register_domain`, `add_domain`, `delete_domain`, `archive_domain`, `restore_domain`, `reset_domain`, `list_domains`, `domain_registry`, `domain_identity`, `domain_state`, `domain.json`, `domains/`, `profile_catalog.json` y `agent_presets.json`.

Archivos/carpetas revisadas:

- `core/domain_registry.py`
- `core/domain_identity.py`
- `core/domain_state.py`
- `core/domain_materialization_preview.py`
- `api.py`
- `ui/web/domains.js`
- `scripts/`
- `tests/`
- `domains/`
- `docs/`

## 4. Clasificacion de rutas

| Ruta | Clasificacion | Resultado |
| --- | --- | --- |
| `core/domain_registry.create_domain()` | `ruta_valida` para fixtures aislados y futura materializacion interna | Aplica catalogos, unicidad, equivalencias, snapshots legacy y escritura segura bajo `domains_dir`. No es endpoint publico de materializacion. |
| `core/domain_registry.list_domains()` | `ruta_valida` | Lista manifests y filtra por `domain_state`; legacy, archived, broken, preview, materialized y estados desconocidos no aparecen activos por defecto. |
| `core/domain_state.archive_domain()` | `ruta_valida` | Retira dominio del flujo activo con trazabilidad y `visible_en_hud=false`. |
| `core/domain_state.restore_domain()` | `ruta_valida` | Restaura a estado no activo; rechaza activacion directa. |
| `core/domain_state.reset_domain()` | `ruta_valida` | Vuelve a `empty` con trazabilidad; no activa dominios. |
| `core/domain_state.delete_domain_safely()` | `ruta_valida` | Requiere `confirm=True`, estado `archived`, trazabilidad y rechaza legacy. |
| `core/domain_materialization_preview.build_domain_materialization_preview()` | `ruta_valida` no operativa | Construye preview derivado; no escribe `domains/`, no registra dominio y no crea agentes/papers/presets. |
| `api.py /api/domains/list` | `ruta_valida` | Usa `list_domains()` y por defecto no expone dominios internos. |
| `api.py /api/domains/create` | `bypass_confirmado` corregido | Antes podia materializar carpetas desde UI/API. Quedo bloqueado para `C:\IA_CORE\domains`; solo se permite cuando tests redirigen `DOMAINS_DIR` a ruta temporal aislada. |
| `ui/web/domains.js` boton de creacion | `ruta_legacy` | Llama al endpoint viejo; al quedar bloqueado no puede crear dominios reales. Deuda UI: reemplazar por preview/materializacion cuando exista contrato de fase posterior. |
| `scripts/generate_domain_profile_catalog.py` | `ruta_valida` derivada | Rechaza salida dentro de `domains/`; no crea dominio real. |
| `scripts/generate_domain_agent_presets.py` | `ruta_valida` derivada | Rechaza salida dentro de `domains/`; no crea presets operativos. |
| `scripts/generate_professional_team_template.py` | `ruta_valida` derivada | Rechaza salida dentro de `domains/`; no crea equipos operativos. |
| `scripts/run_professional_domain_end_to_end.py` | `ruta_valida` derivada | Rechaza salida dentro de `domains/`; produce JSON no operativo. |
| Tests que escriben `domain.json` en `tmp_path` | `ruta_test_fixture` | Son fixtures aislados y no dejan residuos operativos. |
| Documentos que mencionan `domains/` o `domain.json` | `ruta_documental` | No ejecutan escritura. |
| `domains/loteria/` | `ruta_legacy` | Conservado como referencia historica, `status=legacy`, `legacy=true`, `visible_en_hud=false`. |
| `domains/demo_generico/` | `ruta_legacy` interna/demo | `es_demo=true`, `visible_en_hud=false`; no aparece activo. |

## 5. Ruta valida oficial futura

La ruta oficial futura sera:

1. Generar preview con `core/domain_materialization_preview.py`.
2. Validar `artifact_state`, gaps, riesgos y acciones requeridas.
3. Aprobar materializacion en una fase posterior.
4. Materializar con servicio backend interno que use `core/domain_registry.create_domain()` como primitiva controlada.
5. Persistir estado `materialized`, trazabilidad y manifest de materializacion.
6. Activar solo luego de PASSED explicito.

Hasta que exista ese servicio, ninguna ruta publica puede crear dominio real en `domains/`.

## 6. Rutas legacy

- `/api/domains/create` existe por historia y queda bloqueada en el root operativo.
- `ui/web/domains.js` conserva llamada al endpoint viejo; no puede crear porque el backend rechaza la ruta.
- `domains/loteria/` y `domains/demo_generico/` se conservan como legacy/demo internos, no como dominios nuevos activos.

## 7. Rutas de test

Los tests pueden usar `tmp_path` o `config.DOMAINS_DIR` redirigido para crear fixtures temporales. Esos fixtures no son dominio operativo real, no modifican `C:\IA_CORE\domains` y se eliminan al terminar pytest.

## 8. Bypasses detectados

Bypass confirmado: `/api/domains/create` podia crear carpetas y `domain.json` bajo el root operativo antes de pasar por preview/materializacion. Se corrigio bloqueandolo cuando `config.DOMAINS_DIR` apunta a `C:\IA_CORE\domains`.

## 9. Correcciones aplicadas

- `api.py`: bloqueo explicito de `/api/domains/create` contra el root operativo.
- `core/domain_registry.py`: `list_domains()` ahora usa `is_domain_visible_as_active()` para no exponer estados desconocidos o invalidos como activos.
- `tests/test_domain_creation_routes.py`: nueva cobertura de bypasses, estados, preview, fixtures y acciones seguras.
- `tests/test_domain_uniqueness.py`: endpoint publico real ahora espera bloqueo de creacion directa.

## 10. Deudas UI/backend

- Reemplazar el boton/flujo viejo de UI por preview de materializacion cuando exista endpoint formal.
- Crear en PROMPT 1.x el servicio de materializacion sandbox real con manifest, rollback y errores accionables.
- Mantener scripts generadores como salidas derivadas hasta que una fase posterior los conecte al materializador.

## 11. Criterio antes de PROMPT 1.0

Se puede entrar a schema de dominio sandbox cuando:

- no haya endpoints publicos que escriban dominios reales;
- los listados activos dependan de estados centrales;
- el preview siga siendo no operativo;
- los tests de bloqueo de bypasses pasen;
- las rutas legacy esten documentadas.

## 12. Confirmacion

La proxima fase puede disenar el schema sandbox sin rutas paralelas peligrosas. No se materializo ningun dominio, no se creo `profile_catalog`, no se creo `agent_presets`, no se crearon agentes, papers ni equipos.
