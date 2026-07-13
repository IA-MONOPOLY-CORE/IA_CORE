"""Generate safe derived agent presets from a derived profile catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.professional_agent_preset_generator import (  # noqa: E402
    generate_agent_presets_for_profile_catalog,
)
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
            "Genera agent_presets derivados desde un profile_catalog derivado "
            "sin crear agentes ni modificar dominios reales."
        )
    )
    parser.add_argument(
        "--input",
        help="Ruta a un JSON derived_domain_profile_catalog generado por Prompt 21.",
    )
    parser.add_argument("--area", help="area_id para generar profile_catalog en memoria")
    parser.add_argument(
        "--niche",
        action="append",
        default=[],
        help="niche_id. Puede repetirse o recibir valores separados por coma.",
    )
    parser.add_argument(
        "--domain-id",
        default="example_generated_domain",
        help="ID logico para la salida derivada. No crea ni modifica ese dominio.",
    )
    parser.add_argument("--business-scale", help="Escala del negocio para perfil derivado")
    parser.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Capacidad requerida para perfil derivado.",
    )
    parser.add_argument(
        "--model-policy",
        action="append",
        default=[],
        help="Policy preferida para perfil derivado.",
    )
    parser.add_argument("--complexity", help="Complejidad contextual")
    parser.add_argument("--max-profiles", type=int, help="Maximo de perfiles derivados")
    parser.add_argument("--max-presets", type=int, help="Maximo de presets derivados")
    parser.add_argument(
        "--output",
        help="Ruta JSON de salida. Rechaza cualquier ruta dentro de domains/.",
    )
    return parser


def _load_or_generate_profile_catalog(args: argparse.Namespace) -> dict:
    if args.input:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = ROOT / input_path
        return json.loads(input_path.read_text(encoding="utf-8"))

    if not args.area:
        raise ValueError("Debe indicarse --input o --area")

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
    return generate_profile_catalog_for_domain(
        area_id=args.area,
        niche_ids=niche_ids,
        domain_id=args.domain_id,
        business_scale=args.business_scale,
        required_capabilities=capabilities,
        model_policy_preferences=model_policies,
        complexity=args.complexity,
        max_profiles=args.max_profiles,
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    profile_catalog = _load_or_generate_profile_catalog(args)
    presets = generate_agent_presets_for_profile_catalog(
        profile_catalog,
        domain_id=args.domain_id,
        max_presets=args.max_presets,
    )

    summary = presets["summary"]
    print("Generated derived agent presets")
    print(f"domain_id: {presets['domain_id']}")
    print(f"preset_count: {summary['preset_count']}")
    print(f"human_review_required_count: {summary['human_review_required_count']}")
    print(f"privacy_sensitive_count: {summary['privacy_sensitive_count']}")
    print(f"warnings: {len(presets['warnings'])}")

    if args.output:
        output_path = _safe_output_path(args.output)
        if output_path.exists():
            raise FileExistsError(f"Salida existente; no se sobrescribe: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(presets, ensure_ascii=False, indent=2) + "\n",
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
