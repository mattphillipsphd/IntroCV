"""
Simple utilities
"""

import cv2
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

pe = os.path.exists
pj = os.path.join

# Thanks
# https://www.pyimagesearch.com/2015/04/06/
#zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
def detect_edges(image, sigma=0.333):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged


def get_repo_dir():
    if pe("local_cfg.json"):
        cfg_path = "local_cfg.json"
    elif pe("../local_cfg.json"):
        cfg_path = "../local_cfg.json"
    else:
        raise RuntimeError("local_cfg.json file not present")
    cfg = json.load( open(cfg_path) )
    return cfg["repo_dir"]


def make_heatmap(X, Y, fn, bins=(64,64), xlabel="x", ylabel="y"):
    heatmap, xedges, yedges = np.histogram2d(X, Y, bins=bins)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
     
    # Plot heatmap
    plt.clf()
    plt.ylabel(xlabel)
    plt.xlabel(ylabel)
    plt.imshow(heatmap, extent=extent, origin="lower")
    ax = plt.gca()
    ax.set_aspect("equal", "box")
    plt.savefig(fn)


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

