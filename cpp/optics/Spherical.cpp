#include "Spherical.h"

Spherical::Spherical(arr centre, double R, double start, double end)
	: centre(centre), R(R), start(start), end(end)
{
	cos_start = cos(start);
	sin_start = sin(start);

	end_p = { centre[0] + R * cos(end), centre[1] + R * sin(end) };
	end_p = rotate(end_p, start);
}

double Spherical::test_hit(Ray* ry) const
{
	return solve(ry->pos.back(), ry->v);
}

bool Spherical::in_range(arr & p) const
{
	// Determines if the point p satisfies start <= atan2(p) <= end
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
		return -1.0;

	double t_vals[2];

	t_vals[0] = -gamma + sqrt(disc);
	t_vals[1] = -gamma - sqrt(disc);

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

	return -1.0;
}

void Spherical::print(std::ostream & os) const
{
	int N{ 100 };

	for (int i = 0; i < N - 1; ++i)  // x values
	{
		double tp;  // Compute t' 

		tp = start + (end - start) * static_cast<double>(i) / static_cast<double>(N);

		os << centre[0] + R * cos(tp) << '\t';
	}

	// print final x value
	os << centre[0] + R * cos(end) << '\n';

	for (int i = 0; i < N - 1; ++i)  // y values
	{
		double tp;  // Compute t' 

		tp = start + (end - start) * static_cast<double>(i) / static_cast<double>(N);

		os << centre[1] + R * sin(tp) << '\t';
	}

	// print final x value
	os << centre[1] + R * sin(end) << '\n';

}
