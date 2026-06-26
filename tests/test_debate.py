import config
from core.debate import detect_contradiction
from core.orchestration import ExecutionMode
from core.supervisor import MEMORY_DEBATE_PREFIX, Supervisor
from domains.loteria.config_loteria import DEBATE_AGENTS


def _supervisor(tmp_path, monkeypatch):
    tools_dir = tmp_path / "tools"
    tools_dir.mkdir()
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", tools_dir)
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", config.ROOT_DIR / "agents" / "modules")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")

    supervisor = Supervisor(log_dir=tmp_path / "logs")
    supervisor.start()
    return supervisor


def test_detect_contradiction_keywords():
    assert detect_contradiction("There is a risk of failure")
    assert detect_contradiction("weakness in design")
    assert not detect_contradiction("everything looks fine")


def test_debate_flow_four_rounds(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", False)
    monkeypatch.setattr(config, "SAFE_MODE", False)
    supervisor = _supervisor(tmp_path, monkeypatch)

    result = supervisor.orchestrate(
        "Build secure authentication API",
        mode=ExecutionMode.DEBATE,
    )

    assert result.mode == "debate"
    assert result.debate is not None
    assert len(result.debate.steps) == 4
    assert result.debate.rounds[0].agent_name == "analyst"
    assert result.debate.rounds[-1].agent_name == "analyst"
    assert result.debate.final_response is not None
    assert "synthesis" in result.debate.final_response

    # Parent chain
    assert result.debate.steps[0].parent_step_id is None
    assert result.debate.steps[1].parent_step_id == result.debate.steps[0].step_id

    supervisor.stop()


def test_debate_detects_contradiction_on_critic(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("short", mode=ExecutionMode.DEBATE)

    critic_step = next(s for s in result.debate.steps if s.agent_name == "critic")
    assert critic_step.contradiction is True
    assert len(result.debate.contradictions) >= 1
    assert result.debate.contradiction_score > 0

    supervisor.stop()


def test_debate_persisted_in_memory(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("persist debate", mode=ExecutionMode.DEBATE)

    stored = supervisor.get_debate(result.debate.debate_id)
    assert stored is not None
    assert stored["debate_id"] == result.debate.debate_id
    assert stored["final_response"] is not None

    orch = supervisor.get_orchestration(result.execution_id)
    assert orch["debate"]["debate_id"] == result.debate.debate_id

    assert supervisor.memory.get(f"{MEMORY_DEBATE_PREFIX}{result.debate.debate_id}")
    supervisor.stop()


def test_debate_optimizer_is_refinement(tmp_path, monkeypatch):
    supervisor = _supervisor(tmp_path, monkeypatch)
    result = supervisor.orchestrate("refine this plan", mode=ExecutionMode.DEBATE)

    optimizer = next(s for s in result.debate.steps if s.agent_name == "optimizer")
    assert optimizer.refinement is True
    assert len(result.debate.refinements) >= 1
    assert result.debate.agreement_score >= 0

    supervisor.stop()


def test_debate_early_stop_on_high_agreement(tmp_path, monkeypatch):
    """Verifica que el debate se detiene temprano cuando hay alto consenso."""
    # Configurar umbral bajo para facilitar el test
    monkeypatch.setattr(config, "AGREEMENT_EARLY_STOP_THRESHOLD", 0.5)

    supervisor = _supervisor(tmp_path, monkeypatch)

    # Mockear compute_consensus_scores para simular alto acuerdo
    def mock_compute_consensus(steps, contradictions):
        # Siempre devolver alto acuerdo (95%) para activar parada temprana
        return 95.0, 5.0

    # Importar y patchear
    from core import debate
    original_compute = debate.compute_consensus_scores
    monkeypatch.setattr(debate, "compute_consensus_scores", mock_compute_consensus)

    try:
        result = supervisor.orchestrate(
            "test early stop",
            mode=ExecutionMode.DEBATE,
        )

        # Verificar que el debate se ejecutó
        assert result.mode == "debate"
        assert result.debate is not None

        # Verificar que el debate se detuvo en la ronda 2 (no llegó a 5 rondas)
        # El modo DEBATE usa 6 agentes por defecto del sistema
        # Cada ronda tiene 6 agentes, si se detiene en ronda 2 debería tener ~12 pasos de colisión
        # Más los pasos del pipeline de cierre (estadístico, auditor, etc.)
        # Si fuera a 5 rondas tendría ~30 pasos de colisión + cierre
        total_steps = len(result.debate.steps)

        # Con parada temprana en ronda 2: 2 rondas * 6 agentes = 12 pasos de colisión + ~5-8 de cierre = ~17-20
        # Sin parada temprana: 5 rondas * 6 agentes = 30 pasos de colisión + ~5-8 de cierre = ~35-38
        assert total_steps <= 20, f"Debió detenerse en ronda 2 pero tuvo {total_steps} pasos (esperado <= 20)"

    finally:
        # Restaurar función original
        if original_compute:
            monkeypatch.setattr(debate, "compute_consensus_scores", original_compute)
        supervisor.stop()
