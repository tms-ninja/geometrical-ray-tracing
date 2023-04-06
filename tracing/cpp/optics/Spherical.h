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


// Describes a surface in the shape of an arc
// Note setting the start/end angles except in the constructor is non-trivial,
// the relevant setting & getting methods should be used instead.
//
#pragma once
#include "Component.h"

namespace optics
{
	class Spherical :
		public Component
	{
	protected:
		// Rotated end point relative to centre of arc, rotated such that the 
		// start point lies on the positive x axis
		arr end_p;
		double cos_start, sin_start;  // cos and sin of start
		double start, end;

	public:
		arr centre;

		double R;

		Spherical(arr centre, double R, double start = 0.0, double end = 0.0);

		virtual double test_hit(const Ray* ry) const override;

		// helper functions

		// Determines if the point p satisfies start <= atan2(p) <= end
		bool in_range(arr& p) const;

		// Determines the time of interception of a ray with starting position
		// r and initial direction v with the arc. Returns infinity if no
		// interception occurs
		double solve(const arr& r, const arr& v) const;

		double get_start();

		void set_start(double new_start);

		double get_end();

		void set_end(double new_end);

		virtual void print(std::ostream& os) const;
	};
}
