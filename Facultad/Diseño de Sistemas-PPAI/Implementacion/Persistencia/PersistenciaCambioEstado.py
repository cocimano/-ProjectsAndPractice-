from Implementacion.Entities.CambioEstado import CambioEstado, GeneradorCambiosEstado
from Implementacion.Persistencia.ConexionDb import ConexionDb
from Implementacion.Persistencia.PersistenciaEstado import PersistenciaEstado


class PersistenciaCambioEstado:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM CambioEstado;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        cambiosEstados = []
        while row:
            estado = PersistenciaEstado().materializarPorId(row.idEstado)
            cambiosEstados.append(CambioEstado(row.fechaHoraInicio, row.fechaHoraFin, estado))
            row = cursor.fetchone()
        return cambiosEstados

    def desmaterializar(self, objetos, idLlamada):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO CambioEstado (fechaHoraInicio, fechaHoraFin, idEstado, idLlamada) VALUES (?, ?, ?, ?);'
        for cambioEstado in objetos:
            # Verificar que exista el estado
            idEstado = PersistenciaEstado().getIdFromNombre(cambioEstado.getNombreEstado())
            if idEstado is None:
                idEstado = PersistenciaEstado().desmaterializar([cambioEstado.getEstado()])
            cursor.execute(insertQuery, cambioEstado.fechaHoraInicio, cambioEstado.fechaHoraFin, idEstado, idLlamada)
            cursor.commit()

    def materializarPorIdLlamada(self, idLlamada):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM CambioEstado WHERE idLlamada = ?;'
        cursor.execute(selectQuery, idLlamada)
        row = cursor.fetchone()
        cambiosEstados = []
        while row:
            estado = PersistenciaEstado().materializarPorId(row.idEstado)
            cambiosEstados.append(CambioEstado(row.fechaHoraInicio, row.fechaHoraFin, estado))
            row = cursor.fetchone()
        return cambiosEstados

    def deleteAll(self):
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM CambioEstado;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('CambioEstado', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaCambioEstado = PersistenciaCambioEstado()
    estados = persistenciaCambioEstado.materializar()
    for estado in estados:
        print(estado)


def testDesmaterializar():
    persistenciaCambioEstado = PersistenciaCambioEstado()
    cambiosEstado = GeneradorCambiosEstado().obtenerCambiosEstado()
    persistenciaCambioEstado.desmaterializar(cambiosEstado, 1)


def testDeleteAll():
    persistenciaCambioEstado = PersistenciaCambioEstado()
    persistenciaCambioEstado.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    testDesmaterializar()
    # testDeleteAll()
