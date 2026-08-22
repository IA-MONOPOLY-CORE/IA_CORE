from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md"
README = ROOT / "ui" / "web" / "README.md"
INDEX = ROOT / "ui" / "web" / "index.html"
STYLES = ROOT / "ui" / "web" / "styles.css"
WIDGETS = ROOT / "ui" / "web" / "backend-contract-widgets.js"
ADMIN = ROOT / "ui" / "web" / "admin-panels.js"
INTERACTIONS = ROOT / "ui" / "web" / "console-interactions.js"
DOMAINS = ROOT / "ui" / "web" / "domains.js"
I18N = ROOT / "ui" / "web" / "i18n_es.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_audit_1_20_document_exists_and_references_base_plan():
    text = read(DOC)

    for marker in [
        "19e68c32",
        "docs/UI_UX_NEXT_BLOCK_PLAN_1_19.md",
        "Frontend Incongruence Audit",
        "UI_UX_FRONTEND_INCONGRUENCE_AUDIT_COMPLETED",
        "FRONTEND_STRUCTURE_INVENTORY_COMPLETED",
        "UI_READY_FOR_FRONTEND_INCONGRUENCE_HARDENING",
    ]:
        assert marker in text


def test_audit_1_20_contains_required_sections_and_inventories():
    text = read(DOC)

    for marker in [
        "Fase 1 - Inventario De Archivos Frontend",
        "Fase 2 - Auditoria HTML / Estructura Activa",
        "Fase 3 - Auditoria CSS / Estilos",
        "Fase 4 - Auditoria JavaScript / Comportamiento Local",
        "Fase 5 - Auditoria Microcopy / Lenguaje Visible",
        "Fase 6 - Inventario Naming / Identificadores",
        "Fase 7 - Inventario Fetches / Rutas / Endpoints",
        "Fase 8 - Inventario Storage / Estado Local",
        "Fase 9 - Inventario Tests / Cobertura",
        "Fase 10 - Inventario Docs / README",
        "Fase 11 - Mapa Frontend Vivo / Legacy / Muerto",
        "Fase 12 - Matriz P0/P1/P2/P3",
        "Fase 13 - Plan Quirurgico Para 1.21",
        "Falsos Positivos Registrados",
    ]:
        assert marker in text


def test_audit_1_20_covers_all_frontend_files_and_cross_references():
    text = read(DOC)

    for marker in [
        "ui/web/index.html",
        "ui/web/styles.css",
        "ui/web/backend-contract-widgets.js",
        "ui/web/admin-panels.js",
        "ui/web/console-interactions.js",
        "ui/web/domains.js",
        "ui/web/i18n_es.json",
        "ui/web/README.md",
        "tests/test_api_admin_panels.py",
        "tests/test_backend_internal_future_ui_contract_plan_8_7.py",
        "tests/test_backend_internal_ui_payloads_7_6.py",
    ]:
        assert marker in text


def test_audit_1_20_records_residual_incongruences_and_priorities():
    text = read(DOC)

    for marker in [
        "debate-panel",
        "btn-debate",
        "orchestration-task",
        "orchestration-status",
        "logs-runtime",
        ".active",
        "activeAgentProfileCatalog",
        "status.running",
        "active_provider",
        "block: 'start'",
        "P1-001",
        "P1-002",
        "P1-003",
        "P2-001",
        "P3-001",
    ]:
        assert marker in text

    for state in [
        "vivo_contract_aware",
        "vivo_ambiguo",
        "vivo_heredado",
        "vivo_mal_nombrado",
        "no_visible_referenciado",
        "muerto_probable",
        "duplicado",
        "historico_test_fixture",
        "falso_positivo",
        "requiere_hardening_1_21",
        "posponer",
    ]:
        assert state in text


def test_audit_1_20_does_not_recommend_runtime_endpoints_or_dependencies():
    text = read(DOC).lower()

    for marker in [
        "no recomienda endpoints",
        "no recomienda dependencias nuevas",
        "no recomienda runtime/execution",
        "no endpoint publico nuevo",
        "no api/router nuevo",
        "no hash routing operativo",
        "no runtime",
        "no execution",
        "no dispatch real",
        "no controlled execution",
        "no dependencias nuevas",
    ]:
        assert marker in text


def test_active_ui_identity_and_no_legacy_visual_active_are_confirmed():
    text = read(DOC)
    ui = "\n".join(
        read(path)
        for path in [INDEX, STYLES, WIDGETS, ADMIN, INTERACTIONS, DOMAINS, I18N, README]
    )

    assert "IA_CORE permanece como identidad visual activa" in text
    assert "No hay SAAOP" in text
    assert "IA_CORE" in ui

    for legacy in [
        "SAAOP",
        "S.A.A.O.P",
        "Loteria",
        "Lotería",
        "lottery",
        "Tactical HUD",
        "U-Score",
        "CAZADOR",
        "ESPEJO",
        "combinatoria",
    ]:
        assert legacy.lower() not in ui.lower()


def test_active_frontend_routes_and_storage_match_audit_boundaries():
    frontend = "\n".join(read(path) for path in [INDEX, WIDGETS, ADMIN, INTERACTIONS, DOMAINS])
    audit = read(DOC)

    for route in ["/api/debate/start", "/api/dispatch", "/api/runtime", "/api/execution"]:
        assert route not in frontend
        assert route in audit

    for marker in ["location.hash", "hashchange", "history.pushState", "history.replaceState"]:
        assert marker not in frontend

    assert "fetch(" not in read(WIDGETS)
    assert "fetch(" not in read(INTERACTIONS)

    for storage_key in [
        "ia_core_selected",
        "ia_core_logos",
        "ia_core_skin",
        "ia_core_brand",
        "brand_input",
        "ia_core_wallpaper",
        "ia_core_active_domain",
    ]:
        assert storage_key in audit


def test_contractual_tokens_and_previous_blocks_are_preserved_in_audit():
    text = read(DOC)

    for marker in [
        "backend_internal_ui_payload.v1",
        "backend_internal_ui_request.v1",
        "internal_exposure_registry",
        "internal_request_validation",
        "internal_dispatcher_no_runtime",
        "internal_confirmation_gate",
        "internal_response_adapter",
        "allowed_actions",
        "forbidden_actions",
        "blocked_capabilities",
        "warnings",
        "errors",
        "validation",
        "flags",
        "readiness",
        "status",
        "service_kind",
        "schema_version",
        "summary/detail/raw-safe",
        "paneles de detalle 1.7",
        "navegacion interna 1.8",
        "sistema de componentes 1.9",
        "responsive/accessibility hardening 1.13",
        "admin boundary hardening 1.17",
    ]:
        assert marker in text


def test_readme_registers_audit_1_20_and_next_hardening():
    readme = read(README)

    for marker in [
        "Auditoria frontend incongruence 1.20",
        "docs/UI_UX_FRONTEND_INCONGRUENCE_AUDIT_1_20.md",
        "Frontend Incongruence Audit",
        "1.20 no corrige",
        "no-runtime/no-execution",
        "sin endpoints ni dependencias",
        "PROMPT UI/UX 1.21 - Endurecer o documentar incongruencias frontend segun auditoria IA_CORE contract-aware sin runtime/no-execution",
    ]:
        assert marker in readme


def test_next_prompt_exact_is_recorded():
    text = read(DOC)

    assert (
        "PROMPT UI/UX 1.21 - Endurecer o documentar incongruencias frontend segun auditoria IA_CORE contract-aware sin runtime/no-execution"
        in text
    )
