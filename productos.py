from db import connect

def crear_producto(tipo, nombre, editorial, autores, descripcion):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (tipo, nombre, editorial, autores, descripcion) VALUES (%s, %s, %s, %s, %s)',
                       (tipo, nombre, editorial, autores, descripcion))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Producto '{nombre}' creado con éxito.")
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_productos():
    print("\n--- Papelera de Productos ---")

def eliminar_producto(id_producto):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id = %s', (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Producto con ID '{id_producto}' eliminado.")
    else:
        print("No se pudo conectar a la base de datos.")

def mover_a_papelera_producto(id_producto):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET eliminado = 1 WHERE id = %s', (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Producto con ID '{id_producto}' movido a la papelera.")
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_producto(id_producto):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET eliminado = 0 WHERE id = %s', (id_producto,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Producto con ID '{id_producto}' restaurado.")
    else:
        print("No se pudo conectar a la base de datos.")

def listar_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT tipo, nombre, descripcion FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            print("+" + "-" * 80 + "+")
            print("| {:<10} | {:<20} | {:<30} |".format("Tipo", "Nombre", "Descripción"))
            print("+" + "-" * 80 + "+")
            for tipo, nombre, descripcion in productos:
                print("| {:<10} | {:<20} | {:<30} |".format(tipo, nombre, descripcion))
            print("+" + "-" * 80 + "+")
        else:
            print("No hay productos disponibles en la bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")
