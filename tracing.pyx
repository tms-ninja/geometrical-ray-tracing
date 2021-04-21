# distutils: language = c++
from cython.operator import dereference
#from libcpp.memory import unique_ptr, make_unique
from libcpp.vector cimport vector
from libcpp cimport bool
from cython_header cimport *

import numpy as np


cdef make_numpy_from_arr(arr& a):
    cdef double[::1] a_mem_view = <double [:a.size()]>a.data()
    
    return np.asarray(a_mem_view)

cdef arr make_arr_from_numpy(double[:] n):
    cdef arr a
    
    a[0], a[1] = n[0], n[1]
    
    return a
    

def PyTrace(list components, list rays, int n, bool fill_up=True):
    cdef vector[Component*] vec_comp
    
    for c in components:
        if isinstance(c, PyMirror_Plane):
            vec_comp.push_back( <Component*>( (<PyMirror_Plane>c).c_data  ) )
            
        elif isinstance(c, PyRefract_Plane):
            vec_comp.push_back( <Component*>( (<PyRefract_Plane>c).c_data  ) )
        
    cdef vector[Ray*] vec_rays
    
    for r in rays:
        vec_rays.push_back( (<PyRay>r).c_data )
        
    trace(vec_comp, vec_rays, n, fill_up)


cdef class PyRay:
    cdef Ray* c_data
    
    def __cinit__(self, double[:] init not None, double[:] v not None):
        assert tuple(init.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        assert tuple(v.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        
        self.c_data = new Ray(make_arr_from_numpy(init), 
                              make_arr_from_numpy(v))
        
    def __dealloc__(self):
        del self.c_data
        
    @property
    def pos(self):
        n = dereference(self.c_data).pos.size()
        
        ans = np.empty((n, 2), dtype=np.double)
        
        for i in range(n):
            ans[i, 0] = dereference(self.c_data).pos[i][0]
            ans[i, 1] = dereference(self.c_data).pos[i][1]
        
        return ans
    
    @property
    def v(self):
        return make_numpy_from_arr(dereference(self.c_data).v)
    @v.setter
    def v(self, double[:] v not None):
        assert tuple(v.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        
        dereference(self.c_data).v = make_arr_from_numpy(v)
    
    
cdef class _PyPlane:
    cdef Plane* c_plane_ptr
    
    # No __dealloc__ as memory managed by subclass
    cdef load_ptr(self, Plane* ptr):  
        c_plane_ptr = ptr
        
    @property
    def start(self):
        return make_numpy_from_arr(dereference(self.c_plane_ptr).start)
    @start.setter
    def start(self, double[:] start):
        assert tuple(start.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        dereference(self.c_plane_ptr).start = make_arr_from_numpy(start)
        
    @property
    def end(self):
        return make_numpy_from_arr(dereference(self.c_plane_ptr).end)
    @end.setter
    def end(self, double[:] end):
        assert tuple(end.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        dereference(self.c_plane_ptr).end = make_arr_from_numpy(end)


cdef class PyMirror_Plane(_PyPlane):
    cdef Mirror_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end):
        assert tuple(start.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        assert tuple(end.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        
        self.c_data = new Mirror_Plane(make_arr_from_numpy(start), 
                                       make_arr_from_numpy(end))
        
        self.c_plane_ptr = <Plane*>self.c_data
        
    def __dealloc__(self):
        del self.c_data


cdef class PyRefract_Plane(_PyPlane):
    cdef Refract_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end, double n1=1.0, 
                  double n2=1.0):
        
        assert tuple(start.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        assert tuple(end.shape) == (2, 0, 0, 0, 0, 0, 0, 0)
        
        self.c_data = new Refract_Plane(make_arr_from_numpy(start), 
                                        make_arr_from_numpy(end), n1, n2)
        
        self.c_plane_ptr = <Plane*>self.c_data
        
    def __dealloc__(self):
        del self.c_data
    
    @property
    def n1(self):
        return dereference(self.c_data).n1
    @n1.setter
    def n1(self, n1):
        dereference(self.c_data).n1 = n1
    
    @property
    def n2(self):
        return dereference(self.c_data).n2
    @n2.setter
    def n2(self, n2):
        dereference(self.c_data).n2 = n2