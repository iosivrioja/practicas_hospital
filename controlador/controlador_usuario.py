from bd import obtener_conexion

def insertar_usuario(nombre, email, rol, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Usuario (nombre, email, rol, estado) VALUES (%s, %s, %s, %s)",
                       (nombre, email, rol, estado))
    conexion.commit()
    conexion.close()

def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, email, rol, estado FROM Usuario")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Usuario WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT Usuario.id, Usuario.nombre, Usuario.email, Usuario.rol, Usuario.estado
            FROM Usuario 
            WHERE Usuario.id = %s
        """, (id,))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario

def actualizar_usuario(nombre, email, rol, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Usuario SET nombre = %s, email = %s, rol = %s, estado = %s WHERE id = %s",
                       (nombre, email, rol, estado, id))
    conexion.commit()
    conexion.close()

def actualizar_estado_usuario(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Usuario SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()

def existe_email(email):
    conexion = obtener_conexion()
    existe = False
    with conexion.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        existe = resultado[0] > 0
    conexion.close()
    return existe
