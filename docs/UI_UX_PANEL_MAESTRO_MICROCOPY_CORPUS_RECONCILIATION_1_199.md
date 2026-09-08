# UI/UX 1.199 - Reconciliacion de integridad del corpus de microcopy

## Gate

`N1_MICROCOPY_CORPUS_RECONCILIATION_PASSED`

Este artefacto reconstruye la clasificacion desde
`tests/ui_ux_panel_maestro_microcopy_1_198_support.py`. No usa el resumen
narrativo como fuente primaria y no modifica ninguna superficie productiva.

## Conciliacion obligatoria

| Capa | Registros | Evidencia |
| --- | ---: | --- |
| `TOTAL_CORPUS` | 1624 | `corpus_items()` |
| `TOTAL_CLASSIFIED` | 1624 | `semantic_classifications()` |
| `TOTAL_DECISION_PACKAGE` | 1624 | `decision_package_rows()` |
| `TOTAL_RECOMMENDATIONS` | 1624 | una recomendacion por fila del Decision Package |

Resultado demostrable:

`1624 = 1624 = 1624 = 1624`

Los cuatro conjuntos de `MICROCOPY_ID` son iguales. No hay registros sin
clasificacion, sin Decision Package ni sin recomendacion.

## Tabla completa de reconciliacion

| Categoria N3 | Registros |
| --- | ---: |
| `EDITORIAL_SAFE` | 408 |
| `CONTRACTUAL_EXACT` | 556 |
| `CONTRACTUAL_EXPLANATORY` | 93 |
| `STATE_LABEL` | 4 |
| `READINESS_LABEL` | 58 |
| `PERMISSION_SENSITIVE` | 0 |
| `ACTION_SENSITIVE` | 15 |
| `BLOCKER` | 138 |
| `WARNING` | 27 |
| `ERROR` | 19 |
| `FALLBACK` | 10 |
| `NO_PAYLOAD` | 31 |
| `NOT_AVAILABLE` | 52 |
| `NAVIGATION` | 14 |
| `FORM_LABEL` | 42 |
| `PLACEHOLDER` | 20 |
| `ACCESSIBILITY_COPY` | 41 |
| `LEGACY_ACTIVE` | 0 |
| `LEGACY_INACTIVE` | 0 |
| `AMBIGUOUS_REQUIRES_DIRECTION` | 96 |
| `UNKNOWN_REQUIRES_DIRECTION` | 0 |
| **Total** | **1624** |

## Explicacion exacta de los 80

El reporte resumido de 1.198 listaba 1544 registros porque presentaba las
categorias de mayor relevancia contractual, pero no imprimia cuatro categorias
validas de la clasificacion completa:

| Categoria omitida del resumen | Registros | Evidencia en el helper |
| --- | ---: | --- |
| `NAVIGATION` | 14 | `semantic_classifications()` |
| `FORM_LABEL` | 42 | `semantic_classifications()` |
| `PLACEHOLDER` | 20 | `semantic_classifications()` |
| `STATE_LABEL` | 4 | `semantic_classifications()` |
| **Total omitido narrativamente** | **80** | `14 + 42 + 20 + 4` |

Los 80 no constituyen un defecto de clasificacion. Tampoco son registros
duplicados creados para cerrar la suma. Son registros existentes con un
`MICROCOPY_ID` unico dentro del corpus, una clasificacion valida y una fila
correspondiente en el Decision Package.

`STATE_LABEL` aparece en la clasificacion completa con cuatro registros. El
resumen de 1.198 presento otros labels de estado derivados, pero no mostro
esta categoria separada. `NAVIGATION`, `FORM_LABEL` y `PLACEHOLDER` quedaron
fuera de la tabla narrativa aunque estaban definidas en `CLASSIFICATIONS`.

## Presencia en capas posteriores

Cada registro de las cuatro categorias omitidas tiene:

- `MICROCOPY_ID` en el corpus original;
- clasificacion N3 valida;
- binding y superficie N4;
- fila N6 con categoria de decision, riesgo y recomendacion;
- ninguna ausencia en las capas posteriores.

Los 80 no se agregan, eliminan, renombran ni reclasifican en 1.199. La
correccion es documental y de enforcement: el reporte futuro debe imprimir la
tabla completa, no solo el subconjunto contractual destacado.

## Duplicados y digest

Los `714 DUPLICATE_ITEMS` son una señal secundaria de repeticion textual y no
una categoria primaria. Se dividen en `145 DUPLICATE_EQUIVALENT` y `569
DUPLICATE_CONTEXTUAL`; ninguno de los 80 se pierde por esa etiqueta.

El digest permanece valido y sin cambios:

`4e5e84fbfa63aeb257813536febf91b2fc73b99e0384340b4194609ba48201ff`

La fuente productiva sigue siendo read-only. No se cambio HTML, CSS, JS, i18n,
backend, payload, runtime, execution, endpoints, integrations ni wording.

## Resultado N1

`N1_MICROCOPY_CORPUS_RECONCILIATION_PASSED`

N2 queda habilitado. La siguiente estacion puede construir unidades de
decision sobre los 1624 registros completos, sin reparar producto ni inventar
categorias.
