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
    
cdef extern from "Ray.h":
    cdef cppclass Ray:
        Ray(arr, arr)
        vector[arr] pos
        arr v

cdef extern from "general.cpp":
    pass

cdef extern from "general.h":
    pass


cdef extern from "trace_func.cpp":
    pass

cdef extern from "trace_func.h":
    void trace(vector[Component*]&, vector[Ray*] &, int, bool)


# Components

cdef extern from "Component.cpp":
    pass
    
cdef extern from "Component.h":
    cdef cppclass Component:
        pass


# Planar components

cdef extern from "Plane.cpp":
    pass
    
cdef extern from "Plane.h":
    cdef cppclass Plane(Component):
        arr start, end
        double test_hit(Ray*)


cdef extern from "Mirror_Plane.cpp":
    pass
    
cdef extern from "Mirror_Plane.h":
    cdef cppclass Mirror_Plane(Plane):
        Mirror_Plane(arr, arr) except+
        void hit(Ray&, int)


cdef extern from "Refract_Plane.cpp":
    pass

cdef extern from "Refract_Plane.h":
    cdef cppclass Refract_Plane(Plane):
        Refract_Plane(arr, arr, double, double) except+
        double n1, n2
        void hit(Ray&, int)

cdef extern from "Screen_Plane.cpp":
    pass

cdef extern from "Screen_Plane.h":
    cdef cppclass Screen_Plane(Plane):
        Screen_Plane(arr, arr) except+
        void hit(Ray&, int)

# Spherical components

cdef extern from "Spherical.cpp":
    pass

cdef extern from "Spherical.h":
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

cdef extern from "Mirror_Sph.h":
    cdef cppclass Mirror_Sph(Spherical):
        Mirror_Sph(arr, double, double, double)
        void hit(Ray*, int)

    
cdef extern from "Refract_Sph.cpp":
    pass

cdef extern from "Refract_Sph.h":
    cdef cppclass Refract_Sph(Spherical):
        Refract_Sph(arr, double, double, double, double, double)
        double n1, n2
        void hit(Ray*, int)


# Complex component

cdef extern from "Complex_Component.cpp":
    pass

cdef extern from "Complex_Component.h":  # Don't to explicity give constructor
    cdef cppclass Complex_Component:
        comp_list comps
        double test_hit(Ray*)
        void hit(Ray*, int)

