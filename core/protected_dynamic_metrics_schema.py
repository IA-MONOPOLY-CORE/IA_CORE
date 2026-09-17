"""Bounded, domain-neutral schema for protected dynamic metric summaries."""

from __future__ import annotations

import json
import math
from numbers import Real
from typing import Any, Mapping


PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION = "protected_dynamic_metrics.v1"
PROTECTED_DYNAMIC_METRICS_AUDIENCE = "ia-core-private-beta"
PROTECTED_DYNAMIC_METRICS_EXTERNAL_POLICY = "DEFAULT_DENIED"
PROTECTED_DYNAMIC_METRICS_AGGREGATION = "bounded_internal_snapshot"
MAX_OBSERVATION_COUNT = 1_000_000
MAX_RELATIVE_INDEX = 1_000.0
MAX_PAYLOAD_BYTES = 4_096

COMMON_KEYS = frozenset(
    {
        "contract_version",
        "view",
        "scope",
        "status",
        "audience",
        "external_access",
        "bounded",
        "aggregation",
        "data",
    }
)
SUMMARY_DATA_KEYS = frozenset(
    {
        "observation_count",
        "observed_rate",
        "relative_index",
        "snapshot_status",
        "projection",
    }
)
ALLOWED_STATUS = frozenset({"available", "degraded", "not_available"})


class ProtectedDynamicMetricsContractError(ValueError):
    """Raised when a response is outside the protected metrics contract."""


def _finite_real(value: Any, *, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ProtectedDynamicMetricsContractError("metric value is not numeric")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < minimum or numeric > maximum:
        raise ProtectedDynamicMetricsContractError("metric value is outside bounds")
    return numeric


def _bounded_count(value: Any) -> int:
    if type(value) is not int or value < 0 or value > MAX_OBSERVATION_COUNT:
        raise ProtectedDynamicMetricsContractError("observation count is invalid")
    return value


def _rounded(value: Any, *, minimum: float, maximum: float) -> float:
    return round(_finite_real(value, minimum=minimum, maximum=maximum), 3)


def build_dynamic_metrics_payload(
    observation_count: Any,
    observed_rate: Any,
    relative_index: Any,
    *,
    status: str = "available",
    snapshot_status: str | None = None,
) -> dict[str, Any]:
    selected_snapshot_status = snapshot_status or status
    payload = {
        "contract_version": PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION,
        "view": "summary",
        "scope": "platform",
        "status": status,
        "audience": PROTECTED_DYNAMIC_METRICS_AUDIENCE,
        "external_access": {
            "policy": PROTECTED_DYNAMIC_METRICS_EXTERNAL_POLICY,
            "enabled": False,
        },
        "bounded": True,
        "aggregation": PROTECTED_DYNAMIC_METRICS_AGGREGATION,
        "data": {
            "observation_count": _bounded_count(observation_count),
            "observed_rate": _rounded(observed_rate, minimum=0.0, maximum=100.0),
            "relative_index": _rounded(
                relative_index,
                minimum=0.0,
                maximum=MAX_RELATIVE_INDEX,
            ),
            "snapshot_status": selected_snapshot_status,
            "projection": "allowlist_first_domain_neutral",
        },
    }
    return validate_protected_dynamic_metrics_payload(payload)


def project_dynamic_metrics(source: Mapping[str, Any]) -> dict[str, Any]:
    """Map only known legacy observations into the neutral protected summary."""
    if not isinstance(source, Mapping):
        raise ProtectedDynamicMetricsContractError("metric snapshot is not a mapping")

    required = ("sorteos_completados", "aciertos_4")
    missing = any(key not in source for key in required)
    observation_count = source.get("sorteos_completados", 0)
    hit_count = source.get("aciertos_4", 0)
    if type(observation_count) is not int or type(hit_count) is not int:
        raise ProtectedDynamicMetricsContractError("metric snapshot values are invalid")
    if observation_count < 0 or hit_count < 0 or hit_count > observation_count:
        raise ProtectedDynamicMetricsContractError("metric snapshot values are invalid")

    observed_rate = (hit_count / observation_count * 100.0) if observation_count else 0.0
    relative_index = (observed_rate / 22.1) if observation_count else 0.0
    status = "degraded" if missing else "available"
    return build_dynamic_metrics_payload(
        observation_count,
        observed_rate,
        relative_index,
        status=status,
        snapshot_status=status,
    )


def validate_protected_dynamic_metrics_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or set(payload) != set(COMMON_KEYS):
        raise ProtectedDynamicMetricsContractError("payload fields are not allowlisted")
    if payload["contract_version"] != PROTECTED_DYNAMIC_METRICS_CONTRACT_VERSION:
        raise ProtectedDynamicMetricsContractError("unsupported contract version")
    if payload["view"] != "summary" or payload["scope"] != "platform":
        raise ProtectedDynamicMetricsContractError("invalid view or scope")
    if payload["status"] not in ALLOWED_STATUS:
        raise ProtectedDynamicMetricsContractError("invalid status")
    if payload["audience"] != PROTECTED_DYNAMIC_METRICS_AUDIENCE:
        raise ProtectedDynamicMetricsContractError("invalid audience")
    if payload["external_access"] != {
        "policy": PROTECTED_DYNAMIC_METRICS_EXTERNAL_POLICY,
        "enabled": False,
    }:
        raise ProtectedDynamicMetricsContractError("external access must remain denied")
    if payload["bounded"] is not True:
        raise ProtectedDynamicMetricsContractError("payload must be bounded")
    if payload["aggregation"] != PROTECTED_DYNAMIC_METRICS_AGGREGATION:
        raise ProtectedDynamicMetricsContractError("invalid aggregation")
    data = payload["data"]
    if not isinstance(data, Mapping) or set(data) != set(SUMMARY_DATA_KEYS):
        raise ProtectedDynamicMetricsContractError("data fields are not allowlisted")
    _bounded_count(data["observation_count"])
    _rounded(data["observed_rate"], minimum=0.0, maximum=100.0)
    _rounded(data["relative_index"], minimum=0.0, maximum=MAX_RELATIVE_INDEX)
    if data["snapshot_status"] not in ALLOWED_STATUS:
        raise ProtectedDynamicMetricsContractError("invalid snapshot status")
    if data["projection"] != "allowlist_first_domain_neutral":
        raise ProtectedDynamicMetricsContractError("invalid projection")
    try:
        serialized = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ProtectedDynamicMetricsContractError("payload is not serializable") from exc
    if len(serialized.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise ProtectedDynamicMetricsContractError("payload exceeds bounded size")
    return dict(payload)
