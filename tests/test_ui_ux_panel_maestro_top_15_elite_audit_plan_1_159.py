from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_TOP_15_ELITE_AUDIT_PLAN_1_159.md"
RESTORE_POINT_158 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_1_158.md"
DECISION_157 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_RESTORE_POINT_DECISION_1_157.md"
CHECKPOINT_156 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_CHECKPOINT_1_156.md"
LEDGER_155 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_CAPABILITIES_LEDGER_1_155.md"
CONTRACT_151 = ROOT / "docs" / "UI_UX_PANEL_MAESTRO_VOCABULARY_AFFORDANCES_CONTRACT_1_151.md"
INDEX = ROOT / "ui" / "web" / "index.html"
README = ROOT / "README.md"
UI_README = ROOT / "ui" / "web" / "README.md"

PROTECTED_PATHS = [
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "api.py",
    "core",
    "domains",
    "providers",
    "tools",
    "scripts",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_markers(text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    assert not missing


def test_document_exists_with_state_base_and_objective():
    assert DOC.exists()
    text = read(DOC)

    assert_markers(
        text,
        [
            "UI/UX Panel Maestro TOP 15 Elite Audit Plan 1.159",
            "07a15d8",
            "HEAD == origin/main",
            "main` up to date",
            "Working tree limpio",
            "Matriz publicada",
            "Vocabulario/affordances publicado",
            "Ledger publicado",
            "TOP 15 no auditado",
            "TOP 15 no implementado",
            "UI/UX 1.x no cerrado globalmente",
            "Planificar auditoria TOP 15",
            "sin auditar ni implementar",
            "restore point remoto publicado",
            "tres bloques recomendados publicados",
            "matriz",
            "contrato 1.151",
            "ledger 1.155",
            "FSC",
            "DEFER_FINALIZATION",
        ],
    )


def test_purpose_elite_definition_and_non_elite_filters():
    text = read(DOC)

    assert_markers(
        text,
        [
            "TOP 15 sirve para elevar el estandar final",
            "TOP 15 no es lista de features obligatorias",
            "TOP 15 no es roadmap inflado",
            "TOP 15 no es implementacion",
            "TOP 15 no es benchmark copiado",
            "TOP 15 no es excusa para abrir runtime/backend",
            "valor estructural real",
            "cosmetica",
            "Mejora verdad del sistema",
            "Mejora legibilidad contractual",
            "Mejora orientacion del operador",
            "Reduce ambiguedad",
            "Reduce riesgo de affordance fantasma",
            "Mejora trazabilidad",
            "Mejora consistencia visible/documental",
            "Mejora preparacion para futuro User Panel",
            "Mejora capacidad de auditoria",
            "Mejora claridad de estados",
            "Mejora separacion presente/bloqueado/futuro",
            "Mejora experiencia de revision humana",
            "Mejora percepcion profesional sin maquillaje",
            "Mejora mantenibilidad",
            "Mejora cierre sin generar deuda innecesaria",
            "Que NO es elite",
            "Brillo visual sin dato real",
            "Animaciones sin contrato",
            "Botones sin accion permitida",
            "Dashboards falsos",
            "Metricas falsas",
            "Runtime disfrazado",
            "Promesas operativas",
            "Copiar UI externa",
            "Instalar dependencias por estetica",
            "Abrir backend sin necesidad",
            "Convertir futuro en presente",
            "Tapar deuda con copy lindo",
            "Cerrar globalmente sin prueba",
        ],
    )


def test_sources_references_categories_scoring_and_thresholds():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Fuentes internas obligatorias",
            "Matriz de cierre UI/UX 1.x",
            "Contrato de vocabulario/affordances 1.151",
            "Ledger de capacidades 1.155",
            "Checkpoint ledger 1.156",
            "Restore point publication 1.158",
            "Auditoria global post-density 1.140",
            "Auditoria candidatos estandar tope de gama 1.141",
            "Revision de candidatos 1.142",
            "README/cursor",
            "UI actual solo lectura",
            "JS actual solo lectura",
            "Tests relevantes",
            "referencias externas",
            "inspiracion conceptual",
            "benchmarking futuro",
            "No copiar componentes",
            "No copiar estructura visual",
            "No instalar librerias",
            "No importar diseno de terceros",
            "No convertir IA_CORE en clon",
            "fuente de verdad es el repo",
            "APPLIES_NOW_DOCUMENTATION_ONLY",
            "APPLIES_NOW_TEST_ONLY",
            "APPLIES_NOW_STATIC_UI_ONLY",
            "ALREADY_COVERED",
            "FUTURE_REQUIRES_UI_PHASE",
            "FUTURE_REQUIRES_BACKEND",
            "FUTURE_REQUIRES_USER_PANEL",
            "FUTURE_REQUIRES_RUNTIME",
            "BLOCKED_BY_NO_RUNTIME",
            "BLOCKED_BY_NO_EXECUTION",
            "BLOCKED_BY_LEDGER",
            "BLOCKED_BY_VOCABULARY_CONTRACT",
            "OVERBUILT_FOR_1X",
            "DISCARD_NOT_ALIGNED",
            "NEEDS_OPERATOR_DECISION",
            "VISUAL_CLARITY",
            "CONTRACT_CLARITY",
            "STATE_CLARITY",
            "NAVIGATION_CLARITY",
            "HUMAN_REVIEW_CLARITY",
            "TRACEABILITY",
            "DENSITY_BALANCE",
            "DEBT_VISIBILITY",
            "FUTURE_PREPARATION",
            "SAFETY_BOUNDARY",
            "NO_VALUE_ADDED",
            "RISKY_AFFORDANCE",
            "FALSE_OPERATIONAL_SIGNAL",
            "structural_value",
            "truthfulness_gain",
            "operator_clarity_gain",
            "contract_alignment",
            "risk_reduction",
            "implementation_safety",
            "no_runtime_compliance",
            "no_execution_compliance",
            "ledger_alignment",
            "vocabulary_alignment",
            "matrix_alignment",
            "maintenance_cost",
            "visual_noise_risk",
            "ghost_affordance_risk",
            "overbuild_risk",
            "Para valores positivos, 0 es nulo y 3 es alto",
            "Para riesgos/costos, 0 es bajo y 3 es alto",
            "requiere runtime no puede aplicar ahora",
            "requiere backend no puede aplicar ahora",
            "requiere User Panel no puede aplicar ahora",
            "affordance fantasma",
            "decorativa sin verdad",
            "structural_value >= 2",
            "truthfulness_gain >= 2",
            "operator_clarity_gain >= 2",
            "contract_alignment >= 2",
            "implementation_safety >= 2",
            "no_runtime_compliance == 3",
            "no_execution_compliance == 3",
            "ledger_alignment >= 2",
            "vocabulary_alignment >= 2",
            "ghost_affordance_risk <= 1",
            "overbuild_risk <= 1",
            "No requiere backend",
            "No requiere runtime",
            "No requiere User Panel",
            "No viola FSC/DEFER",
            "Debe diferirse",
            "Debe descartarse",
        ],
    )


def test_future_recommendation_format_matrix_rules_families_and_blockers():
    text = read(DOC)

    assert_markers(
        text,
        [
            "recommendation_id",
            "title",
            "summary",
            "source",
            "category_primary",
            "category_secondary",
            "requires_backend",
            "requires_runtime",
            "requires_user_panel",
            "requires_js",
            "requires_static_ui",
            "requires_docs_only",
            "requires_tests_only",
            "blocked_by",
            "already_covered_by",
            "deferred_reason",
            "discard_reason",
            "suggested_next_prompt",
            "operator_decision_required",
            "notes",
            "Resumen ejecutivo",
            "Estado base",
            "Fuentes revisadas",
            "Matriz TOP 15",
            "Recomendaciones aplicables ahora",
            "Recomendaciones ya cubiertas",
            "Recomendaciones futuras",
            "Recomendaciones bloqueadas",
            "Recomendaciones descartadas",
            "Recomendaciones que requieren decision del operador",
            "Riesgos detectados",
            "Deudas relacionadas",
            "Secuencia recomendada de prompts posteriores",
            "Auditar hasta 15 recomendaciones",
            "No forzar 15",
            "TOP_N_ACTUAL < 15",
            "Evitar relleno",
            "Priorizar calidad sobre cantidad",
            "Claridad de cierre UI/UX 1.x",
            "Separacion presente/bloqueado/futuro",
            "Reduccion de affordances fantasma",
            "Claridad de navegacion",
            "Claridad del operador humano",
            "Trazabilidad y evidencia",
            "Coherencia de estados",
            "Legibilidad del Panel Maestro",
            "Densidad informativa",
            "Preparacion futura User Panel",
            "Preparacion futura runtime",
            "Deudas semanticas visibles",
            "Contratos read-only",
            "Documentacion/cursor",
            "Validaciones/test-only",
            "Accesibilidad basica",
            "Resiliencia visual",
            "Riesgo de copy operativo",
            "Riesgo de sobreconstruccion",
            "Readiness para cierre coronado",
            "runtime",
            "execution",
            "dispatch",
            "model invocation",
            "tool invocation",
            "integration invocation",
            "Workers/schedulers/queues",
            "Memory writes",
            "Context injection",
            "Output delivery",
            "Public endpoints",
            "User Panel",
            "Auth/session/secrets",
            "Network/browser runtime",
            "Backend mutation",
            "CI/dependencies nuevas",
            "JSON ledger consumido por UI",
            "Fake metrics",
            "Live status",
            "Active actions",
            "Botones sin accion permitida",
            "Documentacion",
            "Test-only",
            "Copy estatico",
            "Clarificacion contractual",
            "Auditoria de consistencia",
            "Matriz de decision",
        ],
    )


def test_relationships_risks_mitigations_future_validations_decision_and_limits():
    text = read(DOC)

    assert_markers(
        text,
        [
            "Todo TOP 15 debe validarse contra ledger",
            "Si ledger marca una capacidad como bloqueada",
            "Si ledger marca una capacidad como futura",
            "Si ledger marca una deuda",
            "UNKNOWN_NEEDS_AUDIT",
            "NEEDS_OPERATOR_DECISION",
            "No se debe modificar ledger en 1.159",
            "No se debe modificar ledger en 1.160",
            "Toda recomendacion debe respetar vocabulario permitido/prohibido",
            "No puede usar estados prohibidos como estados reales",
            "No puede introducir copy operativo falso",
            "No puede introducir affordance fantasma",
            "active/running/live/operational/executing/dispatching/submitted/processing",
            "solo pueden aparecer en contexto de bloqueo o denylist",
            "TOP 15 no reemplaza matriz",
            "TOP 15 no reemplaza FSC",
            "TOP 15 no elimina DEFER_FINALIZATION",
            "TOP 15 no crea quinta FSC",
            "TOP 15 no crea cierre global automatico",
            "TOP 15 no convierte el Panel Maestro en wizard operativo",
            'data-contract-screen-count="4"',
            "1.159 no toca UI/JS/backend",
            "1.160 tampoco debe tocar UI/JS/backend si es auditoria",
            "Recomendaciones visuales futuras",
            "No se debe crear endpoint",
            "No se debe crear fetch",
            "No se debe crear listener",
            "No se debe crear localStorage",
            "No se debe crear routing/hash/history",
            "Convertir auditoria en implementacion",
            "Forzar 15 recomendaciones sin necesidad",
            "Sobreconstruir",
            "referencias externas como receta",
            "features que requieren runtime",
            "User Panel antes de tiempo",
            "backend antes de tiempo",
            "UI premium cosmetica",
            "Duplicar cosas ya cubiertas",
            "Degradar claridad por exceso documental",
            "Convertir deuda futura en blocker actual",
            "Cerrar UI/UX 1.x sin prueba",
            "ansiedad de terminar",
            "Ocultar deuda con copy",
            "Confundir publicado con terminado globalmente",
            "Planificacion primero",
            "Auditoria despues",
            "Implementacion nunca dentro de auditoria",
            "Scoring explicito",
            "Categorias cerradas",
            "Umbrales claros",
            "Ledger como filtro",
            "Contrato 1.151 como filtro",
            "Matriz/FSC/DEFER como filtros",
            "Permitir TOP_N_ACTUAL menor que 15",
            "Separar aplicable ahora/futuro/bloqueado/descartado",
            "Restore point ya publicado",
            "Proximo prompt de auditoria separado",
            "Cierre global posterior separado",
            "Validaciones futuras para 1.160",
            "Documento de auditoria TOP 15 existe",
            "Test de auditoria TOP 15 existe",
            "Contiene metodologia",
            "Contiene categorias primarias",
            "Contiene categorias secundarias",
            "Contiene scoring",
            "Contiene umbrales",
            "Contiene hasta 15 recomendaciones",
            "No fuerza exactamente 15",
            "Incluye clasificacion de cada recomendacion",
            "Incluye scores de cada recomendacion",
            "Incluye relacion con ledger",
            "Incluye relacion con contrato 1.151",
            "Incluye relacion con matriz/FSC/DEFER",
            "Incluye aplicables ahora",
            "Incluye futuras",
            "Incluye bloqueadas",
            "Incluye descartadas",
            "Incluye ya cubiertas",
            "Incluye decisiones requeridas",
            "No implementa nada",
            "No toca UI/JS/backend",
            "No crea JSON TOP 15",
            "No crea fixture TOP 15",
            "No ejecuta runtime",
            "No cierra UI/UX 1.x globalmente",
            "TOP_15_ELITE_AUDIT_PLAN_READY_FOR_AUDIT",
            "PROMPT UI/UX 1.160 - Auditar TOP 15 recomendaciones elite cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            "no se ejecuto auditoria TOP 15",
            "no se implemento ninguna recomendacion",
            "no se hizo push",
            "no se publico restore point",
        ],
    )


def test_static_file_absence_restore_point_and_contracts_are_preserved():
    assert not (ROOT / "ui" / "web" / "contracts" / "capabilities_ledger.v1.json").exists()
    assert not (ROOT / "tests" / "fixtures" / "ui_capabilities_ledger_v1.json").exists()
    assert not (ROOT / "ui" / "web" / "contracts" / "top_15_elite_audit.v1.json").exists()
    assert not (ROOT / "tests" / "fixtures" / "ui_ux_top_15_elite_audit_v1.json").exists()

    restore = read(RESTORE_POINT_158)
    assert "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLISHED" in restore
    assert "07a15d8" in restore

    assert "CAPABILITIES_LEDGER_RESTORE_POINT_PUBLICATION_SELECTED" in read(DECISION_157)
    assert "CAPABILITIES_LEDGER_CHECKPOINT_PASSED_READY_FOR_RESTORE_POINT_DECISION" in read(CHECKPOINT_156)

    ledger = read(LEDGER_155)
    assert_markers(
        ledger,
        [
            "status: TEST_ONLY_LEDGER",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "json_ledger: NOT_CREATED",
        ],
    )

    contract = read(CONTRACT_151)
    assert_markers(
        contract,
        [
            "mode: DOCUMENTATION_ONLY",
            "status: TEST_ONLY_CONTRACT",
            "runtime: NO_RUNTIME",
            "execution: NO_EXECUTION",
            "ui_consumption: NOT_CONSUMED_BY_UI",
            "backend_consumption: NOT_CONSUMED_BY_BACKEND",
            "json_contract: NOT_CREATED",
            "enforcement: TEST_ONLY",
        ],
    )


def test_ui_surface_read_only_markers_and_forbidden_copy():
    index = read(INDEX)
    assert_markers(
        index,
        [
            "Matriz de cierre UI/UX 1.x",
            "FSC-CO-01",
            "FSC-BF-02",
            "FSC-VR-03",
            "FSC-RCP-04",
            'data-contract-screen-count="4"',
            "DEFER_FINALIZATION",
        ],
    )

    for forbidden in [
        "ready to run",
        "RUNNING",
        "EXECUTING",
        "DISPATCHING",
        "SUBMITTED",
        "Processing request",
        "Capability active",
        "preview-and-run",
    ]:
        assert forbidden not in index


def test_readme_cursors_record_plan_159():
    for path in (README, UI_README):
        text = read(path)
        assert_markers(
            text,
            [
                "Planificacion 1.159 de auditoria TOP 15 elite",
                "HEAD base `07a15d8`",
                "restore point remoto vigente `07a15d8`",
                "matriz publicada",
                "vocabulario/affordances publicado",
                "ledger publicado",
                "tres bloques recomendados publicados",
                "TOP 15 planificado, no auditado",
                "TOP 15 no implementado",
                "UI/UX 1.x no cerrado globalmente",
                "no UI activa",
                "no JS",
                "no backend",
                "no runtime",
                "no execution",
                "no JSON TOP 15",
                "no fixture TOP 15",
                "no push",
                "no restore point",
                "TOP_15_ELITE_AUDIT_PLAN_READY_FOR_AUDIT",
                "PROMPT UI/UX 1.160 - Auditar TOP 15 recomendaciones elite cierre coronado UI UX 1.x Panel Maestro IA_CORE contract-aware sin runtime/no-execution",
            ],
        )


def test_protected_runtime_surfaces_have_no_diff_against_head():
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", *PROTECTED_PATHS],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.strip() == ""

