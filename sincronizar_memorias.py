"""Sincroniza todas las memorias JSON existentes a memoria vectorial (ChromaDB)."""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from core.memoria_perpetua import sincronizar_memoria_vectorial

# Lista de agentes que tienen memoria JSON
agentes = [
    "estadistico_integral",
    "gpt_auditor",
    "gemini_cuantico",
    "viejo_lobo_rey",
    "viejo_deepseek",
]

print("=" * 50)
print("SINCRONIZANDO MEMORIAS A VECTORIAL")
print("=" * 50)

for agente in agentes:
    print(f"\n📦 Procesando {agente}...")
    try:
        sincronizar_memoria_vectorial(agente)
    except Exception as e:
        print(f"❌ Error con {agente}: {e}")

print("\n" + "=" * 50)
print("✅ SINCRONIZACIÓN COMPLETADA")
print("=" * 50)
