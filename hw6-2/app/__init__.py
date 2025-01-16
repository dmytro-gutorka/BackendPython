from flask import Flask, request, session, g
from app.models import db, User
from flask_migrate import Migrate
from .settings import Settings


def create_app():
	app = Flask(__name__, template_folder=Settings.TEMPLATE_FOLDER, static_folder=Settings.STATIC_FOLDER)
	app.config.from_object('app.settings.Settings')

	db.init_app(app)
	Migrate(app, db)

	register_blueprints(app)
	register_error_handlers(app)

	@app.before_request
	def handle_sessions():
		user_id = session.get('user_id')
		if user_id is None:
			g.user = None
		else:
			g.user = User.query.get(int(user_id))

	return app


def register_blueprints(app):
	from . import auth, main

	app.register_blueprint(auth.bp)
	app.register_blueprint(main.bp)


def register_error_handlers(app):
	@app.errorhandler(404)
	def not_found(error):
		return "Page Not Found", 404

	@app.errorhandler(500)
	def internal_error(error):
		return "Internal Server Error", 500


