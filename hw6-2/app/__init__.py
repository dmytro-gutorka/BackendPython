from flask import Flask
from app.models import db
from flask_migrate import Migrate


def create_app():
	app = Flask(__name__)
	app.secret_key = '0000'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

	db.init_app(app)

	migrate = Migrate(app, db)

	from . import auth
	from . import main

	app.register_blueprint(auth.bp)
	app.register_blueprint(main.bp)

	return app