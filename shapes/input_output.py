# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:02:14 2015

@author: dominic
"""

import Shape

def read(filepath, filetype="Landmark.exe", shapename=None):
    if shapename == None:
        shapename == filepath
    if filetype=="Landmark.exe":
        n,p = __parse_landmarkexe__(filepath)
        return Shape.Shape(data=p, shape_name=shapename, lm_names=n)
    else:
        raise Exception("Trying to import an unknown file type: %s" % filepath)


def __parse_landmarkexe__(filepath):
    pts = open(filepath, 'r')
    lm_vals = []
    lm_names = []
    header = pts.readline()
    nbr = int(pts.readline().strip())
    data = pts.readlines()[:-1]
    i = 0
    for line in data:
        ln = line.strip().split()
        lm_names.append(ln[0])
        lm_vals.append([float(ln[1]),float(ln[2]),float(ln[3])])
    pts.close()
    return lm_names, lm_vals
