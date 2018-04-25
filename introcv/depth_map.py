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

    stereo = cv2.StereoBM_create(numDisparities=args.num_disparities,
            blockSize=args.block_size)
    disparity = stereo.compute(imgL,imgR)
    plt.imshow(disparity,'gray')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Image pair " \
            "directory")
    parser.add_argument("-n", "--num-disparities", type=int, default=16)
    parser.add_argument("-b", "--block-size", type=int, default=15)
    args = parser.parse_args()
    main(args)

