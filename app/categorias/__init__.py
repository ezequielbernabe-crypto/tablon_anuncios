
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Categoria
from app.extensions import db

categorias = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias.route("/")
def lista_categorias():
    lista = Categoria.query.all()
    return render_template("categorias/lista.html", categorias=lista)


@categorias.route("/crear", methods=["GET", "POST"])
def crear_categoria():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        existente = Categoria.query.filter_by(nombre=nombre).first()

        if existente:
            flash("La categoría ya existe.")
            return redirect(url_for("categorias.crear_categoria"))

        nueva = Categoria(nombre=nombre, descripcion=descripcion)

        db.session.add(nueva)
        db.session.commit()

        flash("Categoría registrada correctamente.")
        return redirect(url_for("categorias.lista_categorias"))

    return render_template("categorias/crear.html")


@categorias.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == "POST":
        categoria.nombre = request.form["nombre"]
        categoria.descripcion = request.form["descripcion"]

        db.session.commit()

        flash("Categoría actualizada correctamente.")
        return redirect(url_for("categorias.lista_categorias"))

    return render_template("categorias/editar.html", categoria=categoria)


@categorias.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if categoria.anuncios:
        flash("No se puede eliminar una categoría que tiene anuncios.")
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoría eliminada correctamente.")

    return redirect(url_for("categorias.lista_categorias"))
