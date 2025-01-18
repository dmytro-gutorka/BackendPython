from flask import render_template, request, url_for, redirect, session, Blueprint, flash
from sqlalchemy import select, delete, insert
from .models import db, User, Item, Favourite, Contract
from sqlalchemy.orm import selectinload
from .utils import save_object_with_file_in_db
from datetime import datetime


bp = Blueprint("main", __name__)

# TODO: 2 - decorator for unauthorized users


@bp.route('/index')
def index():
	return render_template('main/index.html')


@bp.route('/profile', methods=['GET', 'PUT', 'DELETE'])
def profile_view():
	if request.method == 'GET':
		profile_data = db.session.execute(select(User).where(User.id == session.get('user_id'))).scalar()
		return render_template('main/profile.html', profile_data=profile_data)


@bp.route('/items', methods=['GET', 'POST'])
def item_list_view():
	owner_id = session.get('user_id')

	if request.method == 'POST':
		form_data = request.form.to_dict()
		form_data['owner_id'] = owner_id
		file = request.files['photo']
		save_object_with_file_in_db(form_data, file, Item)

		return redirect(url_for('main.item_list_view'))

	in_favorite_list = db.session.execute(select(Favourite.item_id).where(Favourite.user_id == session.get('user_id'))).scalars().all()
	items_by_owner = db.session.execute(select(Item)).scalars()
	return render_template('main/item_list.html', items_by_owner=items_by_owner, in_favorite_list=in_favorite_list)


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


#


@bp.get('/leaser')
def leaser_list_view():
	stmt = select(User).options(selectinload(User.items))
	all_leasers_with_items = db.session.execute(stmt).scalars().all()

	return render_template('main/leaser_list.html', leasers=all_leasers_with_items)


@bp.get('/leaser/<int:leaser_id>')
def leaser_detail_view(leaser_id):
	stmt = select(User).where(User.id == leaser_id)
	leaser = db.session.execute(stmt).scalars().first()

	return render_template('main/leaser_detail.html', leaser=leaser)


@bp.route('/favourite', methods=['GET', 'POST'])
def favourite_item_list_view():
	if request.method == 'POST':
		form_data = request.form.to_dict()
		stmt = insert(Favourite).values(**form_data)
		db.session.execute(stmt)
		db.session.commit()

		return redirect(url_for('main.item_list_view'))

	stmt = select(Item).where(Item.id.in_(
		select(Favourite.item_id).where(Favourite.user_id == session.get('user_id'))))
	favourite_items = db.session.execute(stmt).scalars().all()

	return render_template('main/favourite_items.html', favourite_items=favourite_items)


@bp.route('/contract', methods=['GET'])
def contract_list_view():
	if request.method == 'POST':
		pass

	return render_template('main/index.html')


@bp.route('/items/<int:item_id>/rent', methods=['POST', 'GET'])
def item_rent_view(item_id):
	if request.method == 'POST':
		form_data = request.form.to_dict()

		print(form_data)
		start_date = datetime.strptime(form_data['start_date'], '%Y-%m-%d')
		end_date = datetime.strptime(form_data['end_date'], '%Y-%m-%d')

		stmt = insert(Contract).values(description=form_data['description'], start_date=start_date
		                               ,end_date=end_date, renter_id=int(form_data['renter_id']),
		                               host_id=int(form_data['host_id']), item_id=int(form_data['item_id']))
		db.session.execute(stmt)
		db.session.commit()
		flash('Your contract has been created.', 'success')

		return redirect(url_for('main.index'))

	return redirect(url_for('main.item_detail_view', item_id=item_id))


@bp.route('/contract/<int:contract_id>', methods=['GET'])
def contracts_detail_view(contract_id):
	if request.method == 'GET':
		return f"Get contract by {contract_id}"



# @app.post('/complain')
# def complain():
# 	return "Create a complaint"

