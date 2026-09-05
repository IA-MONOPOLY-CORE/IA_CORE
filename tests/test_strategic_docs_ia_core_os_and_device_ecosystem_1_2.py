"""Contract checks for STRATEGIC DOCS 1.2; no OS or device validation."""

from pathlib import Path
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OS_NAME = "FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md"
OS_DOC = DOCS / OS_NAME
INDEX = DOCS / "FUTURE_PLATFORM_EXTENSION_INDEX.md"
OWNER = DOCS / "FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md"
SECURITY = DOCS / "FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md"
INTEGRATIONS = DOCS / "FUTURE_INTEGRATIONS_REGISTRY.md"
INTELLIGENCE = DOCS / "FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md"
README = ROOT / "README.md"

ALLOWED_DIFF = {
    "README.md",
    f"docs/{OS_NAME}",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "docs/FUTURE_INTEGRATIONS_REGISTRY.md",
    "docs/FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md",
    "tests/test_strategic_docs_ia_core_os_and_device_ecosystem_1_2.py",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def assert_markers(path: Path, markers: list[str]) -> None:
    text = normalized(read(path))
    missing = [marker for marker in markers if normalized(marker) not in text]
    assert not missing, f"{path.name}: missing {missing}"


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


def test_os_and_device_ecosystem_document_exists():
    assert OS_DOC.is_file()


def test_index_references_os_document_as_future_only():
    assert_markers(
        INDEX,
        [
            OS_NAME,
            "documentación estratégica",
            "no implementa sistema operativo",
            "STRATEGIC_IA_CORE_OS_AND_DEVICE_ECOSYSTEM_DOCUMENTED",
        ],
    )


def test_readme_records_strategic_docs_1_2_briefly():
    assert_markers(
        README,
        [
            "STRATEGIC DOCS 1.2",
            "IA_CORE OS",
            "Mobile OS",
            "terminal nativa",
            "Linux/Unix/AOSP",
            "ecosistema de dispositivos",
            "no implementa ni activa",
        ],
    )


def test_document_identifies_the_four_distinct_layers():
    assert_markers(
        OS_DOC,
        [
            "IA_CORE Platform",
            "IA_CORE OS",
            "IA_CORE Mobile OS / Mobile Environment",
            "IA_CORE Device Ecosystem",
            "terminal nativa",
            "Linux",
            "Unix",
            "AOSP",
        ],
    )


def test_os_is_not_defined_as_a_generic_distribution():
    assert_markers(
        OS_DOC,
        [
            "No una distro genérica",
            "no debe ser una distribución genérica",
            "macOS",
            "Android",
            "Linux/Unix/AOSP",
            "identidad conceptual debería ser propia",
            "no debe rehacer innecesariamente lo que Linux/Unix ya resolvió",
        ],
    )


def test_linux_unix_ecosystem_advantages_are_covered():
    assert_markers(
        OS_DOC,
        [
            "paquetes",
            "servicios",
            "usuarios y grupos",
            "contenedores",
            "repositorios",
            "drivers",
            "herramientas open source",
            "networking",
            "logs",
            "filesystem",
            "procesos",
            "compatibilidad con programas existentes",
            "comunidad y madurez técnica",
        ],
    )


def test_native_terminal_is_capable_in_vision_and_strictly_governed():
    assert_markers(
        OS_DOC,
        [
            "Terminal nativa IA_CORE",
            "instalar paquetes compatibles",
            "administrar servicios",
            "conectar repositorios",
            "GitHub",
            "revisar logs",
            "diagnósticos",
            "revisar permisos",
            "auditar comandos sensibles",
            "bloquear acciones peligrosas sin permisos",
            "terminal futura debe ser poderosa, pero gobernada",
            "auditoría, seguridad y trazabilidad",
        ],
    )


def test_hardware_and_its_realistic_benefits_are_documented():
    assert_markers(
        OS_DOC,
        [
            "CPU",
            "RAM",
            "GPU",
            "almacenamiento local",
            "almacenamiento externo",
            "red",
            "cámaras",
            "micrófonos",
            "puertos",
            "periféricos",
            "teléfono",
            "no hace mágicamente más inteligentes a los agentes",
            "latencia",
            "paralelismo",
            "modelos locales",
            "backups",
            "disponibilidad",
        ],
    )


def test_mobile_is_an_intelligent_terminal_with_native_communication_rules():
    assert_markers(
        OS_DOC,
        [
            "El teléfono no sería solo una pantalla chica del sistema",
            "terminal inteligente del ecosistema IA_CORE",
            "llamadas nativas",
            "mensajes",
            "voz",
            "notificaciones",
            "permisos",
            "consentimiento",
            "privacidad",
            "jurisdicción",
            "canal directo sistema-a-sistema",
        ],
    )


def test_device_roles_and_business_specialization_are_explicit():
    assert_markers(
        OS_DOC,
        [
            "Servidor raíz / Root futuro",
            "Computadora local",
            "Notebook",
            "Teléfono",
            "Dispositivos externos",
            "trabajo",
            "producción",
            "gestión",
            "activos",
            "coordinación de humanos y agentes",
            "automatización controlada",
            "entretenimiento, gaming, redes sociales",
        ],
    )


def test_existing_browsers_and_tools_are_reused_under_governance():
    assert_markers(
        OS_DOC,
        [
            "Brave",
            "Chromium",
            "herramientas de desarrollo",
            "gestores de paquetes",
            "herramientas de monitoreo",
            "suites documentales",
            "El objetivo no es reinventar todo",
            "seleccionar, integrar, gobernar y orientar",
        ],
    )


def test_future_use_cases_and_financial_warning_are_complete():
    assert_markers(
        OS_DOC,
        [
            "Negocio gastronómico",
            "Servicio técnico",
            "Empresa financiera o análisis de mercados",
            "no debe prometer ganancias garantizadas",
            "no debe prometer ganancias garantizadas ni operar capital real sin permisos",
            "gestión de riesgo",
            "backtesting",
            "auditoría de decisiones",
            "sin declarar capacidad actual ni prometer rentabilidad",
        ],
    )


def test_institutional_intelligence_connection_is_governed():
    assert_markers(
        OS_DOC,
        [
            "FUTURE_INSTITUTIONAL_INTELLIGENCE_LAYER.md",
            "inteligencia institucional futura",
            "permisos, contratos, anonimización y aislamiento tenant",
        ],
    )
    assert_markers(
        INTELLIGENCE,
        [
            OS_NAME,
            "señales, evidencia, logs, patrones de uso y contexto de dispositivo",
            "permisos, privacidad, contratos, anonimización y aislamiento tenant",
        ],
    )


def test_current_limits_are_unambiguous():
    assert_markers(
        OS_DOC,
        [
            "IA_CORE OS no existe todavía",
            "IA_CORE Mobile OS no existe todavía",
            "IA_CORE Device Ecosystem no existe todavía",
            "terminal IA_CORE no existe todavía",
            "No hay instalación de paquetes desde IA_CORE",
            "No hay conexión real con GitHub como instalador",
            "No hay llamadas reales implementadas",
            "No hay SMS reales implementados",
            "No hay sistema operativo distribuido",
            "No hay reemplazo actual de Windows, Linux, macOS, Android ni iOS",
            "exclusivamente estratégico y futuro",
        ],
    )


def test_related_security_integrations_and_owner_models_are_connected():
    assert_markers(
        SECURITY,
        [OS_NAME, "hardening", "gestión de dispositivos", "control de terminal"],
    )
    assert_markers(
        INTEGRATIONS,
        [
            OS_NAME,
            "ecosistema Linux/Unix",
            "repositorios y paquetes compatibles",
            "integraciones o extensiones gobernadas",
            "no equivale a que esté activa",
        ],
    )
    assert_markers(
        OWNER,
        [OS_NAME, "dispositivos autorizados", "bloque estratégico 1.3 separado"],
    )


def test_new_document_remains_future_only_and_avoids_current_claims():
    text = normalized(read(OS_DOC))
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

    forbidden = [
        "ya funciona",
        "está operativo",
        "está activo",
        "ejecuta automáticamente",
        "llama automáticamente",
        "instala automáticamente",
        "reemplaza Android",
        "reemplaza Linux",
        "reemplaza Windows",
        "opera capital real",
        "garantiza ganancias",
        "conecta dispositivos reales",
    ]
    assert not [phrase for phrase in forbidden if normalized(phrase) in text]


def test_diff_is_limited_to_documentary_scope_and_protected_paths_are_untouched():
    assert changed_paths() <= ALLOWED_DIFF
    for protected in [
        "core/api.py",
        "ui/web/index.html",
        "ui/web/backend-contract-widgets.js",
        "backend",
        "core",
        "runtime",
        ".env",
    ]:
        assert git("diff", "--name-only", "HEAD", "--", protected) == ""
