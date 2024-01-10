from collections import defaultdict
import numpy as np
from rotate_and_crop import *

def skin_detection(image):
    np.seterr(over='ignore')
    for indexLine, line in enumerate(image):
        for indexPixel, pixel in enumerate(line):
            if pixel[2] > 95 and pixel[1] > 40 and pixel[0] > 20 and max(pixel) - min(pixel) > 15 and abs(pixel[2] - pixel[1]) > 15 and pixel[2] > pixel[0] and pixel[2] > pixel[1] and indexPixel > len(line) / 2:
                # image[indexLine][indexPixel] = (255, 255, 255)
                pass
            else:
                image[indexLine][indexPixel] = (0, 0, 0)

    np.seterr(over='warn')
    return image

def locate_hand(image):
    global currentDensity
    height = len(image)
    width = len(image[0])
    handRegion = np.zeros((height, width, 3), np.uint8)

    xDict = defaultdict(int)
    for line in image:
        for j, pixel in enumerate(line):
            if pixel.any() > 0:

                xDict[j] += 1

    if not xDict:
        return handRegion

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
        if maxXDensity - m == minX:
            break
        m += 1
        currentDensity = xDict[maxXDensity - m]
        if currentDensity < 0.1 * maxDensity:
            break
        elif currentDensity < 0.5 * lastDensity:
            break
        lastDensity = currentDensity

    n = 0
    lastDensity = currentDensity

    while 1:
        if maxXDensity +n == maxX:
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
    maxLimit = maxXDensity + n + tolerance

    for i, line in enumerate(image):
        for j, pixel in enumerate(line):
            if minLimit < j < maxLimit:
                handRegion[i][j] = image[i][j]
    return handRegion

def hand_detection(skin):

    neck = Image(img=skin)
    neck.set_image(locate_hand(skin_detection(neck.image)))
    neck.set_image(cv2.medianBlur(neck.image, 5))
    neck.set_gray(cv2.cvtColor(neck.image, cv2.COLOR_BGR2GRAY))
    cannyEdges = neck.edges_canny(minVal=70, maxVal=100)

    circles = cv2.HoughCircles(cannyEdges, cv2.HOUGH_GRADIENT, 1, 5,
                               param1=100, param2=20, minRadius=20, maxRadius=90)
    if circles is None:
        pass
    else:
        circles = np.uint16(np.around(circles))


    for i in circles[0, :]:

        cv2.circle(neck.image, (i[0], i[1]), i[2], (0, 255, 0), 2)

        cv2.circle(neck.image, (i[0], i[1]), 2, (0, 0, 255), 3)

    return cv2.cvtColor(cannyEdges, cv2.COLOR_GRAY2BGR), neck.image

def refine_hand(neck, skin):

    # Vrem sa verificam unde sunt liniile corzilor, daca nu se gaseste nicio coarda, inseamna ca mana le acopera

    height = len(neck.image)
    width = len(neck.image[0])
    neckWithStrings = np.zeros((height, width, 3), np.uint8)

    edges = neck.edges_sobelY()
    edges = threshold(edges, 127)

    lines = neck.hough_transform(edges, 50, 20)
    size = len(lines)

    for x in range(size):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(neckWithStrings, (x1, y1), (x2, y2), (255, 255, 255), 2)

    neckStrings = Image(img=neckWithStrings)
    neckStringsGray = neckStrings.gray

    # Divizam imaginea cu bratul chitarii in patrate de 40*40 px. Daca detectam coarda prin patratul respectiv il evitam

    squareSize = 40
    xNb = width // squareSize
    yNb = height // squareSize

    for i in range(yNb):
        for j in range(xNb):
            linesInSquareLeft = 0
            linesInSquareRight = 0
            skinInSquareBelow = 0
            for k in range(i * squareSize, min(( i  + 1) * squareSize, height)):
                if neckStringsGray[k][j * squareSize] > 0:
                    linesInSquareLeft += 1
                if neckStringsGray[k][min((j + 1) * squareSize, width)] > 0:
                    linesInSquareRight += 1
            for l in range(j * squareSize, min((j + 1) * squareSize, width)):
                if skin[min((i + 1) * squareSize, height -1)][l].any() > 0:
                    skinInSquareBelow += 1
            if linesInSquareLeft > 1 and linesInSquareRight > 1:
                for k in range(i * squareSize, min ((i + 1) * squareSize, height)):
                    for l in range(j * squareSize, min((j + 1) * squareSize, width)):
                        skin[k][l] = (0, 0, 0)
    return skin

if __name__ == "__main__":
    print("Pentru rezultate ruleaza fingers_detection_test.py")