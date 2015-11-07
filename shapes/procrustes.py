# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 14:02:14 2015

@author: dominic
"""

import numpy as np, math #, matplotlib.cm as cm



def get_centroid(s1):
    c = np.array([0.0,0.0])
    pts = 0
    for p in s1:
        if not np.isnan(p).any():
            c+=p
            pts+=1
    c = c/float(pts)
    return c




def reposition(s1):
    centroid = get_centroid(s1)
    new_shape = []
    for idx, p in enumerate(s1):
        new_shape.append(s1[idx] - centroid)
    new_shape = np.array(new_shape)
    return new_shape



def get_centroid_size(s1):
    """Assumes centred shape"""
    centroid_size = 0
    centroid = get_centroid(s1)
    for idx, p in enumerate(s1):
        for idx, i in enumerate(centroid):
            centroid_size += (p[idx] - i) ** 2
    centroid_size = math.sqrt(centroid_size)
    return centroid_size

def rescaled(s1,scale=1.0):
    centroid_size = get_centroid_size(s1)
    return scale*s1/centroid_size


def rotate(s1, s2):
    both = np.dot(np.transpose(s1), s2)
    u,s,v = np.linalg.svd(both)
    sigma = np.zeros([len(s),len(s)])
    for idx, i in enumerate(s):
        if i >= 0:
            sigma[idx,idx] = 1
        else:
            sigma[idx,idx] = -1
    h = np.dot(np.dot(np.transpose(u), sigma), np.transpose(v))
    s2_rotated = np.dot(s2, h)
    return s2_rotated

def opa(s1, s2):
    """Returns s2 aligned to s1"""
    s1_rescaled = rescaled(reposition(s1))
    s2_rescaled = rescaled(reposition(s2))
    return rotate(s1_rescaled, s2_rescaled)


def gpa(shape_dict):
    names = shape_dict.keys()
    preshape_dict = {}
    for n in names:
        preshape_dict[n] = rescaled(reposition(shape_dict[n]))
    rotated_dict = {}
    rotated_dict[names[0]] = preshape_dict[names[0]]
    consensus_shape = 0
    consensus_shape += preshape_dict[names[0]]
    for n in names[1:]:
        rotated_dict[n] = rotate(preshape_dict[names[0]], preshape_dict[n])
        consensus_shape += rotated_dict[n]
    consensus_shape = consensus_shape/len(names)
    resid_SS = len(names) * (
        1-np.trace(np.dot(consensus_shape, np.transpose(consensus_shape))))
    scale_factors = {}
    for n in names:
        scale_factors[n] = 1
    
    while True:
        rerotated_dict = {}
        new_consensus = 0
        for n in names:
            rerotated_dict[n] = rotate(consensus_shape, rotated_dict[n])
            new_consensus += rerotated_dict[n]
        new_consensus = new_consensus/len(names)
        for n in names:
            top = np.trace(np.dot(rerotated_dict[n],np.transpose(new_consensus)))
            bottom1 = np.trace( np.dot( rerotated_dict[n], np.transpose(rerotated_dict[n]) ))
            bottom2 = np.trace(np.dot(new_consensus,np.transpose(new_consensus)))
            pi_over_pi = math.sqrt((top/(bottom1 * bottom2)))
            rerotated_dict[n] = pi_over_pi * rerotated_dict[n]
            scale_factors[n] = scale_factors[n]*pi_over_pi
        new_consensus = 0
        for n in names:
            new_consensus += rerotated_dict[n]
        new_consensus = new_consensus/len(names)
        new_resid_SS = len(names) * (
            1-np.trace(np.dot(new_consensus, np.transpose(new_consensus))))
        if (resid_SS - new_resid_SS) > 0.001:
            resid_SS = new_resid_SS
            rotated_dict = rerotated_dict
            consensus_shape = new_consensus
        else:
            break
    return rerotated_dict, new_consensus



#def plot_shapes_2D(shape_set):
#    colors = matplotlib.colors.cnames.keys()
#    for idx, n in enumerate(shape_set.keys()):
#        x = shape_set[n][:,0]
#        y = shape_set[n][:,1]
#        cols = [x,y]
#        for i0, col in enumerate(cols):
#            mask = [0 for i1 in xrange(len(col))]
#            for i2, point in enumerate(col):
#                if np.isnan(point):
#                    mask[i2] = 1
#            cols[i0] = np.ma.array(col, mask=mask).compressed()
#        scatter(cols[0],cols[1], c=colors[idx], label=n)
#    legend()


def align_incomplete(shape_set):
    ### Separate into complete and incomplete
    complete = {}
    incomplete = {}
    for shape in shape_set.keys():
        missing = False
        for point in shape_set[shape]:
            if np.isnan(point).any():
                missing = True
                break
        if missing == True:
            incomplete[shape] = shape_set[shape]
        else:
            complete[shape] = shape_set[shape]    
    ### Align the complete shapes
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
        scale_factor = get_centroid_size(sub_consensus)
        aligned_incomplete = rotate(reposition(sub_consensus), rescaled(reposition(sub_incomplete), scale=scale_factor))
        
        ### Calculate translation
        sub_consensus_trans = reposition(sub_consensus)
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
    return aligned


def test():
    #shape1 = [[1,1],[3,1],[2,2]]
    #shape2 = [[7,1],[3,2],[2,3]]
    shape1 = [[0,0],[50,11],[10,-10],[11,21]]
    shape2 = [[0,0],[51,9],[9,-10],[11,22]]
    shape3 = [[0,0],[49,10],[11,-10],[10,20]]
    shape4 = [[0,0],[50,8],[8,-12],[10,20]]
#    shape1 = [[0,0],[0,10],[10,10],[10,0]]
#    shape2 = [[10,0],[0,0],[0,10],[10,10]]
#    shape3 = [[10,10],[10,0],[0,0],[0,10]]
#    shape4 = [[0,10],[10,10],[10,0],[0,0]]
    shape1 = np.array(shape1)
    shape2 = np.array(shape2)
    shape3 = np.array(shape3)
    shape4 = np.array(shape4)
#    opa(shape1, shape2)
##    print "Original shape1:\n", shape1
#    shape1_centred = reposition(shape1)
##    print "centred shape1:\n", shape1_centred
#    shape1_rescaled = rescaled(shape1_centred)
#    
##    print "\n\nShape2"
#    shape2_rescaled = rescaled(reposition(shape2))
#    
##    print shape1_rescaled,"\n", shape2_rescaled
#    
#    shape2_rotated = rotate(shape1_rescaled, shape2_rescaled)
##    print shape2_rotated
#    figure(0)
#    scatter(shape2_rotated[:,0], shape2_rotated[:,1])
#    scatter(shape1_rescaled[:,0],shape1_rescaled[:,1], c="r")
    
    
#    print "\n\nGPA"
#    shape_list = {'s1':shape1,
#                  's2':shape2,
#                  's3':shape3,
#                  's4':shape4
#                  }
#    all_shapes, consensus = gpa(shape_list)
#    figure(0)
#    plot_shapes_2D(all_shapes)
#    print shape1
    shape5 = [[np.nan,np.nan], [48,8],[10,-10],[10,20]]
    shape6 = [[0,0],[np.nan,np.nan],[9,-9],[11,19]]
    shape5 = np.array(shape5)
    shape6 = np.array(shape6)
#    print shape6
    incomp_shapes = {'s1':shape1,'s2':shape2,'s3':shape3,'s4':shape4,'s5':shape5,'s6':shape6}
#    print incomp_shapes
    all_aligned = align_incomplete(incomp_shapes)
    print all_aligned
    figure(1)
#    plot_shapes_2D(all_aligned)
#    for s in all_aligned.keys():
#        print get_centroid(all_aligned[s])


#test()

