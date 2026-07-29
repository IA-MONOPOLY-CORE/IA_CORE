from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MODEL_INVOCATION_BOUNDARY_E2E_CHECKPOINT.md"


def test_model_invocation_boundary_e2e_checkpoint_exists():
    assert DOC.exists()


def test_model_invocation_boundary_e2e_checkpoint_contains_chain_and_next_step():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "MODEL_INVOCATION_BOUNDARY_E2E_PASSED",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
        "PROMPT 3.24 — Defensa contra prompt injection",
        "PROMPT 3.25 — Sandbox boundary y aislamiento pre-runtime",
        "PROMPT 3.26 — Tool boundary y política de herramientas pre-runtime",
        "PROMPT 3.26.1 — Checkpoint E2E de tool boundary",
        "PROMPT 3.27 — Model invocation boundary pre-runtime",
        "PROMPT 3.27.1 — Checkpoint E2E de model invocation boundary",
    ]:
        assert phrase in text


def test_model_invocation_boundary_e2e_checkpoint_contains_required_statuses():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "AGENT_PERMISSION_CONTRACT_READY",
        "SECRETS_POLICY_READY",
        "PROMPT_INJECTION_DEFENSE_READY",
        "SANDBOX_BOUNDARY_READY",
        "TOOL_BOUNDARY_READY",
        "TOOL_BOUNDARY_FULL_E2E_PASSED",
        "MODEL_INVOCATION_BOUNDARY_READY",
        "ready_for_model_invocation_boundary_planning",
        "ready_for_model_invocation_boundary_e2e_checkpoint",
    ]:
        assert phrase in text


def test_model_invocation_boundary_e2e_checkpoint_confirms_boundaries():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "contract-only",
        "security-simulated",
        "non-operational",
        "pre-runtime",
        "model-request-only",
        "deny-by-default",
        "permission-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "sandbox-aware",
        "tool-boundary-aware",
        "no real model invocation",
        "no model router",
        "no model executor",
        "no inference runner",
        "no provider calls",
        "no local provider calls",
        "no remote provider calls",
        "no streaming",
        "no context expansion",
        "no raw prompt logging",
        "no raw output logging",
        "no tool execution",
        "no tool adapters",
        "no tool calls",
        "no API calls",
        "no network",
        "no browser",
        "no command execution",
        "no shell",
        "no process spawn",
        "no real filesystem reads",
        "no real filesystem writes",
        "no env access",
        "no secret access",
        "no memory persistence",
        "no writes reales",
        "no stores operativos",
        "no UI control",
        "no device control",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_model_invocation_boundary_e2e_checkpoint_has_no_contradictory_states():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "runtime_enabled = true",
        "model_invocation_enabled = true",
        "model_router_enabled = true",
        "model_executor_enabled = true",
        "inference_runner_enabled = true",
        "provider_calls_enabled = true",
        "local_provider_enabled = true",
        "remote_provider_enabled = true",
        "streaming_enabled = true",
        "context_expansion_enabled = true",
        "raw_prompt_logging_enabled = true",
        "raw_output_logging_enabled = true",
        "network_enabled = true",
        "api_enabled = true",
        "tool_execution_enabled = true",
        "secret_access_enabled = true",
        "memory_persistence_enabled = true",
        "writes_enabled = true",
        "external_access_enabled = true",
        "ui_tars_enabled = true",
        "hermes_enabled = true",
        "n8n_enabled = true",
        "home_assistant_enabled = true",
        "market_catalog_active",
        "business_composition_enabled = true",
        "gate_open",
        "operations_enabled",
        "ready_for_runtime",
    ]:
        assert phrase not in text
