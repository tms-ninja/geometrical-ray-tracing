#pragma once
#include "Component.h"


class Spherical :
	public Component
{
public:
	arr centre;
	double R, start, end;

	Spherical(arr centre, double R, double start = 0.0, double end = 0.0);

	virtual double test_hit(Ray* ry) const override;

	// helper functions
	std::tuple<double, double> solve(const arr &r, const arr &v) const;

	virtual void print(std::ostream& os) const;
};

