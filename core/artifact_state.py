"""Contrato minimo de estados para artefactos derivados y operativos."""

from __future__ import annotations

from enum import StrEnum


class ArtifactState(StrEnum):
    DERIVED_PREVIEW = "derived_preview"
    READY_TO_MATERIALIZE = "ready_to_materialize"
    MATERIALIZED = "materialized"
    VALIDATED = "validated"
    CANDIDATE_FOR_ACTIVATION = "candidate_for_activation"
    ACTIVE = "active"
    ARCHIVED = "archived"
    LEGACY = "legacy"
    BROKEN = "broken"


STATE_DESCRIPTIONS: dict[ArtifactState, str] = {
    ArtifactState.DERIVED_PREVIEW: (
        "Salida generada para revision. No escribe artefacto operativo y no puede "
        "ser consumida como materializada."
    ),
    ArtifactState.READY_TO_MATERIALIZE: (
        "Salida derivada validada y lista para materializacion posterior. Todavia "
        "no es operativa."
    ),
    ArtifactState.MATERIALIZED: (
        "Artefacto escrito en filesystem o registry sandbox con manifest o "
        "trazabilidad minima. No necesariamente activo."
    ),
    ArtifactState.VALIDATED: (
        "Artefacto materializado que paso validaciones declarativas. No es activo."
    ),
    ArtifactState.CANDIDATE_FOR_ACTIVATION: (
        "Artefacto validado y aprobado como candidato futuro. No es activo."
    ),
    ArtifactState.ACTIVE: (
        "Artefacto operativo PASSED, usable por el backend o flujo correspondiente."
    ),
    ArtifactState.ARCHIVED: (
        "Artefacto retirado del flujo activo y conservado por trazabilidad."
    ),
    ArtifactState.LEGACY: (
        "Artefacto historico conservado, fuera del flujo nuevo salvo recuperacion formal."
    ),
    ArtifactState.BROKEN: (
        "Artefacto inconsistente, incompleto o fallido. No puede usarse."
    ),
}

VALID_TRANSITIONS: dict[ArtifactState, set[ArtifactState]] = {
    ArtifactState.DERIVED_PREVIEW: {
        ArtifactState.READY_TO_MATERIALIZE,
        ArtifactState.BROKEN,
    },
    ArtifactState.READY_TO_MATERIALIZE: {
        ArtifactState.MATERIALIZED,
        ArtifactState.BROKEN,
    },
    ArtifactState.MATERIALIZED: {
        ArtifactState.VALIDATED,
        ArtifactState.CANDIDATE_FOR_ACTIVATION,
        ArtifactState.ACTIVE,
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    },
    ArtifactState.VALIDATED: {
        ArtifactState.CANDIDATE_FOR_ACTIVATION,
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    },
    ArtifactState.CANDIDATE_FOR_ACTIVATION: {
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    },
    ArtifactState.ACTIVE: {
        ArtifactState.ARCHIVED,
        ArtifactState.BROKEN,
    },
    ArtifactState.ARCHIVED: {
        ArtifactState.BROKEN,
    },
    ArtifactState.LEGACY: {
        ArtifactState.READY_TO_MATERIALIZE,
        ArtifactState.BROKEN,
    },
    ArtifactState.BROKEN: {
        ArtifactState.DERIVED_PREVIEW,
        ArtifactState.READY_TO_MATERIALIZE,
    },
}


def coerce_artifact_state(state: ArtifactState | str) -> ArtifactState | None:
    try:
        return state if isinstance(state, ArtifactState) else ArtifactState(str(state))
    except ValueError:
        return None


def is_derived(state: ArtifactState | str) -> bool:
    return coerce_artifact_state(state) in {
        ArtifactState.DERIVED_PREVIEW,
        ArtifactState.READY_TO_MATERIALIZE,
    }


def is_materialized(state: ArtifactState | str) -> bool:
    return coerce_artifact_state(state) in {
        ArtifactState.MATERIALIZED,
        ArtifactState.VALIDATED,
        ArtifactState.CANDIDATE_FOR_ACTIVATION,
        ArtifactState.ACTIVE,
    }


def is_operational(state: ArtifactState | str, *, has_traceability: bool = True) -> bool:
    return coerce_artifact_state(state) is ArtifactState.ACTIVE and has_traceability


def is_visible_as_usable(state: ArtifactState | str, *, has_traceability: bool = True) -> bool:
    return is_operational(state, has_traceability=has_traceability)


def can_materialize(state: ArtifactState | str) -> bool:
    return coerce_artifact_state(state) is ArtifactState.READY_TO_MATERIALIZE


def can_activate(state: ArtifactState | str, *, has_traceability: bool = True) -> bool:
    return coerce_artifact_state(state) is ArtifactState.CANDIDATE_FOR_ACTIVATION and has_traceability


def must_not_be_used_as_operational(state: ArtifactState | str) -> bool:
    return not is_operational(state)


def is_valid_transition(
    from_state: ArtifactState | str,
    to_state: ArtifactState | str,
) -> bool:
    current = coerce_artifact_state(from_state)
    target = coerce_artifact_state(to_state)
    if current is None or target is None:
        return False
    return target in VALID_TRANSITIONS[current]


def require_valid_transition(
    from_state: ArtifactState | str,
    to_state: ArtifactState | str,
) -> ArtifactState:
    current = coerce_artifact_state(from_state)
    target = coerce_artifact_state(to_state)
    if current is None:
        raise ValueError(f"Estado de artefacto desconocido: {from_state}")
    if target is None:
        raise ValueError(f"Estado de artefacto desconocido: {to_state}")
    if target not in VALID_TRANSITIONS[current]:
        raise ValueError(f"Transicion de artefacto invalida: {current.value} -> {target.value}")
    return target
