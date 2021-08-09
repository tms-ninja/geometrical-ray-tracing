import unittest

import numpy as np
from numpy.testing import assert_array_equal

import tracing as tr

# Contains useful checks to avoid duplicating code
class useful_checks:

    def check_float_property(self, obj, attr, expected, new_v):
        """Checks a float property for read write"""

        # Check its curret value is what we expect
        assert_array_equal(getattr(obj, attr), expected)

        # Change it to something else
        setattr(obj, attr, new_v)
        assert_array_equal(getattr(obj, attr), new_v)

        # Set it back
        setattr(obj, attr, expected)
        assert_array_equal(getattr(obj, attr), expected)

    def check_np_view_shape_2(self, obj, attr, expected, new_vw):
        """Checks a numpy view with shape (2, )
        Checks the view equals what we expect it to equal
        and changing it elementwise and by copy
        """
        vw = getattr(obj, attr)

        # Check it is what we initialy expect
        assert_array_equal(vw, expected)

        # Change elementwise
        vw[0], vw[1] = new_vw[0], new_vw[1]

        assert_array_equal(vw, new_vw)

        # Change by copy back to what it was
        setattr(obj, attr, expected)

        assert_array_equal(getattr(obj, attr), expected)



class Test_PyMirror_Plane(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyMirror_Plane"""
    _start = np.array([1.2, 3.4])
    _end = np.array([5.6, 7.8])
    
    def create_PyMiror_Plane(self):
        """Creates an instance of PyMirror_Plane"""
        return tr.PyMirror_Plane(self._start, self._end)

    def test_start_get_set(self):
        """Tests start point property start setting and getting"""
        m = self.create_PyMiror_Plane()

        self.check_np_view_shape_2(m, 'start', self._start, np.array([6.7, 8.9]))
        
    def test_end_get_set(self):
        """Tests end point property end setting and getting"""
        m = self.create_PyMiror_Plane()

        self.check_np_view_shape_2(m, 'end', self._end, np.array([6.7, 8.9]))

    def test_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_PyMiror_Plane()

        expected = np.stack([self._start, self._end])

        assert_array_equal(m.plot(), expected)


class Test_PyRefract_Plane(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyRefract_Plane"""

    _start = np.array([1.2, 3.4])
    _end = np.array([5.6, 7.8])
    _n1 = 1.5
    _n2 = 2.0
    
    def create_PyRefract_Plane(self):
        """Creates an instance of PyRefract_Plane"""
        return tr.PyRefract_Plane(self._start, self._end, self._n1, self._n2)

    def test_start_get_set(self):
        """Tests start point property start setting and getting"""
        m = self.create_PyRefract_Plane()

        self.check_np_view_shape_2(m, 'start', self._start, np.array([6.7, 8.9]))
        
    def test_end_get_set(self):
        """Tests end point property end setting and getting"""
        m = self.create_PyRefract_Plane()

        self.check_np_view_shape_2(m, 'end', self._end, np.array([6.7, 8.9]))

    def test_n1_set_get(self):
        """Tests refractive index property n1 setting and getting"""
        m = self.create_PyRefract_Plane()

        self.check_float_property(m, 'n1', self._n1, self._n1 + 10.0)

    def test_n2_set_get(self):
        """Tests refractive index property n2 setting and getting"""
        m = self.create_PyRefract_Plane()
        
        self.check_float_property(m, 'n2', self._n2, self._n2 + 10.0)

    def test_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_PyRefract_Plane()

        expected = np.stack([self._start, self._end])

        assert_array_equal(m.plot(), expected)



if __name__ == '__main__':
    unittest.main()
