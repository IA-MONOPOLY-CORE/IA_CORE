from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ROADMAP_2_1_METHOD_APPLIED_AUDIT.md"


def test_method_audit_gate_and_required_continuity_rule_exist():
    text = DOC.read_text(encoding="utf-8")
    assert "ROADMAP_2_1_METHOD_APPLIED_AUDIT_PASSED" in text
    assert "METHOD-019" in text
    assert "REPORT_FINAL_AUTOCONTENIDO_PARA_CONTINUIDAD" in text
    assert "ACTIVE_CANONICAL" in text
    assert "ACTIVE_EVOLVED" in text
    assert "CURRENT_CONTRACT_WINS" in text


def test_method_audit_has_all_required_columns_and_twenty_two_rules():
    text = DOC.read_text(encoding="utf-8")
    header = "| rule_id | rule | classification | source | evidence | current status | mandatory future | gokv relation | update needed |"
    assert header in text
    assert text.count("| METHOD-") == 22
    assert "ACTIVE_CANONICAL`: 17" in text
    assert "ACTIVE_EVOLVED`: 5" in text


def test_method_audit_does_not_authorize_product_or_runtime_changes():
    text = DOC.read_text(encoding="utf-8")
    assert "does not rewrite the global method book" in text
    assert "do not authorize product or runtime work" in text
