"""Script para cargar agentes JSON manualmente antes de iniciar el sistema."""

import json
import sys
from pathlib import Path

# Agregar IA_CORE al path
sys.path.insert(0, str(Path(__file__).parent))

from memory.manager import MemoryManager
from tools.manager import ToolManager
from providers.registry import ProviderRegistry
from agents.runtime_json_agent import RuntimeJsonAgent


def cargar_agentes_json():
    """Carga todos los agentes JSON del directorio config."""
    
    print("=" * 60)
    print("CARGANDO AGENTES JSON")
    print("=" * 60)
    
    # Inicializar gestores
    memory = MemoryManager()
    memory.start()
    
    tools = ToolManager()
    tools.start()
    
    providers = ProviderRegistry()
    providers.load_builtin_providers()
    
    # Directorio de configuraciones
    config_dir = Path("domains/loteria/agents/config")
    
    if not config_dir.exists():
        print(f"❌ Directorio no encontrado: {config_dir}")
        return []
    
    agentes_cargados = []
    
    for json_file in config_dir.glob("*.json"):
        if json_file.name.endswith(".bak"):
            continue
            
        print(f"\n📄 Procesando: {json_file.name}")
        
        try:
            with open(json_file, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            
            # Obtener ID del agente
            agent_id = data.get("id") or data.get("agent_id")
            if not agent_id:
                print(f"   ❌ Sin ID en {json_file.name}")
                continue
            
            # Obtener provider
            provider_name = data.get("provider")
            if not provider_name and "llm_config" in data:
                provider_name = data["llm_config"].get("provider")
            provider_name = provider_name or "nvidia"
            
            # Obtener LLM provider
            llm = providers.get(provider_name)
            if not llm:
                print(f"   ⚠️ Provider '{provider_name}' no disponible")
                llm = providers.get("nvidia")
            
            # Crear agente
            agent = RuntimeJsonAgent(
                json_path=json_file,
                memory=memory,
                tools=tools,
                llm_provider=llm,
            )
            
            print(f"   ✅ Cargado: {agent.id}")
            print(f"      Role: {agent.role}")
            print(f"      Provider: {agent.provider_name}")
            print(f"      Model: {agent.model_name}")
            
            agentes_cargados.append(agent)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL AGENTES CARGADOS: {len(agentes_cargados)}")
    print("=" * 60)
    
    return agentes_cargados


if __name__ == "__main__":
    cargar_agentes_json()