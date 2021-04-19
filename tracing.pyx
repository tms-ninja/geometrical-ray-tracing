# distutils: language = c++
from cython.operator import dereference
#from libcpp.memory import unique_ptr, make_unique
from libcpp.vector cimport vector
from cython_header cimport *

import numpy as np


cdef make_numpy_from_arr(arr& a):
	return np.array([a[0], a[1]])

cdef arr make_arr_from_numpy(double[:] n):
	assert tuple(n.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
	
	cdef arr a
	
	a[0] = n[0]
	a[1] = n[1]
	
	return a

cdef class PyMirror_Plane:
	cdef Mirror_Plane* c_data
	
	def __cinit__(self, double[:] a, double[:] b):
		assert tuple(a.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		assert tuple(b.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
		
		cdef arr x1, x2
		
		x1[0] = a[0]
		x1[1] = a[1]
		
		x2[0] = b[0]
		x2[1] = b[1]
		
		self.c_data = new Mirror_Plane(x1, x2)
		
	def __dealloc__(self):
		del self.c_data
		
	@property
	def start(self):
		return make_numpy_from_arr(dereference(self.c_data).start)
	
	@start.setter
	def start(self, double[:] start):
		dereference(self.c_data).start = make_arr_from_numpy(start)
		
	@property
	def end(self):
		return make_numpy_from_arr(dereference(self.c_data).end)
	
	@end.setter
	def end(self, double[:] end):
		dereference(self.c_data).end = make_arr_from_numpy(end)