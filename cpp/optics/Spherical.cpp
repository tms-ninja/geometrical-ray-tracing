#include "Spherical.h"

Spherical::Spherical(arr centre, double R, double start, double end)
	: centre(centre), R(R), start(start), end(end)
{
}

double Spherical::test_hit(Ray* ry) const
{
	double t, tp;

	std::tie(t, tp) = solve(ry->pos.back(), ry->v);

	return t;
}

std::tuple<double, double> Spherical::solve(const arr & r, const arr & v) const
{
	double dx{ r[0] - centre[0] }, dy{ r[1] - centre[1] };
	double delta{ dy*v[0] - dx * v[1] };

	// Discriminant of quadratic
	double disc;

	disc = delta * delta * (v[1] * v[1] - 1) + (v[0] * R)*(v[0] * R);

	// Check if there are any solutions
	if (disc < 0.0)
		return { -1.0, 0.0 };

	disc = sqrt(disc);

	double uvSol[2];

	uvSol[0] = (-v[1] * delta + disc) / R;
	uvSol[1] = (-v[1] * delta - disc) / R;

	bool found_valid_sol{ false };
	double best_t, best_tp;

	double tpSol[4];
	size_t tpSol_MAX{ start < 0.0 ? 4U : 2U };  

	for (double &u : uvSol)
	{
		if (u >= -1 && u <= 1)
		{
			tpSol[0] = acos(u);
			tpSol[1] = 2 * M_PI - acos(u);

			if (start < 0)
			{
				tpSol[2] = 2 * M_PI - acos(u);
				tpSol[3] = -acos(u);
			}

			// Check if any of the tp correspond to physical solutions
			for (std::size_t ind = 0; ind < tpSol_MAX; ++ind)
			{
				const double &tp{ tpSol[ind] };
				
				if (tp >= start && tp <= end)  // Check it hits exisitng part of component
				{
					// u is equal to cos(tp)
					const arr p = { centre[0] + R * u, centre[1] + R * sin(tp) };
					const double t = compute_t(r, v, p);

					// Check t is in the furture and not where we are starting from
					if (t > 0.0 && !is_close(t, 0.0))
					{

						if (is_close(r[0] + v[0] * t, p[0]) && is_close(r[1] + v[1] * t, p[1]))  // Check it is solution for x and y components
						{
							if (found_valid_sol && t < best_t)
							{
								best_t = t;
								best_tp = tp;
							}
							else if (found_valid_sol == false)
							{
								found_valid_sol = true;
								best_t = t;
								best_tp = tp;
							}
						}
					}
				}
							
			}
		}
	}

	// return valid solution if we have one
	if (found_valid_sol)
		return { best_t, best_tp };

	return { -1.0, 0.0 };
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
