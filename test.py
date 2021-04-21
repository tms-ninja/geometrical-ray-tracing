from tracing import PyMirror_Plane, PyRefract_Plane, PyRay, PyTrace
import numpy as np

a = np.array([1.2, 3.4])
b = np.array([5.6, 7.8])
c = np.array([14.6, 6.8])

m = PyMirror_Plane(a, b)

print(f"Mirror has start {m.start} and end {m.end}")
print(f"Changing mirror's start to {c}")

m.start = c

print(f"Mirror's new start is {m.start} and end is still {m.end}")
print()


p = PyRefract_Plane(a, b, 1.5, 2.4)

print(f"p is a refract plane with {p.start=}, {p.end=}, {p.n1=}, {p.n2=}")
print("Changing p.n1 to 9.8")

p.n1 = 9.8

print(f"p is a refract plane with {p.start=}, {p.end=}, {p.n1=}, {p.n2=}")
print()


r = PyRay(a, b)

print(f"Ray's v is {r.v}")
print("Ray's position is:")

print(r.pos)
print()


comps = [PyMirror_Plane(np.array([0.0, -1.0]), np.array([0.25, 0.5]))]


rays = [PyRay(np.array([0.0, 0.0]), np.array([0.83580736, 0.54902282]))]

PyTrace(comps, rays, 3)

print(rays[0].pos)

