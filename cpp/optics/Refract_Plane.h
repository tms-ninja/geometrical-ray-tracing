#pragma once
#include "Plane.h"
class Refract_Plane :
	public Plane
{
public:
	double n1, n2;

	Refract_Plane(arr start, arr end, double n1 = 1.0, double n2 = 1.0);

	// Hit function
	virtual void hit(Ray* ry, int n) const override;

	virtual Refract_Plane* clone() const override;
};

