#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: pnpsolver.py
@time:  下午10:39
@desc:
"""
import cv2
import numpy as np
import os


class PnPSolver(object):
    def __init__(self, target_points_3d=None, cam_matrix=None, dist_coeffs=None):
        self.cam_matrix = cam_matrix
        self.dist_coeffs = dist_coeffs
        self.target_points_3d = target_points_3d
        pass

    def set_cam_matrix(self, cam_matrix):
        self.cam_matrix = cam_matrix
        pass

    def set_dist_coeffs(self, dist_coeffs):
        self.dist_coeffs = dist_coeffs
        pass

    def set_target_points_3d(self, target_points_3d):
        self.target_points_3d = target_points_3d
        pass

    def sort_points(self, points):
        if points.shape[0] != 4:
            raise BaseException('error input')
        result_index = [0, 1, 2, 3]
        xs = points[:, 0]
        ys = points[:, 1]
        index_x = list(np.argsort(xs))
        index_y = list(np.argsort(ys))
        left = index_x[:2]
        if index_y.index(left[0]) > index_y.index(left[1]):
            result_index[0] = left[1]
            result_index[3] = left[0]
        else:
            result_index[0] = left[0]
            result_index[3] = left[1]
        right = index_x[2:]
        if index_y.index(right[0]) > index_y.index(right[1]):
            result_index[1] = right[1]
            result_index[2] = right[0]
        else:
            result_index[1] = right[0]
            result_index[2] = right[1]
        return points[result_index, ...]

    def get_position_in_PTZ(self, points2d):
        points2d = self.sort_points(points2d)
        points2d = np.array(points2d, dtype=np.float)
        x, y, z = None, None, None
        points2d = np.ascontiguousarray(points2d[:, :2]).reshape([points2d.shape[0], 1, 2])
        retval, rvec, tvec = cv2.solvePnP(self.target_points_3d,
            points2d, self.cam_matrix, self.dist_coeffs, None, None, False, flags=cv2.SOLVEPNP_P3P)
        x, y, z = tvec[:3]
        return x[0], y[0], z[0]