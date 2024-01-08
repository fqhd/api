from flask import *
import time, json

app = Flask(__name__)

# This is just a test api

@app.route('/', methods=['GET'])
def home_page():
	data_set = {
		'Page': 'Home',
		'Message': 'Sucessfully loaded the home page',
		'Timestamp': time.time()
	}
	json_dump = json.dumps(data_set)

	return json_dump

@app.route('/user/', methods=['GET'])
def request_page():
	user_query = str(request.args.get('user'))

	data_set = {
		'Page': 'Request',
		'Message': f'Sucessfully loaded the request for {user_query}',
		'Timestamp': time.time()
	}

	json_dump = json.dumps(data_set)

	return json_dump
