# Roadmap 4.x Macro-Mission 04.1

## Agent model fit and fallback contract

## Constitutional split

`MODEL_AGNOSTIC_PLATFORM`

`MODEL_FIT_BOUND_AGENT`

IA_CORE remains independent of a provider as a platform. An agent is a stable
identity and contract whose model assignment is a deliberate, evidence-bound
fit for its duty. Changing the assignment does not create a new agent when the
identity and contract remain the same.

## Required assignment fields

A future agent assignment record must be able to declare:

- capabilities required by the duty;
- primary model and provider policy;
- alternative models and provider policies;
- operational fallback;
- difficult-case escalation model;
- incompatible or insufficient model conditions;
- hardware limits and placement;
- privacy and data boundary;
- latency, cost and context requirements;
- expected quality and reliability;
- evaluation corpus, benchmark, threshold and validity scope;
- evidence and reevaluation triggers.

The repository already contains model policy catalog entries, profile
recommendations, hardware/provider concepts and fallback fields. Those are
partial contracts and are not proof that every model is installed, available,
compatible or recommended. No provider is queried by this mission.

## Fit decision

`EXCELLENCE_MUST_BE_MEASURED_NOT_DECLARED`

The platform must not call an agent "best" without a benchmark, criterion,
evidence and validity scope. A smaller model is acceptable only when required
quality is preserved. A larger model is not sufficient evidence of fitness.
Privacy, hardware, latency, cost and human review can disqualify a technically
capable model.

## Fallback boundary

Fallback is a bounded alternative assignment, not an implicit permission or a
silent change of task. It must preserve the agent identity, task scope,
privacy class, evidence requirements and human approval boundary. If no
compatible fallback exists, the result is a stop or review request. A fallback
must never disclose a secret, cross a tenant, activate runtime or turn an
informational result into execution.
