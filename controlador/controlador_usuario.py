from bd import obtener_conexion
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def insertar_usuario(nombre, email, contrasena, rol, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')
        cursor.execute("INSERT INTO Usuario (nombre, email, contrasena, rol, estado) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, email, hashed_password, rol, estado))
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

def autenticar_usuario(email, contrasena):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, email, contrasena, rol, estado FROM Usuario WHERE email = %s", (email,))
        usuario = cursor.fetchone()
    conexion.close()

    # Verifica la contraseña si el usuario existe
    if usuario and bcrypt.check_password_hash(usuario[3], contrasena):
        return {
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "rol": usuario[4],
            "estado": usuario[5],
        }
    return None
