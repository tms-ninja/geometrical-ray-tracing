import tracing as tr
import numpy as np
from numpy.testing import assert_array_equal

import unittest

class Test_PyMirror_Plane(unittest.TestCase):
    
    def test_start_get(self):
        start = np.array([1.2, 3.4])
        end = np.array([5.6, 7.8])
        
        m = tr.PyMirror_Plane(start, end)

        assert_array_equal(m.start, start)

    def test_start_set(self):
        start = np.array([1.2, 3.4])
        end = np.array([5.6, 7.8])
        
        m = tr.PyMirror_Plane(start, end)

        new_start = np.array([12.0, 4.5])
        m.start = new_start

        assert_array_equal(m.start, new_start)

        m.start[0] = 123.0
        m.start[1] = 456.0

        self.assertEqual(m.start[0], 123.0)
        self.assertEqual(m.start[1], 456.0)

    def test_end_get(self):
        start = np.array([1.2, 3.4])
        end = np.array([5.6, 7.8])
        
        m = tr.PyMirror_Plane(start, end)

        assert_array_equal(m.end, end)

    def test_end_set(self):
        start = np.array([1.2, 3.4])
        end = np.array([5.6, 7.8])
        
        m = tr.PyMirror_Plane(start, end)

        new_end = np.array([12.0, 4.5])
        m.end = new_end

        assert_array_equal(m.end, new_end)

        m.end[0] = 123.0
        m.end[1] = 456.0

        self.assertEqual(m.end[0], 123.0)
        self.assertEqual(m.end[1], 456.0)



if __name__ == '__main__':
    unittest.main()
