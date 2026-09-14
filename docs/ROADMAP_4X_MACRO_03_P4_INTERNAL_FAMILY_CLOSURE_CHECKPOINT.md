# Roadmap 4.x Macro-Mission 03 - P4 Internal Family Closure

## Resultado de la estacion

`P4_INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`

Este checkpoint formaliza el cierre de P4 como la primera familia de Roadmap
4.x tratada internamente. No implementa otra familia, no activa un gate externo
y no convierte una lectura local en readiness de produccion.

## Identidad y alcance

- Mision: `ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE`
- Baseline de entrada: `2969ed469ed482968b4db4deac7b35a855f635e2`
- Rama autorizada: `main`
- Familia: `P4_CATALOG_DOMAIN_READS`
- Rutas: exactamente `7`, todas `GET`
- Estado: `INTERNAL_REMEDIATION_COMPLETE_EXTERNAL_EXPOSURE_DEFAULT_DENIED`
- Proxima familia: se selecciona en una estacion posterior y queda
  `SELECTED_NOT_STARTED`
- Macro-Mission 04: `NOT_STARTED`

## Rutas cerradas

1. `GET /api/catalogs/domain-creation`
2. `GET /api/catalogs/roles`
3. `GET /api/catalogs/specializations`
4. `GET /api/domains/list`
5. `GET /api/domains/{domain_id}/profile-catalog`
6. `GET /api/domains/{domain_id}/agent-presets`
7. `GET /api/domains/{domain_id}/agent-presets/match`

Las capacidades vigentes son `global_catalogs.read`, `tenant_domains.read` y
`tenant_agent_presets.read_sanitized`. El permiso del agente profesional sigue
siendo distinto de la identidad humana y no se usa como sustituto de ella.

## Evidencia de cierre

La evidencia autoritativa se conserva en los checkpoints de Macro 02 y 02.1.
Los guards existentes cubren, sin agregar una auditoria adversarial nueva:

- resolver fail-closed con `503` cuando no existe fuente configurada;
- principal, audiencia y capabilities canonicos;
- rechazo de identidad falsificada por headers, cookies o query params;
- aislamiento tenant, no enumeracion y ausencia de contaminacion entre requests;
- sanitizacion recursiva de presets, incluyendo `decision_criteria` y `avoid`;
- compatibilidad del payload existente, sin payload v2;
- ausencia de provider real, store productivo de tenants y cambios de CORS.

## Estado dual de gates

| Gate | Readiness interna | Exposicion externa | Accion vigente |
| --- | --- | --- | --- |
| G01 Identity | `READY_PROVIDER_INDEPENDENT_CONTRACT` | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G02 Authentication | `READY_FAIL_CLOSED_RESOLUTION` | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G03 Authorization | `ENFORCED_APPROVED_POLICY` | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G04 Tenant isolation | `VERIFIED_CONTROLLED_PRINCIPALS` | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G05 CORS | `PRESERVED_LOCALHOST_ONLY` | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G06 Ingress/hosting | no requerido en tests internos | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G13 Providers/secrets | no requerido | bloqueada | `REMAIN_DISABLED_OR_CONTAINED` |
| G18 External consumers | consumidores locales protegidos | inventario externo pendiente | `REMAIN_DISABLED_OR_CONTAINED` |
| G19 Payload contract | protegido y probado | compatibilidad externa pendiente | `REMAIN_DISABLED_OR_CONTAINED` |

Ningun gate externo se cierra por inferencia. `active_now` permanece `false`.

## Limites preservados

No se modificaron ni se autorizan en esta estacion `api.py`,
`core/p4_request_access.py`, otras superficies de producto, HTML, CSS,
JavaScript contractual, i18n, runtime, execution, providers, integrations,
stores, secretos, CORS, hosting, P0, P1, Matriz P3, widgets contract-aware ni
Request Draft Panel.

`ROADMAP_4X_MACRO_03_P4_INTERNAL_FAMILY_CLOSURE_CHECKPOINT_PUBLISHED`
