from flask import render_template, request
from flask import Flask
from models import *


app = Flask(__name__, template_folder='templates')


@app.route('/registration', methods=['GET', 'POST'])
def registration_view():
	if request.method == 'POST':
		pass
	else:
		pass