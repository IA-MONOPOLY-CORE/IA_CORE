# Roadmap 3.0 N5 - Agent, Preset, Paper, Team and Activation Graph

## Gate

`ROADMAP_3_0_N5_AGENT_DOMAIN_GRAPH_PASSED`

## Inventory

| Surface | Evidence | Current classification |
| --- | --- | --- |
| Python agent modules | `agents/modules/analyst.py`, `assistant.py`, `critic.py`, `echo.py`, `optimizer.py` plus module package files | definitions discoverable by `agents.loader`; instantiation is a legacy manager concern |
| Agent base/runners | `agents/base.py`, `role_agent.py`, `llm_runner.py`, `runtime_json_agent.py`, `lightweight_assistant_runner.py` | callable code present; provider reachability depends on manager/supervisor path |
| JSON agents | `domains/demo_generico/agents/config/*.json` | definitions carry provider/model metadata; not evidence of a running agent |
| Lotería JSON config | `domains/loteria/agents/config/` | directory is present but no active JSON agent files were found |
| Domain preset | `domains/loteria/agent_presets.json` | one placeholder; `activo: false`, no provider/model, explicitly non-operational |
| Paper source | `core/agent_paper_schema.py`, `core/paper_seed_materializer.py`, runtime JSON loader | schema/materializer/loader present; no active Lotería paper file found |
| Team source | `core/sandbox_team_materializer.py`, `core/sandbox_team_schema.py`, read models | declarative sandbox team capability; no materialized active team found |
| Activation contract | `core/active_contract.py`, `core/active_executor.py` | requires a complete artifact chain and approval; external/runtime flags remain blocked |

## Activation graph

`profile_catalog -> agent_presets -> paper_seed -> sandbox_agent -> sandbox_team
-> active_contract -> approval/activation gate -> active executor`.

The first five nodes are artifact definitions/materialization surfaces. The
team materializer rejects operational paths and marks teams non-operational. The
active contract requires profile/preset/paper/agent/team coherence and rejects
missing members. The active executor additionally blocks runtime/external access
unless an explicit, separately approved activation contract exists. No such
activation was performed in this audit.

## What “agent exists” means here

An agent may exist as a Python class, loader-discoverable `AgentSpec`, JSON
definition, sandbox artifact, or active contract target. These are different
states. A source definition is not an active process, a provider session, a
team, or an operational permission grant. Roadmap 3.0 records the state and
caller edges rather than promoting any definition.

## Paper, preset and team findings

- A preset is currently an inactive compatibility placeholder in Lotería. Its
  embedded `paper_seed` is documentary input, not a live paper.
- Paper schemas and materializers can produce sandbox artifacts, but generation
  and regeneration are write-capable functions and were not called.
- Team templates and team materializers are declarative and sandbox-scoped;
  there is no evidence of team coordination runtime in this audit.
- Legacy domain evolution contains paper-regeneration code. This is a callable
  source path, not proof that regeneration ran.

## N5 conclusion

Definitions and activation machinery are present, but current evidence does not
support an active agent/team/paper runtime in the dedicated contract plane. The
legacy supervisor can load agents and connect them to providers when started;
that route remains part of the security/activation frontier.

