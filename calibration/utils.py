#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: utils.py
@time:  上午10:36
@desc:
"""
import os
import cv2 as cv
import numpy as np
import glob
import xml.etree.ElementTree as ET
import argparse


def load_params(param_file: str = 'camera_params.xml'):
    # result_image_size = image_size
    result_matrix = np.zeros((3, 3), np.float)
    result_new_camera_matrix = np.zeros((3, 3), np.float)
    result_dist = np.zeros((1, 5))
    result_roi = np.zeros(4, np.int)

    if not os.path.exists(param_file):
        print("File {} does not exist.", format(param_file))
        exit(-1)
    tree = ET.parse(param_file)
    root = tree.getroot()
    mat_data = root.find('camera_matrix')
    matrix = dict()
    if mat_data:
        for data in mat_data.iter():
            matrix[data.tag] = data.text
        for i in range(9):
            result_matrix[i // 3][i % 3] = float(matrix['data{}'.format(i)])
    else:
        print('No element named camera_matrix was found in {}'.format(param_file))

    new_camera_matrix = dict()
    new_data = root.find('new_camera_matrix')
    if new_data:
        for data in new_data.iter():
            new_camera_matrix[data.tag] = data.text
        for i in range(9):
            result_new_camera_matrix[i // 3][i % 3] = float(new_camera_matrix['data{}'.format(i)])
    else:
        print('No element named new_camera_matrix was found in {}'.format(param_file))

    dist = dict()
    dist_data = root.find('camera_distortion')
    if dist_data:
        for data in dist_data.iter():
            dist[data.tag] = data.text
        for i in range(5):
           result_dist[0][i] = float(dist['data{}'.format(i)])
    else:
        print('No element named camera_distortion was found in {}'.format(param_file))

    roi = dict()
    roi_data = root.find('roi')
    if roi_data:
        for data in roi_data.iter():
            roi[data.tag] = data.text
        for i in range(4):
            result_roi[i] = int(roi['data{}'.format(i)])
    else:
        print('No element named roi was found in {}'.format(param_file))
    return result_matrix, result_dist, result_new_camera_matrix, result_roi


def save_params(matrix, new_camera_matrix, dist, roi, save_path='camera_params.xml'):
    root = ET.Element('root')
    tree = ET.ElementTree(root)

    mat_node = ET.Element('camera_matrix')
    root.append(mat_node)
    for i, elem in enumerate(matrix.flatten()):
        child = ET.Element('data{}'.format(i))
        child.text = str(elem)
        mat_node.append(child)

    new_node = ET.Element('new_camera_matrix')
    root.append(new_node)
    for i, elem in enumerate(new_camera_matrix.flatten()):
        child = ET.Element('data{}'.format(i))
        child.text = str(elem)
        new_node.append(child)

    dist_node = ET.Element('camera_distortion')
    root.append(dist_node)
    for i, elem in enumerate(dist.flatten()):
        child = ET.Element('data{}'.format(i))
        child.text = str(elem)
        dist_node.append(child)

    roi_node = ET.Element('roi')
    root.append(roi_node)
    for i, elem in enumerate(roi):
        child = ET.Element('data{}'.format(i))
        child.text = str(elem)
        roi_node.append(child)

    tree.write(save_path, 'UTF-8')
    print("Saved params in {}.".format(save_path))

