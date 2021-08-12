# ray-tracing-cython
 Cython interface to ray-tracing. It performs 2d geometrical ray tracing through a system of optical components such as mirrors and lenses. It contains four basic components, namely:
 - Plane mirror
 - Planar boundary at which refraction occurs
 - Mirror in the shape of a circular arc
 - Circular arc boundary at which refraction occurs

It also allows for so-called complex components such as lenses that are composed of pre-defined sub-components. These can be defined within Python without needing to write any C++/Cython, so long as they are ulitimately only composed of the four elements above. 
