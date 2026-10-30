
from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(30), default="usuario")

    anuncios = db.relationship("Anuncio", backref="usuario", lazy=True)


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)

    anuncios = db.relationship("Anuncio", backref="categoria", lazy=True)


class Anuncio(db.Model):
    __tablename__ = "anuncios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
