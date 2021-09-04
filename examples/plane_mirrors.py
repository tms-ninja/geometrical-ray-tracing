import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyMirror_Plane

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

