#pragma once
#include <array>
#include <vector>
#include <iostream>
#include "general.h"

class Ray
{
public:
	std::vector<arr> pos;
	arr v;
	bool continue_tracing;

	Ray(arr init, arr v);

	friend std::ostream& operator<<(std::ostream& os, const Ray& ry);

	// Resets the Ray to only the first point in pos with specified new direction
	// and resets the start position if specified
	void reset(const arr& new_v);
	void reset(const arr& new_v, const arr& new_start);
};

