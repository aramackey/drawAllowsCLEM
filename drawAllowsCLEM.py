# -*- coding: utf-8 -*-

"""Option for drawing allows program.
Usage:
prog.py [--scale=<px>] <input_CSV> <output_file>
prog.py [-h | --help]

Options:
  <input_CSV>=required_option   Input file CSV coordinate file.
  <output_file>=require_option  Output file name. File format is JPEG as default.
  --scale=<px>                  Place scale bar at bottom right of the image.
  -h, --help                    show this help message and exit program.
"""

import cv2, csv, sys
import numpy as np
from docopt import docopt
from schema import Schema, And, Or, Use, Optional, SchemaError

def validate_arguments(arguments):
  schema = Schema({
    '<input_CSV>': [Use(open, error="Files should be readable")],
    '<output_file>': [Use(open, error="Files should be readable")],
    '--scale': Or(None, And(Use(int), lambda n: 1<=n), error="--scale should be positive integer greater than 1"),
  })
  arguments = schema.validate(arguments)
  return arguments

# Drawing arrow from start-XY and end-XY coords
def draw_arrow(im, pt1, pt2, color, thickness=1, line_type=8, shift=0, w=5, h=10):
  vx = pt2[0] - pt1[0]
  vy = pt2[1] - pt1[1]
  v  = np.sqrt(vx ** 2 + vy ** 2)
  ux = vx / v
  uy = vy / v
  ptl = (int(pt2[0] - uy*w - ux*h), int(pt2[1] + ux*w - uy*h))
  ptr = (int(pt2[0] + uy*w - ux*h), int(pt2[1] - ux*w - uy*h))
  cv2.line(im, pt1, pt2, color, thickness, line_type, shift)
  cv2.line(im, pt2, ptl, color, thickness, line_type, shift)
  cv2.line(im, pt2, ptr, color, thickness, line_type, shift)

def draw_point(im, pt1, radius, color, thickness=1, line_type=8, shift=0):
  cv2.circle(im, pt1, radius, color, thickness, line_type, shift)

def set_scaleBar(im, scale, thickness):
  offset = int(np.trunc(im.shape[0] - im.shape[0]*0.05))
  start = offset-scale, offset-int(np.trunc(thickness/2))
  end = offset, offset+int(np.trunc(thickness/2))
  print(start, end)
  cv2.rectangle(im, start, end, (0,0,0), -1)

def main():
  arguments = docopt(__doc__)
# arguments = validate_arguments(arguments)
  print(arguments)

  inputImage=arguments['<input_CSV>']
  outputImage=arguments['<output_file>']
#  overwriteImage=argvs[3]

  # Preparing canvas w/ white background
  # Canvas size is 1024x1024x3(RGB)
  size = 1024, 1024, 3
  im = np.zeros(size, dtype=np.uint8)
  im.fill(255)

  # In case, reading image from a file.
#  im = cv2.imread(overwriteImage)
#  im = cv2.imread(outputImage)

  # Opening CSV file
  file = open(inputImage, 'r')
  dataReader = csv.reader(file)

  # Drawing arrows
  for coords_char in dataReader:
    coords = [int(i) for i in coords_char]
    print(coords[0], coords[1], coords[2], coords[3])
    # If the two points have same coordinate, a point will draw insted of an arrow
    if coords[0] == coords [2] and coords[1] == coords [3]:
      draw_point(im,(coords[0],coords[1]), 3, (0,200,0), 2)
      print ("SAME POINT")
    else:
      draw_arrow(im,(coords[0],coords[1]), (coords[2],coords[3]), (0,0,200), 5) 
  file.close()

  # Drawing scale Bar 
  #set_scaleBar(im, 100, 20)
  
  # Displaying to the window
  #cv2.imshow("Test", im)
  #cv2.waitKey(0)
  #cv2.destroyAllWindows()
  #Export as a jpeg image.
  cv2.imwrite(outputImage, im)

if __name__ == '__main__':
  main()
