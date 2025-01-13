from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import db, User
import os
from . import UPLOAD_FOLDER


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_request
def before_request():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = User.query.get(int(user_id))


@bp.route('/registration', methods=['GET', 'POST'])
def registration_view():
	if request.method == 'POST':
		form_data = request.form.to_dict()
		hash_password = generate_password_hash(form_data['password'])
		form_data['password'] = hash_password

		file = request.files['file']
		if file.filename != '':
			file.save(os.path.join(UPLOAD_FOLDER, file.filename))
			form_data['photo'] = secure_filename(file.filename)

		new_user = User(**form_data)
		db.session.add(new_user)
		db.session.commit()

		return redirect(url_for('main.index'))
	else:
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
