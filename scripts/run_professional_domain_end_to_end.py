"""Run a safe, non-operational professional-domain end-to-end validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.professional_domain_end_to_end import run_professional_domain_end_to_end  # noqa: E402


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _safe_output_path(output: str) -> Path:
    path = Path(output)
    if not path.is_absolute():
        path = ROOT / path
    resolved = path.resolve()
    domains = (ROOT / "domains").resolve()
    if resolved == domains or domains in resolved.parents:
        raise ValueError("Salida rechazada: este script no escribe dentro de domains/")
    return resolved


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Valida la cadena profesional end-to-end sin crear agentes, papers ni dominios operativos.")
    parser.add_argument("--area", required=True, help="area_id existente")
    parser.add_argument("--niche", action="append", default=[], help="niche_id; repetible o separado por comas")
    parser.add_argument("--business-scale")
    parser.add_argument("--objective")
    parser.add_argument("--complexity-level")
    parser.add_argument("--max-profiles", type=int)
    parser.add_argument("--max-presets", type=int)
    parser.add_argument("--domain-id", default="example_professional_domain", help="ID logico no operativo")
    parser.add_argument("--output", help="JSON opcional; se rechazan rutas dentro de domains/")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    niche_ids = [item for raw in args.niche for item in _parse_csv(raw)]
    result = run_professional_domain_end_to_end(
        area_id=args.area,
        niche_ids=niche_ids,
        business_scale=args.business_scale,
        objective=args.objective,
        complexity_level=args.complexity_level,
        max_profiles=args.max_profiles,
        max_presets=args.max_presets,
        domain_id=args.domain_id,
    )
    summary = result["summary"]
    print("Professional domain end-to-end validation completed")
    print(f"domain_id: {result['request']['domain_id']}")
    print(f"area_id: {result['request']['area_id']}")
    print(f"requested_niches: {len(result['request']['niche_ids'])}")
    print(f"profile_count: {summary['profile_count']}")
    print(f"preset_count: {summary['preset_count']}")
    print(f"team_template_id: {summary['team_template_id']}")
    print(f"model_recommendations: {summary['model_recommendation_count']}")
    print(f"paper_seeds_expected: {summary['paper_seed_count']}")
    print(f"gaps: {summary['gap_count']}")
    print(f"warnings: {summary['warning_count']}")
    if args.output:
        output = _safe_output_path(args.output)
        if output.exists():
            raise FileExistsError(f"Salida existente; no se sobrescribe: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        try:
            display = output.relative_to(ROOT)
        except ValueError:
            display = output
        print(f"output: {display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
