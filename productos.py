from db import connect
import mysql.connector
import uuid  # Para generar códigos únicos si no los estás generando manualmente

def crear_producto(tipo, nombre, editorial, autores, descripcion):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()

        # Generar un código único para el producto (ejemplo con UUID)
        codigo_producto = str(uuid.uuid4())

        try:
            cursor.execute('INSERT INTO productos (codigo_producto, tipo, nombre, editorial, autores, descripcion) VALUES (%s, %s, %s, %s, %s, %s)',
                           (codigo_producto, tipo, nombre, editorial, autores, descripcion))
            conn.commit()
            print(f"Producto '{nombre}' creado con éxito.")
        except mysql.connector.Error as err:
            if err.errno == 1062:  
                print(f"Error: El código de producto '{codigo_producto}' ya está en uso.")
            else:
                print(f"Error al crear el producto: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def ver_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, tipo, nombre, descripcion, eliminado FROM productos')
            productos = cursor.fetchall()
            if productos:
                print("\n--- Productos ---")
                print("+" + "-" * 80 + "+")
                print("| {:<5} | {:<10} | {:<20} | {:<30} | {:<10} |".format("ID", "Tipo", "Nombre", "Descripción", "Estado"))
                print("+" + "-" * 80 + "+")
                for id_producto, tipo, nombre, descripcion, eliminado in productos:
                    estado = "Disponible" if eliminado == 0 else "En Papelera"
                    print("| {:<5} | {:<10} | {:<20} | {:<30} | {:<10} |".format(id_producto, tipo, nombre, descripcion, estado))
                print("+" + "-" * 80 + "+")
                
                opcion = input("Ingrese el ID del producto a eliminar permanentemente (0 para cancelar): ")
                if opcion != "0":
                    try:
                        id_producto = int(opcion)
                        if id_producto in [prod[0] for prod in productos if prod[4] == 1]:
                            cursor.execute('DELETE FROM productos WHERE id = %s', (id_producto,))
                            conn.commit()
                            print(f"Producto con ID '{id_producto}' eliminado permanentemente.")
                        else:
                            print(f"El ID '{id_producto}' no está en la papelera o no es válido para eliminación.")
                    except ValueError:
                        print(f"Error: '{opcion}' no es un ID válido.")
                    except mysql.connector.Error as err:
                        print(f"Error al eliminar producto permanentemente: {err}")
            else:
                print("No hay productos registrados.")
        except mysql.connector.Error as err:
            print(f"Error al recuperar productos: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")


def listar_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, tipo, nombre, descripcion FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            print("+" + "-" * 80 + "+")
            print("| {:<5} | {:<10} | {:<20} | {:<30} |".format("ID", "Tipo", "Nombre", "Descripción"))
            print("+" + "-" * 80 + "+")
            for id_producto, tipo, nombre, descripcion in productos:
                print("| {:<5} | {:<10} | {:<20} | {:<30} |".format(id_producto, tipo, nombre, descripcion))
            print("+" + "-" * 80 + "+")
            
            # Opción para eliminar producto y mover a papelera
            id_producto = input("Ingrese el ID del producto a eliminar (0 para cancelar): ")
            if id_producto != "0":
                try:
                    cursor.execute('UPDATE productos SET eliminado = 1 WHERE id = %s', (id_producto,))
                    conn.commit()
                    print(f"Producto con ID '{id_producto}' movido a la papelera.")
                except mysql.connector.Error as err:
                    print(f"Error al mover producto a la papelera: {err}")
        else:
            print("No hay productos disponibles en la bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT id, tipo, nombre, descripcion FROM productos WHERE eliminado = 1')
        productos_eliminados = cursor.fetchall()
        if productos_eliminados:
            print("\n--- Productos en la Papelera ---")
            print("+" + "-" * 80 + "+")
            print("| {:<5} | {:<10} | {:<20} | {:<30} |".format("ID", "Tipo", "Nombre", "Descripción"))
            print("+" + "-" * 80 + "+")
            for id_producto, tipo, nombre, descripcion in productos_eliminados:
                print("| {:<5} | {:<10} | {:<20} | {:<30} |".format(id_producto, tipo, nombre, descripcion))
            print("+" + "-" * 80 + "+")
        else:
            print("No hay productos en la papelera.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def ver_productos_eliminados():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, tipo, nombre, descripcion FROM productos WHERE eliminado = 1')
            productos_eliminados = cursor.fetchall()
            if productos_eliminados:
                print("\n--- Productos en la Papelera ---")
                print("+" + "-" * 80 + "+")
                print("| {:<5} | {:<10} | {:<20} | {:<30} |".format("ID", "Tipo", "Nombre", "Descripción"))
                print("+" + "-" * 80 + "+")
                for id_producto, tipo, nombre, descripcion in productos_eliminados:
                    print("| {:<5} | {:<10} | {:<20} | {:<30} |".format(id_producto, tipo, nombre, descripcion))
                print("+" + "-" * 80 + "+")
                
                # Opción para restaurar producto
                id_producto = input("Ingrese el ID del producto a restaurar (0 para cancelar): ")
                if id_producto != "0":
                    restaurar_producto(id_producto)
            else:
                print("No hay productos en la papelera.")
        except mysql.connector.Error as err:
            print(f"Error al recuperar productos eliminados: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_producto(id_producto):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE productos SET eliminado = 0 WHERE id = %s', (id_producto,))
            conn.commit()
            print(f"Producto con ID '{id_producto}' restaurado desde la papelera.")
        except mysql.connector.Error as err:
            print(f"Error al restaurar producto desde la papelera: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

