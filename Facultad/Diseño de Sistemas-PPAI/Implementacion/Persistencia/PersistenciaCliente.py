from Implementacion.Entities.Cliente import Cliente
from Implementacion.Persistencia.ConexionDb import ConexionDb


class PersistenciaCliente:
    def materializar(self):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Cliente;'
        cursor.execute(selectQuery)
        row = cursor.fetchone()
        clientes = []
        while row:
            clientes.append(Cliente(row.dni, row.nombreCompleto, row.nroCelular))
            row = cursor.fetchone()
        return clientes

    def materializarPorDni(self, dni):
        cursor = ConexionDb().getCursor()
        selectQuery = 'SELECT * FROM Cliente WHERE dni = ?;'
        cursor.execute(selectQuery, dni)
        row = cursor.fetchone()
        if row:
            return Cliente(row.dni, row.nombreCompleto, row.nroCelular)
        else:
            return None

    def desmaterializar(self, objetos):
        cursor = ConexionDb().getCursor()
        insertQuery = 'INSERT INTO Cliente (dni, nombreCompleto, nroCelular) VALUES (?, ?, ?);'
        updateQuery = 'UPDATE Cliente SET nombreCompleto = ?, nroCelular = ? WHERE dni = ?;'
        for cliente in objetos:
            # Verificar que no exista ya el cliente
            if self.materializarPorDni(cliente.dni) is None:
                cursor.execute(insertQuery, cliente.dni, cliente.nombreCompleto, cliente.nroCelular)
            else:
                cursor.execute(updateQuery, cliente.nombreCompleto, cliente.nroCelular, cliente.dni)
            cursor.commit()

    def deleteAll(self):
        # Borrar las filas
        cursor = ConexionDb().getCursor()
        deleteQuery = 'DELETE FROM Cliente;'
        cursor.execute(deleteQuery)
        cursor.commit()


def testMaterializar():
    persistenciaCliente = PersistenciaCliente()
    clientes = persistenciaCliente.materializar()
    for cliente in clientes:
        print(cliente)


def testMaterializarPorDni():
    persistenciaCliente = PersistenciaCliente()
    cliente = persistenciaCliente.materializarPorDni(1)
    print(cliente)


def testDesmaterializar():
    persistenciaCliente = PersistenciaCliente()
    clientes = [Cliente(1, 'test4', 12345678),
                Cliente(2, 'test5', 12345678)]
    persistenciaCliente.desmaterializar(clientes)


def testDeleteAll():
    persistenciaCliente = PersistenciaCliente()
    persistenciaCliente.deleteAll()


if __name__ == "__main__":
    # testMaterializar()
    # testMaterializarPorDni()
    # testDesmaterializar()
    testDeleteAll()
