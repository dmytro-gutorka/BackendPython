from flask import render_template, request, flash, url_for, redirect, session, g
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User


app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def before_request():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = User.query.get(int(user_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration_view():
	if request.method == 'POST':
		form_data = request.form.to_dict()
		hash_password = generate_password_hash(form_data['password'])
		form_data['password'] = hash_password
		new_user = User(**form_data)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('index'))
	else:
		return render_template('auth/registration.html')


@app.route('/login', methods=['GET', 'POST'])
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
			return redirect(url_for('index'))
		else:
			error = 'Incorrect username or password'

	return render_template('auth/login.html', error=error)


@app.route('/index')
def index():
	return render_template('main/index.html')