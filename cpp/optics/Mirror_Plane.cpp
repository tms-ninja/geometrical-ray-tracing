#include "Mirror_Plane.h"

Mirror_Plane::Mirror_Plane(arr start, arr end)
	: Plane(start, end)
{
}

void Mirror_Plane::hit(Ray* ry, int n) const
{
	arr newPos;
	arr newV;

	double t{}, tp{};
	arr &r = ry->pos.back();
	arr &v = ry->v;

	std::tie(t, tp) = solve(r, v);

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	// Compute new direction, first compute the angle of the plane
	double angle{ atan2(end[1] - start[1], end[0] - start[0]) };

	newV = rotate(v, angle);
	newV[1] = -newV[1];
	newV = rotate(newV, -angle);

	// Finally update
	ry->pos.push_back(newPos);
	ry->v = newV;
}
