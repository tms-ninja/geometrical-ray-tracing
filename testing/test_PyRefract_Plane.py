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


class Test_PyRefract_Plane(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyRefract_Plane"""

    _start = np.array([1.2, 3.4])
    _end = np.array([5.6, 7.8])
    _n1 = 1.5
    _n2 = 2.0
    
    def create_Obj(self):
        """Creates an instance of PyRefract_Plane"""
        return tr.PyRefract_Plane(self._start, self._end, self._n1, self._n2)

    # TODO: Test __cinit__()

    def test_PyRefract_Plane_cinit_none_check(self):
        """
        Test PyRefract_Plane c initiliser, check None can't be passed to
        arguments that take numpy arrays
        """
        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(None, self._end, self._n1, self._n2)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(self._start, None, self._n1, self._n2)

    def test_PyRefract_Plane_cinit_shape_check(self):
        """
        Test PyRefract_Plane c initiliser, check passed numpy arrays have 
        correct shape of (2, )
        """
        # Correct shape should pass
        c = tr.PyRefract_Plane(self._start, self._end, self._n1, self._n2)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(np.array([1.0]), self._end, self._n1, self._n2)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(np.array([1.0, 2.0, 3.0]), self._end, self._n1, self._n2)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyRefract_Plane(np.array([[1.0, 2.0], [3.0, 4.0]]), self._end, self._n1, self._n2)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(self._start, np.array([1.0]), self._n1, self._n2)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Plane(self._start, np.array([1.0, 2.0, 3.0]), self._n1, self._n2)

        with self.assertRaises(ValueError) as context:
            c = tr.PyRefract_Plane(self._start, np.array([[1.0, 2.0], [3.0, 4.0]]), self._n1, self._n2)
    
    # Testing property start
    def test_PyRefract_Plane_start_get(self):
        """Tests property start getting"""
        m = self.create_Obj()

        assert_array_equal(m.start, self._start)

    def test_PyRefract_Plane_start_set(self):
        """Tests property start setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'start', self._start, np.array([6.7, 8.9]))
        
    def test_PyRefract_Plane_start_set_none_not_allowed(self):
        """Tests property end can't be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.start = None

    # Testing property end
    def test_PyRefract_Plane_end_get(self):
        """Tests property end getting"""
        m = self.create_Obj()

        assert_array_equal(m.end, self._end)

    def test_PyRefract_Plane_end_set(self):
        """Tests property end setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'end', self._end, np.array([6.7, 8.9]))

    def test_PyRefract_Plane_end_set_none_not_allowed(self):
        """Tests property end cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.end = None

    # Test property n1 (first refractive index)
    def test_PyRefract_Plane_n1_get(self):
        """Tests property n1 getting"""
        m = self.create_Obj()

        self.assertEqual(m.n1, self._n1)

    def test_PyRefract_Plane_n1_set(self):
        """Tests property n1 getting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n1', self._n1, self._n1 + 10.0)

    def test_PyRefract_Plane_n1_Set_None_not_allowed(self):
        """Tests property n1 cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.n1 = None

    def test_PyRefract_Plane_n1_Set_Negative_not_allowed(self):
        """Tests property n1 cannot be n1 <= 0.0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.n1 = 0.0

        with self.assertRaises(ValueError) as context:
            m.n1 = -1.0

    # Test property n2 (second refractive index)
    def test_PyRefract_Plane_n2_get(self):
        """Tests property n2 getting"""
        m = self.create_Obj()

        self.assertEqual(m.n2, self._n2)
        
    def test_PyRefract_Plane_n2_set(self):
        """Tests property n2 setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n2', self._n2, self._n2 + 10.0)

    def test_PyRefract_Plane_n2_Set_None_not_allowed(self):
        """Tests property n2 cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.n2 = None

    def test_PyRefract_Plane_n2_Set_Negative_not_allowed(self):
        """Tests property n2 cannot be n2 <= 0.0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.n2 = 0.0

        with self.assertRaises(ValueError) as context:
            m.n2 = -1.0

    # Test plot() method
    def test_PyRefract_Plane_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_Obj()

        expected = np.stack([self._start, self._end])

        assert_array_equal(m.plot(), expected)

    # Testing correct ray tracing
    # TODO: add tests to verify correct ray tracing

    def test_PyRefract_Plane_tracing(self):
        """Tests a ray is traced through correctly"""
        start=np.array([1.0, 0.0])
        end=np.array([1.0, 2.0])
        n1=2.0
        n2=3.0

        c = tr.PyRefract_Plane(start=start, end=end, n1=n1, n2=n2)

        # Ray starting at origin and travelling diagonally at 45 degrees
        ang = 45 * np.pi/180.0
        r = tr.PyRay(init=np.array([0.0, 0.0]), v=unit_vec(ang))

        # Trace ray
        tr.PyTrace([c], [r], n=2, fill_up=False)

        # new angle, applying Snell's law
        new_ang = np.arcsin(np.sin(ang)*n1/n2)

        expected_ans = np.array([
            [0.0, 0.0],
            [1.0, 1.0],
            [1.0 + np.cos(new_ang), 1.0 + np.sin(new_ang)],
        ])

        assert_allclose(r.pos, expected_ans)

