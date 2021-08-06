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


ray_angle = 120.0*np.pi/180.0

unit_vec = np.array([np.cos(ray_angle), np.sin(ray_angle)])

r = PyRay(1.5*R*unit_vec, -unit_vec) 

PyTrace([c], [r], n=3)

# Plotting
m_x, m_y = c.plot().T
r_x, r_y = r.pos.T

plt.gca().set_aspect('equal')

plt.plot(m_x, m_y)
plt.plot(r_x, r_y)
plt.show()


print("End of program")

