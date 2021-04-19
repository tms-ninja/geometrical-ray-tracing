from tracing import *
import numpy as np

start = np.array([1.2, 3.4])
end = np.array([5.6, 7.8])

m = PyMirror_Plane(start, end)

print(f"Mirror has start {m.start} and end {m.end}")

