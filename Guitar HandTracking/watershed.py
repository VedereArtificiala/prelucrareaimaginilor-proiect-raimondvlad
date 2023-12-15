import numpy as np
from matplotlib import pyplot as plot
from rotate_and_crop import *
from imageModule import Image


def watershed_segmentation(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    fg = cv2.erode(thresh, None, iterations=1)
    bgt = cv2.dilate(thresh, None, iterations=1)

    ret, bg = cv2.threshold(bgt, 1, 128, 1)

    marker = cv2.add(fg, bg)
    canny = cv2.Canny(marker, 110, 150)

    new, contours, hirearchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    marker32 = np.int32(marker)
    cv2.watershed(image, marker32)
    m = cv2.convertScaleAbs(marker32)
    ret, thresh = cv2.threshold(m, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_inv = cv2.bitwise_not(thresh)
    res = cv2.bitwise_and(image, image, mask=thresh)
    res3 = cv2.bitwise_and(image, image, mask=thresh_inv)
    res4 = cv2.addWeighted(res, 1, res3, 1, 0)
    final = cv2.drawContours(res4, contours, -1, (0, 255, 0), 1)

    perimeter_array = []
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, False)
        perimeter_array.append(perimeter)

    sortedData = sorted(zip(perimeter_array, contours), key = lambda x: x[0], reverse=True)

    for j in range(1):
        final = cv2.drawContours(res4, sortedData[j][1], -1,(0, 255, 0), 3)

    plot.imshow(final)
    plot.show()


if __name__ == "__main__":
    chordImage = Image(path="Test_images/ChordImage.jpg")
    rc = crop_image(rotate_picture(chordImage)).image
    watershed_segmentation(cv2.cvtColor(rc, cv2.COLOR_RGB2GRAY))