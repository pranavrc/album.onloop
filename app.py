#!/usr/bin/python

from flask import *
from make_html import make_html
from storedata import *
from random import choice

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])

def index():
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		count = request.form['count']
		query = request.form['query']
		#if int(count) == 1:
		#	username = request.form['name']
		#	if username == "" or username == "Album search (Leave blank for random album.)":
		#		data = readJson()
		#		username = choice(data)
		#		storeVar(username)
		#	else:
		#		pass
		#else:
		#	if os.path.exists('userdata.p'):
		#		username = loadVar()
		#	else:
		#		username = request.form['name']
		
		#print username
		#if int(count) == 7:
		#	removePickle()

		return make_html(query, int(count))

if __name__ == "__main__":
	app.run(debug = True)
