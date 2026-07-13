"""Generate safe derived professional team templates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.professional_team_template_generator import (  # noqa: E402
    generate_team_template_for_domain,
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
            "Genera una plantilla de equipo profesional derivada sin crear "
            "agentes ni modificar dominios reales."
        )
    )
    parser.add_argument("--area", required=True, help="area_id existente")
    parser.add_argument(
        "--niche",
        action="append",
        default=[],
        help="niche_id. Puede repetirse o recibir valores separados por coma.",
    )
    parser.add_argument("--business-scale", help="Escala de negocio")
    parser.add_argument("--objective", help="Objetivo principal del equipo")
    parser.add_argument("--complexity-level", help="Complejidad: baja, media, alta")
    parser.add_argument("--max-profiles", type=int, help="Maximo de perfiles del equipo")
    parser.add_argument(
        "--without-optional-roles",
        action="store_true",
        help="Usar solo roles requeridos al seleccionar perfiles.",
    )
    parser.add_argument(
        "--domain-id",
        default="example_generated_domain",
        help="ID logico de salida. No crea ni modifica ese dominio.",
    )
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
    generated = generate_team_template_for_domain(
        area_id=args.area,
        niche_ids=niche_ids,
        business_scale=args.business_scale,
        objective=args.objective,
        complexity_level=args.complexity_level,
        max_profiles=args.max_profiles,
        include_optional_roles=not args.without_optional_roles,
        domain_id=args.domain_id,
    )
    template = generated["team_template"]
    summary = generated["summary"]
    print("Generated derived professional team template")
    print(f"team_template_id: {template['team_template_id']}")
    print(f"area_id: {template['area_id']}")
    print(f"requested_niches: {len(template['requested_niche_ids'])}")
    print(f"profile_count: {summary['profile_count']}")
    print(f"preset_count: {summary['preset_count']}")
    print(f"score: {summary['score']}")
    print(f"warnings: {len(template['warnings'])}")

    if args.output:
        output_path = _safe_output_path(args.output)
        if output_path.exists():
            raise FileExistsError(f"Salida existente; no se sobrescribe: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(generated, ensure_ascii=False, indent=2) + "\n",
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
