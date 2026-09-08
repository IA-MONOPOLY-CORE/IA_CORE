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


def source_hashes() -> dict[str, str]:
    return {
        path: hashlib.sha256((ROOT / path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        for path in PROTECTED_PRODUCT_PATHS
    }


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def baseline_file_bytes(relative_path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{BASELINE}:{relative_path}"], cwd=ROOT)


def protected_files_match_baseline() -> list[str]:
    return [
        path for path in PROTECTED_PRODUCT_PATHS
        if (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        != baseline_file_bytes(path).replace(b"\r\n", b"\n")
    ]


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
