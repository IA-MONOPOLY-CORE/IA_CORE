# Promotion Direction Package - Evidence Review after UI/UX 1.200

## Purpose

Este paquete compacto hace visible a Dirección que la evaluación versionada
detectó siete items `PROMOTION_READY` bajo `PROMOTION_POLICY_V1` y un item
`DIRECTION_APPROVAL_REQUIRED`. No ejecuta promoción y no cambia lifecycle.

La primera promoción global permanece como frontera institucional. La
autoridad de este documento es informativa para revisión humana; el assessment
declara `automatic_promotion=false` y `status_mutation=PROHIBITED`.

## Items para revisión explícita

`PROMOTION_READY` bajo la evidencia derivada de UI/UX 1.200:

- `compress_occurrences_into_decisions`
- `evidence_before_closure`
- `focal_group_canonical_deep_test_policy`
- `preserve_contract_until_explicit_change`
- `real_diff_over_planned_commit_name`
- `station_local_commits`
- `true_hard_frontier`

`DIRECTION_APPROVAL_REQUIRED`:

- `conditioned_autonomy`: la política identifica autonomía institucional y
  exige revisión de Dirección aunque la evidencia operacional ya sea múltiple.

Los otros ocho items VALIDATED permanecen `INSUFFICIENT_EVIDENCE` porque la
misión 1.200 no produjo una referencia independiente para ellos. En particular,
la ausencia de rollback no se convierte en evidencia positiva de
`local_rollback`.

## Decisión requerida

Dirección debe decidir explícitamente si alguno de los siete items debe cruzar
la frontera de promoción. Hasta esa decisión:

- `PROMOTED = 0`;
- los JSON canónicos de knowledge no se modifican;
- no se autoriza uso runtime, ejecución ni payload;
- el overlay de evidencia sigue siendo `DEVELOPMENT_ORIGIN`.

Fuente: `knowledge/global_operational/assessments/promotion_assessment_post_ui_ux_1_200.json`.
