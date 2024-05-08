from abc import ABC, abstractmethod


class IAgregado(ABC):
    @abstractmethod
    def crearIterador(self, elementos, filtros):
        pass
