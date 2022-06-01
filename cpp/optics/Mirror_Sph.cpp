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


#include "Mirror_Sph.h"

Mirror_Sph::Mirror_Sph(arr centre, double R, double start, double end)
	: Spherical(centre, R, start, end)
{
}

void Mirror_Sph::hit(Ray* ry, int n) const
{
	arr &r{ ry->pos.back() };
	arr &v{ ry->v };

	double t;

	t = solve(r, v);

	arr newPos;

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	ry->pos.push_back(newPos);

	// Compute new direction
	arr n_vec = { (newPos[0] - centre[0]) / R, (newPos[1] - centre[1]) / R };

	double v_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };

	for (int i = 0; i < 2; ++i)
		v[i] -= 2 * v_dot_n * n_vec[i];

}

Mirror_Sph * Mirror_Sph::clone() const
{
	return new Mirror_Sph{ *this };
}
