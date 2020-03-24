#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: main.py
@time:  上午10:06
@desc:
"""
import numpy as np
import cv2
import glob
from utils import *

image_root = 'chess'
corner_size = (9, 6)
square_size = 28

if __name__ == '__main__':
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((corner_size[0]*corner_size[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:corner_size[0],0:corner_size[1]].T.reshape(-1,2)
    objp *= square_size

    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    images = glob.glob(image_root + '/' + '*')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        ret, corners = cv2.findChessboardCorners(gray, corner_size,None)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            img = cv2.drawChessboardCorners(img, corner_size, corners2, ret)
            cv2.imshow('img', cv2.resize(img, (img.shape[1]//4, img.shape[0]//4)))
            cv2.waitKey(40)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None, flags=cv2.CALIB_FIX_K3)
    print(tvecs)

    # 反畸变显示
    for fname in images:
        img = cv2.imread(fname)
        cv2.imshow('origin_img', cv2.resize(img, (img.shape[1]//4, img.shape[0]//4)))
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        cv2.imshow('recitfy_img', cv2.resize(img, (dst.shape[1]//4, dst.shape[0]//4)))
        cv2.waitKey(0)

    save_params(mtx, newcameramtx, dist, roi)

    result_matrix, result_dist, result_new_camera_matrix, result_roi = load_params()
    print(result_matrix)
    print(result_dist)
    print(result_new_camera_matrix)
    print(result_roi)
