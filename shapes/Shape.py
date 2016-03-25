# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:10:40 2015

@author: dominic
"""

import numpy as np, math

class Shape:
    """
    A class that represents an individual landmark configuration.
    """
    
    def __init__(self, data=None, shape_name=None, lm_names=None):
        self.landmarks = []
        self.n_landmarks=0
        self.n_dim = 0
        if data != None:
            self.landmarks = data
            self.n_landmarks = len(data)
            self.n_dim = len(data[0])
        self.centroid_size = None
        self.name = shape_name
        self.lm_names = lm_names
    
    def add_landmark(self, point):
        if not self.n_dim == 0:
            assert(len(point)==self.n_dim)
        else:
            self.n_dim = len(point)
        self.landmarks.append(point)
        self.n_landmarks+=1
    
    def as_nparray(self):
        return np.array(self.landmarks)
    
    def is_complete(self):
        for p in self.landmarks:
            if self.__point_present__(p) == False:
                return False
        return True

    def __point_present__(self, pt):
        is_correct = True
        for i in pt:
            if math.isnan(i):
                is_correct=False
        return is_correct


