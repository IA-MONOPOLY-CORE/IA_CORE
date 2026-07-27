from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AGENT_PERMISSION_CONTRACT_E2E_CHECKPOINT.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_agent_permission_contract_e2e_checkpoint_exists():
    assert DOC.exists()


def test_agent_permission_contract_e2e_checkpoint_contains_chain():
    text = _text()
    for phrase in [
        "AGENT_PERMISSION_CONTRACT_E2E_PASSED",
        "PROMPT 3.20 — Planificación de IA_CORE Security Layer",
        "PROMPT 3.21 — Auditoría de superficie de ataque de IA_CORE",
        "PROMPT 3.22 — Contrato de permisos por agente",
        "PROMPT 3.22.1 — Checkpoint E2E de permisos por agente",
    ]:
        assert phrase in text


def test_agent_permission_contract_e2e_checkpoint_contains_statuses():
    text = _text()
    for phrase in [
        "IA_CORE_SECURITY_LAYER_PLAN_READY",
        "IA_CORE_SECURITY_SURFACE_AUDIT_COMPLETED",
        "SECURITY_SURFACE_REQUIRES_PERMISSION_CONTRACT",
        "AGENT_PERMISSION_CONTRACT_READY",
        "ready_for_agent_permission_contract",
        "ready_for_agent_permission_e2e_checkpoint",
    ]:
        assert phrase in text


def test_agent_permission_contract_e2e_checkpoint_contains_boundaries():
    text = _text()
    for phrase in [
        "contract-only",
        "security-simulated",
        "non-operational",
        "default deny",
        "no runtime execution",
        "no tool execution",
        "no model invocation",
        "no memory persistence",
        "no external access",
        "no API",
        "no UI",
        "no UI-TARS runtime",
        "no Hermes runtime",
        "no n8n real workflows",
        "no Home Assistant real actions",
        "Market Catalog remains planned_not_active",
        "Business Composition Layer remains future/non-operational",
        "OBLITERATUS is not an IA_CORE integration",
    ]:
        assert phrase in text


def test_agent_permission_contract_e2e_checkpoint_has_no_contradictory_states():
    text = _text()
    for forbidden in [
        "runtime_enabled = true",
        "security_layer_enabled = true",
        "tools_enabled = true",
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
        assert forbidden not in text
