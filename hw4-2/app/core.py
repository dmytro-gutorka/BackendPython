from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db
import functools


bp = Blueprint('core', __name__, url_prefix='/core')


@bp.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return "Get searched product"
	if request.method == 'POST':
		return "Created product"


@bp.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
	if request.method == 'GET':
		return "Get contract"
	if request.method == 'POST':
		return "Created contract"


@bp.route('/contracts/<int:contract_id>', methods=['GET', 'PUT', 'PATCH'])
def contracts_detail(contract_id):
	if request.method == 'GET':
		return f"Get contract by {contract_id}"
	if request.method == 'POST':
		return f"Created contract with id {contract_id}"


@bp.post('/complain')
def complain():
	return "Create a complain"


@bp.route('/items', methods=['GET', 'POST'])
def items_list():
	if request.method == 'GET':
		return "Items list"
	if request.method == 'POST':
		return "create items"


@bp.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def items_detail(item_id):
	if request.method == 'GET':
		return f"Get item {item_id}"
	if request.method == 'DELETE':
		return f"Item {item_id} was deleted"


@bp.route('/compare', methods=['GET', 'PUT', 'PATCH'])
def compare():
	if request.method == 'GET':
		return "Get compare page"
	if request.method == 'PUT':
		return "Compare item"
	if request.method == 'PATCH':
		return "Compare item"


@bp.get('/leasers')
def leasers_list():
	return 'all the leasers'


@bp.get('/leasers/<int:leaser_id>')
def leasers_detail(leaser_id):
	return f' leaser {leaser_id}'


@bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
	if request.method == 'GET':
		return "Get profile page"
	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"
