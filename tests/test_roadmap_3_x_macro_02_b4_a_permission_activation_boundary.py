from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "ROADMAP_3_X_MACRO_02_B4_A_PERMISSION_ACTIVATION_BOUNDARY.md"


CONTRACT_FILES = [
    "core/agent_permission_contract.py",
    "core/capability_policy_schema.py",
    "core/backend_internal_request_envelope.py",
    "core/backend_internal_dispatcher.py",
    "core/backend_internal_confirmation_gate.py",
    "core/runtime_activation_gate.py",
    "core/operational_readiness_gate.py",
    "core/execution_contract.py",
    "core/execution_lifecycle_contract.py",
]


def test_b4_a_static_chain_is_present_and_route_coverage_stays_unproven():
    doc = DOC.read_text(encoding="utf-8")

    for relative in CONTRACT_FILES:
        assert (ROOT / relative).is_file(), relative
        assert f"`{relative}`" in doc
    for marker in (
        "contract-only",
        "route coverage unresolved",
        "runtime disabled",
        "no execution",
        "No endpoint, integration, provider, network, secret, payload, UI",
        "a callable symbol is not permission",
        "readiness is not activation",
    ):
        assert marker in doc


def test_b4_a_does_not_claim_operational_activation():
    doc = DOC.read_text(encoding="utf-8")

    assert "ROADMAP_3X_MACRO_02_B4_A_PERMISSION_ACTIVATION_BOUNDARY_MATERIALIZED" in doc
    assert "No permission is granted" in doc
    assert "No route is reclassified as covered" in doc
