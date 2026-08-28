import asyncio
import json
from pathlib import Path

import config
import api
import mejorar_papers
from fastapi.testclient import TestClient
from agents.runtime_json_agent import RuntimeJsonAgent
from core.domain_registry import (
    create_domain,
    get_domain_agents_papers_dir,
    get_theme_presets,
    list_domains,
    resolve_agent_json,
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
    assert (domain_dir / "agents" / "memory_sources").is_dir()
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
    paper_path = tmp_path / "investigacion_de_mercado" / "agents" / "papers" / "market_researcher_test_paper.json"
    profile = json.loads(json_path.read_text(encoding="utf-8"))
    paper = json.loads(paper_path.read_text(encoding="utf-8"))
    assert profile["domain_id"] == "investigacion_de_mercado"
    assert profile["domain_instructions"] == "Citar evidencia y declarar incertidumbre."
    assert paper["dominio_id"] == "investigacion_de_mercado"
    assert not (tmp_path / "loteria" / "agents" / "config" / "market_researcher_test.json").exists()
    assert not (tmp_path / "loteria" / "agents" / "papers" / "market_researcher_test_paper.json").exists()

    runtime = RuntimeJsonAgent(memory=object(), json_path=json_path)
    assert runtime.domain_id == "investigacion_de_mercado"
    assert runtime.system_prompt.startswith("[INSTRUCCIONES GLOBALES DEL DOMINIO]")
    assert "Citar evidencia y declarar incertidumbre." in runtime.system_prompt


def test_domain_creation_with_area_and_niche_metadata_persists_manifest(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

    response = TestClient(api.app).post(
        "/api/domains/create",
        json={
            "nombre": "Atención al Cliente — Reclamos Codex",
            "descripcion": "Dominio de prueba para reclamos.",
            "instrucciones": "Priorizar claridad, empatía y trazabilidad.",
            "tema_id": "corporativo",
            "area_profesional_id": "atencion_cliente_call_center_telemarketing",
            "nicho_id": "reclamos_postventa",
            "nicho_sugerido": "Reclamos y postventa",
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    domain_id = response.json()["domain"]["id"]
    manifest = json.loads((tmp_path / domain_id / "domain.json").read_text(encoding="utf-8"))
    assert manifest["area_profesional_id"] == "atencion_cliente_call_center_telemarketing"
    assert manifest["nicho_id"] == "reclamos_postventa"
    assert manifest["nicho_sugerido"] == "Reclamos y postventa"

    listed = TestClient(api.app).get("/api/domains/list").json()["domains"]
    listed_domain = next(domain for domain in listed if domain["id"] == domain_id)
    assert listed_domain["area_profesional_id"] == "atencion_cliente_call_center_telemarketing"
    assert listed_domain["nicho_id"] == "reclamos_postventa"


def test_domain_creation_rejects_invalid_area_or_niche(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
    client = TestClient(api.app)
    base_payload = {
        "nombre": "Dominio inválido",
        "descripcion": "Dominio de prueba.",
        "instrucciones": "Instrucciones de prueba.",
        "tema_id": "corporativo",
    }

    invalid_area = client.post(
        "/api/domains/create",
        json={
            **base_payload,
            "nombre": "Área inválida",
            "area_profesional_id": "area_inexistente",
        },
    )
    assert invalid_area.status_code == 400
    assert "Área profesional inexistente" in invalid_area.json()["detail"]

    invalid_niche = client.post(
        "/api/domains/create",
        json={
            **base_payload,
            "nombre": "Nicho inválido",
            "nicho_id": "nicho_inexistente",
        },
    )
    assert invalid_niche.status_code == 400
    assert "Nicho inexistente" in invalid_niche.json()["detail"]

    mismatched = client.post(
        "/api/domains/create",
        json={
            **base_payload,
            "nombre": "Nicho fuera de área",
            "area_profesional_id": "oficios_otros",
            "nicho_id": "reclamos_postventa",
        },
    )
    assert mismatched.status_code == 400
    assert "no pertenece" in mismatched.json()["detail"]


def test_domain_creation_without_catalog_metadata_remains_compatible(tmp_path):
    domain = create_domain(
        name="Dominio manual legacy",
        description="Creado sin catálogo estructurado.",
        instructions="Mantener compatibilidad.",
        theme_id="editorial",
        suggested_niche="Manual",
        domains_dir=tmp_path,
    )
    manifest = json.loads((tmp_path / domain["id"] / "domain.json").read_text(encoding="utf-8"))

    assert manifest["nicho_sugerido"] == "Manual"
    assert "area_profesional_id" not in manifest
    assert "nicho_id" not in manifest


def test_agent_creation_in_lottery_domain_writes_lottery_config_and_paper(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

    create_domain(
        name="Lotería",
        description="Dominio de test para sorteos.",
        instructions="Aplicar reglas de validación ciega.",
        theme_id="tactico",
        domains_dir=tmp_path,
    )

    result = asyncio.run(
        api.create_agent_endpoint(
            id="lottery_test_agent",
            role="analyst",
            provider="ollama",
            model="phi3:mini",
            system_prompt="Analizá combinaciones.",
            temperature=0.2,
            memory_file=None,
            domain_id="loteria",
        )
    )

    assert result["success"] is True
    config_path = tmp_path / "loteria" / "agents" / "config" / "lottery_test_agent.json"
    paper_path = tmp_path / "loteria" / "agents" / "papers" / "lottery_test_agent_paper.json"
    assert config_path.exists()
    assert paper_path.exists()
    assert json.loads(config_path.read_text(encoding="utf-8"))["domain_id"] == "loteria"
    assert json.loads(paper_path.read_text(encoding="utf-8"))["dominio_id"] == "loteria"


def test_mejorar_paper_resolves_non_lottery_domain(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)
    monkeypatch.setattr(
        mejorar_papers,
        "cargar_memoria",
        lambda _agent_id: {
            "patrones_aprendidos": [{"patron": "Separar evidencia observable de hipótesis de mercado."}],
            "errores_cometidos": [],
            "aciertos_historicos": [],
        },
    )

    create_domain(
        name="Trading",
        description="Dominio de señales financieras.",
        instructions="Evaluar riesgo antes de sugerir acciones.",
        theme_id="corporativo",
        domains_dir=tmp_path,
    )
    config_dir = tmp_path / "trading" / "agents" / "config"
    paper_dir = get_domain_agents_papers_dir("trading", domains_dir=tmp_path, ensure=True)
    agent_config = config_dir / "risk_agent.json"
    agent_config.write_text(
        json.dumps(
            {
                "id": "risk_agent",
                "role": "critic",
                "provider": "mock",
                "model": "mock",
                "system_prompt": "Criticar riesgo.",
                "domain_id": "trading",
            }
        ),
        encoding="utf-8",
    )
    paper_path = paper_dir / "risk_agent_paper.json"
    paper_path.write_text(
        json.dumps({"agente_id": "risk_agent", "reglas_clave": []}),
        encoding="utf-8",
    )

    mejorar_papers.mejorar_paper("risk_agent", usar_llm=False, domain_id="trading")

    updated = json.loads(paper_path.read_text(encoding="utf-8"))
    assert "Separar evidencia observable de hipótesis de mercado." in updated["reglas_clave"]
    assert not (tmp_path / "loteria" / "agents" / "papers" / "risk_agent_paper.json").exists()


def test_resolve_agent_json_reports_ambiguity_and_can_pin_domain(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DOMAINS_DIR", tmp_path)

    for name in ["Trading", "Atención al cliente"]:
        create_domain(
            name=name,
            description="Dominio de prueba.",
            instructions="Instrucciones.",
            theme_id="corporativo",
            domains_dir=tmp_path,
        )

    for domain_id in ["trading", "atencion_al_cliente"]:
        config_dir = tmp_path / domain_id / "agents" / "config"
        (config_dir / "duplicado.json").write_text(
            json.dumps({"id": "duplicado", "domain_id": domain_id}),
            encoding="utf-8",
        )

    try:
        resolve_agent_json("duplicado", domains_dir=tmp_path)
    except ValueError as exc:
        assert "múltiples dominios" in str(exc)
    else:
        raise AssertionError("Se esperaba ambigüedad para IDs duplicados")

    domain_id, path = resolve_agent_json("duplicado", "trading", domains_dir=tmp_path)
    assert domain_id == "trading"
    assert path == tmp_path / "trading" / "agents" / "config" / "duplicado.json"


def test_lottery_domain_has_retroactive_manifest():
    manifest = json.loads(
        Path("domains/loteria/domain.json").read_text(encoding="utf-8")
    )

    assert manifest["id"] == "loteria"
    assert manifest["tema_id"] == "tactico"
    assert manifest["instrucciones"]
    assert manifest["primary_action_widget"] == {
        "id": "proxima_validacion",
        "title": "Próxima validación",
        "endpoint": "/api/validation/next",
        "domain_specific": True,
    }


def test_demo_generico_domain_is_internal_and_hidden_from_default_list():
    manifest = json.loads(Path("domains/demo_generico/domain.json").read_text(encoding="utf-8"))

    assert manifest["id"] == "demo_generico"
    assert manifest["es_demo"] is True
    assert manifest["visible_en_hud"] is False
    assert "demo_generico" not in {domain["id"] for domain in list_domains()}
    assert "demo_generico" in {domain["id"] for domain in list_domains(include_internal=True)}


def test_domain_creation_ui_uses_catalog_and_gates_agent_creation():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    script = Path("ui/web/domains.js").read_text(encoding="utf-8")
    catalog = json.loads(Path("ui/web/i18n_es.json").read_text(encoding="utf-8"))

    assert 'id="domain-modal"' in html
    assert 'id="domain-area" name="area_profesional_id" required' in html
    assert 'id="domain-niche" name="nicho_id" required disabled' in html
    assert 'id="domain-theme-grid"' in html
    assert 'id="agent-domain" required' in html
    assert 'src="/domains.js?v=prompt2"' in html
    assert "/api/catalogs/domain-creation" in script
    assert "ensureDomainCreationCatalog" in script
    assert "applyNicheSuggestion" in script
    assert "domainFieldTouched" in script
    assert "domain-suggestions" not in html
    assert "domain-suggestion" not in html
    assert "niche_suggestions" not in script
    assert "requireDomain" in script
    assert "getActiveDomain" in script
    assert "ia-core-active-domain-changed" in script
    assert "state.domains.length > 0" in script
    assert "niche_suggestions" not in catalog["domains"]


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


def test_widgets_are_functional_and_not_decorative():
    html = Path("ui/web/index.html").read_text(encoding="utf-8")
    script = Path("ui/web/domains.js").read_text(encoding="utf-8")
    catalog = json.loads(Path("ui/web/i18n_es.json").read_text(encoding="utf-8"))

    assert "WIDGETS FUNCIONALES" in html
    assert "Estado backend estable" in html
    assert "Acciones declaradas" in html
    assert "Warnings y errores" in html
    assert "Capabilities bloqueadas" in html
    assert "window.domainUI?.initialize" in html
    assert "window.domainUI.requireDomain" in html
    assert "window.domainUI" in script
    assert "getActiveDomain" in script
    assert "backend_internal_ui_payload.v1" in html
    assert "allowed_actions" in html
    assert "forbidden_actions" in html
    assert "blocked_capabilities" in html
    assert "/api/status" in html
    assert "if (provider.is_placeholder)" in html
    assert catalog["appearance"]["status_widget"] == "Estado backend estable"
    assert catalog["appearance"]["actions_widget"] == "Acciones declaradas"
    assert catalog["appearance"]["blocked_capabilities_widget"] == "Capabilities bloqueadas"

    decorative_artifacts = [
        "WIDGETS_LIBRARY",
        "renderWidgetsLibrary",
        "iniciarDragAndDropWidgets",
        "initRadar",
        "radar-container",
        "animated-widget-box",
        "widget-pulse-ring",
        "widget-compass-rotate",
        "widget-scan-line",
        "widget-glow-pulse",
        "widget-target-rings",
        "radar_widget",
        "show_radar",
    ]
    for artifact in decorative_artifacts:
        assert artifact not in html
        assert artifact not in json.dumps(catalog, ensure_ascii=False)
