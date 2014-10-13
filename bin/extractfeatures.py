from os import path, listdir
import argparse
import numpy as np
import cv2
import os, errno

# Taken from: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

if __name__ == '__main__':
  # Parse arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('src')
  parser.add_argument('-o', '--output-file')
  args = parser.parse_args()

  # Check if input is regular file or directory
  # TODO: filter out non-image files
  if path.isfile(args.src):
    files = [args.src]
  elif path.isdir(args.src):
    files = [args.src + '/' + f for f in listdir(args.src)]
  else:
    print 'Unknown file.'
    exit(1)

  # Create output file
  output_filename = args.output_file or 'output.npz' 

  descriptors = {}

  # Extract feature descriptors from each image file 
  for filename in files:
    # Read image
    img = cv2.imread(filename, 0)

    # Initialize SIFT detector
    orb = cv2.ORB()

    # Find keypoints and descriptors with SIFT
    kp, des = orb.detectAndCompute(img, None)

    # Store descriptors
    id_ = path.splitext(path.basename(filename))[0]
    descriptors[id_] = des

  np.savez_compressed(output_filename, **descriptors)


