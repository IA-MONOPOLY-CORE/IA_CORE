# Checkpoint extremo de confiabilidad y usabilidad sandbox

## 1. Resumen ejecutivo

IA_CORE soporta hoy la cadena sandbox completa:

```txt
domain sandbox -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agent
```

Funciona con evidencia en el flujo minimo controlado y en un stress maximo controlado sobre datos reales del repo.

Validado:

- materializacion en sandbox temporal;
- `artifact_manifest`;
- lineage;
- rollback selectivo;
- rollback total;
- regeneracion;
- frontera runtime;
- aislamiento de `domains/`, `agents/`, catalogos y papers globales.

Parcial:

- el repositorio contiene 200 combinaciones area/nicho activas; la suite ejecutable materializa 12 dominios completos para mantener el checkpoint razonable.
- falta un modo dedicado de benchmark largo para correr los 200 dominios completos fuera de la suite rapida.

Bloqueado por diseno:

- duplicados/equivalentes de dominio;
- duplicados de artefactos sin `regenerate=True`;
- rollback de artefactos con dependientes;
- estado `active`;
- escritura en runtime `agents/`;
- escritura en `domains/` operativo.

No debe usarse todavia:

- runtime de agentes;
- memoria operativa;
- herramientas;
- equipos;
- UI o integraciones.

## 2. Prueba minima controlada

Flujo ejecutado por `tests/test_sandbox_chain_checkpoint.py`:

```txt
preview
  -> materialize sandbox domain
  -> materialize profile_catalog
  -> materialize agent_presets
  -> materialize paper_seed
  -> materialize sandbox_agent
  -> validate artifact_manifest
  -> validate lineage
  -> rollback sandbox_agent
  -> rollback paper_seed
  -> rollback agent_presets
  -> rollback profile_catalog
  -> rollback domain
```

Resultado:

- estado: `PASSED`;
- evidencia: 1 test end-to-end completo;
- rollback selectivo: `PASSED`;
- rollback total: `PASSED`;
- no quedan archivos huerfanos;
- hashes de `domains/`, `agents/`, `catalogs/` y papers globales sin cambios.

Nivel de confiabilidad: alto para el flujo minimo.

## 3. Prueba maxima de maximos actual

Biblioteca detectada:

| Recurso | Cantidad |
|---|---:|
| Areas activas | 30 |
| Nichos activos | 200 |
| Combinaciones area/nicho reales | 200 |
| Perfiles profesionales globales | 106 |
| Roles activos | 20 |
| Especializaciones activas | 80 |
| Model policies | 15 |

Stress ejecutado por `tests/test_sandbox_chain_maximum_checkpoint.py`:

| Medida | Resultado |
|---|---:|
| Dominios intentados | 12 |
| Dominios materializados | 12 |
| Dominios duplicados/equivalentes bloqueados | 12 |
| Profile catalogs generados | 12 |
| Perfiles generados | 295 |
| Presets generados | 295 |
| Paper seeds generados | 295 |
| Agentes sandbox generados | 295 |
| Regeneraciones ejecutadas | 4 |
| Rollbacks totales | 12 |

El test usa datos reales y generadores reales, pero limita dominios materializados a 12 para evitar que la suite normal ejecute los 200 dominios completos. Esa limitacion queda clasificada como `PARTIAL`, no como exito absoluto.

## 4. Mapa de confiabilidad

| Componente | Estado | Evidencia | Riesgo | Recomendacion |
|---|---|---|---|---|
| Dominio sandbox | PASSED | materializacion y rollback total | bajo | seguir |
| Artifact manifest | PASSED | validacion tras cada capa | bajo | seguir |
| Profile catalog | PASSED | minimo + stress | medio | mantener rollback selectivo cubierto |
| Agent presets | PASSED | minimo + stress | medio | reforzar tests de multiples dependientes en fases futuras |
| Paper seed | PASSED | minimo + stress | medio | no confundir con paper operativo |
| Agent schema | PASSED | contrato validado | bajo | seguir |
| Agent lineage | PASSED | origen e historia validados | bajo | seguir |
| Agent materialization | PASSED | 295 agentes sandbox en stress | medio | mantener runtime deshabilitado |
| Rollback selectivo | PASSED | agente, paper_seed, presets, profile_catalog | medio | agregar benchmark largo |
| Rollback total | PASSED | 12 dominios revertidos | bajo | seguir |
| Regeneration | PASSED | dominio/artifactos/agente | medio | ampliar a corrida larga |
| Runtime boundary | PASSED | `runtime_enabled=false`, hash `agents/` intacto | bajo | no activar sin prompt |
| Legacy isolation | PASSED | hash `domains/`, `agents/`, papers globales intacto | bajo | seguir |
| Controlled usability | PASSED | minimo completo | bajo | listo |
| Maximum usability | PARTIAL | stress acotado 12/200 dominios | medio | crear benchmark largo |
| Library scale | PARTIAL | 200 pares detectados, 12 materializados en suite | medio | subprompt de escala/observabilidad |

## 5. Mapa de usabilidad actual

Usable ahora en sandbox:

- dominio sandbox;
- `profile_catalog`;
- `agent_presets`;
- `paper_seed`;
- agente sandbox materializado;
- lineage;
- rollback selectivo;
- rollback total;
- regeneracion controlada.

Usable con limites:

- stress multi-dominio;
- maximo de biblioteca completa;
- metricas de escala.

No usable todavia:

- agentes como trabajadores operativos;
- memoria persistente;
- herramientas;
- equipos;
- activacion PASSED de agentes.

Futuro por diseno:

- runtime;
- providers reales;
- UI;
- integraciones externas.

Legacy/no tocar:

- `domains/` operativo;
- `agents/` runtime;
- papers globales existentes;
- Loteria historica.

## 6. Riesgos detectados

Riesgos tecnicos reales:

- el maximo completo de 200 dominios no debe correr dentro de la suite normal sin presupuesto de tiempo;
- rollback selectivo exige orden correcto por dependencias;
- multiples agentes por dominio requieren rollback cuidadoso de carpeta compartida.

Riesgos de documentacion:

- diferenciar `paper_seed` de paper operativo;
- diferenciar agente sandbox de runtime agent.

Riesgos de arquitectura futura:

- memoria debe ser artefacto separado si se vuelve persistente;
- herramientas deben ser artefactos/policies antes de runtime;
- equipos requieren dependencias sobre varios agentes.

Riesgos legacy:

- no usar writers legacy para sandbox;
- no registrar sandbox en `agents/` runtime.

Riesgos de escala:

- falta reporte automatico persistente de metricas;
- falta modo benchmark largo para 200 dominios.

## 7. Clasificacion interna

| Item | Estado |
|---|---|
| Dominio sandbox | PASSED |
| Artifact manifest | PASSED |
| Profile catalog | PASSED |
| Agent presets | PASSED |
| Paper seed | PASSED |
| Agent schema | PASSED |
| Agent lineage | PASSED |
| Agent materialization | PASSED |
| Rollback selectivo | PASSED |
| Rollback total | PASSED |
| Regeneration | PASSED |
| Runtime boundary | PASSED |
| Legacy isolation | PASSED |
| Controlled usability | PASSED |
| Maximum usability | PARTIAL |
| Library scale | PARTIAL |
| Runtime real | FUTURE |
| Memoria operativa | FUTURE |
| Herramientas | FUTURE |
| Equipos | FUTURE |
| Legacy runtime | LEGACY |

## 8. Respuesta final obligatoria

Respuesta:

```txt
Soporta parcialmente, con refuerzos necesarios.
```

Justificacion:

IA_CORE soporta hoy toda la cadena sandbox construida, con rollback, regeneracion, lineage, aislamiento legacy y frontera runtime. Tambien detecta toda la biblioteca profesional real: 30 areas, 200 nichos, 106 perfiles, 20 roles y 80 especializaciones.

El maximo completo de 200 dominios no queda ejecutado dentro de la suite normal; el checkpoint materializa 12 dominios reales, 295 perfiles, 295 presets, 295 paper_seed y 295 agentes sandbox. Por eso el resultado maximo actual es `PARTIAL`, no un `PASSED` absoluto.

Refuerzo recomendado antes de avanzar a runtime/memoria:

```txt
Subprompt de benchmark largo y metricas persistentes de escala sandbox 200/200.
```
