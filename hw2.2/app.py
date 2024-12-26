from flask import Flask, request

app = Flask(__name__)


@app.get('/login')
def login_get():
	return "Render log in page"


@app.get('/login')
def login_post():
	return "You\'re are logged in"


@app.get('/register')
def register_get():
	return "Render a register page"


@app.post('/register')
def register_post():
	return "You\'re are successfully registered"


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
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
