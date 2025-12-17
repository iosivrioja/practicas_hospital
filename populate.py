"""
Script para poblar la base de datos con datos de prueba (mock data)
"""

from bd import obtener_conexion
import hashlib
from controlador.controlador_usuario import insertar_usuario
from controlador.controlador_area import insertar_area
from controlador.controlador_subarea import insertar_subarea
from controlador.controlador_tipo_equipo import insertar_tipo_equipo
from controlador.controlador_equipo import insertar_equipo
from controlador.controlador_parte import insertar_parte
from controlador.controlador_agente import insertar_agente


def limpiar_base_datos():
    """Limpia todas las tablas de la base de datos en el orden correcto"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            print("\nLimpiando base de datos...")
            # Deshabilitar verificación de claves foráneas temporalmente
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            # Eliminar datos en orden inverso de dependencias
            cursor.execute("DELETE FROM bitacora")
            print("  ✓ Bitácora limpiada")

            cursor.execute("DELETE FROM Parte")
            print("  ✓ Partes eliminadas")

            cursor.execute("DELETE FROM Equipo")
            print("  ✓ Equipos eliminados")

            cursor.execute("DELETE FROM SubArea")
            print("  ✓ Subáreas eliminadas")

            cursor.execute("DELETE FROM Area")
            print("  ✓ Áreas eliminadas")

            cursor.execute("DELETE FROM TipoEquipo")
            print("  ✓ Tipos de equipo eliminados")

            cursor.execute("DELETE FROM Agente")
            print("  ✓ Agentes eliminados")

            cursor.execute("DELETE FROM Usuario WHERE rol != 'Administrador'")
            print("  ✓ Usuarios no administradores eliminados")

            # Limpiar bitácora de usuarios no administradores
            cursor.execute(
                """
                DELETE FROM bitacora 
                WHERE usuario_id NOT IN (SELECT id FROM Usuario WHERE rol = 'Administrador')
            """
            )

            # Rehabilitar verificación de claves foráneas
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            conexion.commit()
            print("✓ Base de datos limpiada exitosamente\n")
    finally:
        conexion.close()


def crear_usuario_inicial():
    """Crea el primer usuario administrador sin registrar en bitácora"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Verificar si ya existe un usuario administrador
            cursor.execute("SELECT id FROM Usuario WHERE rol = 'Administrador' LIMIT 1")
            admin_existente = cursor.fetchone()

            if admin_existente:
                # Si ya existe un administrador, usar ese
                print("✓ Usuario administrador existente encontrado")
                return admin_existente[0], False
            else:
                # Crear usuario administrador inicial
                hashed_password = hashlib.md5("admin123".encode("utf-8")).hexdigest()
                cursor.execute(
                    "INSERT INTO Usuario (nombre, email, contrasena, rol, estado) VALUES (%s, %s, %s, %s, %s)",
                    (
                        "Administrador",
                        "admin@hospital.com",
                        hashed_password,
                        "Administrador",
                        "Activo",
                    ),
                )
                conexion.commit()
                print("✓ Usuario administrador creado: admin@hospital.com / admin123")
                return cursor.lastrowid, True
    finally:
        conexion.close()


def poblar_usuarios(admin_id):
    """Crea usuarios adicionales"""
    usuarios = [
        (
            "Juan Pérez",
            "juan.perez@hospital.com",
            "password123",
            "Operador",
            "Activo",
        ),
        (
            "María López",
            "maria.lopez@hospital.com",
            "password123",
            "Operador",
            "Activo",
        ),
        (
            "Carlos Ruiz",
            "carlos.ruiz@hospital.com",
            "password123",
            "Operador",
            "Activo",
        ),
        ("Ana García", "ana.garcia@hospital.com", "password123", "Invitado", "Activo"),
        (
            "Pedro Sánchez",
            "pedro.sanchez@hospital.com",
            "password123",
            "Invitado",
            "Inactivo",
        ),
    ]

    print("\nCreando usuarios adicionales...")
    for nombre, email, contrasena, rol, estado in usuarios:
        insertar_usuario(nombre, email, contrasena, rol, estado, admin_id)
        print(f"  ✓ {nombre} - {rol}")


def poblar_areas(usuario_id):
    """Crea áreas del hospital"""
    areas = [
        ("Emergencia", "Área de atención de emergencias médicas", "Activo"),
        ("Consulta Externa", "Área de consultas médicas programadas", "Activo"),
        ("Hospitalización", "Área de internamiento de pacientes", "Activo"),
        ("Quirófano", "Salas de operaciones quirúrgicas", "Activo"),
        ("Laboratorio", "Análisis clínicos y estudios de laboratorio", "Activo"),
        ("Radiología", "Imagenología y estudios radiológicos", "Activo"),
        ("Farmacia", "Dispensación de medicamentos", "Activo"),
        ("Administración", "Oficinas administrativas", "Inactivo"),
    ]

    print("\nCreando áreas...")
    area_ids = []
    for nombre, descripcion, estado in areas:
        insertar_area(nombre, descripcion, estado, usuario_id)
        # Obtener el ID del área recién insertada buscando por nombre
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM Area WHERE nombre = %s", (nombre,))
            area_id = cursor.fetchone()[0]  # type: ignore
            area_ids.append(area_id)
        conexion.close()
        print(f"  ✓ {nombre}")

    return area_ids


def poblar_subareas(usuario_id, area_ids):
    """Crea subáreas asociadas a las áreas"""
    # Suponiendo que tenemos al menos 7 áreas
    subareas = [
        (
            "Triaje",
            "Clasificación de pacientes según gravedad",
            "Activo",
            area_ids[0],
        ),  # Emergencia
        ("Sala de Shock", "Atención de emergencias críticas", "Activo", area_ids[0]),
        (
            "Medicina General",
            "Consultas de medicina general",
            "Activo",
            area_ids[1],
        ),  # Consulta Externa
        ("Pediatría", "Consultas pediátricas", "Activo", area_ids[1]),
        ("Cardiología", "Consultas cardiológicas", "Activo", area_ids[1]),
        (
            "Sala de Hombres",
            "Hospitalización de pacientes masculinos",
            "Activo",
            area_ids[2],
        ),  # Hospitalización
        (
            "Sala de Mujeres",
            "Hospitalización de pacientes femeninas",
            "Activo",
            area_ids[2],
        ),
        ("UCI", "Unidad de Cuidados Intensivos", "Activo", area_ids[2]),
        (
            "Quirófano 1",
            "Sala de operaciones principal",
            "Activo",
            area_ids[3],
        ),  # Quirófano
        ("Quirófano 2", "Sala de operaciones secundaria", "Activo", area_ids[3]),
        (
            "Hematología",
            "Análisis de sangre y derivados",
            "Activo",
            area_ids[4],
        ),  # Laboratorio
        ("Microbiología", "Cultivos y análisis microbiológicos", "Activo", area_ids[4]),
        ("Rayos X", "Radiografías convencionales", "Activo", area_ids[5]),  # Radiología
        ("Tomografía", "Estudios de tomografía computarizada", "Activo", area_ids[5]),
        (
            "Farmacia Central",
            "Almacén principal de medicamentos",
            "Activo",
            area_ids[6],
        ),  # Farmacia
    ]

    print("\nCreando subáreas...")
    subarea_ids = []
    for nombre, descripcion, estado, area_id in subareas:
        insertar_subarea(nombre, descripcion, estado, area_id, usuario_id)
        # Obtener el ID de la subárea recién insertada buscando por nombre y area_id
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM SubArea WHERE nombre = %s AND area_id = %s",
                (nombre, area_id),
            )
            subarea_id = cursor.fetchone()[0]  # type: ignore
            subarea_ids.append(subarea_id)
        conexion.close()
        print(f"  ✓ {nombre}")

    return subarea_ids


def poblar_tipos_equipo(usuario_id):
    """Crea tipos de equipos"""
    tipos = [
        (
            "Computadora de Escritorio",
            "PC de escritorio para uso administrativo y clínico",
            "Activo",
        ),
        ("Laptop", "Computadora portátil", "Activo"),
        ("Impresora", "Impresoras para documentos", "Activo"),
        ("Monitor", "Pantallas de visualización", "Activo"),
        ("Servidor", "Servidores para aplicaciones y bases de datos", "Activo"),
        ("Switch de Red", "Equipos de red y conectividad", "Activo"),
        ("Escáner", "Escáneres de documentos", "Activo"),
        ("UPS", "Sistemas de alimentación ininterrumpida", "Inactivo"),
    ]

    print("\nCreando tipos de equipos...")
    tipo_ids = []
    for nombre, descripcion, estado in tipos:
        insertar_tipo_equipo(nombre, descripcion, estado, usuario_id)
        # Obtener el ID del tipo recién insertado buscando por nombre
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id FROM TipoEquipo WHERE nombre = %s", (nombre,))
            tipo_id = cursor.fetchone()[0]  # type: ignore
            tipo_ids.append(tipo_id)
        conexion.close()
        print(f"  ✓ {nombre}")

    return tipo_ids


def poblar_agentes(usuario_id):
    """Crea agentes de soporte técnico"""
    agentes = [
        ("TechSupport S.A.", "soporte@techsupport.com", "987654321", "Activo"),
        ("Soluciones Informáticas", "contacto@soluciones.com", "987654322", "Activo"),
        ("CompuServ", "info@compuserv.com", "987654323", "Activo"),
        ("IT Solutions", "ventas@itsolutions.com", "987654324", "Activo"),
        ("Hardware Perú", "hardware@peru.com", "987654325", "Inactivo"),
    ]

    print("\nCreando agentes...")
    for nombre, email, telefono, estado in agentes:
        insertar_agente(nombre, email, telefono, estado, usuario_id)
        print(f"  ✓ {nombre}")


def poblar_equipos(usuario_id, tipo_ids, subarea_ids):
    """Crea equipos informáticos"""
    equipos = [
        # Computadoras de escritorio
        (
            "00000000001",
            tipo_ids[0],
            "Intel Core i5-10400",
            "8GB DDR4",
            "Windows 10 Pro",
            subarea_ids[0],
            "500GB SSD",
            "Activo",
        ),
        (
            "00000000002",
            tipo_ids[0],
            "Intel Core i5-10400",
            "8GB DDR4",
            "Windows 10 Pro",
            subarea_ids[1],
            "500GB SSD",
            "Activo",
        ),
        (
            "00000000003",
            tipo_ids[0],
            "Intel Core i7-11700",
            "16GB DDR4",
            "Windows 11 Pro",
            subarea_ids[2],
            "1TB SSD",
            "Activo",
        ),
        (
            "00000000004",
            tipo_ids[0],
            "AMD Ryzen 5 5600",
            "8GB DDR4",
            "Windows 10 Pro",
            subarea_ids[3],
            "500GB HDD",
            "Activo",
        ),
        (
            "00000000005",
            tipo_ids[0],
            "Intel Core i3-10100",
            "4GB DDR4",
            "Windows 10 Pro",
            subarea_ids[4],
            "256GB SSD",
            "Mantenimiento",
        ),
        # Laptops
        (
            "00000000006",
            tipo_ids[1],
            "Intel Core i7-1165G7",
            "16GB DDR4",
            "Windows 11 Pro",
            subarea_ids[5],
            "512GB SSD",
            "Activo",
        ),
        (
            "00000000007",
            tipo_ids[1],
            "AMD Ryzen 7 5800H",
            "16GB DDR4",
            "Windows 11 Pro",
            subarea_ids[6],
            "1TB SSD",
            "Activo",
        ),
        (
            "00000000008",
            tipo_ids[1],
            "Intel Core i5-1135G7",
            "8GB DDR4",
            "Windows 10 Pro",
            subarea_ids[7],
            "512GB SSD",
            "Activo",
        ),
        # Impresoras
        (
            "00000000009",
            tipo_ids[2],
            "N/A",
            "N/A",
            "Firmware 2.1",
            subarea_ids[8],
            "N/A",
            "Activo",
        ),
        (
            "00000000010",
            tipo_ids[2],
            "N/A",
            "N/A",
            "Firmware 3.0",
            subarea_ids[9],
            "N/A",
            "Activo",
        ),
        # Servidores
        (
            "00000000011",
            tipo_ids[4],
            "Intel Xeon Gold 6248",
            "64GB DDR4 ECC",
            "Windows Server 2019",
            subarea_ids[0],
            "2TB RAID 5",
            "Activo",
        ),
        (
            "00000000012",
            tipo_ids[4],
            "AMD EPYC 7542",
            "128GB DDR4 ECC",
            "Ubuntu Server 20.04",
            subarea_ids[0],
            "4TB RAID 10",
            "Activo",
        ),
        # Equipos adicionales
        (
            "00000000013",
            tipo_ids[5],
            "N/A",
            "512MB",
            "N/A",
            subarea_ids[1],
            "N/A",
            "Activo",
        ),
        (
            "00000000014",
            tipo_ids[3],
            "N/A",
            "N/A",
            "N/A",
            subarea_ids[2],
            "N/A",
            "Activo",
        ),
        (
            "00000000015",
            tipo_ids[6],
            "N/A",
            "N/A",
            "Firmware 1.5",
            subarea_ids[3],
            "N/A",
            "Inactivo",
        ),
    ]

    print("\nCreando equipos...")
    equipo_ids = []
    for codigo, tipo_id, proc, ram, so, subarea_id, almac, estado in equipos:
        insertar_equipo(
            codigo, tipo_id, proc, ram, so, subarea_id, almac, estado, usuario_id
        )
        # Obtener el ID del equipo recién insertado buscando por código patrimonial
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM Equipo WHERE codigo_patrimonial = %s", (codigo,)
            )
            equipo_id = cursor.fetchone()[0]  # type: ignore
            equipo_ids.append(equipo_id)
        conexion.close()
        print(f"  ✓ Equipo {codigo}")

    return equipo_ids


def poblar_partes(usuario_id, equipo_ids):
    """Crea partes/componentes de equipos"""
    partes = [
        # Partes del primer equipo (PC de escritorio)
        ("Teclado Logitech K120", "Teclado USB estándar", "Activo", equipo_ids[0]),
        ("Mouse Logitech M90", "Mouse óptico USB", "Activo", equipo_ids[0]),
        ('Monitor Dell 24"', "Monitor LED Full HD", "Activo", equipo_ids[0]),
        # Partes del segundo equipo
        ("Teclado HP KB100", "Teclado USB básico", "Activo", equipo_ids[1]),
        ("Mouse HP X500", "Mouse óptico inalámbrico", "Mantenimiento", equipo_ids[1]),
        # Partes de una laptop
        ("Cargador Original", "Adaptador de corriente 65W", "Activo", equipo_ids[5]),
        ("Mouse Inalámbrico", "Mouse Bluetooth portátil", "Activo", equipo_ids[5]),
        # Partes de impresora
        ("Cartucho Negro HP 664", "Tinta negra original", "Activo", equipo_ids[8]),
        ("Cartucho Color HP 664", "Tinta tricolor original", "Activo", equipo_ids[8]),
        ("Bandeja de Papel", "Bandeja de entrada principal", "Activo", equipo_ids[8]),
        # Partes del servidor
        ("Tarjeta de Red 10Gb", "Intel X550-T2", "Activo", equipo_ids[10]),
        ("Fuente de Poder Redundante", "750W 80+ Platinum", "Activo", equipo_ids[10]),
        ("Batería UPS", "Batería de respaldo 12V 9Ah", "Mantenimiento", equipo_ids[10]),
        # Partes adicionales
        ("Cable HDMI", "Cable HDMI 2.0 de 2m", "Activo", equipo_ids[2]),
        ("Webcam Logitech C270", "Cámara web HD 720p", "Activo", equipo_ids[3]),
    ]

    print("\nCreando partes...")
    for nombre, descripcion, estado, equipo_id in partes:
        insertar_parte(nombre, descripcion, estado, equipo_id, usuario_id)
        print(f"  ✓ {nombre}")


def main():
    """Función principal para poblar la base de datos"""
    print("=" * 60)
    print("POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 60)

    try:
        # 0. Limpiar base de datos
        limpiar_base_datos()

        # 1. Crear usuario administrador inicial
        admin_id, admin_creado = crear_usuario_inicial()

        # 2. Crear usuarios adicionales
        poblar_usuarios(admin_id)

        # 3. Crear áreas
        area_ids = poblar_areas(admin_id)

        # 4. Crear subáreas
        subarea_ids = poblar_subareas(admin_id, area_ids)

        # 5. Crear tipos de equipo
        tipo_ids = poblar_tipos_equipo(admin_id)

        # 6. Crear agentes
        poblar_agentes(admin_id)

        # 7. Crear equipos
        equipo_ids = poblar_equipos(admin_id, tipo_ids, subarea_ids)

        # 8. Crear partes
        poblar_partes(admin_id, equipo_ids)

        print("\n" + "=" * 60)
        print("✓ BASE DE DATOS POBLADA EXITOSAMENTE")
        print("=" * 60)

        # Mostrar credenciales solo si se creó un nuevo administrador
        if admin_creado:
            print("\nCredenciales de acceso:")
            print("  Email: admin@hospital.com")
            print("  Contraseña: admin123")
            print("=" * 60)

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
