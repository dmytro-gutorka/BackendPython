from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from .main import save_object_with_file_in_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/registration', methods=['GET', 'POST'])
def registration_view():
	if request.method == 'POST':
		form_data = request.form.to_dict()
		hash_password = generate_password_hash(form_data['password'])
		form_data['password'] = hash_password
		file = request.files['photo']
		save_object_with_file_in_db(form_data, file, User)

		return redirect(url_for('main.index'))

	return render_template('auth/registration.html')


@bp.route('/login', methods=['GET', 'POST'])
def login_view():
	error = None
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		user = User.query.filter_by(username=username).first()
		if user is not None and check_password_hash(user.password, password):
			session.clear()
			session['user_id'] = user.id
			flash('You\'re successfully logged in!')
			return redirect(url_for('main.index'))
		else:
			error = 'Incorrect username or password'

	return render_template('auth/login.html', error=error)


@bp.route('/logout')
def logout_view():
	session.clear()
	return redirect(url_for('main.index'))
