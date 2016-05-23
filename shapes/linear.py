# -*- coding: utf-8 -*-
"""
@author: dominic
"""

import numpy as np, math


def fit_plane(pts, ignore_missing=True):
    """Calculates the plane passing through a set of points.

    Args:
        pts : a list of lists (of 3D coords), i.e. ``shape.landmarks``
        ignore_missing : if True, missing values will be excluded before 
        the plane is fit. Otherwise, an error will be raised.

    Returns a list of 4 numbers -> [a,b,c,d]
    These correspond to a plane with the equation
        ax + by + cz + d = 0
    """
    pts_for_analysis = []
    count = 0
    for p in pts:
        pt_for_analysis = []
        is_present = True
        for c in p:
            try:
                c_num = float(c)
                if math.isnan(c_num):
                    is_present=False
                    break
                pt_for_analysis.append(c_num)
            except:
                raise Exception("Unknown datatype in points passed to fit_plane")
        if is_present == False:
            if ignore_missing!=True:
                raise Exception("Missing data in points passed to fit_plane.")
        else:
            assert(len(pt_for_analysis)==3)
            pts_for_analysis.append(pt_for_analysis)
            count+=1
    try:
        assert(len(pts_for_analysis)>2)
    except:
        raise(Exception("Not enough complete points to make a plane"))
    cps = np.array(pts_for_analysis)
    x = cps[:,0]
    A = cps[:,[1,2]]
    A = np.c_[ A, np.ones(count) ]
    a=-1
    solution = np.linalg.lstsq(A, x)
    b,c,d = solution[0]
    return [a,b,c,d]


def get_angle_between_planes(plane1,plane2,return_val='degrees'):
    """Calculates the angle between two  planes. 
    
    plane1/2 are two lists of four numbers defining each plane, [a,b,c,d],
    where ax+by+cz+d=0
    
    Returns an angle in degrees (unless return_val is set to 'radians')."""
    n1 = np.array(plane1[:3])
    n2 = np.array(plane2[:3])
    top = abs(np.dot(n1,n2))
    bottom = ( math.sqrt(np.dot(n1,n1))*math.sqrt(np.dot(n2,n2)) )
    raw = top/bottom
    rad=math.acos(raw)
    if return_val =='degrees':
        return math.degrees(rad)
    elif return_val == 'radians':
        return rad
    else:
        raise Exception("Unknown units")


def dist_between_two_points(p1,p2):
    return math.sqrt(sum([(x1-x2)**2 for x1, x2 in zip(p1,p2)]))


def average_dist_between_point_pairs(pts_pairs):
    dists = []
    for pair in pts_pairs:
        assert(len(pair)==2)
        if point_present(pair[0])==True and point_present(pair[1])==True:
            dists.append(dist_between_two_points(pair[0], pair[1]))
    if len(dists)>0:
        return sum(dists)/float(len(dists))
    else:
        return float('nan')


def point_present(pt):
    is_correct = True
    for i in pt:
        if math.isnan(i):
            is_correct=False
    return is_correct
    

def average_point(raw_pts):
    pts = []
    for p in raw_pts:
        if not math.isnan(p[0]):
            pts.append(p)
    if len(pts)==1:
        return pts[0]
    elif len(pts)==0:
        return [float('nan') for c in raw_pts[0]]
    else:
        average = [0 for c in pts[0]]
        count = 0
        for p in pts:
            if point_present(p):
                count+=1
                for idx, c in enumerate(p):
                    average[idx]+=c
        for idx, c in enumerate(average):
            average[idx] = average[idx]/float(count)
        return average


def mosimann(variables):
    gm_mean = sum([i**2 for i in variables])
    return [float(i)/gm_mean for i in variables]
    




