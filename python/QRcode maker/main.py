
# pip install pypng
# pip install pyqrcode

import pyqrcode
from PIL import Image
# input link to genrate QRcode
link =input("enter anything to generate QR :")
qr_code=pyqrcode.create(link)
qr_code.png('./QRcode.png',scale=5)
Image.open("./QRcode.png")