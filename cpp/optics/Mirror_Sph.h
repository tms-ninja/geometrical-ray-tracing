#pragma once
#include "Spherical.h"

class Mirror_Sph :
	public Spherical
{
public:
	Mirror_Sph(arr centre, double R, double start, double end);

	virtual void hit(Ray* ry, int n = 1) const override;
};

