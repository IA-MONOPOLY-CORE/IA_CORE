# Roadmap 4.x Macro-Mission 04.3

## P1-A consumer compatibility

| Consumer | Before | After | Failure handling |
|---|---|---|---|
| connection poller in `ui/web/index.html` | `/api/status`, indirectly depended on provider array in a retry helper | `/api/status` minimal contract only | HTTP failure remains a disconnected state; no provider retry |
| Overview in `ui/web/admin-panels.js` | status plus runtime/provider/agent/tool/memory fields | minimal version/view/scope/status/liveness/readiness/exposure markers | fixed sanitized unavailable text |
| Hybrid in `ui/web/admin-panels.js` | `/api/status?full=true` and raw router/provider/model fields | same alias, generic detailed fields only | fixed capability-gated unavailable text; no raw error |
| Providers panel in `ui/web/index.html` | status-backed provider enumeration and health retries | explicit non-enumeration message | no fetch, no retry CTA, no inferred provider state |

No Python consumer of `/api/status` was found. The existing provider diagnostic
helper remains available to its separate model-recommendation route and was not
changed by this mission. The backend-contract widgets do not consume status and
were not modified.

The browser surface was not launched because no approved local browser tooling
was available in this execution context. Node syntax checking, static consumer
assertions, API handler tests and full backend validation are the recorded UI
fallback. This is `TOOLING_UNAVAILABLE`, not a claim of visual approval.
