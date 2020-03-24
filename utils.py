#!/home/hdh3/anaconda3/bin/python
# encoding: utf-8
"""
@author: red0orange
@file: utils.py
@time:  上午11:25
@desc:
"""


def distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)