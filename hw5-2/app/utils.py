from flask import redirect, url_for, g
from app.db import get_db
import functools


def login_required(view):
	@functools.wraps(view)
	def wrapper_view(*args, **kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(*args, **kwargs)

	return wrapper_view


class DBHandler:

	def select(self, table_name, filter_dict=None):
		if filter_dict is None:
			filter_dict = {}

		db = get_db()
		query = f"SELECT * FROM {table_name}"

		if filter_dict:
			query += f" WHERE "
			itms = []
			for k in filter_dict.keys():
				itms.append(f"{k} = ?")
			query += " AND ".join(itms)

		query_result = db.execute(query, tuple(value for value in filter_dict.values()))
		return query_result

	def insert(self, table_name, data_dict):
		db = get_db()
		query = f"INSERT INTO {table_name} ("
		query += ', '.join(data_dict.keys())
		query += ") VALUES ("
		query += ', '.join(['?' for _ in data_dict.keys()])
		query += ")"

		try:
			db.execute(query, tuple(data_dict.values()))
			db.commit()
		except db.IntegrityError:
			return 'User with this username is already registered.'


db_handler = DBHandler()