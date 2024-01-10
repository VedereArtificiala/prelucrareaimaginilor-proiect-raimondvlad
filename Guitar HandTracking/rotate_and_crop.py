from imageModule import Image
from functions import *
from statistics import median
from math import inf

def rotate_picture(image):

    imageToBeRotated = image.image

    edges = image.edges_SobelY()
    edges = threshold(edges, 127)

    lines = image.hough_transform(edges, 50, 50)

    slopes = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slopes.append(abs((y2 - y1) / (x2 - x1)))
    median_slope = median(slopes)
    angle = median_slope

    return Image(img=rotate(imageToBeRotated, -angle))

def crop_image(image):

    imageToBeCroped = image.image

    edges = image.edges_SobelY()
    edges = threshold(edges, 120)

    lines = image.hough_transform(edges, 30, 20)
    y = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            y.append(y1)
            y.append(y2)

    ySort = list(sorted(y))
    yDifferences = [0]

    firstY = 0
    lastY = inf

    for i in range(len(ySort) - 1):
        yDifferences.append(ySort[i + 1] - ySort[i])
    for i in range(len(yDifferences) - 1):
        if yDifferences[i] == 0:
            lastY = ySort[i]
            if i > 3 and firstY == 0:
                firstY = ySort[i]
    return Image(img=imageToBeCroped[firstY: lastY])


if __name__ == "__main__":
    print("Pentru rezultate se ruleaza rotate_and_crop_test.py")