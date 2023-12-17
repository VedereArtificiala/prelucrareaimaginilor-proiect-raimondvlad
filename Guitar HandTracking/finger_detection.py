import numpy as np
from collections import defaultdict
from rotate_and_crop import *


def skin_detect(img):

    for index_line, line in enumerate(img):
        for index_pixel, pixel in enumerate(line):
            if pixel[2] > 95 and pixel[1] > 40 and pixel[0] > 20 and max(pixel) - min(pixel) > 15 and abs(pixel[2] - pixel[1] > 15 and pixel[2] > pixel[0] and pixel[2] > pixel[1] and index_pixel > len(line) / 2):
                # img[index_line][index_pixe] = (255, 255, 255)
                pass
            else:
                img[index_line][index_pixel] = (0, 0, 0)
    return img

def locate_hand(img):
    height = len(img)
    width = len(img[0])
    hand = np.zeros((height, width, 3), dtype=np.uint8)

    xDict = defaultdict(int)

    for line in img:
        for j, pixel in enumerate(line):
            if pixel.all() > 0:
                xDict[j] += 1

    maxDensity = max(xDict.values())
    maxXDensity = 0
    for x, density in xDict.items():
        if density == maxDensity:
            maxXDensity = x
            break
    minX = min(xDict.keys())
    maxX = max(xDict.keys())

    m = 0
    lastDensity = xDict[maxDensity]

    while 1:
        if maxDensity - m == minX:
            break
        m += 1
        currentDensity = xDict[maxXDensity - m]
        if currentDensity < 0.1 * maxDensity:
            break
        elif currentDensity < 0.5 * lastDensity:
            break
        lastDensity = currentDensity

    n = 0
    lastDensity = xDict[maxDensity]

    while 1:
        if maxXDensity + n == maxX:
            break
        n += 1
        currentDensity = xDict[maxXDensity + n]
        if currentDensity < 0.1 * maxDensity:
            break
        elif currentDensity < 0.5 * lastDensity:
            break
        lastDensity = currentDensity

    tolerance = 20
    minLimit = maxXDensity - m - tolerance
    maxLimit = maxXDensity + m + tolerance

    for i, line in enumerate(img):
        for j, pixel in enumerate(line):
            if minLimit < j < maxLimit:
                hand[i][j] = img[i][j]
    return hand

def hand_detection(img):

    image = Image(img=img)
    image.set_image(locate_hand(skin_detect(image.image)))
    image.set_gray(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    edges = image.edges_canny(minVal=70, maxVal=100, aperture=3)

    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 5, param1=100, param2=20, minRadius=20, maxRadius=90)
    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:

        cv2.circle(image.image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(image.image, (i[0], i[1]), 2, (0, 0, 255), 3)

    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), image.image

if __name__ == '__main__':
    print("Pentru teste - finger_detection_test.py")