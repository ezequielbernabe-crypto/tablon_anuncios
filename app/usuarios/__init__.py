
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Usuario
from app.extensions import db, bcrypt

usuarios = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios.route("/")
def lista_usuarios():
    lista = Usuario.query.all()
    return render_template("usuarios/lista.html", usuarios=lista)


@usuarios.route("/crear", methods=["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        existente = Usuario.query.filter_by(correo=correo).first()

        if existente:
            flash("El correo ya está registrado.")
            return redirect(url_for("usuarios.crear_usuario"))

        password_cifrada = bcrypt.generate_password_hash(password).decode("utf-8")

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password=password_cifrada
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente.")
        return redirect(url_for("usuarios.lista_usuarios"))

    return render_template("usuarios/crear.html")


@usuarios.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == "POST":
        usuario.nombre = request.form["nombre"]
        usuario.correo = request.form["correo"]

        password = request.form["password"]

        if password:
            usuario.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.commit()

        flash("Usuario actualizado correctamente.")
        return redirect(url_for("usuarios.lista_usuarios"))

    return render_template("usuarios/editar.html", usuario=usuario)


@usuarios.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)
    db.session.commit()

    flash("Usuario eliminado correctamente.")
    return redirect(url_for("usuarios.lista_usuarios"))
