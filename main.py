from usuarios import autenticar_usuario, crear_usuario, papelera_usuarios, mover_a_papelera_usuario, restaurar_usuario
from productos import crear_producto, papelera_productos, mover_a_papelera_producto, restaurar_producto
from bodegas import crear_bodega, papelera_bodegas, mover_a_papelera_bodega, restaurar_bodega
from movimientos import registrar_movimiento, papelera_movimientos, mover_a_papelera_movimiento, restaurar_movimiento, listar_movimientos
from db import connect

def menu_principal():
    print("Bienvenido al Sistema de Inventario 'El gran Poeta'")
    print("1. Iniciar Sesión")
    print("2. Registrarse")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        iniciar_sesion()
    elif opcion == "2":
        registrar()
    elif opcion == "3":
        print("Gracias por usar nuestro sistema. ¡Hasta luego!")
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
    
def iniciar_sesion():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    
    user = autenticar_usuario(usuario, contraseña)
    
    if not user:
        print("Usuario o contraseña incorrecta.")
        return
    
    if user[4] == "jefe":
        menu_jefe()
    elif user[4] == "bodeguero":
        menu_bodeguero()
    else:
        print("Rol de usuario no reconocido.")

def registrar():
    print("\n--- Registro de Nuevo Usuario ---")
    nombre = input("Nombre: ")
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    rol = input("Rol (jefe/bodeguero): ")

    if nombre.strip() == "" or usuario.strip() == "" or contraseña.strip() == "" or rol.strip() not in ["jefe", "bodeguero"]:
        print("Por favor, complete todos los campos y seleccione un rol válido.")
        return

    if crear_usuario(nombre, usuario, contraseña, rol):
        print("Usuario registrado con éxito. Iniciando sesión...")
        iniciar_sesion()
    else:
        print("Error al registrar usuario. Inténtelo de nuevo.")

def menu_jefe():
    while True:
        print("\n--- Menú Jefe de Bodega ---")
        print("1. Crear Bodega")
        print("2. Crear Producto")
        print("3. Ver Papelera")
        print("4. Ver Bodegas Creadas")
        print("5. Ver Productos Creados")
        print("6. Generar Informe")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre_bodega = input("Nombre de la Bodega: ")
            crear_bodega(nombre_bodega)
        elif opcion == "2":
            tipo = input("Tipo de Producto (Libro/Revista/Enciclopedia): ")
            nombre = input("Nombre del Producto: ")
            editorial = input("Editorial: ")
            autores = input("Autores: ")
            descripcion = input("Descripción: ")
            crear_producto(tipo, nombre, editorial, autores, descripcion)
        elif opcion == "3":
            ver_papelera("jefe")
        elif opcion == "4":
            ver_bodegas_creadas()
        elif opcion == "5":
            ver_productos_creados()
        elif opcion == "6":
            generar_informe()
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")
    
def menu_bodeguero():
    while True:
        print("\n--- Menú Bodeguero ---")
        print("1. Registrar Movimiento")
        print("2. Ver Papelera")
        print("3. Ver Productos en Bodega")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            bodega_origen = input("ID de Bodega Origen: ")
            bodega_destino = input("ID de Bodega Destino: ")
            productos = input("Productos (separados por comas): ")
            cantidades = input("Cantidades (separadas por comas): ")
            usuario = input("Usuario que realiza el movimiento: ")
            registrar_movimiento(bodega_origen, bodega_destino, productos, cantidades, usuario)
        elif opcion == "2":
            ver_papelera("bodeguero")
        elif opcion == "3":
            ver_productos_en_bodega()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def ver_papelera(usuario_rol):
    while True:
        print("\n--- Papelera ---")
        if usuario_rol == "jefe":
            print("1. Ver Bodegas Eliminadas")
            print("2. Ver Productos Eliminados")
            print("3. Ver Movimientos Eliminados")
            print("4. Ver Usuarios Eliminados")
            print("5. Restaurar Bodega")
            print("6. Restaurar Producto")
            print("7. Restaurar Movimiento")
            print("8. Restaurar Usuario")
            print("9. Salir")
        elif usuario_rol == "bodeguero":
            print("1. Ver Productos Eliminados")
            print("2. Ver Movimientos Eliminados")
            print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if usuario_rol == "jefe":
            if opcion == "1":
                papelera_bodegas()
            elif opcion == "2":
                papelera_productos()
            elif opcion == "3":
                papelera_movimientos()
            elif opcion == "4":
                papelera_usuarios()
            elif opcion == "5":
                restaurar_bodega()
            elif opcion == "6":
                restaurar_producto()
            elif opcion == "7":
                restaurar_movimiento()
            elif opcion == "8":
                restaurar_usuario()
            elif opcion == "9":
                break
            else:
                print("Opción no válida.")
        elif usuario_rol == "bodeguero":
            if opcion == "1":
                papelera_productos()
            elif opcion == "2":
                papelera_movimientos()
            elif opcion == "3":
                break
            else:
                print("Opción no válida.")

def ver_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT tipo, nombre, descripcion FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            for tipo, nombre, descripcion in productos:
                print(f"Tipo: {tipo}, Nombre: {nombre}, Descripción: {descripcion}")
        else:
            print("No hay productos disponibles en la bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bodegas WHERE eliminado = 1')
        bodegas_eliminadas = cursor.fetchall()
        if bodegas_eliminadas:
            print("\n--- Bodegas Eliminadas ---")
            for bodega in bodegas_eliminadas:
                print(f"ID: {bodega[0]}, Nombre: {bodega[1]}")
        else:
            print("No hay bodegas eliminadas.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bodegas WHERE eliminado = 1')
        bodegas_eliminadas = cursor.fetchall()
        if bodegas_eliminadas:
            print("\n--- Bodegas Eliminadas ---")
            for bodega in bodegas_eliminadas:
                print(f"ID: {bodega[0]}, Nombre: {bodega[1]}")
            id_bodega = input("Seleccione el ID de la Bodega a restaurar: ")
            cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))
            conn.commit()
            print(f"Bodega con ID '{id_bodega}' restaurada.")
        else:
            print("No hay bodegas eliminadas para restaurar.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def ver_bodegas_creadas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bodegas WHERE eliminado = 0')
        bodegas = cursor.fetchall()
        if bodegas:
            print("\n--- Bodegas Creadas ---")
            for bodega in bodegas:
                print(f"Nombre: {bodega[1]}, Código: {bodega[2]}")
        else:
            print("No hay bodegas creadas.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def ver_productos_creados():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Creados ---")
            for producto in productos:
                print(f"Nombre: {producto[1]}, Código: {producto[2]}")
        else:
            print("No hay productos creados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def cantidad_productos_por_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT b.nombre, COUNT(p.id) AS cantidad_productos FROM bodegas b LEFT JOIN productos p ON b.id = p.bodega_id GROUP BY b.nombre')
        productos_por_bodega = cursor.fetchall()
        if productos_por_bodega:
            print("\n--- Cantidad de Productos por Bodega ---")
            for bodega, cantidad in productos_por_bodega:
                print(f"Bodega: {bodega}, Cantidad de Productos: {cantidad}")
        else:
            print("No hay productos registrados en ninguna bodega.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def tipos_de_productos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT tipo FROM productos')
        tipos_productos = cursor.fetchall()
        if tipos_productos:
            print("\n--- Tipos de Productos Disponibles ---")
            for tipo in tipos_productos:
                print(f"Tipo de Producto: {tipo[0]}")
        else:
            print("No hay tipos de productos registrados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def listar_productos_por_editorial():
    editorial = input("Ingrese el nombre de la editorial: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM bodegas')
        bodegas = cursor.fetchall()
        for bodega in bodegas:
            cursor.execute('SELECT nombre FROM productos WHERE editorial = %s AND bodega_id = (SELECT id FROM bodegas WHERE nombre = %s)', (editorial, bodega[0]))
            productos = cursor.fetchall()
            if productos:
                print(f"\n--- Productos de la Editorial '{editorial}' en la Bodega '{bodega[0]}' ---")
                for producto in productos:
                    print(f"Nombre del Producto: {producto[0]}")
            else:
                print(f"No hay productos de la editorial '{editorial}' en la bodega '{bodega[0]}'.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    menu_principal()