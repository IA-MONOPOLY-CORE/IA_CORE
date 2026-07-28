from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PROMPT_INJECTION_DEFENSE_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_prompt_injection_defense_e2e_checkpoint_exists_and_contains_chain():
    text = _text()
    assert DOC.exists()
    for phrase in [
        "PROMPT_INJECTION_DEFENSE_E2E_PASSED",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.23 — Política de secretos y datos sensibles",
        "PROMPT 3.23.1 — Checkpoint E2E de política de secretos",
        "PROMPT 3.24 — Defensa contra prompt injection",
        "PROMPT 3.24.1 — Checkpoint E2E de defensa contra prompt injection",
    ]:
        assert phrase in text


def test_prompt_injection_defense_e2e_checkpoint_contains_statuses():
    text = _text()
    for phrase in [
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "AGENT_PERMISSION_CONTRACT_READY",
        "SECRETS_POLICY_READY",
        "SECRETS_POLICY_FULL_E2E_PASSED",
        "PROMPT_INJECTION_DEFENSE_READY",
        "ready_for_prompt_injection_defense_planning",
        "ready_for_prompt_injection_defense_e2e_checkpoint",
    ]:
        assert phrase in text


def test_prompt_injection_defense_e2e_checkpoint_contains_boundaries():
    text = _text()
    for phrase in [
        "contract-only",
        "security-simulated",
        "non-operational",
        "input-isolation-first",
        "instruction-hierarchy-aware",
        "no runtime execution",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no untrusted instruction execution",
        "no tool result instruction execution",
        "no document instruction execution",
        "no screen instruction execution",
        "no web instruction execution",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_prompt_injection_defense_e2e_checkpoint_has_no_contradictory_states():
    text = _text()
    for forbidden in [
        "runtime_enabled = true",
        "tool_execution_enabled = true",
        "model_invocation_enabled = true",
        "memory_persistence_enabled = true",
        "external_access_enabled = true",
        "api_enabled = true",
        "ui_enabled = true",
        "untrusted_instruction_execution_enabled = true",
        "tool_result_instruction_execution_enabled = true",
        "document_instruction_execution_enabled = true",
        "screen_instruction_execution_enabled = true",
        "web_instruction_execution_enabled = true",
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
