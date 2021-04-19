from tracing import *
import numpy as np

a = np.array([1.2, 3.4])
b = np.array([5.6, 7.8])
c = np.array([14.6, 6.8])

m = PyMirror_Plane(a, b)

print(f"Mirror has start {m.start} and end {m.end}")
print(f"Chaning mirror's start to {c}")

m.start = c

print(f"Mirror's new start is {m.start} and end is still {m.end}")

r = PyRay(a, b)

print(f"Ray's v is {r.v}")
print("Ray's position is:")

print(r.pos)

