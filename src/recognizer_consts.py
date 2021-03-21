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
MIN_LINES_DIST_COEFF = 0.8
MAX_LINES_DIST_COEFF = 1.2
MIN_GAP_COEFF = 1.7

MIN_COEFF = 0.2 #RENAME!

METHOD = cv2.HOUGH_GRADIENT
DP = 2
PARAM1 = 200

MIN_INTERSECTION_DIST_COEFF = 0.15

WHITE_THRESHOLD = 240
BLACK_THRESHOLD = 5