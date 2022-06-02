// geometrical-ray-tracing: Program to perform geometrical ray tracing
// Copyright (C) 2022  Tom Spencer (tspencerprog@gmail.com)

// This file is part of geometrical-ray-tracing

// geometrical-ray-tracing is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

// Describes a ray
//
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

