"""Estados y acciones internas seguras para dominios."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

import config


class DomainState(StrEnum):
    EMPTY = "empty"
    DRAFT = "draft"
    PREVIEW = "preview"
    MATERIALIZED = "materialized"
    VALIDATED = "validated"
    CANDIDATE_FOR_ACTIVATION = "candidate_for_activation"
    ACTIVE = "active"
    ARCHIVED = "archived"
    LEGACY = "legacy"
    BROKEN = "broken"


DOMAIN_STATE_DESCRIPTIONS: dict[DomainState, str] = {
    DomainState.EMPTY: "Dominio sin contenido operativo todavia.",
    DomainState.DRAFT: "Definicion inicial no lista para uso.",
    DomainState.PREVIEW: "Vista previa derivada antes de materializacion.",
    DomainState.MATERIALIZED: "Dominio escrito y trazado por backend interno.",
    DomainState.VALIDATED: "Dominio sandbox validado de forma declarativa; no activo.",
    DomainState.CANDIDATE_FOR_ACTIVATION: "Dominio candidato futuro a activacion; no activo.",
    DomainState.ACTIVE: "Dominio operativo PASSED.",
    DomainState.ARCHIVED: "Dominio retirado del flujo activo pero conservado.",
    DomainState.LEGACY: "Dominio historico fuera del flujo nuevo.",
    DomainState.BROKEN: "Dominio inconsistente o invalido.",
}

NON_ACTIVE_DOMAIN_STATES = {
    DomainState.EMPTY,
    DomainState.DRAFT,
    DomainState.PREVIEW,
    DomainState.MATERIALIZED,
    DomainState.VALIDATED,
    DomainState.CANDIDATE_FOR_ACTIVATION,
    DomainState.ARCHIVED,
    DomainState.LEGACY,
    DomainState.BROKEN,
}

VALID_DOMAIN_TRANSITIONS: dict[DomainState, set[DomainState]] = {
    DomainState.EMPTY: {DomainState.DRAFT, DomainState.PREVIEW, DomainState.MATERIALIZED, DomainState.ARCHIVED, DomainState.BROKEN},
    DomainState.DRAFT: {DomainState.PREVIEW, DomainState.MATERIALIZED, DomainState.ARCHIVED, DomainState.BROKEN},
    DomainState.PREVIEW: {DomainState.MATERIALIZED, DomainState.ARCHIVED, DomainState.BROKEN},
    DomainState.MATERIALIZED: {
        DomainState.VALIDATED,
        DomainState.CANDIDATE_FOR_ACTIVATION,
        DomainState.ACTIVE,
        DomainState.ARCHIVED,
        DomainState.BROKEN,
    },
    DomainState.VALIDATED: {
        DomainState.CANDIDATE_FOR_ACTIVATION,
        DomainState.ARCHIVED,
        DomainState.BROKEN,
    },
    DomainState.CANDIDATE_FOR_ACTIVATION: {
        DomainState.ARCHIVED,
        DomainState.BROKEN,
    },
    DomainState.ACTIVE: {DomainState.ARCHIVED, DomainState.BROKEN},
    DomainState.ARCHIVED: {DomainState.MATERIALIZED, DomainState.BROKEN},
    DomainState.LEGACY: {DomainState.PREVIEW, DomainState.MATERIALIZED, DomainState.BROKEN},
    DomainState.BROKEN: {DomainState.DRAFT, DomainState.PREVIEW, DomainState.ARCHIVED},
}


def coerce_domain_state(state: DomainState | str | None) -> DomainState | None:
    if state is None:
        return None
    try:
        return state if isinstance(state, DomainState) else DomainState(str(state))
    except ValueError:
        return None


def get_domain_state(domain: dict[str, Any]) -> DomainState:
    if domain.get("legacy") is True and not domain.get("status"):
        return DomainState.LEGACY
    return coerce_domain_state(domain.get("status")) or DomainState.ACTIVE


def is_domain_active(domain: dict[str, Any]) -> bool:
    try:
        return validate_domain_state(domain) is DomainState.ACTIVE
    except ValueError:
        return False


def is_domain_visible_as_active(domain: dict[str, Any]) -> bool:
    return is_domain_active(domain) and domain.get("visible_en_hud") is not False


def is_valid_domain_transition(
    from_state: DomainState | str,
    to_state: DomainState | str,
) -> bool:
    current = coerce_domain_state(from_state)
    target = coerce_domain_state(to_state)
    if current is None or target is None:
        return False
    return target in VALID_DOMAIN_TRANSITIONS[current]


def validate_domain_state(domain: dict[str, Any]) -> DomainState:
    if not isinstance(domain, dict):
        raise ValueError("domain.json debe ser un objeto")
    state = get_domain_state(domain)
    if domain.get("status") is not None and coerce_domain_state(domain.get("status")) is None:
        raise ValueError(f"Estado de dominio invalido: {domain.get('status')}")
    if state is DomainState.ACTIVE and not _has_traceability(domain):
        raise ValueError("Dominio active requiere trazabilidad minima")
    if state in NON_ACTIVE_DOMAIN_STATES and domain.get("visible_en_hud") is True:
        raise ValueError(f"Dominio {state.value} no puede estar visible como activo")
    if state is DomainState.LEGACY and domain.get("legacy") is not True:
        raise ValueError("Dominio legacy debe declarar legacy=true")
    if state is DomainState.BROKEN and not domain.get("broken_reason"):
        raise ValueError("Dominio broken debe declarar broken_reason")
    return state


def archive_domain(
    domain_id: str,
    *,
    domains_dir: str | Path | None = None,
    reason: str = "Archivado por administracion interna.",
) -> dict[str, Any]:
    domain = _load_domain_manifest(domain_id, domains_dir)
    current = validate_domain_state(domain)
    if current is DomainState.LEGACY:
        raise ValueError("Dominio legacy no se archiva automaticamente; requiere recuperacion formal")
    _require_transition(current, DomainState.ARCHIVED)
    _record_transition(domain, current, DomainState.ARCHIVED, reason)
    domain["status"] = DomainState.ARCHIVED.value
    domain["archived"] = True
    domain["visible_en_hud"] = False
    domain["archived_at"] = _now()
    return _write_domain_manifest(domain_id, domain, domains_dir)


def restore_domain(
    domain_id: str,
    *,
    domains_dir: str | Path | None = None,
    target_state: DomainState | str = DomainState.MATERIALIZED,
    reason: str = "Restaurado por administracion interna.",
) -> dict[str, Any]:
    domain = _load_domain_manifest(domain_id, domains_dir)
    current = validate_domain_state(domain)
    target = coerce_domain_state(target_state)
    if target is None:
        raise ValueError(f"Estado de restauracion invalido: {target_state}")
    if current is DomainState.LEGACY and target is DomainState.ACTIVE:
        raise ValueError("Dominio legacy no puede pasar a active sin recuperacion formal")
    if target is DomainState.ACTIVE:
        raise ValueError("restore_domain no activa dominios; active requiere validacion PASSED separada")
    _require_transition(current, target)
    _record_transition(domain, current, target, reason)
    domain["status"] = target.value
    domain["visible_en_hud"] = False
    domain["restored_at"] = _now()
    domain.pop("archived", None)
    return _write_domain_manifest(domain_id, domain, domains_dir)


def reset_domain(
    domain_id: str,
    *,
    domains_dir: str | Path | None = None,
    reason: str = "Reseteado por administracion interna.",
) -> dict[str, Any]:
    domain = _load_domain_manifest(domain_id, domains_dir)
    current = validate_domain_state(domain)
    if current is DomainState.LEGACY:
        raise ValueError("Dominio legacy no puede resetearse sin recuperacion formal")
    _record_transition(domain, current, DomainState.EMPTY, reason)
    domain["status"] = DomainState.EMPTY.value
    domain["visible_en_hud"] = False
    domain["reset_at"] = _now()
    return _write_domain_manifest(domain_id, domain, domains_dir)


def delete_domain_safely(
    domain_id: str,
    *,
    domains_dir: str | Path | None = None,
    confirm: bool = False,
    reason: str = "Eliminado por administracion interna.",
) -> dict[str, Any]:
    if not confirm:
        raise ValueError("delete_domain_safely requiere confirm=True")
    domain_dir = _safe_domain_dir(domain_id, domains_dir)
    domain = _load_domain_manifest(domain_id, domains_dir)
    current = validate_domain_state(domain)
    if current is DomainState.LEGACY:
        raise ValueError("No se borra dominio legacy automaticamente; archivar o recuperar formalmente")
    if current is not DomainState.ARCHIVED:
        raise ValueError("delete_domain_safely requiere dominio archived")
    if not domain.get("domain_state_history"):
        raise ValueError("delete_domain_safely requiere trazabilidad de estado")
    snapshot = {
        "id": domain_id,
        "deleted": True,
        "deleted_at": _now(),
        "reason": reason,
        "previous_status": current.value,
    }
    shutil.rmtree(domain_dir)
    return snapshot


def _has_traceability(domain: dict[str, Any]) -> bool:
    return bool(
        domain.get("traceability")
        or domain.get("creado_en")
        or domain.get("domain_state_history")
    )


def _require_transition(current: DomainState, target: DomainState) -> None:
    if target not in VALID_DOMAIN_TRANSITIONS[current]:
        raise ValueError(f"Transicion de dominio invalida: {current.value} -> {target.value}")


def _record_transition(
    domain: dict[str, Any],
    from_state: DomainState,
    to_state: DomainState,
    reason: str,
) -> None:
    history = domain.setdefault("domain_state_history", [])
    history.append(
        {
            "from": from_state.value,
            "to": to_state.value,
            "reason": reason,
            "at": _now(),
        }
    )


def _domains_dir(domains_dir: str | Path | None = None) -> Path:
    return Path(domains_dir or config.DOMAINS_DIR)


def _safe_domain_dir(domain_id: str, domains_dir: str | Path | None = None) -> Path:
    root = _domains_dir(domains_dir).resolve()
    target = (root / domain_id).resolve()
    if target.parent != root:
        raise ValueError("Ruta de dominio invalida")
    return target


def _load_domain_manifest(domain_id: str, domains_dir: str | Path | None = None) -> dict[str, Any]:
    manifest_path = _safe_domain_dir(domain_id, domains_dir) / "domain.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Dominio no encontrado: {domain_id}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("id") != domain_id:
        raise ValueError(f"Manifiesto invalido para dominio {domain_id}")
    return data


def _write_domain_manifest(
    domain_id: str,
    domain: dict[str, Any],
    domains_dir: str | Path | None = None,
) -> dict[str, Any]:
    manifest_path = _safe_domain_dir(domain_id, domains_dir) / "domain.json"
    manifest_path.write_text(
        json.dumps(domain, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return domain


def _now() -> str:
    return datetime.now().isoformat()
