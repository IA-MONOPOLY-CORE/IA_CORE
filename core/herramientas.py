"""Sistema de herramientas compartidas entre agentes."""

import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Ruta del archivo global de herramientas
HERRAMIENTAS_PATH = Path(__file__).parent.parent / "memory" / "herramientas_compartidas.json"

# Modelo local para traducciones (evita usar NVIDIA)
TRADUCTOR_MODELO = "phi3:mini"


def _cargar_herramientas_globales() -> dict:
    """Carga el registro global de herramientas."""
    if not HERRAMIENTAS_PATH.exists():
        return {"herramientas": [], "ultima_actualizacion": None, "versiones_por_agente": {}}

    with open(HERRAMIENTAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_herramientas_globales(data: dict):
    """Guarda el registro global de herramientas."""
    data["ultima_actualizacion"] = datetime.now().isoformat()
    with open(HERRAMIENTAS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def registrar_herramienta(
    nombre: str,
    descripcion: str,
    agente_creador: str,
    rol_asociado: str,
    contexto_exito: str,
    score: float,
):
    """
    Registra una herramienta nueva en el repositorio global.
    Si ya existe una similar, se actualiza la versión.
    """
    herramientas = _cargar_herramientas_globales()

    # Buscar si ya existe una herramienta similar
    herramienta_existente = None
    for h in herramientas["herramientas"]:
        if h["nombre"].lower() == nombre.lower():
            herramienta_existente = h
            break

    if herramienta_existente:
        # Actualizar versión
        herramienta_existente["versiones"].append(
            {
                "descripcion": descripcion,
                "agente": agente_creador,
                "rol": rol_asociado,
                "contexto": contexto_exito,
                "score": score,
                "fecha": datetime.now().isoformat(),
            }
        )
        herramienta_existente["ultima_version"] = herramienta_existente["versiones"][-1]
    else:
        # Crear nueva herramienta
        herramientas["herramientas"].append(
            {
                "nombre": nombre,
                "versiones": [
                    {
                        "descripcion": descripcion,
                        "agente": agente_creador,
                        "rol": rol_asociado,
                        "contexto": contexto_exito,
                        "score": score,
                        "fecha": datetime.now().isoformat(),
                    }
                ],
                "ultima_version": {
                    "descripcion": descripcion,
                    "agente": agente_creador,
                    "rol": rol_asociado,
                    "contexto": contexto_exito,
                    "score": score,
                },
                "agentes_que_la_adoptaron": [],
            }
        )

    _guardar_herramientas_globales(herramientas)
    return True


def traducir_herramienta_a_rol(
    herramienta: dict, rol_destino: str, usar_ollama: bool = True
) -> Optional[str]:
    """
    Traduce una herramienta al lenguaje de un rol específico.
    Usa Ollama local para evitar consumir tokens de NVIDIA.

    Args:
        herramienta: La herramienta a traducir (de herramientas_compartidas.json)
        rol_destino: El rol al que traducir (critic, analyst, optimizer, orchestrator)
        usar_ollama: Si usar Ollama (True) o traducción simple (False)

    Returns:
        Texto traducido listo para inyectar en el prompt del agente
    """
    nombre = herramienta.get("nombre", "Herramienta")
    version = herramienta.get("ultima_version", {})
    descripcion = version.get("descripcion", "")
    contexto = version.get("contexto", "")
    score = version.get("score", 0)
    rol_origen = version.get("rol", "unknown")

    if not descripcion:
        return None

    # Traducción simple sin LLM (para ahorrar recursos)
    if not usar_ollama:
        traduccion = f"""
[TOOL: {nombre} (score: {score})]
Descripción: {descripcion}
Contexto de éxito: {contexto}
Apropiada desde rol {rol_origen} → aplicable desde mi rol {rol_destino}
"""
        return traduccion

    # Usar Ollama para traducción más natural
    try:
        import requests

        prompt = f"""Traducí esta herramienta al lenguaje de un agente con rol '{rol_destino}'.

La herramienta fue creada por un agente con rol '{rol_origen}'.

DESCRIPCIÓN ORIGINAL: {descripcion}

CONTEXTO DE ÉXITO: {contexto}

SCORE: {score}

INSTRUCCIONES:
- Reescribí la herramienta como si el agente {rol_destino} la hubiera descubierto él mismo.
- Mantené la esencia, cambiá el enfoque según el rol.
- {rol_destino} debe poder usarla desde su función específica.
- Máximo 150 palabras.

RESPUESTA (solo la herramienta traducida, sin explicaciones):"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": TRADUCTOR_MODELO,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 300},
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            traduccion = data.get("response", "")
            if traduccion:
                return f"\n[TOOL: {nombre} (apropiada desde rol {rol_origen})]\n{traduccion}\n"

    except Exception as e:
        logger.warning(f"⚠️ Error traduciendo con Ollama: {e}", exc_info=True)

    # Fallback a traducción simple
    return f"""
[TOOL: {nombre} (score: {score})]
Apropiada desde {rol_origen} → aplicable como {rol_destino}:
{descripcion[:300]}
"""


def obtener_herramientas_para_agente(agente_id: str, rol: str, top_k: int = 5) -> List[str]:
    """
    Obtiene herramientas relevantes para un agente específico.
    Prioriza:
    1. Herramientas que el agente ya adoptó (de su memoria)
    2. Herramientas de alto score de otros roles, traducidas
    """
    herramientas_globales = _cargar_herramientas_globales()

    # Cargar herramientas que el agente ya adoptó desde su memoria
    herramientas_adoptadas = set()
    try:
        from core.memoria_perpetua import cargar_memoria

        memoria = cargar_memoria(agente_id)
        herramientas_adoptadas = set(memoria.get("herramientas_adoptadas", []))
    except Exception:
        pass

    resultados = []

    for h in herramientas_globales.get("herramientas", []):
        # Si el agente ya la adoptó, no la incluimos de nuevo
        if h["nombre"] in herramientas_adoptadas:
            continue

        score = h.get("ultima_version", {}).get("score", 0)
        rol_origen = h.get("ultima_version", {}).get("rol", "unknown")

        # Solo herramientas con score >= 60
        if score >= 60:
            traduccion = traducir_herramienta_a_rol(h, rol, usar_ollama=True)
            if traduccion:
                resultados.append(
                    {
                        "nombre": h["nombre"],
                        "score": score,
                        "rol_origen": rol_origen,
                        "traduccion": traduccion,
                    }
                )

    # Ordenar por score y limitar
    resultados.sort(key=lambda x: x["score"], reverse=True)
    return [r["traduccion"] for r in resultados[:top_k]]


def marcar_herramienta_como_adoptada(agente_id: str, herramienta_nombre: str):
    """Registra que un agente adoptó una herramienta."""
    try:
        from core.memoria_perpetua import cargar_memoria, guardar_memoria

        memoria = cargar_memoria(agente_id)
        if "herramientas_adoptadas" not in memoria:
            memoria["herramientas_adoptadas"] = []

        if herramienta_nombre not in memoria["herramientas_adoptadas"]:
            memoria["herramientas_adoptadas"].append(herramienta_nombre)
            guardar_memoria(agente_id, memoria)

            # También registrar en el global
            herramientas = _cargar_herramientas_globales()
            for h in herramientas.get("herramientas", []):
                if h["nombre"] == herramienta_nombre:
                    if agente_id not in h["agentes_que_la_adoptaron"]:
                        h["agentes_que_la_adoptaron"].append(agente_id)
                    break
            _guardar_herramientas_globales(herramientas)

            return True
    except Exception as e:
        logger.warning(f"⚠️ Error marcando herramienta como adoptada: {e}", exc_info=True)

    return False


def extraer_herramientas_de_respuesta(
    respuesta: str, score: float, agente_id: str, rol: str
) -> List[dict]:
    """
    Analiza la respuesta de un agente y extrae posibles herramientas.
    Detecta patrones como "usé X", "apliqué Y", "funcionó Z".
    """
    herramientas_encontradas = []

    patrones = [
        r"us[ée]\s+([A-ZÁÉÍÓÚÑ0-9]+)",
        r"apliqu[ée]\s+([A-ZÁÉÍÓÚÑ0-9]+)",
        r"funcion[óo]\s+([A-ZÁÉÍÓÚÑ0-9]+)",
        r"herramienta\s+([A-ZÁÉÍÓÚÑ0-9]+)",
        r"métrica\s+([A-ZÁÉÍÓÚÑ0-9]+)",
    ]

    for patron in patrones:
        matches = re.findall(patron, respuesta, re.IGNORECASE)
        for match in matches:
            nombre = match.upper()
            if len(nombre) >= 3 and len(nombre) <= 20:
                herramientas_encontradas.append(
                    {
                        "nombre": nombre,
                        "descripcion": respuesta[:300],
                        "contexto": respuesta[:500],
                        "score": score,
                        "agente": agente_id,
                        "rol": rol,
                    }
                )

    return herramientas_encontradas


# ========================================================================
# PUNTO 4.3: BUSCAR LECCIONES ÚTILES
# ========================================================================


def buscar_lecciones_utiles(rol: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Busca lecciones útiles para un rol específico desde la memoria compartida.

    Args:
        rol: Rol del agente que busca (analyst, critic, optimizer, orchestrator, etc.)
        top_k: Cantidad máxima de lecciones a retornar

    Returns:
        Lista de diccionarios con lecciones útiles
    """
    if not HERRAMIENTAS_PATH.exists():
        return []

    try:
        with open(HERRAMIENTAS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.warning(f"⚠️ Error cargando herramientas_compartidas.json: {e}", exc_info=True)
        return []

    lecciones_utiles = []

    # 1. Extraer lecciones de contradicciones_resueltas
    for contradiccion in data.get("contradicciones_resueltas", []):
        leccion = {
            "tipo": "contradiccion_resuelta",
            "timestamp": contradiccion.get("timestamp"),
            "contenido": contradiccion.get("leccion", ""),
            "score": contradiccion.get("mejor_score", 0),
            "agentes_participantes": contradiccion.get("agentes_participantes", []),
            "consenso_final": contradiccion.get("consenso_final", 0),
            "relevancia": 0,  # se calcula después
        }

        # Calcular relevancia basada en score y consenso
        leccion["relevancia"] = (leccion["score"] * 0.6) + (leccion["consenso_final"] * 0.4)
        lecciones_utiles.append(leccion)

    # 2. Extraer lecciones de lecciones_compartidas
    for leccion in data.get("lecciones_compartidas", []):
        leccion_item = {
            "tipo": "leccion_compartida",
            "timestamp": leccion.get("timestamp"),
            "contenido": leccion.get("contenido", ""),
            "autor": leccion.get("autor", ""),
            "rol_autor": leccion.get("rol_autor", ""),
            "score": leccion.get("score", 0),
            "relevancia": leccion.get("score", 0),
        }

        # Si el rol del autor coincide con el rol buscado, priorizar
        if leccion_item.get("rol_autor") == rol:
            leccion_item["relevancia"] += 20

        lecciones_utiles.append(leccion_item)

    # 3. Ordenar por relevancia y limitar
    lecciones_utiles.sort(key=lambda x: x.get("relevancia", 0), reverse=True)

    return lecciones_utiles[:top_k]


# ========================================================================
# PUNTO 4.4: ABSORBER LECCIÓN
# ========================================================================


def absorber_leccion(agente_id: str, leccion: Dict[str, Any]) -> bool:
    """
    Un agente absorbe una lección y la incorpora a su memoria.

    Args:
        agente_id: ID del agente que absorbe la lección
        leccion: Diccionario con la lección (de buscar_lecciones_utiles)

    Returns:
        True si se absorbió correctamente
    """
    try:
        from core.memoria_perpetua import cargar_memoria, guardar_memoria

        memoria = cargar_memoria(agente_id)

        # Inicializar estructuras si no existen
        if "lecciones_absorbidas" not in memoria:
            memoria["lecciones_absorbidas"] = []

        # Evitar duplicados
        contenido = leccion.get("contenido", "")
        for existente in memoria["lecciones_absorbidas"]:
            if existente.get("contenido") == contenido:
                return False  # ya la tiene

        # Agregar lección
        leccion_absorbida = {
            "contenido": contenido,
            "tipo": leccion.get("tipo", "desconocido"),
            "fecha_absorcion": datetime.now().isoformat(),
            "relevancia": leccion.get("relevancia", 0),
            "score_original": leccion.get("score", 0),
            "aplicada": False,
        }

        memoria["lecciones_absorbidas"].append(leccion_absorbida)

        # Mantener solo las últimas 50 lecciones
        if len(memoria["lecciones_absorbidas"]) > 50:
            memoria["lecciones_absorbidas"] = memoria["lecciones_absorbidas"][-50:]

        guardar_memoria(agente_id, memoria)

        logger.info(
            f"📚 {agente_id}: Lección absorbida exitosamente (relevancia: {leccion.get('relevancia', 0)})"
        )
        return True

    except Exception as e:
        logger.warning(f"⚠️ Error absorbiendo lección para {agente_id}: {e}", exc_info=True)
        return False


def aplicar_lecciones_pendientes(agente_id: str, contexto_actual: str) -> Optional[str]:
    """
    Aplica lecciones absorbidas pero no aplicadas en el contexto actual.
    Retorna un texto formateado para inyectar en el prompt del agente.
    """
    try:
        from core.memoria_perpetua import cargar_memoria, guardar_memoria

        memoria = cargar_memoria(agente_id)
        lecciones_no_aplicadas = [
            l for l in memoria.get("lecciones_absorbidas", []) if not l.get("aplicada", False)
        ]

        if not lecciones_no_aplicadas:
            return None

        # Seleccionar la lección más relevante para el contexto
        # Por ahora, tomamos la de mayor relevancia
        mejor_leccion = max(lecciones_no_aplicadas, key=lambda x: x.get("relevancia", 0))

        # Marcar como aplicada
        for l in memoria["lecciones_absorbidas"]:
            if l.get("contenido") == mejor_leccion.get("contenido"):
                l["aplicada"] = True
                l["fecha_aplicacion"] = datetime.now().isoformat()
                break

        guardar_memoria(agente_id, memoria)

        # Formatear para inyectar en prompt
        return f"""
[LECCIÓN APRENDIDA - APLICAR AHORA]
{mejor_leccion.get("contenido", "")}
[FIN LECCIÓN]
"""

    except Exception as e:
        logger.warning(
            f"⚠️ Error aplicando lecciones pendientes para {agente_id}: {e}", exc_info=True
        )
        return None
