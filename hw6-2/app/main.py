from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint, send_from_directory, \
	current_app
from sqlalchemy import select, delete
from .models import db, User, Item
from werkzeug.utils import secure_filename
import os

bp = Blueprint("main", __name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@bp.route('/index')
def index():
	return render_template('main/index.html')


# def save_object_in_db_with_file()


@bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile_view():
	if request.method == 'GET':
		profile_data = db.session.execute(select(User).where(User.id == session.get('user_id')))
		return render_template('main/profile.html', profile_data=profile_data)

	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@bp.route('/items', methods=['GET'])
def item_list_view():
	owner_id = session.get('user_id')

	if request.method == 'GET':
		items_by_owner = db.session.execute(select(Item).where(owner_id=owner_id)).scalars()
		return render_template('main/item_list.html', items_by_owner=items_by_owner)

	if request.method == 'POST':
		form_data = request.form.to_dict()
		form_data['owner_id'] = owner_id
		file = request.files['photo']

		if file.filename != '' and allowed_file(file.filename):
			secured_filename_with_subdir = f'item_images/{secure_filename(file.filename)}'
			form_data['photo'] = secured_filename_with_subdir
			file.save(os.path.join(current_app.config['MEDIA_FOLDER'], secured_filename_with_subdir))

		new_item = Item(**form_data)
		db.session.add(new_item)
		db.session.commit()

		return redirect(url_for('main.item_list_view'))


@bp.route('/items/<int:item_id>', methods=['DELETE'])
def item_detail_view(item_id):
	item = db.session.execute(select(Item).where(Item.id == item_id)).scalar()

	if request.method == 'DELETE':
		if session.get('user_id') == item.owner_id:
			db.session.delete(item)
			db.session.commit()
			return redirect(url_for('main.item_list_view')), 204

		return 'Unauthorized', 403

	if request.method == 'PUT':
		if session.get('user_id') == item.owner_id:

			form_data = request.form.to_dict()
			form_data['owner_id'] = item.owner_id
			file = request.files['photo']

			if file.filename != '' and allowed_file(file.filename):
				secured_filename_with_subdir = f'item_images/{secure_filename(file.filename)}'
				form_data['photo'] = secured_filename_with_subdir
				file.save(os.path.join(current_app.config['MEDIA_FOLDER'], secured_filename_with_subdir))

			db.session.execute(db.update(Item).filter_by(id=item_id), form_data)
			db.session.commit()

			return redirect(url_for('main.item_list_view')), 204

		return 'Unauthorized', 403

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
# 	return "Create a complaint"

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
