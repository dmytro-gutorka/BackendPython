from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db
from app.utils import login_required
from app.utils import db_handler


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id', None)

	if user_id is None:
		g.user = None
	else:
		g.user = db_handler.select('user', {'id': user_id}).fetchone()


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		error = None

		query_result = db_handler.insert('user', {'username': username, 'password': generate_password_hash(password)})

		if not username or not password:
			error = 'Invalid username or password'

		if query_result is None:
			return redirect(url_for('auth.login'))

		error = query_result
		flash(error)

	return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		error = None
		user = db_handler.select('user', {'username': username}).fetchone()

		if user is None or not check_password_hash(user['password'], password):
			error = 'Incorrect username or password'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('core.index'))  # change index to another URL

		flash(error)

	return render_template('auth/login.html')


@login_required
@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('core.index'))
