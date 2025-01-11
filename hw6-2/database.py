from flask_alembic import Alembic
from models import db, Base
from views import app
from sqlalchemy import create_engine


def create_app(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
	engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
	alembic = Alembic(app=app, engines=engine, metadatas=Base.metadata)

	db.init_app(app)
	alembic.init_app(app)

	return app


flask_app = create_app(app)


if __name__ == '__main__':
	flask_app.run(host='0.0.0.0', debug=True)