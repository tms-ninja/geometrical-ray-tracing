# Simple example to show a ray interacting with a mirror

import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyMirror_Plane


m = PyMirror_Plane(np.array([0.0, 1.0]), np.array([1.0, 0.0]))

r = PyRay(np.array([-0.5, 0.5]), np.array([1.0, 0.0]))

PyTrace([m], [r], 2)

m_x, m_y = m.plot().T
r_x, r_y = r.pos.T

plt.gca().set_aspect('equal')

plt.plot(m_x, m_y)
plt.plot(r_x, r_y)
plt.show()
