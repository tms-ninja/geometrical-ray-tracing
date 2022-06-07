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


# Simple example to show a lens focusing light onto a screen

import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyBiConvexLens, PyScreen_Plane

# This is useful as the plotting routine returns a nested list with the leaves
# corresponding to the plotting data
def crawl(lst):
    """Crawls a nested list and yields none-list items"""
    
    if isinstance(lst, list):  # If lst is a list, we want to crawl its elements
        for elem in lst:
            yield from crawl(elem)
    else:
        yield lst

# Setup lens and rays

lens_1_param = {
            'lens_centre': np.zeros(2),
            'R_lens': 2, 
            'R1': 4, 
            'R2': 4, 
            'd': 0.2, 
            'n_in': 1.33, 
            'n_out': 1.0
        }

lens = PyBiConvexLens(**lens_1_param)
screen = PyScreen_Plane(np.array([4.0, -2.0]), np.array([4.0, 2.0]))

comps = [lens, screen]


ray_starting_y = np.linspace(-1.8, 1.8, 8)

rays = [PyRay(np.array([-1.0, y]), np.array([1.0, 0.0])) for y in ray_starting_y]

# Initial direction of the ray
# Note in the plot even though we specify more interactions, Pytrace doesn't
# stops tracing at the screen
PyTrace(comps, rays, 6)

# Plotting
plt.gca().set_aspect('equal')

# Plot components
for c in comps:
    for sub_comp in crawl(c.plot()):
        c_x, c_y = sub_comp.T

        plt.plot(c_x, c_y, color="C0")

# Plot rays with arrows
for i, r in enumerate(rays):
    pos_plt = r.plot()
    pos = pos_plt.T
    r_x, r_y = pos
    plt.plot(r_x, r_y, color=f"C{i + 1 % 10}")
    
    # Plot an arrow to show direction of ray
    arrow_x = r_x[1] + (r_x[0]-r_x[1])/2
    arrow_y = r_y[1] + (r_y[0]-r_y[1])/2
    
    d = pos_plt[1] - pos_plt[0]

    plt.arrow(arrow_x, arrow_y, d[0]/100, d[1]/100, color=f"C{i + 1 % 10}",
               length_includes_head=True, head_width=.1)

plt.show()

print("End of program")

