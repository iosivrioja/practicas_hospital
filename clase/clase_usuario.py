class Usuario:
    id = 0
    nombre = ""
    email = ""
    rol = ""
    estado = ""

    def __init__(self, p_id, p_nombre, p_email, p_rol, p_estado):
        self.id = p_id
        self.nombre = p_nombre
        self.email = p_email
        self.rol = p_rol
        self.estado = p_estado
