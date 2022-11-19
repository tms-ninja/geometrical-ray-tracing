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

