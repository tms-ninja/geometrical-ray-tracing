#include "Screen_Plane.h"

Screen_Plane::Screen_Plane(arr start, arr end)
	: Plane(start, end)
{
}

void Screen_Plane::hit(Ray* ry, int n) const
{
	arr newPos;

	double t{}, tp{};
	arr &r = ry->pos.back();
	arr &v = ry->v;

	std::tie(t, tp) = solve(r, v);

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	// Add collision point, no need to update v
	ry->pos.push_back(newPos);
}
