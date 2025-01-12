from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint
from .models import db, User


bp = Blueprint("main", __name__)


@bp.route('/index')
def index():
	return render_template('main/index.html')


@bp.route('/profile')
def profile_view():
	return render_template('main/index.html')


@bp.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
	if request.method == 'GET':
		return "Render log out page"
	if request.method == 'POST':
		return "Logout(request.user) + clear session"
	if request.method == 'DELETE':
		return "some logic"


@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return "Get searched product"
	if request.method == 'POST':
		return "Created product"


@app.route('/contracts', methods=['GET', 'POST'])
def contracts_list():
	if request.method == 'GET':
		return "Get contract"
	if request.method == 'POST':
		return "Created contract"


@app.route('/contracts/<int:contract_id>', methods=['GET', 'PUT', 'PATCH'])
def contracts_detail(contract_id):
	if request.method == 'GET':
		return f"Get contract by {contract_id}"
	if request.method == 'POST':
		return f"Created contract with id {contract_id}"


@app.post('/complain')
def complain():
	return "Create a complain"


@app.route('/items', methods=['GET', 'POST'])
def items_list():
	if request.method == 'GET':
		return "Items list"
	if request.method == 'POST':
		return "create items"


@app.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def items_detail(item_id):
	if request.method == 'GET':
		return f"Get item {item_id}"
	if request.method == 'DELETE':
		return f"Item {item_id} was deleted"


@app.route('/compare', methods=['GET', 'PUT', 'PATCH'])
def compare():
	if request.method == 'GET':
		return "Get compare page"
	if request.method == 'PUT':
		return "Compare item"
	if request.method == 'PATCH':
		return "Compare item"


@app.get('/leasers')
def leasers_list():
	return 'all the leasers'


@app.get('/leasers/<int:leaser_id>')
def leasers_detail(leaser_id):
	return f' leaser {leaser_id}'


@app.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile():
	if request.method == 'GET':
		return "Get profile page"
	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@app.get('/test/<name>')
def test(name):
	return render_template('index.html', name=name)