# distutils: language = c++
from cython.operator import dereference
#from libcpp.memory import unique_ptr, make_unique
from libcpp.vector cimport vector
from cython_header cimport *

import numpy as np


cdef make_numpy_from_arr(arr& a):
	return np.array([a[0], a[1]])

cdef arr make_arr_from_numpy(double[:] n):
	cdef arr a
	
	a[0] = n[0]
	a[1] = n[1]
	
	return a
	
# cdef class PyRay:
	# cdef Ray* c_data
	
	# def __cinit__(self, double 

cdef class PyMirror_Plane:
	cdef Mirror_Plane* c_data
	
	def __cinit__(self, double[:] start, double[:] end):
		assert tuple(start.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		assert tuple(end.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		
		self.c_data = new Mirror_Plane(make_arr_from_numpy(start), make_arr_from_numpy(end))
		
	def __dealloc__(self):
		del self.c_data
		
	@property
	def start(self):
		return make_numpy_from_arr(dereference(self.c_data).start)
	
	@start.setter
	def start(self, double[:] start):
		assert tuple(start.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		dereference(self.c_data).start = make_arr_from_numpy(start)
		
	@property
	def end(self):
		return make_numpy_from_arr(dereference(self.c_data).end)
	
	@end.setter
	def end(self, double[:] end):
		assert tuple(end.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		dereference(self.c_data).end = make_arr_from_numpy(end)