# Benchmark largo sandbox 200/200

## 1. Resumen ejecutivo

IA_CORE soporta la tasa full actual de la biblioteca profesional para la cadena sandbox completa:

```txt
domain sandbox -> profile_catalog -> agent_presets -> paper_seed -> sandbox_agent
```

El benchmark intento 200/200 combinaciones area/nicho detectadas y materializo 200/200 dominios sandbox en raiz temporal, sin activar runtime y sin modificar `domains/`, `agents/`, catalogos globales ni papers globales.

Veredicto: `PASSED_FULL_200`.

## 2. Cobertura

| Metrica | Valor |
|---|---:|
| Areas detectadas | 30 |
| Nichos detectados | 200 |
| Combinaciones area/nicho detectadas | 200 |
| Dominios intentados | 200 |
| Dominios completados | 200 |
| Dominios fallidos | 0 |

## 3. Produccion de artefactos

| Artefacto | Valor |
|---|---:|
| Profile catalogs generados | 200 |
| Perfiles generados | 3175 |
| Agent presets generados | 3175 |
| Paper_seed generados | 3175 |
| Sandbox agents generados | 3175 |

## 4. Confiabilidad

| Control | Resultado |
|---|---:|
| Artifact manifest failures | 0 |
| Lineage failures | 0 |
| Runtime boundary failures | 0 |
| Legacy isolation failures | 0 |
| Rollback selectivo | 65 / 65 |
| Rollback total | 200 / 200 |
| Regeneracion | 4 / 4 |
| Sandbox temporal limpio | true |

La regeneracion fue representativa, no full, por criterio de tiempo: `profile_catalog`, `agent_presets`, `paper_seed` y un `sandbox_agent` del primer dominio fueron regenerados con versionado/historial.

## 5. Performance basica

| Metrica | Valor |
|---|---:|
| Duracion total | 648.316 s |
| Promedio por dominio | 3.242 s |

Cuello de botella observado: escritura/validacion masiva de artefactos por dominio. No se optimizo el flujo durante este prompt; el objetivo fue medir la resistencia real.

## 6. Riesgos

- riesgo de escala: bajo para 200/200 actual; queda observar crecimiento futuro de catalogos.
- riesgo de arquitectura: bajo en la cadena actual; no hubo roturas de manifiesto, lineage, rollback ni regeneracion.
- riesgo de aislamiento: bajo; no se detectaron cambios en `domains/`, `agents/`, catalogos ni papers globales.
- riesgo de runtime: bajo en sandbox; todos los agentes quedaron `materialized` y `runtime_enabled=false`.
- riesgo de documentacion: bajo; metricas persistentes en `docs/benchmarks/sandbox_full_200_benchmark.json`.
- riesgo futuro: memoria, herramientas, equipos, providers vivos, UI e integraciones siguen fuera de alcance.

## 7. Veredicto

`PASSED_FULL_200`

## 8. Recomendacion

Listo para PROMPT 2.5.
