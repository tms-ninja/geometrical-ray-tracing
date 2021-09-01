#include "Mirror_Sph.h"

Mirror_Sph::Mirror_Sph(arr centre, double R, double start, double end)
	: Spherical(centre, R, start, end)
{
}

void Mirror_Sph::hit(Ray* ry, int n) const
{
	arr &r{ ry->pos.back() };
	arr &v{ ry->v };

	double t, tp;

	std::tie(t, tp) = solve(r, v);

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
