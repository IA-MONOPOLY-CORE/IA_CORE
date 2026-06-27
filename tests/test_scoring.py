import config
from domains.loteria.scoring import score_response, u_score_v2_1
from core.supervisor import MEMORY_SCORES_KEY, Supervisor


def test_score_failed_response_is_zero():
    score = score_response(
        agent_name="x",
        role="analyst",
        result=None,
        success=False,
        duration_ms=10,
    )
    assert score.total == 0


def test_score_role_agent_gets_bonus():
    result = {
        "role": "analyst",
        "output": "analysis " * 20,
        "key_points": ["a", "b"],
    }
    score = score_response(
        agent_name="analyst",
        role="analyst",
        result=result,
        success=True,
        duration_ms=50,
    )
    assert 0 < score.total <= 100
    assert score.confidence > 0
    assert score.reasoning_quality > 0


def test_orchestrate_role_agents_with_scores(tmp_path, monkeypatch):
    empty_tools = tmp_path / "tools"
    empty_tools.mkdir()
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", empty_tools)
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", config.ROOT_DIR / "agents" / "modules")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()

    result = supervisor.orchestrate(
        "design api",
        agent_names=["analyst", "critic", "optimizer"],
    )

    assert len(result.steps) == 3
    for step in result.steps:
        assert step.role in ("analyst", "critic", "optimizer")
        assert step.score is not None
        assert 0 <= step.score["total"] <= 100
        assert "confidence" in step.score
        assert "reasoning_quality" in step.score
        assert "execution_quality" in step.score

    assert result.scores_summary is not None
    assert result.scores_summary["best_agent"] in ("analyst", "critic", "optimizer")

    history = supervisor.memory.get("orchestration_history")
    assert history[-1]["scores_summary"] is not None
    scores_log = supervisor.memory.get(MEMORY_SCORES_KEY)
    assert scores_log[-1]["execution_id"] == result.execution_id

    supervisor.stop()


def test_u_score_v2_1_components_clipped_to_range():
    """Verifica que los componentes normalizados se clippean al rango [0, 20] y score_total al rango [0, 100]."""
    # Caso extremo 1: todos los números en zona de peso mínimo (0-4)
    combinacion_min_zona = [0, 1, 2, 3, 4, 5]
    score_min = u_score_v2_1(combinacion_min_zona)
    assert 0 <= score_min.total <= 100, f"score_total fuera de rango: {score_min.total}"
    assert 0 <= score_min.ipn <= 20, f"ipn fuera de rango: {score_min.ipn}"
    assert 0 <= score_min.pp <= 20, f"pp fuera de rango: {score_min.pp}"
    assert 0 <= score_min.pz <= 20, f"pz fuera de rango: {score_min.pz}"
    assert 0 <= score_min.dsi <= 20, f"dsi fuera de rango: {score_min.dsi}"
    assert 0 <= score_min.cd <= 20, f"cd fuera de rango: {score_min.cd}"
    assert 0 <= score_min.sd <= 20, f"sd fuera de rango: {score_min.sd}"

    # Caso extremo 2: todos los números en zona de peso máximo (35-39)
    combinacion_max_zona = [35, 36, 37, 38, 39, 40]
    score_max = u_score_v2_1(combinacion_max_zona)
    assert 0 <= score_max.total <= 100, f"score_total fuera de rango: {score_max.total}"
    assert 0 <= score_max.ipn <= 20, f"ipn fuera de rango: {score_max.ipn}"
    assert 0 <= score_max.pp <= 20, f"pp fuera de rango: {score_max.pp}"
    assert 0 <= score_max.pz <= 20, f"pz fuera de rango: {score_max.pz}"
    assert 0 <= score_max.dsi <= 20, f"dsi fuera de rango: {score_max.dsi}"
    assert 0 <= score_max.cd <= 20, f"cd fuera de rango: {score_max.cd}"
    assert 0 <= score_max.sd <= 20, f"sd fuera de rango: {score_max.sd}"

    # Caso extremo 3: máxima concentración por decena (4 números en misma decena)
    combinacion_concentrada = [10, 11, 12, 13, 20, 30]
    score_conc = u_score_v2_1(combinacion_concentrada)
    assert 0 <= score_conc.total <= 100, f"score_total fuera de rango: {score_conc.total}"
    assert 0 <= score_conc.ipn <= 20, f"ipn fuera de rango: {score_conc.ipn}"
    assert 0 <= score_conc.pp <= 20, f"pp fuera de rango: {score_conc.pp}"
    assert 0 <= score_conc.pz <= 20, f"pz fuera de rango: {score_conc.pz}"
    assert 0 <= score_conc.dsi <= 20, f"dsi fuera de rango: {score_conc.dsi}"
    assert 0 <= score_conc.cd <= 20, f"cd fuera de rango: {score_conc.cd}"
    assert 0 <= score_conc.sd <= 20, f"sd fuera de rango: {score_conc.sd}"

    # Caso extremo 4: combinación con valores que podrían causar pz_raw < 4
    # Esto prueba específicamente el bug de pz que puede dar negativo
    combinacion_pz_bajo = [0, 1, 2, 3, 4, 0]
    score_pz_bajo = u_score_v2_1(combinacion_pz_bajo)
    assert 0 <= score_pz_bajo.total <= 100, f"score_total fuera de rango: {score_pz_bajo.total}"
    assert 0 <= score_pz_bajo.pz <= 20, (
        f"pz fuera de rango (debería estar clippeado): {score_pz_bajo.pz}"
    )


def test_responsescore_hybrid_access_and_tolerance():
    """Verifica que ResponseScore soporte acceso como atributo y como dict, y sea tolerante a claves inexistentes."""
    result = {
        "role": "analyst",
        "output": "analysis " * 20,
        "key_points": ["a", "b"],
    }
    score = score_response(
        agent_name="analyst",
        role="analyst",
        result=result,
        success=True,
        duration_ms=50,
    )
    
    # a) Verificar equivalencia de acceso
    assert score.total == score["total"]
    assert score.confidence == score["confidence"]
    assert score.reasoning_quality == score["reasoning_quality"]
    
    # b) Verificar acceso a clave inexistente devuelve None sin error
    assert score["clave_inventada"] is None
    assert score[123] is None  # Probamos con una clave de tipo incorrecto
    
    # c) Verificar __contains__ funciona bien
    assert "total" in score
    assert "clave_inventada" not in score
    
    # d) Verificar iteración funciona
    fields = list(score)
    assert "total" in fields
    assert "ipn" in fields
    assert "confidence" in fields
