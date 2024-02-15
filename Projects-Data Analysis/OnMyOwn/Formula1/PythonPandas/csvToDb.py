import pandas as pd
import sqlite3

# Lee el archivo CSV
df = pd.read_csv('../RawCSVArchives/drivers.csv')

# Conecta con la base de datos SQLite (creará un archivo .db si no existe)
conn = sqlite3.connect('drivers.db')

# Guarda el DataFrame en la base de datos como una tabla llamada 'tu_tabla'
df.to_sql('drivers', conn, index=False, if_exists='replace')

# Cierra la conexión
conn.close()
