"""DOCX importer for the planned, non-active Market Catalog."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from core.market_catalog.normalizer import normalize_market_lines
from core.market_catalog.schema import (
    MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED,
    MARKET_CATALOG_RUNTIME_ENABLED,
    MARKET_CATALOG_STATUS,
    MARKET_CATALOG_UI_ENABLED,
)


CATALOG_NAME = "Market Catalog / Catálogo de Mercados"
DOCX_SOURCE = "external_market_catalog_docx"


def extract_docx_paragraphs(path: str | Path) -> list[str]:
    docx_path = Path(path)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(docx_path) as archive:
        document_xml = archive.read("word/document.xml")
    root = ET.fromstring(document_xml)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def build_market_catalog_from_docx(path: str | Path) -> dict[str, Any]:
    source_path = Path(path)
    paragraphs = extract_docx_paragraphs(source_path)
    normalized = normalize_market_lines(paragraphs)
    total_raw_entries = normalized["total_raw_entries"]
    total_normalized_entries = normalized["total_normalized_entries"]
    duplicates_removed = normalized["duplicates_removed"]
    return {
        "catalog_name": CATALOG_NAME,
        "status": MARKET_CATALOG_STATUS,
        "runtime_enabled": MARKET_CATALOG_RUNTIME_ENABLED,
        "ui_enabled": MARKET_CATALOG_UI_ENABLED,
        "business_composition_enabled": MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED,
        "source_file_name": source_path.name,
        "source": DOCX_SOURCE,
        "total_raw_entries": total_raw_entries,
        "total_normalized_entries": total_normalized_entries,
        "duplicates_removed": duplicates_removed,
        "metadata": {
            "source_path_recorded": str(source_path),
            "total_docx_paragraphs": len(paragraphs),
            "discarded_lines_count": len(normalized["discarded_lines"]),
            "discarded_lines": normalized["discarded_lines"],
            "duplicate_lines": normalized["duplicate_lines"],
            "count_note": _count_note(total_raw_entries, total_normalized_entries, duplicates_removed, normalized["discarded_lines"]),
            "activation_status": "not_evaluated",
            "runtime_boundary": "not_active_no_runtime_no_ui_no_business_composition",
        },
        "entries": normalized["entries"],
    }


def write_market_catalog_from_docx(source_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    catalog = build_market_catalog_from_docx(source_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return catalog


def _count_note(raw_count: int, normalized_count: int, duplicates_removed: int, discarded_lines: list[dict[str, str]]) -> str:
    if normalized_count == 3859:
        return "Normalized count matches the source title count of 3859 market categories."
    return (
        "Normalized count differs from 3859 because the importer discarded "
        f"{len(discarded_lines)} non-market lines and removed {duplicates_removed} duplicate normalized names "
        f"from {raw_count} raw market lines."
    )
