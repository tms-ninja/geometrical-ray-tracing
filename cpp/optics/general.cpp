#pragma once
#include "general.h"


arr rotate(const arr &r, const double theta)
{
	double top{ cos(theta)*r[0] + sin(theta)*r[1] };
	double bottom{ -sin(theta)*r[0] + cos(theta)*r[1] };

	return { top, bottom };
}

void renorm_unit_vec(arr & v)
{
	double v_mag_sq, x, fact;

	v_mag_sq = v[0] * v[0] + v[1] * v[1];

	// using Taylor expansion for 1/sqrt(x) around x=1
	x = v_mag_sq - 1.0;

	fact = 1.0 - x / 2.0;//  +3.0*x*x / 8.0;

	v[0] *= fact;
	v[1] *= fact;
}
