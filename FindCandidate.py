import cv2
import numpy as np
import matplotlib.pyplot as plt
from level4.CandidateData import CandidateData

class FindCandidate:
    def __init__(self):
        pass

    def run(self, image):
        res = self.find_red_lights(image)
        x_red, y_red = self.find_indexes(res)
        res = self.find_green_lights(image)
        x_green, y_green = self.find_indexes(res)
        plt.plot(x_red, y_red, 'ro', color='r', markersize=4)
        plt.plot(x_green, y_green, 'ro', color='g', markersize=4)
        self.candidate_data = CandidateData(x_red, y_red, x_green, y_green)
        return self.candidate_data

    def find_indexes(self, image):
        indices = np.where(np.all(image != 0, axis=-1))
        # coords = list(zip(indices[0], indices[1]))
        return indices[1], indices[0]

    def find_red_lights(self, c_image: np.ndarray, **kwargs):
        print(c_image)
        im = cv2.imread(c_image , 1)
        result = im.copy()
        image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        lower = np.array([120, 20, 60])
        upper = np.array([240, 90, 90])
        mask = cv2.inRange(image, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        return result

    def find_green_lights(self,c_image: np.ndarray, **kwargs):
        im = cv2.imread(c_image, 1)
        result = im.copy()
        image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        lower = np.array([30, 140, 150])
        upper = np.array([200, 200, 255])
        mask = cv2.inRange(image, lower, upper)
        result = cv2.bitwise_and(result, result, mask=mask)
        plt.imshow(result)
        return result


