from fakepinterest import database as db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    foto_perfil = db.Column(db.String, default="vazio")
    fotos = db.relationship("Foto", backref="usuario", lazy=True)
    salvos = db.relationship("SalvarFoto", backref="usuario", lazy=True)
    pastas = db.relationship("Pasta", backref="usuario", lazy=True)
  

class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String, default="default.png")
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String)
    descricao = db.Column(db.Text)
    tags = db.Column(db.String)
    salvos = db.relationship("SalvarFoto", backref="foto", lazy=True)


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tags = db.Column(db.String, default='')


class SalvarFoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    foto_salva = db.Column(db.Integer, db.ForeignKey('foto.id'), nullable=False)
    pasta_salva = db.Column(db.Integer, db.ForeignKey('pasta.id'))


class Pasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    titulo = db.Column(db.String)
    fotos_salvas = db.relationship("SalvarFoto", backref="pasta", lazy=True )


