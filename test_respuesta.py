"""Prueba de generación de respuestas largas."""

from providers.nvidia_provider import NvidiaProvider
from config import NVIDIA_API_KEY

p = NvidiaProvider(api_key=NVIDIA_API_KEY)

prompt = """Eres el Estadístico Integral. Analizá el sorteo 3790 usando los datos históricos.

Respondé con un análisis detallado incluyendo:
- Patrones detectados
- Números calientes y fríos
- Predicción para el próximo sorteo
- Confianza en porcentaje

Sé extenso y detallado. Escribí al menos 500 palabras."""

print("Generando respuesta...")
response = p.generate(prompt=prompt, model="meta/llama-3.1-8b-instruct", temperature=0.3)

print("\n" + "=" * 60)
print("RESPUESTA COMPLETA:")
print("=" * 60)
print(response.text)
print("\n" + "=" * 60)
print(f"LONGITUD: {len(response.text)} caracteres")
print(f"TOKENS DE SALIDA: {response.metadata.get('completion_tokens')}")
print(f"TOKENS DE ENTRADA: {response.metadata.get('prompt_tokens')}")
print(f"LATENCIA: {response.metadata.get('latency_ms')} ms")
print("=" * 60)
