from strings import Strings
from rotate_and_crop import *
import cv2
import numpy as np
from collections import defaultdict


def string_detection(neck):

    height = len(neck.image)
    width = len(neck.image[0])
    neck_with_strings = np.zeros((height, width, 3), np.uint8)
    # Pasul 1: se detecteaza corzile folosing transformata Hough si se formeaza o imagine bazata pe asta
    edges = neck.edges_SobelY()
    edges = threshold(edges, 120)

    lines = neck.hough_transform(edges, 30, 10)   # To do: calibrearea automata a parametrilor
    size = len(lines)
    for x in range(size):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(neck_with_strings, (x1, y1), (x2, y2), (255, 255, 255), 2)

    neck_str = Image(img=neck_with_strings)
    neck_str_gray = neck_str.gray

    # Pasul 2: se decupeaza imaginea pe sectiuni verticale la diferinte puncte si se calucleaza spatiile dintre corzi
    slices = {}
    nb_slices = int(width / 40)
    print(nb_slices)
    for i in range(nb_slices):
        slices[(i + 1) * nb_slices] = []

    for index_line, line in enumerate(neck_str_gray):
        for index_pixel, pixel in enumerate(line):
            if pixel == 255 and index_pixel in slices:
                slices[index_pixel].append(index_line)

    slices_difference = {}
    for k in slices.keys():
        temp = []
        n = 0
        slices[k] = list(sorted(slices[k]))
        for p in range(len(slices[k]) - 1):
            temp.append(slices[k][p + 1] - slices[k][p])
            if slices[k][p + 1] - slices[k][p] > 1:
                n += 1
        slices_difference[k] = temp

    points = []
    points_dict = {}
    for j in slices_difference.keys():
        gaps = [g for g in slices_difference[j] if g > 1]
        points_dict[j] = []

        if len(gaps) > 2:
            median_gap = median(gaps)
            for index, diff in enumerate(slices_difference[j]):
                if abs(diff - median_gap) < 4:
                    points_dict[j].append((j, slices[j][index] + int(median_gap / 2)))
                elif abs(diff / 2 - median_gap) < 4:
                    points_dict[j].append((j, slices[j][index] + int(median_gap / 2)))
                    points_dict[j].append((j, slices[j][index] + int(3 * median_gap / 2)))

        points.extend(points_dict[j])
    '''for p in points:
        print(p)
        cv2.circle(neck.image, p, 3, (0, 255, 0), -1)
    plt.imshow(cv2.cvtColor(neck.image, cv2.COLOR_BGR2RGB))
    plt.show()'''

    points_divided = [[] for i in range(5)]
    for s in points_dict.keys():
        for i in range(6):
            try:
                cv2.circle(neck.image, points_dict[s][i], 3, (255, 0, 0), -1)
                points_divided[i].append(points_dict[s][i])
            except IndexError:
                pass
    if len(points_divided) < 6:
        last_line_points = points_divided[-1]
        x, y = last_line_points[0]
        y += 10
        points_divided.append([(x, y)])

    '''angle_threshold = 5

    for i in range(5):
        cnt = np.array(points_divided[i])
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L12, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180.0 / np.pi

        if abs(angle) > angle_threshold:
            points_divided[5] = [(x, y + 15)]'''
    # Pasul 3: Se formeaza linii care separe fiecare coarda in parte
    tuning = ["E", "A", "D", "G", "B", "E6"]
    strings = Strings(tuning)

    for i in range(6):
        cnt = np.array(points_divided[i])
        [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L12, 0, 0.01, 0.01)

        left_extreme = int((-x * vy / vx) + y)
        right_extreme = int(((width - x) * vy / vx) + y)

        strings.separatingLines[tuning[i]] = [(width - 1, right_extreme), (0, left_extreme)]

        cv2.line(neck.image, (width - 1, right_extreme), (0, left_extreme), (0, 0, 255), 2)

    return strings, Image(img=neck.image)


def fret_detection(neck):

    height = len(neck.image)
    width = len(neck.image[0])
    neck_with_frets = np.zeros((height, width, 3), np.uint8)

    # 1. Detectam tastele cu transformata Hough
    edges = neck.edges_SobelX()
    edges = threshold(edges, 100)
    #edges = cv2.medianBlur(edges, 3)

    lines = neck.hough_transform(edges, 30, 10)  # To DO:Calibrarea parametrilor automata daca e posibila
    size = len(lines)

    for x in range(size):
        for x1, y1, x2, y2 in lines[x]:
            cv2.line(neck_with_frets, (x1, y1), (x2, y2), (255, 255, 255), 2)


    # 2. Decupam imaginea pe orizonatala la diferite puncte si calculam spatiile dintre tastiere
    slices = {}
    nb_slices = int(height / 50)
    for i in range(nb_slices):
        slices[(i + 1) * nb_slices] = []

    for index_line, line in enumerate(edges):
        for index_pixel, pixel in enumerate(line):
            if pixel == 255 and index_line in slices:
                slices[index_line].append(index_pixel)

    slices_differences = {}
    for k in slices.keys():
        temp = []
        n = 0
        slices[k] = list(sorted(slices[k]))
        for p in range(len(slices[k]) - 1):
            temp.append(slices[k][p + 1] - slices[k][p])
            if slices[k][p + 1] - slices[k][p] > 1:
                n += 1

            slices_differences[k] = temp

    xValues = defaultdict(int)
    for j in slices_differences.keys():
        for index, gap in enumerate(slices_differences[j]):
            if gap:
                xValues[slices[j][index]] += 1
    potentialFrets = []
    xValues = dict(xValues)
    for x, nb in xValues.items():
        if nb > 1:
            potentialFrets.append(x)

    potentialFrets = list(sorted(potentialFrets))
    potentialFrets = remove_duplicate(potentialFrets)
    print(potentialFrets)
    # 3. Sortam tastele potentiale verificand un raport si reconstruind tastele care lipsesc
    potentialRatio = []
    for i in range(len(potentialFrets) - 1):
        potentialRatio.append(round(potentialFrets[i + 1] / potentialFrets[i], 3))
    ratio = potentialRatio[-1]
    lastX = potentialFrets[-1]
    while 1:
        lastX *= ratio
        if lastX >= width:
            break
        else:
            potentialFrets.append(int(lastX))
    for x in potentialFrets:
        cv2.line(neck.image, (x, 0), (x, height), (127, 0, 255), 2)

    return Image(img=neck.image)


if __name__ == "__main__":
    print("Pentru rezultate compila programul grid_detection_test.py")
