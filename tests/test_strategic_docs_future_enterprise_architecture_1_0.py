"""Documentary coverage and guardrails, not operational capability validation."""

from pathlib import Path
import re
import unicodedata

import pytest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = "FUTURE_PLATFORM_EXTENSION_INDEX.md"
REQUIRED = {
    INDEX: [
        "5fc5d35", "1.171", "README_DOCS_UI_CONSISTENCY_RESTORE_POINT_PUBLISHED",
        "STRATEGIC_FUTURE_ENTERPRISE_ARCHITECTURE_DOCUMENTED",
        "empresa más grande posible", "documentar no equivale a implementar",
        "integración conocida no equivale a integración activa",
        "módulo documentado no equivale a módulo operativo",
        "mirror documentado no equivale a conexión real",
        "permiso documentado no equivale a sistema auth real",
        "Owner Console documentado no equivale a Owner Console operativo",
        "IA_CORE OS documentado no equivale a sistema operativo instalable actual",
        "UI/UX 1.172",
    ],
    "FUTURE_INTEGRATIONS_REGISTRY.md": [
        "n8n", "Hermes", "OpenClaw", "UI-TARS", "Home Assistant", "WhatsApp",
        "Telegram", "Gmail", "Google Sheets", "Google Docs", "Google Drive",
        "Google Calendar", "CRM", "e-commerce", "external APIs", "banks",
        "payment processors", "POS", "Mercado Pago", "OpenAI", "Anthropic",
        "Google", "Meta", "Llama", "Mistral", "DeepSeek", "Qwen", "Cohere",
        "Groq", "OpenRouter", "NVIDIA", "Ollama", "LM Studio", "vLLM", "llama.cpp",
        "motor cognitivo base", "complementarios, redundantes o excluyentes",
        "aprobación humana", "cliente", "empresa", "unidad", "sector", "usuario",
        "plan", "contrato", "permisos", "configuración",
    ],
    "FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md": [
        "owner", "admin", "director", "sector_manager", "supervisor", "operator",
        "collaborator", "viewer", "support", "external_auditor", "Agregar empleado",
        "Agregar colaborador", "Agregar responsable", "Bohemian Food", "Villa Morra",
        "Márquez", "sucursales", "oficinas", "franquicias", "sedes", "zonas",
        "marcas internas", "locales", "unidades de negocio", "países", "regiones",
        "invitación por email", "contraseña temporal", "cambio obligatorio de contraseña",
        "Dirección", "Marketing", "Ventas", "Atención al cliente", "Administración",
        "Tesorería", "Contabilidad", "Fiscalidad/Impuestos", "Legal/Compliance",
        "Recursos Humanos", "Operaciones", "TI/Soporte técnico interno", "Ciberseguridad",
        "Compras", "Proveedores", "Logística/Supply Chain", "Auditoría interna",
        "Riesgo empresarial", "Gobierno de datos", "Gobierno corporativo",
        "Calidad/Mejora continua", "Producto/I+D", "Continuidad del negocio",
        "Soporte IA_CORE autorizado", "alcance autorizado", "autorización explícita",
    ],
    "FUTURE_INTERNAL_COMMUNICATION_MODEL.md": [
        "chat interno", "chat general de empresa", "chat por sector", "chat por unidad",
        "chat por equipo", "chat por tarea", "chat con agente", "Director IA_CORE",
        "evidencia", "soporte autorizado", "autorización explícita y auditada",
        "documentación formal", "historial auditable",
    ],
    "FUTURE_FINANCIAL_MIRROR_TREASURY_AND_TAX_MODEL.md": [
        "Financial Mirror", "Treasury", "Tax Authority Mirror", "facturas", "remitos",
        "pedidos", "carga de facturas", "organismos fiscales", "bancos", "ARCA",
        "jurisdicción", "autorización humana", "no scraping", "no suplantación",
        "moneda", "regulador", "idioma", "tipo de empresa", "tipo de cliente",
        "actividad económica", "fuente oficial", "credenciales en texto plano",
    ],
    "FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md": [
        "Soporte IA_CORE como proveedor", "TI interno", "ciberseguridad",
        "detección de anomalías", "protección de memoria", "protección de contexto",
        "protección de API keys", "rate limiting", "respuesta a incidentes",
        "finalidad defensiva", "no ataque a terceros", "aislamiento por cliente/negocio/usuario",
        "logs auditables", "backup y restore verificable", "saturación de APIs",
        "borrado indebido de memoria", "agentes defensivos especializados",
    ],
    "FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md": [
        "Owner Console", "Client Edition", "Owner Recovery Kit", "Hardware Security Keys",
        "llaves físicas", "passkey", "MFA", "backup", "restore", "servidor raíz",
        "sin backdoors", "privacidad", "Panel Maestro del cliente",
        "panel sectorial", "panel de soporte autorizado", "instalador cliente",
        "opción oculta", "códigos offline", "archivo de recuperación cifrado",
        "verificación de integridad", "dispositivos confiables", "manual de emergencia",
        "backup de datos críticos", "backup operativo", "backup documental", "snapshots",
        "backup cifrado", "restore probado", "restore parcial", "restore completo",
        "alerta si backup falla", "ubicación externa segura",
    ],
    "FUTURE_ONBOARDING_MANUALS_AND_GOVERNANCE_MODEL.md": [
        "carta de bienvenida", "carta de presentación", "manual general",
        "manual por sector", "manual por rol", "reunión inicial", "dueño", "gerentes",
        "responsables", "soporte/sistemas", "socios", "directorio", "memoria informal",
        "sectores activos", "unidades", "usuarios", "permisos", "colaboradores",
        "agentes", "integraciones habilitadas", "acciones permitidas", "acciones bloqueadas",
        "reportes", "flujos de aprobación", "canales", "manual privado del owner",
        "Owner Console", "fecha de aprobación", "históricas",
    ],
    "FUTURE_LEGAL_COMPLIANCE_AND_JURISDICTIONS_MODEL.md": [
        "Legal", "Compliance", "jurisdicciones", "contratos", "privacidad",
        "propiedad intelectual", "revisión legal", "abogados humanos", "empresa proveedora",
        "empresa cliente", "país de origen", "países donde vende", "tiene empleados",
        "almacena datos", "procesa pagos", "tiene oficinas", "jurisdicción contractual",
        "jurisdicción fiscal", "jurisdicción laboral", "jurisdicción de privacidad",
    ],
    "FUTURE_ENTERPRISE_MODULES_AND_RISK_MODEL.md": [
        "auditoría interna", "riesgo empresarial", "compras", "proveedores", "procurement",
        "supply chain", "logística", "stock", "depósitos", "rutas", "activos", "infraestructura",
        "gobierno de datos", "gobierno corporativo", "continuidad del negocio", "calidad",
        "mejora continua", "producto/I+D", "reporting ejecutivo", "relaciones institucionales",
        "compliance sectorial", "customer success", "formación/capacitación interna",
        "financiero", "operativo", "legal", "reputacional", "tecnológico", "proveedor",
        "país", "mercado", "seguridad", "datos", "continuidad", "reclamos", "indicadores",
    ],
    "FUTURE_ADAPTIVE_BUSINESS_INTELLIGENCE_MODEL.md": [
        "Adaptive Business Intelligence", "aprendizaje", "evidencia", "Guatemala",
        "región", "mercado", "clientes", "economía local", "cultura comercial",
        "privacidad", "anonimización", "cross-client", "resultados", "sectores",
        "decisiones", "errores", "aciertos", "métricas", "condiciones económicas",
        "canales", "productos", "servicios", "jurisdicción", "competencia", "estacionalidad",
        "no se implementa memoria global real", "no se hardcodea",
    ],
}


def read_doc(name):
    path = DOCS / name
    assert path.is_file(), f"Missing required strategic document: {name}"
    return path.read_text(encoding="utf-8")


def normalized(text):
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


@pytest.mark.parametrize("name", REQUIRED)
def test_required_document_has_future_status_and_coverage(name):
    text = normalized(read_doc(name))
    expected = [
        "futuro", "no implementado", "sin runtime", "sin execution", "sin endpoints",
        "sin integraciones reales", "sin conectores reales", "sin credenciales",
        *REQUIRED[name],
    ]
    missing = [term for term in expected if normalized(term) not in text]
    assert not missing, f"{name}: missing {missing}"


def test_index_links_every_required_document():
    links = set(re.findall(r"\]\((FUTURE_[A-Z_]+\.md)\)", read_doc(INDEX)))
    assert links == set(REQUIRED) - {INDEX}


@pytest.mark.parametrize("name", REQUIRED)
def test_strategic_document_links_resolve_within_the_block(name):
    targets = re.findall(r"\]\(([^)]+)\)", read_doc(name))
    assert targets, f"{name}: missing navigation"
    for target in targets:
        assert target in REQUIRED, f"{name}: unexpected or broken target {target}"
        assert (DOCS / target).is_file()
    if name != INDEX:
        assert INDEX in targets


def test_integration_states_do_not_imply_action_authority():
    text = read_doc("FUTURE_INTEGRATIONS_REGISTRY.md")
    states = set(re.findall(r"^\| `([a-z_]+)` \|", text, re.MULTILINE))
    assert states == {
        "future", "available", "licensed", "enabled", "disabled", "configured",
        "missing_credentials", "blocked", "unsupported", "requires_approval", "deprecated",
    }
    for boundary in [
        "integración activa no equivale a acción libre",
        "no conforman una escalera que conceda permiso automáticamente",
        "una transcripción o mensaje recibido no constituye autorización",
    ]:
        assert boundary in normalized(text)


def test_readmes_reference_strategy_without_advancing_active_ui():
    root_text = normalized((ROOT / "README.md").read_text(encoding="utf-8"))
    for term in [
        "STRATEGIC DOCS 1.0", "arquitectura futura empresarial",
        "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md", "sin runtime", "sin execution",
        "sin integraciones reales", "no-runtime", "no-execution", "1.171", "5fc5d35",
    ]:
        assert normalized(term) in root_text
    web_text = normalized((ROOT / "ui/web/README.md").read_text(encoding="utf-8"))
    for term in [
        "STRATEGIC DOCS 1.0", "../../docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
        "no modifica UI activa", "no habilita runtime", "no cambia contracts actuales",
        "no implementa paneles ni modulos",
    ]:
        assert normalized(term) in web_text


# This heuristic catches affirmative present-tense claims, not every paraphrase.
# Restriction/future scope is local to the clause, never to the whole document.
CLAUSE_BOUNDARY = re.compile(r"[.!?;]\s+|\bpero\b|\baunque\b|\bsin embargo\b", re.IGNORECASE)
PRESENT_CLAIM = re.compile(
    r"\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?"
    r"(?:ejecuta|opera|factura|paga|conecta|administra|envía|responde|protege|recupera|"
    r"instala|declara|presenta|controla)\b"
    r"|\bia_core\s+(?:(?:actualmente|hoy|ya)\s+)?(?:tiene|dispone de|ofrece)\s+"
    r"(?:integraciones reales|mirrors reales|multi-tenant real|runtime real|execution real)\b"
    r"|\b(?:owner console|client edition|multi-tenant|runtime|execution)\s+"
    r"(?:(?:actualmente|hoy|ya)\s+)?(?:es|está)\s+"
    r"(?:operativo|operativa|instalable|activo|activa|real|disponible)\b",
    re.IGNORECASE,
)
NON_CURRENT_PREFIX = re.compile(
    r"^(?:no\b|sin\b|prohibido\b|no se debe\b|no debe\b|no afirmar\b|"
    r"en el futuro\b|como visión futura\b|ejemplo de redacción prohibida:)",
    re.IGNORECASE,
)


def current_capability_claims(text):
    claims = []
    for paragraph in re.split(r"\n\s*\n", text):
        for clause in CLAUSE_BOUNDARY.split(normalized(paragraph)):
            clause = clause.strip(" -*#>`\"")
            if PRESENT_CLAIM.search(clause) and not NON_CURRENT_PREFIX.match(clause):
                claims.append(clause)
    return claims


@pytest.mark.parametrize("name", REQUIRED)
def test_documents_do_not_claim_current_operational_capabilities(name):
    assert current_capability_claims(read_doc(name)) == []


@pytest.mark.parametrize("text", [
    "IA_CORE ejecuta bancos reales.", "IA_CORE conecta ARCA real.",
    "IA_CORE hoy factura para empresas reales.", "IA_CORE presenta declaraciones reales.",
    "IA_CORE envía WhatsApp real.", "IA_CORE tiene integraciones reales.",
    "Owner Console es operativo.", "Client Edition está instalable.",
    "IA_CORE dispone de multi-tenant real.", "IA_CORE ofrece runtime real.",
    "IA_CORE tiene execution real.",
    "Sin runtime. IA_CORE ya paga facturas.",
    "En el futuro habrá módulos; IA_CORE actualmente conecta bancos reales.",
    "No hay credenciales, pero IA_CORE actualmente envía WhatsApp real.",
])
def test_claim_guard_detects_affirmations_even_after_restrictions(text):
    assert current_capability_claims(text)


@pytest.mark.parametrize("text", [
    "No afirmar que IA_CORE ejecuta bancos reales.",
    "IA_CORE no ejecuta bancos reales.",
    "En el futuro, IA_CORE ejecuta solo bajo autorización humana.",
    "IA_CORE podría asistir en facturación en el futuro.",
    "Owner Console documentado no equivale a Owner Console operativo.",
    "No se debe decir que Client Edition es instalable.",
    "Estado: futuro; no implementado; sin runtime; sin execution.",
])
def test_claim_guard_accepts_negations_restrictions_and_future_scope(text):
    assert current_capability_claims(text) == []
