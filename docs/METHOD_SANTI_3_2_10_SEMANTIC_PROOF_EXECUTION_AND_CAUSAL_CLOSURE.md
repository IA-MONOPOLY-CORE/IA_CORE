# Método Santi 3.2.10

## Incremento

Este incremento sucede a `3.2.9` y formaliza la corrección de la causa raíz
de Macro-Mission 06.2.2: la metadata declarada no es ejecución probada.

Las siguientes distinciones son normativas:

- `PROOF_METADATA != PROOF_EXECUTION`.
- `DECLARED_PROOF != RECOMPUTED_PROOF`.
- `PASS_IS_DERIVED_NOT_CONSUMED`.
- `GREEN_TEST != PROVEN_PROPERTY`.
- `EXPECTED_REJECTION != CAUSALLY_CORRECT_REJECTION`.
- `DECLARED_COVERAGE != EXECUTED_COVERAGE`.
- `NODEID_REFERENCED != NODEID_EXECUTED`.
- `SCHEMA_SHA_PRESENT != SCHEMA_EXECUTED`.
- `VALIDATOR_NAME != VALIDATOR_EXECUTION`.
- `HASH_OR_LOGICAL_ID != AUTHORIZED_IMPLEMENTATION_BYTES`.
- `ATOMIC_PUBLICATION != AUTHORITATIVE_CLOSED` sin read-back exacto.

## Regla operacional

El resolver gobernado es el único camino para cargar schemas, validators,
profiles y contratos de canonicalización. Cada componente se recupera por
bytes exactos desde el Authorized Validation Input Set, se hashea nuevamente,
se compara contra Trust Root y recién después se ejecuta.

La prueba es válida sólo si mantiene simultáneamente fidelidad de input, path,
causalidad, ejecución y evidencia. Cualquier factor cero elimina autoridad.

## Límites

El Método Santi sigue siendo un contrato versionado de gobernanza, doctrina,
reglas de ejecución, validación y aprendizaje. Este incremento no crea runtime
autónomo, no inicia P3 y no implementa VERO ni FIRE.
