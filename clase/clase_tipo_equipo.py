class TipoEquipo:
    id = 0
    nombre = ""
    descripcion = ""

    def __init__(self, p_id, p_nombre, p_descripcion):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion