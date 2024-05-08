from Implementacion.Entities.Estado import Estado, Generadorestados
from Implementacion.Persistencia.ConexionDb import ConexionDb


class PersistenciaEstado:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Estado;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        estados = []
        while row:
            estados.append(Estado(row.nombre))
            row = cursor.fetchone()
        return estados

    def desmaterializar(self, objetos):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO Estado (nombre) VALUES (?);'
        for estado in objetos:
            if self.materializarPorNombre(estado.nombre) is None:
                cursor.execute(insertQuery, estado.nombre)
                cursor.commit()
                # Devolver el id del estado obtenido
                getIdQuery = 'SELECT @@IDENTITY AS ID;'
                return cursor.execute(getIdQuery).fetchval()


    def materializarPorId(self, id):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Estado WHERE idEstado = ?;'
        cursor.execute(selectQuery, id)
        row = cursor.fetchone()
        if row:
            return Estado(row.nombre)
        else:
            return None

    def materializarPorNombre(self, nombre):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Estado WHERE nombre = ?;'
        cursor.execute(selectQuery, nombre)
        row = cursor.fetchone()
        if row:
            return Estado(row.nombre)
        else:
            return None

    def getIdFromNombre(self, nombre):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Estado WHERE nombre = ?;'
        cursor.execute(selectQuery, nombre)
        row = cursor.fetchone()
        if row:
            return row.idEstado
        else:
            return None

    def deleteAll(self):
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM Estado;'
        cursor.execute(deleteQuery)
        cursor.commit()
        # Reiniciar el contador de id
        resetIdQuery = "DBCC CHECKIDENT ('Estado', RESEED, 0);"
        cursor.execute(resetIdQuery)
        cursor.commit()


def testMaterializar():
    persistenciaEstado = PersistenciaEstado()
    estados = persistenciaEstado.materializar()
    for estado in estados:
        print(estado)


def testMaterializarPorNombre():
    persistenciaEstado = PersistenciaEstado()
    estado = persistenciaEstado.materializarPorNombre('Iniciada')
    print(estado)


def testDesmaterializar():
    persistenciaEstado = PersistenciaEstado()
    # estados = [Estado('test1'), Estado('test2')]
    estados = Generadorestados().obtenerEstados()
    persistenciaEstado.desmaterializar(estados)


def testDeleteAll():
    persistenciaEstado = PersistenciaEstado()
    persistenciaEstado.deleteAll()


if __name__ == "__main__":
    testMaterializar()
    # testMaterializarPorNombre()
    # testDesmaterializar()
    # testDeleteAll()

