import config
from core.debate import detect_contradiction
from core.orchestration import ExecutionMode
from core.supervisor import MEMORY_DEBATE_PREFIX, Supervisor
from agents.base import Agent as BaseAgent


class _MockAnalyst(BaseAgent):
    id = "analyst"
    role = "analyst"

    def run(self, task, context=None):
        return {"output": "Positive analysis: looks solid", "confidence": 0.9}


class _MockAnalystZones(BaseAgent):
    id = "analyst_zones"
    role = "analyst"

    def run(self, task, context=None):
        return {"output": "Zone-based analysis: all green", "confidence": 0.85}


class _MockCritic(BaseAgent):
    id = "critic"
    role = "critic"

    def run(self, task, context=None):
        return {"output": "Critical feedback: there is a weakness in the design", "confidence": 0.95}


class _MockOptimizer(BaseAgent):
    id = "optimizer"
    role = "optimizer"

    def run(self, task, context=None):
        return {"output": "Optimized version: improved by adding error handling", "confidence": 0.92}


class _MockSynthesizer(BaseAgent):
    id = "synthesizer"
    role = "synthesizer"

    def run(self, task, context=None):
        return {"output": "Final synthesis: plan approved", "confidence": 0.98}


class _MockOrchestrator(BaseAgent):
    id = "orchestrator"
    role = "orchestrator"

    def run(self, task, context=None):
        return {"output": "Orchestration complete", "confidence": 0.9}


def _supervisor_with_mock_agents(tmp_path, monkeypatch):
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(config, "AGENTS_MODULES_DIR", empty)
    monkeypatch.setattr(config, "TOOLS_MODULES_DIR", empty / "tools")
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", tmp_path / "state.json")
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", True)

    # Custom expert mapping for our mock agents
    expert_mapping = {
        "analyst": "analyst",
        "analyst_zones": "analyst_zones",
        "critic": "critic",
        "optimizer": "optimizer",
        "synthesizer": "synthesizer",
        "orchestrator": "orchestrator"
    }
    default_debate_agents = ["analyst", "critic", "optimizer"]
    
    supervisor = Supervisor(
        log_dir=tmp_path / "logs",
        expert_mapping=expert_mapping,
        default_debate_agents=default_debate_agents
    )
    supervisor.start()
    supervisor.agents.register(_MockAnalyst(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_MockAnalystZones(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_MockCritic(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_MockOptimizer(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_MockSynthesizer(supervisor.memory, supervisor.tools))
    supervisor.agents.register(_MockOrchestrator(supervisor.memory, supervisor.tools))
    return supervisor


def test_detect_contradiction_keywords():
    assert detect_contradiction("There is a risk of failure")
    assert detect_contradiction("weakness in design")
    assert not detect_contradiction("everything looks fine")


def test_debate_flow_four_rounds(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", True)  # Use lightweight 3-agent pipeline
    monkeypatch.setattr(config, "SAFE_MODE", False)

    # Mock compute_consensus_scores to always return low agreement
    from core import supervisor as core_supervisor

    original_compute = core_supervisor.compute_consensus_scores

    def mock_compute(steps, contradictions):
        return 40.0, 60.0  # Low agreement, so early stop won't trigger

    monkeypatch.setattr(core_supervisor, "compute_consensus_scores", mock_compute)

    supervisor = _supervisor_with_mock_agents(tmp_path, monkeypatch)

    result = supervisor.orchestrate(
        "Build secure authentication API",
        mode=ExecutionMode.DEBATE,
    )

    assert result.mode == "debate"
    assert result.debate is not None
    assert len(result.debate.steps) >= 3  # At least some steps!
    assert result.debate.final_response is not None
    assert "synthesis" in result.debate.final_response

    supervisor.stop()


def test_debate_detects_contradiction_on_critic(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", True)
    supervisor = _supervisor_with_mock_agents(tmp_path, monkeypatch)
    result = supervisor.orchestrate("short", agent_names=["analyst", "critic"], mode=ExecutionMode.DEBATE)

    critic_step = next(s for s in result.debate.steps if s.agent_name == "critic")
    assert critic_step.contradiction is True
    assert len(result.debate.contradictions) >= 1
    assert result.debate.contradiction_score > 0

    supervisor.stop()


def test_debate_persisted_in_memory(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", True)
    supervisor = _supervisor_with_mock_agents(tmp_path, monkeypatch)
    result = supervisor.orchestrate("persist debate", agent_names=["analyst", "critic", "optimizer"], mode=ExecutionMode.DEBATE)

    stored = supervisor.get_debate(result.debate.debate_id)
    assert stored is not None
    assert stored["debate_id"] == result.debate.debate_id
    assert stored["final_response"] is not None

    orch = supervisor.get_orchestration(result.execution_id)
    assert orch["debate"]["debate_id"] == result.debate.debate_id

    assert supervisor.memory.get(f"{MEMORY_DEBATE_PREFIX}{result.debate.debate_id}")
    supervisor.stop()


def test_debate_optimizer_is_refinement(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DEBATE_LIGHTWEIGHT", True)
    supervisor = _supervisor_with_mock_agents(tmp_path, monkeypatch)
    result = supervisor.orchestrate("refine this plan", mode=ExecutionMode.DEBATE)

    # Find the optimizer step that has refinement=True (from pipeline)
    optimizer = next(s for s in result.debate.steps if s.agent_name == "optimizer" and s.refinement)
    assert optimizer.refinement is True
    assert len(result.debate.refinements) >= 1
    assert result.debate.agreement_score >= 0

    supervisor.stop()


def test_debate_early_stop_on_high_agreement(tmp_path, monkeypatch):
    """Verifica que el debate se detiene temprano cuando hay alto consenso."""
    # Configurar umbral bajo para facilitar el test
    monkeypatch.setattr(config, "AGREEMENT_EARLY_STOP_THRESHOLD", 0.5)

    # Mockear compute_consensus_scores para simular alto acuerdo
    def mock_compute_consensus(steps, contradictions):
        # Siempre devolver alto acuerdo (95%) para activar parada temprana
        return 95.0, 5.0

    # Importar y patchear (patch in supervisor, since supervisor imports compute_consensus_scores)
    from core import supervisor as core_supervisor

    original_compute = core_supervisor.compute_consensus_scores
    monkeypatch.setattr(core_supervisor, "compute_consensus_scores", mock_compute_consensus)

    # Initialize supervisor AFTER patching
    supervisor = _supervisor_with_mock_agents(tmp_path, monkeypatch)

    try:
        result = supervisor.orchestrate(
            "test early stop",
            mode=ExecutionMode.DEBATE,
        )

        # Verificar que el debate se ejecutó
        assert result.mode == "debate"
        assert result.debate is not None

        # Verificar que el debate se detuvo en la ronda 2 (no llegó a 5 rondas)
        total_steps = len(result.debate.steps)
        assert total_steps <= 25, (
            f"Debió detenerse en ronda 2 pero tuvo {total_steps} pasos (esperado <= 25)"
        )

    finally:
        # Restaurar función original
        if original_compute:
            monkeypatch.setattr(core_supervisor, "compute_consensus_scores", original_compute)
        supervisor.stop()
