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
					PyRefract_Sph(centre, R, start=0.0, end=np.pi, n1=n_in, n2=n_out)
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

PyTrace([c], rays, n=3)

# Plotting
plt.gca().set_aspect('equal')

m_x, m_y = c.plot().T
plt.plot(m_x, m_y)


for r in rays:
	r_x, r_y = r.plot().T
	plt.plot(r_x, r_y)

plt.show()


print("End of program")

