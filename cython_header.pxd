# distutils: language = c++
from libcpp.vector cimport vector


cdef extern from "<array>" namespace "std" nogil:
	cdef cppclass arr "std::array<double, 2>":
		arr() except+
		double& operator[](size_t)

cdef extern from "Ray.cpp":
	pass
	
cdef extern from "Ray.h":
	cdef cppclass Ray:
		pass

cdef extern from "general.cpp":
	pass

cdef extern from "general.h":
	pass

cdef extern from "Component.cpp":
	cdef cppclass Component:
		pass
	
cdef extern from "Component.h":
		pass

cdef extern from "Plane.cpp":
	pass
	
cdef extern from "Plane.h":
	cdef cppclass Plane(Component):
		pass
	
cdef extern from "Mirror_Plane.cpp":
	pass
	
cdef extern from "Mirror_Plane.h":
	cdef cppclass Mirror_Plane(Plane):
		Mirror_Plane(arr, arr) except+
		arr start, end
		double test_hit(Ray&)
		void hit(Ray&, int)
	