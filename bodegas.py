from db import connect
import random

def generar_codigo_unico():
    numeros_unicos = random.sample(range(1, 101), 6)
    codigo = ''.join(map(str, numeros_unicos))
    return codigo 

def crear_bodega(nombre):
    codigo = generar_codigo_unico()
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bodegas (nombre, codigo) VALUES (%s, %s)', (nombre, codigo))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Bodega '{nombre}' creada con el código '{codigo}'.")
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_bodegas():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bodegas WHERE eliminado = 1')
        bodegas_eliminadas = cursor.fetchall()
        if bodegas_eliminadas:
            print("\n--- Papelera de Bodegas ---")
            for bodega in bodegas_eliminadas:
                print(f"ID: {bodega[0]}, Nombre: {bodega[1]}")
        else:
            print("No hay bodegas eliminadas en la papelera.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def mover_a_papelera_bodega(id_bodega):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM productos WHERE bodega_id = %s AND eliminado = 0', (id_bodega,))
        if cursor.fetchone()[0] > 0:
            print("No se puede mover la bodega a la papelera porque tiene productos.")
        else:
            cursor.execute('UPDATE bodegas SET eliminado = 1 WHERE id = %s', (id_bodega,))
            conn.commit()
            print(f"Bodega con ID '{id_bodega}' movida a la papelera.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_bodega(id_bodega):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE bodegas SET eliminado = 0 WHERE id = %s', (id_bodega,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Bodega con ID '{id_bodega}' restaurada.")
    else:
        print("No se pudo conectar a la base de datos.")
