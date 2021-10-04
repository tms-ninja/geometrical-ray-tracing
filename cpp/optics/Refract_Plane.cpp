#include "Refract_Plane.h"

Refract_Plane::Refract_Plane(arr start, arr end, double n1, double n2)
	: Plane(start, end), n1(n1), n2(n2)
{
}

void Refract_Plane::hit(Ray* ry, int n) const
{
	arr newPos;
	arr &r = ry->pos.back();
	arr &v = ry->v;

	double t, tp;

	std::tie(t, tp) = solve(r, v);

	// Compute new position
	for (int i = 0; i < 2; ++i)
		newPos[i] = (r[i] + v[i] * t);

	ry->pos.push_back(newPos);

	// Now compute new direction, first determine order of refractive indices
	double ni, nf;
	arr n_vec = { -D[1], D[0] };  // normal vector

	double vi_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };

	if (vi_dot_n > 0.0)
	{
		ni = n2;
		nf = n1;
	}
	else
	{
		ni = n1;
		nf = n2;
	}

	double gamma{ (n_vec[0] * v[1] - n_vec[1] * v[0])*ni / nf };
	double disc{ 1 - gamma * gamma };

	// If discriminant is less than zero, we have reflection instead of refraction
	if (disc < 0.0)
	{
		v[0] -= 2 * vi_dot_n*n_vec[0];
		v[1] -= 2 * vi_dot_n*n_vec[1];

		return;
	}

	// we are performing refraction
	disc = sqrt(disc);

	// Either side of +/- of resulting speeds
	double disc_term[2];

	disc_term[0] = n_vec[0] * disc;
	disc_term[1] = n_vec[1] * disc;

	double vi_dot_D{ v[0] * D[0] + v[1] * D[1] };

	v[0] = -n_vec[1] * gamma + disc_term[0];
	v[1] = n_vec[0] * gamma + disc_term[1];

	double vf_dot_n{ v[0] * n_vec[0] + v[1] * n_vec[1] };
	double vf_dot_D{ v[0] * D[0] + v[1] * D[1] };


	if (signbit(vi_dot_n) != signbit(vf_dot_n) || signbit(vi_dot_D) != signbit(vf_dot_D))
	{
		v[0] -= 2 * disc_term[0];
		v[1] -= 2 * disc_term[1];
	}
}

Refract_Plane * Refract_Plane::clone() const
{
	return new Refract_Plane{ *this };
}

