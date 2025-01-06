from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


@app.route('/home/<name>')
def home(name):
	return "Hello " + name


@app.route('/index')
def index():
	return redirect(url_for('home', name='Dima'))


@app.route('/')
def main_page():
	return render_template('index.html')