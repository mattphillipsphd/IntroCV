"""
This example creates 'funhouse mirror' transformations, (piecewise linear)
"""

import argparse
import cv2
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

from skimage.transform import PiecewiseAffineTransform, warp
from skimage import data as skdata

pe = os.path.exists
pj = os.path.join


def main(args):
    if len(args.image_file)==0:
        image = skdata.astronaut()
    else:
        if not pe(args.image_file):
            raise RuntimeError("Image file %s not found" % (args.image_file))
        image = cv2.imread(args.image_file)
    num_rows,num_cols = image.shape[0], image.shape[1]

    src_cols = np.linspace(0, num_cols, 3)
    src_rows = np.linspace(0, num_rows, 3)
    src_rows,src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]

    newx = np.clip(np.random.rand() * num_cols, 10, num_cols-10)
    newy = np.clip(np.random.rand() * num_rows, 10, num_rows-10)

    dst_rows = src_rows.copy()
    dst_cols = src_cols.copy()
    dst_rows[1] = newy
    dst_cols[1] = newx
    dst = np.dstack([dst_cols.flat, dst_rows.flat])[0]
#    dst = np.vstack([dst_cols, dst_rows]).T

    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst)

    out_rows = num_rows
    out_cols = num_cols
    out = warp(image, tform, output_shape=(out_rows, out_cols))

    fig, ax = plt.subplots()
    ax.imshow(out)
    ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.b')
    ax.axis((0, out_cols, out_rows, 0))
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--image-file", type=str, default="")
    args = parser.parse_args()
    main(args)

