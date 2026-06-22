"""Herramienta de ejemplo: devuelve el texto recibido."""

TOOL_NAME = "echo"


def execute(text: str = "", **kwargs) -> dict:
    return {"text": text, **kwargs}
