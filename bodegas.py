import os
import mysql.connector  
from mysql.connector import Error  
import uuid
from db import connect  

# Función para generar un código único
def generate_unique_code():
    return str(uuid.uuid4().hex)[:10] 

# Función para crear una nueva bodega
def crear_bodega():
    try:
        conn = connect()  # Establece la conexión a la base de datos
        if conn is not None:
            cursor = conn.cursor()  

            # Solicita al usuario el nombre y la dirección de la nueva bodega
            nombre = input("Nombre de la nueva bodega: ").strip()
            direccion = input("Dirección de la nueva bodega: ").strip()

            # Verifica que los campos no estén vacíos
            if not nombre or not direccion:
                print("Error: Todos los campos son obligatorios. Por favor, complete todos los campos.")
                return

            # Genera un código único
            codigo = generate_unique_code()

            # Inserta la nueva bodega en la base de datos
            cursor.execute('INSERT INTO bodegas (nombre, codigo, direccion, eliminado) VALUES (%s, %s, %s, 0)',
                           (nombre, codigo, direccion))
            conn.commit()  
            cursor.close()  
            conn.close()  
            print("Bodega creada correctamente.")
        else:
            print("No se pudo conectar a la base de datos.")
    except mysql.connector.Error as error:
        print(f"Error al crear bodega: {error}")  # Maneja errores específicos de MySQL
    except Exception as e:
        print(f"Error general al crear bodega: {str(e)}")  

# Función para listar bodegas creadas
def listar_bodegas():
    try:
        conn = connect()  # Establece la conexión a la base de datos
        if conn is not None:
            cursor = conn.cursor()  
            cursor.execute('SELECT id, nombre, direccion FROM bodegas WHERE eliminado = 0')  # Consulta las bodegas creadas
            bodegas = cursor.fetchall()  # Obtiene todos los resultados de la consulta
            if bodegas:
                # Imprime la lista de bodegas Creadas
                print("\n--- Bodegas Creadas ---")
                print("+" + "-" * 65 + "+")
                print("| {:<5} | {:<30} | {:<30} |".format("ID", "Nombre", "Dirección"))
                print("+" + "-" * 65 + "+")
                for bodega in bodegas:
                    print("| {:<5} | {:<30} | {:<30} |".format(bodega[0], bodega[1], bodega[2]))
                print("+" + "-" * 65 + "+")

                # Pregunta al usuario si desea eliminar alguna bodega
                eliminar = input("¿Desea eliminar alguna bodega? (S/N): ")
                if eliminar.upper() == 'S':
                    id_bodega = input("Ingrese el ID de la bodega a eliminar: ")
                    mover_bodega_a_papelera(id_bodega)

            else:
                print("No hay bodegas activas.")
            cursor.close()  # Cierra el cursor
            conn.close()  
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al listar bodegas: {str(e)}")  # Maneja errores generales

# Función para ver bodegas en la papelera
def papelera_bodegas():
    try:
        conn = connect()  # Establece la conexión a la base de datos
        if conn is not None:
            cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL
            cursor.execute('SELECT id, nombre, direccion FROM bodegas WHERE eliminado = 1')  # Consulta las bodegas en la papelera
            bodegas = cursor.fetchall()  
            if bodegas:
                # Imprime la lista de bodegas en la papelera
                print("\n--- Bodegas en Papelera ---")
                print("+" + "-" * 65 + "+")
                print("| {:<5} | {:<30} | {:<30} |".format("ID", "Nombre", "Dirección"))
                print("+" + "-" * 65 + "+")
                for bodega in bodegas:
                    print("| {:<5} | {:<30} | {:<30} |".format(bodega[0], bodega[1], bodega[2]))
                print("+" + "-" * 65 + "+")

                # Pregunta al usuario si desea restaurar alguna bodega
                restaurar = input("¿Desea restaurar alguna bodega? (S/N): ")
                if restaurar.upper() == 'S':
                    id_bodega = input("Ingrese el ID de la bodega a restaurar: ")
                    restaurar_bodega(id_bodega)

            else:
                print("No hay bodegas en la papelera.")
            cursor.close()  
            conn.close()  
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al listar bodegas en papelera: {str(e)}")  # Maneja errores generales

# Función para mover bodega a la papelera
def mover_bodega_a_papelera(id_bodega):
    try:
        conn = connect()  
        if conn is not None:
            cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL
            cursor.execute('UPDATE bodegas SET eliminado = 1 WHERE id = %s', (id_bodega,))  # Marca la bodega como eliminada
            conn.commit()  
            cursor.close()  
            conn.close()  
            print(f"Bodega con ID '{id_bodega}' movida a la papelera correctamente.")
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al mover bodega a papelera: {str(e)}") 

# Función para restaurar una bodega desde la papelera
def restaurar_bodega(id_bodega):
    try:
        conn = connect()  # Establece la conexión a la base de datos
        if conn is not None:
            cursor = conn.cursor()  # Crea un cursor para ejecutar consultas SQL
            cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))  # Marca la bodega como activa
            conn.commit()  
            cursor.close()  
            conn.close()  
            print(f"Bodega con ID '{id_bodega}' restaurada correctamente desde la papelera.")
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al restaurar la bodega desde la papelera: {str(e)}")  # Maneja errores generales

# Ejecuta las funciones principales si el script es ejecutado directamente
if __name__ == "__main__":
    listar_bodegas()  # Llama a la función para listar bodegas creadas
    crear_bodega()  # Llama a la función para crear una nueva bodega
    papelera_bodegas()  # Llama a la función para ver bodegas en la papelera
