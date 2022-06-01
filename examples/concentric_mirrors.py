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


# Models a ray interacting between two concentric, circular mirrors
import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyMirror_Sph


m1 = PyMirror_Sph(np.zeros(2), 5.0, 0.0, 2*np.pi)
m2 = PyMirror_Sph(np.zeros(2), 10.0, 0.0, 2*np.pi)

comps = [m1, m2]


theta = 10 * np.pi/180.0

r = PyRay(np.array([-8.0, 0.0]), np.array([np.cos(theta), np.sin(theta)]))

PyTrace(comps, [r], 40)


for c in comps:
    c_x, c_y = c.plot().T
    
    plt.plot(c_x, c_y, color='C0')
    

r_x, r_y = r.plot().T

plt.plot(r_x, r_y, color='C1')

plt.gca().set_aspect('equal')

plt.show()

