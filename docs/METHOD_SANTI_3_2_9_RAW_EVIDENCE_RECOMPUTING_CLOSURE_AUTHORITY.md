# Método Santi 3.2.9: autoridad de cierre por recomputación de evidencia cruda

## Estado

Actualización incremental previa al `FINAL_VALIDATION_BASIS` de Macro-Mission
06.2.2. No reescribe los métodos históricos ni altera V1, V2, V2.1, V2.2 o
V2.2.1.

## Contratos incorporados

- `EVIDENCE_EXISTENCE != EVIDENCE_SUFFICIENCY != EVIDENCE_SEMANTIC_FIT`.
- La validación independiente consume bytes crudos ligados por hash; no consume
  el `PASS`, la completitud o la procedencia declarados por el artefacto juzgado.
- La derivación pura es determinista, read-only y content-bound sobre bytes
  exactos. La persistencia real, el read-back, la integridad del package y la
  publicación atómica son precondiciones posteriores de activación.
- Un receipt externo sólo es independiente si recomputa la propiedad sobre los
  bytes exactos del artefacto y liga schema, validator, perfiles y hashes.
- El `ASSURANCE_TRUST_ROOT` es la combinación de una definición pre-basis y un
  binding post-basis. La definición no conoce anclas futuras.
- `derived_closure_candidate: CLOSED` no es todavía `CLOSURE_DECISION: CLOSED`.
  La autoridad sólo nace del evento externo de publicación atómica de un
  payload terminal prevalidado en la ruta canónica.
- Un artifact no puede probar que su propia publicación tuvo éxito. Staging es
  explícitamente no autoritativo.

## Techo de assurance

La observación local fresca prueba únicamente el estado del ref remoto que la
cadena gobernada observó durante la ejecución. `REMOTE_ENFORCEMENT` permanece
`NOT_PROVEN` y `OPERATOR_ACTION_REQUIRED` permanece `YES`.

## Criterio de auditoría

`AUDIT_UNTIL: NO_KNOWN_MATERIAL_BYPASS_REMAINS`. No se continúa con P3, VERO o
FIRE mientras el juez pueda alcanzar autoridad por cualquiera de los bypasses
documentados en A-01..A-07 y T-01..T-12.
