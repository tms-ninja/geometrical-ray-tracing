import numpy as np
import matplotlib.pyplot as plt

from tracing import PyTrace, PyRay, PyLens, PyBiConvexLens, PyCC_Wrap


class LensCombo(PyCC_Wrap):
    def __init__(self, centre_1, centre_2) -> None:
        lens_1_param = {
            'centre': centre_1,
            'R_lens': 2, 
            'R1': 4, 
            'R2': 4, 
            'd': 0.2, 
            'n_in': 1.33, 
            'n_out': 1.0
        }

        lens_2_param = {
            'centre': centre_2,
            'R_lens': 2, 
            'R1': -4, 
            'R2': -4, 
            'd': 1.5, 
            'n_in': 2.0, 
            'n_out': 1.0
        }

        super().__init__([PyBiConvexLens(**lens_1_param), PyLens(**lens_2_param)])

    def plot(self):
        return super().plot(flatten=False)

def crawl(lst):
    """Crawls a nested list and yields none-list items"""
    
    if isinstance(lst, list):  # If lst is a list, we want to crawl its elements
        for elem in lst:
            yield from crawl(elem)
    else:
        yield lst

comps = [LensCombo(np.array([0.0, 0.0]), np.array([2.5, 0.0]))]

ray_starting_y = np.linspace(-1.8, 1.8, 8)

rays = [PyRay(np.array([-1.0, y]), np.array([1.0, 0.0])) for y in ray_starting_y]

# Tracing
PyTrace(comps, rays, n=6)

# Plotting
plt.gca().set_aspect('equal')

for c in comps:

    for sub_comp in crawl(c.plot()):
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

