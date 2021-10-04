#pragma once
#define _USE_MATH_DEFINES
#include <cmath>
#include "general.h"
#include "Ray.h"

class Component
{
public:

	// Virtual destructor as we expect to detroy instances polymorphically
	virtual ~Component() = default;
	
	// Methods for testing whether a ray hits the component and performing the hit
	// Pure virtual functions as class shouldn't be initiated
	virtual double test_hit(Ray* ry) const = 0;
	virtual void hit(Ray* ry, int n = 1) const = 0;

	// CLone method that returns a copy of the component
	virtual Component* clone() const = 0;

	// Printing
	friend std::ostream& operator<< (std::ostream& os, const Component& b);
	virtual void print(std::ostream& os) const = 0;

};

