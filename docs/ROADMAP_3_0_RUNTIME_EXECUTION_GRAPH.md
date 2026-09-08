# Roadmap 3.0 N3 - Runtime, Execution, Queue and Worker Graph

## Gate

`ROADMAP_3_0_N3_RUNTIME_EXECUTION_GRAPH_PASSED`

## Graph result

The codebase contains a large runtime/execution vocabulary, but the dedicated
3.x activation surface is disabled or contract-only. The static distinction is:

| Layer | Evidence | Finding |
| --- | --- | --- |
| Runtime activation | `core/runtime_activation_gate.py` | all runtime, execution, runner, scheduler, worker, queue, dispatcher, background-job, model/tool/network/filesystem/process/secret flags are false |
| Attempt creation | `core/attempt_factory.py` | factory/runtime/store/lifecycle/result/projection/scheduler/worker/queue/model/tool/memory/external/API/UI writes are false |
| Execution runner | `core/execution_runner.py` and dry-run contracts | prepares and reports declarative dry-run/abort/rollback; no operational runner evidence |
| Active executor | `core/active_executor.py` | callable symbol exists, but blocks when runtime/execution/external access is disabled and requires candidate, contract and approval evidence |
| Internal dispatcher | `core/backend_internal_dispatcher.py` | contractual internal dispatch; defaults deny execution and does not dispatch agents/models/tools/integrations |
| Queue/worker/scheduler | runtime contract and gate modules | names and contracts exist; no enabled operational loop found |
| Legacy supervisor | `core/supervisor.py` | application startup can load agents/providers and legacy orchestration can run when API is started |

## Real paths

### Dedicated backend-internal path

`request -> validation/contract -> activation gate -> attempt/runner/dispatcher`
is present as a designed graph, but it terminates in disabled, dry-run, denied,
or confirmation-required states. It is not an enabled operational runtime.

### Legacy application path

`API startup -> Supervisor.start -> AgentManager/ProviderRegistry/Memory/Tools
-> POST /api/chat or debate -> orchestrate_async -> agent runner/provider ->
memory/orchestration persistence` is present in source. It becomes reachable if
the server is deliberately started and its dependencies are available. This
audit did not start it, invoke it, or test it.

## Queue, worker, scheduler and dispatcher assessment

- No operational queue consumption, worker loop, scheduler trigger, or
  background execution was started or observed.
- The presence of names/classes/contracts is classified as `CODE_PRESENT_INACTIVE`
  unless a caller and enabled flag are both evidenced.
- The legacy `BackgroundTasks` usage on debate/validation endpoints is an API
  scheduling primitive, not proof of the dedicated backend worker/scheduler
  plane.

## N3 conclusion

There is a real legacy application execution path and a disabled/contractual
dedicated execution plane. The distinction matters: saying “no execution exists”
would be false, while saying “the 3.x runtime is active” would also be false.

