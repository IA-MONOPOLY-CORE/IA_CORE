# UI/UX Panel Maestro Next Visual Block Selection 1.188

## 1. Estado de entrada

- Carpeta: `C:\IA_CORE`.
- Branch: `main`.
- HEAD inicial: `e2d1653`.
- `origin/main` inicial: `e2d1653`.
- Ahead/behind inicial: `0/0`.
- Working tree inicial: limpio.
- Ultimo cierre: UI/UX 1.187.
- Decision recibida: `UI_UX_MATRIX_VISUAL_HIERARCHY_DEMOTION_CHECKPOINT_PASSED`.
- Readiness recibida: `ready_for_ui_ux_1_188_next_visual_block_selection`.

## 2. Motivo y alcance

Esta es la seleccion visual posterior al checkpoint de Matriz. Se releen los
documentos 1.175-1.187 y se audita la UI activa en modo read-only para elegir
un unico bloque futuro. El alcance queda limitado a documentacion, test y
README minimo: no implementacion, no UI activa, no CSS activo, no JS
contractual, no backend, no-runtime, no-execution, no endpoints y no payload
v2.

No se modifica `backend_internal_ui_payload.v1`, HTML, CSS, JavaScript,
i18n, payloads, runtime, execution, dispatch, integraciones ni contratos.

## 3. Estado visual actual observado

- **P0:** permanece arriba como sintesis Estado -> Contrato -> Limites ->
  Evidencia -> Proximo paso; sigue read-only, no-runtime y no-execution.
- **P1:** conserva Contract Overview, Blocked & Forbidden, Validation &
  Readiness y Request Contract Preview como lectura contractual principal.
- **Matriz:** continua completa, visible y secundaria P3/auditoria, con 20
  filas, seis estados y 26 badges; su opacity observada es `0.94`.
- **P2/P3 restante:** Readiness Global, Contract Core/Payload, Raw-safe,
  Internal Services/Signals y Evidence siguen disponibles como detalle y
  trazabilidad, sin reordenamiento nuevo.
- **Request Contract Preview / Request Draft Panel:** en desktop ocupa 340 px
  fijos a la derecha. Muestra `BLOCKED`, copy read-only y el control deshabilitado
  `BLOQUEADO POR CONTRATO`; conserva un toggle de drawer. En mobile queda
  `collapsed`, con asa de 44 px, sin overflow.
- **Widgets contract-aware:** preservan `allowed_actions`, `forbidden_actions`,
  `blocked_capabilities`, `source`, `status`, `fallback`, `no_payload` y
  `not_available` bajo deny-by-default.
- **Badges/estados:** los seis estados de Matriz y los badges contractuales
  siguen visibles; no representan runtime ni permiso.
- **Affordances bloqueadas:** CFG, DOMAIN y controles inferiores siguen
  `disabled`, `aria-disabled` y contract-blocked; son deuda real, pero estan
  alejados de la lectura principal.
- **Readiness y microcopy:** `no_payload`, `not_available`, no-runtime,
  no-execution y blocked siguen siendo claros, aunque deliberadamente
  reiterados para preservar limites contractuales.

### Evidencia responsive

En desktop 1440x1000 se observo `clientWidth == scrollWidth == 1425`, P0 con
ancho 1024.8 px, Matriz con ancho 1024.8 px y panel derecho de 340 px. En mobile
390x844 se observo `clientWidth == scrollWidth == 375`, Matriz completa y panel
`collapsed`. En resize desktop -> mobile -> desktop no hubo overflow ni errores
de consola; el panel conserva el estado collapsed tras el cambio de viewport.

## 4. Candidatos evaluados

| Candidato | Impacto visual | Claridad de producto | Riesgo contractual | Riesgo tecnico | Riesgo responsive | Dependencia backend/JS | Riesgo P0/P1/Matriz | Reversibilidad | Tamano esperado | Conveniencia | Modelo/herramienta ideal | Nivel de esfuerzo | Veredicto |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Candidato A - Panel derecho Request Contract Preview / Request Draft Panel** | Alto | Alto | Medio | Medio | Medio | Ninguna para CSS; baja si se requiere HTML no funcional | Baja | Alta | Medio | Alta | Modelo avanzado estable, inspeccion visual/DOM y tests | Alto | Seleccionado |
| **Candidato B - Affordances bloqueadas / acciones no ejecutables** | Medio | Medio | Medio-alto | Medio | Bajo | Baja-media por disabled/ARIA/eventos | Baja | Media | Medio | Media | Modelo avanzado estable, auditoria semantica y tests | Alto | Candidato futuro |
| **Candidato C - Repeticion semantica transversal** | Medio-alto | Medio | Alto | Medio-alto | Bajo | Ninguna | Media | Media | Grande | Baja-media | Modelo premium, revision contractual transversal | Muy alto | Postergar |
| **Candidato D - P2/P3 restante** | Medio | Medio | Medio | Medio-alto | Medio | Ninguna | Media | Media | Grande | Media-baja | Modelo premium, mapa visual y regression suite | Muy alto | Postergar |
| **Candidato E - Readiness Global / Proximo paso / Estado de cierre** | Medio | Medio-alto | Medio | Bajo-medio | Bajo | Ninguna | Media por duplicar P0 | Alta | Pequeno-medio | Media | Modelo avanzado estable, inspeccion de copy y layout | Alto | Postergar |
| **Candidato F - Sistema visual de severidad/estado** | Medio-alto | Alto | Medio-alto | Medio | Medio | Ninguna | Media | Media | Medio-grande | Media | Modelo premium, auditoria de semantica visual | Muy alto | Postergar |
| **Candidato G - Compactacion de secciones informativas sin perdida de evidencia** | Medio | Medio | Medio | Medio | Medio-alto | Ninguna | Media | Alta | Medio-grande | Media-baja | Modelo avanzado estable, pruebas responsive extensas | Alto | Postergar |
| **Candidato H - Microcopy contractual / lenguaje de claridad** | Bajo-medio | Medio | Medio-alto | Bajo | Bajo | Ninguna | Media | Alta | Pequeno | Media-baja | Modelo avanzado estable, revision contractual | Alto | Postergar |

## 5. Decision unica

**Candidato seleccionado: A - Panel derecho Request Contract Preview / Request Draft Panel.**

El panel derecho es la deuda visual con mayor impacto sobre la primera lectura
desktop que sigue abierta despues de P0, P1 y la democion de Matriz. Sus 340 px
fijos, su borde lateral fuerte y su boton ancho deshabilitado conservan evidencia
valiosa, pero le dan presencia de herramienta operativa a una vista previa
contractual que no ejecuta.

Ahora es el momento correcto porque P0, P1 y Matriz ya fueron implementados y
checkpointados: ajustar el panel no exige reabrir su jerarquia ni disputar la
lectura principal. Antes era prudente postergarlo por el riesgo de romper P1 o
el drawer responsive; despues, dejarlo igual perpetuaria la principal
competencia lateral restante. La mejora futura debe reducir friccion visual y
evitar promesa falsa de ejecucion, no resolver affordances inferiores,
repeticion transversal, P2/P3 completo ni semantica global de estados.

La seleccion no necesita backend, runtime, execution ni JavaScript contractual:
el primer intento debe ser CSS scoped al panel. Cualquier HTML opcional debe ser
no funcional, conservar textos y controles bloqueados, y quedar prohibido si
invade contrato, handlers o i18n.

## 6. Candidatos no seleccionados

- **B:** los controles bloqueados son una deuda valida, pero CFG y DOMAIN quedan
  en P3; revisar disabled, ARIA y eventos tiene mas riesgo semantico que el
  ajuste puramente visual del panel.
- **C:** reducir repeticion puede ser util, pero atraviesa P0-P3 y puede borrar
  guardas que hoy previenen interpretaciones operativas.
- **D:** P2/P3 restante requiere una seleccion mas quirurgica; no conviene
  compactar secciones heterogeneas como un solo cambio.
- **E:** P0 ya comunica readiness y proximo paso; tocarlo ahora duplicaria la
  sintesis antes de resolver la competencia lateral visible.
- **F:** un sistema transversal de severidad exige validar cada estado y badge;
  es una tarea posterior de mayor superficie.
- **G:** la Matriz ya fue compactada sin ocultamiento; compactar el resto no
  presenta una deuda medible tan directa como el panel fijo.
- **H:** el microcopy es correcto y contractualmente preciso; retocarlo primero
  daria menos claridad que rebajar la presencia del panel.

## 7. Alcance recomendado para UI/UX 1.189

UI/UX 1.189 deberia ser una implementacion visual CSS-only quirurgica del
`Request Draft Panel`, con una excepcion HTML+CSS no funcional solo si la
evidencia muestra que no puede aclararse su rol sin un marker estatico. Debe:

1. Reducir la competencia visual lateral del panel en desktop sin ocultarlo.
2. Mantener `Request Contract Preview`, `BLOCKED`, no submit/no dispatch/no
   execution, `allowed_actions`, `forbidden_actions` y `blocked_capabilities`.
3. Mantener el control deshabilitado como evidencia, sin transformarlo en CTA,
   sin handler nuevo y sin inferir permiso.
4. Preservar la geometria de P0, P1, Matriz, P2/P3 y los cuatro widgets.
5. Probar desktop, mobile y resize; el drawer collapsed debe seguir estable.
6. Incluir checkpoint posterior dedicado al panel.

Archivos probablemente permitidos: `ui/web/styles.css` con selectores scoped al
panel; `ui/web/index.html` solo si hiciera falta copy o marker no funcional;
documento/test 1.189 y README minimos. Archivos que deben seguir prohibidos:
`ui/web/backend-contract-widgets.js`, i18n, admin panels, console interactions,
domains, backend, payload v1, payload v2, API, core, runtime, execution,
endpoints, integrations, package files, secrets y CI.

Validaciones obligatorias recomendadas: conteo y visibilidad de P0/P1/Matriz,
preservacion del panel y control disabled, ausencia de handlers/CTAs/payload v2,
`py_compile`, `node --check`, test focal e historicos, `git diff --check`,
allowlist estricta, desktop 1440x1000, mobile 390x844 y resize sin recarga.
El criterio de cierre es que el panel se lea como preview contractual secundaria,
visible y legible, sin perder limites ni generar overflow. Debe existir un
checkpoint posterior antes de seleccionar otro bloque.

## 8. Recomendacion armonica para el proximo prompt

**Modelo/herramienta ideal:** modelo avanzado estable con inspeccion visual de
navegador/DOM y tests de contrato; portable entre proveedores. En el set actual,
GPT-5.6 Terra o GPT-5.6 Sol son equivalentes razonables.

**Nivel de esfuerzo ideal:** alto. **Tipo de tarea:** CSS-only quirurgica con
posible HTML+CSS no funcional, contract-aware y responsive.

La recomendacion busca un balance: no debe buscar el minimo y no debe buscar el
maximo. Una opcion menor puede quedar justa al medir la competencia visual,
preservar el drawer y evitar que un control blocked parezca ejecucion. Una opcion
premium extrema seria derroche mientras el alcance permanezca scoped al panel y
no toque JavaScript ni contrato. Subir a modelo premium/muy alto solo si la
evidencia exige HTML no funcional cruzado con P0/P1 o revela una regresion
responsive compleja. Bajar a esfuerzo medio solo si el cambio se confirma como
CSS aislado sin ambiguedad visual. Elegir mal aumenta el riesgo de retrabajo por
reabrir P0/P1, alterar el drawer o transformar evidencia blocked en CTA.

Veredicto de eficiencia: `balanceado`.

## 9. Riesgos y deudas aceptadas

Riesgos del Candidato A: ocultar limites, reducir legibilidad, alterar el
drawer mobile, crear una CTA aparente, afectar el ancho reservado a P0/P1 o
introducir reglas CSS demasiado amplias. Las deudas aceptadas son B-H, en el
orden de riesgo y evidencia descrito arriba; UI/UX 1.x no se declara cerrado.

## 10. Veredicto y continuidad

`UI_UX_NEXT_VISUAL_BLOCK_SELECTED_POST_MATRIX_CHECKPOINT`

Readiness: `ready_for_ui_ux_1_189_selected_visual_block_implementation`.

Proximo prompt exacto:

`PROMPT UI/UX 1.189 — Implementar próximo bloque visual seleccionado del Panel Maestro IA_CORE contract-aware`

UI/UX 1.189 no se ejecuta dentro de esta seleccion.
