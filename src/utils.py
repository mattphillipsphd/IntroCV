"""
Simple utilities
"""

import cv2
import json
import numpy as np
import os
import sys

pe = os.path.exists
pj = os.path.join

def get_repo_dir():
    if pe("local_cfg.json"):
        cfg_path = "local_cfg.json"
    elif pe("../local_cfg.json"):
        cfg_path = "../local_cfg.json"
    else:
        raise RuntimeError("local_cfg.json file not present")
    cfg = json.load( open(cfg_path) )
    return cfg["repo_dir"]

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

