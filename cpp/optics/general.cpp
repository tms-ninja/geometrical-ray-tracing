#pragma once
#include "general.h"

// Determines which component, if any, is the next one to interact
//std::pair<size_t, bool> next_component(const std::vector<double> &t)
//{
//	double best_t{ infinity };
//	size_t best_ind;
//
//	for (std::size_t tInd = 0; tInd < t.size(); ++tInd)
//	{
//		if (t[tInd] < best_t)
//		{
//			best_t = t[tInd];
//			best_ind = tInd;
//		}
//	}
//
//	if (best_t != infinity)
//		return { best_ind, true };
//
//	return { 0, false };
//}



arr rotate(const arr &r, const double theta)
{
	double top{ cos(theta)*r[0] + sin(theta)*r[1] };
	double bottom{ -sin(theta)*r[0] + cos(theta)*r[1] };

	return { top, bottom };
}

bool is_close(double v1, double v2, double atol)
{
	return (abs(v1 - v2) < atol);
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
