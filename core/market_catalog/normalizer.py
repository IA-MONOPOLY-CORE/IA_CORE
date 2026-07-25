"""Normalization helpers for the planned Market Catalog."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from core.market_catalog.schema import (
    ACTIVATION_STATUS,
    MARKET_CATALOG_SOURCE,
    MARKET_CATALOG_STATUS,
    MARKET_KIND,
    empty_scoring,
)


IGNORED_LINES = {
    "listado de 3859 nichos",
    "todos los nichos (categorias de google business)",
    "todos los nichos (categorías de google business)",
    "todos los nichos categorias de google business",
}


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_market_name(value: str) -> str:
    text = strip_accents(value).lower()
    text = re.sub(r"[^\w\s&/+-]", " ", text, flags=re.UNICODE)
    text = re.sub(r"[_/+-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def slugify_normalized_name(normalized_name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", strip_accents(normalized_name).lower())
    return re.sub(r"_+", "_", slug).strip("_")


def should_ignore_line(value: str) -> bool:
    text = value.strip()
    if not text:
        return True
    normalized = normalize_market_name(text)
    if normalized in IGNORED_LINES:
        return True
    if normalized.isdigit():
        return True
    return False


def build_market_entry(raw_name: str) -> dict[str, Any]:
    display_name = re.sub(r"\s+", " ", raw_name).strip()
    normalized_name = normalize_market_name(display_name)
    return {
        "market_id": f"market_{slugify_normalized_name(normalized_name)}",
        "source": MARKET_CATALOG_SOURCE,
        "raw_name": raw_name.strip(),
        "normalized_name": normalized_name,
        "display_name": display_name,
        "market_kind": MARKET_KIND,
        "status": MARKET_CATALOG_STATUS,
        "activation_status": ACTIVATION_STATUS,
        "mapped_internal_areas": [],
        "mapped_internal_niches": [],
        "mapped_profiles": [],
        "mapped_specializations": [],
        "mapped_presets": [],
        "business_composition_ready": False,
        "scoring": empty_scoring(),
        "notes": [],
    }


def normalize_market_lines(lines: list[str]) -> dict[str, Any]:
    raw_entries: list[str] = []
    discarded_lines: list[dict[str, str]] = []
    for line in lines:
        if should_ignore_line(line):
            discarded_lines.append({"line": line, "reason": "header_empty_or_non_market_line"})
        else:
            raw_entries.append(line.strip())

    entries_by_name: dict[str, dict[str, Any]] = {}
    duplicate_lines: list[dict[str, str]] = []
    for raw_entry in raw_entries:
        entry = build_market_entry(raw_entry)
        normalized_name = entry["normalized_name"]
        if normalized_name in entries_by_name:
            duplicate_lines.append({"line": raw_entry, "duplicate_of": entries_by_name[normalized_name]["display_name"]})
            continue
        entries_by_name[normalized_name] = entry

    entries = sorted(entries_by_name.values(), key=lambda item: strip_accents(item["display_name"]).casefold())
    return {
        "entries": entries,
        "total_raw_entries": len(raw_entries),
        "total_normalized_entries": len(entries),
        "duplicates_removed": len(duplicate_lines),
        "discarded_lines": discarded_lines,
        "duplicate_lines": duplicate_lines,
    }
