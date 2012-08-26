#!/usr/bin/python

from flask import *
from make_html import make_html

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])

def index():
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		username = request.form['name']
		return make_html(username)

if __name__ == "__main__":
	app.run(debug = True)
