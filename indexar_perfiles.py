"""Indexa las conversaciones markdown de cada perfil en su memoria vectorial."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.memoria_perpetua import sincronizar_memoria_vectorial

# Ruta donde están los archivos markdown
RUTA_PERFILES = Path(
    r"C:\Users\Santi\Documents\Proyecto IA_CORE\mayo 2026\perfiles y paper\perfiles"
)

# Mapeo de archivo a agente_id
MAPEO = {
    "Estadístico Integral.md": "estadistico_integral",
    "experto comun.md": "viejo_lobo_rey",
    "experto cuantico.md": "gemini_cuantico",
    "gpt.md": "gpt_auditor",
    "nuevo deepeek.md": "nuevo_deepseek_saaop",
    "viejo deepeek.md": "viejo_deepseek",
}


def limpiar_markdown(texto: str) -> str:
    """Limpia formato markdown básico para quedarse solo con el texto."""
    # Eliminar bloques de código
    texto = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
    # Eliminar enlaces [texto](url)
    texto = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", texto)
    # Eliminar cabeceras #
    texto = re.sub(r"^#+\s+", "", texto, flags=re.MULTILINE)
    # Eliminar negritas/ cursivas * ** _
    texto = re.sub(r"\*{1,2}([^\*]+)\*{1,2}", r"\1", texto)
    texto = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", texto)
    return texto


def indexar_perfil(archivo: Path, agente_id: str):
    """Lee el archivo y lo indexa en la memoria vectorial del agente."""
    if not archivo.exists():
        print(f"❌ {archivo.name}: no encontrado")
        return False

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            texto_raw = f.read()

        texto_limpio = limpiar_markdown(texto_raw)

        if not texto_limpio.strip():
            print(f"⚠️ {archivo.name}: texto vacío después de limpiar")
            return False

        print(f"📄 Indexando {agente_id} desde {archivo.name} ({len(texto_limpio)} caracteres)...")
        fragmentos = sincronizar_memoria_vectorial(agente_id, texto_limpio)
        print(f"   ✅ Indexados {fragmentos} fragmentos")
        return True

    except Exception as e:
        print(f"❌ Error con {archivo.name}: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("INDEXANDO PERFILES A MEMORIA VECTORIAL")
    print("=" * 60)

    if not RUTA_PERFILES.exists():
        print(f"❌ Ruta no encontrada: {RUTA_PERFILES}")
        sys.exit(1)

    indexados = 0
    for nombre_archivo, agente_id in MAPEO.items():
        archivo = RUTA_PERFILES / nombre_archivo
        if indexar_perfil(archivo, agente_id):
            indexados += 1

    print("\n" + "=" * 60)
    print(f"✅ Total indexados: {indexados}/{len(MAPEO)}")
    print("=" * 60)
