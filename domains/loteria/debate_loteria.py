"""Funciones específicas de debate para el dominio Lotería/S.A.A.O.P."""


def get_loteria_contradiction_patterns() -> list[tuple[tuple[str, ...], tuple[str, ...]]]:
    """
    Retorna patrones de contradicción específicos del dominio Lotería.
    Estos patrones detectan conflictos entre estrategias de zonas (CAZADOR/ESPEJO/PUENTE).
    """
    return [
        (("cazador", "números bajos", "0-15", "zona baja"), 
         ("espejo", "números altos", "31-45", "zona alta")),
        (("puente", "zona media", "16-30"), 
         ("cazador", "espejo", "extremos")),
    ]
