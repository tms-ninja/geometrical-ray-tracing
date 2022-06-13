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


#include "Plane.h"

Plane::Plane(arr start, arr end)
{
	Plane::start = start;
	Plane::end = end;

	// Compute unit vector pointing from start to end
	double mag{ std::hypot(end[0] - start[0], end[1] - start[1]) };

	Plane::D = { (end[0] - start[0]) / mag, (end[1] - start[1]) / mag };
}

double Plane::test_hit(const Ray* ry) const
{
	double t, tp;

	std::tie(t, tp) = solve(ry->pos.back(), ry->v);

	return t;
}

arr& Plane::get_start()
{
	return this->start;
}

void Plane::set_start(const arr& start)
{
	this->start = start;

	double mag{ std::hypot(end[0] - start[0], end[1] - start[1]) };

	D = { (end[0] - start[0]) / mag, (end[1] - start[1]) / mag };
}

arr& Plane::get_end()
{
	return this->end;
}

void Plane::set_end(const arr& end)
{
	this->end = end;

	double mag{ std::hypot(end[0] - start[0], end[1] - start[1]) };

	D = { (end[0] - start[0]) / mag, (end[1] - start[1]) / mag };
}

void Plane::print(std::ostream & os) const
{
	for (int i = 0; i < 2; ++i)
		os << start[i] << '\t' << end[i] << '\n';
}

std::tuple<double, double> Plane::solve(const arr &r, const arr &v) const
{
	double bottom{ v[0] * (start[1] - end[1]) + v[1] * (end[0] - start[0]) };  // denominator of t expression

	if (is_close(bottom, 0.0))  // Check lines aren't parallel
		return { infinity, 0.0 };

	double t{ r[0] * (end[1] - start[1]) - start[0] * end[1] + end[0] * start[1] + r[1] * (start[0] - end[0]) };

	t /= bottom;

	double tp{ v[1] * (start[0] - r[0]) - v[0] * (start[1] - r[1]) };

	tp /= -bottom;

	if (tp < 0 || tp > 1 || t < 0.0 || is_close(t, 0.0))
		return { infinity, 0.0 };

	return { t, tp };
}

