class Parte:
    id = 0
    nombre = ""
    descripcion = ""
    id_equipo = 0

    def __init__(self, p_id, p_nombre, p_descripcion, p_id_equipo):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.id_equipo = p_id_equipo