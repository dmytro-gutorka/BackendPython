from flask import Flask, session, g
from app.models import db, User
from flask_migrate import Migrate
from .settings import Settings
from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
	class FlaskTask(Task):
		def __call__(self, *args: object, **kwargs: object) -> object:
			with app.app_context():
				return self.run(*args, **kwargs)

	celery_app = Celery(app.name, task_cls=FlaskTask)
	celery_app.config_from_object(app.config["CELERY"])
	celery_app.set_default()
	app.extensions["celery"] = celery_app
	return celery_app


def create_app():
	app = Flask(__name__, template_folder=Settings.TEMPLATE_FOLDER, static_folder=Settings.STATIC_FOLDER)
	app.config.from_object('app.settings.Settings')

	db.init_app(app)
	Migrate(app, db)

	register_blueprints(app)
	register_error_handlers(app)

	app.config.from_mapping(
		CELERY=dict(
			broker_url="amqp://guest:guest@localhost:5672//",
			result_backend="rpc://",
			task_ignore_result=True,
		),
	)
	app.config.from_prefixed_env()
	celery_init_app(app)

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
		return "Page Not Found ", 404

	@app.errorhandler(500)
	def internal_error(error):
		return "Internal Server Error", 500
