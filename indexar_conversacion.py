"""Indexa conversaciones completas en la memoria vectorial de cada agente."""

from pathlib import Path

# Ruta donde están las conversaciones (ajustá según donde las tengas)
# Opción: crear un archivo .txt por agente con su conversación completa
CONVERSACIONES_DIR = Path("conversaciones_agentes")  # <- creá esta carpeta

# O podés pegar el texto directamente acá
CONVERSACIONES = {
    "estadistico_integral": """
        Aquí va el texto completo de la conversación con el Estadístico Integral.
        Pegá todo lo que hablaste con él.
    """,
    "gemini_cuantico": """
        Aquí va el texto completo de la conversación con Gemini Cuántico.
    """,
    "gpt_auditor": """
        Aquí va el texto completo de la conversación con GPT Auditor.
    """,
    "viejo_deepseek": """
        Aquí va el texto completo de la conversación con Viejo DeepSeek.
    """,
    "viejo_lobo_rey": """
        Aquí va el texto completo de la conversación con Viejo Lobo Rey.
    """,
    "nuevo_deepseek_saaop": """
        Aquí va el texto completo de la conversación con Nuevo DeepSeek.
    """,
}


def indexar_conversacion(agente_id: str, texto: str):
    """Indexa el texto completo en la memoria vectorial del agente."""
    from core.memoria_perpetua import sincronizar_memoria_vectorial

    if not texto.strip():
        print(f"❌ {agente_id}: texto vacío")
        return

    print(f"📄 Indexando {agente_id}...")
    fragmentos = sincronizar_memoria_vectorial(agente_id, texto)
    print(f"   ✅ Indexados {fragmentos} fragmentos")


if __name__ == "__main__":
    for agente_id, texto in CONVERSACIONES.items():
        indexar_conversacion(agente_id, texto)
