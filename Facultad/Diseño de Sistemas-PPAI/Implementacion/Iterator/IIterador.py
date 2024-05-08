from abc import ABC, abstractmethod


class IIterador(ABC):
    @abstractmethod
    def primero(self):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def actual(self):
        pass

    @abstractmethod
    def haTerminado(self):
        pass

    @abstractmethod
    def cumpleFiltro(self):
        pass
