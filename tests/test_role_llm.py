from typing import Any

from agents.role_agent import RoleAgent
from agents.roles import AgentRole
from agents.result import is_agent_success
from providers.base import BaseProvider, GenerateResponse, HealthStatus


class _MockProvider(BaseProvider):
    def provider_name(self) -> str:
        return "mock"

    def available_models(self) -> list[str]:
        return ["mock-model"]

    def health_check(self) -> HealthStatus:
        return HealthStatus(healthy=True)

    def generate(self, prompt: str, model: str | None = None, **kwargs: Any) -> GenerateResponse:
        return GenerateResponse(
            text="Structured analysis. Key risk: scalability problem and weakness in auth.",
            provider="mock",
            model=model or "mock-model",
            metadata={"latency_ms": 1.0},
        )


class _FailProvider(BaseProvider):
    def provider_name(self) -> str:
        return "fail"

    def available_models(self) -> list[str]:
        return ["x"]

    def health_check(self) -> HealthStatus:
        return HealthStatus(healthy=False)

    def generate(self, prompt: str, model: str | None = None, **kwargs: Any) -> GenerateResponse:
        raise TimeoutError("provider timeout")


class _Analyst(RoleAgent):
    id = "analyst"
    role = AgentRole.ANALYST


def test_role_agent_calls_llm(tmp_path):
    from memory.manager import MemoryManager

    memory = MemoryManager(state_path=tmp_path / "state.json")
    agent = _Analyst(memory=memory, llm_provider=_MockProvider())
    agent.model = "mock-model"

    result = agent.run("design api", context={})

    assert result["ok"] is True
    assert "risk" in result["output"].lower()
    assert result["llm"]["provider"] == "mock"
    assert is_agent_success(result)


def test_role_agent_provider_failure_does_not_raise(tmp_path):
    from memory.manager import MemoryManager

    memory = MemoryManager(state_path=tmp_path / "state.json")
    agent = _Analyst(memory=memory, llm_provider=_FailProvider())

    result = agent.run("task", context={})

    assert result["ok"] is False
    assert result.get("error")
    assert not is_agent_success(result)
