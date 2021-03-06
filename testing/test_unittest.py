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


import unittest

import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

import tracing as tr

def unit_vec(angle):
    """
    Returns a normalised unit vector in the direction pg angle. Angle is
    measured from the x axis counter-clockwise
    """

    return np.array([np.cos(angle), np.sin(angle)])

# Contains useful checks to avoid duplicating code
class useful_checks:

    def check_float_property(self, obj, attr, expected, new_v):
        """Checks a float property for read write"""

        # Check its curret value is what we expect
        unittest.TestCase.assertEqual(self, getattr(obj, attr), expected)

        # Change it to something else
        setattr(obj, attr, new_v)
        unittest.TestCase.assertEqual(self, getattr(obj, attr), new_v)

        # Set it back
        setattr(obj, attr, expected)
        unittest.TestCase.assertEqual(self, getattr(obj, attr), expected)

    def check_writable_np_view_shape_2_set(self, obj, attr, expected, new_vw):
        """
        Checks a writeable numpy view with shape (2, )
        Checks the view equals what we expect it to equal and changing it 
        elementwise and by copy
        Note this should only be used for a numpy view with the writable
        flag set to True. Otherwise the non-writable version of this function
        should be used
        """

        vw = getattr(obj, attr)

        # Check it is what we initialy expect
        assert_array_equal(getattr(obj, attr), expected)

        # make sure vw and expected aren't the same array if it is, changing
        # it elementwise will mean setting by copy check will always return
        # OK
        exp_cp = expected.copy()

        # Change elementwise
        vw[0], vw[1] = new_vw[0], new_vw[1]

        assert_array_equal(getattr(obj, attr), new_vw)

        # Change by copy back to what it was
        setattr(obj, attr, exp_cp)

        assert_array_equal(getattr(obj, attr), exp_cp)

    def check_non_writable_np_view_shape_2_set(self, obj, attr, expected, new_vw):
        """
        Checks a non-writeable numpy view with shape (2, )
        Checks the view equals what we expect it to equal and changing it 
        by copy & that it rejects being set element wise
        Note this should only be used for a numpy view with the writable
        flag set to False. Otherwise the writable version of this function
        should be used
        """

        vw = getattr(obj, attr)

        # Check it is what we initialy expect
        assert_array_equal(getattr(obj, attr), expected)

        # Check it rejects elementwise assignment
        with self.assertRaises(ValueError) as _:
            vw[0], vw[1] = new_vw[0], new_vw[1]

        # Change by copy to new_vw
        setattr(obj, attr, new_vw)

        assert_array_equal(getattr(obj, attr), new_vw)

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



class Test_PyTrace(unittest.TestCase, useful_checks):
    """Tests for the tracing function PyTrace"""

    def test_PyTrace_Fill_Up_True(self):
        """
        Tests fill_up=True parameter by tracing two rays through two 
        components. One ray goes through both, the other goes throguh neither.
        """
        n1, n2 = 3.0, 2.0

        c1 = tr.PyMirror_Plane(np.array([-1.0, 1.0]), np.array([1.0, 1.0]))
        c2 = tr.PyRefract_Plane(np.array([1.0, 1.0]), np.array([1.0, -1.0]),
                                n1=n1, n2=n2)

        r1 = tr.PyRay(np.array([-0.25, 0.0]), unit_vec(180*np.pi/180))
        r2 = tr.PyRay(np.array([-1.0, 0.0]), unit_vec(45*np.pi/180))

        rays = [r1, r2]

        tr.PyTrace([c1, c2], rays, n=6, fill_up=True)

        # Angle of the refracted ray r2
        refract_ray_ang = -np.arcsin( np.sin(45*np.pi/180) *n2/n1 )

        expected_ans = [
            [  # r1 path
                [-0.25, 0.0],
                [-1.25, 0.0],
            ],
            [
                [-1.0, 0.0],
                [0.0, 1.0],
                [1.0, 0.0],
                [1.0 + np.cos(refract_ray_ang), 0.0 + np.sin(refract_ray_ang)]
            ]
        ]

        # Do the filling up
        expected_ans[0].extend([expected_ans[0][-1]] * 5)
        expected_ans[1].extend([expected_ans[1][-1]] * 3)

        expected_ans = np.array(expected_ans)
        
        # Increase atol as some entries in expected_ans are zero
        for r, exp in zip(rays, expected_ans):
            assert_allclose(r.pos, exp, atol=1e-15)

    def test_PyTrace_Fill_Up_False(self):
        """
        Tests fill_up=False parameter by tracing two rays through two 
        components. One ray goes through both, the other goes throguh neither.
        """
        n1, n2 = 3.0, 2.0

        c1 = tr.PyMirror_Plane(np.array([-1.0, 1.0]), np.array([1.0, 1.0]))
        c2 = tr.PyRefract_Plane(np.array([1.0, 1.0]), np.array([1.0, -1.0]),
                                n1=n1, n2=n2)

        r1 = tr.PyRay(np.array([-0.25, 0.0]), unit_vec(180*np.pi/180))
        r2 = tr.PyRay(np.array([-1.0, 0.0]), unit_vec(45*np.pi/180))

        rays = [r1, r2]

        tr.PyTrace([c1, c2], rays, n=6, fill_up=False)

        # Angle of the refracted ray r2
        refract_ray_ang = -np.arcsin( np.sin(45*np.pi/180) *n2/n1 )

        expected_ans = [
            [  # r1 path
                [-0.25, 0.0],
                [-1.25, 0.0],
            ],
            [
                [-1.0, 0.0],
                [0.0, 1.0],
                [1.0, 0.0],
                [1.0 + np.cos(refract_ray_ang), 0.0 + np.sin(refract_ray_ang)]
            ]
        ]

        expected_ans = [np.array(p) for p in expected_ans]
        
        # Increase atol as some entries in expected_ans are zero
        for r, exp in zip(rays, expected_ans):
            assert_allclose(r.pos, exp, atol=1e-15)

    # TODO: check fill_up=False, needs C++ updating not handled properly

    def test_PyTrace_Invalid_Components(self):
        """
        Tests PyTrace raises TypeError if an invalid component is
        passed in the components list
        """
        # "Good" components
        c1 = tr.PyMirror_Plane(np.array([1.0, 0.0]), np.array([1.0, 2.0]))
        c2 = tr.PyRefract_Plane(np.array([-1.0, 0.0]), np.array([-1.0, 4.0]))

        rays = [tr.PyRay(np.array([0.0, 0.0]), np.array([1.0, 0.0]))]

        with self.assertRaises(TypeError):
            comps = [c1, 5, c2]

            tr.PyTrace(comps, rays, n=2, fill_up=True)

        with self.assertRaises(TypeError):
            class FakeComponent:
                pass

            comps = [c1, FakeComponent(), c2]

            tr.PyTrace(comps, rays, n=2, fill_up=True)


# Base components
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


class Test_PyScreen_Plane(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyScreen_Plane"""
    _start = np.array([1.2, 3.4])
    _end = np.array([5.6, 7.8])
    
    def create_Obj(self):
        """Creates an instance of PyScreen_Plane"""
        return tr.PyScreen_Plane(self._start, self._end)

    # TODO: Test __cinit__()

    def test_PyScreen_Plane_cinit_none_check(self):
        """Test PyScreen_Plane c initiliser, check None is not allowed"""
        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(None, self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(self._start, None)

    def test_PyScreen_Plane_cinit_shape_check(self):
        """
        Test PyScreen_Plane c initiliser, check passed numpy arrays have 
        correct shape of (2, )
        """
        # Correct shape should pass
        c = tr.PyScreen_Plane(self._start, self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(np.array([1.0]), self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(np.array([1.0, 2.0, 3.0]), self._end)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyScreen_Plane(np.array([[1.0, 2.0], [3.0, 4.0]]), self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(self._start, np.array([1.0]))

        with self.assertRaises(TypeError) as context:
            c = tr.PyScreen_Plane(self._start, np.array([1.0, 2.0, 3.0]))

        with self.assertRaises(ValueError) as context:
            c = tr.PyScreen_Plane(self._start, np.array([[1.0, 2.0], [3.0, 4.0]]))

        
    # Testing property start
    def test_PyScreen_Plane_start_get(self):
        """Tests property start getting"""
        m = self.create_Obj()

        assert_array_equal(m.start, self._start)

    def test_PyScreen_Plane_start_set(self):
        """Tests property start setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'start', self._start, np.array([6.7, 8.9]))
        
    def test_PyScreen_Plane_start_set_none_not_allowed(self):
        """Tests property start can't be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.start = None

    # Testing property end
    def test_PyScreen_Plane_end_get(self):
        """Tests property end getting"""
        m = self.create_Obj()

        assert_array_equal(m.end, self._end)

    def test_PyScreen_Plane_end_set(self):
        """Tests property end setting"""
        m = self.create_Obj()

        self.check_non_writable_np_view_shape_2_set(m, 'end', self._end, np.array([6.7, 8.9]))

    def test_PyScreen_Plane_end_set_none_not_allowed(self):
        """Tests property end cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.end = None

    # Test plot() method
    def test_PyScreen_Plane_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_Obj()

        expected = np.stack([self._start, self._end])

        assert_array_equal(m.plot(), expected)

    # Testing correct ray tracing
    # TODO: add tests to verify correct ray tracing

    def test_PyScreen_Plane_tracing(sef):
        # Vertical screen at x = 1.0
        m = tr.PyScreen_Plane(start=np.array([1.0, 0.0]), end=np.array([1.0, 2.0]))

        # Ray starting at origin and travelling diagonally at 45 degrees
        ang = 45 * np.pi/180.0
        r = tr.PyRay(init=np.array([0.0, 0.0]), v=unit_vec(ang))

        # Trace ray
        tr.PyTrace([m], [r], n=2, fill_up=False)

        expected_ans = np.array([
            [0.0, 0.0],
            [1.0, 1.0],
        ])

        assert_allclose(r.pos, expected_ans)


class Test_PyMirror_Sph(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyMirror_Plane"""
    _centre = np.array([5.6, 7.8])
    _R = 4.5
    _start = 1.2
    _end = 3.4
    
    def create_Obj(self):
        """Creates an instance of PyMirror_Sph"""
        return tr.PyMirror_Sph(self._centre, self._R, self._start, self._end)

    # TODO: Test __cinit__()
    def test_PyMirror_Sph_cinit_none_check(self):
        """
        Test PyMirror_Sph c initiliser, check None can't be passed to
        arguments that take numpy arrays
        """
        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Sph(None, self._R, self._start, self._end)

    def test_PyMirror_Sph_cinit_shape_check(self):
        """
        Test PyMirror_Sph c initiliser, check passed numpy arrays have 
        correct shape of (2, )
        """
        # Correct shape should pass
        c = tr.PyMirror_Sph(self._centre, self._R, self._start, self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Sph(np.array([1.0]), self._R, self._start, 
                                self._end)

        with self.assertRaises(TypeError) as context:
            c = tr.PyMirror_Sph(np.array([1.0, 2.0, 3.0]), self._R, 
                                self._start, self._end)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyMirror_Sph(np.array([[1.0, 2.0], [3.0, 4.0]]), self._R, 
                                self._start, self._end)

    def test_PyMirror_Sph_cinit_neg_R(self):
        """
        Test PyMirror_Sph c initiliser, check R cannot be less than or equal to
        zero.
        """

        with self.assertRaises(ValueError) as context:
            c = tr.PyMirror_Sph(self._centre, -1.0, self._start, self._end)

        with self.assertRaises(ValueError) as context:
            c = tr.PyMirror_Sph(self._centre, 0.0, self._start, self._end)

    # Testing property centre
    def test_PyMirror_Sph_centre_get(self):
        """Tests property centre getting"""
        m = self.create_Obj()

        assert_array_equal(m.centre, self._centre)

    def test_PyMirror_Sph_centre_set(self):
        """Tests property centre setting"""
        m = self.create_Obj()

        self.check_writable_np_view_shape_2_set(m, 'centre', self._centre, self._centre + 10.0)

    def test_PyMirror_Sph_centre_set_none_not_allowed(self):
        """Tests property centre cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.centre = None

    # Testing property R
    def test_PyMirror_Sph_R_get(self):
        """Tests property R getting"""
        m = self.create_Obj()

        self.assertEqual(m.R, self._R)

    def test_PyMirror_Sph_R_set(self):
        """Tests property R getting"""
        m = self.create_Obj()

        self.check_float_property(m, 'R', self._R, self._R + 10.0)

    def test_PyMirror_Sph_R_Set_None_not_allowed(self):
        """Tests property R cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.R = None

    def test_PyMirror_Sph_R_Set_Negative_not_allowed(self):
        """Tests property R cannot be set R <= 0.0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.R = 0.0

        with self.assertRaises(ValueError) as context:
            m.R = -1.0

    # Testing property start
    def test_PyMirror_Sph_start_get(self):
        """Tests property start getting"""
        m = self.create_Obj()

        self.assertEqual(m.start, self._start)

    def test_PyMirror_Sph_start_set(self):
        """Tests property start setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'start', self._start, self._end - 123.0)
        
    def test_PyMirror_Sph_start_set_none_not_allowed(self):
        """Tests property start can't be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.start = None

    def test_PyMirror_Sph_start_must_be_less_than_end(self):
        """Tests when setting property start that it must be greater than property end"""
        m = self.create_Obj()

        # OK to set it something less than end
        m.start = m.end - 1.0

        # Raises exception if it's more
        with self.assertRaises(ValueError) as context:
            m.start = m.end = 1.0

    # Testing property end
    def test_PyMirror_Sph_end_get(self):
        """Tests property end getting"""
        m = self.create_Obj()

        self.assertEqual(m.end, self._end)

    def test_PyMirror_Sph_end_set(self):
        """Tests property end setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'end', self._end, self._start + 123.0)

    def test_PyMirror_Sph_end_set_none_not_allowed(self):
        """Tests property end cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.end = None

    def test_PyMirror_Sph_end_must_be_greater_than_start(self):
        """Tests when setting property start that it must be greater than property end"""
        m = self.create_Obj()

        # OK to set it something less than end
        m.end = m.start + 1.0

        # Raises exception when trying to set end less than start
        with self.assertRaises(ValueError) as context:
            m.end = m.start - 1.0

    # Test update_start_end() method
    def test_PyMirror_Sph_update_start_end_invalid(self):
        """Tests the update_start_end() doesn't allow end <= start"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as _:
            m.update_start_end(3.0, 3.0)

        with self.assertRaises(ValueError) as _:
            m.update_start_end(3.0, 2.0)

    def test_PyMirror_Sph_update_start_end_valid(self):
        """Tests the update_start_end() allows start < end"""
        m = self.create_Obj()

        m.update_start_end(2.0, 3.0)

    # Test plot() method
    def test_PyMirror_Sph_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_Obj()

        def gen_plot_points(centre, R, start, end, n_points):
            expected = np.empty((n_points, 2), dtype=np.double)
            
            t = np.linspace(start, end, n_points)
            
            expected[:, 0] = centre[0] + R*np.cos(t)
            expected[:, 1] = centre[1] + R*np.sin(t)

            return expected

        # Test using default number of points of 100
        expected = gen_plot_points(self._centre, self._R, self._start, self._end, n_points=100)
        assert_array_equal(m.plot(), expected)

        # Test using more points
        expected = gen_plot_points(self._centre, self._R, self._start, self._end, n_points=155)
        assert_array_equal(m.plot(n_points=155), expected)


    # Testing correct ray tracing
    # TODO: add tests to verify correct ray tracing

    def test_PyMirror_Sph_tracing(self):
        """Tests a ray is traced correctly"""
        d = 1.0
        centre = np.array([d, 0.0])
        R = 3.0
        start = -60.0 * np.pi/180.0
        end = 60.0 * np.pi/180.0

        c = tr.PyMirror_Sph(centre=centre, R=R, start=start, end=end)

        # Setup ray
        ray_ang = 30 * np.pi/180.0
        r = tr.PyRay(init=np.zeros(2), v=unit_vec(ray_ang))

        tr.PyTrace([c], [r], n=2, fill_up=True)

        # Verify
        expected_ans = np.zeros((3, 2))

        # Intercept where ray hits mirror
        expected_ans[1, 0] = d * np.cos(ray_ang)**2 + np.cos(ray_ang)*np.sqrt(( R**2 - d*np.sin(ray_ang)**2 ))
        expected_ans[1, 1] = np.sqrt(R**2 - (expected_ans[1, 0] - d)**2)

        # Verify, theta is angle ray intersects PyMirrir_Sph measured from
        # centre of PyMirrir_Sph
        theta = np.arctan(expected_ans[1, 1] / (expected_ans[1, 0] - d))

        # angle of incidence and the angle of the new ray (not ang of refl)
        ang_inc = theta - ray_ang

        ray_ref_ang = np.pi + ray_ang + 2*ang_inc

        # Position of ray after reflection
        expected_ans[2] = expected_ans[1] + unit_vec(ray_ref_ang)

        assert_allclose(r.pos, expected_ans)


class Test_PyRefract_Sph(unittest.TestCase, useful_checks):
    """Tests property access and methods of PyRefract_Sph"""
    _centre = np.array([5.6, 7.8])
    _R = 4.5
    _start = 1.2
    _end = 3.4
    _n_in = 1.33
    _n_out = 2.0
    
    def create_Obj(self):
        """Creates an instance of PyRefract_Sph"""
        return tr.PyRefract_Sph(self._centre, self._R, self._start, 
                                self._end, self._n_in, self._n_out)

    # TODO: Test __cinit__()
    def test_PyRefract_Sph_cinit_none_check(self):
        """
        Test PyRefract_Sph c initiliser, check None can't be passed to
        arguments that take numpy arrays
        """
        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Sph(None, self._R, self._start, self._end, 
                                 self._n_in, self._n_out)

    def test_PyRefract_Sph_cinit_shape_check(self):
        """
        Test PyRefract_Sph c initiliser, check passed numpy arrays have 
        correct shape of (2, )
        """
        # Correct shape should pass
        c = tr.PyRefract_Sph(self._centre, self._R, self._start, self._end,
                            self._n_in, self._n_out)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Sph(np.array([1.0]), self._R, self._start, 
                                self._end, self._n_in, self._n_out)

        with self.assertRaises(TypeError) as context:
            c = tr.PyRefract_Sph(np.array([1.0, 2.0, 3.0]), self._R, 
                                self._start, self._end, self._n_in, 
                                self._n_out)

        # Cython checks dimensions before my code does
        with self.assertRaises(ValueError) as context:
            c = tr.PyRefract_Sph(np.array([[1.0, 2.0], [3.0, 4.0]]), self._R, 
                                self._start, self._end, self._n_in, 
                                self._n_out)

    def test_PyRefract_Sph_cinit_neg_R(self):
        """
        Test PyRefract_Sph c initiliser, check R cannot be less than or equal
        to zero
        """

        with self.assertRaises(ValueError) as _:
            c = tr.PyRefract_Sph(self._centre, -1.0, self._start, self._end
                                , self._n_in, self._n_out)

        with self.assertRaises(ValueError) as _:
            c = tr.PyRefract_Sph(self._centre, 0.0, self._start, self._end
                                , self._n_in, self._n_out)

    # Testing property centre
    def test_PyRefract_Sph_centre_get(self):
        """Tests property centre getting"""
        m = self.create_Obj()

        assert_array_equal(m.centre, self._centre)

    def test_PyRefract_Sph_centre_set(self):
        """Tests property centre setting"""
        m = self.create_Obj()

        self.check_writable_np_view_shape_2_set(m, 'centre', self._centre, self._centre + 10.0)

    def test_PyRefract_Sph_centre_set_none_not_allowed(self):
        """Tests property centre cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.centre = None

    # Testing property R
    def test_PyRefract_Sph_R_get(self):
        """Tests property R getting"""
        m = self.create_Obj()

        self.assertEqual(m.R, self._R)

    def test_PyRefract_Sph_R_set(self):
        """Tests property R getting"""
        m = self.create_Obj()

        self.check_float_property(m, 'R', self._R, self._R + 10.0)

    def test_PyRefract_Sph_R_Set_None_not_allowed(self):
        """Tests property R cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.R = None

    def test_PyRefract_Sph_R_Set_Negative_not_allowed(self):
        """Tests property R cannot be R <= 0.0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.R = 0.0

        with self.assertRaises(ValueError) as context:
            m.R = -1.0

    # Testing property start
    def test_PyRefract_Sph_start_get(self):
        """Tests property start getting"""
        m = self.create_Obj()

        self.assertEqual(m.start, self._start)

    def test_PyRefract_Sph_start_set(self):
        """Tests property start setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'start', self._start, self._end - 123.0)
        
    def test_PyRefract_Sph_start_set_none_not_allowed(self):
        """Tests property start can't be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.start = None

    def test_PyRefract_Sph_start_must_be_less_than_end(self):
        """Tests when setting property start that it must be greater than property end"""
        m = self.create_Obj()

        # OK to set it something less than end
        m.start = m.end - 1.0

        # Raises exception if it's more
        with self.assertRaises(ValueError) as context:
            m.start = m.end = 1.0

    # Testing property end
    def test_PyRefract_Sph_end_get(self):
        """Tests property end getting"""
        m = self.create_Obj()

        self.assertEqual(m.end, self._end)

    def test_PyRefract_Sph_end_set(self):
        """Tests property end setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'end', self._end, self._start + 123.0)

    def test_PyRefract_Sph_end_set_none_not_allowed(self):
        """Tests property end cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.end = None

    def test_PyRefract_Sph_end_must_be_greater_than_start(self):
        """Tests when setting property start that it must be greater than property end"""
        m = self.create_Obj()

        # OK to set it something less than end
        m.end = m.start + 1.0

        # Raises exception when trying to set end less than start
        with self.assertRaises(ValueError) as context:
            m.end = m.start - 1.0

    # Test property n_in (efractive index r < R)
    def test_PyRefract_Sph_n_in_get(self):
        """Tests property n_in getting"""
        m = self.create_Obj()

        self.assertEqual(m.n_in, self._n_in)

    def test_PyRefract_Sph_n_in_set(self):
        """Tests property n_in getting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n_in', self._n_in, self._n_in + 10.0)

    def test_PyRefract_Sph_n_in_Set_None_not_allowed(self):
        """Tests property n_in cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.n_in = None

    def test_PyRefract_Sph_n_in_Set_Negative_not_allowed(self):
        """Tests property n_in cannot be n_in <= 0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.n_in = 0.0

        with self.assertRaises(ValueError) as context:
            m.n_in = -1.0

    # Test property n_out (refractive index r > R)
    def test_PyRefract_Sph_n_out_get(self):
        """Tests property n_out getting"""
        m = self.create_Obj()

        self.assertEqual(m.n_out, self._n_out)
        
    def test_PyRefract_Sph_n_out_set(self):
        """Tests property n_out setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n_out', self._n_out, self._n_out + 10.0)

    def test_PyRefract_Sph_n_out_Set_None_not_allowed(self):
        """Tests property n_out cannot be set to None"""
        m = self.create_Obj()

        with self.assertRaises(TypeError) as context:
            m.n_out = None

    def test_PyRefract_Sph_n_out_Set_Negative_not_allowed(self):
        """Tests property n_out cannot be n_out <= 0.0"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as context:
            m.n_out = 0.0

        with self.assertRaises(ValueError) as context:
            m.n_out = -1.0

    # Test update_start_end() method
    def test_PyRefract_Sph_update_start_end_invalid(self):
        """Tests the update_start_end() doesn't allow end <= start"""
        m = self.create_Obj()

        with self.assertRaises(ValueError) as _:
            m.update_start_end(3.0, 3.0)

        with self.assertRaises(ValueError) as _:
            m.update_start_end(3.0, 2.0)

    def test_PyRefract_Sph_update_start_end_valid(self):
        """Tests the update_start_end() allows start < end"""
        m = self.create_Obj()

        m.update_start_end(2.0, 3.0)

    # Test plot() method
    def test_PyRefract_Sph_plot(self):
        """Tests the plot method returns start point followed by end point"""
        m = self.create_Obj()

        def gen_plot_points(centre, R, start, end, n_points):
            expected = np.empty((n_points, 2), dtype=np.double)
            
            t = np.linspace(start, end, n_points)
            
            expected[:, 0] = centre[0] + R*np.cos(t)
            expected[:, 1] = centre[1] + R*np.sin(t)

            return expected

        # Test using default number of points of 100
        expected = gen_plot_points(self._centre, self._R, self._start, self._end, n_points=100)
        assert_array_equal(m.plot(), expected)

        # Test using more points
        expected = gen_plot_points(self._centre, self._R, self._start, self._end, n_points=155)
        assert_array_equal(m.plot(n_points=155), expected)


    # Testing correct ray tracing
    # TODO: add tests to verify correct ray tracing

    def test_PyRefract_Sph_tracing(self):
        """Tests a ray is traced correctly through a PyRefract_Sph"""
        d = 1.0  # X offset for centre of PyRefract_Sph 
        centre = np.array([d, 0.0])
        R = 3.0
        start = -60.0 * np.pi/180.0
        end = 60.0 * np.pi/180.0
        n_in = 2.0
        n_out = 3.0

        c = tr.PyRefract_Sph(centre=centre, R=R, start=start, end=end, 
                                n_in=n_in, n_out=n_out)

        # Setup ray
        ray_ang = 30 * np.pi/180.0
        r = tr.PyRay(init=np.zeros(2), v=unit_vec(ray_ang))

        tr.PyTrace([c], [r], n=2, fill_up=True)

        # Verify
        expected_ans = np.zeros((3, 2))

        # Intercept where ray hits PyRefract_Sph
        expected_ans[1, 0] = d * np.cos(ray_ang)**2 + np.cos(ray_ang)*np.sqrt(( R**2 - d*np.sin(ray_ang)**2 ))
        expected_ans[1, 1] = np.sqrt(R**2 - (expected_ans[1, 0] - d)**2)

        # Verify, theta is angle ray intersects PyRefract_Sph measured from
        # centre of PyRefract_Sph
        theta = np.arctan(expected_ans[1, 1] / (expected_ans[1, 0] - d))

        # angle of incidence
        ang_inc = theta - ray_ang

        # Apply Snell's law
        ray_ref_ang = theta - np.arcsin(np.sin(ang_inc) * n_in / n_out)

        # Position of ray after refraction
        expected_ans[2] = expected_ans[1] + unit_vec(ray_ref_ang)

        assert_allclose(r.pos, expected_ans)


class Test_PyLens(unittest.TestCase, useful_checks):
    """Tests for PyLens"""
    _lens_centre = np.zeros(2)
    _R_lens = 2
    _R1 = 4.0
    _R2 = 6.0
    _d = 0.2
    _n_in = 1.33
    _n_out = 1.0

    def create_Obj(self):
        """Creates an instance of PyLens for testing"""

        return tr.PyLens(self._lens_centre, self._R_lens, self._R1, self._R2, 
                        self._d, self._n_in, self._n_out)

    # TODO: test __init__()
    def test_PyLens_init_allowed_R1(self):
        """
        Test PyLens initiliser, check R1 cannot be -R_lens < R1 < R_lens
        """

        # These should be ok
        c = tr.PyLens(self._lens_centre, self._R_lens, -self._R_lens - 1.0, 
                        self._R2, self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens, -self._R_lens, self._R2, 
                        self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens, self._R_lens, self._R2, 
                        self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens, self._R_lens + 1.0, 
                        self._R2, self._d, self._n_in, self._n_out)

        # These should all fail
        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, -self._R_lens/2, 
                        self._R2, self._d, self._n_in, self._n_out)

        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, self._R_lens/2, 
                        self._R2, self._d, self._n_in, self._n_out)

        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, 0.0, 
                        self._R2, self._d, self._n_in, self._n_out)

    def test_PyLens_init_allowed_R2(self):
        """
        Test PyLens initiliser, check R2 cannot be -R_lens < R2 < R_lens
        """

        # These should be ok
        c = tr.PyLens(self._lens_centre, self._R_lens, self._R1, -self._R_lens-1.0,
                         self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens,  self._R1, -self._R_lens,
                        self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens,  self._R1, self._R_lens,
                        self._d, self._n_in, self._n_out)

        c = tr.PyLens(self._lens_centre, self._R_lens, self._R1, self._R_lens + 1.0,
                          self._d, self._n_in, self._n_out)

        # These should all fail
        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, self._R1,
                         -self._R_lens/2,  self._d, self._n_in, self._n_out)

        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, self._R1,
                        self._R_lens/2,  self._d, self._n_in, self._n_out)

        with self.assertRaises(ValueError) as _:
            c = c = tr.PyLens(self._lens_centre, self._R_lens, self._R1,
                        0.0,  self._d, self._n_in, self._n_out)

    # Testing property lens_centre
    def test_PyLens_lens_centre_get(self):
        """Tests property lens_centre getting"""
        m = self.create_Obj()

        assert_array_equal(m.lens_centre, self._lens_centre)

    def test_PyLens_lens_centre_set(self):
        """Tests property lens_centre setting"""
        m = self.create_Obj()

        self.check_writable_np_view_shape_2_set(m, 'lens_centre', self._lens_centre, self._lens_centre + 10.0)

    # Testing property R_lens
    def test_PyLens_R_lens_get(self):
        """Tests property R_lens getting"""
        m = self.create_Obj()

        self.assertEqual(m.R_lens, self._R_lens)

    # Testing property R1
    def test_PyLens_R1_get(self):
        """Tests property R1 getting"""
        m = self.create_Obj()

        self.assertEqual(m.R1, self._R1)

    def test_PyLens_R1_set(self):
        """Tests property R1 setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'R1', self._R1, self._R1 + 0.5)

    def test_PyLens_R1_set_invalid(self):
        """Tests property R1 can't be set -R_lens < R1 < R_lens"""
        m = self.create_Obj()

        with self.assertRaises(ValueError):
            m.R1 = -self._R_lens*0.99

        with self.assertRaises(ValueError):
            m.R1 = 0.0

        with self.assertRaises(ValueError):
            m.R1 = self._R_lens*0.99

    # Testing property R2
    def test_PyLens_R2_get(self):
        """Tests property R2 getting"""
        m = self.create_Obj()

        self.assertEqual(m.R2, self._R2)

    def test_PyLens_R2_set(self):
        """Tests property R2 setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'R2', self._R2, self._R2 + 0.5)

    def test_PyLens_R2_set_invalid(self):
        """Tests property R2 can't be set -R_lens < R2 < R_lens"""
        m = self.create_Obj()

        with self.assertRaises(ValueError):
            m.R2 = -self._R_lens*0.99

        with self.assertRaises(ValueError):
            m.R2 = 0.0

        with self.assertRaises(ValueError):
            m.R2 = self._R_lens*0.99

    # Testing property d
    def test_PyLens_d_get(self):
        """Tests property d getting"""
        m = self.create_Obj()

        self.assertEqual(m.d, self._d)

    # Testing property n_in
    def test_PyLens_n_in_get(self):
        """Tests property n_in getting"""
        m = self.create_Obj()

        self.assertEqual(m.n_in, self._n_in)

    def test_PyLens_n_in_set(self):
        """Tests property n_in setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n_in', self._n_in, self._n_in + 0.5)

    # Testing property n_out
    def test_PyLens_n_out_get(self):
        """Tests property n_out getting"""
        m = self.create_Obj()

        self.assertEqual(m.n_out, self._n_out)

    def test_PyLens_n_out_set(self):
        """Tests property n_out setting"""
        m = self.create_Obj()

        self.check_float_property(m, 'n_out', self._n_out, self._n_out + 0.5)

    # TODO: add tracing tests


if __name__ == '__main__':
    unittest.main()
