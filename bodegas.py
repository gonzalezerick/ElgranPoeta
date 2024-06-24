from db import connect
import uuid

def crear_bodega(nombre_bodega):
    if nombre_bodega.strip() == "":
        print("El nombre de la bodega no puede estar vacío.")
        return
    
    codigo_bodega = str(uuid.uuid4())[:8]  

    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO bodegas (nombre, codigo, eliminado) VALUES (%s, %s, 0)', (nombre_bodega, codigo_bodega))
            conn.commit()
            print(f"Bodega '{nombre_bodega}' creada con éxito.")
        except Exception as e:
            conn.rollback()
            print(f"Error al crear la bodega: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def eliminar_bodega(id_bodega):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE bodegas SET eliminado = 1 WHERE id = %s', (id_bodega,))
            conn.commit()
            print("Bodega eliminada correctamente y movida a la papelera.")
        except Exception as e:
            conn.rollback()
            print(f"Error al eliminar la bodega: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_bodega():
    id_bodega = input("Ingrese el ID de la bodega a restaurar: ")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))
            conn.commit()
            print("Bodega restaurada correctamente.")
        except Exception as e:
            conn.rollback()
            print(f"Error al restaurar la bodega: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, nombre FROM bodegas WHERE eliminado = 1')
            bodegas = cursor.fetchall()
            if bodegas:
                print("\n--- Bodegas Eliminadas ---")
                print("+" + "-" * 40 + "+")
                print("| {:<10} | {:<30} |".format("ID", "Nombre"))
                print("+" + "-" * 40 + "+")
                for id, nombre in bodegas:
                    print("| {:<10} | {:<30} |".format(id, nombre))
                print("+" + "-" * 40 + "+")
            else:
                print("No hay bodegas eliminadas.")
        except Exception as e:
            print(f"Error al listar las bodegas eliminadas: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def listar_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id, nombre FROM bodegas WHERE eliminado = 0')
            bodegas = cursor.fetchall()
            if bodegas:
                print("\n--- Bodegas Disponibles ---")
                print("+" + "-" * 40 + "+")
                print("| {:<10} | {:<30} |".format("ID", "Nombre"))
                print("+" + "-" * 40 + "+")
                for id, nombre in bodegas:
                    print("| {:<10} | {:<30} |".format(id, nombre))
                print("+" + "-" * 40 + "+")
            else:
                print("No se encuentran bodegas.")
        except Exception as e:
            print(f"Error al listar las bodegas: {str(e)}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

