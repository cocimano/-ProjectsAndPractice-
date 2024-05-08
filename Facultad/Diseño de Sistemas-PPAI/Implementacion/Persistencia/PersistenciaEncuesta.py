from Implementacion.Entities.Encuesta import Encuesta, GeneradorEncuestas
from Implementacion.Persistencia.ConexionDb import ConexionDb
from Implementacion.Persistencia.PersistenciaPregunta import PersistenciaPregunta

from Implementacion.Utilidad import FechaYHora


class PersistenciaEncuesta:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Encuesta;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        encuestas = []
        while row:
            preguntas = PersistenciaPregunta().materializarPorIdEncuesta(row.idEncuesta)
            encuestas.append(Encuesta(row.descripcion, row.fechaFinVigencia, preguntas))
            row = cursor.fetchone()
        return encuestas

    def materializarPorId(self, idEncuesta):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Encuesta WHERE idEncuesta = ?;'
        cursor.execute(selectQuery, idEncuesta)
        row = cursor.fetchone()
        if row:
            preguntas, respuestasPosiblesConIds = PersistenciaPregunta().materializarPorIdEncuesta(row.idEncuesta)
            return Encuesta(row.descripcion, row.fechaFinVigencia, preguntas), respuestasPosiblesConIds
        else:
            return None

    # Materializar una encuesta a partir de los ids de las respuestas posibles de la encuesta
    def materializarEncuestaPorIdsRespuestasPosibles(self, idsRespuestasPosibles):
        cursor = ConexionDb().getCursor()
        selectQuery = ("""
        SELECT DISTINCT e.idEncuesta
        FROM RespuestaPosible r
        INNER JOIN Pregunta p ON r.idPregunta = p.idPregunta
        INNER JOIN Encuesta e ON p.idEncuesta = e.idEncuesta
        WHERE r.idRespuestaPosible IN ({seq});""".
                       format(seq=','.join(['?']*len(idsRespuestasPosibles))))
        cursor.execute(selectQuery, *idsRespuestasPosibles)
        row = cursor.fetchone()
        if row:
            encuesta, respuestasPosiblesConIds = self.materializarPorId(row.idEncuesta)
            return encuesta, respuestasPosiblesConIds
        else:
            return None

    def desmaterializarArray(self, objetos):
        for objeto in objetos:
            self.desmaterializarUna(objeto)

    def desmaterializarUna(self, objeto):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO Encuesta (descripcion, fechaFinVigencia) VALUES (?, ?);'
        cursor.execute(insertQuery, objeto.descripcion, objeto.fechaFinVigencia)
        cursor.commit()
        # Desmaterializar las preguntas de la encuesta
        getIdQuery = 'SELECT @@IDENTITY AS ID;'
        idEncuesta = cursor.execute(getIdQuery).fetchval()
        return PersistenciaPregunta().desmaterializar(objeto.getPreguntas(), idEncuesta)

    def deleteAll(self):
        # Borrar las preguntas
        PersistenciaPregunta().deleteAll()
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM Encuesta;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('Encuesta', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaEncuesta = PersistenciaEncuesta()
    encuestas = persistenciaEncuesta.materializar()
    for encuesta in encuestas:
        print(encuesta)


def testMaterializarPorId():
    persistenciaEncuesta = PersistenciaEncuesta()
    encuesta = persistenciaEncuesta.materializarPorId(1)
    print(encuesta)


def testDesmaterializar():
    persistenciaEncuesta = PersistenciaEncuesta()
    # encuestas = [Encuesta('test4', FechaYHora.obtenerFechaHoraRandom()),
    #              Encuesta('test5', FechaYHora.obtenerFechaHoraRandom())]
    encuestas = GeneradorEncuestas().generarEncuestasAleatorias(2)
    persistenciaEncuesta.desmaterializarArray(encuestas)


def testMaterializarEncuestaPorIdsRespuestasPosibles():
    persistenciaEncuesta = PersistenciaEncuesta()
    idsRespuestasPosibles = [1, 2, 3, 4]
    encuesta = persistenciaEncuesta.materializarEncuestaPorIdsRespuestasPosibles(idsRespuestasPosibles)
    print(encuesta)


def testDeleteAll():
    persistenciaEncuesta = PersistenciaEncuesta()
    persistenciaEncuesta.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    # testMaterializarPorId()
    testMaterializarEncuestaPorIdsRespuestasPosibles()
    # testDesmaterializar()
    # testDeleteAll()
