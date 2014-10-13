from os import path, listdir
import csv
import argparse

import numpy as np
import cv2

### Parameters ####
p_threshold = 200

def image_diff(image1, image2):
    '''Compare two images.'''

    # If arguments are filenames, read the image data
    if type(image1) is str:
        img1 = cv2.imread(image1, 0)
    else:
        img1 = image1

    if type(image2) is str:
        img2 = cv2.imread(image2, 0)
    else:
        img2 = image2

    # Initiate feature detector
    ifd = cv2.ORB()

    # Find keypoints and descriptors
    kp1, des1 = ifd.detectAndCompute(img1, None)
    kp2, des2 = ifd.detectAndCompute(img2, None)

    # Create feature matching object
    fm = cv2.BFMatcher(cv2.NORM_HAMMING)

    # Match descriptors.
    matches = fm.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    # Draw matches
    diff_img = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None,flags=2)

    return diff_img, matches

def get_image_id(sample_img, descriptor_fn):

    # Initiate SIFT detector
    orb = cv2.ORB()

    # Find keypoints and descriptors with SIFT
    try:
      sample_kp, sample_des = orb.detectAndCompute(sample_img, None)
    except:
      print 'Skipped image'
      return (None, 0)

    # Load descriptors from database
    descriptors = np.load(descriptor_fn)

    # Create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    nMatches = 0
    closest_match_id = None
    for id_ in descriptors:
        des = descriptors[id_]
        try:
          matches = bf.match(sample_des, des)
        except:
          print 'Skipped matching...'
          continue
        nMatchesSample = len(matches)
        #print 'ID:', id_, 'No. of matches:', nMatchesSample
        if nMatchesSample > nMatches:
            nMatches = len(matches)
            closest_match_id = id_

    return (closest_match_id, nMatches)


