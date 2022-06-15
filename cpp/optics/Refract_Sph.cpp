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


#include "Refract_Sph.h"

Refract_Sph::Refract_Sph(arr centre, double R, double start, double end, double n1, double n2)
	:	Spherical(centre, R, start, end), n1(n1), n2(n2)
{
}

void Refract_Sph::hit(Ray* ry, int n) const
{
	arr &r{ ry->pos.back() };
	arr &v{ ry->v };

	double t;

	t = solve(r, v);

	// Compute new position
	arr newPos = compute_new_pos(*ry, t);
	ry->pos.push_back(newPos);

	// Now compute new direction
	arr n_vec = { (newPos[0] - centre[0]) / R, (newPos[1] - centre[1]) / R };  // normal vector is radial vector

	refract_ray(*ry, n_vec, n1, n2);
}

Refract_Sph * Refract_Sph::clone() const
{
	return new Refract_Sph{ *this };
}
