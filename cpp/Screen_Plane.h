#pragma once
#include "Plane.h"
class Screen_Plane :
	public Plane
{
public:
	
	Screen_Plane(arr start, arr end);
	
	// Hit function
	virtual void hit(Ray* ry, int n) const override;
};

