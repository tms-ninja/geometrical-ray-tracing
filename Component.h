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
	virtual double test_hit(Ray &ry) const = 0;
	virtual void hit(Ray &ry, int n = 1) const = 0;

	// Printing
	friend std::ostream& operator<< (std::ostream& os, const Component& b);
	virtual void print(std::ostream& os) const = 0;

	// Helper functions

	// Rotates the coordinates by alpha (rotates axis, not point)
	arr rotate(const arr &r, const double theta) const;

	// Computes time for a ray starting at r and travelling in the direction v to reach pos
	// Assumes intersection
	double compute_t(const arr &r, const arr &v, const arr &pos) const;

	// Absolute comparison between v1 and v2
	bool is_close(double v1, double v2, double atol = 1e-8) const
	{
		return (abs(v1 - v2) < atol);
	}
};

