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
from libcpp.vector cimport vector
from libcpp.memory cimport shared_ptr
from libcpp cimport bool

# Typedefs used

cdef extern from "<array>" namespace "std" nogil:
    cdef cppclass arr "std::array<double, 2>":
        arr() except+
        double& operator[](size_t)
        double* data()
        size_t size()


ctypedef vector[shared_ptr[Component]] comp_list

# Ray definitions

cdef extern from "Ray.cpp":
    pass
    
cdef extern from "Ray.h" namespace "optics":
    cdef cppclass Ray:
        Ray(arr, arr)
        vector[arr] pos
        arr v

        void reset(arr)
        void reset(arr, arr)

cdef extern from "general.cpp":
    pass

cdef extern from "general.h" namespace "optics":
    pass


cdef extern from "trace_func.cpp":
    pass

cdef extern from "trace_func.h" namespace "optics":
    void trace(vector[Component*]&, vector[Ray*] &, int, bool)


# Components

cdef extern from "Component.cpp":
    pass
    
cdef extern from "Component.h" namespace "optics":
    cdef cppclass Component:
        pass


# Planar components

cdef extern from "Plane.cpp":
    pass
    
cdef extern from "Plane.h" namespace "optics":
    cdef cppclass Plane(Component):
        double test_hit(Ray*)
        
        arr& get_start()
        void set_start(arr&)

        arr& get_end()
        void set_end(arr&)



cdef extern from "Mirror_Plane.cpp":
    pass
    
cdef extern from "Mirror_Plane.h" namespace "optics":
    cdef cppclass Mirror_Plane(Plane):
        Mirror_Plane(arr, arr) except+
        void hit(Ray&, int)


cdef extern from "Refract_Plane.cpp":
    pass

cdef extern from "Refract_Plane.h" namespace "optics":
    cdef cppclass Refract_Plane(Plane):
        Refract_Plane(arr, arr, double, double) except+
        double n1, n2
        void hit(Ray&, int)

cdef extern from "Screen_Plane.cpp":
    pass

cdef extern from "Screen_Plane.h" namespace "optics":
    cdef cppclass Screen_Plane(Plane):
        Screen_Plane(arr, arr) except+
        void hit(Ray&, int)

# Spherical components

cdef extern from "Spherical.cpp":
    pass

cdef extern from "Spherical.h" namespace "optics":
    cdef cppclass Spherical(Component):
        arr centre
        double R
        double get_start()
        void set_start(double)
        double get_end()
        void set_end(double)
        double test_hit(Ray*)
        

cdef extern from "Mirror_Sph.cpp":
    pass

cdef extern from "Mirror_Sph.h" namespace "optics":
    cdef cppclass Mirror_Sph(Spherical):
        Mirror_Sph(arr, double, double, double)
        void hit(Ray*, int)

    
cdef extern from "Refract_Sph.cpp":
    pass

cdef extern from "Refract_Sph.h" namespace "optics":
    cdef cppclass Refract_Sph(Spherical):
        Refract_Sph(arr, double, double, double, double, double)
        double n1, n2
        void hit(Ray*, int)


# Complex component

cdef extern from "Complex_Component.cpp":
    pass

cdef extern from "Complex_Component.h" namespace "optics":  # Don't to explicity give constructor
    cdef cppclass Complex_Component:
        comp_list comps
        double test_hit(Ray*)
        void hit(Ray*, int)

