from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import config

from agents.base import Agent

logger = logging.getLogger(__name__)


class RuntimeJsonAgent(Agent):
    """
    Agente dinámico doctrinal S.A.A.O.P.
    Carga identidad, reglas y personalidad desde JSON.
    La IDENTIDAD PRINCIPAL viene del PAPER (mutable).
    El JSON solo contiene configuración técnica (provider, modelo, etc.)
    """

    def __init__(
        self,
        memory,
        tools=None,
        llm_provider=None,
        json_path: str | Path | None = None,
    ) -> None:
        super().__init__(
            memory=memory,
            tools=tools,
            llm_provider=llm_provider,
        )

        self.json_path = Path(json_path)

        # Leer JSON con manejo de BOM (solo configuración técnica)
        with open(self.json_path, "r", encoding="utf-8-sig") as f:
            self.profile = json.load(f)

        self.id = self.profile.get("id", self.json_path.stem)
        self.role = self.profile.get("role", "specialist")
        self.temperature = self.profile.get("temperature", 0.7)
        self.provider_name = self.profile.get("provider", "nvidia")
        self.model_name = self.profile.get("model", "meta/llama-4-maverick-17b-128e-instruct")
        self.instructions = self.profile.get("instructions", [])

        # ========== IDENTIDAD PRINCIPAL: PAPER (mutable) ==========
        self.paper = None
        self.system_prompt = self._cargar_identidad_desde_paper()

        # Si no hay paper, usar system_prompt del JSON como fallback
        if not self.system_prompt:
            self.system_prompt = self.profile.get("system_prompt", "")
            logger.warning(
                f"⚠️ {self.id}: No se encontró paper, usando system_prompt del JSON como fallback"
            )

        # Inicializar memoria vectorial para este agente (carga diferida)
        self._memoria_vectorial = None

    def _cargar_identidad_desde_paper(self) -> str:
        """
        Carga la identidad del agente desde su paper.
        El paper es la fuente de verdad de la personalidad del agente.
        """
        paper_path = config.AGENTS_PAPERS_DIR / f"{self.id}_paper.json"

        if not paper_path.exists():
            logger.warning(f"⚠️ Paper no encontrado para {self.id} en {paper_path}")
            return ""

        try:
            with open(paper_path, "r", encoding="utf-8") as f:
                self.paper = json.load(f)

            # Construir system_prompt desde el paper
            identidad = self.paper.get("identidad", "")
            reglas = self.paper.get("reglas_clave", [])
            lecciones = self.paper.get("lecciones_aprendidas", [])
            errores = self.paper.get("errores_a_evitar", [])
            estilo = self.paper.get("estilo_respuesta", "Técnico, directo")

            prompt_parts = []

            if identidad:
                prompt_parts.append(identidad)

            if reglas:
                prompt_parts.append("\n📋 MIS REGLAS CLAVE:")
                for r in reglas[:5]:
                    prompt_parts.append(f"  - {r}")

            if lecciones:
                prompt_parts.append("\n💡 LECCIONES APRENDIDAS:")
                for l in lecciones[:3]:
                    prompt_parts.append(f"  - {l}")

            if errores:
                prompt_parts.append("\n❌ ERRORES A EVITAR:")
                for e in errores[:3]:
                    prompt_parts.append(f"  - {e}")

            if estilo:
                prompt_parts.append(f"\n🎯 ESTILO DE RESPUESTA: {estilo}")

            prompt_parts.append(
                "\n⚠️ IMPORTANTE: Esta identidad es MUTABLE. Aprendo de mis experiencias. Si el contexto actual contradice alguna de mis reglas, priman los datos actuales."
            )

            result = "\n".join(prompt_parts)
            logger.info(f"✅ {self.id}: Identidad cargada desde paper ({len(result)} caracteres)")
            return result

        except Exception as e:
            logger.error(f"❌ Error cargando paper para {self.id}: {e}")
            return ""

    def _get_memoria_vectorial(self):
        """Carga diferida de la memoria vectorial para evitar dependencias circulares."""
        if self._memoria_vectorial is None:
            try:
                from domains.loteria.memoria_loteria import MemoriaVectorialLoteria

                self._memoria_vectorial = MemoriaVectorialLoteria(self.id)
            except ImportError as e:
                logger.warning(f"No se pudo cargar memoria vectorial para {self.id}: {e}")
                self._memoria_vectorial = False
        return self._memoria_vectorial if self._memoria_vectorial is not False else None

    def _cargar_lecciones_aprendidas(self, sorteo_actual: int = None) -> str:
        """Carga las lecciones aprendidas del agente desde su memoria.json."""
        try:
            from core.memoria_perpetua import cargar_memoria

            memoria = cargar_memoria(self.id)
            patrones = memoria.get("patrones_aprendidos", [])
            errores = memoria.get("errores_cometidos", [])
            aciertos = memoria.get("aciertos_historicos", [])

            if not patrones and not errores and not aciertos:
                return ""

            texto = "\n[📚 MIS LECCIONES APRENDIDAS HASTA AHORA]\n"

            if patrones:
                texto += "\n✅ PATRONES QUE ME FUNCIONARON:\n"
                for p in patrones[-5:]:
                    if isinstance(p, dict):
                        texto += f"   - {p.get('patron', p)[:200]}\n"
                    else:
                        texto += f"   - {p[:200]}\n"

            if errores:
                texto += "\n❌ ERRORES QUE NO DEBO REPETIR:\n"
                for e in errores[-5:]:
                    if isinstance(e, dict):
                        texto += f"   - {e.get('error', e)[:200]}\n"
                    else:
                        texto += f"   - {e[:200]}\n"

            if aciertos:
                texto += "\n🏆 ACIERTOS HISTÓRICOS:\n"
                for a in aciertos[-3:]:
                    if isinstance(a, dict):
                        texto += f"   - {a.get('acierto', a.get('descripcion', str(a)))[:200]}\n"
                    else:
                        texto += f"   - {a[:200]}\n"

            texto += "\n⚠️ IMPORTANTE: Estas lecciones son el resultado de mi experiencia. Deben guiar mis respuestas, pero no son dogmas. Si el contexto actual las contradice, priman los datos actuales.\n"
            return texto

        except Exception as e:
            logger.warning(f"Error cargando lecciones para {self.id}: {e}")
            return ""

    def build_prompt(
        self,
        task: str,
        custom_system_prompt: str | None = None,
        sorteo_actual: int = None,
        lecciones_externas: list[dict] | None = None,
    ) -> str:
        """
        Construye el prompt optimizado con:
        - System prompt del paper (identidad mutable)
        - Memoria base (resumida)
        - Búsqueda vectorial de fragmentos relevantes
        - Lecciones aprendidas del agente
        - Lecciones externas de otros agentes (si se proporcionan)
        """
        # Si se pasa custom_system_prompt, usarlo (para casos especiales)
        active_system_prompt = custom_system_prompt if custom_system_prompt else self.system_prompt

        # Memoria optimizada
        try:
            from domains.loteria.memoria_loteria import cargar_memoria_al_prompt

            memoria_texto = cargar_memoria_al_prompt(
                self.id,
                consulta_actual=task,
                sorteo_actual=sorteo_actual,
            )
        except Exception as e:
            logger.warning(f"Error cargando memoria para {self.id}: {e}")
            memoria_texto = "\n[Memoria temporalmente no disponible]\n"

        # Lecciones aprendidas
        lecciones_texto = self._cargar_lecciones_aprendidas(sorteo_actual)

        # Lecciones externas de otros agentes (debates anteriores)
        lecciones_externas_texto = ""
        if lecciones_externas:
            # Limitar a máximo 3 lecciones, inyectadas completas
            lecciones_externas_texto = "\n📚 LECCIONES DE DEBATES ANTERIORES (de otros agentes):\n"
            for leccion in lecciones_externas[:3]:
                contenido = leccion.get("leccion", "")
                lecciones_externas_texto += f"  - {contenido}\n"

        # Instrucciones del JSON
        instructions_text = (
            "\n" + "\n".join(f"- {item}" for item in self.instructions) if self.instructions else ""
        )

        # Prompt final
        return (
            f"{active_system_prompt}{instructions_text}\n\n"
            f"{memoria_texto}\n"
            f"{lecciones_texto}\n"
            f"{lecciones_externas_texto}\n\n"
            f"⚠️ INSTRUCCIONES IMPORTANTES:\n"
            f"- Responde de forma directa y técnica.\n"
            f"- No repitas estas instrucciones ni tu identidad en la respuesta.\n"
            f"- Si la información está en tu memoria, usala.\n"
            f"- Si no la encontrás, basate en tu conocimiento y razonamiento.\n"
            f"- Tu identidad es MUTABLE: aprendés de cada interacción.\n\n"
            f"🎯 TAREA ACTUAL:\n{task}"
        )

    def buscar_en_memoria(
        self, consulta: str, top_k: int = 5, sorteo_actual: int = None
    ) -> list[dict]:
        """Busca fragmentos relevantes en la memoria vectorial del agente."""
        mv = self._get_memoria_vectorial()
        if mv and hasattr(mv, "buscar"):
            try:
                return mv.buscar(
                    consulta,
                    top_k=top_k,
                    sorteo_actual=sorteo_actual,
                )
            except Exception as e:
                logger.warning(f"Error en búsqueda vectorial para {self.id}: {e}")
                return []
        return []

    def run(
        self,
        task: str,
        context: dict[str, Any] | None = None,
        system_prompt: str | None = None,
    ) -> Any:
        """Ejecuta el agente con la tarea dada."""
        sorteo_actual = None
        lecciones_externas = None
        if context:
            if "sorteo_actual" in context:
                sorteo_actual = context.get("sorteo_actual")
            if "lecciones_externas" in context:
                lecciones_externas = context.get("lecciones_externas")

        prompt = self.build_prompt(
            task,
            custom_system_prompt=system_prompt,
            sorteo_actual=sorteo_actual,
            lecciones_externas=lecciones_externas,
        )

        if not self.llm_provider:
            raise RuntimeError(
                f"Agente '{self.id}' sin proveedor LLM asignado. "
                f"Provider esperado: {self.provider_name}"
            )

        logger.info(
            f"RuntimeJsonAgent.run | agente={self.id} | "
            f"provider={self.provider_name} | model={self.model_name} | "
            f"prompt_len={len(prompt)}"
        )

        response = self.llm_provider.generate(
            prompt=prompt,
            model=self.model_name,
            temperature=self.temperature,
        )

        if hasattr(response, "text"):
            output_text = response.text
        elif isinstance(response, dict):
            output_text = response.get("output", str(response))
        else:
            output_text = str(response)

        # Actualizar memoria con aprendizaje
        try:
            from core.memoria_perpetua import cargar_memoria, guardar_memoria
            import datetime

            memoria = cargar_memoria(self.id)

            if "historial" not in memoria:
                memoria["historial"] = []

            registro = {
                "timestamp": datetime.datetime.now().isoformat(),
                "task": task[:200],
                "respuesta": output_text[:500],
                "longitud_respuesta": len(output_text),
                "prompt_len": len(prompt),
            }
            if sorteo_actual:
                registro["sorteo"] = sorteo_actual

            memoria["historial"].append(registro)

            if len(memoria["historial"]) > 50:
                memoria["historial"] = memoria["historial"][-50:]

            guardar_memoria(self.id, memoria)

        except Exception as e:
            logger.warning(f"Error guardando historial para {self.id}: {e}")

        return {
            "agent": self.id,
            "output": output_text,
            "llm": {
                "provider": self.provider_name,
                "model": self.model_name,
            },
        }
