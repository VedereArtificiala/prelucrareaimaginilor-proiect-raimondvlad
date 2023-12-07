import numpy as np
from matplotlib import pyplot as plt
import cv2

class Image:
    def __init__(self, path=None, img=None):
        if img is None:
            self.image = cv2.imread(path)
        elif path is None:
            self.image = img
        else:
            print("Bad path or image")
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)


    def __str__(self):
        return self.image

    def set_image(self, img):
        self.image = img

    def set_gray(self, grayscale):
        self.gray = grayscale

    def print_image(self, isGray=True):
        if isGray:
            cv2.imshow('image', self.gray)
        else:
            cv2.imshow('image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def print_plot(self, isGray=True):
        if isGray:
            plt.imshow(self.gray, cmap='gray')
        else:
            plt.imshow(self.image)
        plt.show()


    def edges_canny(self,minVal=100, maxVal=200, step=3):
        return cv2.Canny(self.gray, minVal, maxVal, step)

    def edges_LaPlace(self, size=3):
        return cv2.Laplacian(self.gray, cv2.CV_8U, size)

    def edges_SobelX(self, size=3):
        return cv2.Sobel(self.gray, cv2.CV_8U, 1, 0, size)

    def edges_SobelY(self, size=3):
        return cv2.Sobel(self.gray, cv2.CV_8U, 0, 1, size)

    def hough_transform(self, edges, minLineLength, maxLineGap, threshold=15):
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold, minLineLength, maxLineGap)
        return lines