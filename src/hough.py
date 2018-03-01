"""
Running and visualizing the OpenCV Hough transform
"""

import argparse
import cv2
import numpy as np
import os
import utils as ut

pe = os.path.exists
pj = os.path.join

g_output_dir = None

def hough_lines(edged, img, img_fn):
    lines = cv2.HoughLines(edged, 1, np.pi/180, 100)
    if lines is not None:
        for line in lines:
            rho,theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    hough_fn = img_fn[:-4] + "_houghlines.png" 
    cv2.imwrite( pj(g_output_dir, hough_fn), img )

def hough_lines_p(edged, img, img_fn):
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 100, 10, 10)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    hough_fn = img_fn[:-4] + "_houghlinesp.png" 
    cv2.imwrite( pj(g_output_dir, hough_fn), img )

def main(args):
    global g_output_dir
    g_output_dir = pj( ut.get_repo_dir(), "out/hough" )
    img_dir = pj( ut.get_repo_dir(), "data/hough" )
    img_fn = args.image_file
    img = cv2.imread( pj(img_dir, img_fn) )
    edged = ut.detect_edges(img)
    edged_fn = img_fn[:-4] + "_edged.png"
    cv2.imwrite( pj(g_output_dir, edged_fn), edged )

    hough_lines(np.copy(edged), np.copy(img), img_fn)
    hough_lines_p(np.copy(edged), np.copy(img), img_fn)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--image-file", type=str, required=True)
    args = parser.parse_args()
    main(args)    
