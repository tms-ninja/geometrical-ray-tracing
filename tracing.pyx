# distutils: language = c++
from cython.operator import dereference
from libcpp.memory cimport unique_ptr
from libcpp.vector cimport vector
from libcpp cimport bool
from cython_header cimport *

import numpy as np


# Problem with cython's code generation of std::move, use explicit definition
cdef extern from "<utility>" namespace "std" nogil:
    unique_ptr[Component] move(unique_ptr[Component])
  

# Shape of 1d numpy array with 2 elements
_arr_shape = (2, 0, 0, 0, 0, 0, 0, 0)


cdef make_numpy_from_arr(arr& a):
    cdef double[::1] a_mem_view = <double [:a.size()]>a.data()
    
    return np.asarray(a_mem_view)

cdef arr make_arr_from_numpy(double[:] n):
    cdef arr a
    
    assert tuple(n.shape) == _arr_shape, "Expected a 1d blah numpy array with 2 elements"
        
    a[0], a[1] = n[0], n[1]
    
    return a
    
cdef new_arr(double[:] n, arr& a):
    assert tuple(n.shape) == _arr_shape, "blhahhh"
    
    a[0], a[1] = n[0], n[1]

def PyTrace(list components, list rays, int n, bool fill_up=True):
    cdef vector[Component*] vec_comp
        
    for c in components:
        if isinstance(c, PyMirror_Plane):
            vec_comp.push_back( (<PyMirror_Plane>c).c_component_ptr )
            
        elif isinstance(c, PyRefract_Plane):
            vec_comp.push_back( (<PyRefract_Plane>c).c_component_ptr )
            
        elif isinstance(c, PyMirror_Sph):
            vec_comp.push_back( (<PyMirror_Sph>c).c_component_ptr )
            
        elif isinstance(c, PyRefract_Sph):
            vec_comp.push_back( (<PyRefract_Sph>c).c_component_ptr )
            
        elif isinstance(c, PyCC_Wrap):  # Complex derived from PyCC_Wrap
            vec_comp.push_back( ( <PyComplex_Component>( c.PyCC )).c_component_ptr )
            
        else:
            pass  # Need to throw error that it's an unknown component
            
        
    cdef vector[Ray*] vec_rays
    
    for r in rays:
        vec_rays.push_back( (<PyRay>r).c_data )
        
    trace(vec_comp, vec_rays, n, fill_up)


cdef class PyRay:
    cdef Ray* c_data
    
    def __cinit__(self, double[:] init not None, double[:] v not None):
        assert tuple(init.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(v.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
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
        assert tuple(v.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_data).v = make_arr_from_numpy(v)
        
    def plot(self):
        return self.pos

    
cdef class _PyComponent:
    cdef Component* c_component_ptr
    cdef public bool OWNDATA
    
    def __cinit__(self):
        self.OWNDATA = True
        
    def __dealloc__(self):
        if self.OWNDATA:
            del self.c_component_ptr


# Planar components

cdef class _PyPlane(_PyComponent):
    cdef Plane* c_plane_ptr
        
    @property
    def start(self):
        return make_numpy_from_arr(dereference(self.c_plane_ptr).start)
    @start.setter
    def start(self, double[:] start):
        assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_plane_ptr).start = make_arr_from_numpy(start)
        
    @property
    def end(self):
        return make_numpy_from_arr(dereference(self.c_plane_ptr).end)
    @end.setter
    def end(self, double[:] end):
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_plane_ptr).end = make_arr_from_numpy(end)
        
    def plot(self):
        points = np.empty((2, 2), dtype=np.double)
        
        points[0] = self.start
        points[1] = self.end
        
        return points


cdef class PyMirror_Plane(_PyPlane):
    cdef Mirror_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end):
        #assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        cdef arr s
        
        new_arr(start, s)
        
        
        self.c_data = new Mirror_Plane(make_arr_from_numpy(start), 
                                       make_arr_from_numpy(end))
        
        self.c_plane_ptr = <Plane*>self.c_data
        self.c_component_ptr = <Component*>self.c_data
        
        
    # def __dealloc__(self):
    #     if self.OWNDATA:
    #         del self.c_data


cdef class PyRefract_Plane(_PyPlane):
    cdef Refract_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end, double n1=1.0, 
                  double n2=1.0):
        
        assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Refract_Plane(make_arr_from_numpy(start), 
                                        make_arr_from_numpy(end), n1, n2)
        
        self.c_plane_ptr = <Plane*>self.c_data
        self.c_component_ptr = <Component*>self.c_data
        
    # def __dealloc__(self):
    #     if self.OWNDATA:
    #         del self.c_data
    
    @property
    def n1(self):
        return dereference(self.c_data).n1
    @n1.setter
    def n1(self, double n1):
        dereference(self.c_data).n1 = n1
    
    @property
    def n2(self):
        return dereference(self.c_data).n2
    @n2.setter
    def n2(self, double n2):
        dereference(self.c_data).n2 = n2
        

# Spherical components

cdef class _PySpherical(_PyComponent):
    cdef Spherical* c_sph_ptr
    
    @property
    def centre(self):
        return make_numpy_from_arr(dereference(self.c_sph_ptr).centre)
    @centre.setter
    def centre(self, double[:] centre):
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_sph_ptr).centre = make_arr_from_numpy(centre)
        
    @property
    def R(self):
        return dereference(self.c_sph_ptr).R
    @R.setter
    def R(self, double R):
        dereference(self.c_sph_ptr).R = R
        
    @property
    def start(self):
        return dereference(self.c_sph_ptr).start
    @start.setter
    def start(self, double start):
        dereference(self.c_sph_ptr).start = start
        
    @property
    def end(self):
        return dereference(self.c_sph_ptr).end
    @end.setter
    def end(self, double end):
        dereference(self.c_sph_ptr).end = end
        
    def plot(self, n_points=100):
        points = np.empty((n_points, 2), dtype=np.double)
        
        t = np.linspace(self.start, self.end, n_points)
        
        points[:, 0] = self.centre[0] + self.R*np.cos(t)
        points[:, 1] = self.centre[1] + self.R*np.cos(t)
        
        return points


cdef class PyMirror_Sph(_PySpherical):
    cdef Mirror_Sph* c_data
    
    def __cinit__(self, double[:] centre, double R, double start, double end):
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Mirror_Sph(make_arr_from_numpy(centre), R, start, 
                                     end)
        
        self.c_sph_ptr = <Spherical*>self.c_data
        self.c_component_ptr = <Component*>self.c_data
        
    # def __dealloc__(self):
    #     if self.OWNDATA:
    #         del self.c_data
        
    
cdef class PyRefract_Sph(_PySpherical):
    cdef Refract_Sph* c_data
    
    def __cinit__(self, double[:] centre, double R, double start, double end,
                  double n1=1.0, double n2=1.0):
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Refract_Sph(make_arr_from_numpy(centre), R, start, 
                                     end, n1, n2)
        
        self.c_sph_ptr = <Spherical*>self.c_data
        self.c_component_ptr = <Component*>self.c_data
        
    # def __dealloc__(self):
    #     if self.OWNDATA:
    #         del self.c_data
        
    @property
    def n1(self):
        return dereference(self.c_data).n1
    @n1.setter
    def n1(self, double n1):
        dereference(self.c_data).n1 = n1
    
    @property
    def n2(self):
        return dereference(self.c_data).n2
    @n2.setter
    def n2(self, double n2):
        dereference(self.c_data).n2 = n2
    

# Complex component

cdef class PyComplex_Component(_PyComponent):
    cdef Complex_Component* c_data
    
    def __cinit__(self, list comps):
        self.c_data = new Complex_Component()
        self.c_component_ptr = <Component*>self.c_data
        
        
        cdef Component* comp_ptr
        cdef unique_ptr[Component] comp_unique_ptr
        
        
        for c in comps:
            if isinstance(c, PyMirror_Plane):
                comp_ptr = ( <PyMirror_Plane>c ).c_component_ptr
                
            elif isinstance(c, PyRefract_Plane):
                comp_ptr = ( <PyRefract_Plane>c ).c_component_ptr
            
            elif isinstance(c, PyMirror_Sph):
                comp_ptr = ( <PyMirror_Sph>c ).c_component_ptr
                
            elif isinstance(c, PyRefract_Sph):
                comp_ptr = ( <PyRefract_Sph>c ).c_component_ptr
                
            elif isinstance(c, PyCC_Wrap):
                comp_ptr = ( <PyComplex_Component>( c.PyCC )).c_component_ptr
                
            
            comp_unique_ptr = unique_ptr[Component](comp_ptr)
            
            dereference(self.c_data).comps.push_back(move(comp_unique_ptr))
                        
            # Tell these instances they no longer own the data
            c.OWNDATA = False
        
        
class PyCC_Wrap:
    
    def __init__(self, ls):
        self._components = ls
        
        self.PyCC = PyComplex_Component(self._components)
        
    def __getitem__(self, key):
        return self._components[key]
    
    def plot(self, flatten=True, *args, **kwargs):
        points = (c.plot(*args, **kwargs) for c in self._components)
        
        if flatten:
            sol = []
            
            for p in points:
                
                if type(p) is list:
                    sol.append(*p)
                else:
                    print("Blah")
                    
            return sol
        
        return list(points)


















