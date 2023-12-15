import cv2
import os
from imageModule import Image

for filename in os.listdir("Test_images/"):
    img = Image(path="Test_images/" + filename)
    cv2.imshow("Image", img.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
