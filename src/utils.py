"""
Simple utilities
"""

import cv2
import numpy as np
import os
import sys

pe = os.path.exists
pj = os.path.join

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
g_repo_dir = os.path.dirname( get_script_path() )

# Aspect ratio is preserved and the image is not cropped.  
# new_size: The size of the shortest dimension of the new image, in pixels
def resize_and_convert(directory, new_size):
    for jpg in [f for f in os.listdir(directory) if f.endswith(".jpg")]:
        img = cv2.imread( pj(directory, jpg) )
        small_dim = np.min(img.shape[:2])
        ratio = new_size / small_dim
        new_hw = [int(round(x*ratio)) for x in img.shape[:2]][::-1]
        resz_img = cv2.resize(img, tuple(new_hw))
        png = jpg[:-3] + "png"
        cv2.imwrite(pj(directory, png), resz_img)

