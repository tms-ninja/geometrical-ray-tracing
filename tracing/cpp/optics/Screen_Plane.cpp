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


#include "Screen_Plane.h"

namespace optics
{

	Screen_Plane::Screen_Plane(arr start, arr end)
		: Plane(start, end)
	{
	}

	void Screen_Plane::hit(Ray* ry, int n) const
	{
		arr newPos;

		double t{}, tp{};
		arr& r = ry->pos.back();
		arr& v = ry->v;

		std::tie(t, tp) = solve(r, v);

		// Compute new position
		for (int i = 0; i < 2; ++i)
			newPos[i] = (r[i] + v[i] * t);

		// Add collision point, no need to update v
		ry->pos.push_back(newPos);
		ry->continue_tracing = false;
	}

	Screen_Plane* Screen_Plane::clone() const
	{
		return new Screen_Plane{ *this };
	}

}
