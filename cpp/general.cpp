#pragma once
#include "general.h"

// Determines which component, if any, is the next one to interact. returns -1 if none do
std::pair<size_t, bool> next_component(const std::vector<double> &t)
{
	bool found{ false };
	double best_t{};
	size_t best_ind{};

	for (std::size_t tInd = 0; tInd < t.size(); ++tInd)
	{
		if (!found && t[tInd] > 0)  // Not found one that is positive yet, choose first positive
		{
			best_t = t[tInd];
			best_ind = tInd;
			found = true;
		}
		else if (t[tInd] > 0 && t[tInd] < best_t)  // value is positive and less than current best
		{
			best_t = t[tInd];
			best_ind = tInd;
		}
	}

	if (found)
		return { best_ind, true };

	return { 0, false };
}
