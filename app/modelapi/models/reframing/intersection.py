import numpy as np

def line(p1, p2):
  '''
  Produces coefs A, B, C of line equation by two points provided
  Ex: L1 = line([2,3], [4,0]) --> L1 = (3, 2, 12)
  '''
  A = (p1[1] - p2[1])
  B = (p2[0] - p1[0])
  C = (p1[0]*p2[1] - p2[0]*p1[1])
  return A, B, -C

def intersection(L1, L2):
  '''
  Finds intersection point (if any) of two lines provided by coefs.
  Ex: L1 = line([0,1], [2,3])
      L2 = line([2,3], [4,0])
      intersec = intersection(L1,L2) --> intersec = [2, 3]

      L1 = line([0,1], [2,3])
      L2 = line([0,2], [2,4])
      intersect = intersection(L1,L2) --> None
  '''
  D  = L1[0] * L2[1] - L1[1] * L2[0]
  Dx = L1[2] * L2[1] - L1[1] * L2[2]
  Dy = L1[0] * L2[2] - L1[2] * L2[0]

  if D != 0:
    x = Dx / D
    y = Dy / D
    return [int(x), int(y)]
  else:
    return None

def get_lines_intersections(pts, ncols = 1e158, nrows = 1e158):
  '''
  Input: A list of 4 consecutive lines
         Ex: [[[1,2], [3,4]], # line 1 passes through point [1,2] and [3,4]
              [[5,6], [7,8]],
              [[9,10], [11,12]],
              [[13,14], [15,16]]]

  Compute: The intersection between each consecutive lines
           If the intersection falls outside the image, it is projected on the image

  Return: A new contour with the 4 line intersections/the 4 new corners
          Ex: array([[[3, 0]],
                    [[3, 3]],
                    [[0, 3]],
                    [[0, 0]]], dtype=int32)

  '''
  C = [0, 1, 2, 3, 0] 
  newCnt = []

  assert len(pts) == 4, 'There are more than 4 points in the input list'

  for corner in range(4):

    # First line
    p1 = pts[C[corner]]
    L1 = line(p1[0], p1[1])

    # Second line 
    p2 = pts[C[corner+1]]
    L2 = line(p2[0], p2[1])
    
    # Find intersection
    inter = intersection(L1, L2)
    assert inter, 'could not find any intersection between 2 lines'

    # Projection on the image
    inter = [max(0,min(ncols, inter[0])), max(0,min(nrows, inter[1]))]

    newCnt.append([inter])

  newCnt = np.array(newCnt, dtype = "int32")
  #print('New estimated corners:', newCnt.tolist())

  return newCnt