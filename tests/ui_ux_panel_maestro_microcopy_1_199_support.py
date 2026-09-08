"""Decision-unit normalization support for UI/UX 1.199.

This module is test-only. It groups existing 1.198 records only when a
single decision can honestly govern every member under the same authority.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import re
import unicodedata

from ui_ux_panel_maestro_microcopy_1_198_support import (
    CorpusItem,
    DecisionPackageRow,
    SemanticClassification,
    ContractSurfaceMap,
    contract_surface_maps,
    corpus_items,
    decision_package_rows,
    protected_files_match_baseline,
    semantic_classifications,
)


N3_RESOLUTIONS = (
    "DERIVABLE_WITH_EXISTING_CONTRACT",
    "DERIVABLE_WITH_EXISTING_STYLE_RULE",
    "DERIVABLE_WITH_CONSISTENCY_RULE",
    "DERIVABLE_WITH_GEOMETRY_RULE",
    "DIRECTION_REQUIRED_TRUE",
    "CONTRACT_CHANGE_REQUIRED",
    "KEEP_NO_DECISION",
)
DETERMINISM_LEVELS = (
    "LEVEL_A_FULLY_DETERMINISTIC",
    "LEVEL_B_PREAUTHORIZED_PATTERN",
    "LEVEL_C_DIRECTION_PACKAGE",
    "LEVEL_D_CONTRACT_CHANGE",
)


GROUPING_TYPES = (
    "EXACT_DUPLICATE_UNIT",
    "SEMANTIC_EQUIVALENT_UNIT",
    "CONTEXTUAL_VARIANT_UNIT",
    "CONTRACT_BOUND_UNIT",
    "EDITORIAL_PATTERN_UNIT",
    "SINGLETON_DECISION_UNIT",
)
MERGE_POLICIES = ("SHARED_DECISION", "DO_NOT_MERGE")
CONTRACT_CLASSIFICATIONS = {
    "CONTRACTUAL_EXACT",
    "CONTRACTUAL_EXPLANATORY",
    "BLOCKER",
    "WARNING",
    "ERROR",
    "FALLBACK",
    "NO_PAYLOAD",
    "NOT_AVAILABLE",
    "READINESS_LABEL",
    "STATE_LABEL",
    "ACTION_SENSITIVE",
    "AMBIGUOUS_REQUIRES_DIRECTION",
    "ACCESSIBILITY_COPY",
}
EDITORIAL_CLASSIFICATIONS = {
    "EDITORIAL_SAFE",
    "NAVIGATION",
    "FORM_LABEL",
    "PLACEHOLDER",
}


@dataclass(frozen=True)
class DecisionUnit:
    decision_unit_id: str
    grouping_type: str
    merge_policy: str
    member_ids: tuple[str, ...]
    occurrence_count: int
    texts: tuple[str, ...]
    files: tuple[str, ...]
    surfaces: tuple[str, ...]
    contracts: tuple[str, ...]
    classifications: tuple[str, ...]
    decision_categories: tuple[str, ...]
    recommendations: tuple[str, ...]
    risks: tuple[str, ...]
    shared_decision: bool
    rationale: str


@dataclass(frozen=True)
class DirectionCompression:
    decision_unit_id: str
    resolution: str
    source_decision_category: str
    grouping_type: str
    occurrence_count: int
    original_direction_required: bool
    rationale: str


@dataclass(frozen=True)
class DeterminismBoundary:
    decision_unit_id: str
    level: str
    resolution: str
    occurrence_count: int
    evidence: str
    condition_to_automate: str
    decision_owner: str


@dataclass(frozen=True)
class DirectionPackage:
    direction_package_id: str
    name: str
    level: str
    unit_ids: tuple[str, ...]
    occurrence_count: int
    surfaces: tuple[str, ...]
    contracts: tuple[str, ...]
    representative_texts: tuple[str, ...]
    problem: str
    existing_rule: str
    why_agent_cannot_decide: str
    options: tuple[str, ...]
    recommendation: str
    confidence: str
    minimum_decision: str
    automate_after: str
    remains_blocked: str


@dataclass(frozen=True)
class ExecutionStation:
    graph: str
    station_index: int
    station_id: str
    name: str
    scope: str
    occurrence_count: int
    files: tuple[str, ...]
    tests: tuple[str, ...]
    gate: str
    commit_prefix: str
    rollback: str
    frontier: str


def _exact_key(item: CorpusItem) -> str:
    return item.text.casefold().strip()


def _semantic_key(item: CorpusItem) -> str:
    normalized = unicodedata.normalize("NFC", item.text.casefold())
    return " ".join(re.findall(r"\w+", normalized, flags=re.UNICODE))


def _authority_key(
    item: CorpusItem,
    classification: SemanticClassification,
    mapping: ContractSurfaceMap,
    row: DecisionPackageRow,
) -> tuple[str, str, str]:
    # Surface is intentionally excluded: the same approved contract vocabulary
    # may govern several surfaces, while contract/classification/category stay
    # fixed. Different authorities never share a unit.
    return (classification.classification, mapping.contract, row.decision_category)


def _unique(values: list[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def decision_units(items: list[CorpusItem] | None = None) -> list[DecisionUnit]:
    entries = items if items is not None else corpus_items()
    classifications = {item.microcopy_id: item for item in semantic_classifications(entries)}
    mappings = {item.microcopy_id: item for item in contract_surface_maps(entries)}
    rows = {item.microcopy_id: item for item in decision_package_rows(entries)}
    positions = {item.microcopy_id: index for index, item in enumerate(entries)}
    exact_groups: dict[tuple[str, tuple[str, str, str]], list[CorpusItem]] = defaultdict(list)
    semantic_groups: dict[tuple[str, tuple[str, str, str]], list[CorpusItem]] = defaultdict(list)
    text_groups: dict[str, list[CorpusItem]] = defaultdict(list)
    for item in entries:
        authority = _authority_key(item, classifications[item.microcopy_id], mappings[item.microcopy_id], rows[item.microcopy_id])
        exact_groups[(_exact_key(item), authority)].append(item)
        semantic_groups[(_semantic_key(item), authority)].append(item)
        text_groups[_exact_key(item)].append(item)

    assigned: set[str] = set()
    raw: list[tuple[str, str, list[CorpusItem], str]] = []

    def register(kind: str, policy: str, members: list[CorpusItem], rationale: str) -> None:
        raw.append((kind, policy, members, rationale))
        assigned.update(item.microcopy_id for item in members)

    for key, members in sorted(exact_groups.items(), key=lambda pair: repr(pair[0])):
        if len(members) > 1:
            register(
                "EXACT_DUPLICATE_UNIT",
                "SHARED_DECISION",
                members,
                "Exact text, classification, contract authority and decision category match.",
            )
    for key, members in sorted(semantic_groups.items(), key=lambda pair: repr(pair[0])):
        remaining = [item for item in members if item.microcopy_id not in assigned]
        if len(remaining) > 1:
            register(
                "SEMANTIC_EQUIVALENT_UNIT",
                "SHARED_DECISION",
                remaining,
                "Punctuation/casing/spacing differs, but meaning and contract authority match.",
            )
    for item in entries:
        if item.microcopy_id in assigned:
            continue
        classification = classifications[item.microcopy_id].classification
        if len(text_groups[_exact_key(item)]) > 1:
            register(
                "CONTEXTUAL_VARIANT_UNIT",
                "DO_NOT_MERGE",
                [item],
                "The text repeats under a different context or authority; no shared decision is inferred.",
            )
        elif classification in CONTRACT_CLASSIFICATIONS:
            register(
                "CONTRACT_BOUND_UNIT",
                "DO_NOT_MERGE",
                [item],
                "Contract/state meaning is unique in this corpus slice; broad grouping would change authority.",
            )
        elif classification in EDITORIAL_CLASSIFICATIONS:
            register(
                "EDITORIAL_PATTERN_UNIT",
                "DO_NOT_MERGE",
                [item],
                "Editorial similarity alone is insufficient to share a decision.",
            )
        else:
            register(
                "SINGLETON_DECISION_UNIT",
                "DO_NOT_MERGE",
                [item],
                "No objective equivalence rule applies.",
            )

    raw.sort(key=lambda group: min(positions[item.microcopy_id] for item in group[2]))
    result: list[DecisionUnit] = []
    for index, (kind, policy, members, rationale) in enumerate(raw, 1):
        member_ids = tuple(item.microcopy_id for item in members)
        member_classifications = [classifications[item.microcopy_id] for item in members]
        member_mappings = [mappings[item.microcopy_id] for item in members]
        member_rows = [rows[item.microcopy_id] for item in members]
        result.append(DecisionUnit(
            decision_unit_id=f"DU_{index:04d}",
            grouping_type=kind,
            merge_policy=policy,
            member_ids=member_ids,
            occurrence_count=len(members),
            texts=_unique([item.text for item in members]),
            files=_unique([item.file for item in members]),
            surfaces=_unique([item.surface for item in members]),
            contracts=_unique([mapping.contract for mapping in member_mappings]),
            classifications=_unique([classification.classification for classification in member_classifications]),
            decision_categories=_unique([row.decision_category for row in member_rows]),
            recommendations=_unique([row.recommendation for row in member_rows]),
            risks=_unique([classification.risk for classification in member_classifications]),
            shared_decision=policy == "SHARED_DECISION",
            rationale=rationale,
        ))
    return result


def decision_unit_membership(units: list[DecisionUnit] | None = None) -> dict[str, str]:
    result: dict[str, str] = {}
    for unit in units if units is not None else decision_units():
        for member_id in unit.member_ids:
            if member_id in result:
                raise AssertionError(f"member assigned twice: {member_id}")
            result[member_id] = unit.decision_unit_id
    return result


def decision_unit_summary(units: list[DecisionUnit] | None = None) -> dict[str, int]:
    entries = units if units is not None else decision_units()
    return {
        "TOTAL_DECISION_UNITS": len(entries),
        "TOTAL_OCCURRENCES": sum(unit.occurrence_count for unit in entries),
        "SHARED_DECISION_UNITS": sum(unit.shared_decision for unit in entries),
        "SHARED_DECISION_OCCURRENCES": sum(unit.occurrence_count for unit in entries if unit.shared_decision),
        "DO_NOT_MERGE_UNITS": sum(unit.merge_policy == "DO_NOT_MERGE" for unit in entries),
        "DO_NOT_MERGE_OCCURRENCES": sum(unit.occurrence_count for unit in entries if unit.merge_policy == "DO_NOT_MERGE"),
    }


def protected_product_is_unchanged() -> bool:
    return protected_files_match_baseline() == []


_ANTI_ACTION_TERMS = (
    "no runtime",
    "no_runtime",
    "no-runtime",
    "no execution",
    "no_execution",
    "no-execution",
    "no dispatch",
    "no_dispatch",
    "no-dispatch",
    "no submit",
    "no_submit",
    "no-submit",
    "no cta",
    "no permission",
    "read-only",
    "read only",
    "no live runtime",
    "sin permiso",
    "no ejecuta",
    "no envia",
    "no envía",
    "no activa",
    "no corre",
    "no dispara",
    "no delivery",
)


def _contains_anti_action_boundary(unit: DecisionUnit) -> bool:
    return any(
        any(term in text.casefold() for term in _ANTI_ACTION_TERMS)
        for text in unit.texts
    ) or any("allowed_actions" in contract for contract in unit.contracts)


def _resolve_unit(unit: DecisionUnit) -> tuple[str, str]:
    category = unit.decision_categories[0]
    classifications = set(unit.classifications)
    if category == "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE":
        return "CONTRACT_CHANGE_REQUIRED", "Exact vocabulary needs a future contract version."
    if category == "SAFE_TO_KEEP":
        return "KEEP_NO_DECISION", "No deterministic evidence justifies a change."
    if category == "GEOMETRY_DRIVEN_CANDIDATE":
        return "DERIVABLE_WITH_GEOMETRY_RULE", "Existing browser evidence defines a bounded geometry review."
    if category == "EDITORIAL_CANDIDATE":
        if classifications <= EDITORIAL_CLASSIFICATIONS:
            return "DERIVABLE_WITH_EXISTING_STYLE_RULE", "Existing editorial/presentational rules can preserve meaning."
        return "DIRECTION_REQUIRED_TRUE", "The unit is not safely reducible to a presentational rule."
    if category == "CONSISTENCY_CANDIDATE":
        if unit.shared_decision:
            return "DERIVABLE_WITH_CONSISTENCY_RULE", "Existing equivalent wording supplies the precedent; keep the current value."
        return "DIRECTION_REQUIRED_TRUE", "Contextual variants cannot share a canonical choice without Direction."
    if category == "READINESS_SENSITIVE":
        if classifications <= {"READINESS_LABEL", "STATE_LABEL", "NO_PAYLOAD", "NOT_AVAILABLE"}:
            return "DERIVABLE_WITH_EXISTING_CONTRACT", "Existing readiness/absence vocabulary already defines the boundary."
        return "DIRECTION_REQUIRED_TRUE", "The readiness meaning is not isolated from another authority."
    if category == "AMBIGUOUS_REQUIRES_DIRECTION":
        if unit.shared_decision:
            return "DERIVABLE_WITH_CONSISTENCY_RULE", "Equivalent anti-action wording supplies an existing precedent."
        if _contains_anti_action_boundary(unit):
            return "DERIVABLE_WITH_EXISTING_CONTRACT", "The current anti-action or declared-data contract resolves the role."
        return "DIRECTION_REQUIRED_TRUE", "The source still permits more than one honest semantic reading."
    if category == "ACTION_PERMISSION_SENSITIVE":
        return "DIRECTION_REQUIRED_TRUE", "Action/authority meaning cannot be inferred without a product decision."
    if category == "CONTRACT_SENSITIVE_CANDIDATE":
        return "DIRECTION_REQUIRED_TRUE", "Contract-sensitive explanation needs owner review before wording changes."
    return "DIRECTION_REQUIRED_TRUE", "No safe deterministic rule applies."


def direction_compression(units: list[DecisionUnit] | None = None) -> list[DirectionCompression]:
    entries = units if units is not None else decision_units()
    result: list[DirectionCompression] = []
    for unit in entries:
        resolution, rationale = _resolve_unit(unit)
        result.append(DirectionCompression(
            decision_unit_id=unit.decision_unit_id,
            resolution=resolution,
            source_decision_category=unit.decision_categories[0],
            grouping_type=unit.grouping_type,
            occurrence_count=unit.occurrence_count,
            original_direction_required=unit.recommendations[0] == "DIRECTION_REQUIRED",
            rationale=rationale,
        ))
    return result


def direction_compression_summary(
    units: list[DecisionUnit] | None = None,
) -> dict[str, int]:
    entries = direction_compression(units)
    return {
        "ORIGINAL_DIRECTION_REQUIRED_ITEMS": sum(item.occurrence_count for item in entries if item.original_direction_required),
        "ORIGINAL_DIRECTION_REQUIRED_UNITS": sum(item.original_direction_required for item in entries),
        "TOTAL_DIRECTION_REQUIRED_TRUE_ITEMS": sum(item.occurrence_count for item in entries if item.resolution == "DIRECTION_REQUIRED_TRUE" and item.original_direction_required),
        "TOTAL_DIRECTION_REQUIRED_TRUE_UNITS": sum(item.resolution == "DIRECTION_REQUIRED_TRUE" and item.original_direction_required for item in entries),
        "TOTAL_DERIVABLE_WITH_EXISTING_CONTRACT_ITEMS": sum(item.occurrence_count for item in entries if item.resolution == "DERIVABLE_WITH_EXISTING_CONTRACT" and item.original_direction_required),
        "TOTAL_DERIVABLE_WITH_EXISTING_CONTRACT_UNITS": sum(item.resolution == "DERIVABLE_WITH_EXISTING_CONTRACT" and item.original_direction_required for item in entries),
        "TOTAL_DERIVABLE_WITH_CONSISTENCY_RULE_ITEMS": sum(item.occurrence_count for item in entries if item.resolution == "DERIVABLE_WITH_CONSISTENCY_RULE" and item.original_direction_required),
        "TOTAL_DERIVABLE_WITH_CONSISTENCY_RULE_UNITS": sum(item.resolution == "DERIVABLE_WITH_CONSISTENCY_RULE" and item.original_direction_required for item in entries),
    }


def determinism_boundary(units: list[DecisionUnit] | None = None) -> list[DeterminismBoundary]:
    compressed = {item.decision_unit_id: item for item in direction_compression(units)}
    result: list[DeterminismBoundary] = []
    for unit in units if units is not None else decision_units():
        item = compressed[unit.decision_unit_id]
        if item.resolution in {"KEEP_NO_DECISION", "DERIVABLE_WITH_EXISTING_CONTRACT"}:
            level = "LEVEL_A_FULLY_DETERMINISTIC"
            evidence = "Existing contract or explicit keep evidence supplies one safe outcome."
            condition = "Run only preservation, ID, source and protected-diff checks; no wording edit is implied."
            owner = "AGENT"
        elif item.resolution in {
            "DERIVABLE_WITH_EXISTING_STYLE_RULE",
            "DERIVABLE_WITH_CONSISTENCY_RULE",
            "DERIVABLE_WITH_GEOMETRY_RULE",
        }:
            level = "LEVEL_B_PREAUTHORIZED_PATTERN"
            evidence = "A repeatable editorial, consistency or geometry pattern exists, but a one-time rule approval is still needed."
            condition = "Direction approves the pattern and stable ID allowlist once; the agent then applies only that rule."
            owner = "DIRECTION_PATTERN_OWNER"
        elif item.resolution == "DIRECTION_REQUIRED_TRUE":
            level = "LEVEL_C_DIRECTION_PACKAGE"
            evidence = "More than one honest interpretation or contextual choice remains."
            condition = "Direction selects an option for the coherent package; no record-by-record polling is required."
            owner = "DIRECTION"
        else:
            level = "LEVEL_D_CONTRACT_CHANGE"
            evidence = "The current exact vocabulary or boundary cannot change under the active contract."
            condition = "Version the contract/vocabulary first; keep the current record unchanged until then."
            owner = "CONTRACT_OWNER"
        result.append(DeterminismBoundary(
            decision_unit_id=unit.decision_unit_id,
            level=level,
            resolution=item.resolution,
            occurrence_count=unit.occurrence_count,
            evidence=evidence,
            condition_to_automate=condition,
            decision_owner=owner,
        ))
    return result


def determinism_boundary_summary(
    units: list[DecisionUnit] | None = None,
) -> dict[str, int]:
    entries = determinism_boundary(units)
    return {
        "TOTAL_LEVEL_A_UNITS": sum(item.level == "LEVEL_A_FULLY_DETERMINISTIC" for item in entries),
        "TOTAL_LEVEL_A_OCCURRENCES": sum(item.occurrence_count for item in entries if item.level == "LEVEL_A_FULLY_DETERMINISTIC"),
        "TOTAL_LEVEL_B_UNITS": sum(item.level == "LEVEL_B_PREAUTHORIZED_PATTERN" for item in entries),
        "TOTAL_LEVEL_B_OCCURRENCES": sum(item.occurrence_count for item in entries if item.level == "LEVEL_B_PREAUTHORIZED_PATTERN"),
        "TOTAL_LEVEL_C_UNITS": sum(item.level == "LEVEL_C_DIRECTION_PACKAGE" for item in entries),
        "TOTAL_LEVEL_C_OCCURRENCES": sum(item.occurrence_count for item in entries if item.level == "LEVEL_C_DIRECTION_PACKAGE"),
        "TOTAL_LEVEL_D_UNITS": sum(item.level == "LEVEL_D_CONTRACT_CHANGE" for item in entries),
        "TOTAL_LEVEL_D_OCCURRENCES": sum(item.occurrence_count for item in entries if item.level == "LEVEL_D_CONTRACT_CHANGE"),
    }


_PACKAGE_DEFINITIONS = {
    "PKG_B_EDITORIAL_STYLE": {
        "name": "Regla de estilo editorial y presentacional",
        "level": "LEVEL_B_PREAUTHORIZED_PATTERN",
        "problem": "Hay copy editorial, labels, navegacion, formularios y placeholders que podrian ordenarse sin tocar el contrato.",
        "existing_rule": "Preservar significado, i18n, nombres accesibles y densidad; no convertir labels en acciones.",
        "why": "El agente puede detectar el patron, pero la preferencia de idioma, tono o casing sigue siendo de Direccion.",
        "options": ("A - Mantener el wording actual.", "B - Aprobar una regla editorial acotada por IDs.", "C - Posponer toda normalizacion."),
        "recommendation": "A para el estado actual; B solo con allowlist estable y revision de accesibilidad/localizacion.",
        "confidence": "ALTA para el limite; MEDIA para elegir una preferencia editorial.",
        "minimum": "Aprobar o rechazar una regla de estilo, no cada ocurrencia.",
        "automate": "Aplicar solo IDs aprobados, generar diff/snapshots y validar HTML/i18n/ARIA.",
        "blocked": "Wording contractual, permisos, acciones, readiness y estados exactos.",
    },
    "PKG_B_CONSISTENCY_RULE": {
        "name": "Regla de consistencia sin perdida de contexto",
        "level": "LEVEL_B_PREAUTHORIZED_PATTERN",
        "problem": "Hay repeticiones equivalentes de labels, casing y tokens que no deben convertirse en una mezcla global.",
        "existing_rule": "Compartir solo texto, autoridad y decision category equivalentes; preservar variantes contextuales.",
        "why": "La herramienta puede demostrar equivalencia, pero Direccion debe decidir si quiere una politica de canonizacion.",
        "options": ("A - Preservar cada contexto.", "B - Canonizar solo equivalentes con misma autoridad.", "C - Intentar una canonizacion amplia."),
        "recommendation": "A; B es el maximo patron seguro futuro. C queda rechazada por riesgo de borrar contexto.",
        "confidence": "ALTA sobre la separacion de autoridades; MEDIA sobre la preferencia canonica.",
        "minimum": "Elegir una politica de consistencia para el corpus, no textos uno por uno.",
        "automate": "Aplicar la politica a unidades equivalentes y rechazar merges contextuales.",
        "blocked": "Fusion de superficies o autoridades contractuales diferentes.",
    },
    "PKG_B_GEOMETRY_REMEDIATION": {
        "name": "Owner de riesgos geometricos locales",
        "level": "LEVEL_B_PREAUTHORIZED_PATTERN",
        "problem": "Hay 15 ocurrencias asociadas a wrapping o overflow local sin overflow global.",
        "existing_rule": "Medir geometry, conservar el texto contractual y resolver primero con layout/CSS scoped si corresponde.",
        "why": "La medicion es objetiva, pero asignar el remedio a CSS, layout o wording es una decision de ownership.",
        "options": ("A - Mantener y observar.", "B - Autorizar una correccion CSS/layout scoped.", "C - Abrir una revision de wording contractual."),
        "recommendation": "B para el drawer/boxes locales, manteniendo wording sin cambios.",
        "confidence": "ALTA en la evidencia; MEDIA en el owner final del remedio.",
        "minimum": "Elegir owner y limite de la remediation geometrica.",
        "automate": "Repetir viewport/resize/console checks y bloquear overflow global.",
        "blocked": "Cambios de copy, severidad o contrato por una medicion local.",
    },
    "PKG_C_CONTEXTUAL_VARIANTS": {
        "name": "Variantes contextuales que no se deben mezclar",
        "level": "LEVEL_C_DIRECTION_PACKAGE",
        "problem": "36 ocurrencias parecen consistentes por texto, pero pertenecen a contextos que no comparten una autoridad unica.",
        "existing_rule": "El mismo texto no implica la misma decision cuando cambia superficie, estado o contrato.",
        "why": "Solo Direccion puede preferir uniformidad sobre contexto sin alterar la interpretacion de cada superficie.",
        "options": ("A - Mantener las variantes por contexto.", "B - Unificar solo dentro de la misma autoridad.", "C - Unificar todas las variantes."),
        "recommendation": "A; B requiere una regla de autoridad explícita. C no es segura.",
        "confidence": "ALTA en que no deben fusionarse automaticamente.",
        "minimum": "Elegir preservar contexto o autorizar una regla de autoridad.",
        "automate": "Validar que ningun merge futuro cruce la autoridad aprobada.",
        "blocked": "Canonizacion global o reescritura automatica entre superficies.",
    },
    "PKG_C_CONTRACT_SENSITIVE": {
        "name": "Copy explicativo y diagnostico contract-sensitive",
        "level": "LEVEL_C_DIRECTION_PACKAGE",
        "problem": "139 ocurrencias explican limites, warnings, errors o evidencia y pueden cambiar como se interpreta el contrato.",
        "existing_rule": "Backend contract authoritative, UI read-only, deny-by-default y sin runtime/execution.",
        "why": "El agente puede preservar el limite, pero no elegir tono, severidad o detalle que Direccion considere correcto.",
        "options": ("A - Mantener exactamente.", "B - Aprobar una revision acotada con Contract Owner.", "C - Proponer cambio contractual separado."),
        "recommendation": "A hasta que exista una necesidad demostrable y un owner contractual.",
        "confidence": "ALTA en el riesgo y en la frontera de no cambio.",
        "minimum": "Decidir si se mantiene el texto o se abre una revision contractual.",
        "automate": "Solo snapshots, trazabilidad y checks de vocabulario aprobado.",
        "blocked": "Cambiar significado, severidad, source/status/fallback o limites.",
    },
    "PKG_C_ACTION_PERMISSION": {
        "name": "Interpretacion de acciones y permisos",
        "level": "LEVEL_C_DIRECTION_PACKAGE",
        "problem": "15 ocurrencias usan vocabulario que podria leerse como accion, label o autoridad.",
        "existing_rule": "allowed_actions es dato declarado, no CTA; no se infieren permisos.",
        "why": "El agente no puede elegir por Direccion si la palabra debe ser boundary, etiqueta o permiso.",
        "options": ("A - Mantener como dato/boundary read-only.", "B - Definir vocabulario contractual explicito.", "C - Autorizar una accion o permiso nuevo."),
        "recommendation": "A; B solo mediante version contractual. C esta fuera del alcance 1.199.",
        "confidence": "ALTA en que no puede convertirse en CTA.",
        "minimum": "Elegir el rol semantico, sin habilitar ejecucion.",
        "automate": "Rechazar CTA/submit/dispatch/runtime y validar el vocabulario elegido.",
        "blocked": "Acciones operativas, permisos inferidos y payload v2.",
    },
    "PKG_C_AMBIGUOUS_ROLE": {
        "name": "Rol semantico de copy ambiguo",
        "level": "LEVEL_C_DIRECTION_PACKAGE",
        "problem": "38 ocurrencias siguen admitiendo mas de una lectura honesta despues de contrato, precedentes y consistencia.",
        "existing_rule": "No inventar significado; separar label, boundary, estado y permiso.",
        "why": "Resolverlas requiere una preferencia de producto o semantica que no se deriva de evidencia unica.",
        "options": ("A - Mantener la formulacion actual.", "B - Declararla explicitamente como boundary/dato.", "C - Redefinir su rol en un cambio contractual."),
        "recommendation": "A mientras no exista una contradiccion demostrada; B antes que cualquier alternativa operativa.",
        "confidence": "ALTA en la necesidad de Direccion; MEDIA en la opcion final.",
        "minimum": "Elegir el rol conceptual del paquete, no reescribir fila por fila.",
        "automate": "Aplicar la decision al allowlist aprobado y bloquear interpretaciones no aprobadas.",
        "blocked": "Inferir permiso, runtime, ejecucion, dispatch o submit.",
    },
    "PKG_D_CONTRACT_VOCABULARY": {
        "name": "Version futura del vocabulario contractual",
        "level": "LEVEL_D_CONTRACT_CHANGE",
        "problem": "692 ocurrencias son vocabulario exacto o limites que no pueden cambiar bajo el contrato actual.",
        "existing_rule": "Preservar blockers, source/status/fallback, readiness, no_payload, not_available y deny-by-default.",
        "why": "No es una preferencia editorial: cambiarlo desincronizaria el contrato y la lectura del operador.",
        "options": ("A - No cambiar y mantener el contrato vigente.", "B - Planificar una nueva version contractual.", "C - Rechazar cualquier cambio de vocabulario en esta etapa."),
        "recommendation": "A en 1.199; B solo como trabajo contractual posterior separado.",
        "confidence": "ALTA.",
        "minimum": "Decidir si existe necesidad de versionar el contrato; no aprobar wording aqui.",
        "automate": "Solo despues de versionar contrato, actualizar allowlists y ejecutar regresion completa.",
        "blocked": "Toda edicion de las 692 ocurrencias bajo el contrato actual.",
    },
}


def _package_key(unit: DecisionUnit, boundary: DeterminismBoundary) -> str | None:
    if boundary.resolution == "DERIVABLE_WITH_EXISTING_STYLE_RULE":
        return "PKG_B_EDITORIAL_STYLE"
    if boundary.resolution == "DERIVABLE_WITH_CONSISTENCY_RULE":
        return "PKG_B_CONSISTENCY_RULE"
    if boundary.resolution == "DERIVABLE_WITH_GEOMETRY_RULE":
        return "PKG_B_GEOMETRY_REMEDIATION"
    if boundary.resolution == "CONTRACT_CHANGE_REQUIRED":
        return "PKG_D_CONTRACT_VOCABULARY"
    if boundary.resolution == "DIRECTION_REQUIRED_TRUE":
        return {
            "CONTRACT_SENSITIVE_CANDIDATE": "PKG_C_CONTRACT_SENSITIVE",
            "ACTION_PERMISSION_SENSITIVE": "PKG_C_ACTION_PERMISSION",
            "AMBIGUOUS_REQUIRES_DIRECTION": "PKG_C_AMBIGUOUS_ROLE",
            "CONSISTENCY_CANDIDATE": "PKG_C_CONTEXTUAL_VARIANTS",
        }.get(unit.decision_categories[0], "PKG_C_AMBIGUOUS_ROLE")
    return None


def direction_packages(units: list[DecisionUnit] | None = None) -> list[DirectionPackage]:
    entries = units if units is not None else decision_units()
    boundaries = {item.decision_unit_id: item for item in determinism_boundary(entries)}
    grouped: dict[str, list[DecisionUnit]] = defaultdict(list)
    for unit in entries:
        key = _package_key(unit, boundaries[unit.decision_unit_id])
        if key is not None:
            grouped[key].append(unit)
    result: list[DirectionPackage] = []
    for package_id, definition in _PACKAGE_DEFINITIONS.items():
        members = grouped.get(package_id, [])
        if not members:
            continue
        result.append(DirectionPackage(
            direction_package_id=package_id,
            name=definition["name"],
            level=definition["level"],
            unit_ids=tuple(unit.decision_unit_id for unit in members),
            occurrence_count=sum(unit.occurrence_count for unit in members),
            surfaces=_unique([surface for unit in members for surface in unit.surfaces]),
            contracts=_unique([contract for unit in members for contract in unit.contracts]),
            representative_texts=_unique([text for unit in members for text in unit.texts])[:5],
            problem=definition["problem"],
            existing_rule=definition["existing_rule"],
            why_agent_cannot_decide=definition["why"],
            options=definition["options"],
            recommendation=definition["recommendation"],
            confidence=definition["confidence"],
            minimum_decision=definition["minimum"],
            automate_after=definition["automate"],
            remains_blocked=definition["blocked"],
        ))
    return result


def post_direction_execution_graph() -> tuple[ExecutionStation, ...]:
    return (
        ExecutionStation(
            "GRAPH_A_NO_DIRECTION", 1, "A1", "Preservar contrato existente",
            "170 ocurrencias derivables por contrato y checks de preservacion", 170,
            ("tests/ui_ux_panel_maestro_microcopy_1_199_support.py", "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DETERMINISM_DIRECTION_BOUNDARY_1_199.md"),
            ("tests/test_ui_ux_panel_maestro_microcopy_determinism_direction_boundary_1_199.py",),
            "POST_DIRECTION_LEVEL_A_CONTRACT_PRESERVATION_PASSED", "test(ui)",
            "Eliminar solo el artefacto futuro y conservar el contrato actual.",
            "No abre una frontera nueva.",
        ),
        ExecutionStation(
            "GRAPH_A_NO_DIRECTION", 2, "A2", "Mantener ledger sin decision",
            "30 ocurrencias KEEP_NO_DECISION", 30,
            ("tests/ui_ux_panel_maestro_microcopy_1_199_support.py", "docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_COMPRESSION_1_199.md"),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_compression_1_199.py",),
            "POST_DIRECTION_LEVEL_A_KEEP_LEDGER_PASSED", "docs(ui)",
            "Revertir solo el ledger futuro; no tocar producto.",
            "La siguiente frontera sigue siendo la aprobacion de patrones.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 1, "B1", "Compilar respuestas de Direccion",
            "Decision Sheet, IDs aprobados, opciones y restricciones", 1424,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTOR_DECISION_SHEET_1_199.md", "tests/ui_ux_panel_maestro_microcopy_1_199_support.py"),
            ("tests/test_ui_ux_panel_maestro_microcopy_director_decision_sheet_1_199.py",),
            "POST_DIRECTION_DECISION_ALLOWLIST_COMPILED", "docs(ui)",
            "Eliminar el manifest de aprobacion sin cambiar fuentes activas.",
            "Abre la aplicacion controlada de patrones.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 2, "B2", "Aplicar regla editorial aprobada",
            "PKG_B_EDITORIAL_STYLE / 295 ocurrencias", 295,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md", "ui/web/i18n_es.json"),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_EDITORIAL_ALLOWLIST_PASSED", "docs(ui) o test(ui)",
            "Revertir solo el diff futuro de IDs aprobados.",
            "La siguiente frontera es consistencia/contexto.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 3, "B3", "Aplicar regla de consistencia",
            "PKG_B_CONSISTENCY_RULE / 194 ocurrencias", 194,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_CONSISTENCY_RULE_PASSED", "docs(ui) o test(ui)",
            "Revertir solo canonizaciones aprobadas y preservar contexto.",
            "La siguiente frontera es geometria local.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 4, "B4", "Resolver owner geometrico",
            "PKG_B_GEOMETRY_REMEDIATION / 15 ocurrencias", 15,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_GEOMETRY_OWNER_PASSED", "docs(ui) o test(ui)",
            "Revertir solo el remedio scoped aprobado.",
            "La siguiente frontera son decisiones semanticas Level C.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 5, "B5", "Resolver variantes contextuales",
            "PKG_C_CONTEXTUAL_VARIANTS / 36 ocurrencias", 36,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_CONTEXT_POLICY_PASSED", "docs(ui) o test(ui)",
            "Revertir solo la politica aplicada; no cruzar autoridades.",
            "La siguiente frontera es copy contract-sensitive.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 6, "B6", "Resolver copy contract-sensitive",
            "PKG_C_CONTRACT_SENSITIVE / 139 ocurrencias", 139,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_CONTRACT_SENSITIVE_REVIEW_PASSED", "docs(ui)",
            "Revertir solo un cambio expresamente aprobado por Contract Owner.",
            "La siguiente frontera es accion/permiso.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 7, "B7", "Resolver action y permission vocabulary",
            "PKG_C_ACTION_PERMISSION / 15 ocurrencias", 15,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_ACTION_PERMISSION_BOUNDARY_PASSED", "docs(ui)",
            "Revertir vocabulario aprobado y mantener no-CTA/no-submit.",
            "La siguiente frontera es el rol semantico ambiguo.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 8, "B8", "Resolver roles ambiguos",
            "PKG_C_AMBIGUOUS_ROLE / 38 ocurrencias", 38,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "POST_DIRECTION_AMBIGUOUS_ROLE_PASSED", "docs(ui)",
            "Revertir solo la decision de role aprobada.",
            "La estacion 9 es la frontera contractual dura.",
        ),
        ExecutionStation(
            "GRAPH_B_AFTER_DIRECTION", 9, "B9", "Versionar vocabulario contractual",
            "PKG_D_CONTRACT_VOCABULARY / 692 ocurrencias", 692,
            ("docs/UI_UX_PANEL_MAESTRO_MICROCOPY_DIRECTION_PACKAGES_1_199.md",),
            ("tests/test_ui_ux_panel_maestro_microcopy_direction_packages_1_199.py",),
            "CONTRACT_VERSION_REQUIRED_BEFORE_IMPLEMENTATION", "docs(ui)",
            "No hay rollback de contrato en este bloque; mantener la version vigente.",
            "HARD_FRONTIER: requiere cambio contractual y owner separado.",
        ),
    )


def execution_graph_summary() -> dict[str, int]:
    graph = post_direction_execution_graph()
    return {
        "CURRENT_AUTOMATABLE_STATION_COUNT": sum(item.graph == "GRAPH_A_NO_DIRECTION" for item in graph),
        "POST_DIRECTION_DETERMINISTIC_STATION_COUNT": sum(item.graph == "GRAPH_B_AFTER_DIRECTION" and item.station_index < 9 for item in graph),
        "PREAUTHORIZED_POST_DIRECTION_STATION_COUNT": 3,
        "SELF_BOOTSTRAPPED_POST_DIRECTION_STATION_COUNT": 1,
        "NEXT_HARD_FRONTIER_INDEX": 9,
    }
