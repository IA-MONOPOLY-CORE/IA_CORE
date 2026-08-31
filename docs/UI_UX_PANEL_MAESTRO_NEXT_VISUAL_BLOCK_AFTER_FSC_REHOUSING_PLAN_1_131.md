# UI/UX Panel Maestro Next Visual Block After FSC Rehousing Plan 1.131

## Commit base

- Base esperada: `fd15a84`.
- Restore point remoto vigente: `570b18f`.
- Commits locales previos:
  - `469d963`.
  - `a47a4f8`.
  - `fd15a84`.

## Objetivo

1.131 planifica el siguiente bloque visual post rehousing FSC. No implementa UI, no modifica JavaScript y no activa capacidades. El objetivo es elegir el proximo bloque visual mas seguro despues de `Master Shell + Overview Layer` y `Final Screen Contracts Visual Rehousing`, usando la densidad visual como deuda menor no bloqueante.

## Estado recibido

- Decision vigente 1.130: `FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_CHECKPOINT_PASSED_WITH_DENSITY_DEBT_READY_FOR_NEXT_BLOCK_PLANNING`.
- Revision visual humana: `FINAL_SCREEN_CONTRACTS_VISUAL_REHOUSING_HUMAN_VISUAL_REVIEW_APPROVED`.
- Restore point remoto `570b18f`.
- Estado local esperado: local ahead por 3 commits.
- `Master Shell + Overview Layer` publicado.
- `Final Screen Contracts Visual Rehousing` cerrado.
- densidad visual como deuda menor no bloqueante.

`Master Shell + Overview Layer` esta implementado, aprobado, checkpoint cerrado y publicado en GitHub. `Final Screen Contracts Visual Rehousing` esta planificado, implementado, aprobado visualmente y checkpoint cerrado. No hay push pendiente obligatorio inmediato, pero la publicacion debe reevaluarse antes de una futura implementacion de UI activa.

## Candidatos evaluados

- `Design System / Density Refinement Planning`.
- `Evidence & Details Screen Planning`.
- `Configuration Read-only Screen Planning`.
- `Domains Context Screen Planning`.
- `Roadmap / Future Work Screen Planning`.
- `Master Shell + FSC Micro-polish Planning`.

## Evaluacion comparativa

| Candidato | valor visual inmediato | riesgo contractual | riesgo de reactivar capacidades | impacto sobre deuda de densidad | archivos probables | necesidad de JS | relacion con elementos inferiores | relacion con `CFG`, `+`, `DOMAIN` | relacion con evidencia/payload | dependencia con bloques cerrados | conveniencia antes/despues de publicar restore point | revision visual humana |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Design System / Density Refinement Planning` | Alto: fija reglas visuales antes de tocar otra superficie. | Bajo: planifica tokens y densidad sin cambiar contratos. | Bajo si queda documental y test-only. | Alto: ataca la deuda menor detectada en 1.130. | doc nuevo, test nuevo, `README.md`, `ui/web/README.md`; UI solo lectura. | No. | No absorbe elementos inferiores todavia. | Solo documenta reglas futuras para `CFG`, `+`, `DOMAIN`. | Solo define patrones de evidence/documentation sin payload crudo. | Usa 1.120/1.121/1.122 y checkpoints 1.125/1.130. | Conviene antes de publicar otro restore point; publicar podria reevaluarse despues del plan y antes de UI activa. | Si luego se implementa, si; para esta planificacion no requiere visual nueva. |
| `Evidence & Details Screen Planning` | Medio/alto: ordenaria lectura de detalles. | Medio: puede rozar evidencia sensible. | Medio: riesgo de endpoint/fetch o payload crudo si se redacta mal. | Medio: puede reducir detalle denso, pero no estabiliza reglas globales. | doc/test/readmes; futuro riesgo en `index.html`. | No para plan, posible no recomendado despues. | No toca inferiores directamente. | Indirecta. | Alta relacion con evidencia/payload. | Requiere reglas de tokens/read-only mas maduras. | Mejor despues de Design System y antes de implementacion con restore point evaluado. | Si, por riesgo de parecer inspector operativo. |
| `Configuration Read-only Screen Planning` | Medio: ordenaria `CFG`. | Medio/alto: `CFG` es affordance bloqueada. | Medio/alto: puede parecer configuracion editable. | Bajo/medio: ayuda a una zona, no al core completo. | doc/test/readmes; UI solo lectura en plan. | No para plan, JS prohibido en fase inicial. | Alta relacion con lower console. | Toca `CFG`; `+` y `DOMAIN` quedan cerca semanticamente. | Baja. | Debe esperar reglas visuales de bloqueado/read-only. | Mejor despues de estabilizar lenguaje visual y posiblemente despues de restore point. | Si, por riesgo de mutacion aparente. |
| `Domains Context Screen Planning` | Medio: resolveria deuda `DOMAIN/+`. | Alto: dominio y creacion son semanticas sensibles. | Alto: puede confundirse con activar dominio o crear agente. | Medio: resuelve una deuda puntual. | doc/test/readmes; futuro roce con `domains.js` solo lectura. | No para plan; JS no recomendado. | Alta relacion con elementos inferiores. | Toca directamente `DOMAIN` y `+`. | Baja/media. | Conviene despues de Design System y Configuration read-only. | Mejor despues de plan de tokens y restore point previo a UI activa. | Si, obligatoria. |
| `Roadmap / Future Work Screen Planning` | Medio: separa futuro/pendiente de activo. | Bajo/medio: riesgo de presentar futuro como disponible. | Bajo/medio: depende de copy y estados. | Bajo: no resuelve densidad del core visual actual. | doc/test/readmes. | No. | Puede absorber deuda futura de inferiores sin tocarlos. | Puede mencionar `CFG`, `+`, `DOMAIN` como future-only. | Baja. | Puede esperar porque no desbloquea el problema visual inmediato. | Puede hacerse despues, sin urgencia de restore point. | Probable si se implementa visualmente. |
| `Master Shell + FSC Micro-polish Planning` | Medio/alto: mejora lo ya visible. | Medio: puede reabrir superficies ya cerradas. | Bajo/medio si no toca acciones. | Medio: reduciria densidad local, pero sin reglas generales. | doc/test/readmes; futura UI en `index.html`. | No para plan. | No toca inferiores directamente. | Solo periferico. | Baja/media. | Depende de 1.124/1.129/1.130. | Mejor despues de definir Design System para no hacer polish aislado. | Si, al tocar zonas visibles ya aprobadas. |

## Bloque recomendado

`Design System / Density Refinement Planning`

## Justificacion del bloque recomendado

Despues de cerrar `Master Shell + Overview Layer` y `Final Screen Contracts Visual Rehousing`, la deuda menor visible mas clara es densidad visual. Antes de tocar zonas mas riesgosas como `CFG`, `DOMAIN/+`, evidencia detallada o roadmap/futuro, conviene planificar una capa acotada de refinamiento visual y reglas de densidad/tokens para estabilizar el lenguaje visual del Panel Maestro. Este bloque debe seguir siendo documental y no operativo.

El valor principal es crear criterio antes de tocar UI activa otra vez: tokens visuales, jerarquia, spacing, badges, bordes, colores semanticos y patrones de lectura deben quedar definidos para que el siguiente cambio visual no sume ruido ni parezca una nueva capacidad.

## Por que no elegir otros todavia

- `Evidence & Details Screen Planning` puede rozar payload/evidencia, requiere cuidado posterior.
- `Configuration Read-only Screen Planning` toca `CFG`, que sigue bloqueado y conviene no mover antes de estabilizar lenguaje visual.
- `Domains Context Screen Planning` toca deuda `DOMAIN/+`, mas riesgosa por posible confusion con creacion/activacion.
- `Roadmap / Future Work Screen Planning` es util, pero todavia no resuelve la densidad del core visual actual.
- `Master Shell + FSC Micro-polish Planning` puede ser util, pero conviene primero definir reglas/tokens para no hacer polish aislado sin criterio.

## Alcance futuro del bloque recomendado

Si el siguiente prompt ejecuta `Design System / Density Refinement Planning`, debera planificar:

- reglas de densidad visual;
- tokens visuales;
- jerarquia tipografica;
- spacing;
- uso de badges;
- uso de bordes;
- uso de colores semanticos;
- patrones para read-only;
- patrones para blocked;
- patrones para no-runtime/no-execution;
- patrones para evidence/documentation;
- criterios responsive;
- reglas anti-CTA operativo;
- reglas para evitar pantallas que parecen ejecutables;
- como aplicar despues esos patrones sin cambiar contrato funcional.

Este bloque futuro sera de planificacion, no implementacion directa, salvo que un prompt posterior cambie explicitamente el camino con archivos permitidos, validaciones y revision humana.

## Archivos futuros permitidos/prohibidos

Para una futura planificacion `Design System / Density Refinement Planning`:

Permitidos:

- documento nuevo en `docs/`;
- test documental nuevo en `tests/`;
- `README.md`;
- `ui/web/README.md`.

Solo lectura:

- `ui/web/index.html`;
- `ui/web/styles.css`;
- `ui/web/i18n_es.json`;
- `ui/web/backend-contract-widgets.js`;
- `ui/web/admin-panels.js`;
- `ui/web/console-interactions.js`;
- `ui/web/domains.js`.

Prohibidos:

- UI activa;
- JS;
- backend;
- `api.py`;
- `core/`;
- `domains/`;
- `providers/`;
- `tools/`;
- `scripts/`;
- modelos;
- integraciones;
- CI;
- dependencias;
- `.env`;
- secrets.

## Evaluacion restore point

Decision de publicacion: no publicar todavia.

Justificacion:

- El ultimo restore point remoto `570b18f` es reciente.
- Desde entonces hay tres commits locales: plan FSC rehousing, implementacion FSC rehousing y checkpoint FSC rehousing.
- El bloque FSC quedo aprobado visualmente y checkpoint cerrado.
- El proximo paso recomendado seria planificacion documental, no implementacion.
- No hay una necesidad inmediata de push antes de un prompt documental de planificacion.
- Despues de planificar y antes de otra implementacion visual activa, si podria convenir publicar.

Por eso corresponde continuar con planificacion documental y reevaluar publicacion antes de otra implementacion UI activa.

## Decision final

`NEXT_STEP_DESIGN_SYSTEM_DENSITY_REFINEMENT_PLANNING_SELECTED`

## Justificacion

La decision reduce riesgo porque no toca `CFG`, `+`, `DOMAIN`, evidencia/payload, roadmap ni pantallas ya aprobadas. Primero estabiliza el lenguaje visual compartido del Panel Maestro, convierte la densidad visual en reglas verificables y preserva el contrato no-runtime/no-execution.

## Proximo prompt exacto

`PROMPT UI/UX 1.132 - Planificar Design System y Density Refinement Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento bloque nuevo;
- no se modifico UI activa;
- no se modifico JS;
- no se modificaron Final Screen Contracts;
- no se modificaron elementos inferiores;
- no se modifico contrato funcional;
- no se creo contrato final;
- no se contradijo `DEFER_FINALIZATION`;
- no se creo User Panel;
- no se crearon rutas/hash;
- no se crearon endpoints/fetches nuevos;
- no se activo runtime/execution/dispatch;
- no se toco backend/runtime/endpoints/CI/dependencias;
- no se limpio deuda residual general;
- no se corrigieron pyflakes;
- no se hizo push;
- no se avanzo a 1.132.
