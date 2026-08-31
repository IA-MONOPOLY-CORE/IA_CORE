# UI/UX Panel Maestro Next Visual Block Plan 1.126

## Commit base

- Base esperada: `9ad7ddb`.
- Restore point remoto vigente: `01d09ce`.
- Rama: `main`.
- Estado esperado: local ahead de `origin/main` por 8 commits.
- Commits locales previos:
  - `8843b60`.
  - `03975b9`.
  - `f3a2670`.
  - `5a78211`.
  - `886efe6`.
  - `744d841`.
  - `fee4fd7`.
  - `9ad7ddb`.

## Objetivo

1.126 planifica el siguiente bloque visual del rediseño estructural del Panel Maestro IA_CORE y evalua si conviene publicar un restore point antes de abrir otra implementacion visual. Este documento no implementa bloque nuevo, no modifica UI activa y no avanza a 1.127.

## Estado recibido

- Decision 1.125: `PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_CHECKPOINT_PASSED_READY_FOR_NEXT_BLOCK_PLANNING`.
- Revision visual humana: `PANEL_MAESTRO_MASTER_SHELL_OVERVIEW_HUMAN_VISUAL_REVIEW_APPROVED`.
- Restore point remoto vigente: `01d09ce`.
- Estado inicial: local ahead por 8 commits.
- Primer bloque visual implementado y aprobado: `Master Shell + Overview Layer`.
- La UI mas bloqueada fue el resultado esperado y aprobado por el operador.
- Final Screen Contracts preservados.
- Elementos inferiores preservados y bloqueados.
- JS intacto y sin runtime/no-execution preservado.

## Confirmacion del primer bloque visual cerrado

El primer bloque visual quedo cerrado:

- `Master Shell + Overview Layer` fue implementado en 1.124.
- Fue aprobado visualmente por el operador.
- Fue cerrado en checkpoint 1.125.
- La UI quedo mas bloqueada y eso fue correcto para esta etapa.
- No se toco JS.
- No se tocaron Final Screen Contracts internamente.
- No se tocaron elementos inferiores.
- No se abrio runtime/execution.
- No se creo User Panel/rutas/hash.
- No se crearon endpoints/fetches.

## Candidatos evaluados

Se evaluan los candidatos de la arquitectura 1.121 contra el mapa real 1.120 y el checkpoint 1.125:

1. `Final Screen Contracts Visual Rehousing`.
2. `Domains Context Screen Planning`.
3. `Configuration Read-only Screen Planning`.
4. `Evidence & Details Screen Planning`.
5. `Design System / Visual Tokens Foundation`.
6. `Roadmap / Future Work Screen Planning`.

## Evaluacion comparativa

| Candidato | valor visual | riesgo contractual | riesgo de reactivar capacidades | archivos probables | necesidad de JS | dependencia | decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Final Screen Contracts Visual Rehousing` | Alto: consolida el corazon visible contract-aware dentro del shell nuevo. | Medio: toca el bloque contractual principal y exige preservar IDs/estados/copy. | Bajo/medio si se limita a rehousing externo sin botones, handlers ni rutas. | `ui/web/index.html`, `ui/web/styles.css` solo si hace falta soporte visual, `ui/web/i18n_es.json` solo si hace falta copy visible, docs/tests/readmes. | Ninguna por defecto; JS debe quedar solo lectura. | Requiere 1.125 cerrado y guardrails 1.122. | Bloque visual recomendado, pero despues de publicar restore point. |
| `Domains Context Screen Planning` | Medio/alto: separaria contexto de dominios del lower console. | Alto: roza `DOMAIN`, dominio y formulario historico. | Alto: podria reinterpretar `DOMAIN` o `+` como creacion. | docs/tests/readmes para planning; futura UI podria tocar `ui/web/index.html`, `ui/web/i18n_es.json` y revisar `ui/web/domains.js` solo lectura. | No recomendable; `ui/web/domains.js` debe seguir protegido. | Conviene despues de consolidar FSC y publicar restore point. | No elegir todavia. |
| `Configuration Read-only Screen Planning` | Medio: ordenaria `CFG` y configuracion observada. | Alto: toca una superficie historicamente administrativa. | Alto: podria parecer apply/save/config editable. | docs/tests/readmes para planning; futura UI podria tocar `ui/web/index.html`, `ui/web/styles.css`, `ui/web/i18n_es.json`; `ui/web/admin-panels.js` solo lectura. | No recomendable. | Requiere contrato read-only propio y revision visual fuerte. | No elegir todavia. |
| `Evidence & Details Screen Planning` | Medio/alto: reduciria densidad de `VER DETALLE` y `VER EVIDENCIA`. | Medio/alto: evidencia y payload requieren proyeccion safe. | Medio: un detalle mal rotulado puede parecer live log, fetch o payload ejecutable. | docs/tests/readmes para planning; futura UI podria tocar `ui/web/index.html`, con JS solo lectura. | No por defecto; disclosures existentes pueden conservarse. | Mejor despues de estabilizar Contracts Layer. | No elegir todavia. |
| `Design System / Visual Tokens Foundation` | Medio: daria consistencia de estados, chips y jerarquia. | Bajo/medio: abstracto, pero podria normalizar estados ambiguos si se hace mal. | Bajo si es documental; medio si toca CSS activo antes de rehousing. | docs/tests/readmes; futura UI podria tocar `ui/web/styles.css` si se aprueba. | Ninguna. | Mas util despues de ver necesidades reales del rehousing FSC. | No elegir todavia. |
| `Roadmap / Future Work Screen Planning` | Medio: separaria futuro de activo. | Bajo/medio: riesgo de que planned se lea como ready. | Bajo si solo documental. | docs/tests/readmes. | Ninguna. | No consolida la estructura contractual principal. | No elegir todavia. |

## Bloque visual recomendado

`Final Screen Contracts Visual Rehousing`

## Justificacion del bloque recomendado

Despues de implementar y aprobar `Master Shell + Overview Layer`, el siguiente paso visual logico es reorganizar externamente las cuatro pantallas contractuales ya existentes dentro de la arquitectura nueva. Este bloque consolida el corazon visible contract-aware del Panel Maestro antes de absorber elementos inferiores o crear pantallas contextuales nuevas.

La recomendacion no autoriza implementacion inmediata. El futuro bloque debera preservar completamente `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03`, `FSC-RCP-04`, `DEFER_FINALIZATION`, estados, evidencia, blockers y significado contractual.

## Por que no elegir otros todavia

- `Domains Context Screen Planning` toca la deuda `DOMAIN/+`, mas riesgosa porque puede parecer creacion directa.
- `Configuration Read-only Screen Planning` toca `CFG`, mas riesgosa porque puede parecer configuracion editable o aplicable.
- `Evidence & Details Screen Planning` puede rozar payload/evidencia, raw-safe y logs; requiere cuidado posterior.
- `Design System / Visual Tokens Foundation` puede ser util, pero sin rehousing FSC queda abstracto y no consolida el nucleo visible.
- `Roadmap / Future Work Screen Planning` es util, pero no consolida la estructura contractual principal.

## Alcance futuro del bloque recomendado

Si un prompt futuro implementa `Final Screen Contracts Visual Rehousing`, debera limitarse a:

- reorganizacion visual externa del bloque FSC;
- mejor agrupacion;
- mejor jerarquia;
- mejor separacion entre las cuatro FSC;
- labels contractuales mas claros;
- menos densidad;
- preservacion total de contenido, IDs, estados y contratos;
- revision visual humana obligatoria.

Prohibido para ese futuro prompt:

- no crear quinta seccion;
- no crear quinta sección;
- no renombrar IDs;
- no alterar `FSC-CO-01`;
- no alterar `FSC-BF-02`;
- no alterar `FSC-VR-03`;
- no alterar `FSC-RCP-04`;
- no cambiar `DEFER_FINALIZATION`;
- no agregar botones;
- no agregar acciones;
- no agregar JS;
- no crear rutas/hash;
- no crear User Panel;
- no tocar elementos inferiores;
- no tocar backend.

## Archivos permitidos/prohibidos para futura implementacion

Permitidos para una futura implementacion de `Final Screen Contracts Visual Rehousing`:

- `ui/web/index.html`.
- `ui/web/styles.css`, solo si hace falta soporte visual.
- `ui/web/i18n_es.json`, solo si hace falta copy visible.
- docs/tests/readmes.

Solo lectura:

- `ui/web/backend-contract-widgets.js`.
- `ui/web/admin-panels.js`.
- `ui/web/console-interactions.js`.
- `ui/web/domains.js`.

Prohibidos:

- `api.py`.
- `core/`.
- `domains/`.
- `providers/`.
- `tools/`.
- `scripts/`.
- modelos.
- integraciones.
- CI.
- dependencias.
- `.env`.
- secrets.
- backend operativo.

## Validaciones futuras

Una futura implementacion de rehousing FSC debera ejecutar como minimo:

- `node --check ui/web/backend-contract-widgets.js`.
- `node --check ui/web/admin-panels.js`.
- `node --check ui/web/console-interactions.js`.
- `node --check ui/web/domains.js`.
- Test nuevo especifico del rehousing visual.
- Tests 1.126, 1.125, 1.124, 1.123, 1.122, 1.121, 1.120, 1.117, 1.115, 1.114.A, 1.110, 1.106, 1.100, 1.94 y 1.88.
- Backup readiness.
- Backend contract tests relevantes, sin tocar backend.
- `git diff --check`.
- Revision visual humana obligatoria.

## Criterios de revision humana futura

La revision humana futura debera confirmar:

- las cuatro FSC siguen reconocibles;
- no hay quinta seccion;
- los IDs `FSC-CO-01`, `FSC-BF-02`, `FSC-VR-03` y `FSC-RCP-04` siguen visibles;
- `DEFER_FINALIZATION` sigue visible en Request Contract Preview;
- la reorganizacion mejora jerarquia y lectura;
- nada parece accion operativa;
- no aparecen botones nuevos, rutas/hash, User Panel, endpoint, fetch, runtime, execution ni dispatch;
- elementos inferiores `CFG`, `+` y `DOMAIN` no fueron tocados ni reactivados.

## Riesgos

| Riesgo | Senal | Mitigacion |
| --- | --- | --- |
| Rehousing altera contrato | Cambian IDs, estados, copy critico o `DEFER_FINALIZATION` | Comparar secciones y testear marcadores FSC. |
| Quinta seccion accidental | Aparece otro bloque como FSC | Test negativo y revision de estructura. |
| FSC parece CTA | Tarjetas, chips o headers parecen clickables | Sin botones nuevos, sin href y copy read-only. |
| Densidad empeora | Mas wrappers sin jerarquia clara | Limitar a agrupacion externa y labels. |
| Elementos inferiores se mezclan | `CFG`, `+` o `DOMAIN` entran al bloque FSC | Mantener lower console fuera de alcance. |
| JS innecesario | Aparece listener/handler para rehousing | JS solo lectura; detener si se requiere. |
| Rutas/hash/User Panel | Navegacion nueva aparenta app multipantalla | Prohibicion explicita y test negativo. |
| Restore point lejano | 8 commits locales sin publicacion | Publicar restore point antes de otra UI activa. |

## Evaluacion de publicacion restore point

Hay 8 commits locales desde `01d09ce`:

- planificacion 1.118;
- rediseño estructural 1.119;
- auditoria 1.120;
- arquitectura visual 1.121;
- guardrails 1.122;
- plan primer bloque 1.123;
- implementacion primer bloque 1.124;
- checkpoint 1.125.

El primer bloque visual fue implementado, testeado, commiteado y aprobado visualmente. El working tree inicial estaba limpio, las validaciones del checkpoint pasaron y no hubo push desde `01d09ce`. Como el siguiente bloque recomendado podria volver a modificar UI activa, conviene publicar un restore point remoto antes de implementarlo.

Este prompt no hace push. Solo decide que el proximo prompt deberia publicar el restore point antes de abrir `Final Screen Contracts Visual Rehousing`.

## Decision final

`NEXT_STEP_RESTORE_POINT_PUBLICATION_SELECTED_BEFORE_NEXT_VISUAL_BLOCK`

## Justificacion

Aunque el siguiente bloque visual recomendado es `Final Screen Contracts Visual Rehousing`, ya existen 8 commits locales sin push desde el restore point remoto `01d09ce`. El primer bloque visual quedo cerrado y aprobado visualmente; antes de abrir otra modificacion de UI activa, conviene publicar un restore point remoto reproducible.

## Proximo prompt exacto

`PROMPT UI/UX 1.127 - Publicar restore point primer bloque visual Master Shell Overview Panel Maestro IA_CORE contract-aware sin runtime/no-execution`

## Limites preservados

- no se implemento bloque nuevo;
- no bloque nuevo;
- no se modifico UI activa;
- no UI activa;
- no se modifico JS;
- no JS;
- no se modificaron Final Screen Contracts;
- no Final Screen Contracts;
- no se modificaron elementos inferiores;
- no elementos inferiores;
- no se modifico contrato funcional;
- no contrato funcional;
- no se creo contrato final;
- no contrato final;
- no se contradijo `DEFER_FINALIZATION`;
- no se creo User Panel;
- no User Panel;
- no se crearon rutas/hash;
- no rutas/hash;
- no se crearon endpoints/fetches nuevos;
- no endpoints/fetches nuevos;
- no se activo runtime/execution/dispatch;
- no runtime;
- no execution;
- no dispatch;
- no se toco backend/runtime/endpoints/CI/dependencias;
- no CI;
- no se limpio deuda residual general;
- no deuda residual;
- no se corrigieron pyflakes;
- no pyflakes;
- no se hizo push;
- no push;
- no se avanzo a 1.127.
