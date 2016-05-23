# -*- coding: utf-8 -*-
"""
@author: dominic
"""

import Shape, numpy as np, csv

class ShapeSet:
    """
    A class that contains a multiple PointSets.
    """
    
    def __init__(self, shapeset_name=None):
        self.name = shapeset_name
        self.shapes = {}
        self.n_shapes = 0
        self.n_dims = 0
        self.n_lm = None
        
        self.__is_aligned__ = False
        self.__last_added__ = 0
        
        self.midpoints = None
        self.point_pairs = None
    
    def append_shape(self, points):
        """Add a Shape object to the ShapeSet"""
        assert(points.__class__.__name__=="Shape")
        if self.n_dims != 0:
            assert(self.n_dims == points.n_dims)
        if points.name == None:
            self.shapes["shape"+str(self.__last_added__)] = points
        else:
            self.shapes[points.name] = points
        if self.n_lm == None:
            self.n_lm = points.n_landmarks
        self.n_shapes+=1
        self.__last_added__+=1
        self.__is_aligned__=False
    
    def details(self):
        if self.name != None:
            print self.name
        print "%i shapes of %i landmarks" %(self.n_shapes, self.n_lm)
    
    
    def export(self, filename, filetype='csv', rownames=None):
        f = open(filename, 'w')
        if filetype=='csv':
            csvwriter = csv.writer(f)
            for t in self.shapes.keys():
                if rownames==None:
                    row = [t]
                else:
                    row=[rownames[t]]
                for lm in self.shapes[t].landmarks:
                    row = row+lm
                csvwriter.writerow(row)
        f.close()
    
    def merge_shapes(self,slist,merged_name,replace=True):
        """
        Merges a set of shapes, by taking the average of their points.
        
        Args
            slist is a python list of the ShapeSet.shapes keys of the Shapes to
            merge.
            merged_name is a name of the merged Shape that will be added to the
            dataset.
            replace: if True, the original shapes will be removed from the 
            ShapeSet (default), if False, they will be left in
        
        The ShapeSet must be aligned before merging.
        
        Missing landmarks (with nan coordinates) will be ignored for 
        calculating the average of that landmark.
        """
        if self.__is_aligned__==False:
            raise Exception("ShapeSet must be aligned before shapes can be merged.")
        if len(slist)<2:
            raise Exception("Must be at least two shapes in slist to merge.")
        mean_lms = np.nanmean(np.array([self.shapes[i].landmarks for i in slist]), axis=0)
        merged_shape = Shape.Shape(data = mean_lms.tolist(),shape_name=merged_name)
        if replace==True:
            for s in slist:
                self.shapes.pop(s)
                self.n_shapes = self.n_shapes-1
        self.append_shape(merged_shape)

    def merge_shapeset(shapeset_to_subsume):
        """Merges a second shapeset into this one"""
        return
    
    
    def __kmn__(self, typeof='list'):
        kmn = [self.shapes[i].landmarks for i in sorted(self.shapes.keys())]
        if typeof=='np_array':
            return np.array(kmn)
        else:
            return kmn
    

