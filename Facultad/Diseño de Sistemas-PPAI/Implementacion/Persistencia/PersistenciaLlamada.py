from Implementacion.Entities.Llamada import Llamada, GeneradorLlamadas
from Implementacion.Persistencia.ConexionDb import ConexionDb
from Implementacion.Persistencia.PersistenciaCliente import PersistenciaCliente
from Implementacion.Persistencia.PersistenciaCambioEstado import PersistenciaCambioEstado
from Implementacion.Persistencia.PersistenciaRespuestaDeCliente import PersistenciaRespuestaDeCliente

from datetime import timedelta


class PersistenciaLlamada:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Llamada;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        llamadas = []
        encuestas = []
        while row:
            respuestasDeEncuesta, encuesta = PersistenciaRespuestaDeCliente().materializarPorIdLlamada(row.idLlamada)
            cambiosEstado = PersistenciaCambioEstado().materializarPorIdLlamada(row.idLlamada)
            cliente = PersistenciaCliente().materializarPorDni(row.dni)
            llamadas.append(Llamada(row.descripcionOperador, row.detalleAccionRequerida,
                                    row.encuestaEnviada, row.observacionAuditor,
                                    respuestasDeEncuesta=respuestasDeEncuesta, cambiosEstado=cambiosEstado,
                                    cliente=cliente, duracion=timedelta(seconds=row.duracion)))
            encuestas.append(encuesta)
            row = cursor.fetchone()
        return llamadas, encuestas

    def desmaterializarArray(self, objetos):
        for objeto in objetos:
            self.desmaterializarUna(objeto)

    def desmaterializarUna(self, objeto, idsPreguntas):
        cursor = ConexionDb().getCursor()
        insertQuery = """
        INSERT INTO Llamada (descripcionOperador, detalleAccionRequerida, duracion, encuestaEnviada, observacionAuditor, dni) 
        VALUES (?, ?, ?, ?, ?, ?);"""
        # Desmaterializar cliente
        cliente = PersistenciaCliente().materializarPorDni(objeto.getDniCliente())
        if cliente is None:
            PersistenciaCliente().desmaterializar([objeto.getCliente()])

        cursor.execute(insertQuery, objeto.descripcionOperador, objeto.detalleAccionRequerida,
                       objeto.duracion.total_seconds(), objeto.encuestaEnviada, objeto.observacionAuditor,
                       objeto.getDniCliente())
        cursor.commit()

        # Desmaterializar los cambios de estado de la llamada
        getIdQuery = 'SELECT @@IDENTITY AS ID;'
        idLlamada = cursor.execute(getIdQuery).fetchval()
        PersistenciaCambioEstado().desmaterializar(objeto.getCambiosEstado(), idLlamada)
        # Desmaterializar las respuestas de encuesta
        PersistenciaRespuestaDeCliente().desmaterializar(objeto.getRespuestas(), idLlamada, idsPreguntas)

        return idLlamada

    def deleteAll(self):
        # Borrar sus cambios de estado
        PersistenciaCambioEstado().deleteAll()
        # Borrar sus respuestas
        PersistenciaRespuestaDeCliente().deleteAll()
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM Llamada;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('Llamada', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaLlamada = PersistenciaLlamada()
    llamadas = persistenciaLlamada.materializar()
    for llamada in llamadas:
        print(llamada)


def testDesmaterializar():
    persistenciaLlamada = PersistenciaLlamada()
    llamadas = []
    for i in range(3):
        llamadas.append(GeneradorLlamadas().generarLlamadaRandom())
    persistenciaLlamada.desmaterializarArray(llamadas)


def testDeleteAll():
    persistenciaLlamada = PersistenciaLlamada()
    persistenciaLlamada.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    testDesmaterializar()
    # testDeleteAll()
