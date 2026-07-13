import pytest
from fastapi.testclient import TestClient

import api
from core import domain_registry
from core.domain_identity import (
    DUPLICATE_DOMAIN_ERROR,
    detect_duplicate_domains,
    domains_are_equivalent,
    normalize_domain_name,
    normalize_domain_slug,
)


def test_domain_name_and_slug_normalization_equates_accents_and_cosmetics():
    assert normalize_domain_name("Lotería / IA_CORE") == "loteria"
    assert normalize_domain_slug("Lotería - Análisis de Juegos de Azar") == (
        "loteria_analisis_juegos_azar"
    )


def test_loteria_names_are_conceptually_equivalent():
    old_domain = {
        "id": "loteria",
        "nombre": "Lotería / IA_CORE",
    }
    ui_domain = {
        "id": "loteria_analisis_de_juegos_de_azar",
        "nombre": "Lotería - Análisis de Juegos de Azar",
        "area_profesional_id": "oficios_otros",
        "nicho_id": "analisis_loteria_juegos_azar",
    }

    assert domains_are_equivalent(old_domain, ui_domain)


def test_duplicate_domain_id_is_rejected(tmp_path):
    domain_registry.create_domain(
        name="Dominio Test",
        description="Descripcion",
        instructions="Instrucciones",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        domain_registry.create_domain(
            name="Dominio Test",
            description="Otra descripcion",
            instructions="Otras instrucciones",
            theme_id="corporativo",
            domains_dir=tmp_path,
        )


def test_equivalent_domain_name_is_rejected(tmp_path):
    domain_registry.create_domain(
        name="Lotería",
        description="Descripcion",
        instructions="Instrucciones",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        domain_registry.create_domain(
            name="Loteria / IA_CORE",
            description="Otra descripcion",
            instructions="Otras instrucciones",
            theme_id="corporativo",
            domains_dir=tmp_path,
        )


def test_same_area_and_niche_is_rejected(tmp_path):
    domain_registry.create_domain(
        name="Gestion de Reclamos A",
        description="Descripcion",
        instructions="Instrucciones",
        theme_id="corporativo",
        area_profesional_id="comercial_ventas_negocios",
        nicho_id="prospeccion_b2b",
        domains_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="dominios duplicados"):
        domain_registry.create_domain(
            name="Gestion de Reclamos B",
            description="Otra descripcion",
            instructions="Otras instrucciones",
            theme_id="corporativo",
            area_profesional_id="comercial_ventas_negocios",
            nicho_id="prospeccion_b2b",
            domains_dir=tmp_path,
        )


def test_detector_lists_duplicate_conflicts():
    conflicts = detect_duplicate_domains(
        [
            {"id": "loteria", "nombre": "Lotería / IA_CORE"},
            {
                "id": "loteria_analisis_de_juegos_de_azar",
                "nombre": "Lotería - Análisis de Juegos de Azar",
            },
            {"id": "demo_generico", "nombre": "Demo generico"},
        ]
    )

    assert conflicts == [
        {
            "domain_a": "loteria",
            "domain_b": "loteria_analisis_de_juegos_de_azar",
            "nombre_a": "Lotería / IA_CORE",
            "nombre_b": "Lotería - Análisis de Juegos de Azar",
            "shared_keys": ["concept:loteria_juegos_azar"],
        }
    ]


def test_create_domain_endpoint_rejects_loteria_duplicate():
    response = TestClient(api.app).post(
        "/api/domains/create",
        json={
            "nombre": "Lotería - Análisis de Juegos de Azar",
            "descripcion": "Dominio duplicado",
            "instrucciones": "No deberia crearse.",
            "tema_id": "calido",
            "nicho_sugerido": "Análisis de Lotería y Juegos de Azar",
            "area_profesional_id": "oficios_otros",
            "nicho_id": "analisis_loteria_juegos_azar",
        },
    )

    assert response.status_code == 400
    assert DUPLICATE_DOMAIN_ERROR in response.json()["detail"]


def test_current_active_repo_domains_have_no_duplicates():
    active_domains = domain_registry.list_domains()

    assert detect_duplicate_domains(active_domains) == []
