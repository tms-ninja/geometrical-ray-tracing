#pragma once
#include "Component.h"


class Spherical :
	public Component
{
protected:
	arr end_p;  // Rotated end point
	double cos_start, sin_start;  // cos and sin of start
	double  start, end;

public:
	arr centre;

	double R;

	Spherical(arr centre, double R, double start = 0.0, double end = 0.0);

	virtual double test_hit(Ray* ry) const override;

	// helper functions
	bool in_range(arr& p) const;

	double solve(const arr &r, const arr &v) const;

	double get_start();

	void set_start(double new_start);

	double get_end();

	void set_end(double new_end);

	virtual void print(std::ostream& os) const;
};

