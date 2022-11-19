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

# Tests for PyRay and PyTrace
class Test_PyRay(unittest.TestCase, useful_checks):

    # God values for initialisation
    _init = np.array([1.0, 2.0])
    _v = np.array([0.3, 0.4])*2

    def create_obj(self):
        return tr.PyRay(self._init, self._v)
    
    # Test __cinit__()

    def test_PyRay_cinit_none_check(self):
        """Test PyRay c initiliser, check None is not allowed"""

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(None, self._v)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(self._init, None)

    def test_PyRay_cinit_shape_check(self):
        """
        Test PyRay c initiliser, check passed numpy arrays must have correct
        shape of (2, )
        """

        # Correct shape should pass
        c = tr.PyRay(self._init, self._v)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(np.array([1.0]), self._v)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(np.array([1.0, 2.0, 3.0]), self._v)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyRay(np.array([[1.0, 2.0], [3.0, 4.0]]), self._v)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(self._init, np.array([1.0]))

        with self.assertRaises(TypeError) as context:
            c = tr.PyRay(self._init, np.array([1.0, 2.0, 3.0]))

        with self.assertRaises(ValueError) as context:
            c = tr.PyRay(self._init, np.array([[1.0, 2.0], [3.0, 4.0]]))

    # Testing property v
    def test_PyRay_v_get(self):
        """Tests PyRay.v get"""
        r = self.create_obj()

        assert_array_equal(r.v, self._v)

    def test_PyRay_v_set(self):
        """Tests PyRay.v set"""
        r = self.create_obj()

        self.check_writable_np_view_shape_2_set(r, 'v', self._v, np.array([6.7, 8.9]))

    # Testing property pos
    def test_PyRay_v_get(self):
        """Tests PyRay.pos get"""
        r = self.create_obj()
        
        # Note pos is an array with shape (N, 2)
        assert_array_equal(r.pos, self._init[np.newaxis, ...])

    # Testing method plot()
    def test_PyRay_Plot(self):
        """Test plot() method by computing ray bouncing of PyMirror_Plane"""
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

        assert_allclose(r.plot(), expected_ans)

    # Testing method reset()
    def test_PyRay_reset_v(self):
        """Test pyRay.reset(new_v) method"""
        pos, v = np.zeros(2), np.array([1.0, 0.0])

        r = tr.PyRay(pos, v)

        # Trace the ray so its pos has more than one element
        tr.PyTrace([], [r], n=3, fill_up=True)

        new_v = np.array([0.0, -1.0])
        r.reset(new_v)

        assert_array_equal(r.pos.shape, (1, 2))
        assert_array_equal(r.pos[0], pos)
        assert_array_equal(r.v, new_v)

    def test_PyRay_reset_v_pos(self):
        """Test PyRay.reset(new_v, new_pos) method"""
        pos, v = np.zeros(2), np.array([1.0, 0.0])

        r = tr.PyRay(pos, v)

        # Trace the ray so its pos has more than one element
        tr.PyTrace([], [r], n=3, fill_up=True)

        new_pos = np.array([2.0, 3.0])
        new_v = np.array([0.0, -1.0])
        r.reset(new_v, new_pos)

        assert_array_equal(r.pos.shape, (1, 2))
        assert_array_equal(r.pos[0], new_pos)
        assert_array_equal(r.v, new_v)

