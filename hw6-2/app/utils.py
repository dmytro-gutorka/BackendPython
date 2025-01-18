from flask import current_app
from werkzeug.utils import secure_filename
from .models import db
from sqlalchemy import update, insert

import os


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


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
