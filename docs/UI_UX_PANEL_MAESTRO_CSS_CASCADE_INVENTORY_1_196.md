# Inventario de cascada CSS contract-aware - UI/UX 1.196 N3

## Alcance y baseline

Inventario read-only sobre `357a08d` y la continuidad cerrada N1-N2 de
UI/UX 1.196. N3 no modifica `ui/web/styles.css`, HTML, JavaScript, i18n,
backend ni payload. El contrato `backend_internal_ui_payload.v1` y sus estados
se consideran superficies protegidas. La clasificación es conservadora: una regla se elimina
solo con evidencia de que es redundante y de que el resultado computado queda
preservado.

## Medición reproducible actual

La medición se obtiene leyendo `ui/web/styles.css` en el checkout actual:

| Medida | Valor | Interpretación |
| --- | ---: | --- |
| Líneas CSS | 1874 | superficie total de la cascada |
| Bloques delimitados por `{` | 260 | aproximación determinista de reglas/at-rules |
| Media queries | 10 | boundaries responsive existentes |
| Custom properties | 46 | tokens globales y de design system |
| Comentarios de estación | 22 | historial visual explícitamente marcado |

Los números son inventario, no objetivo de reducción. Menos líneas no es un
criterio suficiente para consolidar.

## Zonas inventariadas

### P0 - KEEP_CANONICAL / DO_NOT_TOUCH_CONTRACT_SURFACE

Se preservan la ruta Estado -> Contrato -> Límites -> Evidencia -> Próximo
paso, sus anchors `data-p0-zone`, el modo read-only y los marcadores
`data-no-runtime` y `data-no-execution`. La presentación puede recibir ritmo y
wrapping en N6, pero no se reordena semánticamente ni se oculta evidencia.

### P1 - KEEP_CANONICAL / OVERRIDE_REQUIRED

La ruta contractual existente usa `.p1-contractual-route`,
`.p1-contractual-stage` y sus marcadores. Las reglas de 1.183 y los overrides
acotados posteriores forman una cadena histórica. N6 puede ajustar jerarquía
visual solo con selectores scoped a esta superficie.

### Matriz P3 - MERGEABLE_DUPLICATE con cautela

La familia `.closure-matrix-*` tiene reglas base, dos boundaries responsive y
overrides documentados de 1.186 y 1.194. Las reglas de wrapping y densidad de
1.194 son candidatas a consolidación visual acotada; las reglas que preservan
20 filas y 26 badges quedan protegidas.

### Widgets - LEGACY_PARALLEL_RULE / OVERRIDE_REQUIRED

`.data-widget`, `.data-widget-title`, `.data-widget-value`, `.data-widget-meta`,
`.data-widget-detail` y `.data-widget-fallback` aparecen en capas históricas y
en la capa 1.194. N7 puede alinear spacing, wrapping y tratamiento visual de
estados existentes; no toca el renderer, payload ni autoridad contract-aware.

### Request Draft Panel - DO_NOT_TOUCH_CONTRACT_SURFACE

`.request-draft-panel` y sus reglas collapsed/1.189/1.194 son evidencia
visible, secundaria, read-only y blocked. No se elimina, no se convierte en
CTA, no se cambia su HTML ni se introduce submit.

### Estados y affordances - KEEP_CANONICAL / UNKNOWN_DO_NOT_DELETE

`.visual-state`, `.contract-chip`, `.admin-status`,
`[data-contract-blocked="true"]`, `disabled` y `[aria-disabled="true"]`
representan estados ya existentes. Se permiten ajustes de legibilidad; no se
crean taxonomías ni se unifican colores si se pierde severidad.

## Reglas por clasificación

- `KEEP_CANONICAL`: conservar por ser la fuente visual vigente.
- `MERGEABLE_DUPLICATE`: solo fusionar si el selector y el resultado están
  demostrablemente duplicados.
- `OVERRIDE_REQUIRED`: conservar la regla histórica y añadir un override
  scoped únicamente cuando el contrato visual lo exige.
- `LEGACY_PARALLEL_RULE`: no borrar durante esta misión sin prueba de muerte.
- `UNUSED_PROVEN`: no hay eliminación demostrada en N3.
- `DO_NOT_TOUCH_CONTRACT_SURFACE`: P0, P1, widgets contract-aware, Matriz,
  Request Draft Panel y affordances bloqueadas.
- `RESPONSIVE_SPECIFIC`: media queries y wrapping deben validarse en browser.
- `UNKNOWN_DO_NOT_DELETE`: cualquier regla cuya fuente o resultado no sea
  completamente trazable queda fuera de N4.

## Candidatos seguros para N4

1. Consolidar declaraciones presentacionales repetidas dentro de la familia
   `.closure-matrix-*` solo si el snapshot computado se preserva.
2. Consolidar wrapping/line-height repetidos en widgets y estados existentes
   con selectores `body` scoped, sin cambiar atributos ni comportamiento.
3. Mantener separados los overrides históricos cuando su especificidad evita
   una regresión en mobile.

No se propone eliminar reglas muertas en esta estación. N4 debe detenerse si
la consolidación requiere HTML, JS, i18n, backend, payload, cambio semántico,
nueva acción, nueva capacidad o modificación de autoridad. No se crean
acciones, capacidades, permisos, estados ni operatividad nueva.
No se toca ninguna superficie contractual protegida en N3.
Microcopy contractual transversal queda fuera de N3 y N4.

## Gate

`N3_VISUAL_CASCADE_INVENTORY_PASSED`

N3 queda cerrado como inventario reproducible, test-only y sin cambio
productivo. N4 queda habilitada únicamente para los candidatos seguros
anteriores.
