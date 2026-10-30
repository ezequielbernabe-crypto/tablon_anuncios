from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Anuncio, Categoria
from app.extensions import db

anuncios = Blueprint("anuncios", __name__, url_prefix="/anuncios")


@anuncios.route("/")
def lista_anuncios():
    lista = Anuncio.query.all()
    return render_template("anuncios/lista.html", anuncios=lista)


@anuncios.route("/crear", methods=["GET", "POST"])
def crear_anuncio():
    if not session.get("usuario_id"):
        flash("Debes iniciar sesión para publicar un anuncio.")
        return redirect(url_for("auth.login"))

    categorias_lista = Categoria.query.all()

    if not categorias_lista:
        flash("Primero debes registrar una categoría.")
        return redirect(url_for("categorias.lista_categorias"))

    if request.method == "POST":
        nuevo = Anuncio(
            titulo=request.form["titulo"],
            descripcion=request.form["descripcion"],
            categoria_id=int(request.form["categoria_id"]),
            usuario_id=session["usuario_id"]
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Anuncio publicado correctamente.")
        return redirect(url_for("anuncios.lista_anuncios"))

    return render_template("anuncios/crear.html", categorias=categorias_lista)


@anuncios.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_anuncio(id):
    if not session.get("usuario_id"):
        flash("Debes iniciar sesión para editar anuncios.")
        return redirect(url_for("auth.login"))

    anuncio = Anuncio.query.get_or_404(id)
    categorias_lista = Categoria.query.all()

    if request.method == "POST":
        anuncio.titulo = request.form["titulo"]
        anuncio.descripcion = request.form["descripcion"]
        anuncio.categoria_id = int(request.form["categoria_id"])

        db.session.commit()

        flash("Anuncio actualizado correctamente.")
        return redirect(url_for("anuncios.lista_anuncios"))

    return render_template(
        "anuncios/editar.html",
        anuncio=anuncio,
        categorias=categorias_lista
    )


@anuncios.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_anuncio(id):
    if not session.get("usuario_id"):
        flash("Debes iniciar sesión para eliminar anuncios.")
        return redirect(url_for("auth.login"))

    anuncio = Anuncio.query.get_or_404(id)

    db.session.delete(anuncio)
    db.session.commit()

    flash("Anuncio eliminado correctamente.")
    return redirect(url_for("anuncios.lista_anuncios"))