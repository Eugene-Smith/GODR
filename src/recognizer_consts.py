import numpy as np
import cv2

CANNY_THRESHOLD1 = 100
CANNY_THRESHOLD2 = 200

HOUGH_RHO = 1
HOUGH_THETA = np.pi / 180

VERTICAL_TAN_MIN = 50
HORIZONTAL_TAN_MAX = 0.02

MIN_DIST = 10

HOUGH_LOW_THRESHOLD = 50
HOUGH_HIGH_THRESHOLD = 200
MIN_LINES_DIST_COEFF = 0.7
MIN_GAP_COEFF = 1.5

METHOD = cv2.HOUGH_GRADIENT
DP = 2
PARAM1 = 200
PARAM2 = 15
MIN_DIST_COEFF = 0.9
MAX_R_COEFF = 0.5
MIN_R_COEFF = 0.5

MIN_INTERSECTION_DIST_COEFF = 0.3

WHITE_THRESHOLD = 255/2