from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "TOOL_BOUNDARY_E2E_CHECKPOINT.md"


def test_tool_boundary_e2e_checkpoint_exists():
    assert DOC.exists()


def test_tool_boundary_e2e_checkpoint_contains_chain_and_next_step():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "TOOL_BOUNDARY_E2E_PASSED",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
        "PROMPT 3.24 — Defensa contra prompt injection",
        "PROMPT 3.25 — Sandbox boundary y aislamiento pre-runtime",
        "PROMPT 3.25.1 — Checkpoint E2E de sandbox boundary",
        "PROMPT 3.26 — Tool boundary y política de herramientas pre-runtime",
        "PROMPT 3.26.1 — Checkpoint E2E de tool boundary",
    ]:
        assert phrase in text


def test_tool_boundary_e2e_checkpoint_contains_required_statuses():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "AGENT_PERMISSION_CONTRACT_READY",
        "SECRETS_POLICY_READY",
        "PROMPT_INJECTION_DEFENSE_READY",
        "SANDBOX_BOUNDARY_READY",
        "SANDBOX_BOUNDARY_FULL_E2E_PASSED",
        "TOOL_BOUNDARY_READY",
        "ready_for_tool_boundary_planning",
        "ready_for_tool_boundary_e2e_checkpoint",
    ]:
        assert phrase in text


def test_tool_boundary_e2e_checkpoint_confirms_boundaries():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "contract-only",
        "security-simulated",
        "non-operational",
        "pre-runtime",
        "tool-request-only",
        "deny-by-default",
        "permission-aware",
        "sandbox-aware",
        "secrets-aware",
        "prompt-injection-aware",
        "no real tool execution",
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


def test_tool_boundary_e2e_checkpoint_has_no_contradictory_states():
    text = DOC.read_text(encoding="utf-8")
    for phrase in [
        "runtime_enabled = true",
        "tool_execution_enabled = true",
        "tool_adapters_enabled = true",
        "tool_calls_enabled = true",
        "network_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
        "secret_access_enabled = true",
        "filesystem_enabled = true",
        "command_execution_enabled = true",
        "memory_persistence_enabled = true",
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
