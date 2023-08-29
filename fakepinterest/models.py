from fakepinterest import database as db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    fotos = db.relationship("Foto", backref="usuario", lazy=True)


class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String, default="default.png")
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tema = db.Column(db.String)
