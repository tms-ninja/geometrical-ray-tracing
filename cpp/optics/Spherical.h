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

	virtual double test_hit(const Ray* ry) const override;

	// helper functions
	bool in_range(arr& p) const;

	double solve(const arr &r, const arr &v) const;

	double get_start();

	void set_start(double new_start);

	double get_end();

	void set_end(double new_end);

	virtual void print(std::ostream& os) const;
};

