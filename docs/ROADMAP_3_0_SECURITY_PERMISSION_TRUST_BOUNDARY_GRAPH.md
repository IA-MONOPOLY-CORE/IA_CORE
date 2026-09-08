# Roadmap 3.0 N6 - Security, Permission and Trust Boundary Graph

## Gate

`ROADMAP_3_0_N6_SECURITY_TRUST_GRAPH_PASSED`

## Boundary inventory

| Boundary | Evidence | Result |
| --- | --- | --- |
| HTTP authentication | static search of `api.py` and route declarations | no FastAPI auth dependency, OAuth/JWT, API-key dependency, or equivalent route guard found |
| HTTP authorization | route handlers and mutation endpoints | no route-level role/permission enforcement evidence found |
| CORS | `api.py` middleware | wildcard origins, methods and headers |
| Input validation | Pydantic request models, path/domain ID validation | present in parts of API; validation is not authorization |
| Agent permission contract | `core/agent_permission_contract.py` | explicit permission model and deny-by-default/decision structures exist at contract level |
| Runtime activation | `core/runtime_activation_gate.py`, `core/attempt_factory.py` | operational flags false; external/model/tool/network/process/secret access denied by default |
| Internal confirmation | `core/backend_internal_confirmation_gate.py` | confirmation is required for controlled service execution |
| Sandbox filesystem | materializers and domain validators | operational roots rejected; sandbox path constraints exist |
| Secret handling | `api.py` settings, `NVIDIA_API_KEY` config | secret-bearing input and config write candidate exist; no HTTP auth proof around them |
| Process/network primitives | `subprocess`, requests/urllib/socket references | present in source; not executed or exploited |

## Permission interpretation

The contract-plane security modules are meaningful safety evidence: they can
deny activation, restrict capabilities, require confirmation and reject unsafe
paths. They do not retroactively secure every legacy API route. The legacy API
is an independent trust boundary and currently lacks sufficient static evidence
of authentication/authz for exposed mutation/provider paths.

## Dangerous primitives

Thirteen non-test primitive calls were inventoried, including `shutil.rmtree`,
`subprocess.run` for a hardware probe and `subprocess.check_output` in a
benchmark script. Their presence was recorded only. No command, delete,
network, provider, secret, or sandbox operation was invoked by Roadmap 3.0.

## Activation decision

Security/auth is **sufficient for the dedicated contract plane to remain
disabled and deny-by-default**, but **not sufficient evidence for activating the
legacy API as a trusted operational boundary**. This is a finding for the next
read-only security/activation audit, not a request to implement remediation now.

## N6 conclusion

The repository has local guardrails but no demonstrated global trust boundary.
The gap is not a missing UI affordance; it is the coexistence of a provider and
write-capable legacy API with absent route auth evidence beside a safer,
contractual internal plane.

