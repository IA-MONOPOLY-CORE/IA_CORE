# Roadmap 3.0 N4 - Provider, Network and Credential Graph

## Gate

`ROADMAP_3_0_N4_PROVIDER_NETWORK_CREDENTIAL_GRAPH_PASSED`

## Provider inventory

| Provider/family | Source | Network behavior | Credential/config evidence | Classification |
| --- | --- | --- | --- | --- |
| NVIDIA | `providers/nvidia_provider.py`, `config.py` | `requests.request` to `https://integrate.api.nvidia.com/v1` with Bearer header | `NVIDIA_API_KEY` environment variable; timeout config is 60/120 seconds depending layer | real network-capable legacy adapter, not called here |
| Ollama | `providers/ollama_provider.py`, `config.py` | `urllib.request.urlopen` to `http://localhost:11434/api/tags`, `/api/chat`, `/api/generate` | local base URL; safe-mode timeout 120 or normal timeout 180; max retries 2 | real local-network-capable adapter, not called here |
| OpenAI | `providers/openai_provider.py` | placeholder; no network implementation observed | registry-imported provider class; no call evidence | definition/placeholder |
| Registry/router | `providers/registry.py`, `core/hybrid/router.py` | selects provider adapters and routing | provider/model metadata | callable through legacy supervisor if started |
| Helper/connectivity | `core/herramientas.py`, `core/hybrid/connectivity.py` | requests helper and socket connectivity check (`1.1.1.1:53`) | helper/provider configuration | network-capable auxiliary path |

Conservative static count: **9 network-capable references** in non-test Python
source. This is a reference count, not a provider count and not a runtime call
count.

## Credential and network boundary

Known variable/config names, with values intentionally omitted:

- `NVIDIA_API_KEY`
- `NVIDIA_BASE_URL`
- `NVIDIA_TIMEOUT`
- `OLLAMA_BASE_URL`
- `OLLAMA_TIMEOUT`
- `OLLAMA_MAX_RETRIES`
- provider/model fields carried by agent and settings configuration

No secret value was read or printed by this audit. The API settings route accepts
an `api_key` input and writes configuration, so the credential boundary is not
only an environment-variable concern.

## Reachability and resilience

- `Supervisor.start` constructs the provider registry and agent manager. Legacy
  orchestration can request provider completion through agent runners.
- NVIDIA uses an HTTP request with a bearer credential and a timeout. The
  historical test evidence contains a 410/availability observation; no new
  request was made here.
- Ollama retries selected 5xx/429/URL/timeout failures with backoff and exposes
  local API calls. This is implementation evidence, not proof that Ollama is
  running.
- No provider reachability, DNS, socket, HTTP, model, or credential test was
  performed. The audit deliberately avoids network and provider invocation.

## N4 conclusion

There is a real path to a provider in the legacy application source, especially
NVIDIA and local Ollama. The path is not the disabled 3.x runtime plane. The
combination of wildcard CORS, absent route auth evidence, secret-bearing
settings, and provider-capable chat makes security/activation boundary review
the natural next backend block.

