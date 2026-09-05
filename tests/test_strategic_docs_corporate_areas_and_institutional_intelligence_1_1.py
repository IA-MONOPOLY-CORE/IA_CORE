"""Contract checks for STRATEGIC DOCS 1.1; no runtime validation."""

from pathlib import Path
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AREAS_NAME = "FUTURE_CORPORATE_AREAS_AND_SUBAREAS_MODEL.md"
INTELLIGENCE_NAME = "FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md"
AREAS = DOCS / AREAS_NAME
INTELLIGENCE = DOCS / INTELLIGENCE_NAME
INDEX = DOCS / "FUTURE_PLATFORM_EXTENSION_INDEX.md"
README = ROOT / "README.md"

ALLOWED_DIFF = {
    "README.md",
    f"docs/{AREAS_NAME}",
    f"docs/{INTELLIGENCE_NAME}",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md",
    "docs/FUTURE_ENTERPRISE_MODULES_AND_RISK_MODEL.md",
    "docs/FUTURE_ADAPTIVE_BUSINESS_INTELLIGENCE_MODEL.md",
    "tests/test_strategic_docs_corporate_areas_and_institutional_intelligence_1_1.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def changed_paths() -> set[str]:
    tracked = set(filter(None, git("diff", "--name-only", "HEAD").splitlines()))
    untracked = set(
        filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())
    )
    return tracked | untracked


def assert_markers(path: Path, markers: list[str]) -> None:
    text = normalized(read(path))
    missing = [marker for marker in markers if normalized(marker) not in text]
    assert not missing, f"{path.name}: missing {missing}"


def test_new_strategic_documents_exist():
    assert AREAS.is_file()
    assert INTELLIGENCE.is_file()


def test_extension_index_references_both_future_documents():
    assert_markers(
        INDEX,
        [
            AREAS_NAME,
            INTELLIGENCE_NAME,
            "documentos estratégicos futuros",
            "STRATEGIC_CORPORATE_AREAS_AND_INSTITUTIONAL_INTELLIGENCE_DOCUMENTED",
        ],
    )


def test_readme_records_strategic_docs_1_1_briefly():
    assert_markers(
        README,
        [
            "STRATEGIC DOCS 1.1",
            "taxonomía futura de áreas/subáreas corporativas",
            "paneles activables por necesidad real",
            "capa futura de inteligencia institucional",
            "no implementado",
        ],
    )


def test_corporate_hierarchy_is_complete_and_ordered():
    hierarchy_block = read(AREAS).split(
        "La jerarquía conceptual futura es:", 1
    )[1].split("Las áreas y subáreas son estructura empresarial.", 1)[0]
    text = normalized(hierarchy_block)
    hierarchy = [
        "Empresa",
        "área madre",
        "subárea",
        "sector/equipo",
        "responsable",
        "colaboradores",
        "agentes",
        "herramientas/módulos",
        "permisos",
        "reportes",
        "evidencia",
    ]
    positions = [text.index(normalized(marker)) for marker in hierarchy]
    assert positions == sorted(positions)


def test_panel_activation_and_progressive_visibility_rules_are_recorded():
    assert_markers(
        AREAS,
        [
            "cada área y subárea corporativa pueda convertirse en panel operativo propio",
            "Todo merece control, chequeo e interacción",
            "no todo merece complejidad visible desde el primer día",
            "La ausencia visual no equivale a ausencia arquitectónica",
            "Un usuario no debe ver paneles que no necesita",
        ],
    )


def test_finance_is_a_mother_area_with_required_subareas():
    assert_markers(
        AREAS,
        [
            "Finanzas / Administración financiera",
            "Finanzas debe ser tratada como área madre",
            "Tesorería",
            "Contabilidad",
            "Fiscalidad / Impuestos",
            "Facturación",
            "Cuentas a pagar",
            "Cuentas a cobrar",
        ],
    )


def test_minimum_corporate_area_taxonomy_is_present():
    assert_markers(
        AREAS,
        [
            "Dirección / Gobierno ejecutivo",
            "Finanzas / Administración financiera",
            "Administración",
            "Marketing",
            "Ventas",
            "Atención al cliente / Customer Success",
            "Operaciones",
            "Recursos Humanos",
            "TI / Soporte interno",
            "Ciberseguridad",
            "Legal / Compliance",
            "Compras / Procurement",
            "Proveedores",
            "Logística / Supply Chain",
            "Auditoría interna",
            "Riesgo empresarial",
            "Calidad / Mejora continua",
            "Gobierno de datos",
            "Gobierno corporativo",
            "Producto / I+D",
            "Continuidad del negocio",
            "Formación / Capacitación interna",
            "Relaciones institucionales",
            "Reporting ejecutivo / BI",
        ],
    )


def test_future_area_states_are_complete():
    assert_markers(
        AREAS,
        [
            "future_only",
            "suggested",
            "enabled",
            "disabled",
            "grouped",
            "merged",
            "split",
            "renamed",
            "requires_configuration",
            "requires_permissions",
            "requires_panel",
            "panel_available",
            "panel_hidden",
            "not_implemented",
        ],
    )


def test_institutional_intelligence_definition_and_scope_are_present():
    assert_markers(
        INTELLIGENCE,
        [
            "inteligencia institucional",
            "aprender de empresas reales",
            "detectar patrones organizacionales",
            "entender qué estructuras funcionan",
            "anticipar problemas",
            "recomendar mejoras",
            "criterio empresarial propio",
            "capa de criterio acumulado",
            "gobierno humano",
        ],
    )


def test_intelligence_layers_are_distinguished():
    assert_markers(
        INTELLIGENCE,
        [
            "Adaptive Business Intelligence adapta análisis",
            "contexto de un negocio específico",
            "Institutional Intelligence Layer",
            "criterio organizacional y empresarial",
            "aprendizaje institucional futuro gobernado y anonimizado",
        ],
    )


def test_institutional_governance_and_tenant_boundaries_are_explicit():
    assert_markers(
        INTELLIGENCE,
        [
            "privacidad",
            "permisos",
            "contratos",
            "anonimización",
            "aislamiento tenant",
            "No usar datos crudos de un cliente para otro",
            "No mezclar tenants",
            "No exponer información privada",
            "No vender datos de clientes",
            "No tomar decisiones sensibles sin humano autorizado",
            "evidencia, métricas, trazabilidad o límites explícitos",
        ],
    )


def test_new_documents_remain_future_only_and_avoid_forbidden_claims():
    forbidden = [
        "ya funciona",
        "está operativo",
        "está activo",
        "ejecuta automáticamente",
        "opera capital real",
        "conecta bancos reales",
        "usa datos de clientes para otros clientes",
    ]
    for path in [AREAS, INTELLIGENCE]:
        text = normalized(read(path))
        for marker in [
            "futuro",
            "no implementado",
            "sin runtime",
            "sin execution",
            "sin endpoints",
            "sin integraciones reales",
            "sin conectores reales",
            "sin credenciales",
        ]:
            assert normalized(marker) in text
        assert not [phrase for phrase in forbidden if normalized(phrase) in text]


def test_legacy_models_connect_to_the_new_taxonomy_without_claiming_runtime():
    expectations = {
        "FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md": [
            AREAS_NAME,
            "empresa, área, subárea, sector/equipo",
            "contrato, la escala, el permiso y la necesidad",
        ],
        "FUTURE_ENTERPRISE_MODULES_AND_RISK_MODEL.md": [
            AREAS_NAME,
            "no reemplazan la estructura organizacional",
        ],
        "FUTURE_ADAPTIVE_BUSINESS_INTELLIGENCE_MODEL.md": [
            INTELLIGENCE_NAME,
            "adaptación contextual por negocio",
            "aprendizaje institucional futuro gobernado y anonimizado",
        ],
    }
    for name, markers in expectations.items():
        assert_markers(DOCS / name, markers)


def test_diff_is_limited_to_documentary_scope_and_protected_paths_are_untouched():
    assert changed_paths() <= ALLOWED_DIFF
    for protected in [
        "core/api.py",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "backend",
        "core",
        "runtime",
        "integrations",
        ".env",
    ]:
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
