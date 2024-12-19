import cv2
import base64
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()

for _ in range(30):  # discard the first 10 frames
    _, _ = cap.read()
ret, image = cap.read()

alpha = 1  # Faktor kontrast
beta = 2    # Faktor kecerahan
brightened_frame = cv2.addWeighted(image, alpha, image, 0, beta)

cv2.imshow("captured_image_brightened", brightened_frame)
#cv2.imwrite("captured_image_brightened.jpg", brightened_frame)
ret, buffer = cv2.imencode('.jpg', brightened_frame)
jpg_as_text = base64.b64encode(buffer).decode()
print("Base64 string: ", jpg_as_text)
cap.release()
cv2.destroyAllWindows()
"""
import cv2

# read the input image
img = cv2.imread('captured_image_brightened.jpg')

# define the contrast and brightness value
contrast = 1.2 # Contrast control ( 0 to 127)
brightness = 12 # Brightness control (0-100)

# call addWeighted function. use beta = 0 to effectively only
#operate on one image
out = cv2.addWeighted( img, contrast, img, 0, brightness)

# display the image with changed contrast and brightness
cv2.imshow('captured_image_brightened', out)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""