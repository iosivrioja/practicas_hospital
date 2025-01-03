from bd import obtener_conexion
from controlador.controlador_bitacora import registrar_bitacora

def insertar_subarea(nombre, descripcion, estado, area_id, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Subarea(nombre, descripcion, estado, area_id) VALUES (%s, %s, %s, %s)",
                       (nombre, descripcion, estado, area_id))
    conexion.commit()
    conexion.close()

    registrar_bitacora(usuario_id, "Añadir", "Subárea", f"Se añadió el subárea '{nombre}' con estado '{estado}'.")

def obtener_subareas():
    conexion = obtener_conexion()
    subareas = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT Subarea.id, Subarea.nombre, Subarea.descripcion, Subarea.estado, Area.nombre FROM Subarea INNER JOIN Area ON Subarea.area_id=Area.id ")
        subareas = cursor.fetchall()
    conexion.close()
    return subareas

def eliminar_subarea(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Subarea WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_subarea_por_id(id):
    conexion = obtener_conexion()
    subarea = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, estado, area_id FROM Subarea WHERE id = %s", (id,))
        subarea = cursor.fetchone()
    conexion.close()
    return subarea

def actualizar_subarea(nombre, descripcion, estado, area_id, id, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Subarea SET nombre = %s, descripcion = %s, estado = %s, area_id = %s WHERE id = %s",
                       (nombre, descripcion, estado, area_id, id))
    conexion.commit()
    conexion.close()

    registrar_bitacora(usuario_id, "Actualizar", "Subárea", f"Se actualizó el subárea '{nombre}'.")

def actualizar_estado_subarea(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE subarea SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()
