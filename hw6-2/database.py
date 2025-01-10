from flask_migrate import Migrate
from models import db
from views import app


def create_app(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	db.init_app(app)
	migrate = Migrate(app, db)

	return app


flask_app = create_app(app)

if __name__ == '__main__':
	flask_app.run(host='0.0.0.0', debug=True)