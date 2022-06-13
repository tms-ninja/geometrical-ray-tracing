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


// Abstract class that describes a planar surface
//
#pragma once
#include "Component.h"
#include <tuple>

class Plane :
	public Component
{
protected:
	arr start;  // Start and end positions of plane
	arr end;
	arr D;      // Unit vector pointing from start to end

public:
	Plane(arr start, arr end);

	// function for testing for hits
	virtual double test_hit(const Ray* ry) const override;

	// getter/setter methods for start & end
	// getter methods shouldn't be used to modify start end values
	arr& get_start();
	void set_start(const arr& start);

	arr& get_end();
	void set_end(const arr& end);

	// Printing
	virtual void print(std::ostream& os) const override;

	// helper functions
	// Solve for point of intersection, returns (t, tp)
	std::tuple<double, double> solve(const arr &r, const arr &v) const;
};

