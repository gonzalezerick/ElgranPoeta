import mysql.connector
from mysql.connector import Error

# Función para establecer la conexión a la base de datos
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

# Función para crear las tablas en la base de datos
def create_tables():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()

        # Crea la tabla usuarios
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255) NOT NULL,
                            usuario VARCHAR(255) NOT NULL UNIQUE,
                            contraseña VARCHAR(255) NOT NULL,
                            rol VARCHAR(255) NOT NULL,
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')

        # Crea la tabla bodegas
        cursor.execute('''CREATE TABLE IF NOT EXISTS bodegas (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(255) NOT NULL,
                            codigo VARCHAR(255) NOT NULL UNIQUE,
                            ubicacion VARCHAR(255),
                            capacidad INT,
                            direccion VARCHAR(255),
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')

        # Crea la tabla productos
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            tipo VARCHAR(255) NOT NULL,
                            nombre VARCHAR(255) NOT NULL,
                            editorial VARCHAR(255),
                            autores VARCHAR(255),
                            descripcion TEXT,
                            codigo_producto VARCHAR(255) NOT NULL,
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')

        # Crea la tabla movimientos
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
        cursor.execute ('''CREATE TABLE IF NOT EXISTS informes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre_informe VARCHAR(255) NOT NULL,
                            nombre_producto VARCHAR(255) NOT NULL,
                            cantidad INT NOT NULL,
                            tipo VARCHAR(255) NOT NULL,
                            editorial VARCHAR(255) NOT NULL,
                            eliminado BOOLEAN DEFAULT FALSE);''')

        conn.commit()
        cursor.close()
        conn.close()
        print("Tablas creadas correctamente.")
    else:
        print("No se pudo conectar a la base de datos.")

# Función para describir la estructura de la tabla 'productos'
def describe_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DESCRIBE productos;")
        result = cursor.fetchall()
        print("\n--- Estructura de la tabla productos ---")
        for row in result:
            print(row)
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

# Función para agregar la columna 'codigo_producto' si no está presente
def add_codigo_producto_column():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER TABLE productos ADD COLUMN codigo_producto VARCHAR(255) NOT NULL UNIQUE;")  
            conn.commit()  # Confirma la transacción
            print("Columna 'codigo_producto' añadida correctamente.")
        except Error as e:  
            if "Duplicate column name" in str(e):  
                print("La columna 'codigo_producto' ya existe.")
            else:
                print(f"Error al agregar la columna 'codigo_producto': {e}")
        
        cursor.close()  
        conn.close()  
    else:
        print("No se pudo conectar a la base de datos.")

# Bloque principal que se ejecuta si el script es ejecutado directamente
if __name__ == "__main__":
    create_tables()  # Llama a la función para crear las tablas
    describe_productos()  # Llama a la función para describir la tabla productos
    add_codigo_producto_column()  # Llama a la función para agregar la columna codigo_producto si no está presente
    describe_productos()  # Llama de nuevo a la función para describir la tabla productos después de modificarla
