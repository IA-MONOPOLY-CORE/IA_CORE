"""Read-only loader for the planned Market Catalog database."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from core.market_catalog.schema import MarketCatalog


def load_market_catalog(path: str | Path) -> MarketCatalog:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return MarketCatalog.from_dict(payload)


def get_market_by_id(catalog: MarketCatalog, market_id: str) -> dict | None:
    for entry in catalog.entries:
        if entry.market_id == market_id:
            return entry.to_dict()
    return None


def find_market_by_normalized_name(catalog: MarketCatalog, normalized_name: str) -> dict | None:
    for entry in catalog.entries:
        if entry.normalized_name == normalized_name:
            return entry.to_dict()
    return None


def list_markets(catalog: MarketCatalog) -> list[dict]:
    return deepcopy([entry.to_dict() for entry in catalog.entries])
