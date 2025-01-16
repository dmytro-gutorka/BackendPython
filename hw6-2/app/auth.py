from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import db, User
from .main import allowed_file

import os


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/registration', methods=['GET', 'POST'])
def registration_view():
	if request.method == 'POST':
		form_data = request.form.to_dict()
		hash_password = generate_password_hash(form_data['password'])
		form_data['password'] = hash_password

		file = request.files['photo']
		if file.filename != '' and allowed_file(file.filename):
			secured_filename = secure_filename(file.filename)
			secured_filename_with_subdir = f'user_avatars/{secured_filename}'
			form_data['photo'] = secured_filename_with_subdir
			file.save(os.path.join(current_app.config['MEDIA_FOLDER'], secured_filename_with_subdir))

		new_user = User(**form_data)
		db.session.add(new_user)
		db.session.commit()

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
