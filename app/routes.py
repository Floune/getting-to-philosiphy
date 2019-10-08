from app import app
from flask import request
from flask import jsonify
from scrap import *

@app.route('/')
@app.route('/index')
def index():
	return "/gtp?s=chaussette"

@app.route('/gtp')
def gtp():
	mot = request.args.get('s', default = 1, type = str)
	tab = start(mot)
	print(tab)
	return jsonify(tab)