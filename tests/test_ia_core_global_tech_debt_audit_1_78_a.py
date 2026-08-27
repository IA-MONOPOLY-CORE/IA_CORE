from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "IA_CORE_GLOBAL_TECH_DEBT_AUDIT_1_78_A.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_global_tech_debt_audit_document_exists():
    assert DOC.exists()


def test_global_tech_debt_audit_contains_required_contract_markers():
    text = read_doc()

    required = [
        "628ab75",
        "Restore point remoto vigente: `628ab75`",
        "Global Technical Debt Audit",
        "Scope global",
        "No-scope",
        "Metodologia",
        "Estado de tests",
        "Inventario global de deuda",
        "debt_id",
        "REUSE",
        "UPDATE",
        "ISOLATE",
        "DELETE",
        "DO_NOT_TOUCH",
        "P0_BLOCKER",
        "P1_HIGH",
        "P2_MEDIUM",
        "P3_LOW",
        "P4_HISTORICAL",
        "SAFE_TO_DELETE_CANDIDATE",
        "SAFE_TO_UPDATE_CANDIDATE",
        "REUSE_AS_GUARDRAIL_CANDIDATE",
        "LEGACY_ARCHIVE_CANDIDATE",
        "NEEDS_HUMAN_REVIEW",
        "Clasificacion por area",
        "Clasificacion por destino",
        "Clasificacion por severidad",
        "Clasificacion por riesgo",
        "Plan maestro de limpieza",
        "Reglas de limpieza posterior",
        "Riesgos",
        "PROMPT IA_CORE 1.78.B - Clasificar y priorizar deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT IA_CORE 1.78.C - Limpiar primera tanda de deuda tecnica segura IA_CORE contract-aware sin runtime/no-execution",
        "PROMPT IA_CORE 1.78.D - Checkpoint limpieza deuda tecnica global IA_CORE contract-aware sin runtime/no-execution",
    ]

    for marker in required:
        assert marker in text


def test_global_tech_debt_audit_declares_boundaries():
    text = read_doc()

    required = [
        "no se borro nada",
        "No se modifico UI activa",
        "no se toco backend/runtime/endpoints/CI",
        "no se avanzo a 1.79",
    ]

    for marker in required:
        assert marker in text
