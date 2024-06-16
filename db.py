import mysql.connector
from mysql.connector import Error

def connect():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='inventario_db',
            user='root',
            password=''
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def create_tables():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255) NOT NULL,
                            usuario VARCHAR(255) NOT NULL UNIQUE,
                            contraseña VARCHAR(255) NOT NULL,
                            rol VARCHAR(255) NOT NULL,
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS bodegas (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255) NOT NULL,
                            codigo VARCHAR(255) NOT NULL UNIQUE,
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            tipo VARCHAR(255) NOT NULL,
                            nombre VARCHAR(255) NOT NULL,
                            editorial VARCHAR(255),
                            autores VARCHAR(255),
                            descripcion TEXT,
                            codigo_producto VARCHAR(255) NOT NULL UNIQUE,  # Se agregó la columna 'codigo_producto'
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS movimientos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            bodega_origen INT,
                            bodega_destino INT,
                            productos TEXT,
                            cantidades TEXT,
                            usuario VARCHAR(255),
                            fecha DATETIME,
                            eliminado BOOLEAN DEFAULT FALSE,
                            FOREIGN KEY (bodega_origen) REFERENCES bodegas(id),
                            FOREIGN KEY (bodega_destino) REFERENCES bodegas(id)
                          )''')
        
        conn.commit()
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def ver_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT tipo, nombre, descripcion, codigo_producto FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            for tipo, nombre, descripcion, codigo_producto in productos:
                print(f"Tipo: {tipo}, Nombre: {nombre}, Descripción: {descripcion}, Código: {codigo_producto}")
        else:
            print("No hay productos disponibles en la bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    create_tables()