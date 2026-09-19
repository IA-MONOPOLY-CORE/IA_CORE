from __future__ import annotations

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
METHOD_324 = ROOT / "docs/METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING.md"
METHOD_325 = ROOT / "docs/METHOD_SANTI_3_2_5_EXECUTABLE_CLOSURE_AUTHORITY_ENGINEERING.md"
GATE = ROOT / "scripts/validate_mission_closure.py"


def test_method_325_adds_executable_authority_without_product_frontier():
    text = METHOD_325.read_text(encoding="utf-8")
    for marker in (
        "AGENT_PROPOSES_CLOSURE",
        "EVIDENCE_SUPPORTS_CLOSURE",
        "EXECUTABLE_GATE_ADJUDICATES_CLOSURE",
        "OPERATOR_ACCEPTS_OR_REJECTS_NEXT_STEP",
        "AGENT_NARRATIVE_HAS_ZERO_CLOSURE_AUTHORITY",
        "EXECUTABLE_CLOSURE_GATE_IS_THE_ONLY_CLOSURE_AUTHORITY",
        "NO_SELF_DECLARED_PASS",
        "NO_REPORT_ONLY_CLOSURE",
        "NO_EVIDENCE_BY_OMISSION",
        "NO_FINAL_HEAD_WITH_UNVALIDATED_EXECUTABLE_DIFF",
        "NO_SECOND_REQUEST_FOR_MANDATORY_INFORMATION",
        "CLOSURE_GATE_APPLIES_TO_ALL_FUTURE_GOVERNED_MISSIONS",
        "METHOD_UPDATE_IS_NOT_PRODUCT_CAPABILITY",
        "METHOD_UPDATE_IS_NOT_RUNTIME",
        "METHOD_UPDATE_IS_NOT_AUTHORITY_SOURCE_FOR_BUSINESS_ACTIONS",
        "METHOD_UPDATE_IS_NOT_GOKV_PROMOTION",
    ):
        assert marker in text
    assert "product feature" not in text.lower()
    assert GATE.exists()


def test_method_324_is_unchanged_and_325_is_additive():
    baseline = subprocess.check_output(
        ["git", "show", "4a9b0613538294f477dcc4631c3c5ee61a8cb34c:docs/METHOD_SANTI_3_2_4_CANONICAL_EVIDENCE_CLOSURE_ENGINEERING.md"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    assert METHOD_324.read_text(encoding="utf-8") == baseline
    assert "3.2.4" in METHOD_325.read_text(encoding="utf-8")


def test_gate_cli_has_only_contractual_operations_and_no_bypass_flags():
    text = GATE.read_text(encoding="utf-8")
    for operation in ("validate-readiness", "validate-prelock", "render-postpublish"):
        assert operation in text
    for forbidden in ("--force", "--skip", "--allow-incomplete", "--ignore-failure", "--trust-agent"):
        assert forbidden in text
    assert "subprocess" in text
