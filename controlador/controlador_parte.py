from bd import obtener_conexion
from controlador.controlador_bitacora import registrar_bitacora

def insertar_parte(nombre, descripcion, estado, equipo_id, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Parte(nombre, descripcion, estado, equipo_id) VALUES (%s, %s, %s, %s)",
                       (nombre, descripcion, estado, equipo_id))
    conexion.commit()
    conexion.close()

    registrar_bitacora(usuario_id, "Añadir", "Parte", f"Se añadió la parte '{nombre}' con estado '{estado}'.")

def obtener_partes():
    conexion = obtener_conexion()
    partes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT p.id, p.nombre, p.descripcion, p.estado, e.codigo_patrimonial FROM Parte p INNER JOIN equipo e ON p.equipo_id = e.id")
        partes = cursor.fetchall()
    conexion.close()
    return partes

def eliminar_parte(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Parte WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_parte_por_id(id):
    conexion = obtener_conexion()
    parte = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, equipo_id FROM Parte WHERE id = %s", (id,))
        parte = cursor.fetchone()
    conexion.close()
    return parte

def actualizar_parte(nombre, descripcion, estado, equipo_id, id, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Parte SET nombre = %s, descripcion = %s, estado = %s, equipo_id = %s WHERE id = %s",
                       (nombre, descripcion, estado, equipo_id, id))
    conexion.commit()
    conexion.close()

    registrar_bitacora(usuario_id, "Actualizar", "Parte", f"Se actualizó la parte '{nombre}'.")

def actualizar_estado_parte(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE parte SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()