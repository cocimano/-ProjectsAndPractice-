from Implementacion.Entities.RespuestaPosible import RespuestaPosible, GeneradoRrespuestasPosibles
from Implementacion.Persistencia.ConexionDb import ConexionDb


class PersistenciaRespuestaPosible:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM RespuestaPosible;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        respuestasPosibles = []
        while row:
            respuestasPosibles.append(RespuestaPosible(row.descripcion, row.valor))
            row = cursor.fetchone()
        return respuestasPosibles

    def desmaterializar(self, objetos, idPregunta):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO RespuestaPosible (descripcion, valor, idPregunta) VALUES (?, ?, ?);'
        for respuestaPosible in objetos:
            cursor.execute(insertQuery, respuestaPosible.getDescripcionRta(), respuestaPosible.getValorRta(), idPregunta)
            cursor.commit()

    def materializarPorIdPregunta(self, idPregunta):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM RespuestaPosible WHERE idPregunta = ?;'
        cursor.execute(selectQuery, idPregunta)
        row = cursor.fetchone()
        respuestasPosibles = []
        respuestasPosiblesConIds = {}
        while row:
            respuestaPosible = RespuestaPosible(row.descripcion, row.valor)
            respuestasPosibles.append(respuestaPosible)
            respuestasPosiblesConIds[row.idRespuestaPosible] = respuestaPosible
            row = cursor.fetchone()
        return respuestasPosibles, respuestasPosiblesConIds

    def materializarPorId(self, idRespuestaPosible):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM RespuestaPosible WHERE idRespuestaPosible = ?;'
        cursor.execute(selectQuery, idRespuestaPosible)
        row = cursor.fetchone()
        if row:
            row.idPregunta
            return RespuestaPosible(row.descripcion, row.valor)
        else:
            return None

    def obtenerIdPorDescripcionValorIdPregunta(self, descripcion, valor, idPregunta):
        cursor = ConexionDb().getCursor()
        selectQuery = """
        SELECT idRespuestaPosible 
        FROM RespuestaPosible
        WHERE descripcion = ? AND valor = ? AND idPregunta = ?;"""
        cursor.execute(selectQuery, descripcion, valor, idPregunta)
        row = cursor.fetchone()
        if row:
            return row.idRespuestaPosible
        else:
            return None


    def deleteAll(self):
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM RespuestaPosible;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('RespuestaPosible', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaRespuestaPosible = PersistenciaRespuestaPosible()
    respuestasPosibles = persistenciaRespuestaPosible.materializar()
    for respuestaPosible in respuestasPosibles:
        print(respuestaPosible)


def testDesmaterializar():
    persistenciaRespuestaPosible = PersistenciaRespuestaPosible()
    # respuestasPosibles = [RespuestaPosible('test1', '1'),
    #                       RespuestaPosible('test2', '2')]
    respuestas1Al10 = GeneradoRrespuestasPosibles().generarRespuestas1Al10()
    respuestasSiNo = GeneradoRrespuestasPosibles().generarRespuestasSiNo()
    respuestasPosibles = respuestas1Al10 + respuestasSiNo

    persistenciaRespuestaPosible.desmaterializar(respuestasPosibles, 1)


def testDeleteAll():
    persistenciaRespuestaPosible = PersistenciaRespuestaPosible()
    persistenciaRespuestaPosible.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    testDesmaterializar()
    # testDeleteAll()
