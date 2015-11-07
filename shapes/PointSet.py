# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 14:10:40 2015

@author: dominic
"""

class PointSet:
    def __init__(self):
        self.points_dict = {}
    
    def add_point(self, name, pointlist, midline=False, opposite=None):
        self.points_dict[name] = {}
        axes = ['x','y','z']
        for idx, val in enumerate(pointlist):
            self.points_dict[name][axes[idx]] = val
        self.points_dict[name]['midline'] = midline
        self.points_dict[name]['opposite'] = opposite
        if opposite != None:
            self.points_dict[opposite]['opposite'] = name
    
    def __str__(self):
        val = ''
        for p in self.points():
            val = val +str(p)+' '
        return val
    
    def points(self):
        return sorted(self.points_dict.keys())

newpoints = PointSet()
newpoints.add_point('p1',[1,2])
newpoints.add_point('p2',[3,2], opposite = 'p1')
newpoints.add_point('p3',[2,2], midline = True)
print newpoints

