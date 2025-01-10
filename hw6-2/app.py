from flask import Flask
from flask_migrate import Migrate
from models import db


def create_app():
	app = Flask(__name__, template_folder='templates')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

	db.init_app(app)

	from views import register_router
	register_router(app, db)

	migrate = Migrate(app, db)

	return app
