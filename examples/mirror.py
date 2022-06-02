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


# Simple example to show a ray interacting with a plane mirror

import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyMirror_Plane


m = PyMirror_Plane(np.array([0.0, 1.0]), np.array([1.0, 0.0]))

r = PyRay(np.array([-0.5, 0.5]), np.array([1.0, 0.0]))

# Initial direction of the ray
d = r.v.copy()

PyTrace([m], [r], 2)

m_x, m_y = m.plot().T
r_x, r_y = r.pos.T

# Plot mirror and ray
plt.plot(m_x, m_y)
plt.plot(r_x, r_y)

# Plot an arrow to show direction of ray
arrow_x = r_x[1] + (r_x[0]-r_x[1])/2
arrow_y = r_y[1] + (r_y[0]-r_y[1])/2

plt.arrow(arrow_x, arrow_y, d[0]/100, d[1]/100, color="C1",
			length_includes_head=True, head_width=.05)

plt.gca().set_aspect('equal')
plt.show()
