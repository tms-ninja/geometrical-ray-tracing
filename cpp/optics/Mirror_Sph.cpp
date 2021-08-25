#include "Mirror_Sph.h"

Mirror_Sph::Mirror_Sph(arr centre, double R, double start, double end)
	:	Spherical(centre, R, start, end)
{
}

void Mirror_Sph::hit(Ray* ry, int n) const
{
	arr &r{ ry->pos.back() };
	arr &v{ ry->v };

	double t, tp;

	std::tie(t, tp) = solve(r, v);

	arr newPos;
	arr newV;

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	double angle{ tp - M_PI_2 };

	newV = rotate(v, angle);
	newV[1] = -newV[1];
	newV = rotate(newV, -angle);

	// Finally update
	ry->pos.push_back(newPos);
	ry->v = newV;
}
