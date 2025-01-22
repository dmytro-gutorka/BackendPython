import os


class Settings:
	SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

	"""DIRECTORIES"""
	BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
	STATIC_FOLDER = os.path.join(BASE_DIR, 'static/')
	MEDIA_FOLDER = os.path.join(BASE_DIR, 'media/')
	TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates/')

	ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
	MAX_CONTENT_LENGTH = 16 * 1000 * 1000

	"""MAILS"""
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USERNAME = 'dgutorka@gmail.com'
	MAIL_PASSWORD = 'effe qttb osgr uxen'
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False

	"""BROKER RABBITMQ"""
	BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
	RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")