import os
import time
import cv2
from matplotlib import pyplot as plot
from imageModule import Image

from rotate_and_crop import rotate_picture, crop_image

i = 1
plot.figure(1)
for filename in os.listdir('Test_images/'):
    print("Imaginea: " + filename + " - se proceseaza...")
    startTime = time.time()
    chordImage = Image(path='./Test_images/'+filename)
    new = Image(img=chordImage)
    rotatedImage = rotate_picture(new)
    croppedImage = crop_image(rotatedImage)
    plot.subplot(int("42" + str(i)))
    i += 1
    plot.imshow(cv2.cvtColor(chordImage.image, cv2.COLOR_BGR2RGB))
    plot.subplot(int("42" + str(i)))
    i += 1
    plot.imshow(cv2.cvtColor(croppedImage.image, cv2.COLOR_BGR2RGB))
    print("Timp %s secunde" % round(time.time() - startTime, 2))

plot.show()
