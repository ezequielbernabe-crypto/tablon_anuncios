
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Usuario
from app.extensions import db, bcrypt

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and bcrypt.check_password_hash(usuario.password, password):
            session["usuario_id"] = usuario.id
            session["usuario_nombre"] = usuario.nombre
            return redirect(url_for("main.inicio"))
        else:
            flash("Correo o contraseña incorrectos.")

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for("main.inicio"))
