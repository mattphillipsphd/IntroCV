"""
Implementation of Hough transform
"""

import argparse
import cv2
import os
import utils as ut

pe = os.path.exists
pj = os.path.join

def main(args):
    img_dir = pj( ut.get_repo_dir(), "data/hough" )
    img = cv2.imread(


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--image-file", type=str, required=True)
    args = parser.parse_args()
    main(args)    
