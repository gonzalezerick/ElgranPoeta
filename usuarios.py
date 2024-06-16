from db import connect

def crear_usuario(nombre, usuario, contraseña, rol):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
            existing_user = cursor.fetchone()
            if existing_user:
                print("Error: El nombre de usuario ya está en uso.")
                return False

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
    
def autenticar_usuario(usuario, contraseña):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s', (usuario, contraseña))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return user
    return None

def papelera_usuarios():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE eliminado = 1')
        usuarios_eliminados = cursor.fetchall()
        if usuarios_eliminados:
            print("\n--- Papelera de Usuarios ---")
            for usuario in usuarios_eliminados:
                print(f"ID: {usuario[0]}, Nombre: {usuario[1]}, Usuario: {usuario[2]}")
        else:
            print("No hay usuarios eliminados en la papelera.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def mover_a_papelera_usuario(id_usuario):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET eliminado = 1 WHERE id = %s', (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Usuario con ID '{id_usuario}' movido a la papelera.")
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_usuario(id_usuario):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET eliminado = 0 WHERE id = %s', (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Usuario con ID '{id_usuario}' restaurado.")
    else:
        print("No se pudo conectar a la base de datos.")
