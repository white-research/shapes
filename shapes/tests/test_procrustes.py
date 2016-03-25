from unittest import TestCase

import numpy as np
import shapes.procrustes as procrustes

class TestProcrustes(TestCase):

    def test_centroid(self):
        shape = np.array(range(9)).reshape((3,3)).astype('float')
        c = procrustes.__centroid__(shape)
        assert(np.array_equal(c,np.array([ 3.,  4.,  5.])))
        print "tested procrustes.__centroid__"
    
    def test_reposition(self):
        shape = np.array(range(9)).reshape((3,3)).astype('float')
        centroid = procrustes.__reposition__(shape)
    
    def test_get_centroid_size(self):
        shape = np.array(range(9)).reshape((3,3)).astype('float')
        centroid_size = procrustes.__centroid_size__(shape)
        
    def test_rescale(self):
        shape = np.array(range(9)).reshape((3,3)).astype('float')
        rescaled = procrustes.__rescale__(shape)
        assert(procrustes.__centroid_size__(rescaled)>0.999)
        assert(procrustes.__centroid_size__(rescaled)<1.001)
