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
                            ubicacion VARCHAR(255),
                            capacidad INT,
                            direccion VARCHAR(255),  -- Nueva columna 'direccion'
                            eliminado BOOLEAN DEFAULT FALSE
                          )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            tipo VARCHAR(255) NOT NULL,
                            nombre VARCHAR(255) NOT NULL,
                            editorial VARCHAR(255),
                            autores VARCHAR(255),
                            descripcion TEXT,
                            codigo_producto VARCHAR(255) NOT NULL UNIQUE,
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
        print("Tablas creadas correctamente.")
    else:
        print("No se pudo conectar a la base de datos.")

def describe_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DESCRIBE bodegas;")
        result = cursor.fetchall()
        for row in result:
            print(row)
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def add_missing_columns():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        columns = {
            "ubicacion": "VARCHAR(255)",
            "capacidad": "INT"
        }
        for column, col_type in columns.items():
            try:
                cursor.execute(f"ALTER TABLE bodegas ADD COLUMN {column} {col_type};")
                conn.commit()
                print(f"Columna '{column}' añadida correctamente.")
            except Error as e:
                if "Duplicate column name" in str(e):
                    print(f"La columna '{column}' ya existe.")
                else:
                    print(f"Error al agregar la columna '{column}': {e}")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    create_tables()
    describe_bodegas()
    add_missing_columns()
    describe_bodegas()
