from bd import obtener_conexion

def insertar_equipo(codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Equipo(codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado))
    conexion.commit()
    conexion.close()

def obtener_equipos():
    conexion = obtener_conexion()
    equipos = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT e.id, e.codigo_patrimonial, t.nombre, e.procesador, e.memoria_ram, e.sistema_operativo, s.nombre, e.almacenamiento, e.estado FROM Equipo e INNER JOIN tipoequipo t ON t.id = e.tipo_equipo_id INNER JOIN subarea s ON s.id = e.subarea_id")
        equipos = cursor.fetchall()
    conexion.close()
    return equipos

def eliminar_equipo(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Equipo WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_equipo_por_id(id):
    conexion = obtener_conexion()
    equipo = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado FROM Equipo WHERE id = %s", (id,))
        equipo = cursor.fetchone()
    conexion.close()
    return equipo

def actualizar_equipo(codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Equipo SET codigo_patrimonial = %s, tipo_equipo_id = %s, procesador = %s, memoria_ram = %s, sistema_operativo = %s, subarea_id = %s, almacenamiento = %s, estado = %s WHERE id = %s",
                       (codigo_patrimonial, tipo_equipo_id, procesador, memoria_ram, sistema_operativo, subarea_id, almacenamiento, estado, id))
    conexion.commit()
    conexion.close()
