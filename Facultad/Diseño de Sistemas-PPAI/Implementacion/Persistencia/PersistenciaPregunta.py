from Implementacion.Entities.Pregunta import Pregunta, GeneradorPreguntas
from Implementacion.Entities.RespuestaPosible import RespuestaPosible
from Implementacion.Persistencia.ConexionDb import ConexionDb
from Implementacion.Persistencia.PersistenciaRespuestaPosible import PersistenciaRespuestaPosible


class PersistenciaPregunta:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Pregunta;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        preguntas = []
        while row:
            respuestasPosibles = PersistenciaRespuestaPosible().materializarPorIdPregunta(row.idPregunta)
            preguntas.append(Pregunta(row.pregunta, respuestasPosibles))
            row = cursor.fetchone()
        return preguntas

    def desmaterializar(self, objetos, idEncuesta):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO Pregunta (pregunta, idEncuesta) VALUES (?, ?);'
        idsPreguntas = []
        for pregunta in objetos:
            cursor.execute(insertQuery, pregunta.pregunta, idEncuesta)
            cursor.commit()
            # Desmaterializar las respuestas de la pregunta
            getIdQuery = 'SELECT @@IDENTITY AS ID;'
            idPregunta = cursor.execute(getIdQuery).fetchval()
            PersistenciaRespuestaPosible().desmaterializar(pregunta.getRespuestasPosibles(), idPregunta)

            idsPreguntas.append(idPregunta)
        return idsPreguntas

    def materializarPorId(self, idPregunta, respuestasPosibles=[]):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Pregunta WHERE idPregunta = ?;'
        cursor.execute(selectQuery, idPregunta)
        row = cursor.fetchone()
        if row:
            if len(respuestasPosibles) == 0:
                respuestasPosibles = PersistenciaRespuestaPosible().materializarPorIdPregunta(row.idPregunta)
            return Pregunta(row.pregunta, respuestasPosibles)
        else:
            return None

    def materializarPorIdEncuesta(self, idEncuesta):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Pregunta WHERE idEncuesta = ?;'
        cursor.execute(selectQuery, idEncuesta)
        row = cursor.fetchone()
        preguntas = []
        respuestasPosiblesConIds = {}
        while row:
            respuestasPosibles, respuestasPosiblesConIdsActual = PersistenciaRespuestaPosible().materializarPorIdPregunta(row.idPregunta)
            pregunta = Pregunta(row.pregunta, respuestasPosibles)
            preguntas.append(pregunta)
            respuestasPosiblesConIds.update(respuestasPosiblesConIdsActual)
            row = cursor.fetchone()
        return preguntas, respuestasPosiblesConIds

    def getIdPorPregunta(self, pregunta):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT idPregunta FROM Pregunta WHERE pregunta = ?;'
        cursor.execute(selectQuery, pregunta)
        row = cursor.fetchone()
        if row:
            return row.idPregunta
        else:
            return None

    def deleteAll(self):
        # Borrar las respuestas posibles
        PersistenciaRespuestaPosible().deleteAll()
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM Pregunta;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('Pregunta', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaPregunta = PersistenciaPregunta()
    preguntas = persistenciaPregunta.materializar()
    for pregunta in preguntas:
        print(pregunta)


def testDesmaterializar():
    persistenciaPregunta = PersistenciaPregunta()
    # preguntas = [Pregunta('test4', [RespuestaPosible('desc1', 'val1'), RespuestaPosible('desc2', 'val2')]),
    #              Pregunta('test5', [RespuestaPosible('desc2', 'val2'), RespuestaPosible('desc3', 'val3')])]
    preguntas = GeneradorPreguntas().obtenerPreguntasAleatorias(2)
    persistenciaPregunta.desmaterializar(preguntas, 1)


def testMaterializarPorId():
    persistenciaPregunta = PersistenciaPregunta()
    pregunta = persistenciaPregunta.materializarPorId()
    print(pregunta)

def testDeleteAll():
    persistenciaPregunta = PersistenciaPregunta()
    persistenciaPregunta.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    # testDesmaterializar()
    # testMaterializarPorId()
    testDeleteAll()
