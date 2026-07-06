import asyncio
import json
from pathlib import Path

import config
import api
from agents.runtime_json_agent import RuntimeJsonAgent
from core.domain_registry import (
    create_domain,
    get_theme_presets,
    list_domains,
    slugify_domain_name,
)


def test_domain_slug_and_theme_presets_are_portable_and_paired():
    assert slugify_domain_name("Atención al cliente") == "atencion_al_cliente"

    themes = get_theme_presets()
    assert {theme["id"] for theme in themes} == {
        "tactico",
        "corporativo",
        "editorial",
        "calido",
    }
    for theme in themes:
        assert theme["color_primario"].startswith("#")
        assert set(theme["tipografia"]) == {
            "familia",
            "titulo_px",
            "cuerpo_px",
            "peso_titulo",
            "peso_cuerpo",
        }


def test_create_domain_writes_manifest_and_agent_directories(tmp_path):
    domain = create_domain(
        name="Análisis de contratos",
        description="Revisión de cláusulas y riesgos.",
        instructions="Separar hechos, riesgos y recomendaciones.",
        theme_id="editorial",
        suggested_niche="Análisis de contratos",
        domains_dir=tmp_path,
    )

    domain_dir = tmp_path / "analisis_de_contratos"
    persisted = json.loads((domain_dir / "domain.json").read_text(encoding="utf-8"))

    assert domain["id"] == "analisis_de_contratos"
    assert persisted["color_primario"] == "#7C3AED"
    assert persisted["tipografia"]["familia"] == "Georgia, serif"
    assert persisted["instrucciones"] == "Separar hechos, riesgos y recomendaciones."
    assert (domain_dir / "agents" / "config").is_dir()
    assert (domain_dir / "agents" / "papers").is_dir()
    assert [item["id"] for item in list_domains(tmp_path)] == ["analisis_de_contratos"]


def test_domain_api_and_agent_creation_inherit_global_instructions(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

    request = api.DomainCreateRequest(
        nombre="Investigación de mercado",
        descripcion="Estudios de consumidores y competencia.",
        instrucciones="Citar evidencia y declarar incertidumbre.",
        tema_id="corporativo",
        nicho_sugerido="Investigación de mercado",
    )
    created = asyncio.run(api.create_domain_endpoint(request))
    assert created["domain"]["id"] == "investigacion_de_mercado"

    result = asyncio.run(
        api.create_agent_endpoint(
            id="market_researcher_test",
            role="analyst",
            provider="ollama",
            model="phi3:mini",
            system_prompt="Analizá el mercado objetivo.",
            temperature=0.3,
            memory_file=None,
            domain_id="investigacion_de_mercado",
        )
    )
    assert result["success"] is True

    json_path = tmp_path / "investigacion_de_mercado" / "agents" / "config" / "market_researcher_test.json"
    profile = json.loads(json_path.read_text(encoding="utf-8"))
    assert profile["domain_id"] == "investigacion_de_mercado"
    assert profile["domain_instructions"] == "Citar evidencia y declarar incertidumbre."

    runtime = RuntimeJsonAgent(memory=object(), json_path=json_path)
    assert runtime.domain_id == "investigacion_de_mercado"
    assert runtime.system_prompt.startswith("[INSTRUCCIONES GLOBALES DEL DOMINIO]")
    assert "Citar evidencia y declarar incertidumbre." in runtime.system_prompt


def test_lottery_domain_has_retroactive_manifest():
    manifest = json.loads(
        Path("domains/loteria/domain.json").read_text(encoding="utf-8")
    )

    assert manifest["id"] == "loteria"
    assert manifest["tema_id"] == "tactico"
    assert manifest["instrucciones"]


def test_domain_creation_ui_uses_catalog_and_gates_agent_creation():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    script = Path("ui/web/domains.js").read_text(encoding="utf-8")
    catalog = json.loads(Path("ui/web/i18n_es.json").read_text(encoding="utf-8"))

    assert 'id="domain-modal"' in html
    assert 'id="domain-theme-grid"' in html
    assert 'id="agent-domain" required' in html
    assert '<script src="/domains.js"></script>' in html
    assert "requireDomain" in script
    assert "state.domains.length > 0" in script
    assert catalog["domains"]["niche_suggestions"] == [
        "Lotería",
        "Trading",
        "Atención al cliente",
        "Análisis de contratos",
        "Investigación de mercado",
    ]


def test_agent_creation_requires_domain_id():
    route = next(
        route
        for route in api.app.routes
        if getattr(route, "path", None) == "/api/agents/create"
    )
    domain_field = next(
        field for field in route.dependant.body_params if field.name == "domain_id"
    )

    assert domain_field.field_info.is_required() is True


def test_agent_form_memory_is_optional_and_labels_are_spanish():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")

    assert "* OBLIGATORIA" not in html
    assert "Debe seleccionar un archivo de memoria" not in html
    assert "MEMORIA <span style=\"color:var(--text-muted);\">(OPCIONAL)</span>" in html

    assert '<option value="simulator">Simulador</option>' in html
    assert '<option value="critic">Crítico</option>' in html
    assert '<option value="optimizer">Optimizador</option>' in html
    assert '<option value="orchestrator">Orquestador</option>' in html
    assert 'bayesian: "Bayesiano"' in html
    assert "option.value = spec;" in html
