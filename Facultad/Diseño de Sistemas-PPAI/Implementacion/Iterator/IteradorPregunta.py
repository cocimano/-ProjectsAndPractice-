from Implementacion.Iterator.IIterador import IIterador


class IteradorPregunta(IIterador):
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
    Se filtra segun si tiene respuesta posible
    El filtro debe ser una RespuestaPosible
    """
    def cumpleFiltro(self):
        preguntaActual = self.elementos[self.indexActual]
        return preguntaActual.tieneRespuestaPosible(self.filtros)


def testIterador():
    from Implementacion.Persistencia.PersistenciaLlamada import PersistenciaLlamada

    llamadasDb, encuestasDb = PersistenciaLlamada().materializar()

    iterador = IteradorPregunta(encuestasDb[0].getPreguntas(), None)
    iterador.primero()
    while not iterador.haTerminado():
        print(iterador.actual())
        iterador.siguiente()


if __name__ == "__main__":
    testIterador()
