# UI/UX 1.199 - Paquetes irreducibles para Direccion

## Gate

`N5_IRREDUCIBLE_DIRECTION_PACKAGES_PASSED`

N5 construye paquetes conceptuales para los niveles B, C y D. Los 200 casos
de `LEVEL_A_FULLY_DETERMINISTIC` quedan fuera porque no requieren decision
humana. El resultado es:

- `TRUE_DIRECTION_PACKAGES = 8`;
- `TOTAL_OCCURRENCES_GOVERNED = 1424`;
- `TOTAL_DECISION_UNITS_GOVERNED = 1032`;
- `LEVEL_A_OUTSIDE_PACKAGES = 111 units / 200 occurrences`.

No se mezclan editorial, accion/permiso y cambio contractual en un mismo
paquete.

## Resumen de paquetes

| ID | Nivel | Unidades | Ocurrencias | Decision conceptual |
| --- | --- | ---: | ---: | --- |
| `PKG_B_EDITORIAL_STYLE` | B | 288 | 295 | Aprobar una regla editorial acotada |
| `PKG_B_CONSISTENCY_RULE` | B | 80 | 194 | Elegir politica de consistencia |
| `PKG_B_GEOMETRY_REMEDIATION` | B | 4 | 15 | Elegir owner del remedio geometrico |
| `PKG_C_CONTEXTUAL_VARIANTS` | C | 36 | 36 | Preservar o unificar variantes contextuales |
| `PKG_C_CONTRACT_SENSITIVE` | C | 134 | 139 | Mantener o abrir revision contractual |
| `PKG_C_ACTION_PERMISSION` | C | 14 | 15 | Fijar rol de action/permission vocabulary |
| `PKG_C_AMBIGUOUS_ROLE` | C | 38 | 38 | Elegir rol semantico de casos ambiguos |
| `PKG_D_CONTRACT_VOCABULARY` | D | 438 | 692 | Decidir si se planifica version contractual |
| **Total** | — | **1032** | **1424** | — |

## PKG_B_EDITORIAL_STYLE

**Nombre:** Regla de estilo editorial y presentacional.

**Problema:** 295 ocurrencias de copy editorial, labels, navegacion,
formularios y placeholders podrian ordenarse sin tocar contrato.

**Superficies:** UI general, admin, domain, navegacion, formularios e i18n
general. **Contrato:** ninguno demostrado como autoridad directa.

**Regla existente:** preservar significado, i18n, nombres accesibles y
densidad; nunca convertir un label en accion.

**Por que no decide solo el agente:** idioma, tono y casing son preferencias de
producto aunque el limite tecnico sea determinista.

**Opciones:** A mantener wording; B aprobar regla editorial por IDs; C
posponer normalizacion.

**Recomendacion:** A en el estado actual; B solo con allowlist estable y
revision de accesibilidad/localizacion.

**Confianza:** alta en el limite, media en la preferencia.

**Decision minima:** aprobar o rechazar una regla, no 295 textos.

**Automatizacion posterior:** aplicar IDs aprobados y verificar HTML/i18n/ARIA.

**Permanece bloqueado:** copy contractual, permisos, acciones, readiness y
estados exactos.

## PKG_B_CONSISTENCY_RULE

**Nombre:** Regla de consistencia sin perdida de contexto.

**Problema:** 194 ocurrencias tienen repeticion equivalente, casing o tokens
que podrian ordenarse, pero los duplicados contextuales no deben fusionarse.

**Superficies:** P0/P1/P2/P3, widgets, Request Draft e i18n contractual.
**Contrato:** autoridad contractual solo cuando la evidencia coincide.

**Regla existente:** compartir unicamente texto, autoridad y categoria de
decision equivalentes.

**Por que no decide solo el agente:** Direccion debe preferir consistencia o
preservacion contextual.

**Opciones:** A preservar contexto; B canonizar equivalentes de misma
autoridad; C canonizacion amplia.

**Recomendacion:** A; B es el maximo patron futuro seguro; C se rechaza.

**Confianza:** alta en la separacion de autoridades, media en la preferencia.

**Decision minima:** elegir politica de consistencia para el corpus.

**Automatizacion posterior:** aplicar la politica a unidades equivalentes y
rechazar merges contextuales.

**Permanece bloqueado:** fusion entre autoridades diferentes.

## PKG_B_GEOMETRY_REMEDIATION

**Nombre:** Owner de riesgos geometricos locales.

**Problema:** 15 ocurrencias tienen wrapping u overflow local sin overflow
global.

**Superficies:** cajas de payload/request y drawer Request Draft mobile.
**Contrato:** wording contractual y payload permanecen intactos.

**Regla existente:** medir geometry, conservar texto y resolver primero con
layout/CSS scoped si corresponde.

**Por que no decide solo el agente:** asignar el remedio a CSS, layout o
wording es una decision de ownership.

**Opciones:** A observar; B CSS/layout scoped; C revision de wording.

**Recomendacion:** B para boxes/drawer, con wording sin cambios.

**Confianza:** alta en evidencia, media en owner.

**Decision minima:** elegir owner y limite de remediation.

**Automatizacion posterior:** repetir viewport, resize, console y overflow
checks.

**Permanece bloqueado:** cambios de copy, severidad o contrato por una medida
local.

## PKG_C_CONTEXTUAL_VARIANTS

**Nombre:** Variantes contextuales que no se deben mezclar.

**Problema:** 36 ocurrencias comparten apariencia textual pero pertenecen a
autoridades o superficies distintas.

**Regla existente:** el mismo texto no implica la misma decision si cambia el
contexto contractual.

**Por que no decide solo el agente:** solo Direccion puede preferir uniformidad
sobre contexto.

**Opciones:** A mantener variantes; B unificar dentro de misma autoridad; C
unificar todo.

**Recomendacion:** A; C no es segura.

**Confianza:** alta en que no deben fusionarse automaticamente.

**Decision minima:** preservar contexto o autorizar regla de autoridad.

**Automatizacion posterior:** bloquear merges que crucen la autoridad
aprobada.

**Permanece bloqueado:** canonizacion global.

## PKG_C_CONTRACT_SENSITIVE

**Nombre:** Copy explicativo y diagnostico contract-sensitive.

**Problema:** 139 ocurrencias explican limites, warnings, errors o evidencia.

**Regla existente:** backend authoritative, UI read-only, deny-by-default y sin
runtime/execution.

**Por que no decide solo el agente:** tono, severidad y detalle pueden cambiar
la lectura del contrato.

**Opciones:** A mantener; B revision acotada con Contract Owner; C cambio
contractual separado.

**Recomendacion:** A hasta que exista necesidad demostrable.

**Confianza:** alta.

**Decision minima:** mantener o abrir revision contractual.

**Automatizacion posterior:** snapshots, trazabilidad y checks de vocabulario.

**Permanece bloqueado:** cambiar severidad, source/status/fallback o limites.

## PKG_C_ACTION_PERMISSION

**Nombre:** Interpretacion de acciones y permisos.

**Problema:** 15 ocurrencias usan vocabulario que podria leerse como accion,
label o autoridad.

**Regla existente:** `allowed_actions` es dato declarado, no CTA; permisos no
se infieren.

**Por que no decide solo el agente:** no puede elegir si la palabra es
boundary, etiqueta o permiso.

**Opciones:** A dato/boundary read-only; B vocabulario contractual explicito; C
accion o permiso nuevo.

**Recomendacion:** A; B solo con version contractual; C fuera de 1.199.

**Confianza:** alta en que no puede convertirse en CTA.

**Decision minima:** elegir rol semantico sin habilitar ejecucion.

**Automatizacion posterior:** rechazar CTA/submit/dispatch/runtime y validar el
vocabulario elegido.

**Permanece bloqueado:** acciones operativas, permisos inferidos y payload v2.

## PKG_C_AMBIGUOUS_ROLE

**Nombre:** Rol semantico de copy ambiguo.

**Problema:** 38 ocurrencias siguen admitiendo mas de una lectura despues de
contrato, precedentes y consistencia.

**Regla existente:** no inventar significado; separar label, boundary, estado
y permiso.

**Por que no decide solo el agente:** queda una preferencia de producto o
semantica no derivable de evidencia unica.

**Opciones:** A mantener; B declararlo boundary/dato; C redefinir rol mediante
cambio contractual.

**Recomendacion:** A mientras no exista contradiccion demostrada; B antes que
cualquier alternativa operativa.

**Confianza:** alta en la necesidad de Direccion, media en la opcion final.

**Decision minima:** elegir rol conceptual del paquete.

**Automatizacion posterior:** aplicar allowlist aprobada y bloquear lecturas no
aprobadas.

**Permanece bloqueado:** permiso, runtime, ejecucion, dispatch y submit.

## PKG_D_CONTRACT_VOCABULARY

**Nombre:** Version futura del vocabulario contractual.

**Problema:** 692 ocurrencias son vocabulario exacto o limites que no pueden
cambiar bajo el contrato actual.

**Regla existente:** preservar blockers, source/status/fallback, readiness,
`no_payload`, `not_available` y deny-by-default.

**Por que no decide solo el agente:** no es preferencia editorial; el cambio
desincronizaria el contrato.

**Opciones:** A no cambiar; B planificar version contractual; C rechazar
cualquier cambio en esta etapa.

**Recomendacion:** A en 1.199; B como trabajo contractual posterior separado.

**Confianza:** alta.

**Decision minima:** decidir si existe necesidad de versionar, sin aprobar
wording ahora.

**Automatizacion posterior:** solo despues de versionar contrato y actualizar
allowlists/regresion.

**Permanece bloqueado:** toda edicion bajo contrato vigente.

## Resultado N5

`N5_IRREDUCIBLE_DIRECTION_PACKAGES_PASSED`

Los ocho paquetes reducen decisiones humanas/patron a conceptos comprensibles
sin pedirle a Direccion que clasifique 1624 ocurrencias ni mezclar autoridades
incompatibles.
