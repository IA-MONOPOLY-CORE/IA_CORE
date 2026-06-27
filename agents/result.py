"""Utilidades para resultados de agentes - CON MÉTRICAS REALES PARA LOTO PLUS - VERSIÓN 5 AGENTES"""

from __future__ import annotations

from typing import Any


def is_agent_success(result: Any) -> bool:
    """True si el agente completó sin error estructurado."""
    if isinstance(result, dict):
        if result.get("ok") is False:
            return False
        if result.get("error"):
            return False
    return True


def error_output(message: str, *, provider: str | None = None, model: str | None = None) -> str:
    return f"[error] {message} (provider={provider or '-'}, model={model or '-'})"


# ============= NUEVAS FUNCIONES PARA LOTO PLUS - 5 AGENTES =============


def calcular_contradiccion_real(intervenciones: dict) -> float:
    """
    Calcula contradicción basada en disimilitud de contenido entre CRITIC y el TOTAL de ANALYSTS.

    Para 5 agentes:
    - CRITIC (gpt_auditor) ataca
    - ANALYSTS: gemini_cuantico + viejo_lobo_rey + estadistico_integral defienden/analizan
    - La contradicción se mide entre CRITIC y la COMBINACIÓN de los 3 ANALYSTS

    Args:
        intervenciones: dict con claves 'CRITIC', 'ANALYST_ZONAS', 'ANALYST_HUMAN', 'ANALYST_V19'

    Returns:
        float: 0-100% de contradicción (mayor = más contradicción)
    """
    critic_text = intervenciones.get("CRITIC", "")

    # Combinar los 3 analysts en un solo texto
    analysts_texts = [
        intervenciones.get("ANALYST_ZONAS", ""),
        intervenciones.get("ANALYST_HUMAN", ""),
        intervenciones.get("ANALYST_V19", ""),
    ]
    analyst_combined = " ".join(analysts_texts)

    if not critic_text or not analyst_combined:
        return 0.0

    # Extraer palabras significativas
    def get_key_words(text: str) -> set:
        text = text.lower()
        stop_words = {
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "y",
            "o",
            "pero",
            "que",
            "es",
            "son",
            "está",
            "están",
            "por",
            "para",
            "con",
            "sin",
            "sobre",
            "tras",
            "durante",
            "mediante",
            "the",
            "a",
            "an",
            "and",
            "of",
            "to",
            "in",
            "for",
            "on",
            "with",
            "by",
            "at",
            "from",
            "this",
            "that",
            "these",
            "those",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "del",
            "una",
            "unas",
            "unos",
            "ante",
            "bajo",
            "cabe",
            "contra",
            "entre",
        }
        words = set()
        for word in text.split():
            word = word.strip(".,!?;:()[]{}\"'")
            if len(word) > 2 and word not in stop_words and not word.isdigit():
                words.add(word)
        return words

    critic_words = get_key_words(critic_text)
    analyst_words = get_key_words(analyst_combined)

    if not critic_words and not analyst_words:
        return 0.0

    # Intersección / unión (Jaccard)
    interseccion = len(critic_words & analyst_words)
    union = len(critic_words | analyst_words)

    similitud = interseccion / union if union > 0 else 0
    contradiccion = (1 - similitud) * 100

    # Penalizar si los textos son muy cortos
    if len(critic_text) < 200 or len(analyst_combined) < 400:
        contradiccion = max(contradiccion, 25)

    # Bonus: si el OPTIMIZER declaró debate inválido, forzar contradicción baja
    optimizer_text = intervenciones.get("OPTIMIZER", "")
    if "INVÁLIDO" in optimizer_text.upper() or "CONSENSO SUSPECHOSO" in optimizer_text.upper():
        contradiccion = min(contradiccion, 15)

    return round(min(contradiccion, 100), 2)


def calcular_contradiccion_por_pares(intervenciones: dict) -> dict:
    """
    Calcula contradicción entre CRITIC y cada ANALYST individualmente.
    Útil para debugging y métricas finas.

    Returns:
        dict: {
            'contra_zona': float,
            'contra_humano': float,
            'contra_v19': float,
            'promedio': float
        }
    """
    critic_text = intervenciones.get("CRITIC", "")

    def get_words(text: str) -> set:
        text = text.lower()
        stop_words = {
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "y",
            "o",
            "pero",
            "que",
            "es",
            "son",
            "con",
            "sin",
            "por",
            "para",
        }
        words = set()
        for word in text.split():
            word = word.strip(".,!?;:()[]{}\"'")
            if len(word) > 2 and word not in stop_words:
                words.add(word)
        return words

    critic_words = get_words(critic_text)

    zonas_text = intervenciones.get("ANALYST_ZONAS", "")
    humano_text = intervenciones.get("ANALYST_HUMAN", "")
    v19_text = intervenciones.get("ANALYST_V19", "")

    def calc(analyst_text: str) -> float:
        if not critic_text or not analyst_text:
            return 50.0
        analyst_words = get_words(analyst_text)
        if not critic_words or not analyst_words:
            return 50.0
        interseccion = len(critic_words & analyst_words)
        union = len(critic_words | analyst_words)
        similitud = interseccion / union if union > 0 else 0
        return (1 - similitud) * 100

    contra_zona = calc(zonas_text)
    contra_humano = calc(humano_text)
    contra_v19 = calc(v19_text)
    promedio = (contra_zona + contra_humano + contra_v19) / 3

    return {
        "contra_gemini_cuantico": round(contra_zona, 2),
        "contra_viejo_lobo": round(contra_humano, 2),
        "contra_estadistico": round(contra_v19, 2),
        "promedio": round(promedio, 2),
    }


def calcular_acuerdo_real(prediccion: dict, resultado: dict) -> float:
    """
    Acuerdo = (aciertos_principales + acierto_plus) / 6 * 100
    NUNCA supera 100% (esto corrige el bug de 10000%)

    Args:
        prediccion: dict con 'n1'..'n5' y 'plus'
        resultado: dict con 'n1'..'n5' y 'plus'

    Returns:
        float: 0-100% de acuerdo (porcentaje de acierto)
    """

    def get_numbers(pred):
        if "n1" in pred:
            return [pred["n1"], pred["n2"], pred["n3"], pred["n4"], pred["n5"]]
        for k in ["principales", "numeros", "numbers"]:
            if k in pred:
                return pred[k][:5]
        return []

    try:
        principales_pred = get_numbers(prediccion)
        principales_real = get_numbers(resultado)

        plus_pred = prediccion.get("plus") or prediccion.get("Plus") or 0
        plus_real = resultado.get("plus") or resultado.get("Plus") or 0

        aciertos_principales = len(set(principales_pred) & set(principales_real))
        acierto_plus = 1 if plus_pred == plus_real else 0

        acuerdo = ((aciertos_principales + acierto_plus) / 6) * 100
        return round(acuerdo, 2)
    except Exception:
        return 0.0


def calcular_u_score(
    prediccion: dict, resultado: dict = None, confianza_declarada: float = None
) -> float:
    """
    U-Score varía según resultado real + confianza calibrada.
    NUNCA es fijo (esto corrige el bug de U-Score=73 siempre)

    Args:
        prediccion: dict con predicción
        resultado: dict con resultado real (si None, U-Score tentativo)
        confianza_declarada: confianza que declararon los agentes (0-100)

    Returns:
        float: U-Score 0-100
    """
    if resultado is None:
        if confianza_declarada is not None:
            return round(confianza_declarada, 2)
        return 50.0

    acuerdo = calcular_acuerdo_real(prediccion, resultado)

    if confianza_declarada is not None:
        error_calibracion = abs(confianza_declarada - acuerdo)
        calibracion = max(0, 100 - error_calibracion)
        u_score = (acuerdo * 0.7) + (calibracion * 0.3)
    else:
        u_score = acuerdo

    return round(u_score, 2)


def validar_consenso(intervenciones: dict, contradiccion_minima: float = 20.0) -> dict:
    """
    Valida si el debate tiene consenso válido para avanzar al siguiente sorteo.
    Versión para 5 agentes.

    Returns:
        dict: {
            'es_valido': bool,
            'contradiccion': float,
            'contradiccion_por_agente': dict,
            'razon': str
        }
    """
    contradiccion = calcular_contradiccion_real(intervenciones)
    contradiccion_por_agente = calcular_contradiccion_por_pares(intervenciones)

    # Verificar si el OPTIMIZER declaró debate inválido
    optimizer_text = intervenciones.get("OPTIMIZER", "")
    optimizer_invalido = (
        "INVÁLIDO" in optimizer_text.upper() or "CONSENSO SUSPECHOSO" in optimizer_text.upper()
    )

    if optimizer_invalido:
        return {
            "es_valido": False,
            "contradiccion": contradiccion,
            "contradiccion_por_agente": contradiccion_por_agente,
            "razon": f"OPTIMIZER declaró debate inválido. Contradicción: {contradiccion}%",
        }

    if contradiccion < contradiccion_minima:
        return {
            "es_valido": False,
            "contradiccion": contradiccion,
            "contradiccion_por_agente": contradiccion_por_agente,
            "razon": f"Contradicción insuficiente ({contradiccion}% < {contradiccion_minima}%). Debate inválido.",
        }

    return {
        "es_valido": True,
        "contradiccion": contradiccion,
        "contradiccion_por_agente": contradiccion_por_agente,
        "razon": f"Contradicción suficiente ({contradiccion}% >= {contradiccion_minima}%). Se puede avanzar.",
    }
