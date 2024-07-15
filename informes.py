import os  
from tabulate import tabulate  # Importa la función tabulate para formatear tablas

# Define los directorios para guardar informes y la papelera de informes
INFORMES_DIR = "informes"
PAPELERA_DIR = "papelera_informes"

# Función para inicializar los directorios de informes y papelera
def inicializar_directorio_informes():
    os.makedirs(INFORMES_DIR, exist_ok=True)  # Crea el directorio de informes si no existe
    os.makedirs(PAPELERA_DIR, exist_ok=True)  # Crea el directorio de la papelera si no existe

next_informe_id = 1  # ID inicial para los informes
informes_creados = []  

# Función para crear un nuevo informe
def crear_informe():
    nombre = input("Ingrese el nombre del informe: ")  
    cantidad = input("Ingrese la cantidad de Producto: ")  
    tipo = input("Ingrese el tipo del producto ") 
    editorial = input("Ingrese la editorial del producto: ")  

    # Lógica para crear el informe con los datos proporcionados
    informe = generar_informe(nombre, cantidad, tipo, editorial) 
    informes_creados.append(informe) 
    return informe  

# Función para generar un informe con los datos proporcionados
def generar_informe(nombre, cantidad, tipo, editorial):
    global next_informe_id  
    informe_id = next_informe_id  # Asigna el ID actual al informe
    next_informe_id += 1  # Incrementa el ID para el próximo informe

    # Crea un diccionario con los datos del informe
    informe_data = {
        "ID": informe_id,
        "Nombre": nombre,
        "Cantidad": cantidad,
        "Tipo": tipo,
        "Editorial": editorial
    }
    print(f"Informe generado correctamente con ID: {informe_id}")  # Muestra un mensaje de éxito
    return informe_data  # Devuelve el diccionario del informe

# Función para listar todos los informes creados
def listar_informes():
    return informes_creados 

# Función para mostrar los informes en una tabla
def mostrar_informes_en_tabla():
    limpiar_pantalla()  
    print("\n+" + "-" * 80 + "+")  # Imprime el borde superior de la tabla
    print("|{:^80}|".format("Listado de Informes"))  # Imprime el título de la tabla centrado
    print("+" + "-" * 80 + "+")  # Imprime el borde inferior del título

    informes = listar_informes() 

    if not informes:  
        print("No hay informes creados.") 
    else:
        headers = ["ID", "Nombre", "Cantidad", "Tipo", "Editorial"] 
       
        rows = [[informe["ID"], informe["Nombre"], informe["Cantidad"], informe["Tipo"], informe["Editorial"]] for informe in informes]
        print(tabulate(rows, headers=headers, tablefmt="pretty")) 


def limpiar_pantalla():
    if os.name == "nt":  #Si el sistema operativo es Windows
        os.system("cls")  # Usa el comando cls para limpiar la pantalla
    else:  # Si el sistema operativo es Unix/Linux/Mac
        os.system("clear")  # Usa el comando clear para limpiar la pantalla


if __name__ == "__main__":
    inicializar_directorio_informes()  # Inicializa los directorios de informes y papelera
