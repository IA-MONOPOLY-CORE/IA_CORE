"""Configuración específica del dominio Lotería/S.A.A.O.P."""

# Agentes que participan en debate (IDs exactos de los JSONs)
DEBATE_AGENTS: list[str] = [
    "gpt_auditor",
    "gemini_cuantico",
    "viejo_lobo_rey",
    "estadistico_integral",
    "viejo_deepseek",
    "nuevo_deepseek_saaop",
]

# Tarea por defecto para debates
DEFAULT_DEBATE_TASK: str = (
    "OBJETIVO TÁCTICO: Evaluar la matriz combinatoria bajo las directrices del búnker.\n\n"
    "PARÁMETROS:\n"
    "- Régimen activo: CAZADOR (zonas bajas Z1-Z4)\n"
    "- Regla V19: 3 números bajos, 2 medios, 1 alto. Suma 110-140\n"
    "- Excluir patrones simétricos, secuenciales o de calendario\n"
    "- Evaluar zonas Z8/Z9 (40-45) para mitigar licuación humana\n"
    "- Garantía matemática defensiva '4 si 5'\n"
    "- Bloquear sobreajuste > 22.1% (azar estructural baseline)"
)

# Límites del sistema de validación
TRAINING_END: int = 3799
BLIND_TEST_START: int = 3800
BLIND_TEST_END: int = 3850
LIVE_TEST_START: int = 3851
LIVE_TEST_END: int = 3885

# Mapeo de roles genéricos a IDs de agentes específicos de S.A.A.O.P.
BUNKER_EXPERT_MAPPING = {
    "critic": "gpt_auditor",  # 1. CRITIC - destruye primero
    "analyst_zones": "gemini_cuantico",  # 2. ANALYST_ZONAS - densidad energética
    "analyst_human": "viejo_lobo_rey",  # 3. ANALYST_HUMAN - cirugía de ruptura
    "analyst": "estadistico_integral",  # 4. ANALYST_V19 - defiende e integra
    "optimizer": "viejo_deepseek",  # 5. OPTIMIZER - árbitro final
    "orchestrator": "nuevo_deepseek_saaop",  # 6. ORCHESTRATOR - cierre metodológico
}

# Alias para compatibilidad con api.py
VALIDATION_AGENTS = DEBATE_AGENTS

# Pipeline de debate específico de S.A.A.O.P. (6 agentes)
DEBATE_PIPELINE_6_AGENTS: list[tuple[str, str]] = [
    ("critic", "initial"),  # 1. GPT Auditor
    ("analyst_zones", "initial"),  # 2. Gemini Cuántico
    ("analyst_human", "initial"),  # 3. Viejo Lobo
    ("analyst", "initial"),  # 4. Estadístico Integral
    ("optimizer", "refine"),  # 5. Viejo DeepSeek
    ("orchestrator", "close"),  # 6. Nuevo DeepSeek - cierra el debate
]

# ============================================================
# CONSTANTES DEL U-SCORE v2.1 (SCORING)
# ============================================================
# IPN (Índice de Popularidad Negativo)
IPN_RAW_MIN: float = 0.75
IPN_RAW_MAX: float = 28.5
IPN_WEIGHT: float = 30.0

# PP (Patrones Penalisados)
PP_RAW_MAX: float = 25.0
PP_WEIGHT: float = 20.0

# PZ (Peso Zonal)
PZ_RAW_MIN: float = 4.0
PZ_RAW_MAX: float = 18.0
PZ_WEIGHT: float = 20.0

# DSI (Distancia Suma Ideal)
DSI_SUM_IDEAL: int = 130
DSI_RAW_MAX: float = 15.0
DSI_WEIGHT: float = 10.0

# CD (Coeficiente de Desviación)
CD_RAW_MAX: float = 10.0
CD_STD_MAX: float = 15.0  # Para normalizar la desviación
CD_WEIGHT: float = 10.0

# SD (Saturación por Decena)
SD_WEIGHT: float = 10.0

# Pesos totales (normalizados a 100)
U_SCORE_WEIGHTS: dict[str, float] = {
    "ipn": IPN_WEIGHT,
    "pp": PP_WEIGHT,
    "pz": PZ_WEIGHT,
    "dsi": DSI_WEIGHT,
    "cd": CD_WEIGHT,
    "sd": SD_WEIGHT,
}
