import os
import mysql.connector
from mysql.connector import Error
import uuid
from db import connect

# Función para generar un código único
def generate_unique_code():
    return str(uuid.uuid4().hex)[:10]  # Generar un código único de 10 caracteres

# Función para listar bodegas activas
def listar_bodegas():
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, direccion FROM bodegas WHERE eliminado = 0')
            bodegas = cursor.fetchall()
            if bodegas:
                print("\n--- Bodegas Creadas ---")
                print("+" + "-" * 65 + "+")
                print("| {:<5} | {:<30} | {:<30} |".format("ID", "Nombre", "Dirección"))
                print("+" + "-" * 65 + "+")
                for bodega in bodegas:
                    print("| {:<5} | {:<30} | {:<30} |".format(bodega[0], bodega[1], bodega[2]))
                print("+" + "-" * 65 + "+")

                eliminar = input("¿Desea eliminar alguna bodega? (S/N): ")
                if eliminar.upper() == 'S':
                    id_bodega = input("Ingrese el ID de la bodega a eliminar: ")
                    mover_bodega_a_papelera(id_bodega)

            else:
                print("No hay bodegas activas.")
            cursor.close()
            conn.close()
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al listar bodegas: {str(e)}")

# Función para crear una nueva bodega
def crear_bodega():
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()

            nombre = input("Nombre de la nueva bodega: ").strip()
            direccion = input("Dirección de la nueva bodega: ").strip()

            if not nombre or not direccion:
                print("Error: Todos los campos son obligatorios. Por favor, complete todos los campos.")
                return

            # Generar código único
            codigo = generate_unique_code()

            # Insertar nueva bodega
            cursor.execute('INSERT INTO bodegas (nombre, codigo, direccion, eliminado) VALUES (%s, %s, %s, 0)',
                           (nombre, codigo, direccion))
            conn.commit()
            cursor.close()
            conn.close()
            print("Bodega creada correctamente.")
        else:
            print("No se pudo conectar a la base de datos.")
    except mysql.connector.Error as error:
        print(f"Error al crear bodega: {error}")
    except Exception as e:
        print(f"Error general al crear bodega: {str(e)}")

# Función para mover bodega a la papelera
def mover_bodega_a_papelera(id_bodega):
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('UPDATE bodegas SET eliminado = 1 WHERE id = %s', (id_bodega,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Bodega con ID '{id_bodega}' movida a la papelera correctamente.")
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al mover bodega a papelera: {str(e)}")

# Función para listar bodegas en la papelera
def papelera_bodegas():
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, direccion FROM bodegas WHERE eliminado = 1')
            bodegas = cursor.fetchall()
            if bodegas:
                print("\n--- Bodegas en Papelera ---")
                print("+" + "-" * 65 + "+")
                print("| {:<5} | {:<30} | {:<30} |".format("ID", "Nombre", "Dirección"))
                print("+" + "-" * 65 + "+")
                for bodega in bodegas:
                    print("| {:<5} | {:<30} | {:<30} |".format(bodega[0], bodega[1], bodega[2]))
                print("+" + "-" * 65 + "+")

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
        print(f"Error al listar bodegas en papelera: {str(e)}")

# Función para restaurar una bodega desde la papelera
def restaurar_bodega(id_bodega):
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Bodega con ID '{id_bodega}' restaurada correctamente desde la papelera.")
        else:
            print("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"Error al restaurar la bodega desde la papelera: {str(e)}")

if __name__ == "__main__":
    listar_bodegas()
    crear_bodega()
    papelera_bodegas()

