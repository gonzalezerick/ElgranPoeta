import os
import getpass
from usuarios import autenticar_usuario, crear_usuario
from productos import crear_producto, listar_productos_en_bodega, papelera_productos, ver_productos_eliminados, restaurar_producto
from bodegas import listar_bodegas, crear_bodega, papelera_bodegas, restaurar_bodega
from informes import generar_informe, mover_informe_a_papelera, restaurar_informe_papelera, inicializar_directorio_informes, ver_informe, listar_informes, listar_informes_papelera, ver_informes_en_papelera, generar_informe_movimiento
from movimientos import guardar_informe_en_bodeguero, inicializar_directorio_informes_bodeguero, realizar_movimiento

# Constante para la carpeta de la papelera de productos
PAPELERA_PRODUCTOS_DIR = "papelera_productos"

# Constante para la carpeta de informes de bodeguero
INFORMES_BODEGUERO_DIR = "informes_bodeguero"

# Funciones de utilidad para limpiar pantalla y pausar
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def pausa():
    input("Presione Enter para continuar...")

# Función para imprimir un cuadro de texto
def imprimir_cuadro(titulo, opciones):
    print("+" + "-" * 40 + "+")
    print("|{:^40}|".format(titulo))
    print("+" + "-" * 40 + "+")
    for opcion in opciones:
        print("+" + "-" * 40 + "+")
        print("| {:<38} |".format(opcion))
    print("+" + "-" * 40 + "+")

# Menú principal del sistema
def menu_principal():
    while True:
        limpiar_pantalla()
        opciones = [
            "1. Iniciar Sesión",
            "2. Registrarse",
            "3. Salir"
        ]
        imprimir_cuadro("Bienvenido al Sistema del El Gran Poeta", opciones)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            registrar()
        elif opcion == "3":
            print("Gracias por usar nuestro sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            pausa()

# Función para iniciar sesión en el sistema
def iniciar_sesion():
    limpiar_pantalla()
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")

    user = autenticar_usuario(usuario, contraseña)

    if not user:
        print("Usuario o contraseña incorrecta.")
        pausa()
        return

    if user[4] == "jefe":
        menu_jefe()
    elif user[4] == "bodeguero":
        menu_bodeguero()
    else:
        print("Rol de usuario no reconocido.")
        pausa()

# Función para registrar un nuevo usuario
def registrar():
    limpiar_pantalla()
    print("\n+" + "-" * 40 + "+")
    print("|{:^40}|".format("Registro de Nuevo Usuario"))
    print("+" + "-" * 40 + "+")

    nombre = input("Nombre: ")
    usuario = input("Usuario: ")
    contraseña = getpass.getpass("Contraseña: ")
    confirmar_contraseña = getpass.getpass("Confirmar Contraseña: ")

    if contraseña != confirmar_contraseña:
        print("Las contraseñas no coinciden.")
        pausa()
        return

    opciones_rol = ["1. Jefe", "2. Bodeguero"]
    imprimir_cuadro("Seleccione el rol del usuario", opciones_rol)
    rol_opcion = input("Seleccione una opción: ")
    if rol_opcion == "1":
        rol = "jefe"
    elif rol_opcion == "2":
        rol = "bodeguero"
    else:
        print("Opción no válida.")
        pausa()
        return

    if not (nombre.strip() and usuario.strip() and contraseña.strip() and rol in ["jefe", "bodeguero"]):
        print("Por favor, complete todos los campos y seleccione un rol válido.")
        pausa()
        return

    if crear_usuario(nombre, usuario, contraseña, rol):
        print("Usuario creado correctamente.")
    else:
        print("Error al crear el usuario. Inténtelo de nuevo.")
    pausa()

# Menú para el rol de jefe
def menu_jefe():
    while True:
        limpiar_pantalla()
        opciones = [
            "1. Gestionar Bodegas",
            "2. Gestionar Productos",
            "3. Generar Informe",
            "4. Ver Informes",
            "5. Papelera de Informes",
            "6. Cerrar Sesión"
        ]
        imprimir_cuadro("Menú del Jefe", opciones)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_gestion_bodegas()
        elif opcion == "2":
            menu_gestion_productos()
        elif opcion == "3":
            generar_informe_menu_jefe()
            pausa()
        elif opcion == "4":
            while True:
                limpiar_pantalla()
                listar_informes()
                informe_seleccionado = input("Ingrese el código del informe a ver (0 para salir): ")
                if informe_seleccionado == "0":
                    break
                try:
                    ver_informe(informe_seleccionado)
                    pausa()
                except ValueError:
                    print("Código no válido. Debe ser un número.")
                    pausa()
        elif opcion == "5":
            menu_papelera_informes()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            pausa()

# Función para generar un informe desde el menú del jefe
def generar_informe_menu_jefe():
    nombre = input("Nombre del informe: ")
    cantidad = input("Cantidad de productos: ")
    tipo = input("Tipo de producto: ")
    editorial = input("Editorial: ")
    generar_informe(nombre, cantidad, tipo, editorial)

# Función para el menú de gestión de bodegas
def menu_gestion_bodegas():
    while True:
        limpiar_pantalla()
        opciones = [
            "1. Crear Bodega",
            "2. Bodegas Creadas",
            "3. Papelera de Bodegas",
            "4. Volver al Menú Principal"
        ]
        imprimir_cuadro("Gestión de Bodegas", opciones)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_bodega()
            pausa()
        elif opcion == "2":
            listar_bodegas()
            pausa()
        elif opcion == "3":
            papelera_bodegas()
            pausa()
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            pausa()

# Función para el menú de gestión de productos
def menu_gestion_productos():
    while True:
        limpiar_pantalla()
        opciones = [
            "1. Crear Producto",
            "2. Listar Productos",
            "3. Papelera de Productos",
            "4. Volver al Menú Principal"
        ]
        imprimir_cuadro("Gestión de Productos", opciones)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo_opciones = [
                "1. Libro",
                "2. Revista",
                "3. Enciclopedia"
            ]
            imprimir_cuadro("Seleccione el tipo de producto", tipo_opciones)
            tipo_opcion = input("Seleccione una opción: ")

            if tipo_opcion == "1":
                tipo = "Libro"
            elif tipo_opcion == "2":
                tipo = "Revista"
            elif tipo_opcion == "3":
                tipo = "Enciclopedia"
            else:
                print("Opción no válida.")
                pausa()
                continue

            nombre = input("Nombre del producto: ")
            editorial = input("Editorial: ")
            autores = input("Autores: ")
            descripcion = input("Descripción: ")
            crear_producto(tipo, nombre, editorial, autores, descripcion)
            pausa()

        elif opcion == "2":
            while True:
                limpiar_pantalla()
                listar_productos_en_bodega()
                producto_a_eliminar = input("Ingrese el ID del producto a eliminar (0 para salir): ")
                if producto_a_eliminar == "0":
                    break
                if confirmacion == "S":
                    eliminar_producto(producto_a_eliminar)
                    print(f"Producto {producto_a_eliminar} eliminado correctamente.")
                elif confirmacion == "N":
                    print("Operación cancelada.")
                else:
                    print("Opción no válida. Por favor, seleccione S o N.")
                    pausa()

        elif opcion == "3":
            papelera_productos()
            pausa()

        elif opcion == "4":
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            pausa()

# Menú para el rol de bodeguero
def menu_bodeguero():
    while True:
        limpiar_pantalla()
        opciones = [
            "1. Realizar Movimiento",
            "2. Cerrar Sesión"
        ]
        imprimir_cuadro("Menú del Bodeguero", opciones)

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            realizar_movimiento()
            pausa()

        elif opcion == "2":
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
            pausa()

# Inicialización del sistema
if __name__ == "__main__":
    inicializar_directorio_informes()
    menu_principal()
