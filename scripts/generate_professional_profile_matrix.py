"""Generate the derived professional profile area/niche matrix."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / "docs" / "PROFESSIONAL_PROFILE_AREA_NICHE_MATRIX.md"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _table(headers: list[str], rows: list[list[object]]) -> str:
    output = [
        "| " + " | ".join(_escape_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(_escape_cell(cell) for cell in row) + " |")
    return "\n".join(output)


def _join_ids(values: list[str], *, empty: str = "-") -> str:
    return ", ".join(values) if values else empty


def _top_counter(counter: Counter[str], *, limit: int = 3) -> str:
    if not counter:
        return "-"
    return ", ".join(f"{key} ({value})" for key, value in counter.most_common(limit))


def build_matrix(root: Path = ROOT) -> dict[str, Any]:
    catalogs_dir = root / "catalogs"
    profiles = _load_json(catalogs_dir / "professional_profiles.json")["profiles"]
    areas = _load_json(catalogs_dir / "areas.json")
    niches = _load_json(catalogs_dir / "niches.json")

    areas_by_id = {area["id"]: area for area in areas}
    niches_by_id = {niche["id"]: niche for niche in niches}
    niches_by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for niche in niches:
        niches_by_area[niche["area_id"]].append(niche)

    profiles_by_area: dict[str, list[dict[str, Any]]] = defaultdict(list)
    profiles_by_niche: dict[str, list[dict[str, Any]]] = defaultdict(list)
    families_by_area: dict[str, Counter[str]] = defaultdict(Counter)
    policies_by_area: dict[str, Counter[str]] = defaultdict(Counter)
    scales_by_area: dict[str, Counter[str]] = defaultdict(Counter)

    for profile in profiles:
        for area_id in profile["areas_compatibles"]:
            profiles_by_area[area_id].append(profile)
            families_by_area[area_id][profile["familia_profesional"]] += 1
            policies_by_area[area_id][profile["default_model_policy"]] += 1
            scales_by_area[area_id].update(profile["compatible_business_scales"])
        for niche_id in profile["nichos_compatibles"]:
            profiles_by_niche[niche_id].append(profile)

    covered_areas = {area_id for area_id in areas_by_id if profiles_by_area.get(area_id)}
    covered_niches = {niche_id for niche_id in niches_by_id if profiles_by_niche.get(niche_id)}
    uncovered_areas = sorted(set(areas_by_id) - covered_areas)
    uncovered_niches = sorted(set(niches_by_id) - covered_niches)
    weak_niches = sorted(
        niche_id for niche_id, items in profiles_by_niche.items() if len(items) == 1
    )

    area_rows = []
    area_coverage_rows = []
    area_dominant_rows = []
    area_profile_counts: list[tuple[str, int]] = []

    for area_id in sorted(areas_by_id):
        area_profiles = sorted(profiles_by_area.get(area_id, []), key=lambda item: item["id"])
        area_niches = niches_by_area.get(area_id, [])
        covered_area_niches = [
            niche for niche in area_niches if profiles_by_niche.get(niche["id"])
        ]
        profile_ids = [profile["id"] for profile in area_profiles]
        area_rows.append(
            [area_id, areas_by_id[area_id]["nombre"], len(profile_ids), _join_ids(profile_ids)]
        )
        area_coverage_rows.append(
            [
                area_id,
                areas_by_id[area_id]["nombre"],
                len(covered_area_niches),
                len(area_niches),
                _join_ids(sorted(niche["id"] for niche in covered_area_niches)),
            ]
        )
        area_dominant_rows.append(
            [
                area_id,
                _top_counter(families_by_area[area_id]),
                _top_counter(policies_by_area[area_id]),
                _top_counter(scales_by_area[area_id]),
            ]
        )
        area_profile_counts.append((area_id, len(profile_ids)))

    niche_rows = []
    for niche_id in sorted(niches_by_id):
        niche = niches_by_id[niche_id]
        profile_ids = sorted(profile["id"] for profile in profiles_by_niche.get(niche_id, []))
        niche_rows.append(
            [niche_id, niche["nombre"], niche["area_id"], len(profile_ids), _join_ids(profile_ids)]
        )

    profile_niche_counts = sorted(
        (profile["id"], len(profile["nichos_compatibles"])) for profile in profiles
    )

    return {
        "profiles": profiles,
        "areas": areas,
        "niches": niches,
        "areas_by_id": areas_by_id,
        "niches_by_id": niches_by_id,
        "profiles_by_area": profiles_by_area,
        "profiles_by_niche": profiles_by_niche,
        "covered_areas": covered_areas,
        "covered_niches": covered_niches,
        "uncovered_areas": uncovered_areas,
        "uncovered_niches": uncovered_niches,
        "weak_niches": weak_niches,
        "area_rows": area_rows,
        "area_coverage_rows": area_coverage_rows,
        "niche_rows": niche_rows,
        "area_dominant_rows": area_dominant_rows,
        "top_areas": sorted(area_profile_counts, key=lambda item: (-item[1], item[0]))[:10],
        "low_areas": sorted(area_profile_counts, key=lambda item: (item[1], item[0]))[:10],
        "top_profiles": sorted(profile_niche_counts, key=lambda item: (-item[1], item[0]))[:10],
        "low_profiles": sorted(profile_niche_counts, key=lambda item: (item[1], item[0]))[:10],
    }


def render_markdown(matrix: dict[str, Any]) -> str:
    profiles = matrix["profiles"]
    areas = matrix["areas"]
    niches = matrix["niches"]
    covered_areas = matrix["covered_areas"]
    covered_niches = matrix["covered_niches"]
    uncovered_areas = matrix["uncovered_areas"]
    uncovered_niches = matrix["uncovered_niches"]
    weak_niches = matrix["weak_niches"]

    lines = [
        "# Matriz Perfil Profesional <-> Area/Nicho",
        "",
        "<!-- GENERATED_BY: scripts/generate_professional_profile_matrix.py -->",
        (
            "<!-- MATRIX_SUMMARY "
            f"profiles={len(profiles)} areas={len(areas)} niches={len(niches)} "
            f"covered_areas={len(covered_areas)} uncovered_areas={len(uncovered_areas)} "
            f"covered_niches={len(covered_niches)} uncovered_niches={len(uncovered_niches)} "
            "-->"
        ),
        "",
        "## Resumen Ejecutivo",
        "",
        "Esta matriz es un artefacto derivado para consulta, auditoria y preparacion de fases futuras.",
        "",
        "- Fuente de verdad: `catalogs/professional_profiles.json`.",
        "- Catalogos de referencia: `catalogs/areas.json` y `catalogs/niches.json`.",
        f"- Total perfiles: {len(profiles)}.",
        f"- Total areas: {len(areas)}.",
        f"- Total nichos: {len(niches)}.",
        f"- Areas cubiertas: {len(covered_areas)}.",
        f"- Areas sin cobertura: {len(uncovered_areas)}.",
        f"- Nichos cubiertos: {len(covered_niches)}.",
        f"- Nichos sin cobertura: {len(uncovered_niches)}.",
        "",
        "La matriz no reemplaza al catalogo global. Si cambia un perfil, se debe regenerar este archivo ejecutando `python scripts/generate_professional_profile_matrix.py`.",
        "",
        "## Regla De Fuente De Verdad",
        "",
        "- La fuente de verdad sigue siendo `catalogs/professional_profiles.json`.",
        "- Este reporte se deriva desde `areas_compatibles` y `nichos_compatibles`.",
        "- No editar esta matriz manualmente como si fuera catalogo.",
        "- Los tests validan que la matriz generada coincide con los catalogos.",
        "",
        "## Area -> Perfiles Compatibles",
        "",
        _table(["area_id", "area", "perfiles", "profile_ids"], matrix["area_rows"]),
        "",
        "## Area -> Nichos Cubiertos",
        "",
        _table(
            ["area_id", "area", "nichos_cubiertos", "nichos_totales", "niche_ids_cubiertos"],
            matrix["area_coverage_rows"],
        ),
        "",
        "## Nicho -> Perfiles Compatibles",
        "",
        _table(["niche_id", "nicho", "area_id", "perfiles", "profile_ids"], matrix["niche_rows"]),
        "",
        "## Top Areas Con Mas Perfiles",
        "",
        _table(["area_id", "perfiles"], [[area_id, count] for area_id, count in matrix["top_areas"]]),
        "",
        "## Top Areas Con Menos Perfiles",
        "",
        _table(["area_id", "perfiles"], [[area_id, count] for area_id, count in matrix["low_areas"]]),
        "",
        "## Nichos Sin Cobertura",
        "",
        _table(
            ["niche_id", "nicho", "area_id"],
            [
                [niche_id, matrix["niches_by_id"][niche_id]["nombre"], matrix["niches_by_id"][niche_id]["area_id"]]
                for niche_id in uncovered_niches
            ],
        ),
        "",
        "## Nichos Con Cobertura Debil",
        "",
        _table(
            ["niche_id", "nicho", "area_id", "perfil"],
            [
                [
                    niche_id,
                    matrix["niches_by_id"][niche_id]["nombre"],
                    matrix["niches_by_id"][niche_id]["area_id"],
                    matrix["profiles_by_niche"][niche_id][0]["id"],
                ]
                for niche_id in weak_niches
            ],
        ),
        "",
        "## Perfiles Con Mas Nichos",
        "",
        _table(["profile_id", "nichos"], [[profile_id, count] for profile_id, count in matrix["top_profiles"]]),
        "",
        "## Perfiles Con Menos Nichos",
        "",
        _table(["profile_id", "nichos"], [[profile_id, count] for profile_id, count in matrix["low_profiles"]]),
        "",
        "## Dominantes Por Area",
        "",
        _table(
            ["area_id", "familias_dominantes", "model_policies_dominantes", "business_scales_dominantes"],
            matrix["area_dominant_rows"],
        ),
        "",
        "## Recomendaciones Para Proximas Fases",
        "",
        "- Usar esta matriz para generar vistas por dominio sin duplicar datos fuente.",
        "- Priorizar Prompt 19.1 si se necesita export JSON/API de la matriz.",
        "- Usar los 34 nichos sin cobertura como backlog de expansion futura, no como bloqueo.",
        "- Usar los nichos con cobertura debil para decidir presets, papers o team templates.",
        "- Mantener Prompt 20 como siguiente fase natural para recomendacion provider/model por perfil.",
        "",
    ]
    return "\n".join(lines)


def write_matrix(root: Path = ROOT, output_path: Path = OUTPUT_PATH) -> str:
    matrix = build_matrix(root)
    markdown = render_markdown(matrix)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return markdown


def main() -> None:
    write_matrix()
    print(f"Generated {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
