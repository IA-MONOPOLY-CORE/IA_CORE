"""Configuración global del proyecto."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Rutas base
ROOT_DIR = Path(__file__).resolve().parent

LOG_DIR = ROOT_DIR / "logs"

MEMORY_DIR = ROOT_DIR / "memory"

MEMORY_STATE_FILE = MEMORY_DIR / "state.json"

TOOLS_MODULES_DIR = ROOT_DIR / "tools" / "modules"

# =========================================================
# CONFIGURACIÓN DE AGENTES - CORREGIDA PARA JSON
# =========================================================
# Directorio donde están los archivos JSON de los agentes
AGENTS_CONFIG_DIR = ROOT_DIR / "agents" / "config"

# Directorio de módulos Python (para agentes personalizados, puede estar vacío)
AGENTS_MODULES_DIR = ROOT_DIR / "agents" / "modules"

# =========================================================
# NVIDIA API CONFIGURACIÓN (RÁPIDO)
# =========================================================
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"
NVIDIA_MAX_TOKENS = 1024
NVIDIA_TIMEOUT = 60.0

# Ollama (runtime local)
OLLAMA_BASE_URL = "http://localhost:11434"

OLLAMA_TIMEOUT = 180.0

OLLAMA_LIGHTWEIGHT_TIMEOUT = 120.0

OLLAMA_MAX_RETRIES = 2

OLLAMA_MAX_OUTPUT_TOKENS = 512

OLLAMA_MAX_PROMPT_CHARS = 2500

OLLAMA_NUM_PREDICT_LIGHTWEIGHT = 384

OLLAMA_NUM_PREDICT_CHAT = 96

OLLAMA_CHAT_NUM_CTX = 512

OLLAMA_PRELOAD_MODEL = True

OLLAMA_KEEP_ALIVE = "30m"

# Fast local chat (assistant only)
FAST_CHAT_ENABLED = True

FAST_CHAT_SYSTEM_PROMPT = (
    "You are OliverSystem assistant. Be practical, concise and helpful. "
    "Reply briefly unless the user asks for detail."
)

FAST_CHAT_MAX_TOKENS = 96

FAST_CHAT_TEMPERATURE = 0.6

FAST_CHAT_TOP_P = 0.9

FAST_CHAT_MAX_USER_CHARS = 400

FAST_CHAT_MAX_PROMPT_CHARS = 600

UI_STREAMING_CHAT = False

# Cola simple: una inferencia Ollama a la vez
OLLAMA_INFERENCE_QUEUE = True

# =========================================================
# HYBRID EXECUTION SYSTEM
# =========================================================

HYBRID_MODE = True

DEFAULT_EXECUTION_MODE = "HYBRID"

SAFE_MODE = True

DEFAULT_RESOURCE_POLICY = "balanced"

HYBRID_REGISTER_CLOUD_STUBS = True

SKIP_PROVIDER_HEALTH_ON_START = True

# UI performance
UI_CACHE_TTL = 60

UI_CACHE_TTL_SAFE = 300

UI_PROVIDER_HEALTH_TTL = 120

# Modelo local por defecto
LIGHTWEIGHT_MODEL = "phi3"

DEFAULT_LOCAL_MODEL = "phi3:mini"

OFFLINE_MODEL = "phi3:mini"

ONLINE_PRIORITY = [
    "nvidia",
    "claude",
    "deepseek",
    "openai",
    "groq",
    "gemini",
    "openrouter",
]

LOCAL_PRIORITY = [
    "phi3",
    "tinyllama",
    "qwen2:1.5b",
    "gemma:2b",
]

# Proveedores LLM por agente (para módulos Python, no afecta JSON)
AGENT_PROVIDERS: dict[str, str] = {
    "assistant": "ollama",
    "analyst": "nvidia",
    "critic": "nvidia",
    "optimizer": "nvidia",
    "echo": "ollama",
}

# Agente por defecto en UI
DEFAULT_UI_AGENT = "assistant"

PROVIDER_FALLBACK_CHAIN: list[str] = [
    "nvidia",
    "ollama",
    "openai",
    "claude",
]

# Orquestación y debate
ORCHESTRATION_TIMEOUT_S = 600.0

DEBATE_ROUND_TIMEOUT_S = 90.0

DEBATE_LIGHTWEIGHT = True

SEQUENTIAL_CONTINUE_ON_FAILURE = True

# Logging
LOG_LEVEL = "INFO"

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


# =========================================================
# NUEVAS VARIABLES EXTERNALIZADAS (PUNTO 5.2)
# =========================================================

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

# Umbrales de aprendizaje (usados en supervisor.py)
APRENDIZAJE_SCORE_MINIMO: float = 60.0    # Score mínimo para considerar acierto
HERRAMIENTA_SCORE_MINIMO: float = 70.0    # Score mínimo para extraer herramienta
CONTRADICCION_ACUERDO_MINIMO: float = 40.0  # Acuerdo mínimo para registrar contradicción resuelta
REGENERACION_PAPER_SCORE_MINIMO: float = 70.0  # Score mínimo para regenerar paper

# Límites del sistema de validación (movidos desde api.py)
TRAINING_END: int = 3799
BLIND_TEST_START: int = 3800
BLIND_TEST_END: int = 3850
LIVE_TEST_START: int = 3851
LIVE_TEST_END: int = 3885

# Rutas importantes compartidas
MEMORY_HERRAMIENTAS_COMPARTIDAS: Path = MEMORY_DIR / "herramientas_compartidas.json"
MEMORY_USER_SETTINGS: Path = MEMORY_DIR / "user_settings.json"
