// Class for describing a triangluar prism
// 
#pragma once
#include "Complex_Component.h"
#include "Refract_Plane.h"

class Prism :
	public Complex_Component
{
public:
	Prism(arr p1, arr p2, arr p3, double n_inside, double n_outside);
};

