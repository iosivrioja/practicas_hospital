class Subarea:
    id = 0
    nombre = ""
    descripcion = ""
    id_area = 0

    def __init__(self, p_id, p_nombre, p_descripcion, p_id_area):
        self.id = p_id
        self.nombre = p_nombre
        self.descripcion = p_descripcion
        self.id_area = p_id_area