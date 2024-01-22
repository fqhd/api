from PIL import Image, ImageDraw, ImageFont
import math

ascii_sorted_by_brightness = ' `.-\':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@'

def draw_ascii_art(ascii_text, font_size):
	# Create a new image with the specified width and height
	font = ImageFont.truetype('consolas.ttf', font_size)

	width = int(font.getlength(ascii_text.split('\n')[0]))
	height = int(font_size * len(ascii_text.split('\n')) - font_size)

	if width >= 2000:
		return -1
	if height >= 2000:
		return -1

	img = Image.new('RGB', (width, height), color='white')
	draw = ImageDraw.Draw(img)

	# Split the ASCII art text into lines
	lines = ascii_text.split('\n')

	# Calculate the starting position for drawing each line
	y = 0

	# Draw each line onto the image
	for line in lines:
		draw.text((0, y), line, font=font, fill='black')
		y += font_size  # Adjust this value based on the font size and line spacing

	return img

def asciify(image, width):
	text = ''

	w, h = image.size
	ratio = h / w
	height = int(width * ratio * 0.5)
	image = image.resize((int(width), height))

	for i in range(height):
		for j in range(int(width)):
			R, G, B = image.getpixel((j, i))[:3]
			brightness = 0.2126*R + 0.7152*G + 0.0722*B
			brightness /= 255
			idx = int(brightness * len(ascii_sorted_by_brightness))
			char = ascii_sorted_by_brightness[-idx]
			text += char
		text += '\n'
	
	return text



