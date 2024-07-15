from db import connect  
import mysql.connector  
import uuid 

# Función para crear un nuevo producto en la base de datos
def crear_producto():
    # Mostrar opciones para seleccionar el tipo de producto
    print("+----------------------------------------+")
    print("|     Seleccione el tipo de producto     |")
    print("+----------------------------------------+")
    print("+----------------------------------------+")
    print("| 1. Libro                               |")
    print("+----------------------------------------+")
    print("| 2. Revista                             |")
    print("+----------------------------------------+")
    print("| 3. Enciclopedia                        |")
    print("+----------------------------------------+")

    respuesta = input("Seleccione una opción: ")

    # Según la respuesta del usuario, establecer el tipo de producto y mostrar editoriales disponibles
    if respuesta == '1':
        tipo_producto = 'libro'
        print("+----------------------------------------+")
        print("|     Seleccione una editorial          |")
        print("+----------------------------------------+")
        print("+----------------------------------------+")
        print("| 1. Editorial Planeta                  |")
        print("+----------------------------------------+")
        print("| 2. Editorial Santillana               |")
        print("+----------------------------------------+")
        print("| 3. Editorial Anaya                    |")
        print("+----------------------------------------+")
    elif respuesta == '2':
        tipo_producto = 'revista'
        print("+----------------------------------------+")
        print("|     Seleccione una editorial          |")
        print("+----------------------------------------+")
        print("+----------------------------------------+")
        print("| 1. Editorial Grupo Z                  |")
        print("+----------------------------------------+")
        print("| 2. Editorial Hachette                 |")
        print("+----------------------------------------+")
        print("| 3. Editorial RBA                      |")
        print("+----------------------------------------+")
    elif respuesta == '3':
        tipo_producto = 'enciclopedia'
        print("+----------------------------------------+")
        print("|     Seleccione una editorial          |")
        print("+----------------------------------------+")
        print("+----------------------------------------+")
        print("| 1. Editorial Océano                   |")
        print("+----------------------------------------+")
        print("| 2. Editorial Larousse                 |")
        print("+----------------------------------------+")
        print("| 3. Editorial Espasa                   |")
        print("+----------------------------------------+")
    else:
        print("Opción no válida")
        return

    respuesta_editorial = input("Seleccione una editorial o 'n' para crear una nueva: ")

    # Según la respuesta del usuario, seleccionar una editorial existente o ingresar una nueva
    if respuesta_editorial.lower() == 'n':
        editorial = input("Ingrese el nombre de la nueva editorial: ")
    else:
        if tipo_producto == 'libro':
            editoriales = ['Editorial Planeta', 'Editorial Santillana', 'Editorial Anaya']
        elif tipo_producto == 'revista':
            editoriales = ['Editorial Grupo Z', 'Editorial Hachette', 'Editorial RBA']
        elif tipo_producto == 'enciclopedia':
            editoriales = ['Editorial Océano', 'Editorial Larousse', 'Editorial Espasa']
        try:
            editorial = editoriales[int(respuesta_editorial) - 1]
        except (ValueError, IndexError):
            print("Opción no válida")
            return

    # Solicitar información adicional del producto al usuario
    nombre = input("Ingrese el nombre del producto: ")
    autores = input("Ingrese los autores del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")

    # Conectar a la base de datos y realizar la inserción del nuevo producto
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()

        # Generar un código único para el producto (ejemplo con UUID)
        codigo_producto = str(uuid.uuid4())

        try:
            # Insertar el nuevo producto en la tabla productos
            cursor.execute('INSERT INTO productos (codigo_producto, tipo, nombre, editorial, autores, descripcion) VALUES (%s, %s, %s, %s, %s, %s)',
                           (codigo_producto, tipo_producto, nombre, editorial, autores, descripcion))
            conn.commit()
            print(f"Producto '{nombre}' creado con éxito.")

            # Agregar el producto a la tabla bodegas con cantidad inicial 0
            cursor.execute('INSERT INTO bodegas (codigo, nombre, ubicacion, capacidad, direccion) VALUES (%s, %s, %s, %s, %s)',
                           (codigo_producto, nombre, 'ubicacion', 'capacidad', 'direccion'))
            conn.commit()
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Error de duplicado de clave única
                print(f"Error: El código de producto '{codigo_producto}' ya está en uso.")
            else:
                print(f"Error al crear el producto: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")
# Función para mostrar todos los productos disponibles y en la papelera
def ver_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            # Consultar todos los productos (tanto disponibles como en la papelera)
            cursor.execute('SELECT id, tipo, nombre, descripcion, editorial, eliminado FROM productos')
            productos = cursor.fetchall()
            if productos:
                print("\n--- Productos ---")
                print("+" + "-" * 100 + "+")
                print("| {:<5} | {:<10} | {:<20} | {:<30} | {:<20} | {:<10} |".format("ID", "Tipo", "Nombre", "Descripción", "Editorial", "Estado"))
                print("+" + "-" * 100 + "+")
                for id_producto, tipo, nombre, descripcion, editorial, eliminado in productos:
                    estado = "Disponible" if eliminado == 0 else "En Papelera"
                    print("| {:<5} | {:<10} | {:<20} | {:<30} | {:<20} | {:<10} |".format(id_producto, tipo, nombre, descripcion, editorial, estado))
                print("+" + "-" * 100 + "+")
                
                opcion = input("Ingrese el ID del producto a eliminar permanentemente (0 para cancelar): ")
                if opcion != "0":
                    try:
                        id_producto = int(opcion)
                        if id_producto in [prod[0] for prod in productos if prod[5] == 1]:
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

# Función para listar productos disponibles en la bodega
def listar_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Consulta para obtener los productos disponibles en la bodega
            cursor.execute("SELECT id, tipo, nombre, editorial, descripcion FROM productos WHERE eliminado = 0;")
            productos = cursor.fetchall()
            
            # Imprimir encabezado
            print("--- Productos Disponibles en la Bodega ---")
            print("+--------------------------------------------------------------------------------+")
            print("| ID    | Tipo       | Nombre               | Editorial            | Descripción                    |")
            print("+--------------------------------------------------------------------------------+")
            
            for producto in productos:
                # Imprimir cada producto con sus detalles
                print(f"| {producto['id']: <5} | {producto['tipo']: <9} | {producto['nombre']: <20} | {producto['editorial']: <20} | {producto['descripcion']: <30} |")
            
            print("+--------------------------------------------------------------------------------+")
            
            # Solicitar al usuario ingresar el ID del producto a eliminar
            while True:
                id_producto = input("Ingrese el ID del producto a eliminar (0 para cancelar): ")
                if id_producto == "0":
                    break
                else:
                    # Verificar si el ID ingresado es válido y eliminar el producto si es así
                    cursor.execute("SELECT id FROM productos WHERE id = %s AND eliminado = 0;", (id_producto,))
                    if cursor.fetchone():
                        eliminar_producto(id_producto)
                        print(f"Producto con ID {id_producto} eliminado correctamente.")
                    else:
                        print("ID de producto no válido o producto ya eliminado.")
            
        except mysql.connector.Error as e:
            print(f"Error al listar productos: {e}")
        
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

# Función para eliminar un producto por su ID
def eliminar_producto(id_producto):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            # Actualizar el campo 'eliminado' del producto a True
            cursor.execute("UPDATE productos SET eliminado = 1 WHERE id = %s;", (id_producto,))
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error al eliminar producto: {e}")
        
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

# Función para mostrar productos en la papelera
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

# Función para mostrar y restaurar productos desde la papelera
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

# Función para restaurar un producto desde la papelera
def restaurar_producto(id_producto):
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('UPDATE productos SET eliminado = 0 WHERE id = %s', (id_producto,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Producto con ID '{id_producto}' restaurado correctamente desde la papelera.")
        else:
            print("No se pudo conectar a la base de datos.")
    except mysql.connector.Error as e:
        print(f"Error al restaurar el producto desde la papelera: {str(e)}")

# Función principal que ejecuta las funciones en orden
if __name__ == "__main__":
    listar_productos_en_bodega()
    crear_producto()
    papelera_productos()
