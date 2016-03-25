from unittest import TestCase

import shapes

class TestShape(TestCase):

    def test_initialization1(self):
        newpoints = shapes.Shape(shape_name="Tyrannosaurus")
        newpoints.add_landmark([1,2])
        newpoints.add_landmark([3,2])
        newpoints.add_landmark([2,2])
        assert(newpoints.name=='Tyrannosaurus')
        assert(newpoints.n_landmarks==3)
        assert(newpoints.n_dim==2)
