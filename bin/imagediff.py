import sys

import cv2

from jc.image_util import image_diff

image1 = sys.argv[1] 
image2 = sys.argv[2]

diff_img, matches = image_diff(image1, image2)

cv2.imshow('image', diff_img)
cv2.waitKey(0)

print 'No. of matches:', len(matches)


