from Implementacion.Iterator.IIterador import IIterador


class IteradorEncuesta(IIterador):
    def __init__(self, elem, filtros):
        self.indexActual = 0

        self.elementos = elem
        self.filtros = filtros

    def primero(self):
        self.indexActual = 0

    def siguiente(self):
        self.indexActual += 1

    def actual(self):
        if self.cumpleFiltro():
            return self.elementos[self.indexActual]
        return None

    def haTerminado(self):
        if self.indexActual >= len(self.elementos):
            return True
        return False

    def cumpleFiltro(self):
        return True


def testIterador():
    from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada

    llamadasDb, encuestasDb = PersistenciaLlamada().materializar()

    iterador = IteradorEncuesta(encuestasDb, None)
    iterador.primero()
    while not iterador.haTerminado():
        print(iterador.actual())
        iterador.siguiente()


if __name__ == "__main__":
    testIterador()
    