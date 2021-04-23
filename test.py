from tracing import PyMirror_Plane, PyRefract_Plane, PyRay, PyTrace
import numpy as np
import matplotlib.pyplot as plt

print()

a = np.array([1.2, 3.4])
b = np.array([5.6, 7.8])
c = np.array([14.6, 6.8])

m = PyMirror_Plane(a, b)

print(f"Mirror has start {m.start} and end {m.end}")
print(f"Changing mirror's start to {c}")

m.start = c

print(f"Mirror's new start is {m.start} and end is still {m.end}")
print("Changing x component of mirror's start to 5.5")

m.start[0] = 5.5

print(f"Mirror's new start is {m.start} and end is still {m.end}")
print()
print(f"Does the mirror own its data? {m.OWNDATA}")
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


comps = [] #[PyRefract_Plane(np.array([0.0, -1.0]), np.array([0.25, 0.5]), 1.0, 2)]

comps.append(PyMirror_Plane(np.array([0.0, 1.0]), np.array([2.0, -1.0])))

#comps.append(PyMirror_Plane(np.array([-5.0, 5.0]), np.array([2.0, -10.0])))


theta = 60.0 * np.pi / 180.0

rays = [PyRay(np.array([0.0, 0.0]), np.array([np.cos(theta), np.sin(theta)]))]

PyTrace(comps, rays, 3)

print(rays[0].pos)


# Test plotting
plt.figure(figsize=(6, 6))

for cp in comps:
    points = cp.plot()
    
    plt.plot(points[:, 0], points[:, 1])

for ry in rays:
    points = ry.plot()
    
    plt.plot(points[:, 0], points[:, 1])


plt.gca().set_aspect('equal')
plt.show()













