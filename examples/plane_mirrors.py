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


# Models a ray bouncing inside a mirrored polygon
import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyMirror_Plane

# Number of sides of polygon
N = 5
comps = []

for i in range(N):
    start = 10.0 * np.array([np.cos(i*2*np.pi/N), np.sin(i*2*np.pi/N)])
    end = 10.0 * np.array([np.cos((i+1)*2*np.pi/N), np.sin((i+1)*2*np.pi/N)])
    
    comps.append(PyMirror_Plane(start, end))

theta = 10 * np.pi/180.0

r = PyRay(np.array([-2.0, 0.0]), np.array([np.cos(theta), np.sin(theta)]))

PyTrace(comps, [r], 40)


for c in comps:
    c_x, c_y = c.plot().T
    
    plt.plot(c_x, c_y, color='C0')
    

r_x, r_y = r.plot().T

plt.plot(r_x, r_y, color='C1')

plt.gca().set_aspect('equal')

plt.show()

