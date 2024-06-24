from db import connect

def papelera_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre FROM bodegas WHERE eliminado = 1')
        bodegas = cursor.fetchall()
        if bodegas:
            print("\n--- Bodegas Eliminadas ---")
            print("+" + "-" * 40 + "+")
            print("| {:<10} | {:<30} |".format("ID", "Nombre"))
            print("+" + "-" * 40 + "+")
            for id, nombre in bodegas:
                print("| {:<10} | {:<30} |".format(id, nombre))
            print("+" + "-" * 40 + "+")
        else:
            print("No se encuentran bodegas eliminadas.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre FROM productos WHERE eliminado = 1')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Eliminados ---")
            print("+" + "-" * 40 + "+")
            print("| {:<10} | {:<30} |".format("ID", "Nombre"))
            print("+" + "-" * 40 + "+")
            for id, nombre in productos:
                print("| {:<10} | {:<30} |".format(id, nombre))
            print("+" + "-" * 40 + "+")
        else:
            print("No se encuentran productos eliminados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_movimientos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, detalle FROM movimientos WHERE eliminado = 1')
        movimientos = cursor.fetchall()
        if movimientos:
            print("\n--- Movimientos Eliminados ---")
            print("+" + "-" * 60 + "+")
            print("| {:<10} | {:<48} |".format("ID", "Detalle"))
            print("+" + "-" * 60 + "+")
            for id, detalle in movimientos:
                print("| {:<10} | {:<48} |".format(id, detalle))
            print("+" + "-" * 60 + "+")
        else:
            print("No se encuentran movimientos eliminados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_usuarios():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, usuario FROM usuarios WHERE eliminado = 1')
        usuarios = cursor.fetchall()
        if usuarios:
            print("\n--- Usuarios Eliminados ---")
            print("+" + "-" * 40 + "+")
            print("| {:<10} | {:<30} |".format("ID", "Usuario"))
            print("+" + "-" * 40 + "+")
            for id, usuario in usuarios:
                print("| {:<10} | {:<30} |".format(id, usuario))
            print("+" + "-" * 40 + "+")
        else:
            print("No se encuentran usuarios eliminados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_bodega():
    id_bodega = input("Ingrese el ID de la bodega a restaurar: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))
        conn.commit()
        print("Bodega restaurada con éxito.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_producto():
    id_producto = input("Ingrese el ID del producto a restaurar: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET eliminado = 0 WHERE id = %s', (id_producto,))
        conn.commit()
        print("Producto restaurado con éxito.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_movimiento():
    id_movimiento = input("Ingrese el ID del movimiento a restaurar: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE movimientos SET eliminado = 0 WHERE id = %s', (id_movimiento,))
        conn.commit()
        print("Movimiento restaurado con éxito.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_usuario():
    id_usuario = input("Ingrese el ID del usuario a restaurar: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET eliminado = 0 WHERE id = %s', (id_usuario,))
        conn.commit()
        print("Usuario restaurado con éxito.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")
