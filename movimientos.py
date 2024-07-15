import os
from db import connect
from tabulate import tabulate
# Constante para la carpeta de informes de bodeguero
INFORMES_BODEGUERO_DIR = "informes_bodeguero"

# Inicialización del directorio de informes de bodeguero
def inicializar_directorio_informes_bodeguero():
    if not os.path.exists(INFORMES_BODEGUERO_DIR):
        os.makedirs(INFORMES_BODEGUERO_DIR)
        print(f"Directorio '{INFORMES_BODEGUERO_DIR}' creado correctamente.")
    else:
        print(f"Directorio '{INFORMES_BODEGUERO_DIR}' ya existe.")


#opciones de bodeguero
def realizar_movimiento():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        print("Realizar movimiento:")
        bodega_origen_id = int(input("Ingrese el ID de la bodega de origen: "))
        bodega_destino_id = int(input("Ingrese el ID de la bodega de destino: "))
        productos = input("Ingrese los productos a mover (separados por coma): ")
        cantidades = input("Ingrese las cantidades de cada producto (separadas por coma): ")
        usuario = input("Ingrese el usuario que realiza el movimiento: ")
        
        #Verificar si las bodegas existen
        cursor.execute("SELECT * FROM bodegas WHERE id = %s", (bodega_origen_id,))
        if cursor.fetchone() is None:
            print("La bodega de origen no existe.")
            return
        cursor.execute("SELECT * FROM bodegas WHERE id = %s", (bodega_destino_id,))
        if cursor.fetchone() is None:
            print("La bodega de destino no existe.")
            return
        
        #Realizar movimiento
        cursor.execute("INSERT INTO movimientos (bodega_origen, bodega_destino, productos, cantidades, usuario, fecha) VALUES (%s, %s, %s, %s, %s, NOW())",
                       (bodega_origen_id, bodega_destino_id, productos, cantidades, usuario))
        conn.commit()
        print("Movimiento realizado correctamente.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")


def ver_movimientos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        print("Movimientos realizados:")
        cursor.execute("SELECT id, bodega_origen, bodega_destino, productos, cantidades, usuario, fecha FROM movimientos ORDER BY fecha DESC")
        result = cursor.fetchall()
        headers = ["ID", "Bodega origen", "Bodega destino", "Productos", "Cantidades", "Usuario", "Fecha"]
        table = tabulate(result, headers, tablefmt="pretty")
        print(table)
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")


# Función para guardar un informe en la carpeta del bodeguero
def guardar_informe_en_bodeguero(nombre_informe, contenido):
    ruta_informe = os.path.join(INFORMES_BODEGUERO_DIR, f"{nombre_informe}.txt")
    with open(ruta_informe, "w") as file:
        file.write(contenido)
    print(f"Informe '{nombre_informe}' guardado en '{ruta_informe}'.")

# Llamada a la función de inicialización
inicializar_directorio_informes_bodeguero()
ver_movimientos()
