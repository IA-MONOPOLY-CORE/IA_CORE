from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "SANDBOX_BOUNDARY_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_sandbox_boundary_e2e_checkpoint_exists_and_contains_chain():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "SANDBOX_BOUNDARY_E2E_PASSED",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
        "PROMPT 3.24 — Defensa contra prompt injection",
        "PROMPT 3.24.1 — Checkpoint E2E de defensa contra prompt injection",
        "PROMPT 3.25 — Sandbox boundary y aislamiento pre-runtime",
        "PROMPT 3.25.1 — Checkpoint E2E de sandbox boundary",
    ]:
        assert phrase in text


def test_sandbox_boundary_e2e_checkpoint_contains_statuses():
    text = _text()
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "AGENT_PERMISSION_CONTRACT_READY",
        "SECRETS_POLICY_READY",
        "PROMPT_INJECTION_DEFENSE_READY",
        "PROMPT_INJECTION_DEFENSE_FULL_E2E_PASSED",
        "SANDBOX_BOUNDARY_READY",
        "ready_for_sandbox_boundary_planning",
        "ready_for_sandbox_boundary_e2e_checkpoint",
    ]:
        assert phrase in text


def test_sandbox_boundary_e2e_checkpoint_contains_boundaries():
    text = _text()
    for phrase in [
        "contract-only",
        "security-simulated",
        "non-operational",
        "pre-runtime",
        "isolation-first",
        "deny-by-default",
        "no command execution",
        "no shell",
        "no process spawn",
        "no real filesystem reads",
        "no real filesystem writes",
        "no env access",
        "no secret access",
        "no network",
        "no browser",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no writes reales",
        "no stores operativos",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_sandbox_boundary_e2e_checkpoint_has_no_contradictory_states():
    text = _text()
    for forbidden in [
        "runtime_enabled = true",
        "command_execution_enabled = true",
        "filesystem_read_enabled = true",
        "filesystem_write_enabled = true",
        "network_enabled = true",
        "secret_access_enabled = true",
        "tool_execution_enabled = true",
        "model_invocation_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
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
        assert forbidden not in text
