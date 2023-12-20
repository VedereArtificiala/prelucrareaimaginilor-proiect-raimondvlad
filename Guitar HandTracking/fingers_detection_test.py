import os
from matplotlib import pyplot as plot
from imageModule import Image
from rotate_and_crop import rotate_picture, crop_image
from fingers_detection import hand_detection, locate_hand, skin_detection
import cv2
import time


def test(b):
    i = 1
    plot.figure(1)
    for filename in os.listdir('./Test_images/'):
        print("Fisierul " + filename + " este in curs de procesare....")
        startTime = time.time()
        img = Image(path='./Test_images/' + filename)
        rotated = rotate_picture(img)
        crop = crop_image(rotated)

        skin = skin_detection(crop.image)
        hand_region = locate_hand(skin)
        hand = hand_detection(hand_region)

        plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(hand[b], cv2.COLOR_BGR2RGB))
        print("S-a terminat procesarea in %s secunde" % round(time.time() - startTime, 2))

    plot.show()

if __name__ == '__main__':
    print("1 - Contur\n2 - Transformata Hough\n")
    choice = input("[1/2]>>")
    if choice == "1":
        test(0)
    elif choice == "2":
        test(1)
    else:
        print("Invalid")
