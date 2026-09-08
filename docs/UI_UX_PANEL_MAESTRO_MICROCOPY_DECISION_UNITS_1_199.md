# UI/UX 1.199 - Unidades de decision de microcopy

## Gate

`N2_MICROCOPY_DECISION_UNIT_NORMALIZATION_PASSED`

N2 transforma ocurrencias en unidades solo cuando una misma decision puede
gobernar honestamente a todos sus miembros. La implementacion determinista
esta en `tests/ui_ux_panel_maestro_microcopy_1_199_support.py` y consume el
corpus, clasificacion, mapa contractual y Decision Package de 1.198.

## Compresion

| Medida | Valor |
| --- | ---: |
| `TOTAL_MICROCOPY_ITEMS` | 1624 |
| `TOTAL_DECISION_UNITS` | 1143 |
| `TOTAL_OCCURRENCES` | 1624 |
| Ocurrencias por unidad, descriptivo | 1.42 |
| `SHARED_DECISION_UNITS` | 202 |
| Ocurrencias gobernadas por unidades compartibles | 683 |
| `DO_NOT_MERGE_UNITS` | 941 |
| Ocurrencias conservadas sin merge | 941 |

La compresion descriptiva es `1624 -> 1143`. No es una metrica de calidad:
indica solo que 202 decisiones potenciales pueden gobernar 683 ocurrencias sin
cruzar autoridades, contextos o contratos incompatibles.

## Tipos de agrupacion

| Tipo | Unidades | Ocurrencias | Politica |
| --- | ---: | ---: | --- |
| `EXACT_DUPLICATE_UNIT` | 189 | 657 | `SHARED_DECISION` |
| `SEMANTIC_EQUIVALENT_UNIT` | 13 | 26 | `SHARED_DECISION` |
| `CONTEXTUAL_VARIANT_UNIT` | 55 | 55 | `DO_NOT_MERGE` |
| `CONTRACT_BOUND_UNIT` | 603 | 603 | `DO_NOT_MERGE` |
| `EDITORIAL_PATTERN_UNIT` | 283 | 283 | `DO_NOT_MERGE` |
| `SINGLETON_DECISION_UNIT` | 0 | 0 | `DO_NOT_MERGE` |
| **Total** | **1143** | **1624** | — |

## Reglas de equivalencia

`EXACT_DUPLICATE_UNIT` exige texto igual ignorando case/espacios exteriores,
misma clasificacion, misma autoridad contractual y misma categoria de
Decision Package. La superficie puede variar cuando la autoridad permanece
igual; esto permite una regla comun sin afirmar que los bloques son iguales.

`SEMANTIC_EQUIVALENT_UNIT` permite solo diferencias de puntuacion, casing o
espaciado cuando el texto normalizado, clasificacion, autoridad y categoria
siguen siendo iguales.

`CONTEXTUAL_VARIANT_UNIT` conserva separada cada ocurrencia de un texto
repetido que aparece bajo otra autoridad, superficie o contexto. La unidad
sirve para rastrear la variante, pero su politica es `DO_NOT_MERGE`.

`CONTRACT_BOUND_UNIT` conserva como singleton cualquier estado, blocker,
fallback, readiness, warning, error, permiso, accion o copy accesible sin una
equivalencia objetiva segura.

`EDITORIAL_PATTERN_UNIT` conserva como singleton labels, navegacion,
placeholders y copy editorial. La similitud de tono o cercania visual no
autoriza compartir una decision.

`SINGLETON_DECISION_UNIT` queda reservado para registros que no entren en
ninguna categoria anterior; el corpus actual no produjo ninguno.

## Autoridad y trazabilidad

Cada unidad conserva:

- `DECISION_UNIT_ID` estable;
- cantidad de ocurrencias;
- `MICROCOPY_ID` miembros;
- textos actuales;
- archivos y superficies;
- contratos y clasificaciones;
- categoria y recomendacion N6;
- riesgos;
- politica de merge;
- razon de agrupacion.

Los 714 duplicados del inventario no se convierten automaticamente en 714
decisiones ni en una sola decision global. La normalizacion comparte solo 683
ocurrencias con 202 unidades y mantiene 941 unidades sin merge por falta de
una eleccion comun demostrable.

## Resultado N2

`N2_MICROCOPY_DECISION_UNIT_NORMALIZATION_PASSED`

La frontera N3 queda preparada sobre 1143 unidades. La compresion no elige
preferencias de producto ni cambia wording; solo reduce repeticion cuando la
misma decision puede aplicarse coherentemente.
