from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import Usuario
from fakepinterest import bcrypt


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Entrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Usuário inexistente, cria uma conta')
            
    
    # def validate_senha(self, senha, email):
    #     usuario = Usuario.query.filter_by(email=email.data).first()
    #     senha_valida = bcrypt.check_password_hash(usuario.senha, senha.data)
    #     if not senha_valida:
    #         raise ValidationError('Senha inválida')


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_confirmacao2 = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, faça login para continuar')
    
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome de usuário já cadastrado, escolha outro nome de usuário')


class FormFoto(FlaskForm):
    foto = FileField("Clique para carregar uma foto", validators=[DataRequired()])
    titulo = StringField("Título")
    descricao = TextAreaField("Descrição")
    tags = StringField('Tags')
    botao_confirmacao = SubmitField("Publicar")


class FormFotoPerfil(FlaskForm):
    foto = FileField( validators=[DataRequired()])
    botao_confirmacao = SubmitField("salvar")




    

