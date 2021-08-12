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
};

