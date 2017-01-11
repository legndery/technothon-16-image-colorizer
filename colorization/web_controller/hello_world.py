from flask import jsonify, Blueprint,render_template
import sys
hello = Blueprint('simple_page', __name__)

@hello.route('/')
def hello_world():
	return '<br>'.join(sys.path)#+'Hello, World!'

@hello.route('/hello/')
@hello.route('/hello/<name>')
def hello_name(name=None):
	if name == 'json':
		d = {"name":"Json", "msg": "Hello Json"};
		return jsonify(**d)
	return render_template('hello.html',name=name)
