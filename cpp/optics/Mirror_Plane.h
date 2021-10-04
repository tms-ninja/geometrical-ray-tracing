#pragma once
#include "Plane.h"
class Mirror_Plane :
	public Plane
{
public:
	
	Mirror_Plane(arr start, arr end);
	
	// Hit function
	virtual void hit(Ray* ry, int n) const override;

	virtual Mirror_Plane* clone() const override;
};

