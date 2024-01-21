import requests
from PIL import Image
from io import BytesIO

def load_image_from_url(url):
	response = requests.get(url)
	if response.status_code == 200:
		image_data = BytesIO(response.content)
		image = Image.open(image_data)
		return image
	else:
		print(f"Failed to retrieve the image. Status code: {response.status_code}")
		return None