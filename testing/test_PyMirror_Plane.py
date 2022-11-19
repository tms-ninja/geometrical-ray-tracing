# geometrical-ray-tracing: Program to perform geometrical ray tracing
# Copyright (C) 2022  Tom Spencer (tspencerprog@gmail.com)

# This file is part of geometrical-ray-tracing

# geometrical-ray-tracing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import tracing as tr
from generic_test_functions import *
from numpy.testing import assert_allclose


class Test_PyMirror_Plane(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyMirror_Plane"""
    _start = np.array([1.2, 3.4])
    _end = np.array([5.6, 7.8])
    
    def create_Obj(self):
        """Creates an instance of PyMirror_Plane"""
        return tr.PyMirror_Plane(self._start, self._end)

    # TODO: Test __cinit__()

    def test_PyMirror_Plane_cinit_none_check(self):
        """Test PyMirror_Plane c initiliser, check None is not allowed"""
        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(None, self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(self._start, None)

    def test_PyMirror_Plane_cinit_shape_check(self):
        """
        Test PyMirror_Plane c initiliser, check passed numpy arrays have 
        correct shape of (2, )
        """
        # Correct shape should pass
        c = tr.PyMirror_Plane(self._start, self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(np.array([1.0]), self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(np.array([1.0, 2.0, 3.0]), self._end)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyMirror_Plane(np.array([[1.0, 2.0], [3.0, 4.0]]), self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(self._start, np.array([1.0]))

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Plane(self._start, np.array([1.0, 2.0, 3.0]))

        with self.assertRaises(ValueError) as context:
            c = tr.PyMirror_Plane(self._start, np.array([[1.0, 2.0], [3.0, 4.0]]))

        
    # Testing property start
    def test_PyMirror_Plane_start_get(self):
        """Tests property start getting"""
        m = self.create_Obj()

        assert_array_equal(m.start, self._start)

    def test_PyMirror_Plane_start_set(self):
        """Tests property start setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'start', self._start, np.array([6.7, 8.9]))
        
    def test_PyMirror_Plane_start_set_none_not_allowed(self):
        """Tests property start can't be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.start = None

    # Testing property end
    def test_PyMirror_Plane_end_get(self):
        """Tests property end getting"""
        m = self.create_Obj()

        assert_array_equal(m.end, self._end)

    def test_PyMirror_Plane_end_set(self):
        """Tests property end setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'end', self._end, np.array([6.7, 8.9]))

    def test_PyMirror_Plane_end_set_none_not_allowed(self):
        """Tests property end cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.end = None

    # Test plot() method
    def test_PyMirror_Plane_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_Obj()

        expected = np.stack([self._start, self._end])

        assert_array_equal(m.plot(), expected)

    # Testing correct ray tracing
    # TODO: add tests to verify correct ray tracing

    def test_PyMirror_Plane_tracing(sef):
        # Vertical mirror at x = 1.0
        m = tr.PyMirror_Plane(start=np.array([1.0, 0.0]), end=np.array([1.0, 2.0]))

        # Ray starting at origin and travelling diagonally at 45 degrees
        ang = 45 * np.pi/180.0
        r = tr.PyRay(init=np.array([0.0, 0.0]), v=unit_vec(ang))

        # Trace ray
        tr.PyTrace([m], [r], n=2, fill_up=False)

        expected_ans = np.array([
            [0.0, 0.0],
            [1.0, 1.0],
            [1.0 + np.cos(ang + np.pi/2), 1.0 + np.sin(ang + np.pi/2)],
        ])

        assert_allclose(r.pos, expected_ans)

