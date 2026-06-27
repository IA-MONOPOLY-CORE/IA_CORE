"""Evolution manager genérico para demo."""

from core.evolution_base import EvolutionManagerBase


class EvolutionManagerDemo(EvolutionManagerBase):
    """Evolution manager simple para el demo genérico."""

    def __init__(self):
        # Initialize with no memory path for demo
        super().__init__(memory_path=None, state_key="demo_evolution")

    def _get_initial_phase(self) -> str:
        return "inicio"

    def get_fase(self, evento: int) -> str:
        return "normal"

    def get_resultados_visibles_hasta(self, evento_actual: int) -> int:
        return evento_actual - 1

    def _get_instruccion_fase(self, fase: str) -> str:
        return "Sigue la conversación y participa constructivamente."
