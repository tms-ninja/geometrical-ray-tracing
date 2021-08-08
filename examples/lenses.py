import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyLens, PyBiConvexLens



centre = np.array([0.0, 0.0])

l = PyBiConvexLens(centre=centre, R_lens=2, R1=4, R2=4, d=0.2, n_in=1.33, n_out=1.0)

comps = [l, PyLens(centre=np.array([2.5, 0.0]), R_lens=2, R1=-4, R2=-4, d=1.5, n_in=2.0, n_out=1.0)]

ray_starting_y = np.linspace(-1.8, 1.8, 8)

rays = [PyRay(np.array([-1.0, y]), np.array([1.0, 0.0])) for y in ray_starting_y]

# Tracing
PyTrace(comps, rays, n=6)

# Plotting
plt.gca().set_aspect('equal')

for c in comps:

    for sub_comp in c.plot():
        c_x, c_y = sub_comp.T

        plt.plot(c_x, c_y, color="C0")

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

