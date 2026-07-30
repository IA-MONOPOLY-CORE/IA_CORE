from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "RUNTIME_ACTIVATION_GATE_E2E_CHECKPOINT.md"


def test_runtime_activation_gate_e2e_checkpoint_exists():
    assert DOC.exists()


def test_runtime_activation_gate_e2e_checkpoint_contains_chain_and_next_step():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "RUNTIME_ACTIVATION_GATE_E2E_PASSED",
        "PROMPT 3.21 - Auditoria de superficie de ataque de IA_CORE",
        "PROMPT 3.22 - Contrato de permisos por agente",
        "PROMPT 3.23 - Politica de secretos y datos sensibles",
        "PROMPT 3.24 - Defensa contra prompt injection",
        "PROMPT 3.25 - Sandbox boundary y aislamiento pre-runtime",
        "PROMPT 3.26 - Tool boundary y politica de herramientas pre-runtime",
        "PROMPT 3.27 - Model invocation boundary pre-runtime",
        "PROMPT 3.28 - Context boundary y politica de contexto pre-runtime",
        "PROMPT 3.29 - Output boundary y politica de salidas pre-runtime",
        "PROMPT 3.29.1 - Checkpoint E2E de output boundary",
        "PROMPT 3.30 - Runtime activation gate pre-runtime",
        "PROMPT 3.30.1 - Checkpoint E2E de runtime activation gate",
    ]:
        assert phrase in text


def test_runtime_activation_gate_e2e_checkpoint_contains_statuses_and_boundaries():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED", "AGENT_PERMISSION_CONTRACT_READY", "SECRETS_POLICY_READY",
        "PROMPT_INJECTION_DEFENSE_READY", "SANDBOX_BOUNDARY_READY", "TOOL_BOUNDARY_READY",
        "MODEL_INVOCATION_BOUNDARY_READY", "CONTEXT_BOUNDARY_READY", "OUTPUT_BOUNDARY_READY",
        "OUTPUT_BOUNDARY_FULL_E2E_PASSED", "RUNTIME_ACTIVATION_GATE_READY",
        "ready_for_runtime_activation_gate_planning", "ready_for_runtime_activation_gate_e2e_checkpoint",
        "contract-only", "security-simulated", "non-operational", "pre-runtime", "activation-gate-only",
        "deny-by-default", "boundary-aware", "permission-aware", "secrets-aware", "prompt-injection-aware",
        "sandbox-aware", "tool-boundary-aware", "model-invocation-aware", "context-boundary-aware",
        "output-boundary-aware", "no runtime activation", "no runtime execution", "no runtime runner",
        "no scheduler", "no worker", "no queue", "no orchestrator", "no executor", "no dispatcher",
        "no background jobs", "no autonomy", "no continuous loop", "no tool execution", "no model invocation",
        "no context injection", "no output delivery", "no output publishing", "no writes reales",
        "no stores operativos", "no memory persistence", "no external access", "no API calls", "no network",
        "no browser", "no command execution", "no shell", "no process spawn", "no real filesystem reads",
        "no real filesystem writes", "no env access", "no secret access", "no UI control", "no device control",
        "no UI-TARS runtime", "no Hermes runtime", "no n8n real workflows", "no Home Assistant real actions",
        "Market Catalog remains planned_not_active", "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_runtime_activation_gate_e2e_checkpoint_has_no_contradictory_states():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "runtime_activation_enabled = true", "runtime_execution_enabled = true", "runtime_runner_enabled = true",
        "runtime_scheduler_enabled = true", "runtime_worker_enabled = true", "runtime_queue_enabled = true",
        "runtime_orchestrator_enabled = true", "runtime_executor_enabled = true", "runtime_dispatcher_enabled = true",
        "runtime_background_jobs_enabled = true", "runtime_autonomy_enabled = true", "runtime_continuous_loop_enabled = true",
        "runtime_tool_execution_enabled = true", "runtime_model_invocation_enabled = true",
        "runtime_context_injection_enabled = true", "runtime_output_delivery_enabled = true",
        "runtime_output_publishing_enabled = true", "runtime_writes_enabled = true", "runtime_stores_enabled = true",
        "runtime_memory_persistence_enabled = true", "runtime_network_enabled = true", "runtime_api_enabled = true",
        "runtime_secret_access_enabled = true", "ui_tars_enabled = true", "hermes_enabled = true", "n8n_enabled = true",
        "home_assistant_enabled = true", "market_catalog_active", "business_composition_enabled = true", "gate_open",
        "operations_enabled", "ready_for_runtime`", "runtime_open", "runtime_active",
    ]:
        assert phrase not in text
