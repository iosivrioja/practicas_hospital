class Agente:
    id = 0
    nombre = ""
    email = ""
    telefono = ""
    estado = ""

    def __init__(self, p_id, p_nombre, p_email, p_telefono, p_estado):
        self.id = p_id
        self.nombre = p_nombre
        self.email = p_email
        self.telefono = p_telefono
        self.estado = p_estado