import os

INFORMES_DIR = "informes"
PAPELERA_DIR = "papelera_informes"
next_informe_id = 1  
INFORMES_BODEGUERO_DIR = "informes_bodeguero"

def inicializar_directorio_informes():
    global INFORMES_DIR, PAPELERA_DIR
    os.makedirs(INFORMES_DIR, exist_ok=True)
    os.makedirs(PAPELERA_DIR, exist_ok=True)

def generar_informe(nombre, cantidad, tipo, editorial):
    global next_informe_id, INFORMES_DIR
    informe_id = next_informe_id
    next_informe_id += 1
    informe_data = {
        "nombre": nombre,
        "cantidad": cantidad,
        "tipo": tipo,
        "editorial": editorial,
        "estado": "Activo"  # Estado inicial del informe
    }
    try:
        with open(os.path.join(INFORMES_DIR, f"{informe_id}.txt"), "w") as file:
            file.write(f"Nombre: {nombre}\n")
            file.write(f"Cantidad: {cantidad}\n")
            file.write(f"Tipo: {tipo}\n")
            file.write(f"Editorial: {editorial}\n")
        print("Informe generado correctamente.")
    except Exception as e:
        print(f"Error al generar el informe: {str(e)}")

def mover_informe_a_papelera(informe_id):
    global INFORMES_DIR, PAPELERA_DIR
    try:
        original_file = os.path.join(INFORMES_DIR, f"{informe_id}.txt")
        if os.path.exists(original_file):
            os.replace(original_file, os.path.join(PAPELERA_DIR, f"{informe_id}.txt"))
            print(f"Informe {informe_id} movido a la papelera correctamente.")
        else:
            print(f"Informe {informe_id} no encontrado en el directorio de informes.")
    except Exception as e:
        print(f"Error al mover el informe a la papelera: {str(e)}")

def restaurar_informe_papelera(informe_id):
    global INFORMES_DIR, PAPELERA_DIR
    try:
        original_file = os.path.join(INFORMES_DIR, f"{informe_id}.txt")
        if os.path.exists(os.path.join(PAPELERA_DIR, f"{informe_id}.txt")):
            os.replace(os.path.join(PAPELERA_DIR, f"{informe_id}.txt"), original_file)
            print(f"Informe {informe_id} restaurado correctamente.")
            ver_informe(informe_id)
        else:
            print(f"Informe {informe_id} no encontrado en la papelera.")
    except Exception as e:
        print(f"Error al restaurar el informe desde la papelera: {str(e)}")

def ver_informe(informe_id, directorio=INFORMES_DIR):
    global INFORMES_DIR, PAPELERA_DIR
    try:
        with open(os.path.join(directorio, f"{informe_id}.txt"), "r") as file:
            print("\n--- Informe ---")
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print(f"Informe {informe_id} no encontrado.")
    except Exception as e:
        print(f"Error al abrir el informe: {str(e)}")

def listar_informes():
    global INFORMES_DIR, PAPELERA_DIR
    try:
        informes = [f for f in os.listdir(INFORMES_DIR) if f.endswith('.txt')]
        if informes:
            print("\n--- Informes Creados ---")
            for idx, informe_file in enumerate(informes, start=1):
                try:
                    print(f"{idx}. {informe_file}")
                except Exception as e:
                    print(f"Error al leer el archivo {informe_file}: {str(e)}")
            
            while True:
                opcion = input("Ingrese el número del informe a eliminar (0 para salir): ")
                if opcion == '0':
                    break
                try:
                    idx = int(opcion) - 1
                    if 0 <= idx < len(informes):
                        informe_file = informes[idx]
                        informe_id = informe_file.split('.')[0]
                        mover_informe_a_papelera(informe_id)
                    else:
                        print("Opción inválida. Intente de nuevo.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                except Exception as e:
                    print(f"Error al eliminar el informe: {str(e)}")
        else:
            print("No hay informes creados.")
    except Exception as e:
        print(f"Error al listar informes: {str(e)}")

def listar_informes_papelera():
    try:
        informes = os.listdir(PAPELERA_DIR)
        return informes
    except FileNotFoundError:
        print("El directorio de la papelera de informes no existe.")
        return []

def ver_informes_en_papelera():
    try:
        informes = listar_informes_papelera()
        if informes:
            print("\n--- Informes en Papelera ---")
            for idx, informe in enumerate(informes, start=1):
                try:
                    original_id = informe.split('.')[0]
                    original_file = os.path.join(INFORMES_DIR, f"{original_id}.txt")
                    if os.path.exists(original_file):
                        print(f"{idx}. {original_file}")
                    else:
                        print(f"Error: Informe original no encontrado para {informe}")
                except Exception as e:
                    print(f"Error al leer informe en papelera: {str(e)}")
            seleccionar_informe_a_restaurar()
        else:
            print("No hay informes en la papelera.")
    except Exception as e:
        print(f"Error al listar informes en papelera: {str(e)}")

def seleccionar_informe_a_restaurar():
    while True:
        informe_seleccionado = input("Ingrese el número del informe a restaurar (0 para salir): ")
        if informe_seleccionado == "0":
            break
        try:
            idx = int(informe_seleccionado) - 1
            informes = listar_informes_papelera()
            if 0 <= idx < len(informes):
                informe_file = informes[idx]
                informe_id = informe_file.split('.')[0]
                restaurar_informe_papelera(informe_id)
            else:
                print("Número de informe fuera de rango.")
        except ValueError:
            print("Ingrese un número válido.")
        except Exception as e:
            print(f"Error al restaurar informe: {str(e)}")
        input("Presione Enter para continuar...")

def generar_informe_movimiento(bodega_origen, bodega_destino, id_producto, cantidad):
    nombre_informe = f"movimiento_{bodega_origen}_{bodega_destino}_{id_producto}"
    tipo_producto = "Tipo_Producto"  # Reemplaza con la lógica para obtener el tipo de producto
    editorial = "Editorial"  # Reemplaza con la lógica para obtener la editorial
    
    # Contenido del informe
    contenido = f"Nombre del informe: {nombre_informe}\n"
    contenido += f"Bodega de origen: {bodega_origen}\n"
    contenido += f"Bodega de destino: {bodega_destino}\n"
    contenido += f"ID del producto: {id_producto}\n"
    contenido += f"Cantidad: {cantidad}\n"
    contenido += f"Tipo de producto: {tipo_producto}\n"
    contenido += f"Editorial: {editorial}\n"
    
    # Guardar informe en la carpeta del bodeguero
    guardar_informe_en_bodeguero(nombre_informe, contenido)

# Función para listar los informes en la carpeta del bodeguero
def listar_informes_bodeguero():
    print("\n--- Informes en la Carpeta del Bodeguero ---")
    informes = os.listdir(INFORMES_BODEGUERO_DIR)
    if informes:
        for informe in informes:
            print(informe)
    else:
        print("No hay informes en la carpeta del bodeguero.")

# Función para generar un informe de movimiento
def generar_informe_movimiento(bodega_origen, bodega_destino, id_producto, cantidad):
    # Aquí va la lógica para generar el contenido del informe
    contenido = f"Informe de movimiento:\n" \
                f"Bodega de origen: {bodega_origen}\n" \
                f"Bodega de destino: {bodega_destino}\n" \
                f"ID del producto: {id_producto}\n" \
                f"Cantidad: {cantidad}\n"

    # Guardar el informe en el bodeguero
    guardar_informe_en_bodeguero("InformeMovimiento", contenido)

if __name__ == "__main__":
    inicializar_directorio_informes()
