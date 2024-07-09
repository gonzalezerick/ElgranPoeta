import os

# Constante para la carpeta de informes de bodeguero
INFORMES_BODEGUERO_DIR = "informes_bodeguero"


# Función para guardar un informe en la carpeta del bodeguero
def guardar_informe_en_bodeguero(nombre_informe, contenido):
    ruta_informe = os.path.join(INFORMES_BODEGUERO_DIR, f"{nombre_informe}.txt")
    with open(ruta_informe, "w") as file:
        file.write(contenido)
    print(f"Informe '{nombre_informe}' guardado en '{ruta_informe}'.")


# Inicialización del directorio de informes de bodeguero
def inicializar_directorio_informes_bodeguero():
    if not os.path.exists(INFORMES_BODEGUERO_DIR):
        os.makedirs(INFORMES_BODEGUERO_DIR)
        print(f"Directorio '{INFORMES_BODEGUERO_DIR}' creado correctamente.")
    else:
        print(f"Directorio '{INFORMES_BODEGUERO_DIR}' ya existe.")




# Función para realizar un movimiento entre bodegas
def realizar_movimiento():
    bodega_origen = input("Ingrese la bodega de origen: ")
    bodega_destino = input("Ingrese la bodega de destino: ")

    id_producto = input("Ingrese el ID del producto a mover (0 para cancelar): ")
    if id_producto == "0":
        return  # Cancelar operación si se ingresa "0"

    cantidad = input("Ingrese la cantidad a mover: ")

    generar_informe_movimiento(bodega_origen, bodega_destino, id_producto, cantidad)

    guardar_informe_en_bodeguero(f"Informe_Movimiento_{bodega_origen}_{bodega_destino}_{id_producto}", f"Información detallada del movimiento.")

    print(f"Producto con ID '{id_producto}' movido de '{bodega_origen}' a '{bodega_destino}'.")
    pausa()

    # Funciones de utilidad para limpiar pantalla y pausar
def limpiar_pantalla():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def pausa():
    input("Presione Enter para continuar...")



# Llamada a la función de inicialización
inicializar_directorio_informes_bodeguero()
