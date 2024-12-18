class TipoEquipo:
    id = 0
    nombre = ""
    descripcion = ""
    estado = ""

    def __init__(self, p_id, p_nombre, p_descripcion, p_estado):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.estado = p_estado