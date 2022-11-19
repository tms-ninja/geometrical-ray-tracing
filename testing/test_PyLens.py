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

