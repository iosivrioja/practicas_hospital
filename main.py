from flask import Flask, render_template, request, redirect, jsonify, session

import controlador.controlador_area as controlador_area
import controlador.controlador_tipo_equipo as controlador_tipo_equipo
import controlador.controlador_subarea as controlador_subarea
import controlador.controlador_equipo as controlador_equipo
import controlador.controlador_parte as controlador_parte
import controlador.controlador_agente as controlador_agente
import controlador.controlador_usuario as controlador_usuario
from controlador.controlador_bitacora import obtener_bitacora

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        usuario = controlador_usuario.autenticar_usuario(email, contrasena)

        if usuario:
            # Guarda el ID del usuario en la sesión
            session['usuario_id'] = usuario['id']
            session['nombre_usuario'] = usuario['nombre']  # Opcional: Guarda el nombre
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Credenciales inválidas')
    else:
        return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    return render_template("maestra.html", titulo="Dashboard")

@app.route("/maestra")
def maestra():
    return render_template("maestra.html")

@app.route("/bitacora")
def bitacora():
    registros = obtener_bitacora()
    return render_template("bitacora.html", bitacora=registros)


@app.route("/agregar_area")
def formulario_agregar_area():
    return render_template("agregar_area.html")

@app.route("/guardar_area", methods=["POST"])
def guardar_area():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'

    usuario_id = session.get('usuario_id')  # Obtén el ID del usuario desde la sesión

    if usuario_id:  # Asegúrate de que el usuario esté autenticado
        controlador_area.insertar_area(nombre, descripcion, estado, usuario_id)
    else:
        return redirect('/login')  # Redirige si no hay usuario autenticado

    return redirect("/areas")


@app.route("/areas")
def areas():
    areas = controlador_area.obtener_areas()
    return render_template("area.html", areas=areas)

@app.route("/eliminar_area", methods=["POST"])
def eliminar_area():
    controlador_area.eliminar_area(request.form["id"])
    return redirect("/areas")

@app.route("/formulario_editar_area/<int:id>")
def editar_area(id):
    area = controlador_area.obtener_area_por_id(id)
    return render_template("editar_area.html", area=area)

@app.route("/actualizar_area", methods=["POST"])
def actualizar_area():
    id_area = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_area.actualizar_area(nombre, descripcion, estado, id_area)
    return redirect("/areas")

@app.route("/cambiar_estado_area", methods=["POST"])
def cambiar_estado_area():
    id_area = request.form["id"]
    nuevo_estado = request.form["estado"]
    controlador_area.actualizar_estado_area(id_area, nuevo_estado)
    return redirect("/areas")

@app.route("/agregar_tipo_equipo")
def formulario_agregar_tipo_equipo():
    return render_template("agregar_tipo_equipo.html")

@app.route("/guardar_tipo_equipo", methods=["POST"])
def guardar_tipo_equipo():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_tipo_equipo.insertar_tipo_equipo(nombre, descripcion, estado)
    return redirect("/tipo_equipos")

@app.route("/tipo_equipos")
def tipo_equipos():
    tipo_equipos = controlador_tipo_equipo.obtener_tipo_equipos()
    return render_template("tipo_equipo.html", tipo_equipos=tipo_equipos)

@app.route("/eliminar_tipo_equipo", methods=["POST"])
def eliminar_tipo_equipo():
    controlador_tipo_equipo.eliminar_tipo_equipo(request.form["id"])
    return redirect("/tipo_equipos")

@app.route("/formulario_editar_tipo_equipo/<int:id>")
def editar_tipo_equipo(id):
    tipo_equipo = controlador_tipo_equipo.obtener_tipo_equipo_por_id(id)
    return render_template("editar_tipo_equipo.html", tipoequipo=tipo_equipo)

@app.route("/cambiar_estado_tipo_equipo", methods=["POST"])
def cambiar_estado_tipo_equipo():
    id_tipo_equipo = request.form["id"]
    nuevo_estado = request.form["estado"]
    controlador_tipo_equipo.actualizar_estado_tipo_equipo(id_tipo_equipo, nuevo_estado)
    return redirect("/tipo_equipos")

@app.route("/actualizar_tipo_equipo", methods=["POST"])
def actualizar_tipo_equipo():
    id_tipo_equipo = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_tipo_equipo.actualizar_tipo_equipo(nombre, descripcion, estado, id_tipo_equipo)
    return redirect("/tipo_equipos")

@app.route("/agregar_subarea")
def formulario_agregar_subarea():
    subareas = controlador_subarea.obtener_subareas()
    areas = controlador_area.obtener_areas()
    return render_template("agregar_subarea.html", subareas=subareas, areas=areas)

@app.route("/guardar_subarea", methods=["POST"])
def guardar_subarea():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    id_area = request.form["area_id"]
    controlador_subarea.insertar_subarea(nombre, descripcion, estado, id_area)
    return redirect("/subareas")

@app.route("/subareas")
def subareas():
    subareas = controlador_subarea.obtener_subareas()
    return render_template("subarea.html", subareas=subareas)

@app.route("/eliminar_subarea", methods=["POST"])
def eliminar_subarea():
    controlador_subarea.eliminar_subarea(request.form["id"])
    return redirect("/subareas")

@app.route("/formulario_editar_subarea/<int:id>")
def editar_subarea(id):
    subarea = controlador_subarea.obtener_subarea_por_id(id)
    areas = controlador_area.obtener_areas()
    return render_template("editar_subarea.html", subarea=subarea, areas=areas)

@app.route("/actualizar_subarea", methods=["POST"])
def actualizar_subarea():
    id_subarea = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    id_area = request.form["area_id"]
    controlador_subarea.actualizar_subarea(nombre, descripcion, estado, id_area, id_subarea)
    return redirect("/subareas")

@app.route("/cambiar_estado_subarea", methods=["POST"])
def cambiar_estado_subarea():
    id_subarea = request.form["id"]
    nuevo_estado = request.form["estado"]
    controlador_subarea.actualizar_estado_subarea(id_subarea, nuevo_estado)
    return redirect("/subareas")

@app.route("/agregar_equipo")
def formulario_agregar_equipo():
    tipo_equipos = controlador_tipo_equipo.obtener_tipo_equipos()
    areas = controlador_area.obtener_areas()
    subareas = controlador_subarea.obtener_subareas()
    return render_template("agregar_equipo.html", tipo_equipos=tipo_equipos, areas=areas, subareas=subareas)

@app.route("/guardar_equipo", methods=["POST"])
def guardar_equipo():
    codigo_patrimonial = request.form["codigo_patrimonial"]
    id_tipo_equipo = request.form["tipo_equipo_id"]
    procesador = request.form["procesador"]
    memoria_ram = request.form["memoria_ram"]
    sistema_operativo = request.form["sistema_operativo"]
    id_subarea = request.form["subarea_id"]
    almacenamiento = request.form["almacenamiento"]
    estado = request.form["estado"]
    controlador_equipo.insertar_equipo(codigo_patrimonial, id_tipo_equipo, procesador, memoria_ram, sistema_operativo, id_subarea, almacenamiento, estado)
    return redirect("/equipos")

@app.route("/equipos")
def equipos():
    equipos = controlador_equipo.obtener_equipos()
    return render_template("equipo.html", equipos=equipos)

@app.route("/eliminar_equipo", methods=["POST"])
def eliminar_equipo():
    controlador_equipo.eliminar_equipo(request.form["id"])
    return redirect("/equipos")

@app.route("/formulario_editar_equipo/<int:id>")
def editar_equipo(id):
    equipos = controlador_equipo.obtener_equipo_por_id(id)
    tipo_equipos = controlador_tipo_equipo.obtener_tipo_equipos()
    areas = controlador_area.obtener_areas()
    subareas = controlador_subarea.obtener_subareas()
    return render_template("editar_equipo.html", equipo = equipos, tipo_equipos=tipo_equipos, areas=areas, subareas = subareas)

@app.route("/actualizar_equipo", methods=["POST"])
def actualizar_equipo():
    id_equipo = request.form["id"]
    codigo_patrimonial = request.form["codigo_patrimonial"]
    id_tipo_equipo = request.form["tipo_equipo_id"]
    procesador = request.form["procesador"]
    memoria_ram = request.form["memoria_ram"]
    sistema_operativo = request.form["sistema_operativo"]
    id_subarea = request.form["subarea_id"]
    almacenamiento = request.form["almacenamiento"]
    estado = request.form["estado"]
    controlador_equipo.actualizar_equipo(codigo_patrimonial, id_tipo_equipo, procesador, memoria_ram, sistema_operativo, id_subarea, almacenamiento, estado, id_equipo)
    return redirect("/equipos")

@app.route("/agregar_parte")
def formulario_agregar_parte():
    partes = controlador_parte.obtener_partes()
    equipos = controlador_equipo.obtener_equipos()
    return render_template("agregar_parte.html", partes=partes, equipos=equipos)

@app.route("/guardar_parte", methods=["POST"])
def guardar_parte():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    id_equipo = request.form["equipo_id"]
    controlador_parte.insertar_parte(nombre, descripcion, estado, id_equipo)
    return redirect("/partes")

@app.route("/partes")
def partes():
    partes = controlador_parte.obtener_partes()
    return render_template("parte.html", partes=partes)

@app.route("/eliminar_parte", methods=["POST"])
def eliminar_parte():
    controlador_parte.eliminar_parte(request.form["id"])
    return redirect("/partes")

@app.route("/formulario_editar_parte/<int:id>")
def editar_parte(id):
    parte = controlador_parte.obtener_parte_por_id(id)
    equipos = controlador_equipo.obtener_equipos()
    return render_template("editar_parte.html", parte=parte, equipos=equipos)

@app.route("/actualizar_parte", methods=["POST"])
def actualizar_parte():
    id_parte = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    id_equipo = request.form["equipo_id"]
    controlador_parte.actualizar_parte(nombre, descripcion, id_equipo, id_parte)
    return redirect("/partes")

@app.route("/agregar_agente")
def formulario_agregar_agente():
    return render_template("agregar_agente.html")

@app.route("/guardar_agente", methods=["POST"])
def guardar_agente():
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_agente.insertar_agente(nombre, email, telefono, estado)
    return redirect("/agentes")

@app.route("/agentes")
def agentes():
    agentes = controlador_agente.obtener_agentes()
    return render_template("agente.html", agentes=agentes)

@app.route("/eliminar_agente", methods=["POST"])
def eliminar_agente():
    controlador_agente.eliminar_agente(request.form["id"])
    return redirect("/agentes")

@app.route("/formulario_editar_agente/<int:id>")
def editar_agente(id):
    agente = controlador_agente.obtener_agente_por_id(id)
    return render_template("editar_agentes.html", agente=agente)

@app.route("/actualizar_agente", methods=["POST"])
def actualizar_agente():
    id_agente = request.form["id"]
    nombre = request.form["nombre"]
    email = request.form["email"]
    telefono = request.form["telefono"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_agente.actualizar_agente(nombre, email, telefono, estado, id_agente)
    return redirect("/agentes")

@app.route("/cambiar_estado_agente", methods=["POST"])
def cambiar_estado_agente():
    id_agente = request.form["id"]
    nuevo_estado = request.form["estado"]
    controlador_agente.actualizar_estado_agente(id_agente, nuevo_estado)
    return redirect("/agentes")

# Usuario
@app.route("/agregar_usuario")
def formulario_agregar_usuario():
    return render_template("agregar_usuario.html")

@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    nombre = request.form["nombre"]
    email = request.form["email"]
    rol = request.form["rol"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    # Verificar si el email ya existe
    if controlador_usuario.existe_email(email):
        error = "El correo ya está registrado. Intente con otro."
        return render_template("agregar_usuario.html", error=error)

    # Insertar el usuario si el email no existe
    controlador_usuario.insertar_usuario(nombre, email, rol, estado)
    return redirect("/usuarios")

@app.route("/usuarios")
def usuarios():
    usuarios = controlador_usuario.obtener_usuarios()
    return render_template("usuario.html", usuarios=usuarios)

@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    controlador_usuario.eliminar_usuario(request.form["id"])
    return redirect("/usuarios")

@app.route("/formulario_editar_usuario/<int:id>")
def editar_usuario(id):
    usuario = controlador_usuario.obtener_usuario_por_id(id)
    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/actualizar_usuario", methods=["POST"])
def actualizar_usuario():
    id_usuario = request.form["id"]
    nombre = request.form["nombre"]
    email = request.form["email"]
    rol = request.form["rol"]
    estado = 'Activo' if 'estado' in request.form else 'Inactivo'
    controlador_usuario.actualizar_usuario(nombre, email, rol, estado, id_usuario)
    return redirect("/usuarios")

@app.route("/cambiar_estado_usuario", methods=["POST"])
def cambiar_estado_usuario():
    id_usuario = request.form["id"]
    nuevo_estado = request.form["estado"]
    controlador_usuario.actualizar_estado_usuario(id_usuario, nuevo_estado)
    return redirect("/usuarios")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)