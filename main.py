#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: main.py
@time:  下午10:19
@desc:
"""
import cv2
import numpy as np
from pnpsolver import PnPSolver
from calibration.utils import load_params
from utils import *


Blue_Range = [[0, 255], [0, 255], [0, 60]]
Orange_Range = [[0, 54], [0, 112], [116, 255]]

if __name__ == '__main__':
    cap = cv2.VideoCapture('video/镜像(到点停留).avi')

    matrix, dist, new_camera_matrix, roi = load_params('calibration/camera_params.xml')
    pnp_solver = PnPSolver(cam_matrix=matrix, dist_coeffs=dist)
    # pnp_solver.set_target_points_3d(np.array([[-100, 50, 0], [100, 50, 0], [100, -50, 0], [-100, -50, 0]], dtype=np.float))
    pnp_solver.set_target_points_3d(np.array([[-50, 100, 0], [50, 100, 0], [50, -100, 0], [-50, -100, 0]], dtype=np.float))

    last_point = None
    map = np.zeros([1000, 1000], dtype=np.uint8)
    cv2.line(map, (0, 500), (1000, 500), 255, 2)
    cv2.circle(map, (500, 500), 3, 255, -1)
    while True:
        _, origin = cap.read()
        cv2.imwrite('test.png', origin)

        origin = cv2.flip(origin, 1)

        blud_binary = cv2.inRange(origin, np.array([i[0] for i in Blue_Range]), np.array([i[1] for i in Blue_Range]))
        orange_binary = cv2.inRange(origin, np.array([i[0] for i in Orange_Range]), np.array([i[1] for i in Orange_Range]))

        _, contours, _ = cv2.findContours(blud_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # _, contours, _ = cv2.findContours(orange_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(origin, contours, 0, (0, 255, 0), 1)

        largest_contour = None
        max_area = -1
        for contour in contours:
            if cv2.contourArea(contour) > max_area:
                largest_contour = contour
                max_area = cv2.contourArea(contour)

        rrect = cv2.minAreaRect(largest_contour)
        points = cv2.boxPoints(rrect)
        points = np.int0(points)
        cv2.drawContours(origin, [points], 0, (0, 255, 0), 1)
        x, y, z = pnp_solver.get_position_in_PTZ(points)
        # TODO why add - ???
        x = -x
        print(x, y, z)

        x_z_point = np.array([x, z])
        if last_point is not None:
            if distance(x_z_point, last_point) > 500:
                continue
            x_z_point /= 10
            last_point /= 10
            x_z_point += 500
            last_point += 500
            x_z_point = x_z_point.astype(np.int)
            last_point = last_point.astype(np.int)
            cv2.line(map, tuple(last_point.tolist()), tuple(x_z_point.tolist()), 255, 1)
        last_point = np.array([x, z])

        cv2.imshow('map', map)
        cv2.imshow('origin', origin)
        cv2.waitKey(0)


        # cv2.imshow('blue_binary', blud_binary)
        # cv2.imshow('orange_binary', orange_binary)
        cv2.waitKey(50)
    pass