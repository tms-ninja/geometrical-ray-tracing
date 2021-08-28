#include "Plane.h"

Plane::Plane(arr start, arr end)
{
	Plane::start = start;
	Plane::end = end;

	// Compute unit vector pointing from start to end
	double mag{ hypot(end[0] - start[0], end[1] - start[1]) };

	Plane::D = { (end[0] - start[0]) / mag, (end[1] - start[1]) / mag };
}

double Plane::test_hit(Ray* ry) const
{
	double t{}, tp{};

	std::tie(t, tp) = solve(ry->pos.back(), ry->v);

	if (tp < 0 || tp > 1 || is_close(t, 0.0))
		return -1.0;

	return t;
}

void Plane::print(std::ostream & os) const
{
	for (int i = 0; i < 2; ++i)
		os << start[i] << '\t' << end[i] << '\n';
}

std::tuple<double, double> Plane::solve(const arr &r, const arr &v) const
{
	const std::tuple<double, double> retError = { -1.0, 0.0 };  // If there 

	double bottom{ v[0] * (start[1] - end[1]) + v[1] * (end[0] - start[0]) };  // denominator of t expression

	if (is_close(bottom, 0))  // Check lines aren't parallel
		return retError;

	double t{ r[0] * (end[1] - start[1]) - start[0] * end[1] + end[0] * start[1] + r[1] * (start[0] - end[0]) };

	t /= bottom;

	double tp{ v[1] * (start[0] - r[0]) - v[0] * (start[1] - r[1]) };

	tp /= -bottom;

	return { t, tp };
}

