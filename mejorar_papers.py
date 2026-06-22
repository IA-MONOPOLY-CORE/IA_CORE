"""Mejora los papers existentes con información de la memoria del agente (JSON + vectorial)."""

import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from core.memoria_perpetua import MemoriaVectorial, cargar_memoria
from providers.registry import ProviderRegistry


def cargar_paper_manual(agente_id: str) -> dict:
    """Carga el paper manual existente."""
    paper_path = Path("agents/papers") / f"{agente_id}_paper.json"
    if paper_path.exists():
        with open(paper_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def extraer_lecciones_de_memoria_json(agente_id: str) -> dict:
    """
    Extrae lecciones aprendidas de la memoria JSON del agente.
    Esto es NUEVO: usa patrones_aprendidos, errores_cometidos, aciertos_historicos.
    """
    memoria = cargar_memoria(agente_id)
    
    patrones = memoria.get("patrones_aprendidos", [])
    errores = memoria.get("errores_cometidos", [])
    aciertos = memoria.get("aciertos_historicos", [])
    
    lecciones = {
        "reglas_clave": [],
        "lecciones_aprendidas": [],
        "errores_a_evitar": [],
        "aciertos_recientes": []
    }
    
    # Extraer patrones como reglas clave
    for p in patrones[-10:]:  # últimos 10
        if isinstance(p, dict):
            texto = p.get("patron", str(p))[:200]
            if texto and len(texto) > 20:
                lecciones["reglas_clave"].append(texto)
        elif isinstance(p, str) and len(p) > 20:
            lecciones["reglas_clave"].append(p[:200])
    
    # Extraer errores como "errores a evitar"
    for e in errores[-10:]:
        if isinstance(e, dict):
            texto = e.get("error", str(e))[:200]
            if texto:
                lecciones["errores_a_evitar"].append(texto)
        elif isinstance(e, str) and len(e) > 10:
            lecciones["errores_a_evitar"].append(e[:200])
    
    # Extraer aciertos como lecciones aprendidas
    for a in aciertos[-5:]:
        if isinstance(a, dict):
            texto = a.get("acierto", a.get("descripcion", str(a)))[:200]
            if texto:
                lecciones["lecciones_aprendidas"].append(texto)
        elif isinstance(a, str) and len(a) > 20:
            lecciones["lecciones_aprendidas"].append(a[:200])
    
    return lecciones


def generar_desde_memoria_vectorial(agente_id: str, llm) -> dict:
    """Genera paper desde la memoria vectorial (como estaba originalmente)."""
    mv = MemoriaVectorial(agente_id)
    if not mv.esta_disponible():
        print(f"   ⚠️ Memoria vectorial no disponible para {agente_id}")
        return None
    
    consulta = f"¿Cuál es tu identidad, reglas clave, lecciones aprendidas y errores a evitar como {agente_id}?"
    resultados = mv.buscar(consulta, top_k=30)
    
    if not resultados:
        print(f"   ⚠️ No se encontraron fragmentos vectoriales para {agente_id}")
        return None
    
    contexto = "\n\n---\n\n".join([r["texto"][:1000] for r in resultados[:15]])
    
    prompt = f"""Eres un arquitecto de identidades. Basado en los fragmentos de conversación del agente '{agente_id}', extraé:

1. reglas_clave (lista de 3-5 reglas que sigue)
2. lecciones_aprendidas (lista de 2-4 lecciones importantes)
3. errores_a_evitar (lista de 2-4 errores que menciona)
4. estilo_respuesta (1 línea describiendo cómo responde)

DEVOLVÉ SOLO JSON:
{{
  "reglas_clave": ["regla 1", "regla 2"],
  "lecciones_aprendidas": ["lección 1", "lección 2"],
  "errores_a_evitar": ["error 1", "error 2"],
  "estilo_respuesta": "descripción"
}}

Fragmentos:
{contexto[:6000]}"""
    
    response = llm.generate(prompt, model="meta/llama-3.1-8b-instruct", temperature=0.3)
    
    if hasattr(response, 'text'):
        texto = response.text
    elif hasattr(response, 'output'):
        texto = response.output
    else:
        texto = str(response)
    
    json_match = re.search(r'\{[^{}]*\{?[^{}]*\}?[^{}]*\}', texto, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            print(f"   ⚠️ Error parseando JSON de memoria vectorial")
            return None
    return None


def merge_todos_los_papers(manual: dict, desde_json: dict, desde_vectorial: dict) -> dict:
    """
    Fusiona:
    - Paper manual (identidad base)
    - Lecciones desde memoria JSON (patrones, errores, aciertos)
    - Lecciones desde memoria vectorial
    """
    if not manual:
        resultado = {
            "agente_id": "unknown",
            "identidad": "Identidad no definida",
            "reglas_clave": [],
            "lecciones_aprendidas": [],
            "errores_a_evitar": [],
            "estilo_respuesta": "Técnico, directo"
        }
    else:
        resultado = manual.copy()
    
    # Agregar lecciones desde JSON (prioridad alta, son experiencias reales)
    if desde_json:
        if desde_json.get("reglas_clave"):
            reglas_existentes = set(resultado.get("reglas_clave", []))
            for r in desde_json["reglas_clave"]:
                if r not in reglas_existentes:
                    resultado.setdefault("reglas_clave", []).append(r)
        
        if desde_json.get("lecciones_aprendidas"):
            lecciones_existentes = set(resultado.get("lecciones_aprendidas", []))
            for l in desde_json["lecciones_aprendidas"]:
                if l not in lecciones_existentes:
                    resultado.setdefault("lecciones_aprendidas", []).append(l)
        
        if desde_json.get("errores_a_evitar"):
            errores_existentes = set(resultado.get("errores_a_evitar", []))
            for e in desde_json["errores_a_evitar"]:
                if e not in errores_existentes:
                    resultado.setdefault("errores_a_evitar", []).append(e)
    
    # Agregar desde vectorial (complementa)
    if desde_vectorial:
        if desde_vectorial.get("reglas_clave"):
            reglas_existentes = set(resultado.get("reglas_clave", []))
            for r in desde_vectorial["reglas_clave"]:
                if r not in reglas_existentes:
                    resultado.setdefault("reglas_clave", []).append(r)
        
        if desde_vectorial.get("lecciones_aprendidas"):
            lecciones_existentes = set(resultado.get("lecciones_aprendidas", []))
            for l in desde_vectorial["lecciones_aprendidas"]:
                if l not in lecciones_existentes:
                    resultado.setdefault("lecciones_aprendidas", []).append(l)
        
        if desde_vectorial.get("errores_a_evitar"):
            errores_existentes = set(resultado.get("errores_a_evitar", []))
            for e in desde_vectorial["errores_a_evitar"]:
                if e not in errores_existentes:
                    resultado.setdefault("errores_a_evitar", []).append(e)
        
        if desde_vectorial.get("estilo_respuesta"):
            resultado["estilo_respuesta"] = desde_vectorial["estilo_respuesta"]
    
    # Limitar listas a 10 elementos máximo
    for key in ["reglas_clave", "lecciones_aprendidas", "errores_a_evitar"]:
        if key in resultado and len(resultado[key]) > 10:
            resultado[key] = resultado[key][:10]
    
    # Agregar metadatos de última actualización
    resultado["ultima_actualizacion"] = datetime.now().isoformat()
    
    return resultado


def mejorar_paper(agente_id: str, usar_llm: bool = True):
    """Mejora un paper existente con información de la memoria."""
    print(f"\n📄 Mejorando paper para {agente_id}...")
    
    manual = cargar_paper_manual(agente_id)
    if manual:
        print(f"   ✅ Paper manual encontrado")
    else:
        print(f"   ⚠️ Sin paper manual, se creará uno nuevo")
    
    # 1. Extraer lecciones desde memoria JSON (siempre disponible)
    lecciones_json = extraer_lecciones_de_memoria_json(agente_id)
    print(f"   📊 Desde JSON: {len(lecciones_json.get('reglas_clave', []))} reglas, {len(lecciones_json.get('errores_a_evitar', []))} errores")
    
    # 2. Generar desde memoria vectorial (requiere LLM)
    lecciones_vectorial = None
    if usar_llm:
        providers = ProviderRegistry()
        providers.load_builtin_providers()
        llm = providers.get("nvidia")
        
        if llm:
            lecciones_vectorial = generar_desde_memoria_vectorial(agente_id, llm)
            if lecciones_vectorial:
                print(f"   🤖 Desde vectorial: {len(lecciones_vectorial.get('reglas_clave', []))} reglas, {len(lecciones_vectorial.get('lecciones_aprendidas', []))} lecciones")
        else:
            print("   ⚠️ No se pudo cargar LLM, omitiendo memoria vectorial")
    else:
        print("   ⏭️ Modo sin LLM: usando solo memoria JSON")
    
    # 3. Fusionar todo
    final = merge_todos_los_papers(manual, lecciones_json, lecciones_vectorial or {})
    
    # 4. Guardar
    paper_path = Path("agents/papers") / f"{agente_id}_paper.json"
    with open(paper_path, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Paper mejorado guardado en {paper_path}")
    return final


def regenerar_todos_los_papers(usar_llm: bool = True):
    """Regenera todos los papers de los agentes."""
    agentes = [
        "estadistico_integral",
        "gemini_cuantico",
        "gpt_auditor",
        "viejo_deepseek",
        "viejo_lobo_rey",
        "nuevo_deepseek_saaop"
    ]
    
    print("=" * 60)
    print("REGENERANDO PAPERS CON MEMORIA DEL AGENTE")
    print("=" * 60)
    print(f"Modo LLM: {'activado' if usar_llm else 'desactivado (solo JSON)'}")
    print("=" * 60)
    
    for agente in agentes:
        mejorar_paper(agente, usar_llm=usar_llm)
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS PAPERS REGENERADOS")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerar papers de agentes desde su memoria")
    parser.add_argument("--agente", type=str, help="ID de un agente específico (opcional)")
    parser.add_argument("--no-llm", action="store_true", help="No usar LLM, solo memoria JSON")
    parser.add_argument("--periodico", action="store_true", help="Modo periódico (sin output verbose)")
    args = parser.parse_args()
    
    if args.periodico:
        # Modo silencioso para ejecución automática
        import logging
        logging.disable(logging.CRITICAL)
    
    if args.agente:
        mejorar_paper(args.agente, usar_llm=not args.no_llm)
    else:
        regenerar_todos_los_papers(usar_llm=not args.no_llm)