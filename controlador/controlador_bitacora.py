from bd import obtener_conexion

def registrar_bitacora(usuario_id, accion, tabla, descripcion=None):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO bitacora (usuario_id, accion, tabla, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, accion, tabla, descripcion))
    conexion.commit()
    conexion.close()

def obtener_bitacora():
    conexion = obtener_conexion()
    registros = []
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT b.id, u.nombre AS usuario, b.accion, b.tabla, b.fecha, b.descripcion
            FROM bitacora b
            JOIN Usuario u ON b.usuario_id = u.id
            ORDER BY b.fecha DESC
        """)
        registros = cursor.fetchall()
    conexion.close()
    return registros

