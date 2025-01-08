from sqlalchemy import text, insert
from database import engine
from models import metadata_obj, workers_table


def create_tables():
	metadata_obj.drop_all(engine)
	metadata_obj.create_all(engine)


def insert_data():
	with engine.connect() as conn:
		statement = insert(workers_table).values(
			[
				{'username': 'Wolf'},
				{'username': 'Cat'},
			]
		)
		conn.execute(statement)
		conn.commit()