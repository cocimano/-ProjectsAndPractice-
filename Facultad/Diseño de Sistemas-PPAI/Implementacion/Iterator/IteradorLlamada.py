from Implementacion.Iterator.IIterador import IIterador


class IteradorLlamada(IIterador):
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

    """
    Se filtra por periodo
    El elemento 0 de los filtros debe ser la fecha inicial
    El elemento 1 de los filtros debe ser la fecha final 
    """
    def cumpleFiltro(self):
        llamadaActual = self.elementos[self.indexActual]
        return llamadaActual.esDePeriodo(self.filtros[0], self.filtros[1]) and llamadaActual.getEncuestaEnviada()


def testIterador():
    from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada

    llamadasDb, encuestasDb = PersistenciaLlamada().materializar()

    iterador = IteradorLlamada(llamadasDb, None)
    iterador.primero()
    while not iterador.haTerminado():
        print(iterador.actual())
        iterador.siguiente()


if __name__ == "__main__":
    testIterador()
