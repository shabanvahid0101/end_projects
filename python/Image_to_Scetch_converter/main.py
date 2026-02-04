import cv2

image = cv2.imread('a1.jpeg')
gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
inverted=255-gray_image
blur=cv2.GaussianBlur(inverted,(21,21),0)
invertedblur=255-blur
sketh=cv2.divide(gray_image,invertedblur,scale=255.0)
cv2.imwrite("sketch_image.png",sketh)
cv2.imshow("image",sketh)
print("save image")
