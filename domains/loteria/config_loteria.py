"""Configuración específica del dominio Lotería/S.A.A.O.P."""

# Agentes que participan en debate (IDs exactos de los JSONs)
DEBATE_AGENTS: list[str] = [
    "gpt_auditor",
    "gemini_cuantico",
    "viejo_lobo_rey",
    "estadistico_integral",
    "viejo_deepseek",
    "nuevo_deepseek_saaop"
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
    "critic": "gpt_auditor",                 # 1. CRITIC - destruye primero
    "analyst_zones": "gemini_cuantico",      # 2. ANALYST_ZONAS - densidad energética
    "analyst_human": "viejo_lobo_rey",       # 3. ANALYST_HUMAN - cirugía de ruptura
    "analyst": "estadistico_integral",       # 4. ANALYST_V19 - defiende e integra
    "optimizer": "viejo_deepseek",           # 5. OPTIMIZER - árbitro final
    "orchestrator": "nuevo_deepseek_saaop"   # 6. ORCHESTRATOR - cierre metodológico
}

# Alias para compatibilidad con api.py
VALIDATION_AGENTS = DEBATE_AGENTS
