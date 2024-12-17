from bd import obtener_conexion

def insertar_agente(nombre, email, telefono, estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO Agente(nombre, email, telefono, estado) VALUES (%s, %s, %s, %s)",
                       (nombre, email, telefono, estado))
    conexion.commit()
    conexion.close()

def obtener_agentes():
    conexion = obtener_conexion()
    agentes = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id, nombre, email, telefono, estado FROM Agente")
        agentes = cursor.fetchall()
    conexion.close()
    return agentes

def eliminar_agente(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM Agente WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()

def obtener_agente_por_id(id):
    conexion = obtener_conexion()
    agente = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, email, telefono, estado FROM Agente WHERE id = %s", (id,))
        agente = cursor.fetchone()
    conexion.close()
    return agente

def actualizar_agente(nombre, email, telefono, estado, id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Agente SET nombre = %s, email = %s, telefono = %s, estado = %s WHERE id = %s",
                       (nombre, email, telefono, estado, id))
    conexion.commit()
    conexion.close()

def actualizar_estado_agente(id, nuevo_estado):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE Agente SET estado = %s WHERE id = %s", (nuevo_estado, id))
    conexion.commit()
    conexion.close()

    