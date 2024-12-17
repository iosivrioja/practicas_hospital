from bd import obtener_conexion

def insertar_area(nombre, descripcion, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Area(nombre, descripcion, estado) VALUES (%s, %s, %s)",
                       (nombre, descripcion, estado))
    conexion.commit()
    conexion.close()

def obtener_areas():
    conexion = obtener_conexion()
    areas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, estado FROM Area")
        areas = cursor.fetchall()
    conexion.close()
    return areas

def eliminar_area(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Area WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_area_por_id(id):
    conexion = obtener_conexion()
    area = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, estado FROM Area WHERE id = %s", (id,))
        area = cursor.fetchone()
    conexion.close()
    return area

def actualizar_area(nombre, descripcion, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Area SET nombre = %s, descripcion = %s, estado = %s WHERE id = %s",
                       (nombre, descripcion, estado, id))
    conexion.commit()
    conexion.close()

def actualizar_estado_area(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE area SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()
