from flask import *
from flask_cors import CORS
import time, json
from asciify import asciify, draw_ascii_art
from utils import load_image_from_url
from io import BytesIO
import subprocess

app = Flask(__name__)
CORS(app, origins='http://localhost:9000')

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

@app.route('/draw_ascii', methods=['GET'])
def request_draw_ascii():
	text = request.headers.get('text')
	font_size = request.headers.get('fontsize')

	if text == None:
		abort(400, 'Bad Request: text not specified')

	if font_size == None:
		abort(400, 'Bad Request: font_size not specified')

	try:
		font_size = int(font_size)
	except:
		abort(400, 'Bad Request: font_size must be a number')

	if font_size > 32:
		abort(400, 'Bad Request: maximum font_size allowed is 32')
	
	image = draw_ascii_art(text, font_size)
	if image == -1:
		abort(400, 'Error: output image dimensions are too large, try reducing font_size or text length')

	if image.size[0] == 0 or image.size[1] == 0:
		abort(400, 'Error: one of the image dimensions is 0')
	#TODO: Figure out why sometimes the image dimensions are 0

	img_bytes = BytesIO()
	image.save(img_bytes, format='JPEG')
	img_bytes.seek(0)

	return send_file(img_bytes, mimetype='image/jpeg')

import os
@app.route('/chessbot', methods=['GET'])
def chess_bot():
	fen = request.headers.get('fen')
	depth = request.headers.get('depth')

	process = subprocess.Popen([f'ChessBot', fen, depth], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	output, error = process.communicate()

	return output