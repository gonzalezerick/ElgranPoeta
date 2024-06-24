from usuarios import autenticar_usuario, crear_usuario
from productos import crear_producto, listar_productos_en_bodega, papelera_productos, restaurar_producto, eliminar_producto
from bodegas import crear_bodega, listar_bodegas
from movimientos import registrar_movimiento
from papelera import papelera_usuarios, papelera_productos, papelera_bodegas, papelera_movimientos, restaurar_usuario, restaurar_producto, restaurar_bodega, restaurar_movimiento
from db import connect
import getpass

def imprimir_cuadro(titulo, opciones):
    print("+" + "-" * 40 + "+")
    print("|{:^40}|".format(titulo))
    print("+" + "-" * 40 + "+")
    for opcion in opciones:
        print("+" + "-" * 40 + "+")
        print("| {:<38} |".format(opcion))
    print("+" + "-" * 40 + "+")

def menu_principal():
    opciones = [
        "1. Iniciar Sesión",
        "2. Registrarse",
        "3. Salir"
    ]
    imprimir_cuadro("Bienvenido al Sistema del El gran Poeta", opciones)
    
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
    contraseña = getpass.getpass("Contraseña: ")
    
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
    print("\n+" + "-" * 40 + "+")
    print("|{:^40}|".format("Registro de Nuevo Usuario"))
    print("+" + "-" * 40 + "+")
    
    nombre = input("Nombre: ")
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")
    confirmar_contraseña = getpass.getpass("Confirmar Contraseña: ")

    if contraseña != confirmar_contraseña:
        print("Las contraseñas no coinciden. Volviendo al menú principal.")
        return menu_principal()

    opciones_rol = ["1. Jefe", "2. Bodeguero"]
    imprimir_cuadro("Seleccione el rol del usuario", opciones_rol)
    rol_opcion = input("Seleccione una opción: ")
    if rol_opcion == "1":
        rol = "jefe"
    elif rol_opcion == "2":
        rol = "bodeguero"
    else:
        print("Opción no válida. Volviendo al menú principal.")
        return menu_principal()

    if nombre.strip() == "" or usuario.strip() == "" or contraseña.strip() == "" or rol.strip() not in ["jefe", "bodeguero"]:
        print("Por favor, complete todos los campos y seleccione un rol válido. Volviendo al menú principal.")
        return menu_principal()

    if crear_usuario(nombre, usuario, contraseña, rol):
        print("Usuario registrado con éxito. Volviendo al menú principal.")
        return menu_principal()
    else:
        print("Error al registrar usuario. Inténtelo de nuevo. Volviendo al menú principal.")
        return menu_principal()

def menu_jefe():
    while True:
        opciones = [
            "1. Crear Bodega",
            "2. Crear Producto",
            "3. Ver Papelera",
            "4. Ver Bodegas Creadas",
            "5. Ver Productos Creados",
            "6. Generar Informe",
            "7. Salir"
        ]
        imprimir_cuadro("Menú Jefe de Bodega", opciones)
        
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
            listar_bodegas()
        elif opcion == "5":
            listar_productos_en_bodega()
        elif opcion == "6":
            generar_informe()
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

def menu_bodeguero():
    while True:
        opciones = [
            "1. Registrar Movimiento",
            "2. Ver Papelera",
            "3. Ver Productos en Bodega",
            "4. Salir"
        ]
        imprimir_cuadro("Menú Bodeguero", opciones)
        
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
            listar_productos_en_bodega()
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def ver_papelera(usuario_rol):
    while True:
        if usuario_rol == "jefe":
            opciones = [
                "1. Ver Bodegas Eliminadas",
                "2. Ver Productos Eliminados",
                "3. Ver Movimientos Eliminados",
                "4. Ver Usuarios Eliminados",
                "5. Restaurar Bodega",
                "6. Restaurar Producto",
                "7. Restaurar Movimiento",
                "8. Restaurar Usuario",
                "9. Salir"
            ]
            imprimir_cuadro("Papelera", opciones)
        elif usuario_rol == "bodeguero":
            opciones = [
                "1. Ver Productos Eliminados",
                "2. Ver Movimientos Eliminados",
                "3. Salir"
            ]
            imprimir_cuadro("Papelera", opciones)
        
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

def listar_productos_en_bodega():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT tipo, nombre, descripcion FROM productos WHERE eliminado = 0')
        productos = cursor.fetchall()
        if productos:
            print("\n--- Productos Disponibles en la Bodega ---")
            print("+" + "-" * 80 + "+")
            print("| {:<20} | {:<30} | {:<30} |".format("Tipo", "Nombre", "Descripción"))
            print("+" + "-" * 80 + "+")
            for tipo, nombre, descripcion in productos:
                print("| {:<20} | {:<30} | {:<30} |".format(tipo, nombre, descripcion))
            print("+" + "-" * 80 + "+")
        else:
            print("No se encuentran productos.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def generar_informe():
    print("Funcionalidad de generar informe no implementada.")

if __name__ == "__main__":
    menu_principal()
