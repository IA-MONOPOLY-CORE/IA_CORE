"""Contract checks for STRATEGIC DOCS 1.3; no infrastructure validation."""

from pathlib import Path
import re
import subprocess
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MODEL_NAME = "FUTURE_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_MODEL.md"
MODEL = DOCS / MODEL_NAME
INDEX = DOCS / "FUTURE_PLATFORM_EXTENSION_INDEX.md"
OWNER = DOCS / "FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md"
OS_MODEL = DOCS / "FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md"
SECURITY = DOCS / "FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md"
ACCESS = DOCS / "FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md"
README = ROOT / "README.md"

ALLOWED_DIFF = {
    "README.md",
    f"docs/{MODEL_NAME}",
    "docs/FUTURE_PLATFORM_EXTENSION_INDEX.md",
    "docs/FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md",
    "docs/FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
    "docs/FUTURE_SECURITY_AND_IT_OPERATIONS_MODEL.md",
    "docs/FUTURE_ORGANIZATIONAL_ACCESS_MODEL.md",
    "tests/test_strategic_docs_root_control_plane_owner_nodes_and_continuity_1_3.py",
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


def affirmative_forbidden_claims(text: str, forbidden: list[str]) -> list[str]:
    claims = []
    for clause in re.split(r"[.!?;]\s+|\n", normalized(text)):
        clause = clause.strip(" -*#>`\"")
        for phrase in forbidden:
            marker = normalized(phrase)
            if marker not in clause:
                continue
            prefix = clause.split(marker, 1)[0]
            if not re.search(r"\b(?:no|sin)\b", prefix):
                claims.append(clause)
    return claims


def test_root_control_plane_document_exists():
    assert MODEL.is_file()


def test_index_references_continuity_document_as_future_only():
    assert_markers(
        INDEX,
        [
            MODEL_NAME,
            "Root Control Plane, Owner Nodes, continuidad operativa",
            "no crea nodos, servidores, failover, cloud, backups ni recovery",
            "STRATEGIC_ROOT_CONTROL_PLANE_OWNER_NODES_AND_CONTINUITY_DOCUMENTED",
        ],
    )


def test_readme_records_strategic_docs_1_3_briefly():
    assert_markers(
        README,
        [
            "STRATEGIC DOCS 1.3",
            "Root Control Plane futuro",
            "Owner Nodes",
            "continuidad operativa",
            "línea de mando",
            "recovery owner",
            "no dependencia de una sola PC owner",
            "documental y no implementado",
        ],
    )


def test_model_separates_all_control_and_continuity_layers():
    assert_markers(
        MODEL,
        [
            "Root Control Plane",
            "Owner Console",
            "Owner Nodes",
            "Owner Node Network",
            "Client Instances",
            "Continuity Layer",
            "Backup / Recovery Layer",
            "Cloud Safety Net",
            "Owner Console no es el servidor",
            "interfaz soberana del owner",
        ],
    )


def test_single_owner_computer_dependency_is_explicitly_rejected():
    assert_markers(
        MODEL,
        [
            "IA_CORE no debe fundarse sobre la disponibilidad física del equipo personal del owner",
            "no debe nacer arquitectónicamente atado a una sola máquina",
            "el owner gobierne el ecosistema, pero no sea el punto único de falla",
            "El owner puede estar desconectado",
            "El ecosistema no debería quedar desconectado por eso",
        ],
    )


def test_failure_scenarios_and_recovery_need_are_documented():
    assert_markers(
        MODEL,
        [
            "corte de electricidad del owner",
            "caída de internet del owner",
            "PC owner apagada",
            "robo del equipo",
            "rotura de disco",
            "pérdida de sesión",
            "falla de hardware",
            "mantenimiento",
            "error humano",
            "desastre físico",
        ],
    )


def test_owner_outage_is_distinguished_from_client_continuity():
    assert_markers(
        MODEL,
        [
            "Diferencia entre caída del owner y continuidad del cliente",
            "Si el owner se cae, no se deben pausar las operaciones normales de los clientes",
            "Las instancias cliente no deben congelarse por indisponibilidad del owner",
            "Cada cliente debe continuar operando dentro de sus propios permisos, contratos, módulos e integraciones habilitadas",
            "acciones cross-tenant",
        ],
    )


def test_client_instance_hierarchy_and_isolation_are_complete():
    assert_markers(
        MODEL,
        [
            "Cliente / Empresa",
            "unidades/sedes si aplica",
            "áreas",
            "subáreas",
            "usuarios",
            "roles",
            "agentes",
            "módulos",
            "integraciones habilitadas",
            "datos",
            "reportes",
            "auditoría",
            "permisos",
            "límites",
            "un error en una instancia no contamine otras",
            "prohibidas por defecto",
        ],
    )


def test_owner_node_network_and_future_locations_are_covered():
    assert_markers(
        MODEL,
        [
            "Owner Node 1",
            "Owner Node 2",
            "Owner Node 3",
            "Owner Server Room futuro",
            "Cloud Safety Net",
            "PC principal",
            "notebook autorizada",
            "segunda PC",
            "servidor propio",
            "server room",
            "VPS",
            "cloud backup",
            "appliance",
            "nodo dedicado con UPS",
            "No basta con tener sesión abierta en varias PCs",
        ],
    )


def test_owner_node_states_and_command_line_are_complete():
    assert_markers(
        MODEL,
        [
            "primary",
            "secondary",
            "standby",
            "candidate",
            "degraded",
            "offline",
            "recovering",
            "revoked",
            "maintenance",
            "compromised",
            "IA_CORE debe tener una línea estricta de mando entre nodos owner",
            "promover un nodo secundario preautorizado",
            "configuración mínima diferencial",
        ],
    )


def test_double_authority_and_split_brain_are_prevented_by_design():
    assert_markers(
        MODEL,
        [
            "No deben existir dos nodos owner actuando como autoridad principal al mismo tiempo",
            "duplicación",
            "doble autoridad",
            "doble escritura",
            "split-brain",
            "pérdida de trazabilidad",
            "reconciliar estado",
            "degradar a modo seguro",
            "bloquear doble liderazgo",
            "evitar aprobación cruzada insegura",
        ],
    )


def test_future_continuity_states_are_complete():
    assert_markers(
        MODEL,
        [
            "system_online",
            "system_degraded",
            "system_offline",
            "owner_online",
            "owner_offline",
            "owner_unreachable",
            "owner_recovery_mode",
            "root_available",
            "root_degraded",
            "root_unavailable",
            "client_online",
            "client_degraded",
            "client_offline",
            "node_primary",
            "node_secondary",
            "node_standby",
            "node_promoted",
            "node_revoked",
            "node_compromised",
            "approval_pending",
            "approval_blocked",
            "backup_ok",
            "backup_failed",
            "recovery_required",
            "cloud_safety_net_available",
            "manual_intervention_required",
            "vocabulario documental futuro, no estados implementados",
        ],
    )


def test_actions_that_may_continue_without_owner_are_bounded():
    assert_markers(
        MODEL,
        [
            "Acciones que pueden continuar sin owner online",
            "paneles de clientes",
            "lectura de datos autorizada",
            "análisis internos",
            "reportes programados",
            "alertas",
            "backups",
            "auditoría",
            "tareas de bajo riesgo",
            "integraciones ya autorizadas",
            "comunicación interna",
            "procesos propios del cliente",
        ],
    )


def test_sensitive_actions_are_held_for_the_correct_approver():
    assert_markers(
        MODEL,
        [
            "Acciones que deben quedar retenidas o requerir aprobación",
            "pagos",
            "operaciones financieras reales",
            "borrado de datos",
            "cambios de permisos altos",
            "activación de integraciones sensibles",
            "acceso soporte a información privada",
            "cambios legales",
            "restauración de backups",
            "promoción manual de nodos",
            "recuperación owner",
            "aprobadores del cliente",
            "No todo depende del owner",
        ],
    )


def test_future_infrastructure_avoids_a_new_single_point_of_failure():
    assert_markers(
        MODEL,
        [
            "workstation o server dedicado",
            "GPU potente",
            "CPU fuerte",
            "mucha RAM",
            "varios terabytes",
            "UPS",
            "backups cloud",
            "server room",
            "redundancia de internet",
            "no debe convertirse en único punto de falla",
            "PC potente local + UPS + nodo secundario + backups automáticos + cloud mínimo de continuidad + recovery owner",
        ],
    )


def test_storage_growth_is_partitioned_by_responsibility():
    assert_markers(
        MODEL,
        [
            "logs",
            "auditoría",
            "evidencia",
            "archivos de clientes",
            "backups",
            "embeddings",
            "modelos locales",
            "snapshots",
            "separar memoria operativa, evidencia, archivos, backups, modelos y logs",
        ],
    )


def test_owner_recovery_and_os_device_models_are_connected():
    assert_markers(
        MODEL,
        [
            "FUTURE_OWNER_SOVEREIGNTY_AND_RECOVERY_MODEL.md",
            "MFA/passkeys",
            "recovery kit",
            "backup cifrado",
            "revocación de dispositivos perdidos",
            "FUTURE_IA_CORE_OS_AND_DEVICE_ECOSYSTEM.md",
            "entorno operativo y de dispositivos",
        ],
    )
    assert_markers(OWNER, [MODEL_NAME, "Owner Console, Owner Nodes, Root Control Plane"])
    assert_markers(OS_MODEL, [MODEL_NAME, "continuidad operativa, línea de mando y recovery"])


def test_security_and_access_models_preserve_isolation_and_governance():
    assert_markers(
        SECURITY,
        [
            MODEL_NAME,
            "detección de nodo comprometido",
            "revocación",
            "protección contra doble autoridad",
            "recovery seguro",
            "aislamiento",
        ],
    )
    assert_markers(
        ACCESS,
        [
            MODEL_NAME,
            "Los clientes deberían seguir operando bajo sus propios permisos",
            "owner no debería ser punto único de falla",
            "soporte owner debe estar gobernado",
            "acceso cross-tenant debe estar restringido por defecto",
        ],
    )


def test_current_limits_are_unambiguous():
    assert_markers(
        MODEL,
        [
            "Root Control Plane no existe todavía",
            "Owner Nodes no existen todavía",
            "Owner Node Network no existe todavía",
            "No hay failover real",
            "No hay leader election real",
            "No hay heartbeat real",
            "No hay Cloud Safety Net real",
            "No hay recovery automático",
            "No hay server room IA_CORE",
            "No hay nodos distribuidos",
            "No hay continuidad operativa distribuida",
            "No hay promoción automática de nodo secundario",
            "No hay backups cloud conectados por este documento",
            "exclusivamente estratégico y futuro",
        ],
    )


def test_new_document_avoids_current_capability_claims():
    forbidden = [
        "ya funciona",
        "está operativo",
        "está activo",
        "failover automático activo",
        "promueve automáticamente",
        "nodos reales",
        "cloud conectado",
        "backups reales configurados",
        "clientes reales conectados",
        "ejecuta recuperación automática",
        "servidor raíz funcionando",
    ]
    assert affirmative_forbidden_claims(read(MODEL), forbidden) == []
    assert affirmative_forbidden_claims("Cloud conectado.", forbidden)
    assert affirmative_forbidden_claims("No hay cloud conectado.", forbidden) == []
    text = normalized(read(MODEL))
    for marker in [
        "futuro",
        "no implementado",
        "sin servidores",
        "sin infraestructura real",
        "sin cloud",
        "sin failover",
        "sin runtime",
        "sin execution",
        "sin endpoints",
        "sin integraciones reales",
        "sin credenciales",
    ]:
        assert normalized(marker) in text


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
