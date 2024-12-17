from bd import obtener_conexion

def insertar_tipo_equipo(nombre, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO tipoequipo(nombre, descripcion) VALUES (%s, %s)",
                       (nombre, descripcion))
    conexion.commit()
    conexion.close()

def obtener_tipo_equipos():
    conexion = obtener_conexion()
    tipo_equipos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, descripcion FROM tipoequipo")
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
            "SELECT id, nombre, descripcion FROM tipoequipo WHERE ID = %s", (id,))
        tipo_equipo = cursor.fetchone()
    conexion.close()
    return tipo_equipo

def actualizar_tipo_equipo(nombre, descripcion, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipoequipo SET nombre = %s, descripcion = %s WHERE id = %s",
                       (nombre, descripcion, id))
    conexion.commit()
    conexion.close()

def actualizar_estado_tipo_equipo(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE tipo_equipo SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()
