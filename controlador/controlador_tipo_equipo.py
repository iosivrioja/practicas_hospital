from bd import obtener_conexion

def insertar_tipo_equipo(nombre, descripcion, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipoequipo(nombre, descripcion, estado) VALUES (%s, %s, %s)",
                       (nombre, descripcion, estado))
    conexion.commit()
    conexion.close()

def obtener_tipo_equipos():
    conexion = obtener_conexion()
    tipo_equipos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion, estado FROM tipoequipo")
        tipo_equipos = cursor.fetchall()
    conexion.close()
    return tipo_equipos

def eliminar_tipo_equipo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM tipoequipo WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_tipo_equipo_por_id(id):
    conexion = obtener_conexion()
    tipo_equipo = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, estado FROM tipoequipo WHERE ID = %s", (id,))
        tipo_equipo = cursor.fetchone()
    conexion.close()
    return tipo_equipo

def actualizar_tipo_equipo(nombre, descripcion, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipoequipo SET nombre = %s, descripcion = %s, estado = %s WHERE id = %s",
                       (nombre, descripcion, estado, id))
    conexion.commit()
    conexion.close()

def actualizar_estado_tipo_equipo(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipoequipo SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()
