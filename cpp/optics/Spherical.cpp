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


#include "Spherical.h"

Spherical::Spherical(arr centre, double R, double start, double end)
	: centre{ centre }, R{ R }, start{ start }, end{ end }
{
	set_start(start);
	set_end(end);
}

double Spherical::test_hit(const Ray* ry) const
{
	return solve(ry->pos.back(), ry->v);
}

bool Spherical::in_range(arr & p) const
{
	arr temp{ p[0] - centre[0], p[1] - centre[1] };

	arr p_rot;

	p_rot[0] = cos_start * temp[0] + sin_start * temp[1];
	p_rot[1] = -sin_start * temp[0] + cos_start * temp[1];


	// end point is above rotated y axis
	if (end_p[1] >= 0.0)
	{
		return  p_rot[1] >= 0.0 && end_p[0] <= p_rot[0];
	}

	// now know y of end point < 0.0
	// check if rotated p is above rotated y axis, all good
	if (p_rot[1] >= 0.0)
		return true;

	// both below rotated y axis
	return p_rot[0] <= end_p[0];
}

double Spherical::solve(const arr & r, const arr & v) const
{
	double dx{ r[0] - centre[0] }, dy{ r[1] - centre[1] };
	double gamma{ dx*v[0] + dy * v[1] };
	double disc;  // discriminant

	disc = gamma * gamma + R * R - dx * dx - dy * dy;

	// No intersections
	if (disc < 0.0)
		return infinity;

	double t_vals[2];

	t_vals[0] = -gamma + std::sqrt(disc);
	t_vals[1] = -gamma - std::sqrt(disc);

	bool found_sol{ false };
	double best_t;
	arr pos;

	for (double t : t_vals)
	{
		// Check t is in the future, it's better than the current time and isn't where we are starting from
		if (t > 0.0 && (!found_sol || t < best_t) && !is_close(t, 0.0))
		{
			pos = { r[0] + v[0] * t, r[1] + v[1] * t };

			// Avoid call to atan2() as we don't need tp, just if it's in range
			if (in_range(pos))
			{
				found_sol = true;
				best_t = t;
			}
		}
	}

	if (found_sol)
		return best_t;

	return infinity;
}

double Spherical::get_start()
{
	return start;
}

void Spherical::set_start(double new_start)
{
	start = new_start;

	cos_start = std::cos(start);
	sin_start = std::sin(start);

	end_p = { R * std::cos(end), R * std::sin(end) };
	end_p = rotate(end_p, start);
}

double Spherical::get_end()
{
	return end;
}

void Spherical::set_end(double new_end)
{
	end = new_end;

	end_p = { R * std::cos(end), R * std::sin(end) };
	end_p = rotate(end_p, start);
}

void Spherical::print(std::ostream & os) const
{
	int N{ 100 };

	for (int i = 0; i < N - 1; ++i)  // x values
	{
		double tp;  // Compute t' 

		tp = start + (end - start) * static_cast<double>(i) / static_cast<double>(N);

		os << centre[0] + R * std::cos(tp) << '\t';
	}

	// print final x value
	os << centre[0] + R * std::cos(end) << '\n';

	for (int i = 0; i < N - 1; ++i)  // y values
	{
		double tp;  // Compute t' 

		tp = start + (end - start) * static_cast<double>(i) / static_cast<double>(N);

		os << centre[1] + R * std::sin(tp) << '\t';
	}

	// print final x value
	os << centre[1] + R * std::sin(end) << '\n';

}
