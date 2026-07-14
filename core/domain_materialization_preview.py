"""Preview no operativo previo a materializacion de dominios."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from core.artifact_state import ArtifactState, is_operational
from core.professional_domain_end_to_end import run_professional_domain_end_to_end


PREVIEW_SCHEMA_VERSION = "1.0"


def build_domain_materialization_preview(
    *,
    domain_id: str,
    area_id: str,
    niche_ids: list[str] | None = None,
    business_scale: str | None = None,
    objective: str | None = None,
    complexity_level: str | None = None,
    max_profiles: int | None = None,
    max_presets: int | None = None,
) -> dict[str, Any]:
    """Construye un preview serializable sin escribir artefactos operativos."""
    domain_request = {
        "domain_id": domain_id,
        "area_id": area_id,
        "niche_ids": list(niche_ids or []),
        "business_scale": business_scale,
        "objective": objective,
        "complexity_level": complexity_level,
        "max_profiles": max_profiles,
        "max_presets": max_presets,
    }
    end_to_end = run_professional_domain_end_to_end(**domain_request)
    derived_outputs = {
        "profile_catalog": _wrap_derived_output(
            end_to_end["profile_catalog"],
            artifact_key="derived_profile_catalog",
        ),
        "agent_presets": _wrap_derived_output(
            end_to_end["agent_presets"],
            artifact_key="derived_agent_presets",
        ),
        "team_template": _wrap_derived_output(
            end_to_end["team_template"],
            artifact_key="derived_team_template",
        ),
        "model_recommendations": _wrap_derived_output(
            end_to_end["model_recommendations"],
            artifact_key="derived_model_recommendations",
        ),
        "paper_seeds": _wrap_derived_output(
            end_to_end["paper_seeds_expected"],
            artifact_key="derived_paper_seeds",
        ),
        "end_to_end": _wrap_derived_output(
            end_to_end,
            artifact_key="derived_end_to_end_output",
        ),
    }
    warnings = list(end_to_end.get("warnings", []))
    gaps = list(end_to_end.get("gaps", []))
    risks = list(end_to_end.get("risks", []))
    preview = {
        "schema_version": PREVIEW_SCHEMA_VERSION,
        "artifact_type": "domain_materialization_preview",
        "preview_id": _preview_id(domain_request),
        "artifact_state": ArtifactState.DERIVED_PREVIEW.value,
        "operational": False,
        "creates_domain": False,
        "creates_agents": False,
        "creates_papers": False,
        "creates_presets": False,
        "modifies_domains": False,
        "domain_request": domain_request,
        "source": {
            "source_of_truth": "catalogs/professional_profiles.json",
            "generator": "core.domain_materialization_preview.build_domain_materialization_preview",
            "end_to_end_generator": "core.professional_domain_end_to_end.run_professional_domain_end_to_end",
            "state_contract": "core.artifact_state.ArtifactState",
        },
        "derived_outputs": derived_outputs,
        "warnings": warnings,
        "gaps": gaps,
        "risks": risks,
        "required_actions": _required_actions(end_to_end),
        "validation_status": _validation_status(warnings=warnings, gaps=gaps, risks=risks),
    }
    return validate_domain_materialization_preview(preview)


def validate_domain_materialization_preview(preview: dict[str, Any]) -> dict[str, Any]:
    required = {
        "preview_id",
        "domain_request",
        "source",
        "derived_outputs",
        "warnings",
        "gaps",
        "risks",
        "required_actions",
        "validation_status",
    }
    missing = required - set(preview)
    if missing:
        raise ValueError(f"preview incompleto: {', '.join(sorted(missing))}")
    if not preview.get("preview_id"):
        raise ValueError("preview sin identificador")
    if not isinstance(preview.get("domain_request"), dict) or not preview["domain_request"].get("domain_id"):
        raise ValueError("preview sin dominio solicitado")
    if not isinstance(preview.get("source"), dict) or not preview["source"].get("source_of_truth"):
        raise ValueError("preview sin origen trazable")
    if preview.get("operational") is not False:
        raise ValueError("preview no puede ser operativo")
    if preview.get("modifies_domains") is not False:
        raise ValueError("preview no puede modificar domains/")
    for flag in ("creates_domain", "creates_agents", "creates_papers", "creates_presets"):
        if preview.get(flag) is not False:
            raise ValueError(f"preview no puede marcar {flag}=true")
    state = preview.get("artifact_state")
    if state not in {
        ArtifactState.DERIVED_PREVIEW.value,
        ArtifactState.READY_TO_MATERIALIZE.value,
        ArtifactState.BROKEN.value,
    }:
        raise ValueError(f"estado de preview invalido: {state}")
    if is_operational(state):
        raise ValueError("preview nunca puede ser operativo")
    _validate_derived_outputs(preview["derived_outputs"])
    json.dumps(preview, ensure_ascii=False)
    return preview


def mark_preview_ready_to_materialize(preview: dict[str, Any]) -> dict[str, Any]:
    ready = deepcopy(preview)
    if ready.get("validation_status") == "broken":
        raise ValueError("preview broken no puede pasar a ready_to_materialize")
    ready["artifact_state"] = ArtifactState.READY_TO_MATERIALIZE.value
    ready["validation_status"] = "ready_to_materialize"
    return validate_domain_materialization_preview(ready)


def mark_preview_broken(preview: dict[str, Any], *, reason: str) -> dict[str, Any]:
    broken = deepcopy(preview)
    broken["artifact_state"] = ArtifactState.BROKEN.value
    broken["validation_status"] = "broken"
    broken.setdefault("gaps", []).append({"type": "broken_preview", "detail": reason})
    return validate_domain_materialization_preview(broken)


def _wrap_derived_output(payload: Any, *, artifact_key: str) -> dict[str, Any]:
    return {
        "artifact_key": artifact_key,
        "artifact_state": ArtifactState.DERIVED_PREVIEW.value,
        "operational": False,
        "payload": payload,
    }


def _validate_derived_outputs(derived_outputs: dict[str, Any]) -> None:
    if not isinstance(derived_outputs, dict) or not derived_outputs:
        raise ValueError("preview sin outputs derivados")
    for key, output in derived_outputs.items():
        if not isinstance(output, dict):
            raise ValueError(f"derived_output {key} debe ser objeto")
        if not output.get("artifact_key"):
            raise ValueError(f"derived_output {key} sin artifact_key")
        if output.get("artifact_state") not in {
            ArtifactState.DERIVED_PREVIEW.value,
            ArtifactState.READY_TO_MATERIALIZE.value,
            ArtifactState.BROKEN.value,
        }:
            raise ValueError(f"derived_output {key} tiene estado invalido")
        if output.get("operational") is not False:
            raise ValueError(f"derived_output {key} no puede ser operativo")
        if "payload" not in output:
            raise ValueError(f"derived_output {key} sin payload")


def _preview_id(domain_request: dict[str, Any]) -> str:
    serialized = json.dumps(domain_request, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return f"preview_{digest}"


def _required_actions(end_to_end: dict[str, Any]) -> list[dict[str, Any]]:
    actions = deepcopy(end_to_end.get("activation_plan", []))
    actions.append(
        {
            "order": len(actions) + 1,
            "action": "Validar preview y aprobar materializacion en una fase posterior.",
            "status": "pending",
            "operational": False,
        }
    )
    return actions


def _validation_status(
    *,
    warnings: list[Any],
    gaps: list[Any],
    risks: list[Any],
) -> str:
    if gaps:
        return "needs_review"
    if warnings or risks:
        return "review_recommended"
    return "valid_preview"
