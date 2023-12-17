import os
import time
from imageModule import Image
from matplotlib import pyplot as plot
from rotate_and_crop import rotate_picture, crop_image
from grid_detection import string_detection, fret_detection
import cv2


def string_detection_test():

    i = 1
    plot.figure(1)
    for filename in os.listdir('Test_images/'):
        print("Fisierul: " + filename + " este in decurs de procesare...")
        startTime = time.time()
        chordImage = Image(path='Test_images/' + filename)
        rotatedImage = rotate_picture(chordImage)
        croppedImage = crop_image(rotatedImage)
        strings = string_detection(croppedImage)[1]
        '''plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(chordImage.image, cv2.COLOR_BGR2RGB))
        plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(strings.image, cv2.COLOR_BGR2RGB))'''
        cv2.imshow('original', chordImage.image)
        cv2.imshow('test', strings.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Gata - timp de prelucrare: %s s" % round(time.time() - startTime, 2))

    plot.show()

def fret_detection_test():
    i = 1
    plot.figure(1)
    for filename in os.listdir('Test_images/'):
        print("Fisierul: " + filename + " este in decurs de procesare...")
        startTime = time.time()
        chordImage = Image(path='Test_images/' + filename)
        rotatedImage = rotate_picture(chordImage)
        croppedImage = crop_image(rotatedImage)
        fret = fret_detection(croppedImage)
        '''plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(chordImage.image, cv2.COLOR_BGR2RGB))
        plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(fret.image, cv2.COLOR_BGR2RGB))'''
        cv2.imshow("original", chordImage.image)
        cv2.imshow("Fret", fret.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Gata - timp de prelucrare: %s s" % round(time.time() - startTime, 2))

    plot.show()

def grid_detection_test():
    i = 1
    plot.figure(1)
    for filename in os.listdir('Test_images/'):
        print("Fisierul: " + filename + " este in decurs de procesare...")
        startTime = time.time()
        chordImage = Image(path='Test_images/' + filename)
        rotatedImage = rotate_picture(chordImage)
        croppedImage = crop_image(rotatedImage)
        strings = string_detection(croppedImage)[0]
        fret = fret_detection(croppedImage)
        for string, points in strings.separatingLines.items():
            cv2.line(fret.image, points[0], points[1], (127, 0, 255), 2)

        '''plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(chordImage.image, cv2.COLOR_BGR2RGB))
        plot.subplot(int("42" + str(i)))
        i += 1
        plot.imshow(cv2.cvtColor(fret.image, cv2.COLOR_BGR2RGB))'''
        cv2.imshow("Original", chordImage.image)
        cv2.imshow("Final", fret.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Gata - timp de prelucrare %s s" % round(time.time() - startTime, 2))

    plot.show()

if __name__ == "__main__":
    print("Optiuni: \n1 - Corzi\n2 - Taste\n3 - Corzi si taste")
    choice = input("1/2/3 > ")
    if choice == "1":
        string_detection_test()
    elif choice == "2":
        fret_detection_test()
    elif choice == "3":
        grid_detection_test()
    else:
        print("Invalid")