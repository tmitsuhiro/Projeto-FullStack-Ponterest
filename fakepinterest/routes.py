from flask import render_template, url_for, redirect, request
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto, Tags, Pasta, SalvarFoto
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto, FormFotoPerfil
from werkzeug.utils import secure_filename
from sqlalchemy.sql.expression import func
from random import shuffle
from wtforms.validators import ValidationError
from secrets import token_hex as th
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


@app.route("/perfil/<username>", methods=["GET", "POST"])
@login_required
def perfil(username):
    usuario_perfil = Usuario.query.filter(Usuario.username==username).first()
    pastas_perfil = Pasta.query.filter(Pasta.id_usuario==current_user.id).all()
    saves = SalvarFoto.query.filter(SalvarFoto.id_usuario==usuario_perfil.id).all()
    fotos_salvas = [save.foto for save in saves]

    if request.method == "POST" and "search" in request.form:
        pesquisa = request.form['search']
        return redirect(url_for('search_mypins', pesquisa=pesquisa))
    
    if request.method == "POST" and "nome_pasta" in request.form:
        nome_pasta = request.form["nome_pasta"]
        nova_pasta = Pasta(id_usuario=current_user.id, titulo=nome_pasta)
        database.session.add(nova_pasta)
        database.session.commit()
    return render_template("perfil.html", usuario=usuario_perfil, pastas=pastas_perfil, fotos_salvas=fotos_salvas)


@app.route("/perfil/<username>/<nome_pasta>", methods=["GET", "POST"])
@login_required
def pasta(username, nome_pasta):
    dono_pasta = Usuario.query.filter(Usuario.username==username).first()
    pasta = Pasta.query.filter(Pasta.titulo==nome_pasta, Pasta.id_usuario==dono_pasta.id).first()
    if nome_pasta == "salvos":
        fotos = dono_pasta.fotos
    else:
        fotos_salvas = SalvarFoto.query.filter(SalvarFoto.pasta_salva==pasta.id, SalvarFoto.id_usuario==dono_pasta.id).all()
        fotos = [foto_salva.foto for foto_salva in fotos_salvas]
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

    dono_post = foto.usuario 
    if request.method == "POST" and "save_pasta" in request.form:
        nome_pasta = request.form['save_pasta']
        pasta = Pasta.query.filter(Pasta.titulo==nome_pasta, Pasta.id_usuario==current_user.id).first()
        salvarfoto = SalvarFoto(id_usuario=current_user.id, foto_salva=foto.id, pasta_salva=pasta.id)
        database.session.add(salvarfoto)
        database.session.commit()
    salvo = SalvarFoto.query.filter(SalvarFoto.id_usuario==current_user.id, SalvarFoto.foto_salva==foto.id).first()
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
        extensao_arquivo = os.path.splitext(arquivo.filename)[1]
        nome_seguro = secure_filename(th(10)+extensao_arquivo)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.config["UPLOAD_FOLDER"],
                                nome_seguro)
        arquivo.save(caminho)
        tags = tag_usuario.tags
        titulo = form_foto.titulo.data
        descricao = form_foto.descricao.data
        foto = Foto(imagem=nome_seguro, id_usuario=current_user.id, tags=tags, titulo=titulo, descricao=descricao)
        database.session.add(foto)
        database.session.commit()
        reset_tag(current_user.id)
        if request.form["pasta"] != "nenhum":
            nome_pasta = request.form["pasta"]
            pasta = Pasta.query.filter(Pasta.titulo==nome_pasta, Pasta.id_usuario==current_user.id).first()
            salvarfoto = SalvarFoto(id_usuario=current_user.id, foto_salva=foto.id, pasta_salva=pasta.id)
            database.session.add(salvarfoto)
            database.session.commit()
        return redirect(url_for('perfil',  username=current_user.username))
    return render_template("criarpost.html", usuario=current_user, form=form_foto, tag_list=None, tag_usuario=tag_usuario)


@app.route("/configuracao", methods=["POST", "GET"])
@login_required
def configuracao():
    form_foto_perfil = FormFotoPerfil()
    nome_pasta = "fotos_perfil"
    if form_foto_perfil.validate_on_submit():
        arquivo = form_foto_perfil.foto.data
        print(arquivo.filename)
        extensao_arquivo = os.path.splitext(arquivo.filename)[1]
        nome_seguro = secure_filename(th(10)+extensao_arquivo)
        caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                app.static_folder, nome_pasta,
                                nome_seguro)
        print(caminho)
        arquivo.save(caminho)
        current_user.foto_perfil = nome_seguro
        database.session.commit()
        return render_template("configuracao.html", usuario=current_user, form=form_foto_perfil)

    # if request.method == "POST" and "mudar_nome_usuario" in request.form:
    #     novo_nome = request.form['mudar_nome_usuario']
    #     current_user.username = novo_nome
    #     database.session.commit()
    #     return render_template("configuracao.html", usuario=current_user, form=form_foto_perfil)

    return render_template("configuracao.html", usuario=current_user, form=form_foto_perfil)

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

@app.route("/teste", methods=["post", "get"])
def teste():
    return render_template('teste.html')