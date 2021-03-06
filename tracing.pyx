# geometrical-ray-tracing: Program to perform geometrical ray tracing
# Copyright (C) 2022  Tom Spencer (tspencerprog@gmail.com)

# This file is part of geometrical-ray-tracing

# geometrical-ray-tracing is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# distutils: language = c++
from cpython.ref cimport Py_INCREF
from cython.operator import dereference
from libcpp.memory cimport shared_ptr
from libcpp.vector cimport vector
from libcpp cimport bool
from cython_header cimport *

import numpy as np
cimport numpy as np

# Initialise numpy's C API
np.import_array()


# Problem with cython's code generation of std::move, use explicit definition
cdef extern from "<utility>" namespace "std" nogil:
    shared_ptr[Component] move(shared_ptr[Component])
  

# Shape of 1d numpy array with 2 elements
_arr_shape = (2, 0, 0, 0, 0, 0, 0, 0)

def wrong_np_shape_except(var_name, bad_arr):
    """
    Returns an exception to be used when an array doesn't have the same shape
    as _arr_shape = (2, 0, 0, 0, 0, 0, 0, 0)

    Parameters
    ----------

    var_name : str
        The name of the variable thatdidn't have the correct shape.
    bad_arr : numpy.ndarray
        The bad array itself.

    Returns
    -------
    TypeError
        A TypeError exception indicating incorrect shape.
    """

    return TypeError(f"expected {var_name} to have shape (2,) but got array with shape {bad_arr.shape}")


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


# make_np_view_from_arr function

cdef make_np_view_from_arr(arr& a, object owning_obj):
    """
    Exposes the arr as a numpy view.

    Parameters
    ----------
    a : arr&
        arr object that will form the base of the numpy view.
    owning_obj : object
        Python object that own's a's memory.

    Returns
    -------
    np_view : np.ndarray
        A numpy view onto the arr's data.
    
    """

    # Uses PyArray_SimpleNewFromData() from numpy C API to create numpy view
    # See https://numpy.org/doc/stable/reference/c-api/array.html

    cdef int nd = 1  # number of dimensions in arr
    cdef int typenum = np.NPY_FLOAT64
    cdef np.npy_intp[1] dims = [2]  # Number of elements in each dimension

    # PyArray_SimpleNewFromData() creates a numpy array from the given pointer
    cdef np.ndarray np_view = np.PyArray_SimpleNewFromData(nd, &(dims[0]), typenum, a.data())

    # PyArray_SetBaseObject() steals a reference so we need to pre-increment
    Py_INCREF(owning_obj)

    # Ensures Python's reference counting system knows it needs to keep
    # owning_obj around while the numpy view is around
    cdef int set_base_err = np.PyArray_SetBaseObject(np_view, owning_obj)

    if set_base_err==-1:
        raise RuntimeError("Failed to set base of numpy view")
    
    return np_view

# PyTrace function

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
        The number of iterations (i.e. interactions) to be performed.
        Interactions count as interactions with leaf level components in only. 
        E.g. if a ray interacts with two sub-components of a complex
        component, this accounts for two of the n interactions.
    fill_up : bool, optional
        If is detected a ray will not interact with any more components before 
        n iterations are reached, PyTrace will fill the ray's position up with 
        the final position so it has added n points. The default is True.

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

        elif isinstance(c, PyScreen_Plane):
            vec_comp.push_back( (<PyScreen_Plane>c).c_component_ptr.get() )
            
        elif isinstance(c, PyMirror_Sph):
            vec_comp.push_back( (<PyMirror_Sph>c).c_component_ptr.get() )
            
        elif isinstance(c, PyRefract_Sph):
            vec_comp.push_back( (<PyRefract_Sph>c).c_component_ptr.get() )
            
        elif isinstance(c, PyCC_Wrap):  # Complex derived from PyCC_Wrap
            vec_comp.push_back( ( <PyComplex_Component>( c.PyCC )).c_component_ptr.get() )
            
        else:
            raise TypeError(f"type {type(c)} is not a recognised type for a component")
            
        
    cdef vector[Ray*] vec_rays
    
    for r in rays:
        vec_rays.push_back( (<PyRay>r).c_data )
        
    trace(vec_comp, vec_rays, n, fill_up)

# class PyRay

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
        
        if tuple(init.shape) != _arr_shape:
            raise wrong_np_shape_except("init", init)

        if tuple(v.shape) != _arr_shape:
            raise wrong_np_shape_except("v", v)

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
        
        return make_np_view_from_arr(self.c_data.v, self)
    @v.setter
    def v(self, double[:] v not None):
        if tuple(v.shape) != _arr_shape:
            raise wrong_np_shape_except("v", v)
        
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

    def reset(self, double[:] new_v not None, double[:] new_p = None):
        """
        Resets the PyRay instance to the start position and is direction to
        that of new_v. new_v is assumed to be normalised.

        Parameters
        ----------
        new_v : numpy.ndarray
            The new 2d direction of the ray. Should be a normalised numpy array
            with shape (2,).
        new_p : numpy.ndarray, optional
            Initial 2d position of the ray. If not specified, the original 
            initial position will be used. Should be a numpy array with shape
            (2,).

        Returns
        -------
        None. 
        
        """

        if tuple(new_v.shape) != _arr_shape:
            raise wrong_np_shape_except("new_v", new_v)

        cdef arr n_v = make_arr_from_numpy(new_v)
        cdef arr n_p

        if new_p is None:
            dereference(self.c_data).reset(n_v)
        else:
            if tuple(new_p.shape) != _arr_shape:
                raise wrong_np_shape_except("new_p", new_p)

            n_p = make_arr_from_numpy(new_p)

            dereference(self.c_data).reset(n_v, n_p)


# class _PyComponent
    
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

    cdef _load_component(self, Component* cmp_ptr):
        """
        Sets the C++ component pointer.

        Parameters
        ----------
        cmp_ptr : Component*

        Returns
        -------
        None.

        """

        self.c_component_ptr = shared_ptr[Component](cmp_ptr)


# Planar components
# class _PyPlane

cdef class _PyPlane(_PyComponent):
    """
    A class to mirror the C++ Plane class which represents a 2d plane. Not 
    intended to be initialised.
    
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
        Returns a numpy array for plotting the plane with shape (2, 2), with
        the first indiex specifying the point.
    
    """
    
    cdef Plane* c_plane_ptr


    cdef _load_Plane(self, Plane* pln_ptr):
        """
        Loads plane properties, namely start & end. Also sets the plane and
        component pointers.

        Parameters
        ----------
        pl_ptr : Plane*
            Pointer to the C++ Plane.

        Returns
        -------
        None.
        
        """

        self.c_plane_ptr = pln_ptr
        self._load_component(<Component*>pln_ptr)

    @property
    def start(self):
        """
        The start point of the plane. Can be set as a copy of the passed numpy
        array.

        Returns
        -------
        start_np : numpy.ndarray
            A read-only numpy view of the start point.

        """

        cdef np.ndarray start_np = make_np_view_from_arr(self.c_plane_ptr.get_start(), self)

        # Make array read-only as Plane.start can't be set trivially
        start_np.flags.writeable = False

        return start_np
    @start.setter
    def start(self, double[:] start not None):
        if tuple(start.shape) != _arr_shape:
            raise wrong_np_shape_except("start", start)
        
        self.c_plane_ptr.set_start(make_arr_from_numpy(start))

    @property
    def end(self):
        """
        The end point of the plane. Can be set as a copy of the passed numpy
        array.

        Returns
        -------
        end_np : numpy.ndarray
            A read only numpy view with shape (2,) of the end point.

        """
        
        cdef np.ndarray end_np = make_np_view_from_arr(self.c_plane_ptr.get_end(), self)

        # Make array read-only as Plane.start can't be set trivially
        end_np.flags.writeable = False

        return end_np
    @end.setter
    def end(self, double[:] end not None):
        if tuple(end.shape) != _arr_shape:
            raise wrong_np_shape_except("end", end)

        self.c_plane_ptr.set_end(make_arr_from_numpy(end))
        
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

# class PyMirror_Plane

cdef class PyMirror_Plane(_PyPlane):
    """
    A class to represent a plane mirror. Mirrors C++ class Mirror_Plane.
    """
    
    cdef Mirror_Plane* c_data
    
    def __cinit__(self, double[:] start not None, double[:] end not None):
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

        if tuple(start.shape) != _arr_shape:
            raise wrong_np_shape_except("start", start)

        if tuple(end.shape) != _arr_shape:
            raise wrong_np_shape_except("end", end)
        
        self.c_data = new Mirror_Plane(make_arr_from_numpy(start), 
                                       make_arr_from_numpy(end))
        
        self._load_Plane(<Plane*>self.c_data)

        
# class Pyrefract_Plane

cdef class PyRefract_Plane(_PyPlane):
    """
    A class to represent a planar boundary at which refraction occurs. Mirrors
    C++ class Refract_Plane.
    """
    
    cdef Refract_Plane* c_data
    
    def __cinit__(self, double[:] start not None, double[:] end not None, double n1=1.0, 
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
        n1 : double, optional
            The refractive index on the left of the planar boundary. Left is 
            defined as left of the vector start->end. The default is 1.0.
        n2 : double, optional
            The refractive index on the right of the planar boundary. Right is 
            defined as right of the vector start->end. The default is 1.0.

        Returns
        -------
        None.

        """
        
        # Verify start and end arrays have correct shape
        if tuple(start.shape) != _arr_shape:
            raise wrong_np_shape_except("start", start)

        if tuple(end.shape) != _arr_shape:
            raise wrong_np_shape_except("end", end)
        
        self.c_data = new Refract_Plane(make_arr_from_numpy(start), 
                                        make_arr_from_numpy(end), n1, n2)
        
        self._load_Plane(<Plane*>self.c_data)
    
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
        if n1 <= 0.0:
            raise ValueError("n1 cannot be less than or equal to zero")

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
        if n2 <= 0.0:
            raise ValueError("n2 cannot be less than or equal to zero")

        dereference(self.c_data).n2 = n2
        
# class Screen_Plane

cdef class PyScreen_Plane(_PyPlane):
    """A class to represent a planar, absorbing screen"""

    cdef Screen_Plane* c_data
    
    def __cinit__(self, double[:] start not None, double[:] end not None):
        """
        Creates an instance of PyScreen_Plane.

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

        if tuple(start.shape) != _arr_shape:
            raise wrong_np_shape_except("start", start)

        if tuple(end.shape) != _arr_shape:
            raise wrong_np_shape_except("end", end)
        
        self.c_data = new Screen_Plane(make_arr_from_numpy(start), 
                                       make_arr_from_numpy(end))
        
        self._load_Plane(<Plane*>self.c_data)

# Spherical components
# class _PySpherical

cdef class _PySpherical(_PyComponent):
    """
    Class to describe a circular arc, mirrors C++ class Spherical. Not intended
    to be initialised.
    """
    
    cdef Spherical* c_sph_ptr
    

    cdef _load_Sph(self, Spherical* sph_ptr):
        """
        Loads spherical properties, namely centre. Also sets the spherical and
        component pointers.

        Parameters
        ----------
        sph_ptr : Spherical*
            Pointer to the C++ Spherical.

        Returns
        -------
        None.
        
        """

        self.c_sph_ptr = sph_ptr
        self._load_component(<Component*>sph_ptr)
    
    @property
    def centre(self):
        """
        The centre of the ciruclar arc. Can be set as a copy of the passed 
        numpy array.

        Returns
        -------
        centre_np : numpy.ndarray
            A numpy view with shape (2,) of the centre.

        """

        return make_np_view_from_arr(self.c_sph_ptr.centre, self)
    @centre.setter
    def centre(self, double[:] centre not None):
        if tuple(centre.shape) != _arr_shape:
            raise wrong_np_shape_except("centre", centre)

        dereference(self.c_sph_ptr).centre = make_arr_from_numpy(centre)
        
    @property
    def R(self):
        """
        The radius of the circular arc, must be positive.

        Returns
        -------
        double
            The radius of the circular arc.

        """
        
        return dereference(self.c_sph_ptr).R
    @R.setter
    def R(self, double R):
        if R <= 0.0:
            raise ValueError("R cannot be less than or equal to zero")

        dereference(self.c_sph_ptr).R = R
        
    @property
    def start(self):
        """
        The start angle of the arc, in radians. It is measured anti-clockwise 
        from the x axis. Must be less than property end.

        Returns
        -------
        double
            The start angle of the arc.

        """
        
        return dereference(self.c_sph_ptr).get_start()
    @start.setter
    def start(self, double start):
        if start >= self.end:
            raise ValueError("start angle must be less than end angle")

        dereference(self.c_sph_ptr).set_start(start)
        
    @property
    def end(self):
        """
        The end angle of the arc, in radians. It is measured anti-clockwise 
        from the x axis. Must be greater than property start.

        Returns
        -------
        double
            The end angle of the arc.

        """
        
        return dereference(self.c_sph_ptr).get_end()
    @end.setter
    def end(self, double end):
        if end <= self.start:
            raise ValueError("end angle must be greater than start angle")

        dereference(self.c_sph_ptr).set_end(end)

    def update_start_end(self, double new_start, double new_end):
        """
        Updates start and end simultaneously. This is useful as it means you
        don't have to ensure self.start < self.end while setting each property
        individually. new_start must be less than new_end.

        Parameters
        ----------
        new_start : double
            The new start angle measured anticlockwise from the x axis.
        new_end : double
            The new end angle measured anticlockwise from the x axis.

        Raises
        ------
        ValueError
            Raised if new_end <= new_start.

        Returns
        -------
        None.

        """

        if new_end <= new_start:
            raise ValueError("end angle must be greater than start angle")

        dereference(self.c_sph_ptr).set_start(new_start)
        dereference(self.c_sph_ptr).set_end(new_end)
        
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


# class PyMirror_Sph 

cdef class PyMirror_Sph(_PySpherical):
    """A class to represent a circular mirror. Mirrors C++ class Mirror_Sph."""
    
    cdef Mirror_Sph* c_data
    
    def __cinit__(self, double[:] centre not None, double R, double start, double end):
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
            anti-clockwise from the x axis. Must be less than end.
        end : double
            The end angle of the arc, in radians. It is measured anti-clockwise 
            from the x axis. Must be greater than start.

        Returns
        -------
        None.

        """

        if tuple(centre.shape) != _arr_shape:
            raise wrong_np_shape_except("centre", centre)

        if R <= 0.0:
            raise ValueError("R cannot be less than or equal to zero")
                
        self.c_data = new Mirror_Sph(make_arr_from_numpy(centre), R, start, 
                                     end)
        
        self._load_Sph(<Spherical*>self.c_data)


# class PyrefractSph

cdef class PyRefract_Sph(_PySpherical):
    """
    A class to describe a circular arc at which refraction occurs. Mirrors
    C++ class Refract_Sph.
    """
    
    cdef Refract_Sph* c_data
    
    def __cinit__(self, double[:] centre not None, double R, double start, double end,
                  double n_in=1.0, double n_out=1.0):
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
            anti-clockwise from the x axis. Must be less than end.
        end : double
            The end angle of the arc, in radians. It is measured anti-clockwise 
            from the x axis. Must be greater than start.
        n_in : double, optional
            The refractive index for r < R. The default is 1.0.
        n_out : double, optional
            The refractive index for r > R. The default is 1.0.

        Returns
        -------
        None.

        """
        
        if tuple(centre.shape) != _arr_shape:
            raise wrong_np_shape_except("centre", centre)

        if R <= 0.0:
            raise ValueError("R cannot be less than or equal to zero")
        
        self.c_data = new Refract_Sph(make_arr_from_numpy(centre), R, start, 
                                     end, n_out, n_in)
        
        self._load_Sph(<Spherical*>self.c_data)
                
    @property
    def n_in(self):
        """
        The refractive index "inside" the arc where r < R.

        Returns
        -------
        double
            The refractive index n_in.

        """
        
        return dereference(self.c_data).n2
    @n_in.setter
    def n_in(self, double n_in):
        if n_in <= 0.0:
            raise ValueError("n_in cannot be less than or equal to zero")

        dereference(self.c_data).n2 = n_in
    
    @property
    def n_out(self):
        """
        The refractive index "outside" the arc where r > R.

        Returns
        -------
        double
            The refractive index n_out.

        """
        
        return dereference(self.c_data).n1
    @n_out.setter
    def n_out(self, double n_out):
        if n_out <= 0.0:
            raise ValueError("n_out cannot be less than or equal to zero")

        dereference(self.c_data).n1 = n_out
    


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
            should be one of the following: PyMirror_Plane, PyRefract_Plane,
            PyScreen_Plane, PyMirror_Sph, PyRefract_Sph or inherit from 
            PyCC_Wrap.

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

# class PyCCWrap

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
            should be one of the following: PyMirror_Plane, PyRefract_Plane,
            PyScreen_Plane, PyMirror_Sph, PyRefract_Sph or inherit from 
            PyCC_Wrap.

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
    
    def plot(self, *args, **kwargs):
        """
        Creates an object that can be used to plot the complex component.

        Parameters
        ----------
        *args : Any
            Additional arguments to pass to sub-component plotting methods.
        **kwargs : Any
            Additional keyword arguments to pass to sub-component plotting 
            methods.

        Returns
        -------
        list of numpy.ndarray or list of list
            A list of either numpy.ndarray or list. If the complex component
            is itself composed of complex components, plot() will return a 
            nested list. The leaves will be the points to plot.

        """
        
        return [c.plot(*args, **kwargs) for c in self._components]


# Pre defined Complex components

class PyLens(PyCC_Wrap):
    """A class to represent a lens"""

    def __init__(self, lens_centre, R_lens, R1, R2, d, n_in, n_out=1.0) -> None:
        """
        Creates an instance of PyLens.

        Parameters
        ----------
        lens_centre : numpy.ndarray
            A numpy array of shape (2,) that gives the centre of the lens.
        R_lens : double
            The radius of the lens.
        R1 : double
            The radius of curvature of the left side of the lens. If R1 is
            positive this arc of the lens is convex, if it is negative it 
            is concave. R1 must satisfy R1 >= R_lens or R1 <= -R_lens.
        R2 : double
            The radius of curvature of the right side of the lens. If R2 is
            positive this arc of the lens is convex, if it is negative it 
            is concave. R2 must satisfy R2 >= R_lens or R2 <= -R_lens.
        d : double
            The distance between the end of one arc and the nearest end
            of the other. See figure in LaTeX docs.
        n_in : double
            The refractive index of the interior of the lens.
        n_out : double, optional
            The refractive index outside of the lens. The default is 1.0.

        Returns
        -------
        None.

        """

        self._lens_centre = lens_centre
        self._R_lens = R_lens
        self._R1 = R1
        self._R2 = R2
        self._d = d
        self._n_in = n_in
        self._n_out = n_out

        # left arc
        if -R_lens < R1 < R_lens:
            raise ValueError(f"R1 = {R1} is invalid")

        l_p = self._create_arc_param(True, lens_centre, R_lens, R1, R2, d, n_in, n_out)

        self._left_arc = PyRefract_Sph(**l_p)

        # Right arc
        if -R_lens < R2 < R_lens:
            raise ValueError(f"R2 = {R2} is invalid")

        r_p = self._create_arc_param(False, lens_centre, R_lens, R1, R2, d, n_in, n_out)

        self._right_arc = PyRefract_Sph(**r_p)

        c_x, c_y = lens_centre

        # positions of "box"
        top_left = np.array([c_x - d/2, c_y + R_lens])
        top_right = np.array([c_x + d/2, c_y + R_lens])
        bottom_left = np.array([c_x - d/2, c_y - R_lens])
        bottom_right = np.array([c_x + d/2, c_y - R_lens])

        self._top_plane = PyRefract_Plane(top_right, top_left, n_in, n_out)
        self._bottom_plane = PyRefract_Plane(bottom_left, bottom_right, n_in, n_out)

        comps = [
            self._left_arc,
            self._bottom_plane,
            self._right_arc,
            self._top_plane,
        ]

        super().__init__(comps)

    def _comp_arc_centre(self, left, lens_centre, R_lens, R1, R2, d, n_in, n_out):
        """Returns the centre of the arc"""
        ans = lens_centre.copy()

        R = R1 if left else R2
        lft = 1 if left else -1

        ans[0] += lft *( np.sign(R) * np.sqrt(R**2 - R_lens**2) - d/2)

        return ans

    def _comp_arc_angles(self, left, lens_centre, R_lens, R1, R2, d, n_in, n_out):
        """Returns the angles of the arc"""

        R = R1 if left else R2
        lft = 1 if left else -1

        ang = np.arcsin(np.abs(R_lens / R))

        start, end = -ang, ang

        if lft * R >= R_lens:
            start += np.pi
            end += np.pi

        return (start, end)

    def _comp_arc_refr_ind(self, left, lens_centre, R_lens, R1, R2, d, n_in, n_out):
        """Returns refractive indices n_in and n_out"""

        R = R1 if left else R2

        # Convex arc
        if R >= R_lens:
            return (n_in, n_out)

        return (n_out, n_in)

    def _create_arc_param(self, left, lens_centre, R_lens, R1, R2, d, n_in, n_out):
        """Returns a dictionary of params for creating the left arc"""

        param = dict()

        param['centre'] = self._comp_arc_centre(left, lens_centre, R_lens, R1, R2, d, n_in, n_out)

        param['R'] = np.abs(R1 if left else R2)

        param["start"], param['end'] = self._comp_arc_angles(left, lens_centre, R_lens, R1, R2, d, n_in, n_out)

        param['n_in'], param['n_out'] = self._comp_arc_refr_ind(left, lens_centre, R_lens, R1, R2, d, n_in, n_out)

        return param

    def get_current_params(self):
        """Returns a dictionary of the current lens parameters"""
        d = dict()
        
        d['lens_centre'] = self.lens_centre
        d['R_lens'] = self.R_lens
        d['R1'] = self.R1
        d['R2'] = self.R2
        d['d'] = self.d
        d['n_in'] = self.n_in
        d['n_out'] = self.n_out

        return d

    @property
    def lens_centre(self):
        """
        The centre of the lens. Note lens_centre cannot be modified by changing
        the elements of the returned numpy.ndarray. Doing so will corrput te
        PyLens instance.

        Returns
        -------
        numpy.ndarray
            A numpy array with shape (2,) giving the lens centre.

        """

        return self._lens_centre
    @lens_centre.setter
    def lens_centre(self, new_centre):
        """Setter for lens_centre"""
        diff = new_centre - self._lens_centre

        self._lens_centre += diff

        # arcs
        self._left_arc.centre += diff
        self._right_arc.centre += diff

        # planes
        self._top_plane.start = self._top_plane.start + diff
        self._top_plane.end = self._top_plane.end + diff

        self._bottom_plane.start = self._bottom_plane.start + diff
        self._bottom_plane.end = self._bottom_plane.end + diff

    @property
    def R_lens(self):
        """
        The radius of the lens.

        Returns
        -------
        double
            The radius of the lens.

        """

        return self._R_lens

    @property
    def R1(self):
        """
        The radius of curvature the left side of the lens. R1 is positive if
        the left side is convex, negative if it is concave.

        Returns
        -------
        double
            The radius of curvature the left side of the lens.

        """

        return self._R1
    @R1.setter
    def R1(self, new_R1):

        if -self.R_lens < new_R1 < self.R_lens:
            raise ValueError(f"R1 = {new_R1} is invalid")

        # Need to update R1 first as things like centre will also change
        self._R1 = new_R1

        p = self.get_current_params()
        p['left'] = True

        l_p = self._create_arc_param(**p)

        # Need to update arc centre, R and start/end
        self._left_arc.centre = l_p['centre']
        self._left_arc.R = l_p['R']
        self._left_arc.update_start_end(l_p['start'], l_p['end'])

    @property
    def R2(self):
        """
        The radius of curvature the right side of the lens. R2 is positive if
        the right side is convex, negative if it is concave.

        Returns
        -------
        double
            The radius of curvature the right side of the lens.

        """

        return self._R2
    @R2.setter
    def R2(self, new_R2):

        if -self.R_lens < new_R2 < self.R_lens:
            raise ValueError(f"R1 = {new_R2} is invalid")

        # Need to update R1 first as things like centre will also change
        self._R2 = new_R2

        p = self.get_current_params()
        p['left'] = False

        r_p = self._create_arc_param(**p)

        # Need to update arc centre, R and start/end
        self._left_arc.centre = r_p['centre']
        self._left_arc.R = r_p['R']
        self._left_arc.update_start_end(r_p['start'], r_p['end'])

    @property
    def d(self):
        """
        The distance between the end of one arc and the nearest end of the 
        other.

        Returns
        -------
        double
            The distance between the end of one arc and the nearest end of
            the other.

        """

        return self._d

    @property
    def n_in(self):
        """
        The refractive index inside the lens.

        Returns
        -------
        double
            The refractive index inside the lens.

        """

        return self._n_in
    @n_in.setter
    def n_in(self, new_n_in):
        """Setter for property n_in"""

        self._n_in = new_n_in

        p = self.get_current_params()

        # left & right arcs
        p['left'] = True
        ni, no = self._comp_arc_refr_ind(**p)

        self._left_arc.n_in = ni
        self._left_arc.n_out = no

        p['left'] = False
        ni, no = self._comp_arc_refr_ind(**p)

        self._right_arc.n_in = ni
        self._right_arc.n_out = no

        # Components defined anticlockwise, so n1 is inside
        # top and bottom planes
        self._bottom_plane.n1 = new_n_in
        self._top_plane.n1 = new_n_in

    @property
    def n_out(self):
        """
        The refractive index outside the lens.

        Returns
        -------
        double
            The refractive index outside the lens.

        """
        
        return self._n_out
    @n_out.setter
    def n_out(self, new_n_out):
        """Setter for property n_out"""

        self._n_out = new_n_out

        p = self.get_current_params()

        # left & right arcs
        p['left'] = True
        ni, no = self._comp_arc_refr_ind(**p)

        self._left_arc.n_in = ni
        self._left_arc.n_out = no

        p['left'] = False
        ni, no = self._comp_arc_refr_ind(**p)

        self._right_arc.n_in = ni
        self._right_arc.n_out = no

        # Components defined anticlockwise, so n2 is outside
        # top and bottom planes
        self._bottom_plane.n2 = new_n_out
        self._top_plane.n2 = new_n_out


# class PyBiConvexLens

class PyBiConvexLens(PyLens):
    """A class to represent a Bi-convex lens"""

    def __init__(self, lens_centre, R_lens, R1, R2, d, n_in, n_out=1.0) -> None:
        """
        Creates an instance of PyBiConvexLens.

        Parameters
        ----------
        lens_centre : numpy.ndarray
            A numpy array of shape (2,) that gives the centre of the lens.
        R_lens : double
            The radius of the lens.
        R1 : double
            The radius of curvature of the left side of the lens. If R1 is
            positive this arc of the lens is convex, if it is negative it 
            is concave. R1 must statisfy R1 >= R_lens.
        R2 : double
            The radius of curvature of the right side of the lens. If R2 is
            positive this arc of the lens is convex, if it is negative it 
            is concave. R2 must statisfy R2 >= R_lens.
        d : double
            The distance between the end of one arc and the nearest end
            of the other. See figure in LaTeX docs.
        n_in : double
            The refractive index of the interior of the lens.
        n_out : double, optional
            The refractive index outside of the lens. The default is 1.0.

        Returns
        -------
        None.

        """

        assert R1 >= R_lens, f"R1 = {R1} was less than radius of lens R_lens = {R_lens}"
        assert R2 >= R_lens, f"R2 = {R2} was less than radius of lens R_lens = {R_lens}"

        super().__init__(lens_centre, R_lens, R1, R2, d, n_in, n_out)
