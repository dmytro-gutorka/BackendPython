from flask import Flask
from app.models import db
from flask_migrate import Migrate
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/')
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates/')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_app():
	app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=UPLOAD_FOLDER)
	app.secret_key = '0000'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

	db.init_app(app)

	migrate = Migrate(app, db)

	from . import auth
	from . import main

	app.register_blueprint(auth.bp)
	app.register_blueprint(main.bp)

	return app