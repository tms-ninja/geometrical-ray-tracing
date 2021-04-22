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

	std::vector<double> uvSol;  // u and v solutions

	uvSol.push_back((-v[1] * delta + disc) / R);
	uvSol.push_back((-v[1] * delta - disc) / R);

	std::vector<double> tArr;  // Contains just the t solutions
	std::vector<std::tuple<double, double>> sol;

	for (double &u : uvSol)
	{
		if (u >= -1 && u <= 1)
		{
			std::vector<double> tpSol;

			tpSol.push_back(acos(u));
			tpSol.push_back(2 * M_PI - acos(u));

			if (start < 0)
			{
				tpSol.push_back(2 * M_PI - acos(u));
				tpSol.push_back(-acos(u));
			}

			// Compute the positions of intersections and their times
			std::vector<arr> pos;
			std::vector<double> tSol;

			for (double &tp : tpSol)
			{
				arr temp;

				temp[0] = centre[0] + R * cos(tp);
				temp[1] = centre[1] + R * sin(tp);

				pos.push_back(temp);

				tSol.push_back(compute_t(r, v, temp));
			}
				
			for (std::size_t ind = 0; ind < tpSol.size(); ++ind)
			{
				const double  &t{ tSol[ind] };
				const double &tp{ tpSol[ind] };
				const arr &p{ pos[ind] };

				// First check t is in the furture and not where we are starting from
				if (t > 0.0 && !is_close(t, 0.0))
				{
					if (tp >= start && tp <= end)  // Check it hits exisitng part of component
					{
						if (is_close(r[0] + v[0] * t, p[0]) && is_close(r[1] + v[1] * t, p[1]))  // Check it is solution for x and y components
						{
							sol.push_back({ t, tp });
							tArr.push_back(t);  // add t value so we can work out next next interacting solution
						}
					}
				}
							
			}

		}
	}

	// sol now contains 0, 1, or two solutions, need to find one with smallest t
	switch (sol.size())
	{
	case 0:
		return { -1.0, 0.0 };
	case 1:
		return sol[0];
	default:
		size_t ind;

		std::tie(ind, std::ignore) = next_component(tArr);

		return sol[ind];
	}
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
