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

	arr newPos;

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	ry->pos.push_back(newPos);

	// Now compute new direction
	double ni, nf;
	arr n_vec = { (newPos[0] - centre[0]) / R, (newPos[1] - centre[1]) / R };  // normal vector is radial vector
	arr D = { n_vec[1], -n_vec[0] };  // Consistent with definitions of D & n for a plane

	double vi_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };

	if (vi_dot_n > 0.0)
	{
		ni = n2;
		nf = n1;
	}
	else
	{
		ni = n1;
		nf = n2;
	}

	double gamma{ (n_vec[0] * v[1] - n_vec[1] * v[0])*ni / nf };
	double disc{ 1 - gamma * gamma };

	// If discriminant is less than zero, we have reflection instead of refraction
	if (disc < 0.0)
	{
		v[0] -= 2 * vi_dot_n*n_vec[0];
		v[1] -= 2 * vi_dot_n*n_vec[1];

		return;
	}

	// we are performing refraction
	disc = std::sqrt(disc);

	// Either side of +/- of resulting speeds
	double disc_term[2];

	disc_term[0] = n_vec[0] * disc;
	disc_term[1] = n_vec[1] * disc;

	double vi_dot_D{ v[0] * D[0] + v[1] * D[1] };

	v[0] = -n_vec[1] * gamma + disc_term[0];
	v[1] = n_vec[0] * gamma + disc_term[1];

	double vf_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };
	double vf_dot_D{ v[0] * D[0] + v[1] * D[1] };


	if (std::signbit(vi_dot_n) != std::signbit(vf_dot_n) || std::signbit(vi_dot_D) != std::signbit(vf_dot_D))
	{
		v[0] -= 2 * disc_term[0];
		v[1] -= 2 * disc_term[1];
	}
}

Refract_Sph * Refract_Sph::clone() const
{
	return new Refract_Sph{ *this };
}
