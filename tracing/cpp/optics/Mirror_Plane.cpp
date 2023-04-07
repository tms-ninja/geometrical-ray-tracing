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


#include "Mirror_Plane.h"

namespace optics
{
	Mirror_Plane::Mirror_Plane(arr start, arr end)
		: Plane(start, end)
	{
	}

	void Mirror_Plane::hit(Ray* ry, int n) const
	{
		double t;
		arr& r = ry->pos.back();
		arr& v = ry->v;

		std::tie(t, std::ignore) = solve(r, v);

		// compute new position of ray
		arr newPos = compute_new_pos(*ry, t);
		ry->pos.push_back(newPos);

		// perform the change of direction
		reflect_ray(*ry, n_vec);
	}

	Mirror_Plane* Mirror_Plane::clone() const
	{
		return new Mirror_Plane{ *this };
	}
}
