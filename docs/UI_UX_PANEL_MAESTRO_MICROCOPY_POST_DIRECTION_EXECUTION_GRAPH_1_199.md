# UI/UX 1.199 - Grafo de ejecucion post-Direccion

## Gate

`N6_POST_DIRECTION_EXECUTION_GRAPH_PASSED`

Este documento describe trabajo futuro. No implementa ninguna aprobacion,
wording, CSS, HTML, i18n, contrato ni cambio productivo.

## Conteos operativos

| Campo | Valor |
| --- | ---: |
| `CURRENT_AUTOMATABLE_STATION_COUNT` | 2 |
| `POST_DIRECTION_DETERMINISTIC_STATION_COUNT` | 8 |
| `PREAUTHORIZED_POST_DIRECTION_STATION_COUNT` | 3 |
| `SELF_BOOTSTRAPPED_POST_DIRECTION_STATION_COUNT` | 1 |
| `NEXT_HARD_FRONTIER_INDEX` | 9 |

## Grafo A - sin decisiones humanas

| Estacion | Alcance | Ocurrencias | Gate | Rollback |
| --- | --- | ---: | --- | --- |
| A1 | Preservar contrato existente y sus 170 registros derivables | 170 | `POST_DIRECTION_LEVEL_A_CONTRACT_PRESERVATION_PASSED` | Eliminar solo artefacto futuro |
| A2 | Ledger de 30 registros `KEEP_NO_DECISION` | 30 | `POST_DIRECTION_LEVEL_A_KEEP_LEDGER_PASSED` | Eliminar solo ledger futuro |

Estas dos estaciones pueden ejecutarse sin pedir una preferencia a Direccion.
Su trabajo es generar evidencia, snapshots, allowlists de preservacion y
regresion; no cambian wording activo.

## Grafo B - despues de aprobacion

| Indice | Estacion | Alcance | Ocurrencias | Estado |
| ---: | --- | --- | ---: | --- |
| 1 | Compilar respuestas | Decision Sheet, IDs y restricciones | 1424 | `SELF_BOOTSTRAPPED` |
| 2 | Regla editorial | `PKG_B_EDITORIAL_STYLE` | 295 | Determinista despues de patron |
| 3 | Consistencia | `PKG_B_CONSISTENCY_RULE` | 194 | Determinista despues de patron |
| 4 | Geometria | `PKG_B_GEOMETRY_REMEDIATION` | 15 | Determinista despues de owner |
| 5 | Variantes contextuales | `PKG_C_CONTEXTUAL_VARIANTS` | 36 | Determinista despues de decision |
| 6 | Contract-sensitive | `PKG_C_CONTRACT_SENSITIVE` | 139 | Determinista despues de decision |
| 7 | Action/permission | `PKG_C_ACTION_PERMISSION` | 15 | Determinista despues de decision |
| 8 | Roles ambiguos | `PKG_C_AMBIGUOUS_ROLE` | 38 | Determinista despues de decision |
| 9 | Vocabulario contractual | `PKG_D_CONTRACT_VOCABULARY` | 692 | `HARD_FRONTIER` |

Las estaciones 2-8 suman ocho estaciones deterministas post-aprobacion. La
estacion 9 no se cuenta como determinista: requiere version contractual,
Contract Owner y un bloque posterior independiente.

## Recomendacion de secuencia

Se recomienda la secuencia **A -> aprobacion de paquetes -> B1 -> B2-B8 ->
frontera B9**.

Motivos:

- A reduce ruido sin consumir decisiones humanas;
- B1 convierte la respuesta de Direccion en una allowlist comprobable;
- B2-B4 resuelven patrones repetibles antes de abrir decisiones semanticas;
- B5-B8 aplican decisiones conceptuales separadas sin mezclar permisos,
  editorial y contrato;
- B9 queda visible como frontera, sin forzar una falsa conclusion.

No se recomienda ejecutar un bloque grande unico porque mezclaria CSS/layout,
consistencia, action/permission y contrato, aumentando retrabajo y riesgo de
interpretacion.

## Archivos, tests, gates y commits

Cada estacion futura debe declarar sus rutas exactas, tests focales, gate,
rollback y prefijo de commit despues de inspeccionar el diff real. El graph
actual registra los artefactos y tests de referencia sin autorizarlos a
modificar producto. No se acepta glob, commit globo, `feat(ui)` sin producto,
payload v2, runtime, execution o endpoint.

## Resultado N6

`N6_POST_DIRECTION_EXECUTION_GRAPH_PASSED`

La proxima escala queda calculada sin asumir que Direccion ya eligio una
opcion.
