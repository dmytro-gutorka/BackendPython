from flask import render_template, request, url_for, redirect, session, Blueprint, current_app, flash
from sqlalchemy import select, delete, update, insert
from .models import db, User, Item
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Bundle, selectinload

import os

bp = Blueprint("main", __name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


# TODO: 2 - decorator for unauthorized users

@bp.route('/index')
def index():
	return render_template('main/index.html')


def save_object_with_file_in_db(form_data, file, class_model, obj_id=None, is_update=False):

	if file.filename != '' and allowed_file(file.filename):
		# if not os.exists -> os.mkdir
		secured_filename_with_subdir = f'{class_model.__name__.lower()}_images/{secure_filename(file.filename)}'
		form_data['photo'] = secured_filename_with_subdir
		file.save(os.path.join(current_app.config['MEDIA_FOLDER'], secured_filename_with_subdir))

	if is_update and obj_id is not None:
		db.session.execute(update(class_model).where(class_model.id == obj_id).values(**form_data))
	else:
		db.session.execute(insert(class_model).values(**form_data))
	db.session.commit()


@bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile_view():
	if request.method == 'GET':
		profile_data = db.session.execute(select(User).where(User.id == session.get('user_id'))).scalar()
		return render_template('main/profile.html', profile_data=profile_data)

	if request.method == 'PUT':
		return "Update profile"
	if request.method == 'DELETE':
		return "Delete profile"


@bp.route('/items', methods=['GET', 'POST'])
def item_list_view():
	owner_id = session.get('user_id')
	print(request.form.to_dict())

	if request.method == 'POST':
		form_data = request.form.to_dict()
		form_data['owner_id'] = owner_id
		file = request.files['photo']
		save_object_with_file_in_db(form_data, file, Item)

		return redirect(url_for('main.item_list_view'))

	items_by_owner = db.session.execute(select(Item).where(Item.owner_id == owner_id)).scalars()
	return render_template('main/item_list.html', items_by_owner=items_by_owner)


@bp.route('/items/<int:item_id>', methods=['DELETE', 'GET'])
def item_detail_view(item_id):
	item = db.session.execute(select(Item).where(Item.id == item_id)).scalar()

	if request.method == 'DELETE':
		if session.get('user_id') == item.owner_id:
			db.session.execute(delete(Item).where(Item.id == item_id))
			db.session.commit()
			return redirect(url_for('main.item_list_view')), 204

		return 'Unauthorized', 403

	return render_template('main/item_detail.html', item=item)


@bp.route('/items/<int:item_id>/edit', methods=['POST', 'GET', 'PUT'])
def item_edit_view(item_id):
	item = db.session.execute(select(Item).where(Item.id == item_id)).scalar()

	if 'edit_item' in request.form.to_dict():
		if session.get('user_id') == item.owner_id:
			form_data = request.form.to_dict()
			del form_data['edit_item']
			form_data['owner_id'] = item.owner_id
			file = request.files['photo']
			save_object_with_file_in_db(form_data, file, Item, item_id, is_update=True)

			flash('Your item has been updated.', 'success')

			return redirect(url_for('main.item_detail_view', item_id=item_id))

		return 'Unauthorized', 403

	return render_template('main/item_detail_edit.html', item=item)


@bp.get('/leaser')
def leaser_list():
	stmt = select(User).options(selectinload(User.items))
	all_leasers_with_items = db.session.execute(stmt).scalars().all()

	return render_template('main/leaser_list.html', leasers=all_leasers_with_items)


@bp.get('/leaser/<int:leaser_id>')
def leaser_detail(leaser_id):
	stmt = select(User).where(User.id == leaser_id)
	leaser = db.session.execute(stmt).scalars().first()

	return render_template('main/leaser_detail.html', leaser=leaser)


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

