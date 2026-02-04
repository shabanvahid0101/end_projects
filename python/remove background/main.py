from rembg import remove
from PIL import Image

# image address
image_file = 'D:/code/end_project/python/remove background/1742017620713.jpg'
# remove background image address
image_converted = 'output.png'
inserted_image = Image.open(image_file)
output = remove(inserted_image)
output.save(image_converted)