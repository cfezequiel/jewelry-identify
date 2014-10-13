import sys
from os import mkdir

import numpy as np
import cv2

sys.path.append('../')
from jc.image_util import get_image_id

db_file = '../data/spacers/spacers.npz'
src_image_file = '../data/spacers/spacers_3x3.jpg'

# Tile image

## Load color image
image = cv2.imread(src_image_file)

## Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

## Apply Gaussian smoothing
gray_image = cv2.GaussianBlur(gray_image, (5,5), 0)

## Detect edges
def nothing(x):
    pass
cv2.namedWindow('edges')
cv2.createTrackbar('min_val', 'edges', 25, 255, nothing)
cv2.createTrackbar('max_val', 'edges', 43, 255, nothing)

while (1):

    min_val = cv2.getTrackbarPos('min_val', 'edges')
    max_val = cv2.getTrackbarPos('max_val', 'edges')
    edges = cv2.Canny(gray_image, min_val, max_val, L2gradient=True)
    break
    cv2.imshow('edges', edges)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

## Detect lines

cv2.namedWindow('image')
cv2.createTrackbar('thresh', 'image', 172, 255, nothing)

while (1):

    hough_threshold = cv2.getTrackbarPos('thresh', 'image')
    lines = cv2.HoughLines(edges, 1, np.pi/180, hough_threshold)

    ## Draw lines on the color image
    image = cv2.imread(src_image_file)
    COLOR_RED = (0,0,255)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(image,(x1,y1),(x2,y2),COLOR_RED,2)

    # Add border
    image = cv2.copyMakeBorder(image, 2, 2, 2, 2, borderType=cv2.BORDER_CONSTANT, value=(0,0,255))
    cv2.imshow('image', image)

    break

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

## Find bounding boxes and extract tiles
_, _, red_channel_image = cv2.split(image)
ret, threshold_image = cv2.threshold(red_channel_image, 250, 255, 0)
_, contours, _ = cv2.findContours(threshold_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
tile_images = []
tile_min_size = 40000
tile_max_size = 100000
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    roi = image[y:y+h,x:x+w]
    #filter out the non-important tiles
    if roi.size > tile_min_size and roi.size < tile_max_size:
        tile_images.append(roi)

# Match each tile image with database images
dst_dir = 'tiles'
try:
    mkdir(dst_dir)
except OSError as e:
    print 'Directory exists: %s' % dst_dir 
items = {}
for ti in tile_images:
    (id_, nMatches) = get_image_id(ti, db_file)

    # Save tile image with label as filename
    cv2.imwrite(dst_dir + '/' + str(id_) + '.png', ti)

    # Log inventory
    try:
        real_id = id_.split('_')[0]
    except AttributeError:
        real_id = "unknown"
    if items.has_key(real_id):
        items[real_id] += 1
    else:
        items[real_id] = 1
    
# Report matches
for id_, quantity in items.items():
    print '%s:%3d' % (id_, quantity)
