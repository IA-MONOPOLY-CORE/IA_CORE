#!/usr/bin/env python3
"""Script para probar el motor de debate cuántico desde consola."""

import asyncio
import logging
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from core.orchestration import ExecutionMode
from supervisor import Supervisor

# Configurar logging para ver todo en consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Reducir logs ruidosos de librerías externas (opcional)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


async def main():
    """Punto de entrada asíncrono."""
    
    # Tarea de prueba (cambiala por lo que quieras analizar)
    task = """
    Analizá el siguiente patrón de números y determiná si hay una tendencia:
    [12, 14, 16, 18, 20, 22]
    
    Respondé con los números clave, tus cálculos y la conclusión final.
    """
    
    # Inicializar el supervisor
    supervisor = Supervisor()
    supervisor.start()
    
    try:
        print("\n" + "="*60)
        print("🚀 INICIANDO DEBATE CUÁNTICO S.A.A.O.P.")
        print("="*60 + "\n")
        
        # Ejecutar el debate
        result = await supervisor.orchestrate_async(
            task=task,
            mode=ExecutionMode.DEBATE
        )
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("📊 RESULTADOS DEL DEBATE")
        print("="*60)
        print(f"✅ Éxito: {result.success}")
        print(f"⏱️  Duración total: {result.duration_ms:.0f}ms")
        print(f"🤖 Agentes participantes: {result.agents}")
        print(f"📈 Cantidad de pasos: {len(result.steps)}")
        
        if hasattr(result, 'debate') and result.debate:
            print(f"🎯 Acuerdo: {result.debate.agreement_score}%")
            print(f"🔥 Contradicciones: {result.debate.contradiction_score}%")
            print("\n" + "─"*60)
            print("💬 RESPUESTA FINAL SINTETIZADA:")
            print("─"*60)
            print(result.debate.final_response)
        
        print("\n" + "="*60)
        print("✅ DEBATE COMPLETADO")
        print("="*60)
        
    except Exception as e:
        logging.error(f"❌ Error durante la ejecución: {e}", exc_info=True)
    finally:
        supervisor.stop()


if __name__ == "__main__":
    asyncio.run(main())