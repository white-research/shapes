# -*- coding: utf-8 -*-
"""
@author: dominic
"""

import linear, math, numpy as np
import Shape, ShapeSet

def estimate_from_symmetry(shape,lm_pairs,**kwargs):
    """
    Estimates missing landmarks by reflecting through a plane of symmetry.
    
    Args:
        shape is a Shape object.
        lm_pairs is a list of lists/tuples of pairs of integers that specify
        which points are pairs.
        
        In addition either plane or midpoints needs to be specified.
        plane : a list of four numbers specifying a plane
        midpoints : a list of the integer indices of the landmarks that lie on
        the plane of symmetry.
    """
    assert('plane' in kwargs.keys() or 'midpoints' in kwargs.keys())
    if 'plane' in kwargs.keys():
        plane = kwargs['plane']
    else:
        mid_lms = []
        for idx, lm in enumerate(shape.landmarks):
            if idx in kwargs['midpoints']:
                mid_lms.append(lm)
        plane = linear.fit_plane(mid_lms)
    new_lms = shape.landmarks
    for idx, p in enumerate(shape.landmarks):
        if __point_present__(p) == False:
             opp = __opposite_lm__(idx, lm_pairs)
             if opp != -1 and __point_present__(shape.landmarks[opp])==True:
                 new_lms[idx] = __symm_point__(shape.landmarks[opp], plane)
    filled_shape = Shape.Shape(data=new_lms, shape_name=shape.name,lm_names=shape.lm_names)
    return filled_shape


def estimate_from_mean(shapeset, shapes=None):
    """
    Estimates missing landmarks in a ShapeSet from present values in other 
    specimens.
    
    Args:
        shapeset: the ShapeSet to be filled.
        shapes: an optional list of Shapes to have missing data imputed for. 
        If left as the default (None), then any taxa with missing data will be 
        estimated.
    
    Note: the shapeset must be aligned before using this function.
    """
    assert(shapeset.__is_aligned__==True)
    mean_vals = np.nanmean(shapeset.__kmn__(typeof='np_array'),axis=0).tolist()
    new_shapeset = ShapeSet.ShapeSet(shapeset_name=shapeset.name)
    if shapes==None:
        shapes=shapeset.shapes.keys()
    for t in shapeset.shapes.keys():
        new_data=np.array(shapeset.shapes[t].landmarks)
        for idx, lm in enumerate(shapeset.shapes[t].landmarks):
            if __point_present__(lm)==False:
                new_data[idx]=mean_vals[idx]
        new_shape = Shape.Shape(data=new_data.tolist(),shape_name=t)
        new_shapeset.append_shape(new_shape)
    return new_shapeset
                
    
        
        

def __point_present__(pt):
    is_correct = True
    for i in pt:
        if math.isnan(i):
            is_correct=False
    return is_correct
    


def __opposite_lm__(lmid,pairslist):
    for p in pairslist:
        if lmid == p[0]:
            return p[1]
        if lmid == p[1]:
            return p[0]
    return -1


def __symm_point__(orig_pt, plane):
    """
    Takes a point and a plane and returns a second point on the
    other side of the plane to the first point.
    """
    dist = -(plane[0]*orig_pt[0]+plane[1]*orig_pt[1]+plane[2]*orig_pt[2]+plane[3])/(plane[0]**2 + plane[1]**2 + plane[2]**2)
    mid_pt = [i+dist*a for i,a in zip(orig_pt, plane[:-1])]
    ref_pt = [i+2*(x-i) for x,i in zip(mid_pt,orig_pt)]
    return ref_pt

