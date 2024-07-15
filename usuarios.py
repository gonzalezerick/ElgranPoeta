from db import connect  

# funcion para crear usuario
def crear_usuario(nombre, usuario, contraseña, rol):
    conn = connect()  # Establece la conexión a la base de datos
    if conn is not None:
        cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL
        try:
            # Verifica si ya existe un usuario con el mismo nombre
            cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
            existing_user = cursor.fetchone()
            if existing_user:
                print("Error: El nombre de usuario ya está en uso.")
                return False

            # Inserta el nuevo usuario en la base de datos
            cursor.execute('INSERT INTO usuarios (nombre, usuario, contraseña, rol) VALUES (%s, %s, %s, %s)',
                           (nombre, usuario, contraseña, rol))
            conn.commit()  
            print(f"Usuario '{nombre}' creado con éxito.")
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()    
    else:
        print("No se pudo conectar a la base de datos.")
    return False
#funcion para autenticar usuario
def autenticar_usuario(usuario, contraseña):
    conn = connect()  # Establece la conexión a la base de datos
    if conn is not None:
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s', (usuario, contraseña))
        user = cursor.fetchone()  
        cursor.close()
        conn.close()    
        if user:
            return user  # Retorna el usuario autenticado si se encontró uno
    return None  # Retorna None si no se encontró ningún usuario que coincida
