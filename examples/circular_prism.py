# Example of how to define a complex component in Python
# Creates and traces multiple rays through a semi-circular
# prism 

import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyRefract_Plane, PyRefract_Sph, PyCC_Wrap


class SemiCircPrism(PyCC_Wrap):
	
	def __init__(self, centre, R, n_in, n_out=1.0):
		left, right = centre.copy(), centre.copy()
		
		left[0] -= R
		right[0] += R
		
		comps = [
					PyRefract_Plane(left, right, n_in, n_out),
					PyRefract_Sph(centre, R, start=0.0, end=np.pi, n_in=n_in, n_out=n_out)
				]
		
		super().__init__(comps)  # Must remember to call super __init__


centre = np.array([0.0, 0.0])
R = 1.0
n_in = 1.33
n_out = 1.0

c = SemiCircPrism(centre, R, n_in, n_out)

# Incidence angles for rays
ray_angles = np.linspace(90.0, 160.0, 8)*np.pi/180.0

unit_vecs = [np.array([np.cos(ang), np.sin(ang)]) for ang in ray_angles]

rays = [PyRay(1.5*R*uv, -uv) for uv in unit_vecs]

PyTrace([c], rays, n=4)

# Plotting
plt.gca().set_aspect('equal')

# Plot components
for c_plt in c.plot():
	m_x, m_y = c_plt.T
	plt.plot(m_x, m_y, color="C0")

# Plot rays
for i, (r, d) in enumerate(zip(rays, unit_vecs)):
	r_x, r_y = r.plot().T
	plt.plot(r_x, r_y, color=f"C{i + 1 % 10}")
	
	# Plot an arrow to show direction of ray
	arrow_x = r_x[1] + (r_x[0]-r_x[1])/2
	arrow_y = r_y[1] + (r_y[0]-r_y[1])/2
	
	plt.arrow(arrow_x, arrow_y, -d[0]/100, -d[1]/100, color=f"C{i + 1 % 10}",
			   length_includes_head=True, head_width=.05)

plt.show()


print("End of program")

