import os
from db import connect

PAPELERA_PRODUCTOS_DIR = "papelera_productos"
PAPELERA_BODEGAS_DIR = "papelera_bodegas"
PAPELERA_INFORMES_DIR = "papelera_informes"

# Función para manejar la papelera
def papelera():
    while True:
        try:
            opciones = [
                "1. Productos Eliminados",
                "2. Bodegas Eliminadas",
                "3. Informes Eliminados",
                "4. Salir"
            ]
            imprimir_opciones("Menú Papelera", opciones)

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                papelera_productos()
            elif opcion == "2":
                papelera_bodegas()
            elif opcion == "3":
                papelera_informes()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")
        except Exception as e:
            print(f"Error en papelera: {str(e)}")

# Función para imprimir las opciones del menú
def imprimir_opciones(titulo, opciones):
    print(f"\n--- {titulo} ---")
    for opcion in opciones:
        print(opcion)

# Función para ver la papelera de productos
def papelera_productos():
    try:
        productos = os.listdir(PAPELERA_PRODUCTOS_DIR)
        if productos:
            print("\n--- Productos Eliminados ---")
            for producto in productos:
                print(producto)
        else:
            print("No hay productos en la papelera.")
    except Exception as e:
        print(f"Error al ver la papelera de productos: {str(e)}")

# Función para ver la papelera de bodegas
def papelera_bodegas():
    try:
        bodegas = os.listdir(PAPELERA_BODEGAS_DIR)
        if bodegas:
            print("\n--- Bodegas Eliminadas ---")
            for bodega in bodegas:
                print(bodega)
        else:
            print("No hay bodegas en la papelera.")
    except Exception as e:
        print(f"Error al ver la papelera de bodegas: {str(e)}")

# Función para ver la papelera de informes
def papelera_informes():
    try:
        informes = os.listdir(PAPELERA_INFORMES_DIR)
        if informes:
            print("\n--- Informes Eliminados ---")
            for informe in informes:
                print(informe)
        else:
            print("No hay informes en la papelera.")
    except Exception as e:
        print(f"Error al ver la papelera de informes: {str(e)}")

