from Implementacion.Utilidad.SingletonMeta import SingletonMeta

import pyodbc


class ConexionDb(metaclass=SingletonMeta):
    def __init__(self):
        driver = '{ODBC Driver 18 for SQL Server}'
        server = 'localhost\sqlexpress'
        database = 'IVR'
        self.connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};ENCRYPT=no;TRUSTED_CONNECTION=yes'

    def getCursor(self):
        return pyodbc.connect(self.connectionString).cursor()


if __name__ == "__main__":
    # Test

    # conexion = ConexionDb()
    # cursor = conexion.getCursor()
    # selectQuery = 'SELECT * FROM Estado;'
    # cursor.execute(selectQuery)
    # row = cursor.fetchone()
    # print('{:<10}'.format('nombre'))
    # while row:
    #     print('{:<10}'.format(row.nombre))
    #     row = cursor.fetchone()
    print(pyodbc.drivers())