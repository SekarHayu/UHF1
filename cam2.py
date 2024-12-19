
import cv2

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    
    ret, image = cam.read()
    
    # Check if the frame is correctly received
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #
    cv2.imshow('coba_v3', image)
    k = cv2.waitKey(1)
    
    if k != -1:  # If any key is pressed, break the loop
        cv2.imwrite('/home/gaskan/UHF/PICAM2/image/coba_v3.jpg', image)
        break

cam.release()
cv2.destroyAllWindows()
"""

import cv2

cv2.namedWindow('coba_v3', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('coba_v3', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    ret, image = cam.read()

    # Check if the frame is correctly received
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('coba_v3', image)
    k = cv2.waitKey(1)

    if k != -1:  # If any key is pressed, break the loop
        cv2.imwrite('/home/gaskan/UHF/PICAM2/image/coba_v3.jpg', image)
        break

cam.release()
cv2.destroyAllWindows()
"""