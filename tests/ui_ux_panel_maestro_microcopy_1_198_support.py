"""Deterministic, read-only corpus support for UI/UX 1.198.

This module is deliberately test-only. It reads product files, never writes
them, and keeps the source registry narrower than a permissive glob.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "6b9c806"
PROTECTED_PRODUCT_PATHS = (
    "ui/web/index.html",
    "ui/web/styles.css",
    "ui/web/backend-contract-widgets.js",
    "ui/web/i18n_es.json",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
    "core/backend_internal_ui_payloads.py",
    "api.py",
)
MICROCOPY_SOURCE_PATHS = (
    "ui/web/index.html",
    "ui/web/i18n_es.json",
    "ui/web/backend-contract-widgets.js",
    "ui/web/admin-panels.js",
    "ui/web/console-interactions.js",
    "ui/web/domains.js",
)
JS_SOURCE_PATHS = MICROCOPY_SOURCE_PATHS[2:]
I18N_PATH = "ui/web/i18n_es.json"
I18N_KEY_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
JS_LITERAL_RE = re.compile(r"(?P<q>['\"`])(?P<text>[^\n]*?)(?P=q)")
CONTRACT_TERMS = (
    "no_payload",
    "not_available",
    "blocked",
    "forbidden",
    "readiness",
    "allowed_actions",
    "forbidden_actions",
    "blocked_capabilities",
    "source",
    "status",
    "fallback",
    "runtime",
    "execution",
    "dispatch",
    "submit",
    "payload",
    "contract",
    "permission",
    "deny-by-default",
)
TEXTUAL_JS_HINTS = (
    " ",
    ".",
    ":",
    ",",
    "¿",
    "¡",
    "á",
    "é",
    "í",
    "ó",
    "ú",
    "ñ",
)


@dataclass(frozen=True)
class CorpusItem:
    microcopy_id: str
    text: str
    source: str
    file: str
    location: str
    surface: str
    visibility: str
    language: str
    initial_type: str
    contract_aware: bool
    active: bool
    legacy: bool
    potential_duplicate: bool
    wrapping_risk: str
    semantic_risk: str


class _HtmlCorpusParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.stack: list[tuple[str, dict[str, str]]] = []
        self.text_items: list[tuple[str, int, str]] = []
        self.attribute_items: list[tuple[str, int, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key: value or "" for key, value in attrs}
        self.stack.append((tag, attributes))
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        for name in ("aria-label", "title", "placeholder", "alt"):
            value = attributes.get(name, "").strip()
            if value:
                self.attribute_items.append((name, self.getpos()[0], value, tag))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if self.stack:
            self.stack.pop()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.text_items.append((text, self.getpos()[0], self._context()))

    def _context(self) -> str:
        ids = [attrs.get("id", "") for _, attrs in self.stack]
        classes = [attrs.get("class", "") for _, attrs in self.stack]
        return " ".join(value for value in ids + classes if value)


def _read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _surface(file: str, line: int, context: str, text: str) -> str:
    haystack = f"{context} {text}".casefold()
    if file == "ui/web/index.html":
        if 2870 <= line < 2960:
            return "MASTER_SHELL_P0"
        if 2960 <= line < 3090:
            return "P1_CONTRACT_OVERVIEW"
        if 3090 <= line < 3180:
            return "P1_BLOCKED_FORBIDDEN"
        if 3180 <= line < 3300:
            return "P1_VALIDATION_READINESS"
        if 3300 <= line < 3410:
            return "REQUEST_DRAFT_PANEL"
        if 3410 <= line < 3558:
            return "P2_P3_MATRIX_CLOSURE"
        if "widget" in haystack or "contract-aware" in haystack:
            return "CONTRACT_AWARE_WIDGETS"
        if "request-draft" in haystack or "draft" in haystack:
            return "REQUEST_DRAFT_PANEL"
        if "navigation" in haystack or "nav" in haystack:
            return "NAVIGATION"
        return "P2_P3_PANEL"
    if file == I18N_PATH:
        if haystack.startswith("navigation.") or "navigation" in haystack:
            return "NAVIGATION"
        if any(term in haystack for term in ("readiness", "status", "blocked", "warning", "error", "fallback")):
            return "I18N_CONTRACT_SURFACES"
        return "I18N_GENERAL_UI"
    if file.endswith("backend-contract-widgets.js"):
        return "CONTRACT_AWARE_WIDGETS"
    if file.endswith("console-interactions.js"):
        return "REQUEST_DRAFT_PANEL"
    if file.endswith("domains.js"):
        return "DOMAIN_ADMIN"
    if file.endswith("admin-panels.js"):
        return "ADMIN_PANELS"
    return "UNKNOWN_SURFACE"


def _initial_type(text: str, source: str) -> str:
    value = text.casefold()
    if "no_payload" in value:
        return "NO_PAYLOAD"
    if "not_available" in value:
        return "NOT_AVAILABLE"
    if "fallback" in value:
        return "FALLBACK"
    if "warning" in value or "advertencia" in value or "warning" in value:
        return "WARNING"
    if "error" in value or "error" in value or "failed" in value:
        return "ERROR"
    if any(term in value for term in ("blocked", "forbidden", "no-runtime", "no-execution", "no submit", "sin permiso")):
        return "BLOCKER"
    if "readiness" in value or "ready" in value or "pending" in value:
        return "READINESS_LABEL"
    if any(term in value for term in ("allowed_actions", "forbidden_actions", "blocked_capabilities", "permitido", "prohibid")):
        return "CONTRACTUAL_EXACT"
    if source == "i18n":
        return "EDITORIAL_SAFE"
    return "EDITORIAL_SAFE"


def _risk(text: str, initial_type: str) -> str:
    value = text.casefold()
    if initial_type in {"BLOCKER", "NO_PAYLOAD", "NOT_AVAILABLE", "READINESS_LABEL", "ERROR", "WARNING", "FALLBACK", "CONTRACTUAL_EXACT"}:
        return "RISK_3_CONTRACT_SENSITIVE"
    if any(term in value for term in ("permit", "action", "execute", "dispatch", "submit", "run", "permission", "authority")):
        return "RISK_4_DIRECTION_REQUIRED"
    if len(text) > 80:
        return "RISK_1_PRESENTATIONAL"
    return "RISK_0_EDITORIAL"


def _wrapping_risk(text: str) -> str:
    if len(text) >= 120:
        return "WRAP_RISK"
    if len(text) >= 72:
        return "DENSITY_RISK"
    return "NO_ISSUE"


def _is_contract_aware(surface: str, text: str) -> bool:
    value = text.casefold()
    return surface in {
        "MASTER_SHELL_P0",
        "P1_CONTRACT_OVERVIEW",
        "P1_BLOCKED_FORBIDDEN",
        "P1_VALIDATION_READINESS",
        "REQUEST_DRAFT_PANEL",
        "P2_P3_MATRIX_CLOSURE",
        "CONTRACT_AWARE_WIDGETS",
        "I18N_CONTRACT_SURFACES",
    } or any(term in value for term in CONTRACT_TERMS)


def _flatten_i18n(value: object, prefix: str = "") -> list[tuple[str, str]]:
    if isinstance(value, dict):
        result: list[tuple[str, str]] = []
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            result.extend(_flatten_i18n(child, path))
        return result
    if isinstance(value, str):
        return [(prefix, value)]
    return []


def _js_literals(file: str) -> Iterable[CorpusItem]:
    content = _read_text(file)
    ordinal = 0
    for match in JS_LITERAL_RE.finditer(content):
        text = match.group("text").strip()
        if not text or (not any(hint in text for hint in TEXTUAL_JS_HINTS) and not any(term in text.casefold() for term in CONTRACT_TERMS)):
            continue
        ordinal += 1
        line = content.count("\n", 0, match.start()) + 1
        surface = _surface(file, line, "", text)
        initial_type = _initial_type(text, "js")
        yield CorpusItem(
            microcopy_id=f"JS_{Path(file).stem.upper()}_{line:04d}_{ordinal:03d}",
            text=text,
            source="JS_RENDERABLE_LITERAL",
            file=file,
            location=f"line {line}",
            surface=surface,
            visibility="POTENTIAL_VISIBLE",
            language="es-AR/mixed" if any(char in text for char in "áéíóúñ¿¡") else "en/mixed",
            initial_type=initial_type,
            contract_aware=_is_contract_aware(surface, text),
            active=True,
            legacy="legacy" in text.casefold(),
            potential_duplicate=False,
            wrapping_risk=_wrapping_risk(text),
            semantic_risk=_risk(text, initial_type),
        )


def corpus_items() -> list[CorpusItem]:
    items: list[CorpusItem] = []
    parser = _HtmlCorpusParser()
    html_path = ROOT / "ui/web/index.html"
    parser.feed(html_path.read_text(encoding="utf-8"))
    for index, (text, line, context) in enumerate(parser.text_items, 1):
        surface = _surface("ui/web/index.html", line, context, text)
        initial_type = _initial_type(text, "html")
        items.append(CorpusItem(
            microcopy_id=f"HTML_TEXT_{index:04d}",
            text=text,
            source="HTML_DIRECT_TEXT",
            file="ui/web/index.html",
            location=f"line {line}; context={context or 'document'}",
            surface=surface,
            visibility="VISIBLE",
            language="es-AR/mixed" if any(char in text for char in "áéíóúñ¿¡") else "en/mixed",
            initial_type=initial_type,
            contract_aware=_is_contract_aware(surface, text),
            active=True,
            legacy="legacy" in text.casefold(),
            potential_duplicate=False,
            wrapping_risk=_wrapping_risk(text),
            semantic_risk=_risk(text, initial_type),
        ))
    for index, (name, line, text, tag) in enumerate(parser.attribute_items, 1):
        surface = _surface("ui/web/index.html", line, tag, text)
        initial_type = "ACCESSIBILITY_COPY" if name == "aria-label" else "EDITORIAL_SAFE"
        items.append(CorpusItem(
            microcopy_id=f"HTML_ATTR_{index:04d}",
            text=text,
            source=f"HTML_{name.upper().replace('-', '_')}",
            file="ui/web/index.html",
            location=f"line {line}; <{tag} {name}>",
            surface=surface,
            visibility="ACCESSIBLE_ATTRIBUTE",
            language="es-AR/mixed" if any(char in text for char in "áéíóúñ¿¡") else "en/mixed",
            initial_type=initial_type,
            contract_aware=_is_contract_aware(surface, text),
            active=True,
            legacy="legacy" in text.casefold(),
            potential_duplicate=False,
            wrapping_risk=_wrapping_risk(text),
            semantic_risk=_risk(text, initial_type),
        ))
    for index, (key, text) in enumerate(_flatten_i18n(json.loads(_read_text(I18N_PATH))), 1):
        surface = _surface(I18N_PATH, index, key, text)
        initial_type = _initial_type(text, "i18n")
        items.append(CorpusItem(
            microcopy_id=f"I18N_{index:04d}_{key.replace('.', '_')}",
            text=text,
            source="I18N_VALUE",
            file=I18N_PATH,
            location=f"key {key}",
            surface=surface,
            visibility="POTENTIAL_VISIBLE",
            language="es-AR/mixed" if any(char in text for char in "áéíóúñ¿¡") else "en/mixed",
            initial_type=initial_type,
            contract_aware=_is_contract_aware(surface, text),
            active=True,
            legacy=False,
            potential_duplicate=False,
            wrapping_risk=_wrapping_risk(text),
            semantic_risk=_risk(text, initial_type),
        ))
    for file in JS_SOURCE_PATHS:
        items.extend(_js_literals(file))
    counts = Counter(item.text.casefold() for item in items)
    return [
        CorpusItem(**{**asdict(item), "potential_duplicate": counts[item.text.casefold()] > 1})
        for item in items
    ]


def corpus_digest(items: list[CorpusItem] | None = None) -> str:
    entries = items if items is not None else corpus_items()
    encoded = json.dumps([asdict(item) for item in entries], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def corpus_counts(items: list[CorpusItem] | None = None) -> dict[str, int]:
    entries = items if items is not None else corpus_items()
    return {
        "TOTAL_CORPUS_ITEMS": len(entries),
        "HTML_ITEMS": sum(item.source == "HTML_DIRECT_TEXT" or item.source.startswith("HTML_") for item in entries),
        "HTML_TEXT_ITEMS": sum(item.source == "HTML_DIRECT_TEXT" for item in entries),
        "HTML_ATTRIBUTE_ITEMS": sum(item.source.startswith("HTML_") and item.source != "HTML_DIRECT_TEXT" for item in entries),
        "I18N_ITEMS": sum(item.source == "I18N_VALUE" for item in entries),
        "JS_ITEMS": sum(item.source == "JS_RENDERABLE_LITERAL" for item in entries),
        "STATE_ITEMS": sum(item.initial_type in {"BLOCKER", "READINESS_LABEL", "CONTRACTUAL_EXACT"} for item in entries),
        "WARNING_ITEMS": sum(item.initial_type == "WARNING" for item in entries),
        "ERROR_ITEMS": sum(item.initial_type == "ERROR" for item in entries),
        "FALLBACK_ITEMS": sum(item.initial_type in {"FALLBACK", "NO_PAYLOAD", "NOT_AVAILABLE"} for item in entries),
        "EDITORIAL_ITEMS": sum(item.initial_type == "EDITORIAL_SAFE" for item in entries),
        "UNKNOWN_ITEMS": sum(item.surface == "UNKNOWN_SURFACE" for item in entries),
        "ACCESSIBILITY_ITEMS": sum(item.initial_type == "ACCESSIBILITY_COPY" for item in entries),
        "DUPLICATE_ITEMS": sum(item.potential_duplicate for item in entries),
        "CONTRACT_AWARE_ITEMS": sum(item.contract_aware for item in entries),
        "WRAP_RISK_ITEMS": sum(item.wrapping_risk == "WRAP_RISK" for item in entries),
        "DENSITY_RISK_ITEMS": sum(item.wrapping_risk == "DENSITY_RISK" for item in entries),
    }


CLASSIFICATIONS = (
    "CONTRACTUAL_EXACT",
    "CONTRACTUAL_EXPLANATORY",
    "STATE_LABEL",
    "READINESS_LABEL",
    "PERMISSION_SENSITIVE",
    "ACTION_SENSITIVE",
    "BLOCKER",
    "WARNING",
    "ERROR",
    "FALLBACK",
    "NO_PAYLOAD",
    "NOT_AVAILABLE",
    "EDITORIAL_SAFE",
    "NAVIGATION",
    "FORM_LABEL",
    "PLACEHOLDER",
    "ACCESSIBILITY_COPY",
    "LEGACY_ACTIVE",
    "LEGACY_INACTIVE",
    "AMBIGUOUS_REQUIRES_DIRECTION",
    "UNKNOWN_REQUIRES_DIRECTION",
)
RISK_LEVELS = (
    "RISK_0_EDITORIAL",
    "RISK_1_PRESENTATIONAL",
    "RISK_2_CONTRACT_ADJACENT",
    "RISK_3_CONTRACT_SENSITIVE",
    "RISK_4_DIRECTION_REQUIRED",
)


@dataclass(frozen=True)
class SemanticClassification:
    microcopy_id: str
    classification: str
    duplicate_classification: str
    reason: str
    risk: str
    future_change: str
    decision_owner: str
    contract_touched: str
    automatable: bool
    direction_required: bool
    must_remain_exact: bool


def _duplicate_classification(item: CorpusItem, entries: list[CorpusItem]) -> str:
    matching = [other for other in entries if other.text.casefold() == item.text.casefold()]
    if len(matching) <= 1:
        return "NONE"
    if len({other.surface for other in matching}) == 1 and len({other.initial_type for other in matching}) == 1:
        return "DUPLICATE_EQUIVALENT"
    return "DUPLICATE_CONTEXTUAL"


def semantic_classifications(items: list[CorpusItem] | None = None) -> list[SemanticClassification]:
    entries = items if items is not None else corpus_items()
    result: list[SemanticClassification] = []
    for item in entries:
        value = item.text.casefold()
        duplicate = _duplicate_classification(item, entries)
        classification = "EDITORIAL_SAFE"
        reason = "General copy with no demonstrated contract binding."
        risk = "RISK_0_EDITORIAL"
        future_change = "Editorial change can be automated only after a Direction-approved allowlist."
        owner = "UI_EDITORIAL_OWNER"
        contract = "NONE_DEMONSTRATED"
        automatable = True
        direction = False
        exact = False
        if item.legacy:
            classification = "LEGACY_ACTIVE" if item.active else "LEGACY_INACTIVE"
            reason = "Legacy marker is present in an active or inactive source record."
            risk = "RISK_2_CONTRACT_ADJACENT"
            future_change = "Requires a removal or migration decision before editing."
            owner = "DIRECTION"
            automatable = False
            direction = True
        elif item.initial_type == "NO_PAYLOAD":
            classification = "NO_PAYLOAD"
            reason = "Honest absence-of-payload signal; it must not become permission or availability."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Only a contract-preserving source change may update it."
            owner = "CONTRACT_OWNER"
            contract = "backend_internal_ui_payload.v1 / deny-by-default"
            automatable = False
            direction = True
            exact = True
        elif item.initial_type == "NOT_AVAILABLE":
            classification = "NOT_AVAILABLE"
            reason = "Declared unavailable state; absence does not imply an error or unlock."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Requires contract/source evidence."
            owner = "CONTRACT_OWNER"
            contract = "source/status/fallback"
            automatable = False
            direction = True
            exact = True
        elif item.initial_type == "FALLBACK":
            classification = "FALLBACK"
            reason = "Fallback or safe projection language preserves an honest boundary."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Can be templated after contract vocabulary is approved."
            owner = "CONTRACT_OWNER"
            contract = "source/status/fallback"
            automatable = False
            direction = True
            exact = True
        elif item.initial_type == "ERROR":
            classification = "ERROR"
            reason = "Error/failed diagnostic; changing tone or cause can change operator interpretation."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Requires error taxonomy and source evidence."
            owner = "CONTRACT_OWNER"
            contract = "warnings/errors"
            automatable = False
            direction = True
        elif item.initial_type == "WARNING":
            classification = "WARNING"
            reason = "Warning/diagnostic copy; it orients reading without representing live runtime."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Can be normalized only after warning taxonomy approval."
            owner = "CONTRACT_OWNER"
            contract = "warnings/errors"
            automatable = False
            direction = True
        elif item.initial_type == "BLOCKER":
            classification = "BLOCKER"
            reason = "Visible hard boundary or blocked state; it cannot imply an alternate action."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Requires contract and anti-affordance review."
            owner = "CONTRACT_OWNER"
            contract = "blocked_capabilities / forbidden_actions / deny-by-default"
            automatable = False
            direction = True
            exact = True
        elif item.initial_type == "READINESS_LABEL":
            classification = "READINESS_LABEL"
            reason = "Readiness/validation label; it must not be equated with permission or execution."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Requires readiness vocabulary approval."
            owner = "CONTRACT_OWNER"
            contract = "readiness / validation"
            automatable = False
            direction = True
            exact = True
        elif item.initial_type == "ACCESSIBILITY_COPY":
            classification = "ACCESSIBILITY_COPY"
            reason = "Accessible name or assistive copy; changes can alter control meaning."
            risk = "RISK_2_CONTRACT_ADJACENT"
            future_change = "Can be automated only after visible and accessible names are paired."
            owner = "ACCESSIBILITY_OWNER"
            contract = "surface semantics"
            automatable = False
            direction = True
        elif item.source == "I18N_VALUE" and any(term in value for term in ("crear", "editar", "eliminar", "guardar", "cancelar", "mostrar", "cerrar")):
            classification = "ACTION_SENSITIVE"
            reason = "Control-oriented i18n value; its wording may imply an action without proving authority."
            risk = "RISK_4_DIRECTION_REQUIRED"
            future_change = "Requires Direction to separate label from action/permission semantics."
            owner = "DIRECTION"
            contract = "possible UI action; no permission inferred"
            automatable = False
            direction = True
        elif any(term in value for term in ("run", "execute", "dispatch", "submit", "approve", "activate", "permiso", "permitido", "allowed")):
            classification = "AMBIGUOUS_REQUIRES_DIRECTION"
            reason = "Action/permission-like vocabulary is present, but source evidence alone cannot select a safe meaning."
            risk = "RISK_4_DIRECTION_REQUIRED"
            future_change = "Direction must choose whether it is label, boundary, or action language."
            owner = "DIRECTION"
            contract = "possible allowed_actions / forbidden_actions / authority"
            automatable = False
            direction = True
        elif item.initial_type == "CONTRACTUAL_EXACT" or item.contract_aware:
            classification = "CONTRACTUAL_EXACT" if len(item.text) < 48 else "CONTRACTUAL_EXPLANATORY"
            reason = "Contract term or contract-aware surface is evidenced, but no wording change is authorized."
            risk = "RISK_3_CONTRACT_SENSITIVE"
            future_change = "Can be updated only from a contract-approved vocabulary change."
            owner = "CONTRACT_OWNER"
            contract = "contract-aware surface / declared source"
            automatable = False
            direction = True
            exact = classification == "CONTRACTUAL_EXACT"
        elif item.surface == "NAVIGATION":
            classification = "NAVIGATION"
            reason = "Navigation label with no demonstrated state or authority semantics."
            risk = "RISK_1_PRESENTATIONAL"
            owner = "UI_EDITORIAL_OWNER"
        elif any(term in value for term in ("placeholder", "draft local", "seleccion", "ingres")):
            classification = "PLACEHOLDER"
            reason = "Input guidance or empty-input copy; not a proof of action permission."
            risk = "RISK_2_CONTRACT_ADJACENT"
            owner = "UI_EDITORIAL_OWNER"
        elif any(term in value for term in ("nombre", "modelo", "rol", "proveedor", "memoria", "tema", "descripci", "instrucci")):
            classification = "FORM_LABEL"
            reason = "Form or data label; meaning is presentational unless contract evidence says otherwise."
            risk = "RISK_1_PRESENTATIONAL"
            owner = "UI_EDITORIAL_OWNER"
        elif value in {"ready", "passed", "pending", "planned", "invalid", "failed", "blocked", "connected", "disconnected", "online", "offline"}:
            classification = "STATE_LABEL"
            reason = "Short state token requires its source/status context to remain visible."
            risk = "RISK_2_CONTRACT_ADJACENT"
            owner = "CONTRACT_OWNER"
            contract = "status/source"
            automatable = False
            direction = True
        if classification in {"EDITORIAL_SAFE", "NAVIGATION", "FORM_LABEL", "PLACEHOLDER"} and item.semantic_risk == "RISK_1_PRESENTATIONAL":
            risk = "RISK_1_PRESENTATIONAL"
        result.append(SemanticClassification(
            microcopy_id=item.microcopy_id,
            classification=classification,
            duplicate_classification=duplicate,
            reason=reason,
            risk=risk,
            future_change=future_change,
            decision_owner=owner,
            contract_touched=contract,
            automatable=automatable,
            direction_required=direction,
            must_remain_exact=exact,
        ))
    return result


@dataclass(frozen=True)
class ContractSurfaceMap:
    microcopy_id: str
    surface: str
    contract_anchor: str
    binding_type: str
    contract: str
    authority: str
    payload_or_source: str
    owner: str
    state: str
    risk: str
    dependency: str
    future_change: str


def _contract_anchor(surface: str) -> str:
    return {
        "MASTER_SHELL_P0": "P0",
        "P1_CONTRACT_OVERVIEW": "P1 / FSC-CO-01 / Contract Overview",
        "P1_BLOCKED_FORBIDDEN": "P1 / FSC-BF-02 / Blocked & Forbidden",
        "P1_VALIDATION_READINESS": "P1 / FSC-VR-03 / Validation & Readiness",
        "REQUEST_DRAFT_PANEL": "Request Draft Panel / FSC-RCP-04",
        "P2_P3_MATRIX_CLOSURE": "P2 / P3 / Matriz P3 / closure evidence",
        "P2_P3_PANEL": "P2 / P3 detail panel",
        "CONTRACT_AWARE_WIDGETS": "widgets contract-aware",
        "NAVIGATION": "navigation / route reading",
        "DOMAIN_ADMIN": "domain administration",
        "ADMIN_PANELS": "administrative panels",
        "I18N_CONTRACT_SURFACES": "i18n contract vocabulary",
        "I18N_GENERAL_UI": "i18n general UI",
    }.get(surface, "unresolved surface")


def contract_surface_maps(items: list[CorpusItem] | None = None) -> list[ContractSurfaceMap]:
    entries = items if items is not None else corpus_items()
    classifications = {item.microcopy_id: item for item in semantic_classifications(entries)}
    result: list[ContractSurfaceMap] = []
    direct_surfaces = {
        "MASTER_SHELL_P0", "P1_CONTRACT_OVERVIEW", "P1_BLOCKED_FORBIDDEN",
        "P1_VALIDATION_READINESS", "REQUEST_DRAFT_PANEL", "P2_P3_MATRIX_CLOSURE",
        "CONTRACT_AWARE_WIDGETS", "I18N_CONTRACT_SURFACES",
    }
    for item in entries:
        classification = classifications[item.microcopy_id]
        value = item.text.casefold()
        if classification.classification in {"AMBIGUOUS_REQUIRES_DIRECTION", "UNKNOWN_REQUIRES_DIRECTION"}:
            binding = "DIRECTION_REQUIRED_BINDING"
        elif classification.classification in {"EDITORIAL_SAFE", "NAVIGATION", "FORM_LABEL", "PLACEHOLDER"} and item.surface not in direct_surfaces:
            binding = "EDITORIAL_ONLY" if classification.classification == "EDITORIAL_SAFE" else "PRESENTATIONAL_ONLY"
        elif item.surface in direct_surfaces and classification.classification not in {"EDITORIAL_SAFE", "NAVIGATION", "FORM_LABEL", "PLACEHOLDER"}:
            binding = "DIRECT_CONTRACT_BINDING"
        elif item.contract_aware:
            binding = "INDIRECT_CONTRACT_CONTEXT"
        elif item.surface == "UNKNOWN_SURFACE":
            binding = "UNKNOWN_BINDING"
        else:
            binding = "PRESENTATIONAL_ONLY"
        if "allowed_actions" in value:
            contract = "allowed_actions (declared data, not a CTA)"
        elif "forbidden_actions" in value or "forbidden" in value:
            contract = "forbidden_actions (visible boundary, not a control)"
        elif "blocked_capabilities" in value or "blocked" in value:
            contract = "blocked_capabilities / deny-by-default"
        elif "readiness" in value or classification.classification == "READINESS_LABEL":
            contract = "readiness / validation (not permission)"
        elif "no_payload" in value:
            contract = "backend_internal_ui_payload.v1 / no_payload"
        elif "not_available" in value:
            contract = "source/status/fallback / not_available"
        elif any(term in value for term in ("source", "status", "fallback")):
            contract = "source/status/fallback"
        elif binding in {"DIRECT_CONTRACT_BINDING", "INDIRECT_CONTRACT_CONTEXT"}:
            contract = "backend_internal_ui_payload.v1 / declared surface"
        else:
            contract = "none demonstrated"
        authority = "backend contract; UI read-only; deny-by-default" if binding in {"DIRECT_CONTRACT_BINDING", "INDIRECT_CONTRACT_CONTEXT", "DIRECTION_REQUIRED_BINDING"} else "UI presentation only"
        payload = "backend_internal_ui_payload.v1" if binding in {"DIRECT_CONTRACT_BINDING", "INDIRECT_CONTRACT_CONTEXT"} else "source text/i18n only"
        state = "declared state preserved" if classification.classification in {"BLOCKER", "WARNING", "ERROR", "FALLBACK", "NO_PAYLOAD", "NOT_AVAILABLE", "READINESS_LABEL", "STATE_LABEL"} else "no state inferred"
        dependency = "N3 classification + protected product baseline"
        if binding == "DIRECT_CONTRACT_BINDING":
            owner = "contract surface owner"
        elif binding == "DIRECTION_REQUIRED_BINDING":
            owner = "Direction + contract owner"
        elif binding == "INDIRECT_CONTRACT_CONTEXT":
            owner = "surface owner + contract owner"
        else:
            owner = "UI/editorial owner"
        result.append(ContractSurfaceMap(
            microcopy_id=item.microcopy_id,
            surface=item.surface,
            contract_anchor=_contract_anchor(item.surface),
            binding_type=binding,
            contract=contract,
            authority=authority,
            payload_or_source=payload,
            owner=owner,
            state=state,
            risk=classification.risk,
            dependency=dependency,
            future_change=classification.future_change,
        ))
    return result


DECISION_CATEGORIES = (
    "SAFE_TO_KEEP",
    "EDITORIAL_CANDIDATE",
    "CONSISTENCY_CANDIDATE",
    "GEOMETRY_DRIVEN_CANDIDATE",
    "CONTRACT_SENSITIVE_CANDIDATE",
    "ACTION_PERMISSION_SENSITIVE",
    "READINESS_SENSITIVE",
    "AMBIGUOUS_REQUIRES_DIRECTION",
    "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE",
)
DECISION_RECOMMENDATIONS = (
    "KEEP",
    "REVIEW",
    "DIRECTION_REQUIRED",
    "CONTRACT_CHANGE_REQUIRED",
    "NO_CHANGE",
)


@dataclass(frozen=True)
class DecisionPackageRow:
    microcopy_id: str
    text: str
    file: str
    location: str
    classification: str
    decision_category: str
    risk: str
    reason: str
    possible_breakage: str
    contract_touched: str
    duplicate: str
    visual_issue: str
    inconsistency: str
    recommendation: str
    proposal_status: str


def _geometry_issue(item: CorpusItem) -> str:
    if item.text in {"backend_internal_ui_payload.v1", "backend_internal_ui_request.v1"}:
        return "OVERFLOW_RISK at desktop local value box; no global page overflow."
    if item.text.startswith("Si no hay lista de detalle, el bloqueo sigue vigente"):
        return "WRAP_RISK across desktop/tablet/mobile; no clipping observed."
    if item.text == "Contract request draft":
        return "OVERFLOW_RISK for collapsed mobile drawer edge; no global page overflow."
    return "NO_ISSUE"


def decision_package_rows(items: list[CorpusItem] | None = None) -> list[DecisionPackageRow]:
    entries = items if items is not None else corpus_items()
    classifications = {item.microcopy_id: item for item in semantic_classifications(entries)}
    mappings = {item.microcopy_id: item for item in contract_surface_maps(entries)}
    rows: list[DecisionPackageRow] = []
    for item in entries:
        classification = classifications[item.microcopy_id]
        mapping = mappings[item.microcopy_id]
        visual = _geometry_issue(item)
        if classification.classification in {"ACTION_SENSITIVE", "AMBIGUOUS_REQUIRES_DIRECTION"}:
            category = "ACTION_PERMISSION_SENSITIVE" if classification.classification == "ACTION_SENSITIVE" else "AMBIGUOUS_REQUIRES_DIRECTION"
            recommendation = "DIRECTION_REQUIRED"
            reason = "Action/permission meaning cannot be selected from deterministic evidence."
            breakage = "Could imply or remove authority, submit, dispatch, run, execute or permission."
        elif classification.classification in {"READINESS_LABEL", "STATE_LABEL", "NO_PAYLOAD", "NOT_AVAILABLE"}:
            category = "READINESS_SENSITIVE"
            recommendation = "DIRECTION_REQUIRED"
            reason = "State/readiness/fallback wording can alter the boundary between information and permission."
            breakage = "Could turn readiness, absence or status into operational success or availability."
        elif visual != "NO_ISSUE":
            category = "GEOMETRY_DRIVEN_CANDIDATE"
            recommendation = "REVIEW"
            reason = "Browser evidence found a local wrapping or geometry risk without a product fix."
            breakage = "A copy or CSS change could clip evidence, change density or change contract emphasis."
        elif classification.must_remain_exact:
            category = "MUST_NOT_CHANGE_WITHOUT_CONTRACT_CHANGE"
            recommendation = "CONTRACT_CHANGE_REQUIRED"
            reason = "Exact contract vocabulary is preserved by the current boundary."
            breakage = "Could desynchronize source/status/fallback, blockers, forbidden actions or capabilities."
        elif classification.classification in {"CONTRACTUAL_EXACT", "CONTRACTUAL_EXPLANATORY", "BLOCKER", "WARNING", "ERROR", "FALLBACK"}:
            category = "CONTRACT_SENSITIVE_CANDIDATE"
            recommendation = "DIRECTION_REQUIRED"
            reason = "Contract-aware or diagnostic copy needs owner review before any wording change."
            breakage = "Could change state interpretation, severity, source provenance or anti-affordance meaning."
        elif classification.duplicate_classification != "NONE":
            category = "CONSISTENCY_CANDIDATE"
            recommendation = "REVIEW"
            reason = "Repeated text may be equivalent or contextual; the corpus does not choose a merge."
            breakage = "Could erase surface-specific context or create inconsistent labels."
        elif classification.classification in {"EDITORIAL_SAFE", "NAVIGATION", "FORM_LABEL", "PLACEHOLDER"}:
            category = "EDITORIAL_CANDIDATE"
            recommendation = "REVIEW"
            reason = "Editorial/presentational copy is a possible future cleanup subset."
            breakage = "Could affect comprehension, localization or available width without changing contract."
        else:
            category = "SAFE_TO_KEEP"
            recommendation = "KEEP"
            reason = "No deterministic reason to change the current record."
            breakage = "No demonstrated breakage."
        inconsistency = "DUPLICATE_CONTEXTUAL" if classification.duplicate_classification == "DUPLICATE_CONTEXTUAL" else ("DUPLICATE_EQUIVALENT" if classification.duplicate_classification == "DUPLICATE_EQUIVALENT" else "NO_DEMONSTRATED_INCONSISTENCY")
        rows.append(DecisionPackageRow(
            microcopy_id=item.microcopy_id,
            text=item.text,
            file=item.file,
            location=item.location,
            classification=classification.classification,
            decision_category=category,
            risk=classification.risk,
            reason=reason,
            possible_breakage=breakage,
            contract_touched=mapping.contract,
            duplicate=classification.duplicate_classification,
            visual_issue=visual,
            inconsistency=inconsistency,
            recommendation=recommendation,
            proposal_status="NO_PROPOSAL" if recommendation != "REVIEW" else "PROPOSED_NOT_IMPLEMENTED",
        ))
    return rows


def source_hashes() -> dict[str, str]:
    return {
        path: hashlib.sha256((ROOT / path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for path in PROTECTED_PRODUCT_PATHS
    }


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def baseline_file_bytes(relative_path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASELINE}:{relative_path}"], cwd=ROOT)


AUTHORIZED_UI_UX_1_200_CSS_SUFFIX = """
/* UI/UX 1.200 N5: remediate only the measured local geometry risks. */
body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] [data-main-console-zone="readiness"] .readiness-card,
body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] [data-main-console-zone="readiness"] .readiness-card .layout-value {
    min-width: 0;
}

body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] [data-main-console-zone="readiness"] .readiness-card .layout-value {
    overflow-wrap: anywhere;
    word-break: break-word;
}

body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] .state-guidance-card strong,
body .ia-core-shell[data-visual-hierarchy-first-pass="1.180"] .state-guidance-card span {
    min-width: 0;
    overflow-wrap: anywhere;
}

/* Keep the existing read-only disclosure tab fully inside the viewport. */
body #request-draft-panel.request-draft-panel.collapsed {
    width: 44px !important;
    max-width: 44px !important;
    right: 1px !important;
    transform: none !important;
    overflow: hidden;
}

body #request-draft-panel.request-draft-panel.collapsed .request-draft-toggle {
    width: 43px !important;
    min-width: 43px !important;
}
"""


def protected_files_match_baseline() -> list[str]:
    changed = []
    for path in PROTECTED_PRODUCT_PATHS:
        current = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        baseline = baseline_file_bytes(path).replace(b"\r\n", b"\n")
        if current == baseline:
            continue
        if path == "ui/web/styles.css" and current == baseline + AUTHORIZED_UI_UX_1_200_CSS_SUFFIX.encode():
            continue
        changed.append(path)
    return changed


def validate_source_registry(paths: Iterable[str]) -> None:
    allowed = set(MICROCOPY_SOURCE_PATHS)
    for path in paths:
        if any(char in path for char in "*?[]"):
            raise ValueError("wildcard source is not permitted")
        if path not in allowed:
            raise ValueError(f"unregistered source: {path}")


def validate_i18n_key(key: str) -> None:
    keys = {key for key, _ in _flatten_i18n(json.loads(_read_text(I18N_PATH)))}
    if not I18N_KEY_RE.fullmatch(key) or key not in keys:
        raise ValueError(f"unknown i18n key: {key}")


def protected_source_manifest() -> dict[str, object]:
    return {
        "baseline": BASELINE,
        "source_paths": list(MICROCOPY_SOURCE_PATHS),
        "protected_product_paths": list(PROTECTED_PRODUCT_PATHS),
        "source_hashes": source_hashes(),
        "corpus_counts": corpus_counts(),
        "corpus_digest": corpus_digest(),
    }
