"""Contrato común para componentes del sistema."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseManager(ABC):
    """Ciclo de vida compartido: start al arrancar, stop al apagar."""

    @abstractmethod
    def start(self) -> None:
        """Prepara el componente para usarse."""

    @abstractmethod
    def stop(self) -> None:
        """Libera recursos de forma ordenada."""
