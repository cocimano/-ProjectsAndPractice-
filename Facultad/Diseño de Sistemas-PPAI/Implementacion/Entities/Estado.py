import random


class Estado:
    def __init__(self, nombre):
        self.nombre = nombre

    # region Estados
    def esFinalizada(self):
        if self.nombre == 'Finalizada':
            return True
        return False

    def esIniciada(self):
        if self.nombre == 'Iniciada':
            return True
        return False

    def esEnCurso(self):
        if self.nombre == 'En Curso':
            return True
        return False

    def esCancelada(self):
        if self.nombre == 'Cancelada':
            return True
        return False

    # endregion

    def getNombre(self):
        return self.nombre

    def __str__(self):
        r = ''
        r += '{:<30}'.format("Nombre Estado: " + str(self.nombre))
        return r


class Generadorestados:
    def __init__(self):
        self.estadoIniciada = Estado('Iniciada')
        self.estadoEnCurso = Estado('En Curso')
        self.estadoFinalizada = Estado('Finalizada')
        self.estadoCancelada = Estado('Cancelada')

    # Método para obtener los Estados de la Llamada
    def obtenerEstados(self):
        arrayEstados = [self.estadoIniciada, self.estadoEnCurso, self.estadoFinalizada, self.estadoCancelada]
        return arrayEstados


def test():
    estados = Generadorestados().obtenerEstados()
    for estado in estados:
        print()
        print(estado)
        print("Get nombre:", estado.getNombre())
        print("Es finalizada:", estado.esFinalizada())
        print("Es iniciada:", estado.esIniciada())


if __name__ == "__main__":
    test()
