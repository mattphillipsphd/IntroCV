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

    cv2.imwrite(pj(args.directory, "imL_gray.png"), imgL)
    cv2.imwrite(pj(args.directory, "imR_gray.png"), imgL)

    stereo = cv2.StereoSGBM_create(numDisparities=args.num_disparities,
            blockSize=args.block_size, mode=1, P1=1024//8, P2=4096//8)
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

