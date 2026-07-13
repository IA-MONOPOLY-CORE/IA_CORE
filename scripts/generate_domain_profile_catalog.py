"""Generate a safe derived profile catalog for a prospective domain."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.professional_profile_catalog_generator import (  # noqa: E402
    generate_profile_catalog_for_domain,
)


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _safe_output_path(output: str) -> Path:
    path = Path(output)
    if not path.is_absolute():
        path = ROOT / path
    resolved = path.resolve()
    domains_dir = (ROOT / "domains").resolve()
    if resolved == domains_dir or domains_dir in resolved.parents:
        raise ValueError("Salida rechazada: este script no escribe dentro de domains/")
    return resolved


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Genera un profile_catalog derivado desde la Biblioteca Profesional Global "
            "sin modificar dominios reales."
        )
    )
    parser.add_argument("--area", required=True, help="area_id existente en catalogs/areas.json")
    parser.add_argument(
        "--niche",
        action="append",
        default=[],
        help="niche_id existente. Puede repetirse o recibir valores separados por coma.",
    )
    parser.add_argument(
        "--domain-id",
        default="example_generated_domain",
        help="ID logico para la salida derivada. No crea ni modifica ese dominio.",
    )
    parser.add_argument("--business-scale", help="Escala del negocio a priorizar")
    parser.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Capacidad requerida. Puede repetirse o recibir valores separados por coma.",
    )
    parser.add_argument(
        "--model-policy",
        action="append",
        default=[],
        help="Policy preferida. Puede repetirse o recibir valores separados por coma.",
    )
    parser.add_argument("--complexity", help="Complejidad contextual: simple, media, alta")
    parser.add_argument("--max-profiles", type=int, help="Cantidad maxima de perfiles")
    parser.add_argument(
        "--output",
        help="Ruta JSON de salida. Rechaza cualquier ruta dentro de domains/.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    niche_ids = [
        niche_id
        for raw_value in args.niche
        for niche_id in _parse_csv(raw_value)
    ]
    capabilities = [
        capability
        for raw_value in args.capability
        for capability in _parse_csv(raw_value)
    ]
    model_policies = [
        policy
        for raw_value in args.model_policy
        for policy in _parse_csv(raw_value)
    ]

    catalog = generate_profile_catalog_for_domain(
        area_id=args.area,
        niche_ids=niche_ids,
        domain_id=args.domain_id,
        business_scale=args.business_scale,
        required_capabilities=capabilities,
        model_policy_preferences=model_policies,
        complexity=args.complexity,
        max_profiles=args.max_profiles,
    )

    summary = catalog["coverage_summary"]
    print("Generated derived profile catalog")
    print(f"area_id: {summary['requested_area']}")
    print(f"requested_niches: {len(summary['requested_niches'])}")
    print(f"covered_requested_niches: {len(summary['covered_requested_niches'])}")
    print(f"candidate_count: {summary['candidate_count']}")
    print(f"warnings: {len(catalog['warnings'])}")

    if args.output:
        output_path = _safe_output_path(args.output)
        if output_path.exists():
            raise FileExistsError(f"Salida existente; no se sobrescribe: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        try:
            display_path = output_path.relative_to(ROOT)
        except ValueError:
            display_path = output_path
        print(f"output: {display_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
