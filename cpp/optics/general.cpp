#pragma once
#include "general.h"

// Determines which component, if any, is the next one to interact
std::pair<size_t, bool> next_component(const std::vector<double> &t)
{
	double best_t{ infinity };
	size_t best_ind;

	for (std::size_t tInd = 0; tInd < t.size(); ++tInd)
	{
		if (t[tInd] < best_t)
		{
			best_t = t[tInd];
			best_ind = tInd;
		}
	}

	if (best_t != infinity)
		return { best_ind, true };

	return { 0, false };
}

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
