from unittest import TestCase

import shapes, math

class TestShape(TestCase):

    def test_reflect_through_plane(self):
        pts = [[0,0,0],[0,0,2]]
        pln = [1,0,0,-4]
        ref = [[8,0,0],[8,0,2]]
        for idx, p in enumerate(pts):
            assert(shapes.missing.__symm_point__(p, pln) == ref[idx])
    
    def test_symmetry(self):
        pts = [[0,0,0],[float('nan'),float('nan'),float('nan')],[1,0,0],[0,1,0],[0,1,1]]
        sh = shapes.Shape(data=pts)
        est = shapes.missing.estimate_from_symmetry(sh,[[1,2]],midpoints=[0,3,4])
        assert(est.landmarks[1] == [-1,0,0])
