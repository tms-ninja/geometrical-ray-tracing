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

