import csv
import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tomate160121",
    database="nutriapp"
)
cursor = conexion.cursor()

# Leer el archivo CSV
with open('recetas_cat_0301.csv', 'r', encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)
    next(lector_csv)  # Saltar la cabecera
    for fila in lector_csv:
        cursor.execute("""
            INSERT INTO recetas (nom, ingredients, passos, desdejuni, dinar, sopar, snack, apartat)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, fila)

# Confirmar los cambios
conexion.commit()
cursor.close()
conexion.close()