# UI/UX 1.199 - Decision Sheet de Direccion

## DECISIONES QUE NECESITA TOMAR SANTI
**Cantidad total: 8**

Este documento convierte el corpus de microcopy contractual en ocho decisiones
de paquete. No solicita elegir texto por texto y no autoriza cambios activos.
Las decisiones se responden por paquete, conservando las restricciones del
contrato actual y separando patrones automatizables de cambios que requieren
Direccion o Contract Owner.

## Compresion ejecutiva

`1624 MICROCOPY_ITEMS -> 1143 DECISION_UNITS -> 8 DIRECTION_PACKAGES -> 8 DECISIONES REALES PARA SANTI`

- `LEVEL_A_FULLY_DETERMINISTIC`: 111 unidades / 200 ocurrencias; no requiere una preferencia nueva.
- `LEVEL_B_PREAUTHORIZED_PATTERN`: 372 unidades / 504 ocurrencias; requiere aprobar un patrón, no cada fila.
- `LEVEL_C_DIRECTION_PACKAGE`: 222 unidades / 228 ocurrencias; requiere una decisión semántica por paquete.
- `LEVEL_D_CONTRACT_CHANGE`: 438 unidades / 692 ocurrencias; no es una decisión de microcopy simple.
- `KEEP_NO_DECISION`: 30 unidades / 30 ocurrencias; se preservan sin intervención.

## 1. PKG_B_EDITORIAL_STYLE

- **Alcance:** 295 ocurrencias; estilo editorial repetible dentro de la autoridad existente.
- **Problema:** casing, labels o patrones editoriales pueden normalizarse sin alterar el contrato si la autoridad y el rol son equivalentes.
- **Opciones:** A) mantener cada formulación; B) aprobar un patrón editorial scoped; C) canonizar ampliamente.
- **Recomendación:** B, con allowlist por unidad y sin cruzar superficies contractuales.
- **Consecuencia:** A conserva variantes; B reduce repetición controlada; C queda rechazada por riesgo de borrar contexto.
- **Respuesta requerida:** elegir A, B o C para el patrón editorial, no editar 295 filas.

## 2. PKG_B_CONSISTENCY_RULE

- **Alcance:** 194 ocurrencias; consistencia de labels, casing y tokens con autoridad equivalente.
- **Problema:** equivalencia textual no alcanza para fusionar superficies o estados diferentes.
- **Opciones:** A) preservar cada contexto; B) canonizar solo equivalentes con misma autoridad; C) intentar canonización amplia.
- **Recomendación:** A por defecto; B es el máximo patrón seguro futuro; C queda rechazada.
- **Consecuencia:** una regla aprobada puede aplicarse automáticamente, pero los merges contextuales seguirán bloqueados.
- **Respuesta requerida:** definir la política de consistencia, no seleccionar textos individuales.

## 3. PKG_B_GEOMETRY_REMEDIATION

- **Alcance:** 15 ocurrencias con wrapping u overflow local medido, sin overflow global.
- **Problema:** la evidencia geométrica es objetiva, pero el owner del remedio puede ser CSS/layout o wording.
- **Opciones:** A) mantener y observar; B) autorizar corrección CSS/layout scoped; C) abrir revisión de wording contractual.
- **Recomendación:** B para drawer y cajas locales, manteniendo el wording.
- **Consecuencia:** B permite remediar presentación sin crear estados, CTA ni cambio semántico.
- **Respuesta requerida:** elegir owner y límite de la remediation geométrica.

## 4. PKG_C_CONTEXTUAL_VARIANTS

- **Alcance:** 36 ocurrencias consistentes por texto, pero pertenecientes a contextos que no comparten una autoridad única.
- **Problema:** el mismo texto no implica la misma decisión cuando cambia superficie, estado o contrato.
- **Opciones:** A) mantener variantes por contexto; B) unificar solo dentro de la misma autoridad; C) unificar todas.
- **Recomendación:** A; B requiere una regla explícita de autoridad; C no es segura.
- **Consecuencia:** preservar contexto evita que una normalización visual cambie el significado operativo.
- **Respuesta requerida:** elegir preservar contexto o autorizar una regla de autoridad acotada.

## 5. PKG_C_CONTRACT_SENSITIVE

- **Alcance:** 139 ocurrencias explicativas o diagnósticas relacionadas con límites, warnings, errors o evidencia.
- **Problema:** una modificación puede cambiar cómo el operador interpreta el contrato.
- **Opciones:** A) mantener exactamente; B) aprobar revisión acotada con Contract Owner; C) proponer cambio contractual separado.
- **Recomendación:** A hasta que exista necesidad demostrable y owner contractual.
- **Consecuencia:** B o C abren trabajo posterior; ninguna autoriza wording activo dentro de 1.199.
- **Respuesta requerida:** decidir si se mantiene el texto o se abre una revisión contractual.

## 6. PKG_C_ACTION_PERMISSION

- **Alcance:** 15 ocurrencias con vocabulario que podría leerse como acción, label o autoridad.
- **Problema:** `allowed_actions` es dato declarado, no CTA; no se infieren permisos.
- **Opciones:** A) mantener como dato/boundary read-only; B) definir vocabulario contractual explícito; C) autorizar acción o permiso nuevo.
- **Recomendación:** A; B solo mediante versión contractual; C está fuera del alcance 1.199.
- **Consecuencia:** cualquier decisión debe conservar no-CTA, no-submit, no-dispatch y no-runtime.
- **Respuesta requerida:** elegir el rol semántico sin habilitar ejecución.

## 7. PKG_C_AMBIGUOUS_ROLE

- **Alcance:** 38 ocurrencias que admiten más de una lectura honesta después de contrato, precedentes y consistencia.
- **Problema:** no hay evidencia única para decidir entre label, boundary, estado o permiso.
- **Opciones:** A) mantener formulación actual; B) declararla explícitamente boundary/dato; C) redefinir el rol mediante cambio contractual.
- **Recomendación:** A mientras no exista contradicción; B antes que cualquier alternativa operativa.
- **Consecuencia:** A conserva seguridad; B requiere allowlist semántica; C sale de 1.199.
- **Respuesta requerida:** elegir el rol conceptual del paquete, no reescribir fila por fila.

## 8. PKG_D_CONTRACT_VOCABULARY

- **Alcance:** 692 ocurrencias de vocabulario exacto o límites contractuales.
- **Problema:** cambiar estos términos puede desincronizar contrato, UI y lectura del operador.
- **Opciones:** A) no cambiar y mantener el contrato vigente; B) planificar una nueva versión contractual; C) rechazar cualquier cambio de vocabulario en esta etapa.
- **Recomendación:** A en 1.199; B solo como trabajo contractual posterior separado.
- **Consecuencia:** no existe autorización para editar las 692 ocurrencias bajo el contrato actual.
- **Respuesta requerida:** decidir si alguna necesidad justifica versionar el contrato; no aprobar wording aquí.
- **Advertencia:** **NO ES UNA DECISION DE MICROCOPY SIMPLE.** Requiere Contract Owner, versión contractual, allowlists nuevas y regresión completa.

## Lo que Santi no necesita decidir

- Los 111 grupos Level A completamente deterministas.
- Los 170 registros derivables del contrato existente.
- Los 30 registros `KEEP_NO_DECISION`.
- La deduplicación mecánica que ya fue normalizada sin fusionar autoridades.
- La evidencia de geometría, conteos, digest y regresión.

## Lo que el agente puede hacer solo después de una respuesta aprobada

- Compilar una allowlist por `decision_unit_id` y paquete.
- Aplicar únicamente el patrón autorizado y rechazar merges fuera de autoridad.
- Repetir geometry, resize, consola, accesibilidad y regresión.
- Preservar no-CTA, no-submit, no-dispatch, no-runtime, deny-by-default y payload v1.
- Detenerse ante una solicitud de cambio contractual o permiso no declarado.

## Aprobación de patrones

La aprobación de un patrón cubre 504 ocurrencias Level B: editorial, consistencia
y geometría. No autoriza cambios de contrato, acciones, permisos ni variantes
contextuales. La futura ejecución debe permanecer scoped, auditable y reversible.

## Cambio contractual

Las 692 ocurrencias Level D no pueden entrar en una implementación de microcopy.
Un eventual cambio requiere owner contractual, nueva versión, actualización de
allowlist, revisión de payload y regresión separada. Hasta entonces se mantiene
el vocabulario vigente.

## Estado de cierre de N7

`N7_MICROCOPY_DIRECTOR_DECISION_SHEET_CHECKPOINT_PASSED`

`UI_UX_MICROCOPY_DIRECTION_DECISION_COMPRESSION_REVIEW_PASSED`

Este documento no modifica producto, wording activo, HTML, CSS, JavaScript,
i18n, backend, payload, runtime, execution, endpoints ni integrations.

Readiness: `ready_for_ui_ux_1_200_microcopy_direction_decisions`

Siguiente prompt exacto:

`PROMPT UI/UX 1.200 — Resolver decisiones de Dirección del microcopy contractual y compilar bloque de ejecución post-aprobación del Panel Maestro IA_CORE`

UI/UX 1.200 no se ejecuta dentro de 1.199.
