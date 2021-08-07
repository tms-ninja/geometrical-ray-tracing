#pragma once
#include "Spherical.h"
class Refract_Sph :
	public Spherical
{
public:
	double n1, n2;

	Refract_Sph(arr centre, double R, double start = 0.0, double end = 0.0, double n1=1.0, double n2=1.0);

	virtual void hit(Ray* ry, int n = 1) const override;
};

