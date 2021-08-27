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

	// Compute new direction, first compute the angle of the plane
	double angle{ atan2(end[1] - start[1], end[0] - start[0]) };

	double c_theta{ cos(angle) }, s_theta{ sin(angle) };

	double new_v_x{ c_theta*v[0] + s_theta * v[1] };
	double new_v_y{ -s_theta * v[0] + c_theta * v[1] };

	new_v_y = -new_v_y;

	v[0] = c_theta * new_v_x - s_theta * new_v_y;
	v[1] = s_theta * new_v_x + c_theta * new_v_y;
}
