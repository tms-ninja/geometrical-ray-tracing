#include "Prism.h"

Prism::Prism(arr p1, arr p2, arr p3, double n_inside, double n_outside)
{
	Prism::add(Refract_Plane(p1, p2, n_outside, n_inside));
	Prism::add(Refract_Plane(p2, p3, n_outside, n_inside));
	Prism::add(Refract_Plane(p3, p2, n_outside, n_inside));
}
