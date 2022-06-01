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


#pragma once
#define _USE_MATH_DEFINES
#include <cmath>
#include "general.h"
#include "Ray.h"

class Component
{
public:

	// Virtual destructor as we expect to detroy instances polymorphically
	virtual ~Component() = default;
	
	// Methods for testing whether a ray hits the component and performing the hit
	// Pure virtual functions as class shouldn't be initiated
	virtual double test_hit(const Ray* ry) const = 0;
	virtual void hit(Ray* ry, int n = 1) const = 0;

	// CLone method that returns a copy of the component
	virtual Component* clone() const = 0;

	// Printing
	friend std::ostream& operator<< (std::ostream& os, const Component& b);
	virtual void print(std::ostream& os) const = 0;

};

