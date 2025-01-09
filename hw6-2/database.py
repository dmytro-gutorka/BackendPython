from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text, insert, select
from config import settings
from models import Base, Workers, Resumes


engine = create_engine(
	url=settings.DATABASE_URL_psycopg,
	echo=False,
	# pool_size=5,
	# max_overflow=10
)

session_factory = sessionmaker(engine)


def create_tables():
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)


def select_data():
	with session_factory() as session:
		query = select(Workers)
		result = session.execute(query)
		workers = result.scalars().all()


def insert_data():
	with session_factory() as session:
		worker1 = Workers(username='Worker1')
		worker2 = Workers(username='Worker2')

		print(worker1)

		session.add_all([worker1, worker2])
		session.commit()


def update_date():
	with session_factory() as session:
		worker = session.get(Workers, 1)
		worker.username = 'New name'
		session.commit()


def main():
	create_tables()
	insert_data()
	update_date()
	select_data()


if __name__ == '__main__':
	main()
