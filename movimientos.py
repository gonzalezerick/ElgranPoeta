from db import connect
from datetime import datetime

def registrar_movimiento(bodega_origen, bodega_destino, productos, cantidades, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movimientos (bodega_origen, bodega_destino, productos, cantidades, usuario, fecha) VALUES (%s, %s, %s, %s, %s, %s)',
                       (bodega_origen, bodega_destino, productos, cantidades, usuario, fecha))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Movimiento registrado con éxito de '{bodega_origen}' a '{bodega_destino}'.")
    else:
        print("No se pudo conectar a la base de datos.")

def papelera_movimientos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos WHERE eliminado = 1')
        movimientos_eliminados = cursor.fetchall()
        if movimientos_eliminados:
            print("\n--- Papelera de Movimientos ---")
            for movimiento in movimientos_eliminados:
                print(f"ID: {movimiento[0]}, Origen: {movimiento[1]}, Destino: {movimiento[2]}, Productos: {movimiento[3]}, Cantidades: {movimiento[4]}, Usuario: {movimiento[5]}, Fecha: {movimiento[6]}")
        else:
            print("No hay movimientos eliminados en la papelera.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

def mover_a_papelera_movimiento(id_movimiento):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE movimientos SET eliminado = 1 WHERE id = %s', (id_movimiento,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Movimiento con ID '{id_movimiento}' movido a la papelera.")
    else:
        print("No se pudo conectar a la base de datos.")

def restaurar_movimiento(id_movimiento):
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('UPDATE movimientos SET eliminado = 0 WHERE id = %s', (id_movimiento,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Movimiento con ID '{id_movimiento}' restaurado.")
    else:
        print("No se pudo conectar a la base de datos.")

def listar_movimientos():
    conn = connect()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos WHERE eliminado = 0')
        movimientos = cursor.fetchall()
        if movimientos:
            print("\n--- Movimientos Realizados ---")
            for movimiento in movimientos:
                print(f"ID: {movimiento[0]}, Origen: {movimiento[1]}, Destino: {movimiento[2]}, Productos: {movimiento[3]}, Cantidades: {movimiento[4]}, Usuario: {movimiento[5]}, Fecha: {movimiento[6]}")
        else:
            print("No hay movimientos registrados.")
        cursor.close()
        conn.close()
    else:
        print("No se pudo conectar a la base de datos.")

if __name__ == "__main__":
    listar_movimientos()