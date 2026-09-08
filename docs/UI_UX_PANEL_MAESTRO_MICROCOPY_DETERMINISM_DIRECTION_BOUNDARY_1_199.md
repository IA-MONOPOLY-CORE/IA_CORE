# UI/UX 1.199 - Frontera determinista y de Direccion

## Gate

`N4_MICROCOPY_DETERMINISM_DIRECTION_BOUNDARY_PASSED`

N4 asigna cada una de las 1143 unidades a un nivel de autoridad. La frontera
describe lo que podria hacerse despues; no autoriza cambios de wording ni
modifica el producto actual.

## Niveles

| Nivel | Unidades | Ocurrencias | Owner | Significado |
| --- | ---: | ---: | --- | --- |
| `LEVEL_A_FULLY_DETERMINISTIC` | 111 | 200 | Agente | Una unica salida segura se deriva del contrato existente o de mantener |
| `LEVEL_B_PREAUTHORIZED_PATTERN` | 372 | 504 | Direccion de patron | Una regla puede gobernar muchas unidades despues de una aprobacion unica |
| `LEVEL_C_DIRECTION_PACKAGE` | 222 | 228 | Direccion | Queda una eleccion humana o contextual genuina |
| `LEVEL_D_CONTRACT_CHANGE` | 438 | 692 | Owner contractual | Requiere versionar contrato/vocabulario antes de cualquier cambio |
| **Total** | **1143** | **1624** | — | — |

La frontera original de `DIRECTION_REQUIRED` queda contenida en:

- `LEVEL_A`: 170 ocurrencias derivadas por contrato existente;
- `LEVEL_B`: 33 ocurrencias derivadas por consistencia/precedente;
- `LEVEL_C`: 192 ocurrencias genuinamente humanas;
- `LEVEL_D`: no se mezcla con las 395; sus 692 ocurrencias requieren cambio
  contractual por una razon distinta y mas fuerte.

## LEVEL_A - totalmente determinista

Incluye `KEEP_NO_DECISION` y `DERIVABLE_WITH_EXISTING_CONTRACT`. El agente
puede comprobar preservacion, IDs, origen, pairing accesible y diff protegido.
No puede aprovechar este nivel para cambiar una palabra: la salida segura es
mantener el valor o respetar el contrato ya declarado.

## LEVEL_B - patron preautorizado

Incluye reglas editoriales/presentacionales, consistencia equivalente y la
frontera geometrica observada. Direccion aprueba una regla y una allowlist de
IDs una sola vez; luego el agente puede aplicar esa regla, generar snapshots,
validar i18n/HTML/ARIA y repetir browser checks.

LEVEL_B no permite mezclar una decision editorial con una decision de accion,
permiso, readiness o contrato. La geometria tampoco autoriza CSS por si sola.

## LEVEL_C - paquete de Direccion

Incluye 222 unidades/228 ocurrencias en el universo completo. Dentro de la
frontera original 1.198 son 186 unidades/192 ocurrencias. Son casos donde
persisten alternativas validas: nomenclatura, politica de casing/idioma,
interpretacion contextual de accion/permiso o eleccion entre variantes.

Direccion decide por paquete conceptual, no por registro individual.

## LEVEL_D - cambio contractual

Incluye 438 unidades/692 ocurrencias. Son vocabulario exacto, blockers,
fallbacks, estados y limites cuya edicion desincronizaria el contrato actual.
No deben presentarse como microcopy editorial ni entrar en una aprobacion de
patron. Primero requieren una version contractual o de vocabulario.

## Campos de frontera

Cada unidad conserva `DECISION_UNIT_ID`, nivel, resolucion N3, cantidad de
ocurrencias, evidencia, condicion de automatizacion y owner. Las pruebas
rechazan niveles desconocidos, perdida de unidades o una asignacion de
`LEVEL_D` a una regla editorial.

## Resultado N4

`N4_MICROCOPY_DETERMINISM_DIRECTION_BOUNDARY_PASSED`

N5 puede convertir los niveles B/C/D en paquetes humanos irreducibles sin
volver a abrir decisiones ya derivables.
