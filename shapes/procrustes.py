# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:02:14 2015

@author: dominic
"""

import numpy as np, math, ShapeSet, Shape


def __centroid__(shape_array):
    """Takes a shape as a numpy array."""
#    print type(shape_array)
#    print shape_array
    return np.nanmean(shape_array, axis=0)


def __reposition__(shape_array):
    """Takes a shape as a numpy array."""
    centroid = __centroid__(shape_array)
    return shape_array - centroid


def __centroid_size__(shape_array): # rewrite to use just numpy
    """Takes a shape as a shape array. Assumes centred shape."""
    centroid_size = 0
    centroid = __centroid__(shape_array)
    for idx, p in enumerate(shape_array):
        for idx, i in enumerate(centroid):
            centroid_size += (p[idx] - i) ** 2
    centroid_size = math.sqrt(centroid_size)
    return centroid_size


def __rescale__(shape_array,scale=1.0):
    """Takes a shape as a shape array. Assumes centred shape."""
    centroid_size = __centroid_size__(shape_array)
    return scale*shape_array/centroid_size


def __rotate__(s1, s2):
    both = np.dot(np.transpose(s1), s2)
    u,s,v = np.linalg.svd(both)
    sigma = np.zeros([len(s),len(s)])
    for idx, i in enumerate(s):
        if i >= 0:
            sigma[idx,idx] = 1
        else:
            sigma[idx,idx] = -1
    h = np.dot(np.dot(np.transpose(v),sigma),np.transpose(u))
    s2_rotated = np.dot(s2, h)
    return s2_rotated


def opa(s1, s2):
    """Returns s2 aligned to s1"""
    s1_rescaled = __rescale__(__reposition__(s1))
    s2_rescaled = __rescale__(__reposition__(s2))
    return __rotate__(s1_rescaled, s2_rescaled)


def gpa(shapeset):
    shape_dict = shapeset
    names = shape_dict.keys()
    #Step 1: Center and scale all shapes
    preshape_dict = {}
    for n in names:
        print n
        preshape_dict[n] = __rescale__(__reposition__(np.array(shape_dict[n])))
    #Step 2: Set first shape as initial estimate of consensus
    rotated_dict = {}
    rotated_dict[names[0]] = preshape_dict[names[0]]
    consensus_shape = 0
    consensus_shape += preshape_dict[names[0]]
    for n in names[1:]:
        rotated_dict[n] = __rotate__(preshape_dict[names[0]], preshape_dict[n])
        consensus_shape += rotated_dict[n]
    #Step 3: Calculate initial consensus
    consensus_shape = __rescale__(consensus_shape)/len(names) #rescale?
    #Step 4: Compute initial residue sum of squares
    resid_SS = len(names) * (
        1-np.trace(np.dot(consensus_shape, np.transpose(consensus_shape))))
    #Step 5: Set initial scale factors to 1 for all shapes
    scale_factors = {}
    for n in names:
        scale_factors[n] = 1
    
    #Step 6: Rotate each shape to fit consensus using least squares
    while True:
        rerotated_dict = {}
        new_consensus = 0
        for n in names:
            rerotated_dict[n] = __rotate__(consensus_shape, rotated_dict[n]) #*scale_factors[n]
            new_consensus += rerotated_dict[n]
        new_consensus = __rescale__(new_consensus) #rescale?
#        print new_consensus[0]
#        print new_consensus[0], '\n', rescaled(new_consensus)[0]
#        for n in names:
#            print ' ', n
#            fig = plt.figure()
#            ax = fig.add_subplot(111, projection='3d')
#            ax.scatter(rerotated_dict[n][:,0],rerotated_dict[n][:,1],rerotated_dict[n][:,2], label='1')
#            ax.set_xlabel('X Label')
#            ax.set_ylabel('Y Label')
#            ax.set_zlabel('Z Label')
#            title(rerotated_dict[n])
#            fig.show()
#            top = np.trace(np.dot(rerotated_dict[n],np.transpose(new_consensus)))
#            print top
#            print np.dot(rerotated_dict[n],np.transpose(new_consensus))
#            bottom1 = np.trace( np.dot( rerotated_dict[n], np.transpose(rerotated_dict[n]) ))
#            bottom2 = np.trace(np.dot(new_consensus,np.transpose(new_consensus)))
#            
#            print '  ', top, bottom1, bottom2
#            pi_over_pi = math.sqrt((top/(bottom1 * bottom2)))
#            rerotated_dict[n] = pi_over_pi * rerotated_dict[n]
#            scale_factors[n] = scale_factors[n]*pi_over_pi
        new_consensus = 0
        for n in names:
            new_consensus += rerotated_dict[n]
        new_consensus = __rescale__(new_consensus)#/len(names)
        new_resid_SS = len(names) * (
            1-np.trace(np.dot(new_consensus, np.transpose(new_consensus))))
        print '  SS', resid_SS, new_resid_SS, (resid_SS - new_resid_SS)
        if (resid_SS - new_resid_SS) > 0.0000001:
            resid_SS = new_resid_SS
            rotated_dict = rerotated_dict
            consensus_shape = new_consensus
        else:
            break
    return rerotated_dict, new_consensus

def procrustes_align(shapes):
    shape_set = shapes.shapes
    ### Separate into complete and incomplete
    complete = {}
    incomplete = {}
    for shape in shape_set.keys():
        missing = False
        for point in shape_set[shape].landmarks:
            try:
                if np.isnan(point).any():
                    missing = True
                    break
            except TypeError:
                raise Exception("Unknown datatype in landmarks. Cannot align.")
        if missing == True:
            incomplete[shape] = shape_set[shape].landmarks
        else:
            complete[shape] = shape_set[shape].landmarks
    
    ### Align the complete shapes
#    print complete.keys()
    aligned, consensus = gpa(complete)
    
    ### Align each incomplete shape to the complete shape consensus shape
    for shape in incomplete.keys():
        ### Make subset of shape and consensus with points that are present
        points_existing = [1 for i in xrange(len(incomplete[shape]))]
        for i, point in enumerate(incomplete[shape]):
            if np.isnan(point).any():
                points_existing[i] = 0
        sub_consensus = []
        sub_incomplete = []
        for i, presence in enumerate(points_existing):
            if presence == 1:
                sub_consensus.append(list(consensus[i]))
                new_p = []
                for val in incomplete[shape][i]:
                    new_p.append(float(val))
                sub_incomplete.append(new_p)
        sub_consensus = np.array(sub_consensus)
        sub_incomplete = np.array(sub_incomplete)
        scale_factor = __centroid_size__(sub_consensus)
        aligned_incomplete = __rotate__(__reposition__(sub_consensus), __rescale__(__reposition__(sub_incomplete), scale=scale_factor))
        
        ### Calculate translation
        sub_consensus_trans = __reposition__(sub_consensus)
        translation = sub_consensus[0] - sub_consensus_trans[0]
        
        ### Reconstruct full shape including missing (and with translation)
        full_aligned_incomplete = []
        counter = 0
        for i, presence in enumerate(points_existing):
            if presence == 1:
                p = aligned_incomplete[counter] + translation
                p = [np.float(i) for i in p]
                full_aligned_incomplete.append(p)
                counter += 1
            else:
                missing_p = [np.nan for i in xrange(len(aligned_incomplete[0]))]
                full_aligned_incomplete.append(missing_p)
        full_aligned_incomplete = np.array(full_aligned_incomplete)
        ### Add to full point set
        aligned[shape] = full_aligned_incomplete

    aligned_shapeset = ShapeSet.ShapeSet(shapeset_name=str(shapes.name)+"_aligned")
    for t in aligned.keys():
        aligned_shapeset.append_shape(Shape.Shape(data=aligned[t].tolist(),
                                            shape_name=shapes.shapes[t].name,
                                            lm_names=shapes.shapes[t].name))
    aligned_shapeset.__is_aligned__ = True
    return aligned_shapeset

