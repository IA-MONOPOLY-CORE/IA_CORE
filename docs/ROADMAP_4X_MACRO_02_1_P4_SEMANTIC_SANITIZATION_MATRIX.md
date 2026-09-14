# P4 Semantic Sanitization Matrix - Roadmap 4.x Macro 02.1

La decision se tomo sobre contenido real del registry y consumidores locales,
no por el nombre del campo. La sanitizacion ocurre en la frontera HTTP, sin
reescribir los artefactos privados del registry.

| Campo | Consumidor local demostrado | Necesidad | Sensibilidad evaluada | Disposicion |
| --- | --- | --- | --- | --- |
| `id` | selector y match local | identificar preset | safe si es ID canonico | `REQUIRED_SAFE_EXPOSED` |
| `role_id` | selector, match y catalogo | relacionar rol | safe como ID canonico | `REQUIRED_SAFE_EXPOSED` |
| `specialization_id` | selector, match y catalogo | relacionar especializacion | safe como ID canonico | `REQUIRED_SAFE_EXPOSED` |
| `nombre_visible` | `ui/web/index.html` | eleccion humana visible | safe si es texto corto sin saltos | `REQUIRED_SAFE_EXPOSED` |
| `suggested_agent_id` | `ui/web/index.html` | preseleccion local demostrada | safe como referencia visible | `REQUIRED_SAFE_EXPOSED` |
| `suggested_agent_name` | `ui/web/index.html` | rotulo visible | safe si es texto corto | `REQUIRED_SAFE_EXPOSED` |
| `short_description` | selector local | comparar presets | safe solo como texto corto | `REQUIRED_SAFE_EXPOSED` |
| `decision_criteria` | render en `ui/web/index.html` | elegir un preset con criterio descriptivo | fixture real: lista de strings descriptivos; no prompt interno | `REQUIRED_SAFE_EXPOSED` |
| `avoid` | `core/agent_paper_schema.py` y flujo local de paper | conservar restricciones funcionales | fixture real: lista de strings descriptivos; no secretos ni instrucciones privadas | `REQUIRED_SAFE_EXPOSED` |
| `orden` | ordenamiento de coleccion | estabilidad de presentacion | entero exacto; bool rechazado | `REQUIRED_SAFE_EXPOSED` |

## Reglas estructurales

- La allowlist es explicita y se recorre por campo, de modo que el orden de
  entrada no modifica la decision.
- Los campos de texto deben ser strings sin espacios de borde ni CR/LF.
- `decision_criteria` y `avoid` solo conservan elementos string, sin espacios
  de borde ni CR/LF; objetos, metadata anidada y valores no-string se eliminan.
- `orden` solo conserva `int` exacto, no `bool`.
- Valores de tipo objeto en campos de texto no se convierten ni se serializan.
- La misma funcion se aplica a la coleccion de presets y al resultado de
  `agent-presets/match` antes de la respuesta HTTP.

## Campos excluidos

Siempre permanecen ausentes `system_prompt`, `recommended_provider`,
`recommended_model`, `recommended_temperature`, `memory_policy`, `paper_seed`,
`activo`, secretos o referencias a secretos, instrucciones operacionales
privadas y cualquier campo desconocido. El fixture contaminado incluyo esos
campos, objetos anidados y metadata operacional; ninguno sobrevivio en la
respuesta serializada.

## Evidencia de compatibilidad

El fixture real `domains/loteria/agent_presets.json` contiene listas de strings
para `decision_criteria` y `avoid`. `ui/web/index.html` consume
`decision_criteria` y `suggested_agent_id`; `core/agent_paper_schema.py` consume
`decision_criteria` y `avoid`. Por eso ambos campos se preservan, pero solo en
su forma estructural segura. No se cambio ningun consumidor ni el registry.

Resultado: `REQUIRED_SAFE_EXPOSED` para los diez campos de la allowlist;
`REQUIRED_BUT_SENSITIVE_INTERNAL_ONLY`, `NOT_REQUIRED_EXCLUDED` y
`UNKNOWN_REMAIN_DEFAULT_DENIED` aplican a los campos fuera de esa allowlist.
