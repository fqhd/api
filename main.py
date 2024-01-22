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
def request_asciify():
	img_url = request.args.get('img_url')
	width = request.args.get('width')

	if img_url == None:
		abort(400, 'Bad Request: img_url not specified')

	if width == None:
		abort(400, 'Bad Request: width not specified')

	try:
		width = int(width)
	except:
		abort(400, 'Bad Request: width must be a number')

	if width > 1000:
		abort(400, 'Bad Request: maximum width allowed is 1000')

	try:
		image = load_image_from_url(img_url)
	except:
		abort(400, 'Bad Request: could not load image from specified url')
	
	ascii_image_text = asciify(image, width)

	return ascii_image_text
