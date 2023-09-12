from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://banco_ponterest_e0g1_user:9zLR6pEoY9jBHgGeCE6kQVnpULBH6nm2@dpg-cjvs87fhdsdc73a0m4og-a.oregon-postgres.render.com/banco_ponterest_e0g1"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = "11097aa57aae4ca7bd64d5bef4499521"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"
app.static_folder = 'static'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"
   

from fakepinterest import routes