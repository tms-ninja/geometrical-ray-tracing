#include "Mirror_Plane.h"

Mirror_Plane::Mirror_Plane(arr start, arr end)
	: Plane(start, end)
{
}

void Mirror_Plane::hit(Ray* ry, int n) const
{
	arr newPos;

	double t, tp;
	arr &r = ry->pos.back();
	arr &v = ry->v;

	std::tie(t, tp) = solve(r, v);

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	ry->pos.push_back(newPos);

	// Compute new direction
	double v_dot_D{ v[0] * D[0] + v[1] * D[1] };

	for (int i = 0; i < 2; ++i)
		v[i] = 2*v_dot_D*D[i] - v[i];
}

Mirror_Plane* Mirror_Plane::clone() const
{
	return new Mirror_Plane{ *this };
}
