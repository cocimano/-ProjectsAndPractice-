from Implementacion.Entities.RespuestaDeCliente import RespuestaDeCliente, GeneradorRespuestasDeCliente
from Implementacion.Persistencia.ConexionDb import ConexionDb
from Implementacion.Persistencia.PersistenciaRespuestaPosible import PersistenciaRespuestaPosible
from Implementacion.Persistencia.PersistenciaEncuesta import PersistenciaEncuesta

class PersistenciaRespuestaDeCliente:
    def materializar(self, respuestasSeleccionadas=None):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM RespuestaDeCliente;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        respuestasDeCliente = []
        while row:
            if respuestasSeleccionadas is None:
                # Obtener respuesta seleccionada a partir del id
                respuestasSeleccionadas = PersistenciaRespuestaPosible().materializarPorId(row.idRespuestaPosible)
            respuestasDeCliente.append(RespuestaDeCliente(row.fechaEncuesta, respuestasSeleccionadas))
            row = cursor.fetchone()
        return respuestasDeCliente

    def desmaterializar(self, objetos, idLlamada, idsPreguntas):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO RespuestaDeCliente (fechaEncuesta, idRespuestaPosible, idLlamada) VALUES (?, ?, ?);'
        for i in range(len(objetos)):
            respuestaDeCliente = objetos[i]
            idRespuestaPosible = PersistenciaRespuestaPosible().obtenerIdPorDescripcionValorIdPregunta(
                respuestaDeCliente.getDescripcionRespuestaSeleccionada(),
                respuestaDeCliente.getValorRespuestaSeleccionada(),
                idsPreguntas[i])
            cursor.execute(insertQuery, respuestaDeCliente.getFechaEncuesta(), idRespuestaPosible, idLlamada)
            cursor.commit()

    def materializarPorIdLlamada(self, idLlamada):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM RespuestaDeCliente WHERE idLlamada = ?;'
        cursor.execute(selectQuery, idLlamada)
        row = cursor.fetchone()
        respuestasDeCliente = []

        encuesta, respuestasPosiblesConIds = PersistenciaEncuesta().materializarEncuestaPorIdsRespuestasPosibles(
            self.getIdsPorIdLlamada(idLlamada))

        while row:
            # respuestaPosible = PersistenciaRespuestaPosible().materializarPorId(row.idRespuestaPosible)
            respuestaPosible = respuestasPosiblesConIds[row.idRespuestaPosible]
            respuestasDeCliente.append(RespuestaDeCliente(row.fechaEncuesta, respuestaPosible))
            row = cursor.fetchone()

        return respuestasDeCliente, encuesta

    def getIdsPorIdLlamada(self, idLlamada):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT r.idRespuestaPosible FROM RespuestaDeCliente r WHERE r.idLlamada = ?;'
        cursor.execute(selectQuery, idLlamada)
        row = cursor.fetchone()
        idsRespuestasPosibles = []
        while row:
            idsRespuestasPosibles.append(row.idRespuestaPosible)
            row = cursor.fetchone()
        return idsRespuestasPosibles

    def deleteAll(self):
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM RespuestaDeCliente;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('RespuestaDeCliente', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaRespuestaDeCliente = PersistenciaRespuestaDeCliente()
    respuestasDeCliente = persistenciaRespuestaDeCliente.materializar()
    for respuestaDeCliente in respuestasDeCliente:
        print(respuestaDeCliente)

def testMaterializarPorIdLlamada():
    persistenciaRespuestaDeCliente = PersistenciaRespuestaDeCliente()
    respuestasDeCliente = persistenciaRespuestaDeCliente.materializarPorIdLlamada(1)
    # for respuestaDeCliente in respuestasDeCliente:
    #     print(respuestaDeCliente)


def testDesmaterializar():
    persistenciaRespuestaDeCliente = PersistenciaRespuestaDeCliente()
    respuestasDeCliente = GeneradorRespuestasDeCliente().generarRtasCliente()
    persistenciaRespuestaDeCliente.desmaterializar(respuestasDeCliente, 1, 1)


def testDeleteAll():
    persistenciaRespuestaDeCliente = PersistenciaRespuestaDeCliente()
    persistenciaRespuestaDeCliente.deleteAll()


if __name__ == '__main__':
    # testMaterializar()
    # testDesmaterializar()
    testMaterializarPorIdLlamada()
    # testDeleteAll()
