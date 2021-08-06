# distutils: language = c++
from cython.operator import dereference
from libcpp.memory cimport shared_ptr
from libcpp.vector cimport vector
from libcpp cimport bool
from cython_header cimport *

import numpy as np
cimport numpy as np


# Problem with cython's code generation of std::move, use explicit definition
cdef extern from "<utility>" namespace "std" nogil:
    shared_ptr[Component] move(shared_ptr[Component])
  

# Shape of 1d numpy array with 2 elements
_arr_shape = (2, 0, 0, 0, 0, 0, 0, 0)


cdef arr make_arr_from_numpy(double[:] n):
    """
    Creates an instance of the C++ arr from the numpy array n.
    
    Parameters
    ----------
    n : numpy.ndarray
        A numpy array with shape (2,).
        
    Returns
    -------
    a : arr
        The arr created from n.
    
    """
    
    cdef arr a
        
    a[0], a[1] = n[0], n[1]
    
    return a
    

def PyTrace(list components, list rays, int n, bool fill_up=True):
    """
    Traces the rays through the component list for n iterations.

    Parameters
    ----------
    components : list
        The components rays will be traced through.
    rays : list
        The rays to be traced.
    n : int
        The number of iterations (i.e. interations) to be performed.
    fill_up : bool, optional
        If is detected a ray will not interact with any more components before 
        n iterations are reached, PyTrace will fill the ray's position up with 
        the final position so it contains n points. The default is True.

    Raises
    ------
    TypeError
        Raised if an element in components is not recognised as a component.

    Returns
    -------
    None.

    """
    
    cdef vector[Component*] vec_comp
        
    for c in components:
        if isinstance(c, PyMirror_Plane):
            vec_comp.push_back( (<PyMirror_Plane>c).c_component_ptr.get() )
            
        elif isinstance(c, PyRefract_Plane):
            vec_comp.push_back( (<PyRefract_Plane>c).c_component_ptr.get() )
            
        elif isinstance(c, PyMirror_Sph):
            vec_comp.push_back( (<PyMirror_Sph>c).c_component_ptr.get() )
            
        elif isinstance(c, PyRefract_Sph):
            vec_comp.push_back( (<PyRefract_Sph>c).c_component_ptr.get() )
            
        elif isinstance(c, PyCC_Wrap):  # Complex derived from PyCC_Wrap
            vec_comp.push_back( ( <PyComplex_Component>( c.PyCC )).c_component_ptr.get() )
            
        else:
            raise TypeError(f"Type '{type(c)}' is not a recognised type for a component")
            
        
    cdef vector[Ray*] vec_rays
    
    for r in rays:
        vec_rays.push_back( (<PyRay>r).c_data )
        
    trace(vec_comp, vec_rays, n, fill_up)


cdef class PyRay:
    """
    A class to describe a ray.
    
    ...
    
    Attributes
    ----------
    pos : numpy.ndarray
        Returns a numpy array of the positions of the ray.
    v : numpy.ndarray
        The current 2d direction of the ray.
        
    Methods
    -------
    
    plot()
        Returns a numpy array with shape (N, 2) of the positions of the ray.
        Intended for plotting.
    
    """
    
    cdef Ray* c_data
    
    # Memory views & numpy views onto them used for properties that return numpy views
    cdef double[::1] v_mem_view
    cdef np.ndarray  v_np
    
    def __cinit__(self, double[:] init not None, double[:] v not None):
        """
        Creates an instance of PyRay

        Parameters
        ----------
        init : numpy.ndarray
            Initial 2d position of the ray. Should be a numpy array with shape
            (2,).
        v : numpy.ndarray
            Initial 2d direction of the ray. Should be a normalised numpy array
            with shape (2,).

        Returns
        -------
        None.

        """
        
        assert tuple(init.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(v.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Ray(make_arr_from_numpy(init), 
                              make_arr_from_numpy(v))
        
    def __dealloc__(self):
        """
        Deallocates the memory held by PyRay

        Returns
        -------
        None.

        """
        
        del self.c_data
        
    @property
    def pos(self):
        """
        Returns the positions of each interaction of the ray.

        Returns
        -------
        ans : numpy.ndarray
            A numpy array with shape (N, 2).

        """
        
        n = dereference(self.c_data).pos.size()
        
        ans = np.empty((n, 2), dtype=np.double)
        
        for i in range(n):
            ans[i, 0] = dereference(self.c_data).pos[i][0]
            ans[i, 1] = dereference(self.c_data).pos[i][1]
        
        return ans
    
    @property
    def v(self):
        """
        Gets a view of the current 2d direction of the ray. It returns a numpy
        view so can be used to modify PyRay.v elementwise.

        Returns
        -------
        v_np : numpy.ndarray
            A numpy view with shape (2,).

        """
        
        self.v_mem_view = <double[:2]>( dereference(self.c_data).v.data() )
        
        v_np = np.asarray(self.v_mem_view)
        
        return v_np
    @v.setter
    def v(self, double[:] v not None):
        assert tuple(v.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_data).v = make_arr_from_numpy(v)
        
    def plot(self):
        """
        Produces a numpy arrays that can be used to plot the path of the ray.

        Returns
        -------
        numpy.ndarray
            A numpy array with shape (N, 2).

        """
        
        return self.pos

    
cdef class _PyComponent:
    """
    A class to mirror the C++ Component class. Not intended to be initialized.
    
    ...
    
    Attributes
    ----------
    
    None.
    
    Methods
    -------
    
    None.
    
    """
    
    cdef shared_ptr[Component] c_component_ptr


# Planar components

cdef class _PyPlane(_PyComponent):
    """
    A class to mirror the C++ Plane class. Not intended to be initialised.
    
    ...
    
    Attributes
    ----------
    
    start : numpy.ndarray
        The start point of the plane.
    end : numpy.ndarray
        The end point of the plane.
    
    Methods
    -------
    
    plot() : numpy.ndarray
        Returns a numpy array for plotting the plane with shape (2, 2).
    
    """
    
    cdef Plane* c_plane_ptr
    
    # Memory views & numpy views onto them used for properties that return numpy views
    cdef double[::1] start_mem_view
    cdef np.ndarray  start_np
    cdef double[::1] end_mem_view
    cdef np.ndarray  end_np
        
    @property
    def start(self):
        """
        The start point of the plane. Can be set as a copy of the passed numpy
        array.

        Returns
        -------
        start_np : numpy.ndarray
            A 2d numpy view of the start point.

        """
        
        self.start_mem_view = <double[:2]>( dereference(self.c_plane_ptr).start.data() )
        
        start_np = np.asarray(self.start_mem_view)
        
        return start_np
    @start.setter
    def start(self, double[:] start):
        assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_plane_ptr).start = make_arr_from_numpy(start)
        
    @property
    def end(self):
        """
        The end point of the plane. Can be set as a copy of the passed numpy
        array.

        Returns
        -------
        end_np : numpy.ndarray
            A numpy view with shape (2,) of the end point.

        """
        
        self.end_mem_view = <double[:2]>( dereference(self.c_plane_ptr).end.data() )
        
        end_np = np.asarray(self.end_mem_view)
        
        return end_np
    @end.setter
    def end(self, double[:] end):
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_plane_ptr).end = make_arr_from_numpy(end)
        
    def plot(self):
        """
        Returns a numpy array that can be used to plot the plane.

        Returns
        -------
        numpy.ndarray
            A numpy array with shape (2, 2). The first index spcifies the start
            or end points.

        """
        
        points = np.empty((2, 2), dtype=np.double)
        
        points[0] = self.start
        points[1] = self.end
        
        return points



cdef class PyMirror_Plane(_PyPlane):
    """
    A class to represent a plane mirror. Mirrors C++ class Mirror_Plane.
    """
    
    
    cdef Mirror_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end):
        """
        Creates an instance of PyMirror_Plane.

        Parameters
        ----------
        start : numpy.ndarray
            The start point of the plane. It should be a numpy.ndarray with 
            shape (2,).
        end : numpy.ndarray
            The end point of the plane. It should be a numpy.ndarray with 
            shape (2,).

        Returns
        -------
        None.

        """
        
        assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"       
        
        self.c_data = new Mirror_Plane(make_arr_from_numpy(start), 
                                       make_arr_from_numpy(end))
        
        self.c_plane_ptr = <Plane*>self.c_data
        self.c_component_ptr = shared_ptr[Component]( <Component*>self.c_data )
        


cdef class PyRefract_Plane(_PyPlane):
    """
    A class to represent a planar boundary at which refraction occurs. Mirrors
    C++ class Refract_Plane.
    """
    
    cdef Refract_Plane* c_data
    
    def __cinit__(self, double[:] start, double[:] end, double n1=1.0, 
                  double n2=1.0):
        """
        Creates an instance of PyRefract_Plane.

        Parameters
        ----------
        start : numpy.ndarray
            The start point of the mirror plane. It should be a numpy.ndarray
            with shape (2,).
        end : numpy.ndarray
            The end point of the mirror plane. It should be a numpy.ndarray
            with shape (2,).
        double n1 : TYPE, optional
            The refractive index on the left of the planar boundary. Left is 
            defined as left of the vector start->end. The default is 1.0.
        double n2 : TYPE, optional
            The refractive index on the right of the planar boundary. Right is 
            defined as right of the vector start->end. The default is 1.0.

        Returns
        -------
        None.

        """
        
        assert tuple(start.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        assert tuple(end.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Refract_Plane(make_arr_from_numpy(start), 
                                        make_arr_from_numpy(end), n1, n2)
        
        self.c_plane_ptr = <Plane*>self.c_data
        self.c_component_ptr = shared_ptr[Component]( <Component*>self.c_data )
    
    @property
    def n1(self):
        """
        The refractive index on the left of the planar boundary. Left is 
        defined as left of the vector start->end.

        Returns
        -------
        double
            The refractive index n1.

        """
        
        return dereference(self.c_data).n1
    @n1.setter
    def n1(self, double n1):
        dereference(self.c_data).n1 = n1
    
    @property
    def n2(self):
        """
        The refractive index on the right of the planar boundary. Right is 
        defined as right of the vector start->end.

        Returns
        -------
        double
            The refractive index n2.

        """
        
        return dereference(self.c_data).n2
    @n2.setter
    def n2(self, double n2):
        dereference(self.c_data).n2 = n2
        


# Spherical components

cdef class _PySpherical(_PyComponent):
    """
    Class to describe a circular arc, mirrors C++ class Shperical. Not intended
    to be user initialised.
    """
    
    cdef Spherical* c_sph_ptr
    
    # Memory views & numpy views onto them used for properties that return numpy views
    cdef double[::1] centre_mem_view
    cdef np.ndarray  centre_np
    
    @property
    def centre(self):
        """
        The centre of the ciruclar arc.

        Returns
        -------
        centre_np : numpy.ndarray
            A numpy view with shape (2,) of the centre.

        """
        
        self.centre_mem_view = <double[:2]>( dereference(self.c_sph_ptr).centre.data() )
        
        centre_np = np.asarray(self.centre_mem_view)
        
        return centre_np
    @centre.setter
    def centre(self, double[:] centre):
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        dereference(self.c_sph_ptr).centre = make_arr_from_numpy(centre)
        
    @property
    def R(self):
        """
        The radius of the circular arc.

        Returns
        -------
        double
            The radius of the circular arc.

        """
        
        return dereference(self.c_sph_ptr).R
    @R.setter
    def R(self, double R):       
        dereference(self.c_sph_ptr).R = R
        
    @property
    def start(self):
        """
        The start angle of the arc, in radians. It is measured anti-clockwise 
        from the x axis.

        Returns
        -------
        double
            The start angle of the arc.

        """
        
        return dereference(self.c_sph_ptr).start
    @start.setter
    def start(self, double start):
        dereference(self.c_sph_ptr).start = start
        
    @property
    def end(self):
        """
        The end angle of the arc, in radians. It is measured anti-clockwise 
        from the x axis.

        Returns
        -------
        double
            The end angle of the arc.

        """
        
        return dereference(self.c_sph_ptr).end
    @end.setter
    def end(self, double end):
        dereference(self.c_sph_ptr).end = end
        
    def plot(self, n_points=100):
        """
        Returns a numpy array that can be used to plot the arc.

        Parameters
        ----------
        n_points : int, optional
            The number of points returned. The default is 100.

        Returns
        -------
        points : numpy.ndarray
            A numpy array with shape (n_points, 2).

        """
        
        points = np.empty((n_points, 2), dtype=np.double)
        
        t = np.linspace(self.start, self.end, n_points)
        
        points[:, 0] = self.centre[0] + self.R*np.cos(t)
        points[:, 1] = self.centre[1] + self.R*np.sin(t)
        
        return points



cdef class PyMirror_Sph(_PySpherical):
    """A class to represent a circular mirror. Mirrors C++ class Mirror_Sph"""
    
    cdef Mirror_Sph* c_data
    
    def __cinit__(self, double[:] centre, double R, double start, double end):
        """
        Creates an instance of PyMirror_Sph.

        Parameters
        ----------
        centre : numpy.ndarray
            The centre of the circular arc. It should be a numpy.ndarray with
            shape (2,).
        R : double
            The radius of the arc.
        start : double
            The start angle of the arc, in radians. It is measured 
            anti-clockwise from the x axis.
        end : double
            The end angle of the arc, in radians. It is measured anti-clockwise 
            from the x axis.

        Returns
        -------
        None.

        """
        
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Mirror_Sph(make_arr_from_numpy(centre), R, start, 
                                     end)
        
        self.c_sph_ptr = <Spherical*>self.c_data
        self.c_component_ptr = shared_ptr[Component]( <Component*>self.c_data )
        
        
    
cdef class PyRefract_Sph(_PySpherical):
    """
    A class to describe a circular arc at which refraction occurs. Mirrors
    C++ class Refract_Sph.
    """
    
    cdef Refract_Sph* c_data
    
    def __cinit__(self, double[:] centre, double R, double start, double end,
                  double n1=1.0, double n2=1.0):
        """
        Creates an instance of PyRefract_Sph.

        Parameters
        ----------
        centre : numpy.ndarray
            The centre of the circular arc. It should be a numpy.ndarray with
            shape (2,).
        R : double
            The radius of the arc.
        start : double
            The start angle of the arc, in radians. It is measured 
            anti-clockwise from the x axis.
        end : double
            The end angle of the arc, in radians. It is measured anti-clockwise 
            from the x axis.
        n1 : double, optional
            The refractive index for r < R. The default is 1.0.
        n2 : double, optional
            The refractive index for r > R. The default is 1.0.

        Returns
        -------
        None.

        """
        
        assert tuple(centre.shape) == _arr_shape, "Expected a 1d numpy array with 2 elements"
        
        self.c_data = new Refract_Sph(make_arr_from_numpy(centre), R, start, 
                                     end, n1, n2)
        
        self.c_sph_ptr = <Spherical*>self.c_data
        self.c_component_ptr = shared_ptr[Component]( <Component*>self.c_data )
                
    @property
    def n1(self):
        """
        The refractive index "inside" the arc where r < R.

        Returns
        -------
        double
            The refractive index n1.

        """
        
        return dereference(self.c_data).n1
    @n1.setter
    def n1(self, double n1):
        dereference(self.c_data).n1 = n1
    
    @property
    def n2(self):
        """
        The refractive index "outside" the arc where r > R.

        Returns
        -------
        double
            The refractive index n2.

        """
        
        return dereference(self.c_data).n2
    @n2.setter
    def n2(self, double n2):
        dereference(self.c_data).n2 = n2
    


# Complex component

cdef class PyComplex_Component(_PyComponent):
    """
    A class to represent a complex component. Mirrors C++ class 
    Complex_Component.
    """
    
    cdef Complex_Component* c_data
    
    def __cinit__(self, list comps):
        """
        Creates an instance of PyComplex_Component.

        Parameters
        ----------
        comps : list 
            The list of components which describe the complex component. They
            should be one of the following: PyMirror_Plan, PyMirror_Sph,
            PyRefract_Plane, PyRefract_Sph or inherit from PyCC_Wrap.

        Returns
        -------
        None.

        """
        
        self.c_data = new Complex_Component()
        self.c_component_ptr = shared_ptr[Component]( <Component*>self.c_data )
        
        cdef Component* comp_ptr
        cdef shared_ptr[Component] comp_shared_ptr
                
        for c in comps:
            if isinstance(c, PyMirror_Plane):
                comp_shared_ptr = ( <PyMirror_Plane>c ).c_component_ptr
                
            elif isinstance(c, PyRefract_Plane):
                comp_shared_ptr = ( <PyRefract_Plane>c ).c_component_ptr
                
            elif isinstance(c, PyMirror_Sph):
                comp_shared_ptr = ( <PyMirror_Sph>c ).c_component_ptr
                
            elif isinstance(c, PyRefract_Sph):
                comp_shared_ptr = ( <PyRefract_Sph>c ).c_component_ptr
                
                # isinstance() covers PyCC_Wrap and anything that inherits from
                # it
            elif isinstance(c, PyCC_Wrap):
                comp_shared_ptr = ( <PyComplex_Component?>( c.PyCC )).c_component_ptr
            
            dereference(self.c_data).comps.push_back(comp_shared_ptr)   
        
        
class PyCC_Wrap:
    """
    A class for creating complex components. It is not intended to be 
    initialised directly but inherited from to easily create complex 
    component classes using only Python.
    
    To create a complex component class in Python using PyCC_Wrap, call
    PyCC_Wrap's initialiser from the sub-classes's initialiser with the list
    of components, i.e. call:
    
    super().__init__(list_of_componentss)
    
    """
    
    def __init__(self, ls):
        """
        Creates an instance of PyCC_Wrap.

        Parameters
        ----------
        ls : list
            The list of components which describe the complex component. They
            should be one of the following: PyMirror_Plan, PyMirror_Sph,
            PyRefract_Plane, PyRefract_Sph or inherit from PyCC_Wrap.

        Returns
        -------
        None.

        """
        
        self._components = ls
        
        # Originally created PyCC_Wrap so could easily store components and the
        # not having a valid python object when __cinit__() is called, not 
        # sure this is necessary anymore
        self.PyCC = PyComplex_Component(self._components)
        
    def __getitem__(self, key):
        """
        Gets a component by its index.

        Parameters
        ----------
        key : int
            The index of the component.

        Returns
        -------
        Any
            The component.

        """
        
        return self._components[key]
    
    def plot(self, flatten=True, *args, **kwargs):
        """
        Creates an object that can be used to plot the complex component.

        Parameters
        ----------
        flatten : TYPE, optional
            Flattens the resulting object to return a numpy array with shape 
            (total_points, 2), where total_points is the total number of points
            across all sub-components. If False, plot() will return a list of 
            numpy arrays of points corresponding to each sub-component. The
            default is True.
        *args : Any
            Additional arguments to pass to sub-component plotting methods.
        **kwargs : Any
            Additional keyword arguments to pass to sub-component plotting 
            methods.

        Returns
        -------
        list or numpy.ndarray
            If flatten is True, a numpy array with shape (total_points, 2), 
            otherwise a list of numpy arrays with shape (N, 2).

        """
        
        points = (c.plot(*args, **kwargs) for c in self._components)
        
        if flatten:
            sol = []
            
            for p in points:
                
                if type(p) is list:
                    sol.append(*p)
                else:
                    sol.append(p)
                    
            return np.vstack(sol)
        
        return list(points)

