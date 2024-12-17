class Equipo:
    id = 0
    codigo_patrimonial = ""
    id_tipo_equipo = 0
    procesador = ""
    memoria_ram = ""
    sistema_operativo = ""
    id_subarea = 0
    almacenamiento = ""
    estado = ""

    def __init__(self, p_id, p_codigo_patrimonial, p_id_tipo_equipo, p_procesador, p_memoria_ram, p_sistema_operativo, p_subarea, p_almacenamiento, p_estado):
        self.id = p_id
        self.codigo_patrimonial = p_codigo_patrimonial
        self.id_tipo_equipo = p_id_tipo_equipo
        self.procesador = p_procesador
        self.memoria_ram = p_memoria_ram
        self.sistema_operativo = p_sistema_operativo
        self.id_subarea = p_subarea
        self.almacenamiento = p_almacenamiento
        self.estado = p_estado