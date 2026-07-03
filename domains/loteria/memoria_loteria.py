"""Adaptador de la memoria genérica para el dominio Lotería."""

from typing import Optional

from core.memoria_perpetua import (
    MemoriaVectorial,
    actualizar_memoria as actualizar_memoria_generica,
    cargar_memoria_al_prompt as cargar_memoria_al_prompt_generica,
    cargar_memoria_completa_para_entrenamiento as cargar_memoria_completa_generica,
    obtener_memoria_para_paper as obtener_memoria_para_paper_generica,
    sincronizar_memoria_vectorial as sincronizar_memoria_vectorial_generica,
)


def _metadata_sorteo(sorteo: Optional[int]) -> Optional[dict]:
    """Traduce el concepto de sorteo a metadata comprendida por el Core."""
    return {"sorteo": sorteo} if sorteo is not None else None


class MemoriaVectorialLoteria:
    """Expone la API histórica de Lotería sobre ``MemoriaVectorial``."""

    def __init__(self, agente_id: str):
        self._memoria = MemoriaVectorial(agente_id)

    def __getattr__(self, nombre: str):
        return getattr(self._memoria, nombre)

    def agregar_documento(
        self, texto: str, fuente: str = "conocimiento_base", sorteo: Optional[int] = None
    ) -> int:
        return self._memoria.agregar_documento(
            texto,
            fuente=fuente,
            metadata_filtro=_metadata_sorteo(sorteo),
        )

    def buscar(
        self, consulta: str, top_k: int = 5, sorteo_actual: Optional[int] = None
    ) -> list[dict]:
        return self._memoria.buscar(
            consulta,
            top_k=top_k,
            metadata_filtro=_metadata_sorteo(sorteo_actual),
        )


def actualizar_memoria(
    agente_id: str,
    nueva_info: str,
    tipo: str = "general",
    sorteo: Optional[int] = None,
):
    return actualizar_memoria_generica(
        agente_id,
        nueva_info,
        tipo=tipo,
        metadata_filtro=_metadata_sorteo(sorteo),
    )


def cargar_memoria_al_prompt(
    agente_id: str,
    consulta_actual: str = "",
    sorteo_actual: Optional[int] = None,
) -> str:
    return cargar_memoria_al_prompt_generica(
        agente_id,
        consulta_actual=consulta_actual,
        metadata_filtro=_metadata_sorteo(sorteo_actual),
    )


def cargar_memoria_completa_para_entrenamiento(
    agente_id: str, sorteo_actual: Optional[int] = None
) -> str:
    return cargar_memoria_completa_generica(
        agente_id,
        metadata_filtro=_metadata_sorteo(sorteo_actual),
    )


def sincronizar_memoria_vectorial(
    agente_id: str,
    texto_base: Optional[str] = None,
    sorteo_limite: Optional[int] = None,
):
    return sincronizar_memoria_vectorial_generica(
        agente_id,
        texto_base=texto_base,
        metadata_filtro=_metadata_sorteo(sorteo_limite),
    )


def obtener_memoria_para_paper(
    agente_id: str, sorteo_actual: Optional[int] = None
) -> str:
    return obtener_memoria_para_paper_generica(
        agente_id,
        metadata_filtro=_metadata_sorteo(sorteo_actual),
    )
