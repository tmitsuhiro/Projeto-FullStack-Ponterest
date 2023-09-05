from flask import render_template, url_for, redirect, request
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto, Tags, Pasta, SavePin
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func
from random import shuffle
from wtforms.validators import ValidationError
import os



def reset_tag(id):
    tag_usuario = Tags.query.filter_by(id_usuario=id).first()
    tag_usuario.tags = ""
    database.session.commit()

def get_foto(salvo):
    foto = Foto.query.filter(Foto.imagem==salvo.foto_imagem).first()
    return foto


@app.route("/", methods=['GET', 'POST'])
def homepage():
    form_login = FormLogin()
    form_cadastro = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_confirmacao' in request.form: 
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('feed', id_usuario=current_user.id))
        
        elif usuario and not bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            return render_template('homepage.html', form_login=form_login, form_cadastro=form_cadastro, erro="login", erro_senha="senha invalida")

    if form_login.errors and 'botao_confirmacao' in request.form:
        return render_template('homepage.html', form_login=form_login, form_cadastro=form_cadastro, erro="login")
    
    if form_cadastro.validate_on_submit() and 'botao_confirmacao2' in request.form:
        senha = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(username=form_cadastro.username.data, 
                          senha=senha, email=form_cadastro.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('feed', id_usuario=current_user.id))

    if form_cadastro.errors and 'botao_confirmacao' in request.form:
        return render_template('homepage.html', form_login=form_login, form_cadastro=form_cadastro, erro="cadastro")

    return render_template('homepage.html', form_login=form_login, form_cadastro=form_cadastro)



@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    form_cadastro = FormCriarConta()
    if form_cadastro.validate_on_submit() and 'botao_confirmacao2' in request.form:
        senha = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(username=form_cadastro.username.data, 
                          senha=senha, email=form_cadastro.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('homepage'))
    
    return render_template('cadastro.html', form_cadastro=form_cadastro)


@app.route("/perfil/<username>", methods=["GET", "POST"])
@login_required
def perfil(username):
    if username == current_user.username:
        pastas = Pasta.query.filter(Pasta.id_usuario==current_user.id).all()

        if request.method == "POST" and "search" in request.form:
            pesquisa = request.form['search']
            return redirect(url_for('search_mypins', pesquisa=pesquisa))
        
        if request.method == "POST" and "nome_pasta" in request.form:
            nome_pasta = request.form["nome_pasta"]
            nova_pasta = Pasta(id_usuario=current_user.id, titulo=nome_pasta)
            database.session.add(nova_pasta)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, usuario_visitado=None, pastas=pastas)
    
    else:
        usuario_visitado = Usuario.query.filter(Usuario.username==username).first()
        pastas = Pasta.query.filter(Pasta.id_usuario==usuario_visitado.id).all()
        return render_template("perfil.html", usuario=current_user, usuario_visitado=usuario_visitado, pastas=pastas)


@app.route("/perfil/<username>/<nome_pasta>", methods=["GET", "POST"])
@login_required
def pasta(username, nome_pasta):
    if username == current_user.username:
        fotos_salvas = Pasta.query.filter(Pasta.titulo==nome_pasta, Pasta.id_usuario==current_user.id).first().fotos_salvas
        fotos = list(map(get_foto, fotos_salvas))
        return render_template("pasta.html", usuario=current_user, fotos=fotos)
    else:
        return render_template("pasta.html", usuario=current_user, fotos=fotos)



@app.route('/feed', methods=["GET", "POST"])
@login_required
def feed():
    usuario = current_user
    if request.method == "POST":
        pesquisa = request.form['search']
        return redirect(url_for("search", pesquisa=pesquisa, usuario=usuario))
    
    fotos = Foto.query.order_by(func.random()).all()
    return render_template("feed.html", fotos=fotos, usuario=usuario)


@app.route('/search/<pesquisa>', methods=["GET", "POST"])
@login_required
def search(pesquisa):
    usuario = current_user
    fotos_pesquisa = Foto.query.filter(Foto.tags.like("%{}%".format(pesquisa))).order_by(func.random()).all()
    return render_template("feed.html", fotos=fotos_pesquisa, usuario=usuario)


@app.route('/search/my_pins/<pesquisa>', methods=["GET", "POST"])
@login_required
def search_mypins(pesquisa):
    usuario = current_user
    fotos_pesquisa = Foto.query.filter(Foto.tags.like("%{}%".format(pesquisa)), Foto.id_usuario==current_user.id).all()
    return render_template("feed.html", fotos=fotos_pesquisa, usuario=usuario)


@app.route("/post/<id_foto>", methods=["GET", "POST"])
@login_required 
def post(id_foto):
    usuario = current_user
    foto = Foto.query.get(int(id_foto))
    if request.method == "POST" and "search" in request.form:
        pesquisa = request.form['search']
        return redirect(url_for("search", pesquisa=pesquisa, usuario=usuario))
    tags = foto.tags.split('#')[1:]
    fotos_relacionados = []
    for tag in tags:
        fotos = Foto.query.filter(Foto.tags.like("%{}%".format(tag)), Foto.id!=id_foto).all()
        for i in fotos:
            fotos_relacionados.append(i)

    fotos_relacionados = list(set(fotos_relacionados))
    shuffle(fotos_relacionados)

    dono_post = Usuario.query.get(int(foto.id_usuario)) 
    if request.method == "POST" and "save_pasta" in request.form:
        nome_pasta = request.form['save_pasta']
        pasta = Pasta.query.filter(Pasta.titulo==nome_pasta, Pasta.id_usuario==current_user.id).first()
        savepin = SavePin(id_usuario=current_user.id, foto_imagem=foto.imagem, pasta_salva=pasta.id)
        database.session.add(savepin)
        database.session.commit()
    salvo = SavePin.query.filter(SavePin.id_usuario==current_user.id, SavePin.foto_imagem==foto.imagem).first()
    return render_template("post.html", usuario=usuario, foto=foto, dono_post=dono_post, fotos_relacionados=fotos_relacionados, salvo=salvo)


@app.route("/criar_post", methods=["GET", "POST"])
@login_required 
def criar_post():
    if request.method == "POST" and "search" in request.form:
        pesquisa = request.form['search']
        return redirect(url_for("search", pesquisa=pesquisa, usuario=current_user))
    
    tag_usuario = Tags.query.filter_by(id_usuario=current_user.id).first()
    form_foto = FormFoto()
    if form_foto.validate_on_submit():
        arquivo = form_foto.foto.data
        nome_seguro = secure_filename(arquivo.filename)
        # salvar o arquivo dentro da pasta certa
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"],
                                nome_seguro)
        arquivo.save(caminho)
        tags = tag_usuario.tags
        titulo = form_foto.titulo.data
        descricao = form_foto.descricao.data
        # criar a foto no banco com o item "imagem" sendo o nome do arqivo
        foto = Foto(imagem=nome_seguro, id_usuario=current_user.id, tags=tags, titulo=titulo, descricao=descricao)
        database.session.add(foto)
        database.session.commit()
        reset_tag(current_user.id)
        return redirect(url_for('perfil',  username=current_user.username))
    return render_template("criarpost.html", usuario=current_user, form=form_foto, tag_list=None, tag_usuario=tag_usuario)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route("/tag_manager", methods=["post", "get"])
@login_required
def tag_manager():
    tag_usuario = Tags.query.filter_by(id_usuario=current_user.id).first()
    if not tag_usuario:
        new_tags = Tags(id_usuario=current_user.id)
        database.session.add(new_tags)
        database.session.commit()

    if request.method == "POST" and "tag" in request.form and request.form["tag"] != "":
        tag = request.form["tag"]  
        if tag not in tag_usuario.tags.split("#"):
            tag_usuario.tags = tag_usuario.tags + "#" + tag 
            database.session.commit()
        tag_list = tag_usuario.tags.split("#")
        return render_template("tag_manager.html", usuario=current_user, tag_list=tag_list)
    if request.method == "POST" and "delete" in request.form:
        delete_tag = request.form["delete"] 
        tag_usuario.tags = tag_usuario.tags.replace(f'#{delete_tag}', '')
        database.session.commit()
        tag_list = tag_usuario.tags.split("#")
        return render_template("tag_manager.html", usuario=current_user, tag_list=tag_list)
    return render_template("tag_manager.html", usuario=current_user)

@app.route("/teste")
def teste():
    pass