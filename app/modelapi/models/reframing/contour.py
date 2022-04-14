import cv2
import imutils
import numpy as np


def find_contour(mask):
    # find the contours of the mask
    cnts = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    # keep only the biggest one
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
    cnts = cnts[0]

    assert cnts.shape[1:] == (1, 2), "cnts.shape[1:] should be (1,2)"

    return cnts


def minimum_area_enclosing(cnts):
  """
Find the minimum-area rotated rectangle that encloses the given contour
"""
    rect = cv2.minAreaRect(cnts)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    screenCnt = np.array([[i] for i in box.tolist()])
    # print('Estimated corners:', screenCnt.tolist())
    return screenCnt


def fit_lines_on_edges(cnts, screenCnt, rows, cols, threshold=100, epsilon=100):
  """
  Input:
  - cnts: the full contour
  - screenCnt: 4 estimated corners of the contour, obtained with methods 1 or 2

  Steps:
  - For each side, delimited by 2 consecutive corners of screenCnt (c1 and c2)
  - Find all the points of cnts that are located between c1 and c2 (+- margin)
  - Fit a line, using cv2.fitLine, on these points

  Output:
  - pts: the list of the 4 fitted lines
       Ex: [[[1,2], [3,4]], # line 1 passes through point [1,2] and [3,4]
            [[5,6], [7,8]],
            [[9,10], [11,12]],
            [[13,14], [15,16]]]
  """

  assert screenCnt.shape == (4, 1, 2), 'screenCnt.shape should be (4, 1, 2)'

    X = [i[0][0] for i in cnts]
    Y = [i[0][1] for i in cnts]

    lefty = []
    righty = []
    leftx = []
    rightx = []
    cutCnt = []
    C = [0, 1, 2, 3, 0]

    for edge in range(4):
        # define 2 extreme points of the edge
        c1 = screenCnt[C[edge]][0]
        c2 = screenCnt[C[edge + 1]][0]

        # select all the contour points that are located between these 2 points +- margin --> cutCnt
        if abs(c1[0] - c2[0]) < threshold:  # if the 2 pts have almost the same abscissa
            c_mean = (c1[0] + c2[0]) / 2
            X_margin = [max(0, c_mean - epsilon), min(c_mean + epsilon, cols)]
            Y_margin = sorted([c1[1], c2[1]])

        elif abs(c1[1] - c2[1]) < threshold:  # if the 2 pts have almost the same ordinate
            c_mean = (c1[1] + c2[1]) / 2
            X_margin = sorted([c1[0], c2[0]])
            Y_margin = [max(0, c_mean - epsilon), min(c_mean + epsilon, rows)]

        else:
            X_margin = sorted([c1[0], c2[0]])
            Y_margin = sorted([c1[1], c2[1]])

        c = [[[X[ind], Y[ind]]] for ind in range(len(X)) if
             X_margin[0] <= X[ind] <= X_margin[1] and Y_margin[0] <= Y[ind] <= Y_margin[1]]
        cutCnt.append(np.array(c))

        # fit a line on c
        [vx, vy, x, y] = cv2.fitLine(np.array(c), cv2.DIST_L2, 0, 0.01, 0.01)

        # append the result for this edge to left and right points
        leftx.append(0)
        rightx.append(cols)
        lefty.append(int((-x * vy / vx) + y))
        righty.append(int(((cols - x) * vy / vx) + y))

    pts = [[[leftx[ind], lefty[ind]], [rightx[ind], righty[ind]]] for ind in range(4)]
    return pts
