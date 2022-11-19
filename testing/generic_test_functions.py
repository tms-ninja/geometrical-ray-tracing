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
from numpy.testing import assert_array_equal


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

