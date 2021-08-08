import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyCC_Wrap, PyRefract_Plane, PyRefract_Sph

class Lens(PyCC_Wrap):
    def __init__(self, centre, R_lens, R1, R2, d, n_in, n_out=1.0) -> None:
        """
        R_lens is the radius of the len itself
        R1 is radius of curvature on left, R2 on the right
        d is the width of the lens between each circular part
        """
        if R1 >= R_lens:
            # Convex
            # cetres of the arcs used to describe lens
            left_centre = centre.copy()
            left_centre[0] += np.sqrt(R1**2 - R_lens**2) - d/2
            left_ang = np.arcsin(R_lens / R1)

            left_arc = PyRefract_Sph(left_centre, R1, np.pi-left_ang, np.pi+left_ang, n_out, n_in)

        elif R1 <= -R_lens:
            # Concanve
            left_centre = centre.copy()
            left_centre[0] -= np.sqrt(R1**2 - R_lens**2) + d/2
            left_ang = np.arcsin(-R_lens / R1)   

            left_arc = PyRefract_Sph(left_centre, -R1, -left_ang, left_ang, n_in, n_out)

        else:
            raise ValueError(f"{R1 = } is invalid")


        if R2 >= R_lens:
            # Convex
            # cetres of the arc used to describe lens
            right_centre = centre.copy()
            right_centre[0] -= np.sqrt(R2**2 - R_lens**2) - d/2
            right_ang = np.arcsin(R_lens / R2)

            right_arc = PyRefract_Sph(right_centre, R2, -right_ang, right_ang, n_out, n_in)

        elif R2 <= -R_lens:
            # Concanve
            right_centre = centre.copy()
            right_centre[0] += np.sqrt(R2**2 - R_lens**2) + d/2
            right_ang = np.arcsin(-R_lens / R2)

            right_arc = PyRefract_Sph(right_centre, -R2, np.pi-right_ang, np.pi+right_ang, n_in, n_out)

        else:
            raise ValueError(f"{R2 = } is invalid")


        c_x, c_y = centre

        # positions of "box"
        top_left = np.array([c_x - d/2, c_y + R_lens])
        top_right = np.array([c_x + d/2, c_y + R_lens])
        bottom_left = np.array([c_x - d/2, c_y - R_lens])
        bottom_right = np.array([c_x + d/2, c_y - R_lens])

        comps = [
            left_arc,
            PyRefract_Plane(bottom_left, bottom_right, n_in, n_out),
            right_arc,
            PyRefract_Plane(top_right, top_left, n_in, n_out),
        ]

        super().__init__(comps)

    def plot(self):
        # Return list of sub-comp plots to avoid needing them in the correct order 
        return super().plot(flatten=False)

class ConvexLens(Lens):
    def __init__(self, centre, R_lens, R1, R2, n_in, n_out=1.0) -> None:
        """
        R_lens is the radius of the len itself
        R1 is radius of curvature on left, R2 on the right
        """
        super().__init__(centre, R_lens, R1, R2, d=0.2, n_in=n_in, n_out=n_out)


centre = np.array([0.0, 0.0])

l = ConvexLens(centre=centre, R_lens=2, R1=4, R2=4, n_in=1.33, n_out=1.0)

comps = [l, Lens(centre=np.array([2.5, 0.0]), R_lens=2, R1=-4, R2=-4, d=1.5, n_in=2.0, n_out=1.0)]

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

