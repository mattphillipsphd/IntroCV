"""
Compute a depth map from two images
"""

import argparse
import cv2
import numpy as np
import os

import matplotlib.pyplot as plt

pe = os.path.exists
pj = os.path.join

def main(args):
    imgL = cv2.imread( pj(args.directory, "imL.png"), cv2.IMREAD_GRAYSCALE)
    imgR = cv2.imread( pj(args.directory, "imR.png"), cv2.IMREAD_GRAYSCALE)

    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(imgL,imgR)
    plt.imshow(disparity,'gray')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Image pair " \
            "directory")
    args = parser.parse_args()
    main(args)

