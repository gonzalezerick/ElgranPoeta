import os
import getpass
from usuarios import  crear_usuario,autenticar_usuario
from productos import crear_producto, listar_productos_en_bodega, papelera_productos, restaurar_producto
from bodegas import listar_bodegas, crear_bodega, papelera_bodegas, restaurar_bodega
from informes import crear_informe,generar_informe, listar_informes, mostrar_informes_en_tabla
from tabulate import tabulate
from movimientos import realizar_movimiento, guardar_informe_en_bodeguero, ver_movimientos

# Constantes para la carpeta de la papelera de productos e informes
PAPELERA_PRODUCTOS_DIR = "papelera_productos"  
PAPELERA_INFORMES_DIR = "papelera_informes"    

# Funciones de utilidad para limpiar pantalla y pausar
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")  
    else:
        os.system("clear")  

def pausa():
    input("Presione Enter para continuar...")  # Pausar y esperar a que el usuario presione Enter

# Función para imprimir un cuadro de texto
def imprimir_cuadro(titulo, opciones):
    print("+" + "-" * 40 + "+")  # Borde superior del cuadro
    print("|{:^40}|".format(titulo))  # Título centrado del cuadro
    print("+" + "-" * 40 + "+")  # Borde medio del cuadro
    for opcion in opciones:
        print("+" + "-" * 40 + "+")  # Borde inferior de cada opción
        print("| {:<38} |".format(opcion))  # Opción alineada a la izquierda dentro del cuadro
    print("+" + "-" * 40 + "+")  # Borde final del cuadro

# Menú principal del sistema
def menu_principal():
    while True:
        limpiar_pantalla()  # Limpiar la pantalla antes de mostrar el menú
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
        menu_jefe()  # Si el usuario es un jefe, mostrar el menú del jefe
    elif user[4] == "bodeguero":
        menu_bodeguero()  # Si el usuario es un bodeguero, mostrar el menú del bodeguero
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

    # Solicitar aceptación de términos y condiciones
    print("\nPor favor, lea y acepte los términos y condiciones:")
    print("1. Los usuarios deben seguir las políticas de uso del sistema.")
    print("2. La información del sistema es confidencial y no debe ser compartida sin autorización.")
    aceptar_terminos = input("¿Acepta los términos y condiciones? (s/n): ")

    if aceptar_terminos.lower() != "s":
        print("Debe aceptar los términos y condiciones para continuar.")
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
            "3. Gestionar Informes",  
            "4. Cerrar Sesión"
        ]
        imprimir_cuadro("Menú del Jefe", opciones)  
        opcion = input("Seleccione una opción: ")  

        if opcion == "1":
            menu_gestion_bodegas()  
        elif opcion == "2":
            menu_gestion_productos() 
        elif opcion == "3":
            menu_gestion_informes()  
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
            "2. Ver Movimientos Realizados",
            "3. Cerrar Sesión"
        ]
        imprimir_cuadro("Menú del Bodeguero", opciones)  

        opcion = input("Seleccione una opción: ")  

        if opcion == "1":
            realizar_movimiento()  
            pausa()  
        elif opcion == "2":
            ver_movimientos()  
            pausa()  
        elif opcion == "3":
            break  
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")  
            pausa()  

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
            "2. Ver Productos",
            "3. Papelera de Productos",
            "4. Volver al Menú Principal"
        ]
        imprimir_cuadro("Gestión de Productos", opciones) 

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            limpiar_pantalla()
            crear_producto()  
            pausa()
        elif opcion == "2":
            limpiar_pantalla()
            listar_productos_en_bodega()  
            pausa()  
        elif opcion == "3":
            limpiar_pantalla()
            papelera_productos()  
            id_producto = input("Ingrese el ID del producto a restaurar (0 para cancelar): ")
            if id_producto != "0":
                restaurar_producto(id_producto)  
            pausa()  
        elif opcion == "4":
            break  
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")  
            pausa()  

# Función para el menú de gestión de informes
def menu_gestion_informes():
    while True:
        limpiar_pantalla() 
        opciones = [
            "1. Crear Informe",
            "2. Ver Informes",
            "3. Volver al Menú Principal"
        ]
        imprimir_cuadro("Gestión de Informes", opciones)

        opcion = input("Seleccione una opción: ")  

        if opcion == "1":
            crear_informe() 
            pausa()  
        elif opcion == "2":
            mostrar_informes_en_tabla()  
            pausa()  
        elif opcion == "3":
            break  
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")  
            pausa()  

# Inicialización del sistema
if __name__ == "__main__":
    menu_principal()  
