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

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	ry->pos.push_back(newPos);

	// Compute new direction
	double angle{ tp - M_PI_2 };

	double c_theta{ cos(angle) }, s_theta{ sin(angle) };

	double new_v_x{ c_theta*v[0] + s_theta*v[1] };
	double new_v_y{ -s_theta*v[0] + c_theta*v[1] };

	new_v_y = -new_v_y;

	v[0] = c_theta * new_v_x - s_theta * new_v_y;
	v[1] = s_theta * new_v_x + c_theta * new_v_y;
}
