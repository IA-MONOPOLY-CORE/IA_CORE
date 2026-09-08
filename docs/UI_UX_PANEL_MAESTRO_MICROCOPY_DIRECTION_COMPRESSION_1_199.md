# UI/UX 1.199 - Compresion de decisiones `DIRECTION_REQUIRED`

## Gate

`N3_DIRECTION_REQUIRED_COMPRESSION_PASSED`

N3 evalua primero las 279 unidades afectadas por los 395 registros que N6
habia marcado como `DIRECTION_REQUIRED`. No trata cada ocurrencia como una
pregunta independiente y no elige preferencias de producto por Direccion.

## Resultado de compresion

| Medida | Unidades | Ocurrencias |
| --- | ---: | ---: |
| `ORIGINAL_DIRECTION_REQUIRED` | 279 | 395 |
| `DERIVABLE_WITH_EXISTING_CONTRACT` | 81 | 170 |
| `DERIVABLE_WITH_CONSISTENCY_RULE` | 12 | 33 |
| `DIRECTION_REQUIRED_TRUE` | 186 | 192 |

La ecuacion de la frontera humana es:

`395 = 170 + 33 + 192`

Por unidad:

`279 = 81 + 12 + 186`

Los 192 registros restantes no se reducen mas sin seleccionar una preferencia
real de producto, una lectura semantica entre alternativas validas o una
autoridad contractual. Esos son los casos que deben llegar a Direccion.

## Reconciliacion de los 96 ambiguos

| Resolucion | Unidades | Ocurrencias | Lectura |
| --- | ---: | ---: | --- |
| Contrato existente | 25 | 25 | Anti-accion o `allowed_actions` ya declarado como dato, no CTA |
| Consistencia/precedente | 12 | 33 | Repeticion equivalente con una misma autoridad |
| Direccion genuina | 38 | 38 | Persisten dos o mas interpretaciones honestas |
| **Total** | **75** | **96** | — |

Las 21 unidades restantes de los 96 registros forman parte de unidades
compartidas ya contabilizadas por la regla de equivalencia. No se pierde
ningun `MICROCOPY_ID`.

## Regla de resolucion para todas las unidades

| Resolucion | Unidades | Ocurrencias | Significado |
| --- | ---: | ---: | --- |
| `DERIVABLE_WITH_EXISTING_CONTRACT` | 81 | 170 | El contrato existente resuelve la lectura sin preferencia nueva |
| `DERIVABLE_WITH_EXISTING_STYLE_RULE` | 288 | 295 | Regla editorial/presentacional existente, sin alterar semantica |
| `DERIVABLE_WITH_CONSISTENCY_RULE` | 80 | 194 | Precedente equivalente; conservar contexto y valor actual |
| `DERIVABLE_WITH_GEOMETRY_RULE` | 4 | 15 | Riesgo observado por browser con frontera geometrica acotada |
| `DIRECTION_REQUIRED_TRUE` | 222 | 228 | Eleccion humana genuina o variante contextual incompatible |
| `CONTRACT_CHANGE_REQUIRED` | 438 | 692 | No se puede cambiar bajo el contrato actual |
| `KEEP_NO_DECISION` | 30 | 30 | No existe evidencia para modificar |
| **Total** | **1143** | **1624** | — |

La tabla completa incluye tambien unidades que N6 no habia contado dentro de
los 395, por eso `DIRECTION_REQUIRED_TRUE` global es 228; la frontera humana
original de 1.198 queda congelada en 192 registros genuinos.

## Tipos de resolucion

`DERIVABLE_WITH_EXISTING_CONTRACT` cubre readiness, `no_payload`,
`not_available` y copy anti-accion cuando el contrato vigente ya expresa que
la UI es read-only, deny-by-default y sin runtime/execution. No habilita nada.

`DERIVABLE_WITH_EXISTING_STYLE_RULE` cubre exclusivamente labels editoriales,
navegacion, formularios y placeholders donde preservar significado, pairing
accesible y localizacion es una regla suficiente.

`DERIVABLE_WITH_CONSISTENCY_RULE` usa precedentes exactos o semanticamente
equivalentes. La regla es conservar el valor actual y no fusionar contextos.

`DERIVABLE_WITH_GEOMETRY_RULE` no autoriza CSS: solo deja una frontera de
revisión geometrica acotada para un bloque futuro.

`DIRECTION_REQUIRED_TRUE` no es una solicitud para 228 preguntas. En la
frontera original son 186 unidades/192 ocurrencias; los casos extra del total
global son variantes contextuales que tampoco deben mezclarse.

`CONTRACT_CHANGE_REQUIRED` permanece fuera de cualquier paquete editorial.
Cambiar una de esas 692 ocurrencias requiere una version nueva del vocabulario
o contrato correspondiente.

## Resultado N3

`N3_DIRECTION_REQUIRED_COMPRESSION_PASSED`

N4 puede construir la frontera formal entre lo que el agente puede derivar,
lo que requiere una aprobacion de patron y lo que exige una decision humana.
