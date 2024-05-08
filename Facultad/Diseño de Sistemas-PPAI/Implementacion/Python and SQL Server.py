# Este script no se usa en el proyecto, es solo para probar la conexión a la base de datos

# 1 - Download and install ODBC, which is Open DataBase Connectivity, the driver for the connection to the db
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows
# 2 - Install pyodbc, the library for the connection to the db
# pip install pyodbc
import pyodbc

# First, connect to the server
# The connection string is used to initialize the ODBC driver connection to the server

# The available drivers can be obtained with the folling line, we'll use ODBC Driver 18 for SQL Server
# pyodbc.drivers()
driver = '{ODBC Driver 18 for SQL Server}'
# Some example server values are
# server = 'tcp:myserver.database.windows.net' # for a server running on Azure
# server = 'localhost\sqlexpress' # for a named instance, this is the default name when installing sql server express
# server = 'myserver,port' # to specify an alternate port
server = 'localhost\sqlexpress'
# The name of the db
database = 'IVR'
# If we're connecting using username and password, we need to specify the UID and PWD keyword arguments
# If we're connecting using windows authetication, we need to specify the TRUSTED_CONNECTION keyword argument
# We dont need encription for local connections
# The connection string
connectionString = f'DRIVER={driver};SERVER={server};DATABASE={database};ENCRYPT=no;TRUSTED_CONNECTION=yes'
# Create the connection and get a cursor object to start executing queries
connection = pyodbc.connect(connectionString)
cursor = connection.cursor()

# Sample SELECT query
selectQuery = 'SELECT * FROM Estado;'
cursor.execute(selectQuery)
# To get the obtained data from the cursor, we can use fetchall() to get all the rows
# row = cursor.fetchall()
# print(row)

# or fetchone() to get one row at a time, and the cursor will move to the next one
row = cursor.fetchone()
print('{:<10}'.format('nombre'))
while row:
    # We can use row[0] to get the first tuple
    # We can also use row.columnName[0] to get the value of a specific column
    print('{:<10}'.format(row.nombre))
    row = cursor.fetchone()

# We can also get the column names with
# columns = [row.column_name for row in cursor.columns(table='Table1')]
# print(columns)

# We can list the tables
# tables = [row.table_name for row in cursor.tables()]
# print(tables[:5])


# Sample INSERT query
# The parameters (?) are used to protect from SQL injection
# insertQuery = 'INSERT INTO Estado (Nombre) VALUES (?);'
# count = cursor.execute(insertQuery, 'test3').rowcount
# connection.commit()
# print('Rows inserted: ' + str(count))

# Close the connection
connection.close()
