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
        cursor.execute('SELECT tipo, nombre, descripcion, codigo_producto FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            for tipo, nombre, descripcion, codigo in productos:
                print(f"Tipo: {tipo}, Nombre: {nombre}, Descripción: {descripcion}, Código: {codigo}")
        else:
            print("No hay productos disponibles en la bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    listar_productos_en_bodega()