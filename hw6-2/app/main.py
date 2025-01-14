import os

from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint, send_from_directory
from .models import db, User, Item
from . import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug.utils import secure_filename


bp = Blueprint("main", __name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.before_request
def before_request():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = User.query.get(int(user_id))


@bp.route('/index')
def index():
	return render_template('main/index.html')


@bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile_view():
	if request.method == 'GET':
		profile_data = User.query.get(session.get('user_id'))
		photo_name = profile_data.photo
		return render_template('main/profile.html', profile_data=profile_data, photo_name=photo_name)
	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@bp.route('/items', methods=['GET', 'POST', 'DELETE'])
def items_list():
	owner_id = session.get('user_id')

	if request.method == 'DELETE':
		item_id = request.form['item_id']
		item = Item.query.get(int(item_id))
		db.session.delete(item)
		db.session.commit()

	if request.method == 'POST':
		form_data = request.form.to_dict()
		form_data['owner_id'] = owner_id

		file = request.files['photo']
		if file.filename != '' and allowed_file(file.filename):
			secured_filename_with_subdir = f'item_images/{secure_filename(file.filename)}'
			form_data['photo'] = secured_filename_with_subdir
			file.save(os.path.join(UPLOAD_FOLDER, secured_filename_with_subdir))

		new_item = Item(**form_data)
		db.session.add(new_item)
		db.session.commit()

	owner_items = Item.query.filter_by(owner_id=owner_id).all()

	return render_template('main/items.html', owner_items=owner_items)


@bp.route('/items/<int:item_id>', methods=['GET'])
def items_detail(item_id):
	if request.method == 'GET':
		return f"Get item {item_id}"
	if request.method == 'DELETE':
		return f"Item {item_id} was deleted"


# @app.route('/search', methods=['GET', 'POST'])
# def search():
# 	if request.method == 'GET':
# 		return "Get searched product"
# 	if request.method == 'POST':
# 		return "Created product"
#
#
# @app.route('/contracts', methods=['GET', 'POST'])
# def contracts_list():
# 	if request.method == 'GET':
# 		return "Get contract"
# 	if request.method == 'POST':
# 		return "Created contract"
#
#
# @app.route('/contracts/<int:contract_id>', methods=['GET', 'PUT', 'PATCH'])
# def contracts_detail(contract_id):
# 	if request.method == 'GET':
# 		return f"Get contract by {contract_id}"
# 	if request.method == 'POST':
# 		return f"Created contract with id {contract_id}"
#
#
# @app.post('/complain')
# def complain():
# 	return "Create a complain"

#
#
# @app.route('/compare', methods=['GET', 'PUT', 'PATCH'])
# def compare():
# 	if request.method == 'GET':
# 		return "Get compare page"
# 	if request.method == 'PUT':
# 		return "Compare item"
# 	if request.method == 'PATCH':
# 		return "Compare item"
#
#
# @app.get('/leasers')
# def leasers_list():
# 	return 'all the leasers'
#
#
# @app.get('/leasers/<int:leaser_id>')
# def leasers_detail(leaser_id):
# 	return f' leaser {leaser_id}'