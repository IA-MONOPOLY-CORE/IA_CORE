"""Cargar memoria de un agente desde un archivo de chat (TXT o JSON)"""

import json
from pathlib import Path

# Agregar la ruta del proyecto para poder importar
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.memoria_perpetua import cargar_memoria, guardar_memoria


def cargar_memoria_desde_texto(agente_id: str, archivo_txt: Path):
    """
    Carga la memoria de un agente desde un archivo de texto.
    
    Args:
        agente_id: ID del agente (ej: "estadistico_integral")
        archivo_txt: Ruta al archivo .txt con el chat entrenado
    """
    if not archivo_txt.exists():
        print(f"❌ Archivo no encontrado: {archivo_txt}")
        return False
    
    with open(archivo_txt, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    memoria = cargar_memoria(agente_id)
    memoria["conocimiento_base"] = contenido
    memoria["notas_personalizadas"] = f"Cargado desde {archivo_txt.name}"
    
    guardar_memoria(agente_id, memoria)
    print(f"✅ Memoria cargada para {agente_id} desde {archivo_txt.name}")
    return True


def cargar_memoria_desde_json(agente_id: str, archivo_json: Path):
    """
    Carga la memoria de un agente desde un archivo JSON estructurado.
    
    Args:
        agente_id: ID del agente
        archivo_json: Ruta al archivo .json con la memoria preformateada
    """
    if not archivo_json.exists():
        print(f"❌ Archivo no encontrado: {archivo_json}")
        return False
    
    with open(archivo_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    memoria = cargar_memoria(agente_id)
    
    # Actualizar campos según el JSON
    if "conocimiento_base" in datos:
        memoria["conocimiento_base"] = datos["conocimiento_base"]
    if "patrones_aprendidos" in datos:
        memoria["patrones_aprendidos"] = datos["patrones_aprendidos"]
    if "notas_personales" in datos:
        memoria["notas_personales"] = datos["notas_personales"]
    
    guardar_memoria(agente_id, memoria)
    print(f"✅ Memoria cargada para {agente_id} desde {archivo_json.name}")
    return True


def ver_memoria(agente_id: str):
    """Muestra la memoria actual de un agente"""
    memoria = cargar_memoria(agente_id)
    print(f"\n📚 MEMORIA DE {agente_id}:")
    print(f"   Conocimiento base: {len(memoria.get('conocimiento_base', ''))} caracteres")
    print(f"   Patrones aprendidos: {len(memoria.get('patrones_aprendidos', []))}")
    print(f"   Errores cometidos: {len(memoria.get('errores_cometidos', []))}")
    print(f"   Última actualización: {memoria.get('ultima_actualizacion', 'Nunca')}")


if __name__ == "__main__":
    # Ejemplos de uso:
    
    # 1. Ver memoria de un agente
    # ver_memoria("estadistico_integral")
    
    # 2. Cargar desde archivo TXT
    # cargar_memoria_desde_texto("estadistico_integral", Path("C:/mis_chats/estadistico.txt"))
    
    # 3. Cargar desde archivo JSON
    # cargar_memoria_desde_json("gpt_auditor", Path("C:/mis_chats/auditor.json"))
    
    print("🔧 Script listo. Descomentá las líneas que necesites usar.")