#include "Spherical.h"

Spherical::Spherical(arr centre, double R, double start, double end)
	: centre(centre), R(R), start(start), end(end)
{
}

double Spherical::test_hit(Ray* ry) const
{
	return solve(ry->pos.back(), ry->v);
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

			double tp{ atan2(pos[1] - centre[1], pos[0] - centre[0]) };

			// atan2() returns in range -pi to pi
			if (tp < 0.0 && start >= 0.0)
				tp += 2 * M_PI;

			if (start <= tp && tp <= end)  // Check it hits exisitng part of component
			{
				found_sol = true;
				best_t = t;
			}
		}
	}

	if (found_sol)
		return best_t;

	return -1.0 ;
}

void Spherical::print(std::ostream & os) const
{
	int N{ 100 };

	for (int i = 0; i < N-1; ++i)  // x values
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
