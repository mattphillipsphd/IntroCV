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
    vrho = []
    vtheta = []
    vx = []
    vy = []
    if lines is not None:
        for line in lines:
            rho,theta = line[0]
            vrho.append(rho)
            vtheta.append(theta)
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            vx.append(x0)
            vy.append(y0)
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        print("%d lines found with regular Hough transform." %(len(lines)))

    hough_fn = img_fn[:-4] + "_houghlines.png" 
    cv2.imwrite( pj(g_output_dir, hough_fn), img )

    vrho = np.array(vrho)
    vtheta = np.array(vtheta)
    vx = np.array(vx)
    vy = np.array(vy)
    heatmap_fn = hough_fn[:-4] + "_heat.png"
    ut.make_heatmap(vx, vy, pj(g_output_dir, heatmap_fn))


def hough_lines_p(edged, img, img_fn):
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 100, 50, 10)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        print("%d lines found with probabilistic Hough transform." \
                % (len(lines)))

    hough_fn = img_fn[:-4] + "_houghlinesp.png" 
    cv2.imwrite( pj(g_output_dir, hough_fn), img )

def hough_circles(bw, img, img_fn):
    bw = cv2.GaussianBlur(bw, (5,5), 3)
    bw_fn = img_fn[:-4] + "_bw.png"
    cv2.imwrite( pj(g_output_dir, bw_fn), bw )

    circles = cv2.HoughCircles(\
            bw, 
            cv2.HOUGH_GRADIENT, 
            1,              # accumulator resolution (ratio)
            5,              # separation between lines--concentric circles are \
                                # tricky!
            param1=100,     # upper Canny threshold
            param2=50,      # unnormalized accumulator threshold
            minRadius=0,    # smallest allowable radius
            maxRadius=100)  # largest allowable radius

    if circles is not None:
        print("%d circles found." % (len(circles[0,:])))
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        
    hough_fn = img_fn[:-4] + "_houghcircles.png"
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
    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hough_circles(bw, np.copy(img), img_fn)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--image-file", type=str, required=True)
    args = parser.parse_args()
    main(args)    
