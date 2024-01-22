from flask import *
import time, json
from asciify import asciify
from utils import load_image_from_url

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
	data_set = {
		'Page': 'Home',
		'Message': 'Sucessfully loaded the home page',
		'Timestamp': time.time()
	}
	json_dump = json.dumps(data_set)

	return json_dump

@app.route('/asciify', methods=['GET'])
def request_page():
	img_url = str(request.args.get('img_url'))
	width = str(request.args.get('width'))

	if width > 1000:
		abort(410, 'Bad Request: Maximum width allowed is 1000')

	image = load_image_from_url(img_url)
	if image == None:
		abort(400, 'Bad Request: Invalid URL')
	
	ascii_image_text = asciify(image, width)

	return ascii_image_text

@app.route('/deepdream', methods=['GET'])
def request_page():
	img_url = str(request.args.get('img_url'))
	width = str(request.args.get('width'))

	if img_url == None:
		abort(400, 'Bad Request: img_url not specified')

	if width == None:
		abort(400, 'Bad Request: width not specified')

	if width > 1000:
		abort(410, 'Bad Request: Maximum width allowed is 1000')

	image = load_image_from_url(img_url)
	if image == None:
		abort(400, 'Bad Request: Invalid URL')
	
	ascii_image_text = asciify(image, width)

	return ascii_image_text
