from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db
from app.utils import login_required
import functools


bp = Blueprint('core', __name__, url_prefix='/core')


@bp.route('/search', methods=['GET', 'POST'])
def search():
	db = get_db()
	if request.method == 'GET':
		full_search_history = db.execute("SELECT * FROM search_history").fetchall()
		return render_template('core/index.html', full_search_history=full_search_history)

	if request.method == 'POST':
		return "Created product"


@bp.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
	db = get_db()
	if request.method == 'GET':
		contract_list = db.execute("SELECT * FROM contract").fetchall()
		return render_template('core/index.html', contract_list=contract_list)
	if request.method == 'POST':
		return "Created contract"


@bp.route('/contracts/<int:contract_id>', methods=['GET', 'PUT', 'PATCH'])
def contracts_detail(contract_id):
	db = get_db()
	if request.method == 'GET':
		contract_detail = db.execute("SELECT * FROM contract WHERE id = ?", (contract_id,)).fetchone()
		return render_template('core/index.html', contract_detail=contract_detail)
	if request.method == 'POST':
		return f"Created contract with id {contract_id}"


@bp.post('/complain')
def complain():
	return "Create a complain"


@bp.route('/items', methods=['GET', 'POST'])
def items_list():
	db = get_db()
	if request.method == 'GET':
		item_list = db.execute("SELECT * FROM item").fetchall()
		return render_template('core/item_create.html', item_list=item_list)

	if request.method == 'POST':
		db = get_db()
		error = None

		name = request.form['name']
		photo = request.form['photo']
		price_per_hour = request.form['price_per_hour']
		price_per_day = request.form['price_per_day']
		price_per_week = request.form['price_per_week']
		price_per_month = request.form['price_per_month']
		
		if not name or not photo:
			error = 'Fields name and photo are required'
			
		if error is None:
			db.execute(
				"INSERT INTO item (name, photo, price_per_hour, price_per_day, price_per_week, price_per_month)"
				"VALUES (?, ?, ?, ?, ?, ?)", (name, photo, price_per_hour, price_per_day, price_per_week, price_per_month), )
			db.commit()
			flash('Item created', 'info')
			
		return redirect(url_for('core.index'))


@bp.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def items_detail(item_id):
	db = get_db()
	if request.method == 'GET':
		item_detail = db.execute("SELECT * FROM item WHERE id = ?", (item_id,)).fetchone()
		return render_template('core/index.html', item_detail=item_detail)
	if request.method == 'DELETE':
		return f"Item {item_id} was deleted"


@bp.get('/leasers')
def leasers_list():
	db = get_db()
	leaser_list = db.execute("SELECT leaser_id FROM contract").fethall()
	return render_template('core/index.html', leaser_list=leaser_list)


@bp.get('/leasers/<int:leaser_id>')
def leasers_detail(leaser_id):
	db = get_db()
	leaser_detail = db.execute("SELECT leaser_id FROM contract WHERE leaser_id = ?", (leaser_id, )).fetchone()
	return render_template('core/index.html', leaser_detail=leaser_detail)


@bp.route('/profile/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def profiles_detail(user_id):
	if request.method == 'GET':
		db = get_db()
		user_profile_data = db.execute("SELECT * FROM user WHERE id = ?", (user_id, )).fetchone()
		return render_template('core/profile.html', user_profile_data=user_profile_data)
	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@bp.get('/index')
def index():
	return render_template('core/index.html')