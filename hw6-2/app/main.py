from flask import render_template, request, flash, url_for, redirect, session, g, Blueprint
from .models import db, User


bp = Blueprint("main", __name__)


@bp.route('/index')
def index():
	return render_template('main/index.html')


@bp.route('/profile')
def profile_view():
	return render_template('main/index.html')