import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyCC_Wrap, PyRefract_Plane, PyRefract_Sph

class lens(PyCC_Wrap):
    def __init__(self, centre, R_lens, R1, R2, d, n_in, n_out=1.0) -> None:
        """
        R_lens is the radius of the len itself
        R1 is radius of curvature on left, R2 on the right
        d is the width of the lens between each circular part
        """
        # cetres of the arcs used to describe lens
        left_centre = centre.copy()
        left_centre[0] += np.sqrt(R1**2 - R_lens**2) - d/2
        left_ang = np.arcsin(R_lens / R1)

        right_centre = centre.copy()
        right_centre[0] -= np.sqrt(R2**2 - R_lens**2) - d/2
        right_ang = np.arcsin(R_lens / R2)

        c_x, c_y = centre

        # positions o 
        top_left = np.array([c_x - d/2, c_y + R_lens])
        top_right = np.array([c_x + d/2, c_y + R_lens])
        bottom_left = np.array([c_x - d/2, c_y - R_lens])
        bottom_right = np.array([c_x + d/2, c_y - R_lens])

        comps = [
            PyRefract_Sph(left_centre, R1, np.pi-left_ang, np.pi+left_ang, n_out, n_in),
            PyRefract_Plane(bottom_left, bottom_right, n_in, n_out),
            PyRefract_Sph(right_centre, R1, -right_ang, right_ang, n_out, n_in),
            PyRefract_Plane(top_right, top_left, n_in, n_out),
        ]

        super().__init__(comps)

class ConvexLens(lens):
    def __init__(self, centre, R_lens, R1, R2, n_in, n_out=1.0) -> None:
        """
        R_lens is the radius of the len itself
        R1 is radius of curvature on left, R2 on the right
        """
        super().__init__(centre, R_lens, R1, R2, d=0.2, n_in=n_in, n_out=n_out)


centre = np.array([0.0, 0.0])

l = ConvexLens(centre=centre, R_lens=2, R1=4, R2=4, n_in=1.33, n_out=1.0)

comps = [l, ConvexLens(centre=np.array([3.0, 0.0]), R_lens=2, R1=4, R2=4, n_in=1.33, n_out=1.0)]

ray_starting_y = np.linspace(-1.8, 1.8, 8)

rays = [PyRay(np.array([-1.0, y]), np.array([1.0, 0.0])) for y in ray_starting_y]

# Tracing
PyTrace(comps, rays, n=6)

# Plotting
plt.gca().set_aspect('equal')

for c in comps:
    c_x, c_y = c.plot().T

    plt.plot(c_x, c_y, color="C0")

for i, r in enumerate(rays):
    pos = r.plot().T
    r_x, r_y = pos
    plt.plot(r_x, r_y, color=f"C{i + 1 % 10}")
    
    # Plot an arrow to show direction of ray
    arrow_x = r_x[1] + (r_x[0]-r_x[1])/2
    arrow_y = r_y[1] + (r_y[0]-r_y[1])/2
    
    d = pos[1] - pos[1]

    plt.arrow(arrow_x, arrow_y, -d[0]/100, -d[1]/100, color=f"C{i + 1 % 10}",
               length_includes_head=True, head_width=.05)

plt.show()

print("End of program")

