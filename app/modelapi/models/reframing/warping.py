import cv2
import numpy as np


def warping(img, pts, newSize = 500):
  '''
  example pts = [[1170,200], [3760,100], [3890,2700], [1250,2800]]
  coordinates are ordered such that the first entry in the list is the top-left,
	the second entry is the top-right, the third is the bottom-right, 
  and the fourth is the bottom-left
  '''

  # compute the perspective transform matrix
  dst = np.array([
		[0, 0],
    [0, newSize],
    [newSize, newSize],
		[newSize, 0]], dtype = "float32")
  
  M = cv2.getPerspectiveTransform(pts, dst)

  # apply the transformation matrix 
  warped = cv2.warpPerspective(img, M, (newSize, newSize))

  # return
  return warped