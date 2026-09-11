"""Explicit NVIDIA integration probe; never executes during import or default pytest."""

import os

import pytest


PROMPT = """Eres el Estadístico Integral. Analizá el sorteo 3790 usando los datos históricos.

Respondé con un análisis detallado incluyendo:
- Patrones detectados
- Números calientes y fríos
- Predicción para el próximo sorteo
- Confianza en porcentaje

Sé extenso y detallado. Escribí al menos 500 palabras."""


def _external_tests_enabled() -> bool:
    return os.environ.get("IA_CORE_ALLOW_EXTERNAL_TESTS") == "1"


@pytest.mark.external
def test_nvidia_response_integration():
    """Run only with explicit external-test authorization and a configured key."""
    if not _external_tests_enabled():
        pytest.skip(
            "NVIDIA integration is opt-in; set IA_CORE_ALLOW_EXTERNAL_TESTS=1 explicitly"
        )

    from config import NVIDIA_API_KEY
    from providers.nvidia_provider import NvidiaProvider

    if not NVIDIA_API_KEY:
        pytest.skip("NVIDIA_API_KEY is not configured for the explicit integration run")

    response = NvidiaProvider(api_key=NVIDIA_API_KEY).generate(
        prompt=PROMPT,
        model="meta/llama-3.1-8b-instruct",
        temperature=0.3,
    )
    assert response.text


if __name__ == "__main__":
    if not _external_tests_enabled():
        raise SystemExit(
            "test_respuesta.py is an external integration probe; "
            "set IA_CORE_ALLOW_EXTERNAL_TESTS=1 explicitly"
        )
    raise SystemExit(pytest.main([__file__, "-v", "-m", "external"]))
