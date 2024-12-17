from bd import obtener_conexion

def insertar_parte(nombre, descripcion, equipo_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Parte(nombre, descripcion, equipo_id) VALUES (%s, %s, %s)",
                       (nombre, descripcion, equipo_id))
    conexion.commit()
    conexion.close()

def obtener_partes():
    conexion = obtener_conexion()
    partes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT p.id, p.nombre, p.descripcion, e.codigo_patrimonial FROM Parte p INNER JOIN equipo e ON p.equipo_id = e.id")
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

def actualizar_parte(nombre, descripcion, equipo_id, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Parte SET nombre = %s, descripcion = %s, equipo_id = %s WHERE id = %s",
                       (nombre, descripcion, equipo_id, id))
    conexion.commit()
    conexion.close()
