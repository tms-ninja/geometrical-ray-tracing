#pragma once
#include "Component.h"
#include <tuple>

class Plane :
	public Component
{
public:
	arr start;  // Start and end positions of plane
	arr end;

	Plane(arr start, arr end);

	// function for testing for hits
	virtual double test_hit(Ray* ry) const override;

	// Printing
	virtual void print(std::ostream& os) const override;

	// helper functions
	// Solve for point of intersection, returns (t, tp)
	std::tuple<double, double> solve(const arr &r, const arr &v) const;
};

