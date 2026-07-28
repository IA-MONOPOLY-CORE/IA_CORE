# Secrets and Sensitive Data Policy — Security Layer

Estado: `SECRETS_POLICY_READY`

Readiness: `ready_for_secrets_policy_e2e_checkpoint`

Proximo paso: `PROMPT 3.23.1 — Checkpoint E2E de política de secretos`

## Definicion

Un secreto es cualquier valor que permita acceso, autenticación, sesión, firma, conexión o escalamiento de privilegio: api keys, access tokens, refresh tokens, bearer tokens, passwords, private keys, ssh keys, jwt, cookies, session ids, database urls, connection strings, webhook secrets, OAuth client secrets, env vars sensibles, configs secretas y credential files.

Un dato sensible es información personal, comercial, financiera, legal, sanitaria, de ubicación, prompts internos, system prompts, developer prompts, agent instructions, tool results sensibles, datos de pantalla o documentos sensibles.

## Que NO hace todavia

Esta política no lee secretos reales, no escribe secretos reales, no imprime secretos, no muestra valores de env, no hace scan operativo de `.env` con valores, no crea secret manager real, no crea vault, no se conecta a servicios externos, no persiste datos sensibles, no activa runtime, no activa tools, no activa API/UI, no activa UI-TARS/Hermes/n8n/Home Assistant y no activa stores.

## Redaction-first

La regla principal es redaction-first: si un texto o mapping recibido explícitamente parece contener un secreto o dato sensible, el resultado debe redacted o blocked antes de llegar a prompts, logs, outputs, memory, reports, read models o audit trails visibles.

No se leen secretos reales porque esta fase es contract-only. No se imprimen secretos porque los logs no deben mostrar raw secret values. No se guardan secretos en prompts/logs/outputs/memory/read models porque `secret` y `restricted` nunca deben aparecer crudos.

## Categorias

```txt
api_key
access_token
refresh_token
bearer_token
password
private_key
ssh_key
jwt
cookie
session_id
database_url
connection_string
webhook_secret
oauth_client_secret
env_var_sensitive
config_secret
credential_file
personal_data
business_sensitive_data
financial_data
legal_data
health_data
location_data
internal_prompt
system_prompt
developer_prompt
agent_instruction
tool_result_sensitive
screen_sensitive_data
document_sensitive_data
```

## Niveles de sensibilidad

```txt
public
internal
confidential
secret
restricted
```

`secret` y `restricted` nunca deben aparecer crudos en prompts, logs, outputs, memoria, reports, read models ni audit trails visibles.

## Acciones permitidas

```txt
classify_secret_candidate
redact_text
redact_mapping_values
detect_placeholder_only
build_secret_policy_decision
validate_secret_policy_decision
serialize_secret_policy_decision
generate_secret_risk_report
```

## Acciones prohibidas

```txt
read_real_secret
write_real_secret
print_secret_value
log_secret_value
persist_secret_value
inject_secret_into_prompt
send_secret_to_external_service
store_secret_in_memory
store_secret_in_history
store_secret_in_read_model
expose_secret_in_output
scan_env_values_operationally
connect_secret_manager
decrypt_secret
rotate_secret_real
```

## Decision policy

- `allowed`: solo para `public` o `internal` sin patrón sensible.
- `redacted`: para secret candidates que pueden representarse como placeholder seguro.
- `blocked`: para `memory`, `env` o `config` con `secret`/`restricted`, y para persistencia sensible.
- `invalid`: para schema inválido, sensibilidad inválida, exposición contradictoria, raw value no redactado u OBLITERATUS como source/integration.

`public` puede `allowed` si no contiene patrón sensible. `internal` puede `allowed` o `redacted` según contexto. `confidential` debe `redacted` salvo política explícita futura. `secret` debe `redacted` o `blocked`. `restricted` debe `blocked` o `redacted` con `allowed_to_display=False`.

## Redaction

```txt
[REDACTED]
[REDACTED:API_KEY]
[REDACTED:TOKEN]
[REDACTED:PASSWORD]
[REDACTED:PRIVATE_KEY]
[REDACTED:DATABASE_URL]
[REDACTED:SECRET]
[REDACTED:PERSONAL_DATA]
```

Los tests deben usar valores fake. Los docs no deben incluir claves reales. Los logs no deben mostrar raw_value. La serialización no debe incluir raw secret values.

## Relaciones

Con Agent Permission Contract: aunque un agente tenga capabilities seguras, esta política define qué datos ningún agente puede exponer.

Con Security Surface Audit: consume el riesgo de secret leakage, prompt secret injection, output secret leaks, memory poisoning y datos sensibles en documents/screens/tool results.

Con prompt injection futura: prepara la regla de no inyectar secretos en prompts y de redactar inputs antes de evaluar instrucciones.

Con UI-TARS/Hermes/n8n/Home Assistant: cualquier dato sensible que estas integraciones futuras pudieran ver debe estar gobernado por redaction, approval, sandbox y audit. Siguen no activas.

Con OBLITERATUS: OBLITERATUS is not an IA_CORE integration, no es dependency, adapter, capability, secret source ni roadmap operativo.

## Boundaries explicitas

```txt
contract-only
security-simulated
non-operational
redaction-first
no secret manager runtime
no secret reads
no secret writes
no environment scanning with values
no raw secret logging
no prompt secret injection
no output secret leaks
no memory persistence
no external access
no API
no UI
no UI-TARS runtime
no Hermes runtime
no n8n real workflows
no Home Assistant real actions
Market Catalog remains planned_not_active
Business Composition Layer remains future/non-operational
OBLITERATUS is not an IA_CORE integration
```

## PROMPT 3.23.1 result

La politica de secretos fue validada por checkpoint E2E full.

Resultado: `SECRETS_POLICY_FULL_E2E_PASSED`.

Veredicto: `SECRETS_POLICY_CHAIN_READY`.

Readiness: `ready_for_prompt_injection_defense_planning`.

Proximo paso: `PROMPT 3.24 - Defensa contra prompt injection`.

La validacion confirma classification, redaction, policy decisions y serializacion sin exponer raw secret values, sin secret reads reales, sin secret writes reales, sin env scan con valores, sin secret manager runtime, sin memory persistence, sin external access, sin API/UI, sin writes/stores operativos y sin integraciones futuras activas.

## PROMPT 3.24 result

`PROMPT 3.24 - Defensa contra prompt injection` impide que contenido no confiable use secretos, fuerce exposicion, pida exfiltracion o convierta valores sensibles en instrucciones ejecutables.

Resultado: `PROMPT_INJECTION_DEFENSE_READY`.

E2E: `PROMPT_INJECTION_DEFENSE_E2E_PASSED`.

Readiness: `ready_for_prompt_injection_defense_e2e_checkpoint`.

Proximo paso: `PROMPT 3.24.1 - Checkpoint E2E de defensa contra prompt injection`.

## PROMPT 3.25 result

Sandbox boundary no habilita lectura de secretos reales ni acceso a env, host, filesystem, network, tools o stores.

Resultado: `SANDBOX_BOUNDARY_READY`.

E2E: `SANDBOX_BOUNDARY_E2E_PASSED`.

Readiness: `ready_for_sandbox_boundary_e2e_checkpoint`.

Proximo paso: `PROMPT 3.25.1 - Checkpoint E2E de sandbox boundary`.

## PROMPT 3.26 result

Tool Boundary Policy impide secret tools reales y acceso a secretos por herramientas. Una redaccion o clasificacion de secreto no habilita lectura de env, secret manager, archivos reales ni adapters.

Estado: `TOOL_BOUNDARY_READY`.
Readiness: `ready_for_tool_boundary_e2e_checkpoint`.
