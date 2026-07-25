"""Schema for the planned, non-active Market Catalog database."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


MARKET_CATALOG_STATUS = "planned_not_active"
MARKET_CATALOG_RUNTIME_ENABLED = False
MARKET_CATALOG_UI_ENABLED = False
MARKET_CATALOG_BUSINESS_COMPOSITION_ENABLED = False
MARKET_CATALOG_SOURCE = "external_market_catalog_docx"
MARKET_KIND = "external_business_category"
ACTIVATION_STATUS = "not_evaluated"

SCORING_FIELDS = (
    "purchasing_power",
    "pain_intensity",
    "market_size",
    "online_reachability",
    "competition_signal",
    "stability_or_growth",
    "delivery_ease",
    "strategic_fit",
)

EMPTY_MAPPING_FIELDS = (
    "mapped_internal_areas",
    "mapped_internal_niches",
    "mapped_profiles",
    "mapped_specializations",
    "mapped_presets",
)


@dataclass(frozen=True)
class MarketCatalogEntry:
    market_id: str
    source: str
    raw_name: str
    normalized_name: str
    display_name: str
    market_kind: str
    status: str
    activation_status: str
    mapped_internal_areas: tuple[str, ...]
    mapped_internal_niches: tuple[str, ...]
    mapped_profiles: tuple[str, ...]
    mapped_specializations: tuple[str, ...]
    mapped_presets: tuple[str, ...]
    business_composition_ready: bool
    scoring: Mapping[str, Any]
    notes: tuple[str, ...]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MarketCatalogEntry":
        return cls(
            market_id=str(payload["market_id"]),
            source=str(payload["source"]),
            raw_name=str(payload["raw_name"]),
            normalized_name=str(payload["normalized_name"]),
            display_name=str(payload["display_name"]),
            market_kind=str(payload["market_kind"]),
            status=str(payload["status"]),
            activation_status=str(payload["activation_status"]),
            mapped_internal_areas=tuple(payload.get("mapped_internal_areas") or ()),
            mapped_internal_niches=tuple(payload.get("mapped_internal_niches") or ()),
            mapped_profiles=tuple(payload.get("mapped_profiles") or ()),
            mapped_specializations=tuple(payload.get("mapped_specializations") or ()),
            mapped_presets=tuple(payload.get("mapped_presets") or ()),
            business_composition_ready=payload.get("business_composition_ready") is True,
            scoring=MappingProxyType(dict(payload.get("scoring") or {})),
            notes=tuple(payload.get("notes") or ()),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "market_id": self.market_id,
            "source": self.source,
            "raw_name": self.raw_name,
            "normalized_name": self.normalized_name,
            "display_name": self.display_name,
            "market_kind": self.market_kind,
            "status": self.status,
            "activation_status": self.activation_status,
            "mapped_internal_areas": list(self.mapped_internal_areas),
            "mapped_internal_niches": list(self.mapped_internal_niches),
            "mapped_profiles": list(self.mapped_profiles),
            "mapped_specializations": list(self.mapped_specializations),
            "mapped_presets": list(self.mapped_presets),
            "business_composition_ready": self.business_composition_ready,
            "scoring": dict(self.scoring),
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class MarketCatalog:
    catalog_name: str
    status: str
    runtime_enabled: bool
    ui_enabled: bool
    business_composition_enabled: bool
    source_file_name: str
    total_raw_entries: int
    total_normalized_entries: int
    duplicates_removed: int
    metadata: Mapping[str, Any]
    entries: tuple[MarketCatalogEntry, ...]

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MarketCatalog":
        return cls(
            catalog_name=str(payload["catalog_name"]),
            status=str(payload["status"]),
            runtime_enabled=payload.get("runtime_enabled") is True,
            ui_enabled=payload.get("ui_enabled") is True,
            business_composition_enabled=payload.get("business_composition_enabled") is True,
            source_file_name=str(payload["source_file_name"]),
            total_raw_entries=int(payload["total_raw_entries"]),
            total_normalized_entries=int(payload["total_normalized_entries"]),
            duplicates_removed=int(payload["duplicates_removed"]),
            metadata=MappingProxyType(deepcopy(dict(payload.get("metadata") or {}))),
            entries=tuple(MarketCatalogEntry.from_dict(entry) for entry in payload.get("entries") or ()),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "catalog_name": self.catalog_name,
            "status": self.status,
            "runtime_enabled": self.runtime_enabled,
            "ui_enabled": self.ui_enabled,
            "business_composition_enabled": self.business_composition_enabled,
            "source_file_name": self.source_file_name,
            "total_raw_entries": self.total_raw_entries,
            "total_normalized_entries": self.total_normalized_entries,
            "duplicates_removed": self.duplicates_removed,
            "metadata": deepcopy(dict(self.metadata)),
            "entries": [entry.to_dict() for entry in self.entries],
        }


def empty_scoring() -> dict[str, None]:
    return {field: None for field in SCORING_FIELDS}


def validate_market_catalog_entry(entry: Mapping[str, Any]) -> bool:
    if not entry.get("market_id") or not entry.get("raw_name") or not entry.get("normalized_name"):
        return False
    if entry.get("source") != MARKET_CATALOG_SOURCE:
        return False
    if entry.get("market_kind") != MARKET_KIND:
        return False
    if entry.get("status") != MARKET_CATALOG_STATUS:
        return False
    if entry.get("activation_status") != ACTIVATION_STATUS:
        return False
    if entry.get("business_composition_ready") is not False:
        return False
    if set(entry.get("scoring") or {}) != set(SCORING_FIELDS):
        return False
    return all(entry.get(field) == [] for field in EMPTY_MAPPING_FIELDS)
