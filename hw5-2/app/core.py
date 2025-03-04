from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.db import get_db
from app.utils import db_handler

bp = Blueprint('core', __name__, url_prefix='/core')


@bp.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		full_search_history = db_handler.select('search_history').fetchall()
		return render_template('core/index.html', full_search_history=full_search_history)

	if request.method == 'POST':
		return "Created product"


@bp.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
	if request.method == 'GET':
		contract_list = db_handler.select('contract').fetchall()
		return render_template('core/index.html', contract_list=contract_list)
	if request.method == 'POST':
		return "Created contract"


@bp.route('/contracts/<int:contract_id>', methods=['GET', 'PUT', 'PATCH'])
def contracts_detail(contract_id):
	if request.method == 'GET':
		contract_detail = db_handler.select('contract', {'id': contract_id}).fetchone()
		return render_template('core/index.html', contract_detail=contract_detail)
	if request.method == 'POST':
		return f"Created contract with id {contract_id}"


@bp.route('/items', methods=['GET', 'POST'])
def items_list():
	if request.method == 'GET':
		item_list = db_handler.select('item').fetchall()
		return render_template('core/item_create.html', item_list=item_list)

	if request.method == 'POST':
		form_data = request.form.to_dict()
		error = None

		if not form_data['name'] or not form_data['photo']:
			error = 'Fields name and photo are required'
			
		if error is None:
			db_handler.insert('item', form_data)
			flash('Item created', 'info')
			
		return redirect(url_for('core.index'))


@bp.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def items_detail(item_id):
	if request.method == 'GET':
		item_detail = db_handler.select('item', {'id': item_id}).fetchone()
		return render_template('core/index.html', item_detail=item_detail)

	if request.method == 'DELETE':
		return f"Item {item_id} was deleted"


@bp.get('/leasers')
def leasers_list():
	leaser_list = db_handler.select('item').fethall()
	return render_template('core/index.html', leaser_list=leaser_list)


@bp.get('/leasers/<int:leaser_id>')
def leasers_detail(leaser_id):
	leaser_detail = db_handler.select('contract', {'leaser_id': leaser_id}).fetchone()
	return render_template('core/index.html', leaser_detail=leaser_detail)


@bp.route('/profile/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def profiles_detail(user_id):
	if request.method == 'GET':
		user_profile_data = db_handler.select('user', {'id': user_id}).fetchone()

		return render_template('core/profile.html', user_profile_data=user_profile_data)
	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@bp.post('/complain')
def complain():
	return "Create a complain"


@bp.get('/index')
def index():
	return render_template('core/index.html')