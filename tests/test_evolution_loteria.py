import config

from domains.loteria.evolution_loteria import EvolutionManagerLoteria


def test_evolution_uses_configured_memory_path_and_recalculates_phase(monkeypatch, tmp_path):
    state_path = tmp_path / "state.json"
    monkeypatch.setattr(config, "MEMORY_STATE_FILE", state_path)

    evolution = EvolutionManagerLoteria()
    ciclo = evolution._state["evolucion_lotoplus"]["ciclo_actual"]
    ciclo["sorteo_actual"] = 3800
    ciclo["fase_actual"] = "entrenamiento"

    stats = evolution.get_estadisticas_ciclo()

    assert evolution.memory_path == state_path
    assert stats["fase_actual"] == "validacion_ciega"
    assert ciclo["fase_actual"] == "validacion_ciega"
