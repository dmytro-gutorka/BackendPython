from flask import render_template, request
from models import *


def register_router(app, db):

	@app.route('/')
	def index():
		users = User.query.all()
		return str(users)