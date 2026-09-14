# Roadmap 4.x Macro-Mission 02.1 - P4 Post-Boundary E2E Checkpoint

## Resultado

`ROADMAP_4X_MACRO_02_1_P4_POST_BOUNDARY_E2E_ADVERSARIAL_CHECKPOINT_PASSED_AFTER_EVIDENCE_BOUND_REPAIR`

La frontera P4 queda validada end to end para las siete rutas GET ya
existentes. El resultado B corresponde a una reparacion de producto real,
reproducible y contenida: el primer replay de la nueva suite encontro siete
fallos; la reparacion fue limitada a `core/p4_request_access.py` y al wiring
P4 de `api.py`, con pruebas rojas y verdes separadas. No se agregaron rutas,
capabilities, estados, providers, stores ni exposicion externa.

## Identidad de la mision

- Baseline: `05674020671e98557262e26df8c380da631138b2`.
- Rama: `main`.
- Inicio instrumentado: `2026-09-13T21:30:56.4026519-03:00`.
- `VALIDATION_BASIS_HEAD`: `d0fe3b789249101b9acf526db47b89ee4d797715`.
- Commit documental: `EXTERNAL_REPORT_REFERENCE`.
- Verificacion post-fetch: `EXTERNAL_REPORT_REFERENCE`.
- Regla de publicacion: `publication_metadata_must_not_chase_its_own_head`.

La corrida final de Level A sobre la base indicada paso `7003 passed, 6
skipped, 6 warnings` en `1534.39 s` segun pytest (`1538.76 s` de duracion
instrumentada). Los cuatro segundos de diferencia corresponden al wrapper y
su overhead de proceso, no a una diferencia de resultado.

El replay acotado de Level B sobre los documentos nuevos paso `210 passed, 6
warnings` en `16.84 s`; el parseo final incluyo `269` archivos JSON.

## Flujo E2E reconstruido

Cada request sigue esta cadena verificable:

`HTTP request -> resolve_p4_principal -> require_p4_access -> exact capability /
tenant / domain decision -> registry reader -> output sanitizer -> HTTP JSON`

1. FastAPI resuelve primero `resolve_p4_principal`. Su comportamiento por
   defecto es `503 P4_ACCESS_RESOLVER_NOT_CONFIGURED`; headers, cookies y query
   params no son una fuente de identidad.
2. `validate_p4_principal` exige la forma controlada, textos canonicos,
   audiencia exacta, sets `frozenset` y tenant/domain IDs validos.
3. `evaluate_p4_access` comprueba autenticacion, audiencia y la capability
   exacta necesaria. Para las rutas tenant exige tenant y membresia explicita.
4. La autorizacion de dominio se decide antes del reader del registry. La lista
   se filtra por tenant e IDs autorizados; las rutas directas requieren el ID
   explicito.
5. Los presets se proyectan con allowlist y validacion estructural antes de
   serializar. `match` usa la misma sanitizacion que la coleccion.

## Matriz de las siete rutas

| Ruta | Capability exacta | Condiciones adicionales | Salida |
| --- | --- | --- | --- |
| `GET /api/catalogs/domain-creation` | `global_catalogs.read` | principal autenticado y audiencia `ia-core-private-beta` | catalogo global existente |
| `GET /api/catalogs/roles` | `global_catalogs.read` | principal autenticado y audiencia exacta | roles/arquetipos profesionales |
| `GET /api/catalogs/specializations` | `global_catalogs.read` | principal autenticado y audiencia exacta | especializaciones globales |
| `GET /api/domains/list` | `tenant_domains.read` | tenant valido y set de dominios autorizado; filtrado por tenant | lista filtrada y shape existente |
| `GET /api/domains/{domain_id}/profile-catalog` | `tenant_domains.read` | tenant valido e ID explicitamente autorizado | catalogo de perfiles existente |
| `GET /api/domains/{domain_id}/agent-presets` | `tenant_agent_presets.read_sanitized` | tenant valido, ID autorizado y proyeccion sanitizada | presets safe |
| `GET /api/domains/{domain_id}/agent-presets/match` | `tenant_agent_presets.read_sanitized` | tenant valido, ID autorizado, match exacto y proyeccion sanitizada | preset safe o match-not-found |

La doctrina aplicada es `NECESSARY_AND_SUFFICIENT_ROLE_PERMISSIONS`: cada ruta
tiene una capability necesaria y suficiente para su superficie, sin matching
por prefijo, wildcard, casing, espacios, similitud Unicode ni capability
sustitutiva. `core/agent_permission_contract.py` continua separado; los roles
profesionales del catalogo no son roles humanos de autorizacion.

## Fail-closed y no enumeracion

| Condicion | Status | Codigo |
| --- | ---: | --- |
| resolver no configurado | 503 | `P4_ACCESS_RESOLVER_NOT_CONFIGURED` |
| principal ausente, no autenticado o invalido | 401 | `P4_PRINCIPAL_INVALID` |
| audiencia incorrecta | 401 | `P4_AUDIENCE_INVALID` |
| capability necesaria ausente | 403 | `P4_CAPABILITY_REQUIRED` |
| resource ID invalido o traversal-shaped | 400 | `P4_RESOURCE_IDENTIFIER_INVALID` |
| dominio inexistente, no autorizado o cross-tenant | 404 | `P4_DOMAIN_NOT_AUTHORIZED` |
| set autorizado vacio, con tenant valido | 200 | shape de lista existente y coleccion vacia |

Los errores no revelan dominio, tenant, sujeto, membresia, capabilities,
registry, paths internos, configuracion ni secretos. El fixture de ausencia de
dominio, dominio existente no autorizado y dominio de otro tenant produjo el
mismo `404` y el mismo cuerpo generico. La decision de dominio no autorizado
ocurre antes de invocar el reader del registry.

## Identidad adversarial y tenants

La suite nueva cubre headers de usuario/tenant/capability, query params,
cookies, sujeto vacio, tenant vacio, audiencia vacia, tipos incorrectos,
espacios, casing, duplicados, wildcard, confusable Unicode y representaciones
manipuladas de IDs. Los inputs controlados por el cliente no sustituyen el
resolver ni conceden autoridad.

Los fixtures usan Tenant A (`A1`, `A2`) y Tenant B (`B1`):

- Principal A solo ve A1.
- A2 no aparece y no es accesible directamente.
- B1 nunca aparece ni es accesible para A.
- Principal sin tenant no lee datos empresariales.
- Principal con tenant sin membresias explicitas recibe el rechazo generico;
  el set autorizado vacio valido conserva la lista vacia `200`.
- La secuencia A -> B alternada confirma que la identidad no persiste entre
  requests y que el filtro de una request no contamina la siguiente.
- Se eligio prueba secuencial determinista. No se agrego concurrencia porque
  `app.dependency_overrides` de FastAPI es estado global de test; una prueba
  concurrente sobre esa superficie introduciria flakiness del harness en vez
  de evidencia de la frontera productiva.

## Reparacion de producto y rollback

El replay inicial de la nueva suite, antes del cambio productivo, dio `7
failed, 12 passed, 6 warnings` en `13.23 s`:

- la lista sin tenant concedia `200` en vez de rechazar;
- capabilities y authorized IDs con tipos de lista eran aceptados;
- un dominio autorizado pero ausente podia diferenciarse por el error de
  recurso;
- valores anidados contaminados sobrevivian al sanitizer.

La reparacion en `fc3e5952eab6f7ff1f4cdda89fd03990f375920b`:

- exige `frozenset` canonico para capabilities y IDs autorizados;
- rechaza falta de tenant o membresia para superficies tenant sin tocar la
  semantica del set vacio autorizado;
- normaliza el error de recurso ausente de las tres rutas de dominio a
  `P4_DOMAIN_NOT_AUTHORIZED`;
- valida texto, listas de texto y `orden` antes de exponerlos.

El rollback documentado es revertir exclusivamente ese commit de producto;
no requiere tocar rutas ajenas, registry, consumidores ni artefactos privados.
La suite adversarial y Macro 02 paso despues con `37 passed, 6 warnings` en
`11.80 s`; no se requirio rollback.

## Criterios de cierre

- P4 fail-closed: PASS.
- Identidad no falsificable por inputs del cliente: PASS.
- Capabilities necesarias, suficientes y exactas: PASS.
- Aislamiento tenant y no enumeracion: PASS.
- No contaminacion entre requests: PASS.
- Sanitizacion semantica y estructural: PASS.
- Payloads exitosos compatibles: PASS.
- CORS preservado y sin exposicion externa: PASS.
- Suite completa y replays historicos: PASS.

No se modificaron HTML, CSS, JavaScript contractual, i18n, rutas ajenas,
runtime, execution, providers, integrations, secretos, stores productivos,
P0, P1, matriz P3, widgets contract-aware ni Request Draft Panel. No hubo
llamadas externas ni activacion de provider. Macro-Mission 03 no fue iniciada.

`ROADMAP_4X_MACRO_02_1_P4_POST_BOUNDARY_E2E_ADVERSARIAL_CHECKPOINT_PASSED_AFTER_EVIDENCE_BOUND_REPAIR`
